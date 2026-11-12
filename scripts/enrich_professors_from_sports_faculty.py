#!/usr/bin/env python3
"""Fill blank professor emails and offices from the 체육대학 faculty pages.

http://sports.khu.ac.kr/02/01_02.php ... 05_02.php
The cards carry no professor code, so rows are matched by name. When several
rows share a name, the row is chosen by the courses it teaches: only a row
that teaches a course also taught by an unambiguously matched 체육대학
professor (e.g. the college's 전공탐색및기업가정신세미나 sections) qualifies.
Only blank emails are filled; an existing email that disagrees with the page
is reported, not overwritten. Offices are taken from the page whenever it
lists one, replacing any existing value. Listed professors missing from
professors.csv (except 명예교수) are appended with a stand-in professor_code
continuing their page's (department's) numbering; see professor_codes.py.
"""

from __future__ import annotations

import csv
import html
import re
from collections import defaultdict
from pathlib import Path
from urllib.request import Request, urlopen

from enrich_professor_emails import valid_email
from enrich_professor_offices import normalized_name, valid_office
from professor_codes import next_department_code


PROJECT_DIR = Path(__file__).resolve().parent.parent
TABLES_DIR = PROJECT_DIR / "processed_data" / "website_tables"
PROFESSORS_PATH = TABLES_DIR / "professors.csv"
OFFERINGS_PATH = TABLES_DIR / "course_offerings.csv"
OFFERING_PROFESSORS_PATH = TABLES_DIR / "offering_professors.csv"
FACULTY_URLS = [f"http://sports.khu.ac.kr/02/{index:02d}_02.php" for index in range(1, 6)]

CARD_PATTERN = re.compile(r'<div class="txt">(.*?)</ul>', re.DOTALL)
NAME_PATTERN = re.compile(r"<h5>(.*?)<span>(.*?)</span>", re.DOTALL)
ROW_PATTERN = re.compile(r"<strong>(.*?)</strong>\s*<span>(.*?)</span>", re.DOTALL)
TAG_PATTERN = re.compile(r"<[^>]+>")
# "체413호 (031-201-2736)": the parenthesised phone number is not part of the office.
PHONE_SUFFIX = re.compile(r"\s*\([\d\s-]+\)\s*$")


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.is_file():
        raise SystemExit(f"Required input not found: {path}")
    with path.open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        return list(reader.fieldnames or []), list(reader)


def text(fragment: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(TAG_PATTERN.sub(" ", fragment))).strip()


def fetch_faculty() -> list[dict[str, str]]:
    faculty = []
    for page_index, url in enumerate(FACULTY_URLS):
        request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(request, timeout=30) as response:
            page = response.read().decode("utf-8")
        for card in CARD_PATTERN.findall(page):
            name_match = NAME_PATTERN.search(card)
            if not name_match:
                continue
            entry = {
                "name": text(name_match.group(1)),
                "title": text(name_match.group(2)),
                "page": page_index,
                "email": "",
                "office": "",
                "courses": "",
            }
            for label, value in ROW_PATTERN.findall(card):
                label = re.sub(r"\s", "", text(label)).lower()
                if label == "e-mail":
                    entry["email"] = text(value).lower()
                elif label == "연구실":
                    entry["office"] = PHONE_SUFFIX.sub("", text(value))
                elif label == "담당과목":
                    entry["courses"] = text(value)
            faculty.append(entry)
    if not faculty:
        raise SystemExit("No professors parsed from the 체육대학 faculty pages")
    return faculty


def main() -> int:
    fields, professors = read_csv(PROFESSORS_PATH)
    _, offerings = read_csv(OFFERINGS_PATH)
    _, offering_professors = read_csv(OFFERING_PROFESSORS_PATH)
    if not {"professor_id", "name", "email", "office"}.issubset(fields):
        raise SystemExit("professors.csv does not contain the required columns")

    course_by_offering = {row["offering_id"]: row["course_code"] for row in offerings}
    courses_by_professor: dict[str, set[str]] = defaultdict(set)
    for row in offering_professors:
        course = course_by_offering.get(row["offering_id"])
        if course:
            courses_by_professor[row["professor_id"]].add(course)
    rows_by_name: dict[str, list[dict[str, str]]] = defaultdict(list)
    for professor in professors:
        rows_by_name[normalized_name(professor["name"])].append(professor)

    faculty = fetch_faculty()
    # Courses taught by faculty whose name identifies exactly one row
    # characterise the college and resolve namesakes below.
    college_courses: set[str] = set()
    for entry in faculty:
        rows = rows_by_name.get(normalized_name(entry["name"]), [])
        if len(rows) == 1:
            college_courses |= courses_by_professor[rows[0]["professor_id"]]

    matched = []
    resolved_namesakes = []
    ambiguous = []
    unmatched = []
    for entry in faculty:
        rows = rows_by_name.get(normalized_name(entry["name"]), [])
        if len(rows) > 1:
            candidates = [
                row for row in rows if courses_by_professor[row["professor_id"]] & college_courses
            ]
            if len(candidates) != 1:
                ambiguous.append((entry, rows))
                continue
            resolved_namesakes.append((entry, candidates[0], rows))
            rows = candidates
        if not rows:
            unmatched.append(entry)
            continue
        matched.append((entry, rows[0]))

    filled_emails = []
    filled_offices = []
    conflicts = []
    for entry, professor in matched:
        label = f"{professor['professor_id']}/{professor['professor_code']}: {entry['name']}"
        existing_email = professor["email"].strip()
        if valid_email(entry["email"]):
            if not existing_email:
                professor["email"] = entry["email"]
                filled_emails.append((label, entry["email"]))
            elif existing_email.lower() != entry["email"]:
                conflicts.append((label, "email", existing_email, entry["email"]))
        existing_office = professor["office"].strip()
        if valid_office(entry["office"]):
            # The page is authoritative for offices: it replaces any other value.
            if existing_office != entry["office"]:
                professor["office"] = entry["office"]
                filled_offices.append((label, existing_office, entry["office"]))

    next_professor_id = max(int(professor["professor_id"]) for professor in professors) + 1
    added = []
    for entry in unmatched:
        if "명예" in entry["title"]:
            continue
        department_codes = [
            professor["professor_code"]
            for matched_entry, professor in matched
            if matched_entry["page"] == entry["page"]
        ] or [professor["professor_code"] for _, professor in matched]
        professor = {field_name: "" for field_name in fields}
        professor.update(
            professor_id=str(next_professor_id),
            professor_code=next_department_code(professors, department_codes),
            name=entry["name"],
            email=entry["email"] if valid_email(entry["email"]) else "",
            office=entry["office"] if valid_office(entry["office"]) else "",
        )
        next_professor_id += 1
        professors.append(professor)
        added.append(professor)

    temporary = PROFESSORS_PATH.with_suffix(".csv.tmp")
    with temporary.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(professors)
    temporary.replace(PROFESSORS_PATH)

    print(f"Faculty page professors: {len(faculty)}")
    print(f"Namesakes resolved by taught courses: {len(resolved_namesakes)}")
    for entry, chosen, rows in resolved_namesakes:
        others = ", ".join(
            f"{row['professor_id']}({','.join(sorted(courses_by_professor[row['professor_id']]))})"
            for row in rows
            if row is not chosen
        )
        print(
            f"  {entry['name']} [{entry['courses']}] -> {chosen['professor_id']}"
            f"({','.join(sorted(courses_by_professor[chosen['professor_id']]))}); not {others}"
        )
    print(f"Blank emails filled: {len(filled_emails)}")
    for label, value in filled_emails:
        print(f"  {label} -> {value!r}")
    print(f"Offices set from the page: {len(filled_offices)}")
    for label, existing, value in filled_offices:
        print(f"  {label} {existing!r} -> {value!r}")
    print(f"Existing values kept despite differing from the page: {len(conflicts)}")
    for label, field, existing, value in conflicts:
        print(f"  {label} {field} kept {existing!r}, page {value!r}")
    print(f"Namesakes left unresolved: {len(ambiguous)}")
    for entry, rows in ambiguous:
        print(f"  {entry['name']}: {[row['professor_id'] for row in rows]}")
    print(f"Added to professors.csv (stand-in professor_code): {len(added)}")
    for professor in added:
        print(
            f"  {professor['professor_id']}/{professor['professor_code']}: {professor['name']} "
            f"{professor['email']!r} {professor['office']!r}"
        )
    print(f"Output: {PROFESSORS_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
