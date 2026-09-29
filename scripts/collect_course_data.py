#!/usr/bin/env python3
"""Collect public KHU course-list JSON for the College of Software.

The script discovers the historical major codes from each year's public
``data_YEAR.js`` file, then requests the public ``lectListJson`` endpoint for
each year, term, and major combination. Existing raw files are skipped unless
``--refresh`` is supplied.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


PROJECT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_DIR / "raw_data" / "course_lists"

BASE_URL = "https://sugang.khu.ac.kr"
COLLEGE_CODE = "A07340"
COLLEGE_NAME = "소프트웨어융합대학"
DEFAULT_YEARS = tuple(range(2020, 2027))
DEFAULT_TERMS = ("1", "2", "summer", "winter")

TERM_CODES = {
    "1": "10",
    "2": "20",
    "summer": "15",
    "winter": "25",
}

TERM_VARIABLE_SUFFIXES = {
    "1": "10",
    "2": "20",
    "summer": "15",
    "winter": "25",
}

USER_AGENT = (
    "Mozilla/5.0 (compatible; CampusAI-Capstone/1.0; "
    "+public-academic-data-research)"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Collect public KHU course-list JSON for majors belonging to "
            f"{COLLEGE_NAME} ({COLLEGE_CODE})."
        )
    )
    parser.add_argument(
        "--years",
        nargs="+",
        type=int,
        default=list(DEFAULT_YEARS),
        metavar="YEAR",
        help="years to collect (default: 2020 2021 ... 2026)",
    )
    parser.add_argument(
        "--terms",
        nargs="+",
        choices=tuple(TERM_CODES),
        default=list(DEFAULT_TERMS),
        help="terms to collect (default: 1 2 summer winter)",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="seconds to wait between network requests (default: 1.0)",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="network timeout in seconds (default: 30)",
    )
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="replace raw files that already exist",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="discover and print collection jobs without requesting course lists",
    )
    return parser.parse_args()


def validate_args(args: argparse.Namespace) -> None:
    invalid_years = sorted({year for year in args.years if year < 2000 or year > 2100})
    if invalid_years:
        raise SystemExit(f"Unsupported year values: {invalid_years}")
    if args.delay < 0:
        raise SystemExit("--delay must be zero or greater")
    if args.timeout <= 0:
        raise SystemExit("--timeout must be greater than zero")


def fetch_text(url: str, timeout: float) -> str:
    request = Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/json,text/javascript,text/plain,*/*",
            "Referer": f"{BASE_URL}/",
        },
    )
    with urlopen(request, timeout=timeout) as response:
        raw = response.read()
        charset = response.headers.get_content_charset() or "utf-8"
    return raw.decode(charset, errors="strict")


def extract_js_variables(source: str) -> dict[str, Any]:
    """Extract JSON-valued ``var name = ...`` declarations from JavaScript."""
    decoder = json.JSONDecoder()
    variables: dict[str, Any] = {}
    declaration = re.compile(r"\bvar\s+([A-Za-z_$][\w$]*)\s*=\s*")

    for match in declaration.finditer(source):
        name = match.group(1)
        try:
            value, _ = decoder.raw_decode(source, match.end())
        except json.JSONDecodeError:
            continue
        variables[name] = value
    return variables


def load_year_metadata(year: int, timeout: float) -> dict[str, Any]:
    url = f"{BASE_URL}/resources/data/data_{year}.js"
    return extract_js_variables(fetch_text(url, timeout))


def discover_majors(
    variables: dict[str, Any], year: int, term: str
) -> list[dict[str, str]]:
    suffix = TERM_VARIABLE_SUFFIXES[term]
    variable_name = f"major_{year}{suffix}"
    payload = variables.get(variable_name)
    if not isinstance(payload, dict) or not isinstance(payload.get("rows"), list):
        return []

    majors: dict[str, dict[str, str]] = {}
    for row in payload["rows"]:
        if not isinstance(row, dict) or str(row.get("dh", "")).strip() != COLLEGE_CODE:
            continue
        code = str(row.get("cd", "")).strip()
        if not code:
            continue
        majors[code] = {
            "code": code,
            "name": str(row.get("nm", "")).strip(),
            "english_name": str(row.get("enm", "")).strip(),
        }
    return [majors[code] for code in sorted(majors)]


def course_list_url(year: int, term: str, major_code: str) -> str:
    params = {
        "attribute": "lectListJson",
        "lang": "ko",
        "loginYn": "N",
        "menu": "1",
        "search_div": "E",
        "p_day": "",
        "p_time": "",
        "p_teach": "",
        "p_subjt": "",
        "p_major": major_code,
        "p_lang": "",
        "p_year": str(year),
        "p_term": TERM_CODES[term],
        "lecture_cd": "",
        "initYn": "Y",
        "_search": "false",
        "rows": "-1",
        "page": "1",
        "sidx": "",
        "sord": "asc",
    }
    return f"{BASE_URL}/core?{urlencode(params)}"


def fetch_course_list(
    year: int, term: str, major_code: str, timeout: float
) -> dict[str, Any]:
    url = course_list_url(year, term, major_code)
    payload = json.loads(fetch_text(url, timeout))
    if not isinstance(payload, dict) or not isinstance(payload.get("rows"), list):
        raise ValueError("response does not contain a top-level rows array")
    return payload


def output_path(year: int, term: str, major_code: str) -> Path:
    return OUTPUT_DIR / f"{year}-{term}_{major_code}_raw.json"


def write_json_atomic(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def polite_wait(delay: float) -> None:
    if delay > 0:
        time.sleep(delay)


def main() -> int:
    args = parse_args()
    validate_args(args)

    years = sorted(set(args.years))
    terms = list(dict.fromkeys(args.terms))
    report: dict[str, Any] = {
        "started_at_utc": datetime.now(timezone.utc).isoformat(),
        "college_code": COLLEGE_CODE,
        "college_name": COLLEGE_NAME,
        "years": years,
        "terms": terms,
        "dry_run": args.dry_run,
        "refresh": args.refresh,
        "jobs": [],
        "errors": [],
    }

    downloaded = 0
    skipped = 0
    empty = 0
    failed = 0

    for year in years:
        print(f"\n[{year}] Loading public major metadata...")
        try:
            variables = load_year_metadata(year, args.timeout)
            polite_wait(args.delay)
        except (HTTPError, URLError, TimeoutError, UnicodeError) as error:
            failed += 1
            message = f"{year}: could not load data_{year}.js: {error}"
            print(f"ERROR: {message}", file=sys.stderr)
            report["errors"].append(message)
            continue

        for term in terms:
            majors = discover_majors(variables, year, term)
            if not majors:
                message = f"{year}-{term}: no majors found under {COLLEGE_CODE}"
                print(f"WARNING: {message}")
                report["errors"].append(message)
                continue

            print(f"[{year}-{term}] majors: {len(majors)}")
            for major in majors:
                path = output_path(year, term, major["code"])
                job = {
                    "year": year,
                    "term": term,
                    "term_code": TERM_CODES[term],
                    "major_code": major["code"],
                    "major_name": major["name"],
                    "path": str(path.relative_to(PROJECT_DIR)),
                }

                if args.dry_run:
                    job["status"] = "planned"
                    print(
                        f"  PLAN {year}-{term} {major['code']} "
                        f"{major['name']} -> {path.name}"
                    )
                    report["jobs"].append(job)
                    continue

                if path.exists() and not args.refresh:
                    job["status"] = "skipped_existing"
                    skipped += 1
                    print(f"  SKIP {path.name}")
                    report["jobs"].append(job)
                    continue

                try:
                    payload = fetch_course_list(
                        year, term, major["code"], args.timeout
                    )
                    polite_wait(args.delay)
                    row_count = len(payload["rows"])
                    job["row_count"] = row_count
                    if row_count == 0:
                        job["status"] = "empty"
                        empty += 1
                        print(f"  EMPTY {path.name}")
                    else:
                        write_json_atomic(path, payload)
                        job["status"] = "downloaded"
                        downloaded += 1
                        print(f"  SAVE {path.name}: {row_count} rows")
                except (
                    HTTPError,
                    URLError,
                    TimeoutError,
                    UnicodeError,
                    json.JSONDecodeError,
                    ValueError,
                ) as error:
                    job["status"] = "failed"
                    job["error"] = str(error)
                    failed += 1
                    print(f"  ERROR {path.name}: {error}", file=sys.stderr)
                report["jobs"].append(job)

    report["finished_at_utc"] = datetime.now(timezone.utc).isoformat()
    report["summary"] = {
        "downloaded": downloaded,
        "skipped_existing": skipped,
        "empty": empty,
        "failed": failed,
    }

    if not args.dry_run:
        write_json_atomic(OUTPUT_DIR / "collection_report.json", report)

    print("\nCollection summary")
    print(f"  Downloaded: {downloaded}")
    print(f"  Skipped existing: {skipped}")
    print(f"  Empty: {empty}")
    print(f"  Failed: {failed}")
    if not args.dry_run:
        print(f"  Report: {OUTPUT_DIR / 'collection_report.json'}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
