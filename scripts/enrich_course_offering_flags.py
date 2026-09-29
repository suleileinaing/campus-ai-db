#!/usr/bin/env python3
"""Add industry-required and English-course flags to course offerings."""

from __future__ import annotations

import csv
import json
import re
from collections import defaultdict
from pathlib import Path

from website_json_to_csv import ENGLISH_TYPE_NAMES, clean, parse_section


PROJECT_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_DIR / "raw_data" / "course_lists"
OFFERINGS_PATH = (
    PROJECT_DIR / "processed_data" / "website_tables" / "course_offerings.csv"
)
FILE_PATTERN = re.compile(
    r"^(?P<year>\d{4})-(?P<semester>[^_]+)_(?P<major>[^_]+)_raw\.json$"
)


def offering_key(
    year: str, semester: str, course_code: str, section: str
) -> tuple[str, str, str, str]:
    return year, semester, course_code, section


def main() -> int:
    grouped: dict[tuple[str, str, str, str], list[dict]] = defaultdict(list)
    for path in sorted(RAW_DIR.glob("*_raw.json")):
        match = FILE_PATTERN.match(path.name)
        if not match:
            continue
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
        for row in payload.get("rows", []):
            key = offering_key(
                match.group("year"),
                match.group("semester"),
                clean(row.get("subjt_cd")),
                parse_section(row),
            )
            grouped[key].append(row)

    with OFFERINGS_PATH.open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        source_fields = list(reader.fieldnames or [])
        offerings = list(reader)

    insert_at = source_fields.index("capacity") + 1
    fields = [
        field
        for field in source_fields
        if field not in {"industry_required", "english_type"}
    ]
    insert_at = fields.index("capacity") + 1
    fields[insert_at:insert_at] = ["industry_required", "english_type"]

    missing = []
    industry_count = 0
    english_counts = {"NONE": 0, "PARTIAL": 0, "FULL": 0}
    for offering in offerings:
        key = offering_key(
            offering["year"],
            offering["semester"],
            offering["course_code"],
            offering["section"],
        )
        rows = grouped.get(key, [])
        if not rows:
            missing.append(key)
            continue

        industry_required = any(
            re.search(r"산학\s*필수", clean(row.get("bigo"))) is not None
            for row in rows
        )
        raw_english = {clean(row.get("eng_yn_nm")) for row in rows}
        unknown = raw_english.difference(ENGLISH_TYPE_NAMES)
        if unknown:
            raise SystemExit(f"{key}: unknown eng_yn_nm values {sorted(unknown)!r}")
        normalized = {ENGLISH_TYPE_NAMES[value] for value in raw_english}
        english_type = (
            "FULL" if "FULL" in normalized
            else "PARTIAL" if "PARTIAL" in normalized
            else "NONE"
        )

        offering["industry_required"] = "1" if industry_required else "0"
        offering["english_type"] = english_type
        industry_count += industry_required
        english_counts[english_type] += 1

    if missing:
        raise SystemExit(f"No raw-data match for {len(missing)} offerings: {missing[:10]}")

    temporary = OFFERINGS_PATH.with_suffix(".csv.tmp")
    with temporary.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows({field: row.get(field, "") for field in fields} for row in offerings)
    temporary.replace(OFFERINGS_PATH)

    print(f"Offerings: {len(offerings)}")
    print(f"Industry-required: {industry_count}")
    for english_type in ("NONE", "PARTIAL", "FULL"):
        print(f"English {english_type}: {english_counts[english_type]}")
    print(f"Output: {OFFERINGS_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
