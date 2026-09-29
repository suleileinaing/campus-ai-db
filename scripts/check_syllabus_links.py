#!/usr/bin/env python3
"""Check KHU syllabus links without saving their response bodies."""

from __future__ import annotations

import argparse
import csv
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlparse
from urllib.request import Request, urlopen


PROJECT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = PROJECT_DIR / "processed_data" / "website_tables" / "syllabi.csv"
DEFAULT_OUTPUT = PROJECT_DIR / "validation_report" / "syllabus_link_report.csv"
USER_AGENT = (
    "Mozilla/5.0 (compatible; CampusAI-Capstone/1.0; "
    "+public-academic-data-research)"
)
REPORT_FIELDS = [
    "checked_at_utc",
    "syllabus_id",
    "offering_id",
    "year",
    "term_code",
    "status",
    "http_status",
    "content_type",
    "content_length",
    "pdf_signature",
    "final_url",
    "error",
    "source_url",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Check public KHU syllabus URLs by reading only the first response "
            "bytes; HTML or PDF responses are not saved."
        )
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="number of evenly spaced links to check (default: 10)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="check every matching link instead of the default sample",
    )
    parser.add_argument("--years", nargs="+", type=int, metavar="YEAR")
    parser.add_argument(
        "--term-codes",
        nargs="+",
        choices=("10", "15", "20", "25"),
        metavar="TERM_CODE",
        help="10=semester 1, 20=semester 2, 15=summer, 25=winter",
    )
    parser.add_argument(
        "--timeout", type=float, default=20.0, help="request timeout in seconds"
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="polite delay between requests in seconds (default: 1.0)",
    )
    return parser.parse_args()


def validate_args(args: argparse.Namespace) -> None:
    if args.limit <= 0:
        raise SystemExit("--limit must be greater than zero")
    if args.timeout <= 0:
        raise SystemExit("--timeout must be greater than zero")
    if args.delay < 0:
        raise SystemExit("--delay must be zero or greater")
    if not args.input.is_file():
        raise SystemExit(f"Input CSV not found: {args.input}")


def url_metadata(url: str) -> tuple[str, str]:
    query = parse_qs(urlparse(url).query)
    return query.get("p_year", [""])[0], query.get("p_term", [""])[0]


def load_candidates(args: argparse.Namespace) -> list[dict[str, str]]:
    with args.input.open(encoding="utf-8-sig", newline="") as file:
        rows = list(csv.DictReader(file))

    required = {"syllabus_id", "offering_id", "source_url"}
    missing = required.difference(rows[0] if rows else {})
    if missing:
        raise SystemExit(f"Input CSV is missing columns: {sorted(missing)}")

    candidates = []
    allowed_years = {str(year) for year in args.years or []}
    allowed_terms = set(args.term_codes or [])
    for row in rows:
        year, term_code = url_metadata(row["source_url"])
        if allowed_years and year not in allowed_years:
            continue
        if allowed_terms and term_code not in allowed_terms:
            continue
        candidates.append({**row, "year": year, "term_code": term_code})
    return candidates


def evenly_spaced_sample(rows: list[dict[str, str]], limit: int) -> list[dict[str, str]]:
    if len(rows) <= limit:
        return rows
    if limit == 1:
        return [rows[0]]
    indexes = {
        round(index * (len(rows) - 1) / (limit - 1))
        for index in range(limit)
    }
    return [rows[index] for index in sorted(indexes)]


def check_link(row: dict[str, str], timeout: float) -> dict[str, str]:
    source_url = row["source_url"]
    result = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "syllabus_id": row["syllabus_id"],
        "offering_id": row["offering_id"],
        "year": row["year"],
        "term_code": row["term_code"],
        "status": "failed",
        "http_status": "",
        "content_type": "",
        "content_length": "",
        "pdf_signature": "false",
        "final_url": "",
        "error": "",
        "source_url": source_url,
    }
    request = Request(
        source_url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/pdf,*/*;q=0.8",
            "Range": "bytes=0-8191",
            "Referer": "https://sugang.khu.ac.kr/",
        },
    )

    try:
        with urlopen(request, timeout=timeout) as response:
            prefix = response.read(8192)
            result["http_status"] = str(response.status)
            result["content_type"] = response.headers.get_content_type()
            result["content_length"] = response.headers.get("Content-Length", "")
            result["final_url"] = response.geturl()

        is_pdf = prefix.lstrip().startswith(b"%PDF-")
        result["pdf_signature"] = str(is_pdf).lower()
        if is_pdf:
            result["status"] = "valid_pdf"
        elif result["content_type"] in {"text/html", "application/xhtml+xml"}:
            html = prefix.decode("utf-8", errors="replace")
            if "강의계획서" in html and "기본정보" in html:
                result["status"] = "valid_syllabus_html"
            else:
                result["status"] = "unexpected_html"
        elif not prefix:
            result["status"] = "empty_response"
        else:
            result["status"] = "unexpected_content"
    except HTTPError as error:
        result["http_status"] = str(error.code)
        result["content_type"] = error.headers.get_content_type()
        result["error"] = str(error)
    except (URLError, TimeoutError, OSError) as error:
        result["error"] = str(error)
    return result


def write_report(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=REPORT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def main() -> int:
    args = parse_args()
    validate_args(args)
    candidates = load_candidates(args)
    if not candidates:
        raise SystemExit("No syllabus links match the selected filters")

    selected = candidates if args.all else evenly_spaced_sample(candidates, args.limit)
    print(f"Checking {len(selected)} of {len(candidates)} matching syllabus links")
    results = []
    for index, row in enumerate(selected, 1):
        result = check_link(row, args.timeout)
        results.append(result)
        print(
            f"[{index}/{len(selected)}] syllabus {row['syllabus_id']}: "
            f"{result['status']}"
        )
        if index < len(selected) and args.delay:
            time.sleep(args.delay)

    write_report(args.output, results)
    valid_statuses = {"valid_pdf", "valid_syllabus_html"}
    valid = sum(row["status"] in valid_statuses for row in results)
    failed = len(results) - valid
    print(f"Valid syllabi: {valid}")
    print(f"Needs review: {failed}")
    print(f"Report: {args.output}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
