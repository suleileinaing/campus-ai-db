"""강의계획서 본문 검색(RAG의 검색 단계).

표로 정리되지 않은 강의계획서 글(개요·목표·과제·공지·주차별 계획 등)을 조각으로 나눠 임베딩하고,
질문과 뜻이 가까운 조각을 찾는다. 학생 개인정보는 다루지 않는다(공개 강의계획서만).

  python -m text2sql.syllabus_rag build --term 2026-2            # 조각 만들고 임베딩(ChatKHU)
  python -m text2sql.syllabus_rag build --term 2026-2 --limit 20 # 앞 20개 강의계획서만
  python -m text2sql.syllabus_rag search "캡스톤디자인 팀플이야?" -k 5

- 결과는 공유 DB(campus_ai.db, git 추적)를 건드리지 않고 text2sql/rag_index/syllabus_<학기>.sqlite 에 저장한다.
- 중간에 끊겨도 다시 build 하면 임베딩 안 된 조각만 이어서 처리한다. --model 을 바꾸면 그 모델로 다시 만든다.
"""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from .config import CURRENT_TERM, DATABASE_PATH, TEXT2SQL_DIR

INDEX_DIR = TEXT2SQL_DIR / "rag_index"
DEFAULT_EMBED_MODEL = "qwen3.7-text-embedding"
CHUNK_CHARS = 800
BATCH = 32

# (컬럼, 한국어 이름) — 강의계획서에서 글로 된 칸
TEXT_FIELDS = [
    ("overview", "수업 개요"), ("objectives", "수업 목표"), ("assignments", "과제"),
    ("course_notices", "공지사항"), ("operation_note", "운영 방식"), ("class_type_note", "수업 유형 설명"),
    ("teaching_method_note", "수업 방법 설명"), ("additional_materials", "참고 자료"),
    ("other_weekly_content", "기타 수업 내용"), ("consultation_time", "상담 시간"),
    ("midterm_detail", "중간고사 안내"), ("final_exam_detail", "기말고사 안내"),
    ("assignment_detail", "과제 평가 안내"), ("presentation_detail", "발표 평가 안내"),
    ("attendance_detail", "출석 평가 안내"), ("other_detail", "기타 평가 안내"),
]
JSON_FIELDS = [("class_types_json", "수업 유형"), ("teaching_methods_json", "수업 방법")]


@dataclass
class Chunk:
    syllabus_id: int
    offering_id: int
    course_code: str
    section: str
    course_name: str
    term: str
    content: str


def _clean(s: str | None) -> str:
    return re.sub(r"[ \t]+", " ", (s or "").replace("\xad", "")).strip()


def _split(text: str, limit: int = CHUNK_CHARS) -> list[str]:
    """줄 단위로 limit 글자 안쪽 조각을 만든다(한 줄이 너무 길면 자른다)."""
    out, cur = [], ""
    for line in text.splitlines():
        while len(line) > limit:
            out.append(line[:limit])
            line = line[limit:]
        if cur and len(cur) + len(line) + 1 > limit:
            out.append(cur)
            cur = ""
        cur = f"{cur}\n{line}" if cur else line
    if cur.strip():
        out.append(cur)
    return out


def build_chunks(term: str, limit: int | None = None, db_path: Path = DATABASE_PATH) -> list[Chunk]:
    year, _, sem = term.partition("-")
    conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    try:
        cols = ", ".join(f"s.{c}" for c, _ in TEXT_FIELDS + JSON_FIELDS)
        rows = conn.execute(
            f"SELECT s.syllabus_id, o.offering_id, o.course_code, o.section, o.course_name, {cols} "
            "FROM syllabi s JOIN course_offerings o USING (offering_id) "
            "WHERE o.year = ? AND o.semester = ? ORDER BY o.course_code, o.section",
            (int(year), sem),
        ).fetchall()[:limit]
        profs = {
            oid: names for oid, names in conn.execute(
                "SELECT op.offering_id, group_concat(DISTINCT p.name) FROM offering_professors op "
                "JOIN professors p USING (professor_id) GROUP BY op.offering_id")
        }
        weekly: dict[int, list[str]] = {}
        for sid, week, topic, note in conn.execute(
                "SELECT syllabus_id, week, topic_content, note FROM syllabus_weekly_plans ORDER BY syllabus_id, week"):
            t = _clean(topic) + (f" ({_clean(note)})" if _clean(note) else "")
            if t:
                weekly.setdefault(sid, []).append(f"{week}주: {t}")
    finally:
        conn.close()

    chunks = []
    for r in rows:
        head = (f"[{r['course_code']}-{r['section']}] {r['course_name']} ({term})"
                + (f" 담당 {profs[r['offering_id']]}" if profs.get(r["offering_id"]) else ""))
        parts = []
        for col, label in JSON_FIELDS:
            try:
                vals = json.loads(r[col] or "[]")
            except json.JSONDecodeError:
                vals = []
            if vals:
                parts.append(f"{label}: {', '.join(map(str, vals))}")
        for col, label in TEXT_FIELDS:
            if _clean(r[col]):
                parts.append(f"{label}:\n{_clean(r[col])}")
        if weekly.get(r["syllabus_id"]):
            parts.append("주차별 계획:\n" + "\n".join(weekly[r["syllabus_id"]]))
        for piece in _split("\n".join(parts), CHUNK_CHARS - len(head) - 1):
            chunks.append(Chunk(r["syllabus_id"], r["offering_id"], r["course_code"], r["section"],
                                r["course_name"], term, f"{head}\n{piece}"))
    return chunks


# ---------- 인덱스 파일 ----------

def index_path(term: str) -> Path:
    return INDEX_DIR / f"syllabus_{term}.sqlite"


def _open_index(path: Path) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS chunks (chunk_id INTEGER PRIMARY KEY, syllabus_id INTEGER, offering_id INTEGER, "
        "course_code TEXT, section TEXT, course_name TEXT, term TEXT, content TEXT UNIQUE, "
        "model TEXT, embedding BLOB)")
    conn.execute("CREATE TABLE IF NOT EXISTS usage (model TEXT, tokens INTEGER, at TEXT DEFAULT CURRENT_TIMESTAMP)")
    return conn


def _embed(client, model: str, texts: list[str]) -> tuple[list[list[float]], int]:
    r = client.embeddings.create(model=model, input=texts)
    usage = getattr(r, "usage", None)
    return [d.embedding for d in sorted(r.data, key=lambda d: d.index)], getattr(usage, "total_tokens", 0) or 0


def build_index(term: str, model: str = DEFAULT_EMBED_MODEL, limit: int | None = None, client=None) -> dict:
    chunks = build_chunks(term, limit)
    conn = _open_index(index_path(term))
    with conn:
        conn.executemany(
            "INSERT OR IGNORE INTO chunks (syllabus_id, offering_id, course_code, section, course_name, term, content) "
            "VALUES (?,?,?,?,?,?,?)",
            [(c.syllabus_id, c.offering_id, c.course_code, c.section, c.course_name, c.term, c.content) for c in chunks])
    todo = conn.execute("SELECT chunk_id, content FROM chunks WHERE embedding IS NULL OR model IS NOT ? "
                        "ORDER BY chunk_id", (model,)).fetchall()
    if client is None:
        from .chatkhu_client import ChatKHUClient
        client = ChatKHUClient().client
    tokens = 0
    for i in range(0, len(todo), BATCH):
        batch = todo[i:i + BATCH]
        vecs, used = _embed(client, model, [t for _, t in batch])
        tokens += used
        with conn:  # 배치마다 저장 → 끊겨도 이어서
            conn.executemany("UPDATE chunks SET embedding = ?, model = ? WHERE chunk_id = ?",
                             [(np.asarray(v, dtype=np.float32).tobytes(), model, cid) for (cid, _), v in zip(batch, vecs)])
            conn.execute("INSERT INTO usage (model, tokens) VALUES (?, ?)", (model, used))
        print(f"  임베딩 {min(i + BATCH, len(todo))}/{len(todo)} 조각 (누적 {tokens:,} 토큰)")
    total = conn.execute("SELECT COUNT(*), COUNT(DISTINCT syllabus_id) FROM chunks").fetchone()
    all_tokens = conn.execute("SELECT COALESCE(SUM(tokens),0) FROM usage WHERE model = ?", (model,)).fetchone()[0]
    conn.close()
    return {"term": term, "model": model, "chunks": total[0], "syllabi": total[1],
            "embedded_now": len(todo), "tokens_now": tokens, "tokens_total": all_tokens,
            "path": str(index_path(term))}


# ---------- 검색 ----------

@dataclass
class Hit:
    score: float
    course_code: str
    section: str
    course_name: str
    content: str


def matches_course(f: str, code: str, section: str, name: str) -> bool:
    """[과목] 필터 한 개: 'CSE406' · 'CSE406-07' · 과목명(일부) 중 하나와 맞으면 True."""
    f = f.strip()
    if not f:
        return True
    fu = f.upper().replace(" ", "")
    if fu in (code.upper(), f"{code}-{section}".upper()) or f.replace(" ", "") in name.replace(" ", ""):
        return True
    # '캡스톤디자인 07분반' · '캡스톤디자인-07' · 'CSE406 07' 처럼 분반이 붙은 경우
    m = re.fullmatch(r"(.*?\D)[\s\-]*(\d{1,2})\s*(?:분반|반)?", f)
    if not m or not m.group(1).strip(" -"):
        return False
    base = m.group(1).strip(" -")
    return m.group(2).zfill(2) == section and matches_course(base, code, section, name)


ANSWER_SYSTEM = """너는 경희대학교 학사 챗봇 '쿠옹이'다. 아래 강의계획서 발췌만 근거로 학생 질문에 답한다.
- 발췌에 없는 내용은 지어내지 말고 "강의계획서에서 찾지 못했어요"라고 말한다.
- 어느 과목(과목코드-분반) 이야기인지 밝힌다. 분반마다 내용이 다르면 나눠서 말한다.
- 존댓말로 2~4문장, 필요하면 짧은 목록. SQL·내부 용어는 쓰지 않는다."""


class SyllabusRetriever:
    """임베딩을 한 번 읽어 두고 질문마다 검색·답변한다. 강의계획서(공개 정보)만 LLM 에 보낸다."""

    def __init__(self, term: str = CURRENT_TERM, llm=None, embed_client=None, k: int = 5):
        conn = _open_index(index_path(term))
        rows = conn.execute("SELECT course_code, section, course_name, content, model, embedding FROM chunks "
                            "WHERE embedding IS NOT NULL ORDER BY chunk_id").fetchall()
        conn.close()
        if not rows:
            raise FileNotFoundError(f"{index_path(term)} 에 임베딩이 없습니다. 먼저 build 하세요.")
        self.term, self.k, self.llm = term, k, llm
        self.model = rows[0][4]
        self.meta = [(r[0], r[1], r[2], r[3]) for r in rows]
        m = np.stack([np.frombuffer(r[5], dtype=np.float32) for r in rows])
        self.matrix = m / (np.linalg.norm(m, axis=1, keepdims=True) + 1e-9)
        if embed_client is None:
            from .chatkhu_client import ChatKHUClient
            embed_client = ChatKHUClient().client
        self.embed_client = embed_client

    @staticmethod
    def exists(term: str = CURRENT_TERM) -> bool:
        return index_path(term).exists()

    def search(self, query: str, courses: list[str] | None = None, k: int | None = None) -> list[Hit]:
        courses = [c for c in (courses or []) if c.strip()]
        idx = [i for i, (code, sec, name, _) in enumerate(self.meta)
               if not courses or any(matches_course(c, code, sec, name) for c in courses)]
        if not idx:
            return []
        (q,), _ = _embed(self.embed_client, self.model, [query])
        qv = np.asarray(q, dtype=np.float32)
        qv /= np.linalg.norm(qv) + 1e-9
        scores = self.matrix[idx] @ qv
        top = np.argsort(-scores)[: (k or self.k)]
        return [Hit(float(scores[j]), *self.meta[idx[j]]) for j in top]

    def answer(self, question: str, hits: list[Hit]):
        """(답변, LLMResponse 또는 None). 찾은 조각이 없으면 LLM 을 부르지 않는다."""
        if not hits:
            return f"{self.term} 강의계획서에서 해당 과목이나 내용을 찾지 못했어요.", None
        excerpts = "\n\n---\n\n".join(h.content for h in hits)
        resp = self.llm.complete([
            {"role": "system", "content": ANSWER_SYSTEM},
            {"role": "user", "content": f"강의계획서 발췌:\n{excerpts}\n\n학생 질문: {question}"},
        ])
        return resp.text.strip(), resp


def search(question: str, term: str, k: int = 5, client=None) -> list[Hit]:
    return SyllabusRetriever(term, embed_client=client, k=k).search(question)


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("--term", default=CURRENT_TERM)
    b.add_argument("--model", default=DEFAULT_EMBED_MODEL)
    b.add_argument("--limit", type=int, default=None, help="앞에서부터 N개 강의계획서만")
    s = sub.add_parser("search")
    s.add_argument("question")
    s.add_argument("--term", default=CURRENT_TERM)
    s.add_argument("-k", type=int, default=5)
    args = ap.parse_args()

    if args.cmd == "build":
        r = build_index(args.term, args.model, args.limit)
        print(f"\n{r['term']} 강의계획서 {r['syllabi']}개 → 조각 {r['chunks']}개 | 이번에 임베딩 {r['embedded_now']}개, "
              f"{r['tokens_now']:,} 토큰 (누적 {r['tokens_total']:,}) → {r['path']}")
    else:
        for i, h in enumerate(search(args.question, args.term, args.k), 1):
            print(f"\n[{i}] {h.score:.3f} {h.course_code}-{h.section} {h.course_name}\n{h.content[:400]}")


if __name__ == "__main__":
    main()
