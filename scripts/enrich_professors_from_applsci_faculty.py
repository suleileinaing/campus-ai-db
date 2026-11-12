#!/usr/bin/env python3
"""Fill blank professor emails and offices from the 응용과학대학 faculty boards.

Both the college site and each department site publish their faculty as
free-form board posts (BMSR00047); every card of a person is merged:

* applsci.khu.ac.kr menuNo 3200070/3200072/3200074/3200076 (college site)
* math.khu.ac.kr (응용수학과, also lists 연구실), applchem.khu.ac.kr,
  physics.khu.ac.kr and space.khu.ac.kr

The cards carry no professor code field, but many photos are uploaded as
"<professor_code>.jpg". When such a code is known, the row must have that
code and name. Otherwise rows are matched by name and confirmed by courses:

* Anchors are uniquely named matches that teach the college's own courses
  (AMTH/APHY/APCH course codes).
* Any other match must share a course with an anchor, or teach a
  전공탐색및기업가정신세미나 section within SEMINAR_SECTION_WINDOW of an
  anchor's section in the same term (the college's block of sections).

A row whose email equals the sites' is also accepted, which keeps the rows
appended below matched on later runs.

Only blank emails are filled; offices are taken from the sites whenever they
list one, replacing any existing value. When the sites
publish different addresses for one person, an official khu.ac.kr address
is preferred, then the department site's address over the college site's;
if several addresses still remain, the email is not filled.

Listed professors missing from professors.csv (except 명예교수) are appended,
as is a person whose photo code differs from every same-named row, or whose
same-named rows all carry another email (they are other people). They get
their photo code, or else a stand-in professor_code continuing their
department's numbering (professor_codes.py).
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
# (board list URL, menuNo, department); the college site comes first.
FACULTY_BOARDS = [
    ("https://applsci.khu.ac.kr/applsci/user/bbs/BMSR00047/list.do", "3200070", "응용수학과"),
    ("https://applsci.khu.ac.kr/applsci/user/bbs/BMSR00047/list.do", "3200072", "응용물리학과"),
    ("https://applsci.khu.ac.kr/applsci/user/bbs/BMSR00047/list.do", "3200074", "응용화학과"),
    ("https://applsci.khu.ac.kr/applsci/user/bbs/BMSR00047/list.do", "3200076", "우주과학과"),
    ("https://math.khu.ac.kr/math/user/bbs/BMSR00047/list.do", "3100029", "응용수학과"),
    ("https://applchem.khu.ac.kr/applchem/user/bbs/BMSR00047/list.do", "2900010", "응용화학과"),
    ("https://physics.khu.ac.kr/physics/user/bbs/BMSR00047/list.do", "3000060", "응용물리학과"),
    ("https://space.khu.ac.kr/space/user/bbs/BMSR00047/list.do", "2800123", "우주과학과"),
]
COLLEGE_SITE = "https://applsci.khu.ac.kr/"
COLLEGE_COURSE_PREFIXES = ("AMTH", "APHY", "APCH")
SEMINAR_CODE = "GEE1952"
SEMINAR_SECTION_WINDOW = 2

NAME_PATTERN = re.compile(r'<div class="name">(.*?)</div>', re.DOTALL)
PHOTO_CODE_PATTERN = re.compile(r'<img[^>]*\balt="(\d{6})\.\w+"')
# Field values run until the next field label; emails are sometimes split by
# stray spaces in the board HTML ("kyusung.hwang@k hu. ac.kr").
EMAIL_FIELD_PATTERN = re.compile(
    r"(?:이메일|E-MAIL)\s*(.*?)\s*(?=홈페이지|HOMEPAGE|HOMPAGE|연구실|Research|TEL|전화번호|NAME|\||$)",
    re.IGNORECASE,
)
# "연구실 전423호", "연구실 우7062호"; lab names under HOMEPAGE are not offices.
OFFICE_PATTERN = re.compile(r"연구실\s*([가-힣]{0,6}\s*[\d-]+호)")
TAG_PATTERN = re.compile(r"<[^>]+>")


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.is_file():
        raise SystemExit(f"Required input not found: {path}")
    with path.open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        return list(reader.fieldnames or []), list(reader)


def text(fragment: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(TAG_PATTERN.sub(" ", fragment))).strip()


def fetch_faculty() -> list[dict]:
    people: dict[tuple[str, str], dict] = {}
    for url, menu_no, department in FACULTY_BOARDS:
        query = {"menuNo": menu_no, "pageIndex": "1", "pageUnit": "100"}
        request = Request(f"{url}?{urlencode(query)}", headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(request, timeout=30) as response:
            page = response.read().decode("utf-8")
        cards = 0
        for item in page.split('<li class="item">')[1:]:
            name_match = NAME_PATTERN.search(item)
            if not name_match:
                continue
            item = item.split("btn-more")[0]
            heading = text(name_match.group(1))
            name = re.sub(r"\s*(?:명예)?\s*교수$", "", heading)
            person = people.setdefault(
                (normalized_name(name), department),
                {
                    "name": name,
                    "department": department,
                    "codes": set(),
                    "emails": set(),
                    "department_emails": set(),
                    "offices": set(),
                    "emeritus": False,
                },
            )
            person["emeritus"] |= "명예" in heading
            if code_match := PHOTO_CODE_PATTERN.search(item):
                person["codes"].add(code_match.group(1))
            card_text = text(item)
            if email_match := EMAIL_FIELD_PATTERN.search(card_text):
                email = re.sub(r"\s", "", email_match.group(1)).lower()
                if valid_email(email):
                    person["emails"].add(email)
                    if not url.startswith(COLLEGE_SITE):
                        person["department_emails"].add(email)
            if office_match := OFFICE_PATTERN.search(card_text):
                person["offices"].add(re.sub(r"\s", "", office_match.group(1)))
            cards += 1
        if not cards:
            raise SystemExit(f"No professors parsed from {url}?menuNo={menu_no}")
    return list(people.values())


def site_emails(person: dict) -> set[str]:
    emails = person["emails"]
    official = {email for email in emails if email.endswith(OFFICIAL_DOMAIN)}
    emails = official or emails
    if len(emails) > 1 and emails & person["department_emails"]:
        emails &= person["department_emails"]
    return emails


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

    def courses(professor: dict[str, str]) -> set[str]:
        return {row["course_code"] for row in offerings_by_professor[professor["professor_id"]]}

    def seminar_sections(professor: dict[str, str]) -> set[tuple[str, str, int]]:
        return {
            (row["year"], row["semester"], number)
            for row in offerings_by_professor[professor["professor_id"]]
            if row["course_code"] == SEMINAR_CODE
            and (number := section_number(row["section"])) is not None
        }

    faculty = fetch_faculty()
    anchors = []
    for person in faculty:
        rows = rows_by_name.get(normalized_name(person["name"]), [])
        if len(rows) == 1 and any(
            code.startswith(COLLEGE_COURSE_PREFIXES) for code in courses(rows[0])
        ):
            anchors.append(rows[0])
    anchor_ids = {row["professor_id"] for row in anchors}
    college_courses = set().union(*(courses(row) for row in anchors)) - {SEMINAR_CODE}
    college_seminar_sections = set().union(*(seminar_sections(row) for row in anchors))

    def belongs_to_college(professor: dict[str, str]) -> bool:
        if professor["professor_id"] in anchor_ids or courses(professor) & college_courses:
            return True
        return any(
            year == anchor_year
            and semester == anchor_semester
            and abs(number - anchor_number) <= SEMINAR_SECTION_WINDOW
            for year, semester, number in seminar_sections(professor)
            for anchor_year, anchor_semester, anchor_number in college_seminar_sections
        )

    def course_list(professor: dict[str, str]) -> str:
        return ",".join(sorted(courses(professor))) or "-"

    matched = []
    namesakes = []
    code_mismatches = []
    rejected = []
    unmatched = []
    for person in faculty:
        rows = rows_by_name.get(normalized_name(person["name"]), [])
        if not rows:
            unmatched.append(person)
            continue
        if person["codes"]:
            candidates = [row for row in rows if row["professor_code"] in person["codes"]]
            if not candidates:
                code_mismatches.append((person, rows))
                continue
        else:
            candidates = [
                row
                for row in rows
                if belongs_to_college(row) or row["email"].strip().lower() in person["emails"]
            ]
        if not candidates and person["emails"] and all(
            row["email"].strip() and row["email"].strip().lower() not in person["emails"]
            for row in rows
        ):
            code_mismatches.append((person, rows))
            continue
        if len(candidates) != 1:
            rejected.append((person, rows))
            continue
        if len(rows) > 1:
            namesakes.append((person, candidates[0], rows))
        matched.append((person, candidates[0]))

    filled_emails = []
    filled_offices = []
    already = 0
    conflicts = []
    for person, professor in matched:
        label = f"{professor['professor_id']}/{professor['professor_code']}: {person['department']} {person['name']}"
        emails = site_emails(person)
        existing = professor["email"].strip()
        if len(emails) == 1:
            (email,) = emails
            if not existing:
                professor["email"] = email
                filled_emails.append((label, email))
            elif existing.lower() == email:
                already += 1
            else:
                conflicts.append((label, "email", existing, email))
        elif len(emails) > 1:
            conflicts.append((label, "email", existing, " / ".join(sorted(emails))))

        offices = {office for office in person["offices"] if valid_office(office)}
        existing_office = professor["office"].strip()
        if len(offices) == 1:
            (office,) = offices
            if existing_office != office:
                professor["office"] = office
                filled_offices.append((label, existing_office, office))

    next_professor_id = max(int(professor["professor_id"]) for professor in professors) + 1
    added = []
    additions = unmatched + [person for person, _ in code_mismatches]
    # Photo codes go first so that no stand-in takes one of them.
    for person in sorted(additions, key=lambda person: not person["codes"]):
        if person["emeritus"]:
            continue
        department_codes = [
            professor["professor_code"]
            for matched_person, professor in matched
            if matched_person["department"] == person["department"]
        ] or [professor["professor_code"] for _, professor in matched]
        emails = site_emails(person)
        offices = {office for office in person["offices"] if valid_office(office)}
        professor = {field_name: "" for field_name in fields}
        professor.update(
            professor_id=str(next_professor_id),
            professor_code=min(person["codes"])
            if person["codes"]
            else next_department_code(professors, department_codes),
            name=person["name"],
            email=next(iter(emails)) if len(emails) == 1 else "",
            office=next(iter(offices)) if len(offices) == 1 else "",
        )
        next_professor_id += 1
        professors.append(professor)
        added.append((person, professor))

    temporary = PROFESSORS_PATH.with_suffix(".csv.tmp")
    with temporary.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(professors)
    temporary.replace(PROFESSORS_PATH)

    print(f"Faculty board professors: {len(faculty)} (anchors: {len(anchors)})")
    print(f"Matched: {len(matched)} ({sum(bool(p['codes']) for p, _ in matched)} confirmed by photo code)")
    print(f"Namesakes resolved: {len(namesakes)}")
    for person, chosen, rows in namesakes:
        others = ", ".join(
            f"{row['professor_id']}({course_list(row)})" for row in rows if row is not chosen
        )
        print(f"  {person['name']} -> {chosen['professor_id']}({course_list(chosen)}); not {others}")
    print(f"Blank emails filled: {len(filled_emails)}")
    for label, value in filled_emails:
        print(f"  {label} -> {value!r}")
    print(f"Offices set from the sites: {len(filled_offices)}")
    for label, existing, value in filled_offices:
        print(f"  {label} {existing!r} -> {value!r}")
    print(f"Emails already matching the sites: {already}")
    print(f"Existing or conflicting values left unchanged: {len(conflicts)}")
    for label, field, existing, value in conflicts:
        print(f"  {label} {field} kept {existing!r}, sites {value!r}")
    print(f"Name matches that are other people (code or email differs): {len(code_mismatches)}")
    for person, rows in code_mismatches:
        details = ", ".join(
            f"{row['professor_id']}/{row['professor_code']} {row['email']}" for row in rows
        )
        print(f"  {person['department']} {person['name']} photo code {sorted(person['codes'])}: {details}")
    print(f"Name matches not confirmed by taught courses: {len(rejected)}")
    for person, rows in rejected:
        details = ", ".join(f"{row['professor_id']}({course_list(row)})" for row in rows)
        print(f"  {person['department']} {person['name']}: {details}")
    print(f"Added to professors.csv: {len(added)}")
    for person, professor in added:
        source = "photo code" if person["codes"] else "stand-in code"
        print(
            f"  {professor['professor_id']}/{professor['professor_code']} ({source}): "
            f"{person['department']} {person['name']} {professor['email']!r} {professor['office']!r}"
        )
    print(f"Output: {PROFESSORS_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
