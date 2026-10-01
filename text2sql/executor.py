"""LLM 이 만든 SQL 을 추출·검증하고 읽기 전용으로 실행한다.

방어선
1) 문자열 검사: 단일 SELECT/WITH 문만 허용
2) DB 를 mode=ro 로 열기
3) sqlite authorizer: READ/SELECT/FUNCTION 외 동작 거부, 읽은 테이블 기록
4) 개인정보 테이블(students, enrollments) 접근 시 로그인 학생 ID 만 쓰는지 검사
5) 실행 시간 제한과 결과 행 수 제한
"""

from __future__ import annotations

import re
import sqlite3
import time
from dataclasses import dataclass, field
from pathlib import Path

from .config import DATABASE_PATH

PERSONAL_TABLES = {"students", "enrollments"}
STUDENT_ID_PATTERN = re.compile(r"\b(20\d{7})\b")  # 예: 202210001

_ALLOWED_ACTIONS = {
    sqlite3.SQLITE_SELECT,
    sqlite3.SQLITE_READ,
    sqlite3.SQLITE_FUNCTION,
    getattr(sqlite3, "SQLITE_RECURSIVE", 33),
}


class GuardError(Exception):
    """실행 전에 거부된 SQL."""


@dataclass
class ExecutionResult:
    ok: bool
    columns: list[str] = field(default_factory=list)
    rows: list[tuple] = field(default_factory=list)
    error: str | None = None
    error_kind: str | None = None  # "guard" | "sqlite" | "timeout"
    truncated: bool = False
    tables_read: set[str] = field(default_factory=set)
    elapsed_sec: float = 0.0


def extract_sql(text: str) -> str | None:
    """```sql 블록 → 일반 ``` 블록 → SELECT/WITH 로 시작하는 본문 순으로 찾는다."""
    for pattern in (r"```sql\s*(.*?)```", r"```\s*(.*?)```"):
        m = re.search(pattern, text, flags=re.S | re.I)
        if m and m.group(1).strip():
            return m.group(1).strip()
    m = re.search(r"\b(WITH|SELECT)\b.*", text, flags=re.S | re.I)
    return m.group(0).strip() if m else None


def _strip_comments_and_strings(sql: str) -> str:
    sql = re.sub(r"--[^\n]*", " ", sql)
    sql = re.sub(r"/\*.*?\*/", " ", sql, flags=re.S)
    return re.sub(r"'(?:[^']|'')*'", "''", sql)


def check_statement(sql: str) -> str:
    """단일 읽기 전용 문장인지 확인하고, 끝의 세미콜론을 정리해 돌려준다."""
    cleaned = sql.strip().rstrip(";").strip()
    bare = _strip_comments_and_strings(cleaned)
    if ";" in bare:
        raise GuardError("여러 개의 SQL 문은 허용되지 않습니다.")
    if not re.match(r"^\s*(WITH|SELECT)\b", bare, flags=re.I):
        raise GuardError("SELECT 또는 WITH 로 시작하는 조회문만 허용됩니다.")
    if re.search(r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|REPLACE|ATTACH|DETACH|PRAGMA|VACUUM)\b", bare, re.I):
        raise GuardError("데이터를 변경하거나 DB 설정을 바꾸는 구문은 허용되지 않습니다.")
    return cleaned


def check_student_scope(sql: str, tables_read: set[str], student_id: int | None) -> None:
    """개인정보 테이블 접근 범위 검사 (백엔드 인가를 대신하지 않는 1차 방어선)."""
    touched = tables_read & PERSONAL_TABLES
    if not touched:
        return
    if student_id is None:
        raise GuardError(f"로그인 학생 없이 개인정보 테이블({', '.join(sorted(touched))})을 조회할 수 없습니다.")
    literals = {int(x) for x in STUDENT_ID_PATTERN.findall(_strip_comments_and_strings(sql))}
    if not literals:
        raise GuardError("개인정보 테이블 조회에는 로그인 학생 ID 조건이 필요합니다.")
    if literals - {student_id}:
        raise GuardError("로그인한 학생이 아닌 다른 학생 ID 가 포함되어 있습니다.")


class SQLExecutor:
    def __init__(self, db_path: Path = DATABASE_PATH, row_limit: int = 500, timeout_sec: float = 10.0):
        self.db_path = db_path
        self.row_limit = row_limit
        self.timeout_sec = timeout_sec

    def _connect(self, tables_read: set[str]) -> sqlite3.Connection:
        conn = sqlite3.connect(f"file:{self.db_path}?mode=ro", uri=True)

        def authorizer(action, arg1, arg2, dbname, source):
            if action == sqlite3.SQLITE_READ and arg1:
                tables_read.add(arg1.lower())
            return sqlite3.SQLITE_OK if action in _ALLOWED_ACTIONS else sqlite3.SQLITE_DENY

        conn.set_authorizer(authorizer)
        return conn

    def run(self, sql: str, student_id: int | None = None, enforce_scope: bool = True) -> ExecutionResult:
        """enforce_scope=False 는 gold SQL 처럼 신뢰하는 쿼리를 돌릴 때만 쓴다."""
        tables_read: set[str] = set()
        start = time.perf_counter()
        try:
            sql = check_statement(sql)
        except GuardError as exc:
            return ExecutionResult(ok=False, error=str(exc), error_kind="guard")

        conn = self._connect(tables_read)
        deadline = start + self.timeout_sec
        conn.set_progress_handler(lambda: 1 if time.perf_counter() > deadline else 0, 10_000)
        try:
            # EXPLAIN 단계에서 authorizer 가 읽는 테이블을 모두 기록 → 실행 전에 범위 검사
            conn.execute("EXPLAIN " + sql).fetchall()
            if enforce_scope:
                check_student_scope(sql, tables_read, student_id)
            cur = conn.execute(sql)
            columns = [d[0] for d in cur.description or []]
            rows = cur.fetchmany(self.row_limit + 1)
            truncated = len(rows) > self.row_limit
            return ExecutionResult(
                ok=True, columns=columns, rows=[tuple(r) for r in rows[: self.row_limit]],
                truncated=truncated, tables_read=tables_read, elapsed_sec=time.perf_counter() - start,
            )
        except GuardError as exc:
            return ExecutionResult(ok=False, error=str(exc), error_kind="guard", tables_read=tables_read)
        except sqlite3.OperationalError as exc:
            kind = "timeout" if "interrupted" in str(exc).lower() else "sqlite"
            msg = f"실행 시간 {self.timeout_sec}초 초과" if kind == "timeout" else str(exc)
            return ExecutionResult(ok=False, error=msg, error_kind=kind, tables_read=tables_read)
        except sqlite3.DatabaseError as exc:
            kind = "guard" if "not authorized" in str(exc).lower() else "sqlite"
            return ExecutionResult(ok=False, error=str(exc), error_kind=kind, tables_read=tables_read)
        finally:
            conn.close()
