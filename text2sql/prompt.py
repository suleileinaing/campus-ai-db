"""시스템 프롬프트 구성: 스키마 + DB에서 자동 추출한 값 형식 + 도메인 규칙 + few-shot 예시.

스키마는 실제로 연결한 DB(sqlite_master)에서 읽는다. 그래서 레포 DB 든 팀 통합 DB 든
TEXT2SQL_DB_PATH 만 바꾸면 그 DB 에 맞는 프롬프트가 만들어진다.

개인정보 보호: 학생 이름, 수강 이력 행 등 실제 데이터 행은 프롬프트에 넣지 않는다.
값 형식 힌트는 개인을 식별할 수 없는 코드성 컬럼의 DISTINCT 값만 사용한다.
"""

from __future__ import annotations

import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path

from .answer import ANSWER_TOKEN
from .config import CURRENT_TERM, DATABASE_PATH, SAMPLE_QUERIES_PATH

# (table, column) — 개인 식별 정보가 아닌 코드성 컬럼만. DB 에 없는 컬럼은 건너뛴다.
VALUE_HINT_COLUMNS = [
    ("course_offerings", "semester"),
    ("course_offerings", "english_type"),
    ("course_offerings", "delivery_mode"),
    ("course_offerings", "schedule_status"),
    ("course_offerings", "campus"),
    ("course_offerings", "target_year"),
    ("time_slots", "day"),
    ("enrollments", "status"),
    ("enrollments", "grade"),
    ("students", "track"),
    ("students", "status"),
    ("students", "extra_track_type"),
    ("course_prerequisites", "prerequisite_type"),
    ("requirement_others", "type"),
    ("academic_calendar", "event_type"),
    ("academic_calendar", "semester"),
    ("library_hours", "period_type"),
    ("library_hours", "day_type"),
    ("library_book", "material_type"),
]

# 프롬프트에서 뺄 테이블(내부용·비어 있음)
SKIP_TABLES = {"sqlite_sequence", "sqlite_stat1", "sqlite_stat4", "syllabus_chunks"}

REFUSE_TOKEN = "REFUSE"
CLARIFY_TOKEN = "CLARIFY"
SEARCH_TOKEN = "SEARCH"


@dataclass
class FewShotExample:
    title: str
    sql: str


def _connect_ro(db_path: Path) -> sqlite3.Connection:
    return sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)


def _table_columns(conn: sqlite3.Connection) -> dict[str, set[str]]:
    out = {}
    for (name,) in conn.execute("SELECT name FROM sqlite_master WHERE type IN ('table','view')"):
        out[name] = {r[1] for r in conn.execute(f'PRAGMA table_info("{name}")')}
    return out


def load_schema(db_path: Path = DATABASE_PATH) -> str:
    """DB 의 CREATE TABLE / CREATE VIEW 문을 그대로 가져온다."""
    conn = _connect_ro(db_path)
    try:
        rows = conn.execute(
            "SELECT type, name, sql FROM sqlite_master "
            "WHERE type IN ('table','view') AND sql IS NOT NULL ORDER BY type DESC, rowid"
        ).fetchall()
    finally:
        conn.close()
    parts = [sql.strip().rstrip(";") + ";" for _, name, sql in rows if name not in SKIP_TABLES]
    return "\n\n".join(parts)


def extract_value_hints(db_path: Path = DATABASE_PATH, max_values: int = 20) -> str:
    conn = _connect_ro(db_path)
    lines: list[str] = []
    try:
        cols = _table_columns(conn)
        for table, column in VALUE_HINT_COLUMNS:
            if column not in cols.get(table, set()):
                continue
            rows = conn.execute(
                f'SELECT DISTINCT "{column}" FROM "{table}" WHERE "{column}" IS NOT NULL ORDER BY 1 LIMIT ?',
                (max_values + 1,),
            ).fetchall()
            values = [r[0] for r in rows]
            suffix = " ..." if len(values) > max_values else ""
            lines.append(f"- {table}.{column}: {values[:max_values]!r}{suffix}")

        cats = conn.execute("SELECT category_id, category_name FROM course_categories ORDER BY 1").fetchall()
        lines.append("- course_categories (category_id: 이름): " + ", ".join(f"{i}: {n}" for i, n in cats))

        depts = conn.execute(
            "SELECT DISTINCT d.department_id, d.name FROM departments d "
            "JOIN graduation_requirements g ON g.department_id = d.department_id ORDER BY 1"
        ).fetchall()
        lines.append("- 졸업요건이 있는 학과 (department_id: 이름): " + ", ".join(f"{i}: {n}" for i, n in depts))

        y0, y1 = conn.execute("SELECT MIN(year), MAX(year) FROM course_offerings").fetchone()
        lines.append(f"- course_offerings.year 범위: {y0} ~ {y1}")
    finally:
        conn.close()
    return "\n".join(lines)


def build_domain_rules(db_path: Path = DATABASE_PATH, current_term: str = CURRENT_TERM) -> str:
    """공통 규칙 + 연결한 DB 에 해당 테이블/컬럼이 있을 때만 붙는 규칙."""
    conn = _connect_ro(db_path)
    try:
        cols = _table_columns(conn)
    finally:
        conn.close()
    year, _, sem = current_term.partition("-")

    rules = [
        "- 학기(semester)는 TEXT 이다. '1', '2', 'summer', 'winter' 처럼 따옴표로 비교한다. 연도(year)는 INTEGER.",
        f"- '이번 학기', '현재 학기', '지금'은 {year}년 {sem}학기(year = {year} AND semester = '{sem}')를 뜻한다. "
        "학기를 말하지 않은 개설강좌·학사일정 질문도 이 학기를 기준으로 한다.",
        "- 요일(time_slots.day)은 영어 소문자('monday' ...), 시간은 'HH:MM' 문자열이다. "
        "수업시간은 course_offerings → class_times → time_slots 로 조인한다.",
        "- 분반(section)은 '01' 처럼 0으로 채운 TEXT 이다.",
        "- 교수는 course_offerings → offering_professors → professors 로 조인한다(팀티칭이면 여러 명).",
        "- 강의계획서 정보(평가비율, 교재, 주차별 계획)는 course_offerings → syllabi(offering_id) → "
        "syllabus_textbooks / syllabus_weekly_plans(syllabus_id) 로 조인한다.",
        "- NULL 은 '정보 없음'이다(예: 강의계획서에 중간고사 비율이 안 적힘). COALESCE·IFNULL 로 0 이나 다른 값으로 "
        "바꾸지 말고 NULL 그대로 계산·비교한다. 그러면 비율 조건(>= 30 등)에서 정보 없는 강좌는 빠지고, "
        "NULL 이 섞인 계산 결과는 NULL 로 남는다. 질문이 '없으면 0으로' 처럼 직접 정할 때만 바꾼다.",
        "- 학생에게 적용되는 졸업요건은 students 와 graduation_requirements 를 department_id, track 이 같고 "
        "cohort_start <= admission_year AND (cohort_end IS NULL OR cohort_end >= admission_year) 로 매칭한다.",
        "- 이수구분별 최소학점은 requirement_categories, 지정 필수과목은 requirement_courses, "
        "기타 조건(산학필수·영어강좌 등)은 requirement_others 에 있다.",
        "- 선수과목은 course_prerequisites 이며 학번 조건은 (cohort_start IS NULL OR cohort_start <= 입학연도) "
        "AND (cohort_end IS NULL OR cohort_end >= 입학연도) 로 건다.",
        "- 과목 이름으로 찾을 때는 course_offerings.course_name 또는 courses.current_name 에 LIKE '%이름%' 을 쓴다.",
        "- 목록 질문에는 임의로 LIMIT 을 붙이지 않는다. 순위·최근 N개처럼 질문이 개수를 정할 때만 ORDER BY 와 함께 쓴다.",
    ]

    enr = cols.get("enrollments", set())
    if "retaken" in enr:
        line = ("- 취득(이수) 학점은 enrollments.status = '완료' AND enrollments.retaken = 0 인 행만 합산한다"
                "(retaken = 1 은 재수강해서 대체된 예전 수강 기록).")
        if "is_retake" in enr:
            line += " is_retake = 1 은 '이번 수강이 재수강'이라는 뜻이다. '재수강한 과목'은 is_retake = 1 로 찾는다."
        rules.append(line)
    if "credits" in cols.get("course_offerings", set()):
        rules.append("- 학점은 course_offerings.credits(해당 개설강좌 기준) 또는 courses.credits 에 있다. "
                     "수강 기록 학점 합산은 enrollments → course_offerings(offering_id) 의 credits 를 쓴다.")
    else:
        rules.append("- 학점은 courses.credits 에 있다. enrollments → courses(course_code) 로 조인한다.")
    if "category_id" in enr:
        rules.append("- 학생이 들은 과목의 이수구분은 enrollments.category_id 를 쓴다.")
    if "academic_calendar" in cols:
        rules.append("- 학사일정(개강, 수강신청·정정, 시험, 방학 등)은 academic_calendar 에 있다. "
                     "event_type 값으로 거르고 year/semester 로 학기를 지정한다. 날짜는 'YYYY-MM-DD' 문자열이다.")
    if "library_book" in cols:
        rules.append("- 도서관 자료는 library_book, 분관은 library_branch, 개방시간은 library_hours, "
                     "좌석 현황은 library_seat_snapshot 에 있다. 교재와는 isbn 으로 조인한다.")

    rules += [
        "- students, enrollments 를 조회할 때는 반드시 '현재 로그인 학생 ID' 로 WHERE student_id = ... 조건을 건다.",
        f"- 다른 학생(이름이나 학번으로 지목된 타인)의 정보를 묻거나, 데이터 수정·삭제를 요구하면 SQL 대신 "
        f"'{REFUSE_TOKEN}: 이유' 한 줄만 출력한다.",
    ]
    return "\n".join(rules)


OUTPUT_FORMAT = f"""\
출력 형식:
- SQLite 문법의 SELECT(또는 WITH ... SELECT) 문 하나만 ```sql 코드블록 하나에 담아 출력한다.
- 설명, 주석, 여러 개의 문장, INSERT/UPDATE/DELETE/PRAGMA 는 출력하지 않는다.
- 질문에 답하는 데 필요한 컬럼만 SELECT 한다.
- 거부해야 하는 질문이면 코드블록 없이 '{REFUSE_TOKEN}: 이유' 만 출력한다.
"""


MULTITURN_RULES = f"""\
대화:
- 앞선 질문과 네가 낸 SQL 이 대화로 함께 주어질 수 있다. '그 교수님', '방금 과목'처럼 앞을 가리키는 말은 이전 질문과 SQL 을 보고 풀어서, 이번 질문에 답하는 SQL 하나를 새로 만든다.
- 이전 조회 결과 값은 주어지지 않는다. 앞 턴의 값이 필요하면 이전 SQL 을 서브쿼리나 CTE 로 다시 쓴다.
- 답을 하나로 정하는 데 필요한 정보(예: 분반)가 빠져 있어 추측해야 한다면 SQL 대신 코드블록 없이 '{CLARIFY_TOKEN}: 되물을 질문' 한 줄만 출력한다.
"""


ANSWER_RULES = f"""\
답변 틀:
- SQL 코드블록 다음 줄에 사용자에게 보여 줄 한국어 답변 틀을 '{ANSWER_TOKEN}: ...' 한 줄로 출력한다. (위 출력 형식의 '설명 금지'에서 이 한 줄만 예외)
- 조회 결과는 너에게 보이지 않는다. 값을 짐작해 쓰지 말고, SELECT 한 컬럼 이름을 {{컬럼}} 자리로 넣는다.
- 여러 행을 나열할 부분은 [[ ]] 로 감싼다. 행 수는 {{count}} 로 쓴다.
  예: {ANSWER_TOKEN}: 담당 교수님은 {{professor_name}} 교수님이에요.
  예: {ANSWER_TOKEN}: 같은 학기에 맡은 다른 과목은 [[{{course_code}}-{{section}}]]로 {{count}}개예요.
- 존댓말로 한두 문장만 쓴다.
"""


def search_rules(current_term: str = CURRENT_TERM) -> str:
    return f"""강의계획서 본문 검색:
- 강의계획서에 글로 적힌 내용(수업 진행 방식, 팀 프로젝트 여부, 과제 내용, 주차별 주제, 상담 시간, 준비물·참고자료, 수업 분위기 등)을 묻는 질문은 SQL 대신 코드블록 없이 '{SEARCH_TOKEN}: [과목] 찾을 내용' 한 줄만 출력한다.
  [과목] 에는 질문에 나온 과목코드(분반 포함 가능) 또는 과목명을 쉼표로 넣고, 특정 과목이 없으면 [] 로 비운다.
  예: {SEARCH_TOKEN}: [CSE406] 팀 프로젝트 진행 방식
  예: {SEARCH_TOKEN}: [캡스톤디자인] 교수님 상담 시간
  예: {SEARCH_TOKEN}: [] 파이썬 실습 위주로 진행하는 수업
- 숫자·조건으로 답할 수 있는 질문(평가 비율, 시험 유무, 학점, 영어강좌 여부, 산학필수, 시간표, 담당 교수, 개설 여부, 졸업요건, 학생 본인 정보)은 검색하지 말고 SQL 로 답한다.
- 본문 검색은 {current_term} 학기 강의계획서만 가능하다. 다른 학기 강의계획서 내용을 물으면 SQL 로 답할 수 있는 부분만 SQL 로 답한다.
"""


def load_sample_queries(path: Path = SAMPLE_QUERIES_PATH) -> list[FewShotExample]:
    """sample_queries.sql 의 '-- N. 제목' 블록을 예시로 파싱한다."""
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    blocks = re.split(r"^-- \d+\.\s*", text, flags=re.M)[1:]
    examples = []
    for block in blocks:
        title, _, sql = block.partition("\n")
        examples.append(FewShotExample(title=title.strip(), sql=sql.strip().rstrip(";") + ";"))
    return examples


def normalize_sql(sql: str) -> str:
    return re.sub(r"\s+", " ", sql.strip().rstrip(";")).lower()


def fewshot_runs_on(examples: list[FewShotExample], db_path: Path) -> list[FewShotExample]:
    """연결한 DB 에서 실제로 실행되는 예시만 남긴다(스키마가 다른 DB 대비)."""
    conn = _connect_ro(db_path)
    ok = []
    try:
        for e in examples:
            try:
                conn.execute("EXPLAIN " + e.sql.rstrip(";"))
                ok.append(e)
            except sqlite3.Error:
                pass
    finally:
        conn.close()
    return ok


def select_fewshot(
    examples: list[FewShotExample],
    exclude_sqls: list[str] | None = None,
    max_examples: int | None = None,
    exclude_titles: list[str] | None = None,
) -> list[FewShotExample]:
    """gold/참고 SQL 과 같거나 제목으로 지정한 예시는 제외해서 평가 누수를 막는다."""
    excluded = {normalize_sql(s) for s in (exclude_sqls or [])}
    titles = {t.strip() for t in (exclude_titles or [])}
    unknown = titles - {e.title for e in examples}
    if unknown:
        raise ValueError(f"없는 few-shot 제목: {sorted(unknown)}")
    kept = [e for e in examples if normalize_sql(e.sql) not in excluded and e.title not in titles]
    return kept[:max_examples] if max_examples else kept


class PromptBuilder:
    def __init__(
        self,
        use_fewshot: bool = True,
        exclude_sqls: list[str] | None = None,
        max_fewshot: int | None = None,
        db_path: Path = DATABASE_PATH,
        current_term: str = CURRENT_TERM,
        exclude_titles: list[str] | None = None,
        multiturn: bool = False,
        answer_template: bool = False,
        search: bool = False,
    ):
        self.search = search
        self.current_term = current_term
        self.multiturn = multiturn
        self.answer_template = answer_template
        self.db_path = db_path
        self.schema = load_schema(db_path)
        self.value_hints = extract_value_hints(db_path)
        self.rules = build_domain_rules(db_path, current_term)
        available = fewshot_runs_on(load_sample_queries(), db_path) if use_fewshot else []
        self.fewshot = select_fewshot(available, exclude_sqls, max_fewshot, exclude_titles) if use_fewshot else []
        kept = {e.title for e in self.fewshot}
        self.excluded_fewshot = [e.title for e in available if e.title not in kept]

    def system_prompt(self) -> str:
        parts = [
            "너는 경희대학교 소프트웨어융합대학 학사 데이터용 SQLite Text2SQL 변환기다.",
            "사용자의 한국어 질문을 아래 스키마에 대해 실행 가능한 SQLite 쿼리로 바꾼다.",
            "\n## 스키마\n```sql\n" + self.schema + "\n```",
            "\n## 실제 저장된 값 형식\n" + self.value_hints,
            "\n## 도메인 규칙\n" + self.rules,
            "\n## " + OUTPUT_FORMAT,
        ]
        if self.multiturn:
            parts.append("\n## " + MULTITURN_RULES)
        if self.answer_template:
            parts.append("\n## " + ANSWER_RULES)
        if self.search:
            parts.append("\n## " + search_rules(self.current_term))
        if self.fewshot:
            shots = "\n\n".join(f"질문: {e.title}\n```sql\n{e.sql}\n```" for e in self.fewshot)
            parts.append("\n## 예시\n" + shots)
        return "\n".join(parts)

    @staticmethod
    def user_prompt(question: str, student_id: int | None) -> str:
        who = f"현재 로그인 학생 ID: {student_id}" if student_id else "현재 로그인 학생: 없음 (개인 정보 테이블 조회 불가)"
        return f"{who}\n질문: {question}"

    @staticmethod
    def repair_prompt(sql: str, error: str) -> str:
        return (
            "위 SQL 을 실행했더니 다음 오류가 났다. 스키마와 규칙을 다시 확인해 고친 SQL 하나만 출력하라.\n"
            f"```sql\n{sql}\n```\n오류: {error}"
        )
