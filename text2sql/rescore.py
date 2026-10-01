"""이미 돌린 평가 결과를 API 호출 없이 다시 채점한다(비교 기준을 바꿨을 때 크레딧 절약용).

  python -m text2sql.rescore --run v2_fewshot
  → results/v2_fewshot/summary_rescored.md, results_rescored.csv, results_rescored.jsonl
"""

from __future__ import annotations

import argparse
import json

from .compare import gold_is_ordered
from .config import RESULTS_DIR, Settings
from .evaluate import _pct, score_record, write_outputs
from .executor import SQLExecutor


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True, help="results/ 아래 폴더 이름")
    args = ap.parse_args()

    out_dir = RESULTS_DIR / args.run
    src = out_dir / "results.jsonl"
    if not src.exists():
        raise SystemExit(f"{src} 가 없습니다.")
    settings = Settings()
    executor = SQLExecutor(row_limit=settings.row_limit, timeout_sec=settings.query_timeout_sec)

    records = [json.loads(line) for line in src.read_text(encoding="utf-8").splitlines() if line.strip()]
    changed = 0
    for rec in records:
        if not rec.get("exec_ok") or rec.get("expect_refusal") or rec.get("gold_error") or rec.get("api_error"):
            rec.setdefault("subset", rec.get("relaxed"))
            continue
        if rec.get("gold_sql"):
            gres = executor.run(rec["gold_sql"], student_id=rec.get("student_id"), enforce_scope=False)
            gold_rows, gold_cols = gres.rows, gres.columns
        else:
            gold_rows, gold_cols = [tuple(r) for r in rec.get("gold_rows", [])], rec.get("gold_columns", [])
        # 예측 행은 다시 실행해서 전체를 얻는다(예전 결과 파일은 50행까지만 저장했음)
        pres = executor.run(rec["pred_sql"], student_id=rec.get("student_id"))
        pred_rows = pres.rows if pres.ok else [tuple(r) for r in rec.get("pred_rows", [])]
        before = rec.get("diagnosis")
        rec["gold_columns"] = gold_cols
        ordered = rec.get("ordered")
        if ordered is None:
            ordered = bool(rec.get("gold_sql") and gold_is_ordered(rec["gold_sql"]))
        score_record(rec, gold_rows, gold_cols, pred_rows, ordered)
        changed += before != rec["diagnosis"]
        mark = "O" if rec["strict"] else ("△" if rec["relaxed"] else ("▽" if rec["subset"] else "X"))
        extra = f" (빠진 컬럼: {', '.join(rec['missing_columns'])})" if rec.get("missing_columns") else ""
        print(f"{mark} {rec['id']} {rec['diagnosis']}{extra}")

    s = write_outputs(records, out_dir, suffix="_rescored")
    o = s["overall"]
    print(f"\n진단이 바뀐 문항 {changed}개")
    print(f"strict {_pct(o['strict'], o['n'])} | relaxed {_pct(o['relaxed'], o['n'])} | subset {_pct(o['subset'], o['n'])}"
          f" → {out_dir / 'summary_rescored.md'}")


if __name__ == "__main__":
    main()