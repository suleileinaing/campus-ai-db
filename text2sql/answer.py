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


def format_value(v) -> str:
    if v is None:
        return "없음"
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return str(v)


def _fill(template: str, values: dict[str, str]) -> str:
    def sub(m: re.Match) -> str:
        if m.group(1) not in values:
            raise KeyError(m.group(1))
        return values[m.group(1)]
    return _PLACEHOLDER.sub(sub, template)


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
    per_row = [{c: format_value(v) for c, v in zip(columns, r)} for r in shown]

    def repeat(m: re.Match) -> str:
        return _join([_fill(m.group(1), vals) for vals in per_row], len(rows))

    text = _REPEAT.sub(repeat, template)
    if len(rows) == 1:
        values = dict(per_row[0])
    else:  # 여러 행이면 컬럼 값을 이어 붙인다(같은 값은 한 번만)
        values = {}
        for j, c in enumerate(columns):
            uniq = list(dict.fromkeys(format_value(r[j]) for r in rows))
            values[c] = _join(uniq[:MAX_LISTED], len(uniq))
    values["count"] = str(len(rows))
    return _fill(text, values)


def default_answer(columns: list[str], rows: list[tuple]) -> str:
    if len(rows) == 1 and len(columns) == 1:
        return f"결과는 {format_value(rows[0][0])}이에요."
    lines = [" / ".join(f"{c}: {format_value(v)}" for c, v in zip(columns, r)) for r in rows[:MAX_LISTED]]
    more = f"\n(외 {len(rows) - MAX_LISTED}건)" if len(rows) > MAX_LISTED else ""
    return f"결과 {len(rows)}건이에요.\n" + "\n".join(f"- {l}" for l in lines) + more
