#!/usr/bin/env python3
"""Fill professor offices from already-extracted public syllabus details."""

from __future__ import annotations

import csv
import re
from collections import defaultdict
from pathlib import Path
from urllib.parse import parse_qs, urlparse


PROJECT_DIR = Path(__file__).resolve().parent.parent
PROFESSORS_PATH = PROJECT_DIR / "processed_data" / "website_tables" / "professors.csv"
DETAILS_PATH = PROJECT_DIR / "processed_data" / "syllabus_tables" / "syllabus_details.csv"
TERM_ORDER = {"10": 1, "15": 2, "20": 3, "25": 4}
OFFICE_PLACEHOLDERS = {
    "-",
    ".",
    "없음",
    "미정",
    "로그인 하세요",
    "로그인 하세요.",
    "로그인하세요",
    "해당사항없음",
}

OFFICE_HINTS = (
    "호",
    "관",
    "건물",
    "대학",
    "연구실",
    "사무실",
    "센터",
    "room",
    "building",
    "center",
    "laboratory",
    "lab",
)


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.is_file():
        raise SystemExit(f"Required input not found: {path}")
    with path.open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        return list(reader.fieldnames or []), list(reader)


def url_value(url: str, key: str) -> str:
    return parse_qs(urlparse(url).query).get(key, [""])[0]


def detail_sort_key(row: dict[str, str]) -> tuple[int, int, int]:
    year = row.get("year") or url_value(row["source_url"], "p_year")
    term = row.get("term_code") or url_value(row["source_url"], "p_term")
    return int(year or 0), TERM_ORDER.get(term, 0), int(row["syllabus_id"])


def valid_office(value: str) -> bool:
    value = value.strip()
    lowered = value.lower()
    if not value or lowered in {item.lower() for item in OFFICE_PLACEHOLDERS}:
        return False
    if "nowhere" in lowered or "temporally" in lowered:
        return False
    # A phone number or email address alone is contact information, not an office.
    if "@" in value and not any(hint in lowered for hint in OFFICE_HINTS):
        return False
    if re.fullmatch(r"[\d\s()+./-]+", value):
        return "호" in value
    return any(hint in lowered for hint in OFFICE_HINTS)


def normalized_name(value: str) -> str:
    return re.sub(r"\s+", "", value).casefold()


def main() -> int:
    fields, professors = read_csv(PROFESSORS_PATH)
    _, details = read_csv(DETAILS_PATH)
    required_professor_fields = {"professor_code", "name", "email", "office"}
    required_detail_fields = {
        "syllabus_id",
        "year",
        "term_code",
        "professor_name",
        "professor_office",
        "source_url",
    }
    if not required_professor_fields.issubset(fields):
        raise SystemExit("professors.csv does not contain the required columns")
    if details and not required_detail_fields.issubset(details[0]):
        raise SystemExit("syllabus_details.csv does not contain the required columns")

    professors_per_code: dict[str, int] = defaultdict(int)
    for professor in professors:
        professors_per_code[professor["professor_code"]] += 1

    candidates_by_code: dict[str, list[dict[str, str]]] = defaultdict(list)
    candidates_by_code_name: dict[tuple[str, str], list[dict[str, str]]] = (
        defaultdict(list)
    )
    rejected_candidates = 0
    for detail in details:
        professor_code = url_value(detail["source_url"], "p_teach")
        office = detail["professor_office"].strip()
        if professor_code and valid_office(office):
            candidates_by_code[professor_code].append(detail)
            professor_name = normalized_name(detail["professor_name"])
            if professor_name:
                candidates_by_code_name[(professor_code, professor_name)].append(detail)
        elif professor_code and office:
            rejected_candidates += 1
    for rows in candidates_by_code.values():
        rows.sort(key=detail_sort_key, reverse=True)
    for rows in candidates_by_code_name.values():
        rows.sort(key=detail_sort_key, reverse=True)

    filled = 0
    preserved = 0
    missing = []
    for professor in professors:
        existing_office = professor["office"].strip()
        if valid_office(existing_office):
            professor["office"] = existing_office
            preserved += 1
            continue

        professor_code = professor["professor_code"]
        matches = candidates_by_code_name.get(
            (professor_code, normalized_name(professor["name"])), []
        )
        # A code-only fallback is safe only when the code identifies one professor.
        if not matches and professors_per_code[professor_code] == 1:
            matches = candidates_by_code.get(professor_code, [])
        if matches:
            professor["office"] = matches[0]["professor_office"].strip()
            filled += 1
        else:
            professor["office"] = ""
            missing.append((professor_code, professor["name"]))

    temporary = PROFESSORS_PATH.with_suffix(".csv.tmp")
    with temporary.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(professors)
    temporary.replace(PROFESSORS_PATH)

    print(f"Professors: {len(professors)}")
    print(f"Existing valid offices preserved: {preserved}")
    print(f"Previously blank/invalid offices populated: {filled}")
    print(f"Rejected non-office syllabus values: {rejected_candidates}")
    print(f"Office unavailable: {len(missing)}")
    for code, name in missing:
        print(f"  {code}: {name}")
    print("Email values were left unchanged.")
    print(f"Output: {PROFESSORS_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
