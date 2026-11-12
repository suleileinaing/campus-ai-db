#!/usr/bin/env python3
"""Fill professor emails and offices from the 컴퓨터공학부 faculty page.

https://ce.khu.ac.kr/ce25/user/bbs/BMSR00047/list.do?menuNo=21600011
The page is authoritative: its values replace blank or differing ones. A
professors.csv row is matched by name and confirmed by the courses it teaches,
so namesakes in other departments are left alone.
"""

from __future__ import annotations

import csv
import html
import re
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from enrich_professor_emails import valid_email
from enrich_professor_offices import normalized_name, valid_office


PROJECT_DIR = Path(__file__).resolve().parent.parent
PROFESSORS_PATH = PROJECT_DIR / "processed_data" / "website_tables" / "professors.csv"
DEPARTMENTS_PATH = PROJECT_DIR / "processed_data" / "website_tables" / "departments.csv"
OFFERINGS_PATH = PROJECT_DIR / "processed_data" / "website_tables" / "course_offerings.csv"
OFFERING_PROFESSORS_PATH = (
    PROJECT_DIR / "processed_data" / "website_tables" / "offering_professors.csv"
)
COURSES_PATH = PROJECT_DIR / "processed_data" / "website_tables" / "courses.csv"
FACULTY_URL = "https://ce.khu.ac.kr/ce25/user/bbs/BMSR00047/list.do"
FACULTY_QUERY = {"menuNo": "21600011", "pageIndex": "1", "pageUnit": "100"}
COLLEGE_NAME = "소프트웨어융합대학"
# The faculty page lists professors of these departments only.
DEPARTMENT_NAMES = {"컴퓨터공학부", "컴퓨터공학과", "인공지능학과"}

COMMENT_PATTERN = re.compile(r"<!--.*?-->", re.DOTALL)
ITEM_PATTERN = re.compile(r'<li class="item">(.*?)</li>', re.DOTALL)
NAME_PATTERN = re.compile(r'<div class="name">(.*?)</div>', re.DOTALL)
ROW_PATTERN = re.compile(r"<th[^>]*>(.*?)</th>\s*<td[^>]*>(.*?)</td>", re.DOTALL)
TAG_PATTERN = re.compile(r"<[^>]+>")


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.is_file():
        raise SystemExit(f"Required input not found: {path}")
    with path.open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        return list(reader.fieldnames or []), list(reader)


def text(fragment: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(TAG_PATTERN.sub(" ", fragment))).strip()


def fetch_faculty() -> list[dict[str, str]]:
    request = Request(
        f"{FACULTY_URL}?{urlencode(FACULTY_QUERY)}",
        headers={"User-Agent": "Mozilla/5.0"},
    )
    with urlopen(request, timeout=30) as response:
        page = response.read().decode("utf-8")
    # Outdated rows are kept in HTML comments; they must not be parsed.
    page = COMMENT_PATTERN.sub("", page)

    faculty = []
    for item in ITEM_PATTERN.findall(page):
        name_match = NAME_PATTERN.search(item)
        if not name_match:
            continue
        # "김성태 부교수 (학부장 / AI 학과장)" -> "김성태"
        entry = {"name": text(name_match.group(1)).split()[0], "email": "", "office": ""}
        for label, value in ROW_PATTERN.findall(item):
            label = re.sub(r"\s|:", "", text(label))
            if label == "이메일":
                entry["email"] = text(value).lower()
            elif label == "연구실":
                entry["office"] = text(value)
        faculty.append(entry)
    if not faculty:
        raise SystemExit(f"No professors parsed from {FACULTY_URL}")
    return faculty


def main() -> int:
    fields, professors = read_csv(PROFESSORS_PATH)
    _, departments = read_csv(DEPARTMENTS_PATH)
    _, courses = read_csv(COURSES_PATH)
    _, offerings = read_csv(OFFERINGS_PATH)
    _, offering_professors = read_csv(OFFERING_PROFESSORS_PATH)
    if not {"professor_id", "department_id", "name", "email", "office"}.issubset(fields):
        raise SystemExit("professors.csv does not contain the required columns")
    department_ids = {
        row["department_id"] for row in departments if row["name"] in DEPARTMENT_NAMES
    }
    college_department_ids = {
        row["department_id"] for row in departments if row["college"] == COLLEGE_NAME
    }
    college_courses = {
        row["course_code"]
        for row in courses
        if row["department_id"] in college_department_ids
    }
    course_by_offering = {row["offering_id"]: row["course_code"] for row in offerings}
    taught: dict[str, set[str]] = defaultdict(set)
    for row in offering_professors:
        course_code = course_by_offering.get(row["offering_id"])
        if course_code:
            taught[row["professor_id"]].add(course_code)

    def same_person(professor: dict[str, str]) -> bool:
        """Tell the faculty member apart from a namesake by the courses taught."""
        courses_taught = taught[professor["professor_id"]]
        if courses_taught:
            return bool(courses_taught & college_courses)
        return professor["department_id"] in department_ids

    rows_by_name: dict[str, list[dict[str, str]]] = defaultdict(list)
    for professor in professors:
        rows_by_name[normalized_name(professor["name"])].append(professor)

    faculty = fetch_faculty()
    changed = {"email": [], "office": []}
    namesakes = []
    unmatched = []
    for entry in faculty:
        rows = []
        for professor in rows_by_name.get(normalized_name(entry["name"]), []):
            if same_person(professor):
                rows.append(professor)
            else:
                namesakes.append(professor)
        if not rows:
            unmatched.append(entry["name"])
            continue
        # The same person may hold several professor codes; update every row.
        # The faculty page is authoritative, so it replaces differing values.
        for professor in rows:
            for field, valid in (("email", valid_email), ("office", valid_office)):
                value = entry[field]
                existing = professor[field].strip()
                if valid(value) and existing != value:
                    professor[field] = value
                    changed[field].append(
                        (professor["professor_code"], entry["name"], existing, value)
                    )

    temporary = PROFESSORS_PATH.with_suffix(".csv.tmp")
    with temporary.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(professors)
    temporary.replace(PROFESSORS_PATH)

    print(f"Faculty page professors: {len(faculty)}")
    for field, rows in changed.items():
        print(f"{field.capitalize()} values set from the page: {len(rows)}")
        for code, name, existing, value in rows:
            print(f"  {code}: {name} {existing!r} -> {value!r}")
    print(f"Namesakes skipped (no {COLLEGE_NAME} courses taught): {len(namesakes)}")
    for professor in namesakes:
        print(f"  {professor['professor_code']}: {professor['name']}")
    print(f"Not found in professors.csv: {len(unmatched)}")
    for name in unmatched:
        print(f"  {name}")
    print(f"Output: {PROFESSORS_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
