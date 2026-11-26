"""answer_judge·sql_judge 가 같이 쓰는 부분: JSON 응답 받기(형식 틀리면 재요청), 중단 후 이어서 채점."""

from __future__ import annotations

import json
import re
from collections.abc import Callable
from pathlib import Path

RETRY_MSG = "형식 오류. 다른 글 없이 지시한 JSON 한 줄만 다시 출력하라."
REASON_MAX = 200


def parse_json_obj(text: str) -> dict:
    m = re.search(r"\{.*\}", text or "", flags=re.S)
    if not m:
        raise ValueError("JSON 객체가 없음")
    obj = json.loads(m.group(0))
    if not isinstance(obj, dict):
        raise ValueError("JSON 객체가 아님")
    return obj


def call_json(llm, messages: list[dict], parse: Callable[[dict], dict], max_retries: int = 1) -> tuple[dict | None, str, str, int]:
    """(파싱 결과, 상태, 원문, 토큰). 상태: judged / parse_error / api_error"""
    raw, tokens = "", 0
    for _ in range(max_retries + 1):
        try:
            resp = llm.complete(messages)
        except Exception as exc:  # 크레딧 부족·네트워크 등: 기록하고 다음 실행에서 다시 시도
            return None, "api_error", f"{type(exc).__name__}: {exc}"[:REASON_MAX], tokens
        raw, tokens = resp.text, tokens + resp.prompt_tokens + resp.completion_tokens
        try:
            return parse(parse_json_obj(raw)), "judged", raw, tokens
        except (ValueError, TypeError, json.JSONDecodeError):
            messages = [*messages, {"role": "assistant", "content": raw}, {"role": "user", "content": RETRY_MSG}]
    return None, "parse_error", raw, tokens


def load_records(out_dir: Path) -> list[dict]:
    src = out_dir / "results.jsonl"
    if not src.exists():
        raise SystemExit(f"{src} 가 없습니다. 먼저 evaluate 를 돌리세요.")
    return [json.loads(line) for line in src.read_text(encoding="utf-8").splitlines() if line.strip()]


def run_resumable(
    out_dir: Path,
    log_name: str,
    records: list[dict],
    judge_model: str,
    judge_one: Callable[[dict], dict],
    same_input: Callable[[dict, dict], bool],
    describe: Callable[[dict], str],
    force: bool = False,
) -> list[dict]:
    """문항마다 judge_one(rec) → 결과 행. 한 줄씩 log 에 덧붙여서 끊겨도 다음 실행이 이어받는다.
    같은 judge 모델로 끝난 판정(status=judged/skipped*)이고 입력이 같으면 다시 부르지 않는다."""
    log_path = out_dir / log_name
    done: dict[str, dict] = {}
    if log_path.exists() and not force:
        for line in log_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                j = json.loads(line)
                if j.get("status") not in ("api_error", "parse_error") and j.get("judge_model") == judge_model:
                    done[j["id"]] = j
    elif log_path.exists():
        log_path.unlink()

    rows = []
    with log_path.open("a", encoding="utf-8") as log:
        for idx, rec in enumerate(records, 1):
            prev = done.get(rec["id"])
            if prev and same_input(prev, rec):
                row, tag = prev, " (이전 판정)"
            else:
                row = {**judge_one(rec), "judge_model": judge_model}
                tag = ""
                log.write(json.dumps(row, ensure_ascii=False, default=str) + "\n")
                log.flush()
            rows.append(row)
            print(f"[{idx}/{len(records)}] {row['id']} {row['status']}{tag} - {describe(row)}")

    with log_path.open("w", encoding="utf-8") as log:  # 끝나면 문항 순서대로 다시 쓴다
        for row in rows:
            log.write(json.dumps(row, ensure_ascii=False, default=str) + "\n")
    return rows
