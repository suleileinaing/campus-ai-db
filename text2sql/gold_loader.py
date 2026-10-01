"""gold 질의셋 로더. JSON(list) 또는 CSV 를 읽는다.

필드: id, question, student_id(선택), gold_sql, gold_answer(선택), ordered(선택), tags(선택),
      expect_refusal(선택), note(선택)
팀 질의셋의 한국어 헤더(질문, 대상 학생 ID, 정답 SQL, 정답 값, 유형, 출처)도 그대로 읽는다.
- 학생 ID 가 '-' 이면 로그인 없음.
- 정답 SQL 이 '없음' 으로 시작하거나 정답 값이 '접근 거부' 로 시작하면 거부가 정답인 문항(expect_refusal).
- gold_sql 이 있으면 DB 에서 실행해서 정답 행을 만든다(권장).
- gold_sql 없이 gold_answer 만 있으면 그 값을 정답 행으로 쓴다.
  gold_answer 형식: 스칼라 → [[값]], 1차원 리스트 → 한 열, 2차원 리스트 → 그대로,
  [{"컬럼": 값, ...}, ...] (행 단위 JSON) → 각 dict 의 값 순서대로.
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class GoldItem:
    id: str
    question: str
    student_id: int | None = None
    gold_sql: str | None = None
    gold_answer: object = None
    ordered: bool | None = None
    tags: list[str] = field(default_factory=list)
    expect_refusal: bool = False
    note: str = ""

    def answer_rows(self) -> list[tuple] | None:
        a = self.gold_answer
        if a is None or a == "":
            return None
        if isinstance(a, str):
            try:
                a = json.loads(a)
            except json.JSONDecodeError:
                return [(a,)]
        if not isinstance(a, list):
            return [(a,)]
        if a and all(isinstance(x, dict) for x in a):
            return [tuple(x.values()) for x in a]
        if a and all(isinstance(x, list) for x in a):
            return [tuple(x) for x in a]
        return [(x,) for x in a]


KOREAN_HEADERS = {
    "질문": "question",
    "대상 학생 ID": "student_id",
    "대상 학생ID": "student_id",
    "학생 ID": "student_id",
    "정답 SQL": "gold_sql",
    "정답 값": "gold_answer",
    "유형": "tags",
    "출처": "source",
    "비고": "note",
}


def _to_int(v) -> int | None:
    if v is None or str(v).strip() in ("", "-", "null", "None", "없음"):
        return None
    return int(str(v).strip())


def _to_bool(v) -> bool | None:
    if v in (None, ""):
        return None
    if isinstance(v, bool):
        return v
    return str(v).strip().lower() in {"1", "true", "yes", "y"}


def _to_tags(v) -> list[str]:
    if not v:
        return []
    if isinstance(v, list):
        return [str(t) for t in v]
    return [t.strip() for t in str(v).replace(";", ",").split(",") if t.strip()]


def load_gold(path: str | Path) -> list[GoldItem]:
    path = Path(path)
    if path.suffix.lower() == ".json":
        raw = json.loads(path.read_text(encoding="utf-8"))
    elif path.suffix.lower() == ".csv":
        with path.open(encoding="utf-8-sig", newline="") as f:
            raw = list(csv.DictReader(f))
    else:
        raise ValueError("gold 파일은 .json 또는 .csv 여야 합니다.")

    items = []
    for i, r in enumerate(raw, 1):
        r = {KOREAN_HEADERS.get(k.strip(), k.strip()): v for k, v in r.items() if k}
        if not (r.get("question") or "").strip():
            continue
        gold_sql = (r.get("gold_sql") or "").strip() or None
        answer = r.get("gold_answer")
        refusal = _to_bool(r.get("expect_refusal")) or (
            (gold_sql or "").startswith("없음") or str(answer or "").strip().startswith("접근 거부")
        )
        if refusal:
            gold_sql, answer = None, None
        items.append(GoldItem(
            id=str(r.get("id") or f"q{i:03d}"),
            question=r["question"].strip(),
            student_id=_to_int(r.get("student_id")),
            gold_sql=gold_sql,
            gold_answer=answer,
            ordered=_to_bool(r.get("ordered")),
            tags=_to_tags(r.get("tags")),
            expect_refusal=bool(refusal),
            note=str(r.get("note") or ""),
        ))
    if not items:
        raise ValueError(f"{path} 에서 질문을 찾지 못했습니다.")
    return items
