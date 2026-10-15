#!/usr/bin/env python3
"""Fill professor emails and offices from the 생명과학대학 faculty board.

https://cls.khu.ac.kr/cls/user/bbs/BMSR00047/list.do, one menuNo per
department (BOARD_MENUS). Professors holding joint appointments appear on
several tabs; their cards are merged. 명예교수 cards are skipped.

Cards list 연구실, 실험실 and 이메일 but no professor code or courses, so rows
are matched by name and accepted only when one of these confirms the person:

* the row's existing office has the room number of the card's 연구실 or 실험실;
* the row shares a course (other than 전공탐색및기업가정신세미나) with a
  confirmed professor, or teaches a 전공탐색및기업가정신세미나 section within
  SEMINAR_SECTION_WINDOW of a confirmed professor's section in the same term.
  Professors confirmed this way confirm others in turn, until nothing changes.

Exactly one row must be confirmed, otherwise nothing is filled. Offices
(the card's 연구실) replace any existing value; emails fill blanks only and
differing emails are reported. Listed professors missing from professors.csv
are appended with a blank department_id (departments.csv has no 생명과학대학
departments) and, since the board publishes no code, a stand-in
professor_code continuing their department's numbering (professor_codes.py).
"""

from __future__ import annotations

import csv
import html
import re
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from enrich_professor_emails import OFFICIAL_DOMAIN, valid_email
from enrich_professor_offices import normalized_name, valid_office
from professor_codes import next_department_code


PROJECT_DIR = Path(__file__).resolve().parent.parent
TABLES_DIR = PROJECT_DIR / "processed_data" / "website_tables"
PROFESSORS_PATH = TABLES_DIR / "professors.csv"
OFFERINGS_PATH = TABLES_DIR / "course_offerings.csv"
OFFERING_PROFESSORS_PATH = TABLES_DIR / "offering_professors.csv"
BOARD_URL = "https://cls.khu.ac.kr/cls/user/bbs/BMSR00047/list.do"
BOARD_MENUS = {
    "11600082": "스마트팜과학과",
    "11600087": "식물환경신소재공학과",
    "11600089": "식품생명공학과",
    "11600091": "원예생명공학과",
    "11600093": "유전생명공학과",
    "11600095": "한방생명공학과",
    "11600131": "융합바이오신소재공학과",
}
SEMINAR_CODE = "GEE1952"
SEMINAR_SECTION_WINDOW = 2

NAME_PATTERN = re.compile(r'<div class="name">(.*?)</div>', re.DOTALL)
FIELD_PATTERN = r"{label}\s*(.*?)\s*(?=학과|연구실|실험실|홈페이지|연락처|이메일|연구업적|$)"
EMAIL_FIELD = re.compile(FIELD_PATTERN.format(label="이메일"))
OFFICE_FIELD = re.compile(FIELD_PATTERN.format(label="연구실"))
LAB_FIELD = re.compile(FIELD_PATTERN.format(label="실험실"))
ROOM_PATTERN = re.compile(r"(\d+(?:-\d+)?)\s*호")
TAG_PATTERN = re.compile(r"<[^>]+>")


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.is_file():
        raise SystemExit(f"Required input not found: {path}")
    with path.open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        return list(reader.fieldnames or []), list(reader)


def text(fragment: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(TAG_PATTERN.sub(" ", fragment))).strip()


def field(pattern: re.Pattern, card_text: str) -> str:
    match = pattern.search(card_text)
    value = match.group(1).strip() if match else ""
    return "" if value == "-" else value


def rooms(value: str) -> set[str]:
    return set(ROOM_PATTERN.findall(value))


def fetch_faculty() -> tuple[list[dict], list[str]]:
    people: dict[str, dict] = {}
    emeriti = []
    for menu_no, department in BOARD_MENUS.items():
        query = {"menuNo": menu_no, "pageIndex": "1", "pageUnit": "100"}
        request = Request(f"{BOARD_URL}?{urlencode(query)}", headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(request, timeout=60) as response:
            page = response.read().decode("utf-8")
        cards = 0
        for item in page.split('<li class="item">')[1:]:
            name_match = NAME_PATTERN.search(item)
            if not name_match:
                continue
            cards += 1
            heading = text(name_match.group(1))
            # "권춘탁(Choon-Tak Kwon) 교수", "한정우(Jungwoo Hahn)교수"
            name = re.sub(r"\s*\(.*$|\s*교수$", "", heading).strip()
            if "명예" in heading:
                emeriti.append(name)
                continue
            card_text = text(item.split('<a href="javascript')[0])
            entry = people.setdefault(
                normalized_name(name),
                {"name": name, "departments": [], "email": "", "office": "", "lab": ""},
            )
            entry["departments"].append(department)
            emails = [
                email.lower()
                for email in re.split(r"[\s/,]+", field(EMAIL_FIELD, card_text))
                if valid_email(email)
            ]
            official = [email for email in emails if email.endswith(OFFICIAL_DOMAIN)]
            # A joint appointee's card on another tab may leave fields empty.
            for key, value in (
                ("email", (official or emails or [""])[0]),
                ("office", field(OFFICE_FIELD, card_text)),
                ("lab", field(LAB_FIELD, card_text)),
            ):
                if value and not entry[key]:
                    entry[key] = value
        if not cards:
            raise SystemExit(f"No professors parsed from {BOARD_URL}?menuNo={menu_no}")
    return list(people.values()), emeriti


def section_number(section: str) -> int | None:
    digits = re.sub(r"\D", "", section)
    return int(digits) if digits else None


def main() -> int:
    fields, professors = read_csv(PROFESSORS_PATH)
    _, offerings = read_csv(OFFERINGS_PATH)
    _, offering_professors = read_csv(OFFERING_PROFESSORS_PATH)
    if not {"professor_id", "professor_code", "name", "email", "office"}.issubset(fields):
        raise SystemExit("professors.csv does not contain the required columns")

    offering_by_id = {row["offering_id"]: row for row in offerings}
    offerings_by_professor: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in offering_professors:
        offering = offering_by_id.get(row["offering_id"])
        if offering:
            offerings_by_professor[row["professor_id"]].append(offering)
    rows_by_name: dict[str, list[dict[str, str]]] = defaultdict(list)
    for professor in professors:
        rows_by_name[normalized_name(professor["name"])].append(professor)

    def taught(professor: dict[str, str]) -> list[dict[str, str]]:
        return offerings_by_professor[professor["professor_id"]]

    def seminar_sections(professor: dict[str, str]) -> set[tuple[str, str, int]]:
        return {
            (row["year"], row["semester"], number)
            for row in taught(professor)
            if row["course_code"] == SEMINAR_CODE
            and (number := section_number(row["section"])) is not None
        }

    faculty, emeriti = fetch_faculty()
    candidates_by_entry = [
        (entry, rows_by_name.get(normalized_name(entry["name"]), [])) for entry in faculty
    ]
    confirmed: dict[str, dict[str, str]] = {}

    def evidence(entry: dict, professor: dict[str, str]) -> str:
        if rooms(entry["office"] + " " + entry["lab"]) & rooms(professor["office"]):
            return "office"
        others = [other for other in confirmed.values() if other is not professor]
        own_courses = {row["course_code"] for row in taught(professor)} - {SEMINAR_CODE}
        if any(own_courses & {row["course_code"] for row in taught(other)} for other in others):
            return "shared course"
        other_sections = set().union(*(seminar_sections(other) for other in others))
        if any(
            year == other_year
            and semester == other_semester
            and abs(number - other_number) <= SEMINAR_SECTION_WINDOW
            for year, semester, number in seminar_sections(professor)
            for other_year, other_semester, other_number in other_sections
        ):
            return "seminar block"
        return ""

    while True:
        newly_confirmed = {
            row["professor_id"]: row
            for entry, rows in candidates_by_entry
            for row in rows
            if row["professor_id"] not in confirmed and evidence(entry, row)
        }
        if not newly_confirmed:
            break
        confirmed.update(newly_confirmed)

    def course_list(professor: dict[str, str]) -> str:
        return ",".join(sorted({row["course_name"] for row in taught(professor)})) or "-"

    matched = []
    namesakes = []
    rejected = []
    unmatched = []
    for entry, rows in candidates_by_entry:
        if not rows:
            unmatched.append(entry)
            continue
        candidates = [(row, found) for row in rows if (found := evidence(entry, row))]
        if len(candidates) != 1:
            rejected.append((entry, rows, candidates))
            continue
        professor, found = candidates[0]
        if len(rows) > 1:
            namesakes.append((entry, professor, found, rows))
        matched.append((entry, professor))

    filled_emails = []
    filled_offices = []
    conflicts = []
    for entry, professor in matched:
        label = f"{professor['professor_id']}/{professor['professor_code']}: {entry['name']}"
        existing = professor["email"].strip()
        if valid_email(entry["email"]) and existing.lower() != entry["email"]:
            if not existing:
                professor["email"] = entry["email"]
                filled_emails.append((label, entry["email"]))
            else:
                conflicts.append((label, "email", existing, entry["email"]))
        existing_office = professor["office"].strip()
        # The board is authoritative for offices: it replaces any other value.
        if valid_office(entry["office"]) and existing_office != entry["office"]:
            professor["office"] = entry["office"]
            filled_offices.append((label, existing_office, entry["office"]))

    next_professor_id = max(int(professor["professor_id"]) for professor in professors) + 1
    added = []
    for entry in unmatched:
        department_codes = [
            professor["professor_code"]
            for matched_entry, professor in matched
            if set(matched_entry["departments"]) & set(entry["departments"])
        ] or [professor["professor_code"] for _, professor in matched]
        professor = {field_name: "" for field_name in fields}
        professor.update(
            professor_id=str(next_professor_id),
            professor_code=next_department_code(professors, department_codes),
            name=entry["name"],
            email=entry["email"],
            office=entry["office"] if valid_office(entry["office"]) else "",
        )
        next_professor_id += 1
        professors.append(professor)
        added.append((entry, professor))

    temporary = PROFESSORS_PATH.with_suffix(".csv.tmp")
    with temporary.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(professors)
    temporary.replace(PROFESSORS_PATH)

    print(f"Faculty board professors: {len(faculty)} (명예교수 skipped: {len(emeriti)})")
    print(f"Matched: {len(matched)}")
    print(f"Namesakes resolved: {len(namesakes)}")
    for entry, chosen, found, rows in namesakes:
        others = ", ".join(
            f"{row['professor_id']}({course_list(row)})" for row in rows if row is not chosen
        )
        print(
            f"  {entry['name']} -> {chosen['professor_id']}({course_list(chosen)}; by {found}); "
            f"not {others}"
        )
    print(f"Blank emails filled: {len(filled_emails)}")
    for label, value in filled_emails:
        print(f"  {label} -> {value!r}")
    print(f"Offices set from the board: {len(filled_offices)}")
    for label, existing, value in filled_offices:
        print(f"  {label} {existing!r} -> {value!r}")
    print(f"Existing emails kept despite differing from the board: {len(conflicts)}")
    for label, field_name, existing, value in conflicts:
        print(f"  {label} {field_name} kept {existing!r}, board {value!r}")
    print(f"Name matches not confirmed or not unique (left unchanged): {len(rejected)}")
    for entry, rows, candidates in rejected:
        details = ", ".join(
            f"{row['professor_id']}/{row['professor_code']}({course_list(row)})" for row in rows
        )
        print(f"  {'/'.join(entry['departments'])} {entry['name']} confirmed {len(candidates)}: {details}")
    print(f"Added to professors.csv (stand-in professor_code): {len(added)}")
    for entry, professor in added:
        print(
            f"  {professor['professor_id']}/{professor['professor_code']}: "
            f"{'/'.join(entry['departments'])} {entry['name']} "
            f"{professor['email']!r} {professor['office']!r}"
        )
    print(f"Output: {PROFESSORS_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
