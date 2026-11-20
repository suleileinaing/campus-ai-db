"""시스템 프롬프트 구성: 스키마 + DB에서 자동 추출한 값 형식 + 도메인 규칙 + few-shot 예시.

스키마는 실제로 연결한 DB(sqlite_master)에서 읽는다. 그래서 레포 DB 든 팀 통합 DB 든
TEXT2SQL_DB_PATH 만 바꾸면 그 DB 에 맞는 프롬프트가 만들어진다.

개인정보 보호: 학생 이름, 수강 이력 행 등 실제 데이터 행은 프롬프트에 넣지 않는다.
값 형식 힌트는 개인을 식별할 수 없는 코드성 컬럼의 DISTINCT 값만 사용한다.
bilingual-text-search 를 켠 경우 질문에 명시된 강좌의 비개인 강의계획서 텍스트만 추가한다.
"""

from __future__ import annotations

import re
import sqlite3
import math
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

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

_TEXT_SEARCH_CUES = (
    "강의계획서", "주차", "주차별", "교재", "참고서", "면담", "수업방식", "수업 방식",
    "운영방식", "운영 방식", "수업방법", "수업 방법", "공지", "제출", "숙제", "과제",
    "발표", "시험", "중간고사", "기말고사", "내용", "주제", "준비", "llm", "언어 모델",
)


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


def _compact_text(value: object, max_chars: int = 500) -> str:
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    return text if len(text) <= max_chars else text[: max_chars - 1] + "…"


def extract_bilingual_text_context(
    question: str,
    db_path: Path = DATABASE_PATH,
    current_term: str = CURRENT_TERM,
    max_offerings: int = 4,
    require_text_cue: bool = True,
) -> str:
    """질문에 명시된 강좌의 실제 강의계획서 텍스트를 작게 묶어 반환한다.

    한국어 질문과 DB 원문(HW, Large Language Models 등)의 표현 차이를 모델이
    직접 확인하게 한다. 학생·수강정보는 읽지 않으며, 강좌 식별자가 없거나 텍스트
    검색 성격이 아닌 질문에는 아무 내용도 추가하지 않는다.
    """
    lowered = question.lower()
    if require_text_cue and not any(cue in lowered for cue in _TEXT_SEARCH_CUES):
        return ""

    pair_matches = re.findall(r"\b([A-Z]{2,}\d+[A-Z0-9]*)-(\d{2})\b", question.upper())
    codes = sorted(set(re.findall(r"\b[A-Z]{2,}\d+[A-Z0-9]*\b", question.upper())))
    if not codes:
        return ""

    year_match = re.search(r"(20\d{2})\s*(?:학년도|년)", question)
    semester_match = re.search(r"([12])\s*학기", question)
    current_year, _, current_semester = current_term.partition("-")
    year = int(year_match.group(1)) if year_match else int(current_year)
    semester = semester_match.group(1) if semester_match else current_semester

    clauses: list[str] = []
    params: list[object] = [year, semester]
    paired_codes = {code for code, _ in pair_matches}
    for code, section in pair_matches:
        clauses.append("(o.course_code = ? AND o.section = ?)")
        params.extend((code, section))
    for code in codes:
        if code not in paired_codes:
            clauses.append("o.course_code = ?")
            params.append(code)
    if not clauses:
        return ""

    conn = _connect_ro(db_path)
    try:
        offerings = conn.execute(
            "SELECT o.offering_id, o.year, o.semester, o.course_code, o.section, o.course_name, "
            "s.syllabus_id, s.operation_modes, s.operation_note, s.consultation_time, "
            "s.assignments, s.course_notices "
            "FROM course_offerings AS o "
            "JOIN syllabi AS s ON s.offering_id = o.offering_id "
            "WHERE o.year = ? AND o.semester = ? AND (" + " OR ".join(clauses) + ") "
            "ORDER BY o.course_code, o.section LIMIT ?",
            (*params, max_offerings),
        ).fetchall()

        blocks: list[str] = []
        for offering in offerings:
            (offering_id, offer_year, offer_semester, code, section, name, syllabus_id,
             operation_modes, operation_note, consultation_time, assignments, course_notices) = offering
            lines = [f"- {offer_year}년 {offer_semester}학기 {code}-{section} {name}"]

            for label, value in (
                ("수업 운영방식", operation_modes),
                ("운영 안내", operation_note),
                ("면담 안내", consultation_time),
                ("과제 안내", assignments),
                ("수업 공지", course_notices),
            ):
                if value:
                    lines.append(f"  - {label}: {_compact_text(value)}")

            textbooks = conn.execute(
                "SELECT sequence, title, author, publisher, publication_year, isbn, note "
                "FROM syllabus_textbooks WHERE syllabus_id = ? ORDER BY sequence",
                (syllabus_id,),
            ).fetchall()
            for sequence, title, author, publisher, publication_year, isbn, note in textbooks:
                values = [
                    f"제목={_compact_text(title)}" if title else "",
                    f"저자={_compact_text(author)}" if author else "",
                    f"출판사={_compact_text(publisher)}" if publisher else "",
                    f"연도={_compact_text(publication_year)}" if publication_year else "",
                    f"ISBN={_compact_text(isbn)}" if isbn else "",
                    f"비고={_compact_text(note)}" if note else "",
                ]
                lines.append(f"  - 교재 {sequence}: " + "; ".join(v for v in values if v))

            weekly = conn.execute(
                "SELECT week, date_range, topic_content, note "
                "FROM syllabus_weekly_plans WHERE syllabus_id = ? ORDER BY week",
                (syllabus_id,),
            ).fetchall()
            for week, date_range, topic_content, note in weekly:
                values = [
                    f"기간={_compact_text(date_range)}" if date_range else "",
                    f"내용={_compact_text(topic_content)}" if topic_content else "",
                    f"비고={_compact_text(note)}" if note else "",
                ]
                lines.append(f"  - {week}주차: " + "; ".join(v for v in values if v))
            blocks.append("\n".join(lines))
        return "\n".join(blocks)
    finally:
        conn.close()


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
        "- 학생에게 적용되는 졸업요건은 students 와 graduation_requirements 를 department_id, track 이 같고 "
        "cohort_start <= admission_year AND (cohort_end IS NULL OR cohort_end >= admission_year) 로 매칭한다.",
        "- 이수구분별 최소학점은 requirement_categories, 공통 지정 필수과목은 requirement_courses, "
        "트랙별 필수·선택과목은 requirement_track_courses, 기타 조건은 requirement_others 에 있다.",
        "- 산학필수 최소학점은 전공선택 전체 최소학점에 포함되는 하위 조건이며 별도로 더하지 않는다. "
        "'전공선택' 또는 '전공선택 졸업요건'을 묻는 경우 requirement_categories 의 전체 최소학점을 "
        "그대로 답한다. '산학필수'를 묻는 경우 requirement_others 의 type = '산학필수' 조건을 답한다. "
        "'일반 전공선택' 또는 '산학필수를 제외한 전공선택'처럼 제외 범위를 명시적으로 묻는 경우에만 "
        "전공선택 전체 최소학점에서 산학필수 최소학점을 뺀다.",
        "- 학생에게 필요한 전체 필수과목을 묻는 경우 requirement_courses 의 공통 지정과목과 "
        "학생에게 적용되는 requirement_track_courses 의 TRACK_REQUIRED 과목을 합치고 중복을 제거한다.",
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


TASK_TAG_KEYWORDS = {
    "professor": {"교수", "담당", "강의한", "수업한"},
    "offering_department": {"개설목록", "개설학과", "이수구분", "전공필수", "전공선택"},
    "course_offering": {"개설", "과목", "강좌", "분반", "학기"},
    "prerequisite": {"선수과목", "선수", "수강 가능", "수강할 수"},
    "syllabus": {"강의계획서", "교재", "주차별", "중간고사", "기말고사", "과제", "평가비율"},
    "graduation": {"졸업요건", "졸업", "이수학점", "잔여학점", "부족학점"},
    "general_education": {"교양", "배분이수", "필수교과", "자유이수"},
    "student_history": {"수강기록", "수강이력", "재수강", "성적", "학적"},
    "schedule": {"수업시간", "요일", "강의실", "시간표"},
    "aggregation": {"몇 개", "개수", "합계", "총합", "평균", "비율", "비교", "감소", "증가"},
}

RELEVANCE_WEIGHTS = {
    "tfidf_cosine": 0.65,
    "entity_match": 0.20,
    "task_tag_match": 0.15,
}


def _normalize_retrieval_text(text: str) -> str:
    return re.sub(r"[^0-9a-z가-힣]+", "", text.lower())


def _char_ngrams(text: str, min_n: int = 2, max_n: int = 4) -> Counter[str]:
    normalized = _normalize_retrieval_text(text)
    return Counter(
        normalized[i : i + n]
        for n in range(min_n, max_n + 1)
        for i in range(max(0, len(normalized) - n + 1))
    )


def _tfidf_cosine(question: str, title: str, corpus_titles: list[str]) -> float:
    """문자 n-gram TF-IDF 벡터의 cosine similarity를 계산한다."""
    corpus_counts = [_char_ngrams(text) for text in corpus_titles]
    q_counts = _char_ngrams(question)
    t_counts = _char_ngrams(title)
    if not q_counts or not t_counts:
        return 0.0

    document_frequency = Counter()
    for counts in corpus_counts:
        document_frequency.update(counts.keys())
    n_documents = max(1, len(corpus_counts))

    def vector(counts: Counter[str]) -> dict[str, float]:
        total = sum(counts.values()) or 1
        return {
            term: (count / total) * (math.log((1 + n_documents) / (1 + document_frequency[term])) + 1)
            for term, count in counts.items()
        }

    q_vector = vector(q_counts)
    t_vector = vector(t_counts)
    dot = sum(value * t_vector.get(term, 0.0) for term, value in q_vector.items())
    q_norm = math.sqrt(sum(value * value for value in q_vector.values()))
    t_norm = math.sqrt(sum(value * value for value in t_vector.values()))
    return dot / (q_norm * t_norm) if q_norm and t_norm else 0.0


def _entities(text: str) -> set[str]:
    lowered = text.lower()
    features: set[str] = set()
    patterns = {
        "course_code": r"[a-z]{2,}\d+[a-z0-9]*",
        "year": r"20\d{2}",
        "semester": r"\b\d{1,2}학기",
        "section": r"(?<=-)\d{2}\b|\b\d{2}\s*분반",
    }
    for kind, pattern in patterns.items():
        values = re.findall(pattern, lowered)
        if values:
            features.add(f"type:{kind}")
            features.update(f"{kind}:{value}" for value in values)
    return features


def _task_tags(text: str) -> set[str]:
    lowered = text.lower()
    return {
        tag for tag, keywords in TASK_TAG_KEYWORDS.items()
        if any(keyword in lowered for keyword in keywords)
    }


def _overlap_ratio(left: set[str], right: set[str]) -> float:
    union = left | right
    return len(left & right) / len(union) if union else 0.0


def _relevance_score(question: str, title: str, corpus_titles: list[str]) -> float:
    """TF-IDF cosine과 구체 조건·학사 task 태그를 결합한 관련도 점수."""
    text_similarity = _tfidf_cosine(question, title, corpus_titles)
    entity_similarity = _overlap_ratio(_entities(question), _entities(title))
    task_similarity = _overlap_ratio(_task_tags(question), _task_tags(title))
    return (
        RELEVANCE_WEIGHTS["tfidf_cosine"] * text_similarity
        + RELEVANCE_WEIGHTS["entity_match"] * entity_similarity
        + RELEVANCE_WEIGHTS["task_tag_match"] * task_similarity
    )


class PromptBuilder:
    def __init__(
        self,
        use_fewshot: bool = True,
        exclude_sqls: list[str] | None = None,
        max_fewshot: int | None = None,
        db_path: Path = DATABASE_PATH,
        current_term: str = CURRENT_TERM,
        exclude_titles: list[str] | None = None,
        sample_queries_path: Path = SAMPLE_QUERIES_PATH,
        fewshot_selection: str = "fixed",
        bilingual_text_search: bool = False,
    ):
        if fewshot_selection not in {"fixed", "relevant"}:
            raise ValueError("fewshot_selection 은 'fixed' 또는 'relevant' 이어야 합니다.")
        self.db_path = db_path
        self.sample_queries_path = sample_queries_path
        self.fewshot_selection = fewshot_selection
        self.max_fewshot = max_fewshot
        self.bilingual_text_search = bilingual_text_search
        self.current_term = current_term
        self.schema = load_schema(db_path)
        self.value_hints = extract_value_hints(db_path)
        self.rules = build_domain_rules(db_path, current_term)
        available = fewshot_runs_on(load_sample_queries(sample_queries_path), db_path) if use_fewshot else []
        self.candidate_fewshot = (
            select_fewshot(available, exclude_sqls, None, exclude_titles) if use_fewshot else []
        )
        self.fewshot = (
            self.candidate_fewshot[:max_fewshot] if use_fewshot and fewshot_selection == "fixed" and max_fewshot
            else self.candidate_fewshot if use_fewshot and fewshot_selection == "fixed"
            else []
        )
        candidates = {e.title for e in self.candidate_fewshot}
        self.excluded_fewshot = [e.title for e in available if e.title not in candidates]

    def fewshot_for(self, question: str) -> list[FewShotExample]:
        if self.fewshot_selection == "fixed":
            return self.fewshot
        corpus_titles = [example.title for example in self.candidate_fewshot]
        ranked = sorted(
            enumerate(self.candidate_fewshot),
            key=lambda pair: (-_relevance_score(question, pair[1].title, corpus_titles), pair[0]),
        )
        limit = self.max_fewshot or len(ranked)
        return [example for _, example in ranked[:limit]]

    def system_prompt(
        self,
        question: str | None = None,
        include_bilingual_text: bool = False,
        force_bilingual_text: bool = False,
    ) -> str:
        parts = [
            "너는 경희대학교 소프트웨어융합대학 학사 데이터용 SQLite Text2SQL 변환기다.",
            "사용자의 한국어 질문을 아래 스키마에 대해 실행 가능한 SQLite 쿼리로 바꾼다.",
            "\n## 스키마\n```sql\n" + self.schema + "\n```",
            "\n## 실제 저장된 값 형식\n" + self.value_hints,
            "\n## 도메인 규칙\n" + self.rules,
            "\n## " + OUTPUT_FORMAT,
        ]
        if self.bilingual_text_search and include_bilingual_text and question:
            text_context = extract_bilingual_text_context(
                question,
                db_path=self.db_path,
                current_term=self.current_term,
                require_text_cue=not force_bilingual_text,
            )
            if text_context:
                parts.append(
                    "\n## 질문과 관련된 실제 강의계획서 텍스트\n"
                    "아래 내용은 DB에 저장된 원문이다. 한국어 질문과 영어·약어 표현이 달라도 "
                    "원문을 근거로 SQL 조건을 작성한다. 최종 출력은 반드시 SQL 하나만 반환한다.\n"
                    + text_context
                )
        selected = self.fewshot_for(question) if question is not None else self.fewshot
        if selected:
            shots = "\n\n".join(f"질문: {e.title}\n```sql\n{e.sql}\n```" for e in selected)
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
