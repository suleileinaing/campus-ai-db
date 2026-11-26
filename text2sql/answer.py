"""LLM 이 만든 답변 틀에 DB 결과를 로컬에서 채워 자연어 답변을 만든다.

조회 결과 행은 LLM 에 보내지 않는다. LLM 은 SQL 과 함께 값 자리만 비운 틀을 낸다.
  ANSWER: 담당 교수님은 {professor_name} 교수님이에요.
  ANSWER: 다른 과목은 [[{course_code}-{section}]] 이렇게 {count}개예요.
- {컬럼}: 결과가 한 행이면 그 값, 여러 행이면 그 컬럼 값을 쉼표로 이어 붙인다.
- [[ ... ]]: 안의 틀을 행마다 채워 쉼표로 이어 붙인다.
- {count}: 결과 행 수.
틀이 없거나 채울 수 없으면(없는 컬럼 등) 결과를 간단히 나열하는 기본 문장을 쓴다.
"""

from __future__ import annotations

import re

ANSWER_TOKEN = "ANSWER"
MAX_LISTED = 20  # 답변 문장에 나열할 최대 행 수

_ANSWER_LINE = re.compile(rf"^\s*{ANSWER_TOKEN}\s*:\s*(.+?)\s*$", flags=re.M)
_PLACEHOLDER = re.compile(r"\{(\w+)\}")
_REPEAT = re.compile(r"\[\[(.+?)\]\]", flags=re.S)


def split_answer_template(text: str) -> tuple[str, str | None]:
    """응답에서 'ANSWER: ...' 줄을 떼어 낸다. (나머지 텍스트, 틀)"""
    m = _ANSWER_LINE.search(text)
    if not m:
        return text, None
    return text[: m.start()] + text[m.end():], m.group(1)


# DB 에 영어 코드로 저장된 값 → 답변에 보일 한국어. 값만 봐도 뜻이 분명한 코드는 항상 바꾸고,
# 'NONE'·'TBD' 처럼 흔한 단어는 컬럼 이름으로 어떤 값인지 알 수 있을 때만 바꾼다.
_CODE_KO = {
    "FULL": "영어 전체 강의", "PARTIAL": "영어 일부 강의", "SECOND_FOREIGN_LANGUAGE": "제2외국어 강의",
    "OFFLINE": "대면", "ONLINE": "비대면", "HYBRID": "혼합(대면+비대면)",
    "SCHEDULED": "시간표 있음", "ASYNCHRONOUS": "비동기(시간 미지정)", "INTENSIVE": "집중 이수",
    "ROOM_ONLY": "강의실만 배정",
    "REQUIRED": "필수", "RECOMMENDED": "권장",
    "CORE_REQUIRED": "필수교과", "DISTRIBUTION": "배분이수", "FREE_ELECTIVE": "자유이수",
    "monday": "월요일", "tuesday": "화요일", "wednesday": "수요일", "thursday": "목요일",
    "friday": "금요일", "saturday": "토요일", "sunday": "일요일",
}
_CONTEXT_CODE_KO = {  # 컬럼 이름에 들어 있는 말 → 그 컬럼에서만 바꿀 값
    "english": {"NONE": "해당 없음"},
    "delivery": {"TBD": "미정"},
    "schedule": {"TBD": "미정"},
    "mode": {"TBD": "미정"},
}


def format_value(v, column: str | None = None) -> str:
    if v is None:
        return "없음"
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    if isinstance(v, str):
        if v in _CODE_KO:
            return _CODE_KO[v]
        col = (column or "").lower()
        for hint, table in _CONTEXT_CODE_KO.items():
            if hint in col and v in table:
                return table[v]
    return str(v)


def _lookup(values: dict[str, str], key: str) -> str:
    """틀의 {이름} 에 맞는 값. 정확히 같은 컬럼이 없으면 대소문자 무시 → 한쪽이 다른 쪽으로 끝나는
    컬럼이 하나뿐일 때 그것을 쓴다(예: 모델이 'AS' 뒤 공백을 빠뜨려 생긴 'AScredit_shortfall')."""
    if key in values:
        return values[key]
    k = key.lower()
    for cands in ([c for c in values if c.lower() == k],
                  [c for c in values if c != "count" and (c.lower().endswith(k) or k.endswith(c.lower()))]):
        if len(cands) == 1:
            return values[cands[0]]
    raise KeyError(key)


def _fill(template: str, values: dict[str, str]) -> str:
    return _PLACEHOLDER.sub(lambda m: _lookup(values, m.group(1)), template)


def _join(items: list[str], total: int) -> str:
    s = ", ".join(items)
    return s + (f" 외 {total - len(items)}건" if total > len(items) else "")


def render_answer(template: str | None, columns: list[str], rows: list[tuple]) -> str:
    if not rows:
        return "조건에 맞는 결과가 없어요."
    if template:
        try:
            return _render(template, columns, rows)
        except (KeyError, ValueError):
            pass  # 틀이 결과 컬럼과 맞지 않으면 기본 문장으로
    return default_answer(columns, rows)


def _render(template: str, columns: list[str], rows: list[tuple]) -> str:
    shown = rows[:MAX_LISTED]
    per_row = [{c: format_value(v, c) for c, v in zip(columns, r)} for r in shown]

    def repeat(m: re.Match) -> str:
        return _join([_fill(m.group(1), vals) for vals in per_row], len(rows))

    text = _REPEAT.sub(repeat, template)
    if len(rows) == 1:
        values = dict(per_row[0])
    else:  # 여러 행이면 컬럼 값을 이어 붙인다(같은 값은 한 번만)
        values = {}
        for j, c in enumerate(columns):
            uniq = list(dict.fromkeys(format_value(r[j], c) for r in rows))
            values[c] = _join(uniq[:MAX_LISTED], len(uniq))
    values["count"] = str(len(rows))
    return _fill(text, values)


# 기본 문장에서 영어 컬럼 이름을 그대로 보이지 않도록 단어 단위로 한국어로 바꾼다.
_WORD_KO = {
    "student": "학생", "id": "번호", "name": "이름", "names": "이름", "professor": "교수",
    "professors": "교수", "instructor": "교수", "instructors": "교수", "list": "목록", "course": "과목", "title": "과목명",
    "code": "코드", "section": "분반", "offering": "강좌", "year": "연도", "semester": "학기", "term": "학기",
    "credit": "학점", "credits": "학점", "grade": "성적", "score": "점수", "points": "점수", "point": "점수",
    "department": "학과", "dept": "학과", "college": "단과대", "category": "이수구분", "track": "트랙",
    "status": "상태", "email": "이메일", "office": "연구실", "phone": "전화번호", "room": "강의실",
    "day": "요일", "time": "시간", "start": "시작", "end": "종료", "minutes": "분", "hours": "시간",
    "total": "총", "sum": "합계", "count": "수", "num": "수", "avg": "평균", "average": "평균",
    "min": "최소", "max": "최대", "required": "필요", "remaining": "남은", "shortfall": "부족", "shortage": "부족",
    "earned": "취득", "completed": "이수", "areas": "영역 수", "area": "영역", "perarea": "영역당",
    "percentage": "비율", "ratio": "비율", "rate": "비율", "midterm": "중간고사", "final": "기말", "exam": "시험",
    "assignment": "과제", "attendance": "출석", "general": "교양", "major": "전공", "distribution": "배분이수",
    "difference": "차이", "diff": "차이", "reduction": "감소", "overlap": "겹침", "cohort": "학번",
    "satisfied": "충족 여부", "meets": "충족", "both": "모두", "is": "", "has": "", "the": "",
}


def column_label(col: str) -> str | None:
    """'per_area_min_credits' → '영역 당 최소 학점'. 모르는 단어가 있으면 None(이름을 숨긴다)."""
    words = [w for w in re.split(r"[_\s]+", col.strip().lower().replace("per_area", "perarea")) if w]
    if not words or any(w not in _WORD_KO for w in words):
        return None
    label = " ".join(_WORD_KO[w] for w in words if _WORD_KO[w])
    return label or None


def _labeled(col: str, v) -> str:
    label = column_label(col) if re.fullmatch(r"[A-Za-z0-9_]+", col) else col  # 한글 별칭은 그대로
    return f"{label}: {format_value(v, col)}" if label else format_value(v, col)


def default_answer(columns: list[str], rows: list[tuple]) -> str:
    if len(rows) == 1 and len(columns) == 1:
        return f"결과는 {format_value(rows[0][0], columns[0])}이에요."
    lines = [" / ".join(_labeled(c, v) for c, v in zip(columns, r)) for r in rows[:MAX_LISTED]]
    more = f"\n(외 {len(rows) - MAX_LISTED}건)" if len(rows) > MAX_LISTED else ""
    return f"결과 {len(rows)}건이에요.\n" + "\n".join(f"- {l}" for l in lines) + more
