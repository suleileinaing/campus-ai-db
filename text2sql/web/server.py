"""경희 Campus AI 웹 데모 서버 (표준 라이브러리만 사용).

  python -m text2sql.web.server            # http://127.0.0.1:8000
  python -m text2sql.web.server --port 8080 --no-rag

API
  POST /api/login   {student_id, password}      → {token, name, expires_in}
  POST /api/logout  (Authorization: Bearer ...)
  POST /api/chat    {question, conversation_id} → {answer, route, kind, table, sources, personal}
  POST /api/reset   {conversation_id}
  GET  /api/syllabus?code=CSE406&section=07     → 강의계획서 원문(공개 정보)

- 조회 결과 행은 브라우저로만 보내고 LLM 에는 보내지 않는다(파이프라인 규칙 그대로).
- 로그인은 데모용이다. DB 에 비밀번호가 없어서 학번이 있으면 통과시킨다(실서비스는 학교 인증 필요).
- 세션이 만료되면 401 {expired: true} 를 돌려주고, 그 세션의 대화 기록도 지운다.
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import secrets
import sqlite3
import threading
import time
import traceback
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from ..answer import column_label, format_value
from ..config import CURRENT_TERM, DATABASE_PATH, Settings
from ..executor import PERSONAL_TABLES, SQLExecutor
from ..pipeline import Text2SQL
from ..prompt import PromptBuilder

STATIC_DIR = Path(__file__).resolve().parent / "static"
SESSION_SEC = 30 * 60
MAX_HISTORY_TURNS = 6  # 앞 대화는 최근 6턴만 기억
MAX_TABLE_ROWS = 50
# 공개 배포 시 크레딧 보호: 하루(서버 시간 기준) 질문 수 한도. 0 이면 제한 없음.
DAILY_LIMIT = int(os.environ.get("WEB_DAILY_LIMIT", "300"))   # 전체 합계
IP_DAILY_LIMIT = int(os.environ.get("WEB_IP_DAILY_LIMIT", "40"))  # 접속 주소(IP) 하나당


class App:
    def __init__(self, use_rag: bool = True, session_sec: int = SESSION_SEC):
        from ..chatkhu_client import ChatKHUClient
        from ..syllabus_rag import SyllabusRetriever

        settings = Settings()
        self.settings = settings
        use_rag = use_rag and SyllabusRetriever.exists()
        self.prompt = PromptBuilder(use_fewshot=True, multiturn=True, answer_template=True, search=use_rag)
        self.llm = ChatKHUClient(settings)
        retriever = SyllabusRetriever(llm=self.llm, embed_client=self.llm.client) if use_rag else None
        self.engine = Text2SQL(
            self.llm, self.prompt,
            SQLExecutor(row_limit=settings.row_limit, timeout_sec=settings.query_timeout_sec),
            settings.max_repair_attempts, retriever=retriever,
        )
        self.use_rag = use_rag
        self.session_sec = session_sec
        self.sessions: dict[str, dict] = {}  # token → {student_id, name, expires}
        self.histories: dict[str, list[dict]] = {}  # conversation_id → messages
        self.lock = threading.Lock()
        self.usage_day = ""
        self.usage_total = 0
        self.usage_ip: dict[str, int] = {}

    def _take_quota(self, ip: str) -> None:
        """질문 한 번을 한도에서 뺀다. 넘으면 ApiError(429)."""
        today = datetime.date.today().isoformat()
        with self.lock:
            if self.usage_day != today:
                self.usage_day, self.usage_total, self.usage_ip = today, 0, {}
            if DAILY_LIMIT and self.usage_total >= DAILY_LIMIT:
                raise ApiError(429, "오늘 서비스 전체 질문 한도를 다 썼어요. 내일 다시 이용해 주세요.")
            if IP_DAILY_LIMIT and self.usage_ip.get(ip, 0) >= IP_DAILY_LIMIT:
                raise ApiError(429, f"오늘 질문 한도({IP_DAILY_LIMIT}회)를 다 썼어요. 내일 다시 이용해 주세요.")
            self.usage_total += 1
            self.usage_ip[ip] = self.usage_ip.get(ip, 0) + 1

    # ---- 로그인 ----
    def login(self, student_id, password) -> dict:
        try:
            sid = int(str(student_id).strip())
        except ValueError:
            raise ApiError(400, "학번은 숫자로 입력해 주세요.")
        if not str(password or "").strip():
            raise ApiError(400, "비밀번호를 입력해 주세요.")
        conn = sqlite3.connect(f"file:{DATABASE_PATH}?mode=ro", uri=True)
        try:
            row = conn.execute("SELECT s.name, COALESCE(d.college, d.name, '') FROM students s "
                               "LEFT JOIN departments d ON d.department_id = s.department_id "
                               "WHERE s.student_id = ?", (sid,)).fetchone()
        finally:
            conn.close()
        if not row:
            raise ApiError(401, "학번 또는 비밀번호가 맞지 않아요.")
        token = secrets.token_urlsafe(24)
        with self.lock:
            self.sessions[token] = {"student_id": sid, "name": row[0], "expires": time.time() + self.session_sec}
        return {"token": token, "name": row[0], "college": row[1], "student_id": sid, "expires_in": self.session_sec}

    def session(self, token: str | None) -> dict | None:
        """토큰이 없으면 None(비로그인). 있는데 만료됐으면 ApiError(401, expired)."""
        if not token:
            return None
        with self.lock:
            s = self.sessions.get(token)
            if s and s["expires"] > time.time():
                return s
            self.sessions.pop(token, None)
        raise ApiError(401, "로그인 시간이 만료됐어요. 다시 로그인해 주세요.", expired=True)

    def logout(self, token: str | None) -> None:
        with self.lock:
            self.sessions.pop(token or "", None)

    # ---- 채팅 ----
    def chat(self, question: str, conversation_id: str, token: str | None, ip: str = "") -> dict:
        question = (question or "").strip()
        if not question:
            raise ApiError(400, "질문을 입력해 주세요.")
        if len(question) > 500:
            raise ApiError(400, "질문은 500자 안으로 입력해 주세요.")
        conv = (conversation_id or "default")[:64]
        try:
            s = self.session(token)
        except ApiError:
            with self.lock:  # 만료되면 개인 정보가 섞였을 수 있는 대화 기록도 지운다
                self.histories.pop(conv, None)
            raise
        sid = s["student_id"] if s else None
        self._take_quota(ip)
        with self.lock:
            history = list(self.histories.get(conv, []))
        out = self.engine.ask(question, sid, history)
        with self.lock:
            h = self.histories.setdefault(conv, [])
            h.append({"role": "user", "content": self.prompt.user_prompt(question, sid)})
            h.append({"role": "assistant", "content": out.attempts[-1].raw_response if out.attempts else ""})
            del h[:-MAX_HISTORY_TURNS * 2]
        return self._response(out, sid)

    def _response(self, out, sid) -> dict:
        res = out.result
        personal = bool(sid and res is not None and res.tables_read & PERSONAL_TABLES)
        kind = out.route  # sql / search / refused / clarify
        table = None
        if out.route == "sql":
            if res is None or not res.ok:
                kind = "error" if res is None or res.error_kind in ("timeout",) else "not_found"
            elif not res.rows:
                kind = "empty"
            elif len(res.rows) > 1 or len(res.columns) > 2:
                cols = [column_label(c) or (c if not c.isascii() else f"항목 {i + 1}")
                        for i, c in enumerate(res.columns)]
                rows = [[("미기재" if v is None else format_value(v, c)) for c, v in zip(res.columns, r)]
                        for r in res.rows[:MAX_TABLE_ROWS]]
                table = {"columns": cols, "rows": rows, "total": len(res.rows)}
        if out.route == "refused" and res is not None and res.error_kind == "guard" and sid is None:
            kind = "login_required"
        if kind == "login_required":
            answer = "본인 정보는 로그인한 뒤에 조회할 수 있어요."
        elif kind == "not_found":
            answer = ("이 질문은 지금 가진 자료에서 확인하지 못했어요. "
                      "강좌·시간표, 강의계획서, 졸업요건, 내 수강 이력 범위에서 물어봐 주세요.")
        elif table and len(out.answer or "") > 160:  # 긴 나열은 표와 겹치므로 짧게
            answer = f"{table['total']}건을 찾았어요. 아래 표에 정리했어요."
        else:
            answer = out.answer
        return {
            "answer": answer, "route": out.route, "kind": kind, "table": table,
            "sources": [{"label": s, "code": s.rsplit("-", 1)[0], "section": s.rsplit("-", 1)[-1],
                         "snippets": out.snippets.get(s, [])} for s in out.sources],
            "personal": personal, "student_id": sid if personal else None,
        }

    def reset(self, conversation_id: str) -> None:
        with self.lock:
            self.histories.pop((conversation_id or "default")[:64], None)

    # ---- 강의계획서 원문 ----
    @staticmethod
    def syllabus(code: str, section: str, term: str = CURRENT_TERM) -> dict:
        year, _, sem = term.partition("-")
        conn = sqlite3.connect(f"file:{DATABASE_PATH}?mode=ro", uri=True)
        conn.row_factory = sqlite3.Row
        try:
            o = conn.execute(
                "SELECT co.offering_id, co.course_code, co.course_name, co.section, co.credits, s.* "
                "FROM course_offerings co JOIN syllabi s ON s.offering_id = co.offering_id "
                "WHERE co.course_code = ? AND co.section = ? AND co.year = ? AND co.semester = ?",
                (code, section, int(year), sem)).fetchone()
            if not o:
                raise ApiError(404, "강의계획서를 찾지 못했어요.")
            profs = [r[0] for r in conn.execute(
                "SELECT DISTINCT p.name FROM offering_professors op JOIN professors p "
                "ON p.professor_id = op.professor_id WHERE op.offering_id = ?", (o["offering_id"],))]
            weeks = [dict(r) for r in conn.execute(
                "SELECT week, topic_content, note FROM syllabus_weekly_plans WHERE syllabus_id = ? ORDER BY week",
                (o["syllabus_id"],))]
        finally:
            conn.close()
        rates = [(label, o[f"{key}_percentage"]) for key, label in
                 (("midterm", "중간고사"), ("final_exam", "기말고사"), ("assignment", "과제"),
                  ("presentation", "발표"), ("attendance", "출석"), ("other", "기타"))]
        return {
            "title": f"{o['course_name']} {o['course_code']}-{o['section']}",
            "methods": _json_list(o["teaching_methods_json"]) or _json_list(o["class_types_json"]),
            "term": term, "credits": o["credits"], "professors": profs,
            "overview": o["overview"], "objectives": o["objectives"], "assignments": o["assignments"],
            "rates": [{"label": l, "value": None if v is None else format_value(v)} for l, v in rates],
            "weeks": weeks, "source_url": o["source_url"],
        }


def _json_list(raw) -> list[str]:
    try:
        return [str(x) for x in json.loads(raw or "[]") if x]
    except (ValueError, TypeError):
        return []


class ApiError(Exception):
    def __init__(self, status: int, message: str, **extra):
        super().__init__(message)
        self.status, self.message, self.extra = status, message, extra


def make_handler(app: App):
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *a, **kw):
            super().__init__(*a, directory=str(STATIC_DIR), **kw)

        def log_message(self, fmt, *args):  # 질문 내용은 남기지 않고 경로만
            print(f"[{self.log_date_time_string()}] {self.command} {urlparse(self.path).path} {args[1] if len(args) > 1 else ''}")

        def _json(self, status: int, body: dict) -> None:
            data = json.dumps(body, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(data)

        def _ip(self) -> str:
            """프록시(앱 라우팅) 뒤에서는 원래 접속 주소가 헤더로 온다."""
            for h in ("CF-Connecting-IP", "X-Real-IP", "X-Forwarded-For"):
                v = self.headers.get(h)
                if v:
                    return v.split(",")[0].strip()
            return self.client_address[0]

        def _token(self) -> str | None:
            auth = self.headers.get("Authorization", "")
            return auth[7:].strip() or None if auth.startswith("Bearer ") else None

        def _body(self) -> dict:
            n = int(self.headers.get("Content-Length") or 0)
            if n > 20_000:
                raise ApiError(413, "요청이 너무 커요.")
            try:
                return json.loads(self.rfile.read(n) or b"{}")
            except json.JSONDecodeError:
                raise ApiError(400, "잘못된 요청이에요.")

        def _handle(self, fn) -> None:
            try:
                self._json(200, fn() or {"ok": True})
            except ApiError as e:
                self._json(e.status, {"error": e.message, **e.extra})
            except (BrokenPipeError, ConnectionResetError):
                pass  # 사용자가 답변을 멈추면 연결이 끊긴다
            except Exception:
                traceback.print_exc()
                self._json(502, {"error": "결과를 불러오지 못했어요. 잠시 뒤 다시 시도해 주세요.", "retry": True})

        def do_GET(self):
            u = urlparse(self.path)
            if u.path == "/api/syllabus":
                q = parse_qs(u.query)
                return self._handle(lambda: app.syllabus(q.get("code", [""])[0], q.get("section", [""])[0]))
            if u.path == "/api/status":
                return self._handle(lambda: {"rag": app.use_rag, "term": CURRENT_TERM, "model": app.settings.model})
            if u.path.startswith("/api/"):
                return self._json(404, {"error": "없는 주소예요."})
            return super().do_GET()

        def do_POST(self):
            path = urlparse(self.path).path
            routes = {
                "/api/login": lambda b: app.login(b.get("student_id"), b.get("password")),
                "/api/logout": lambda b: app.logout(self._token()),
                "/api/chat": lambda b: app.chat(b.get("question", ""), b.get("conversation_id", ""), self._token(), self._ip()),
                "/api/reset": lambda b: app.reset(b.get("conversation_id", "")),
            }
            if path not in routes:
                return self._json(404, {"error": "없는 주소예요."})
            self._handle(lambda: routes[path](self._body()))

    return Handler


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--no-rag", action="store_true")
    ap.add_argument("--session-min", type=float, default=SESSION_SEC / 60, help="로그인 유지 시간(분)")
    args = ap.parse_args()
    app = App(use_rag=not args.no_rag, session_sec=int(args.session_min * 60))
    server = ThreadingHTTPServer((args.host, args.port), make_handler(app))
    print(f"경희 Campus AI - http://{args.host}:{args.port}  (RAG {'켜짐' if app.use_rag else '꺼짐'}, "
          f"로그인 {args.session_min:g}분, 하루 한도 전체 {DAILY_LIMIT or '없음'} / IP당 {IP_DAILY_LIMIT or '없음'})")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
