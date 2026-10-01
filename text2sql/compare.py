"""실행 결과 비교(execution accuracy).

- strict : 결과 행 집합이 완전히 같다(컬럼 순서 포함). gold 에 ORDER BY 가 있으면 순서도 비교.
- relaxed: 예측 결과에서 gold 컬럼과 대응되는 컬럼만 골라 냈을 때 행 집합이 같다.
           (예측 SQL 이 컬럼을 더 뽑거나 컬럼 순서를 바꾼 경우를 허용, 행 순서는 보지 않음)
           gold 의 ORDER BY 는 보여주기용인 경우가 많아서, 행 순서는 strict 에서만 따진다.
- subset : 예측 컬럼이 모두 gold 컬럼 중 하나와 값이 일치하고, gold 를 그 컬럼들로 줄였을 때
           (중복 제거 후) 같은 행 집합이 된다. gold 에 student_id·requirement_id 같은 보조 컬럼이
           많아서, 모델이 핵심 값만 답하면 relaxed 에서도 틀리는 문제를 보완한다.
           빠진 gold 컬럼(missing_columns)을 같이 기록하므로, 빠진 게 핵심 정보인지 사람이 확인해야 한다.
"""

from __future__ import annotations

import itertools
import re
from collections import Counter
from dataclasses import dataclass

FLOAT_DIGITS = 4
MAX_MAPPINGS = 5000


def norm_value(v):
    if isinstance(v, bool):
        return int(v)
    if isinstance(v, float):
        return int(v) if v.is_integer() else round(v, FLOAT_DIGITS)
    if isinstance(v, str):
        return v.strip()
    return v


def norm_rows(rows) -> list[tuple]:
    return [tuple(norm_value(v) for v in r) for r in rows]


def _key(row: tuple) -> tuple:
    # None/int/str 섞여도 정렬 가능하도록
    return tuple((type(v).__name__, str(v)) for v in row)


def rows_equal(gold, pred, ordered: bool) -> bool:
    g, p = norm_rows(gold), norm_rows(pred)
    if ordered:
        return g == p
    return Counter(map(_key, g)) == Counter(map(_key, p))


def gold_is_ordered(gold_sql: str) -> bool:
    """가장 바깥 쿼리 끝부분에 ORDER BY 가 있으면 순서 비교."""
    tail = re.sub(r"\s+", " ", gold_sql.strip().rstrip(";")).upper()
    depth, last_order = 0, -1
    for i, ch in enumerate(tail):
        depth += (ch == "(") - (ch == ")")
        if depth == 0 and tail.startswith("ORDER BY", i):
            last_order = i
    return last_order != -1


def relaxed_match(gold, pred, ordered: bool) -> bool:
    g, p = norm_rows(gold), norm_rows(pred)
    if len(g) != len(p):
        return False
    if not g:
        return True
    n_gold, n_pred = len(g[0]), len(p[0])
    if n_pred < n_gold:
        return False

    # gold 컬럼마다 값 multiset 이 같은 예측 컬럼 후보를 찾는다
    def col_counter(rows, j):
        return Counter((type(r[j]).__name__, str(r[j])) for r in rows)

    candidates = []
    for gi in range(n_gold):
        gc = col_counter(g, gi)
        cands = [pj for pj in range(n_pred) if col_counter(p, pj) == gc]
        if not cands:
            return False
        candidates.append(cands)

    for count, mapping in enumerate(itertools.product(*candidates)):
        if count >= MAX_MAPPINGS:
            break
        if len(set(mapping)) != len(mapping):
            continue
        projected = [tuple(r[j] for j in mapping) for r in p]
        if rows_equal(g, projected, ordered):
            return True
    return False


def _col_key_counter(rows, j):
    return Counter((type(r[j]).__name__, str(r[j])) for r in rows)


def subset_match(gold, pred) -> list[int] | None:
    """예측 컬럼 → gold 컬럼 대응(gold 인덱스 목록)을 찾으면 돌려준다. 행은 중복 제거 후 집합으로 비교."""
    g, p = norm_rows(gold), norm_rows(pred)
    if not g or not p:
        return None
    n_gold, n_pred = len(g[0]), len(p[0])
    if n_pred == 0 or n_pred > n_gold:
        return None
    g_sets = [{(type(r[j]).__name__, str(r[j])) for r in g} for j in range(n_gold)]
    candidates = []
    for pj in range(n_pred):
        p_set = {(type(r[pj]).__name__, str(r[pj])) for r in p}
        cands = [gi for gi in range(n_gold) if g_sets[gi] == p_set]
        if not cands:
            return None
        candidates.append(cands)
    p_rows = {_key(r) for r in p}
    for count, mapping in enumerate(itertools.product(*candidates)):
        if count >= MAX_MAPPINGS:
            break
        if len(set(mapping)) != len(mapping):
            continue
        if {_key(tuple(r[j] for j in mapping)) for r in g} == p_rows:
            return list(mapping)
    return None


@dataclass
class Comparison:
    strict: bool
    relaxed: bool
    ordered: bool
    gold_row_count: int
    pred_row_count: int
    diagnosis: str
    subset: bool = False
    missing_columns: list[str] | None = None


def compare_results(gold_rows, pred_rows, ordered: bool, gold_columns: list[str] | None = None) -> Comparison:
    strict = rows_equal(gold_rows, pred_rows, ordered) and (
        not gold_rows or not pred_rows or len(gold_rows[0]) == len(pred_rows[0])
    )
    relaxed = strict or relaxed_match(gold_rows, pred_rows, ordered=False)
    same_shape = not gold_rows or not pred_rows or len(gold_rows[0]) == len(pred_rows[0])
    if strict:
        diag = "correct"
    elif relaxed and same_shape and rows_equal(gold_rows, pred_rows, ordered=False):
        diag = "order_mismatch"
    elif relaxed:
        diag = "correct_extra_columns"
    elif len(gold_rows) != len(pred_rows):
        diag = "row_count_mismatch"
    else:
        diag = "value_mismatch"

    subset, missing = relaxed, None
    if not relaxed:
        mapping = subset_match(gold_rows, pred_rows)
        if mapping is not None:
            subset = True
            n_gold = len(gold_rows[0])
            names = gold_columns or [f"col{j + 1}" for j in range(n_gold)]
            missing = [names[j] for j in range(n_gold) if j not in mapping]
            diag = "missing_columns"
    return Comparison(strict, relaxed, ordered, len(gold_rows), len(pred_rows), diag, subset, missing)