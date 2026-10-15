#!/usr/bin/env python3
"""Fill professor emails and offices from the 외국어대학 faculty boards.

https://foreign.khu.ac.kr/foreign_kor/user/bbs/BMSR00047/list.do
menuNo 16500075 (프랑스어학과) ... 16500081 (글로벌커뮤니케이션학부), plus each
department's own site (DEPARTMENT_BOARDS, and 중국어학과's professor list,
which links professor codes). A department site is more current than the
college board, so its values win where both list a person.

Cards list 이메일, 연구실 and 담당과목. When a card links a professor code, the
row must have that code and name. Otherwise rows are matched by name and
accepted only when one of these confirms the person:

* the row's existing office has the same room number as the card;
* a course the row teaches shares a word (Hangul bigram) with 담당과목;
* the row teaches a 전공탐색및기업가정신세미나 section within
  SEMINAR_SECTION_WINDOW of a confirmed professor's section in the same term
  (the college's block of sections), or shares another course with one.
  Professors confirmed this way confirm others in turn, until nothing changes.

A row whose email equals the card's is also accepted, which keeps the rows
appended below matched on later runs.

Exactly one row must be confirmed, otherwise nothing is filled. Offices, and
emails published on a department site, replace any existing value; an email
found only on the college board fills a blank email, and a differing one is
reported. Listed professors missing from professors.csv (except 명예교수) are
appended with their linked professor code (a professor-list link, or an
email address of the form <professor_code>@khu.ac.kr), or else a stand-in
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
BOARD_URL = "https://foreign.khu.ac.kr/foreign_kor/user/bbs/BMSR00047/list.do"
BOARD_MENUS = {
    "16500075": "프랑스어학과",
    "16500076": "스페인어학과",
    "16500077": "러시아어학과",
    "16500078": "중국어학과",
    "16500079": "일본어학과",
    "16500080": "한국어학과",
    "16500081": "글로벌커뮤니케이션학부",
}
# (board list URL, menuNo, department) on the departments' own sites.
DEPARTMENT_BOARDS = [
    ("https://france.khu.ac.kr/france/user/bbs/BMSR00047/list.do", "2600008", "프랑스어학과"),
    ("https://spanish.khu.ac.kr/spanish/user/bbs/BMSR00047/list.do", "2500010", "스페인어학과"),
    ("https://russia.khu.ac.kr/russia/user/bbs/BMSR00047/list.do", "2400008", "러시아어학과"),
    ("https://japanese.khu.ac.kr/japanese/user/bbs/BMSR00047/list.do", "2200011", "일본어학과"),
    ("https://korean.khu.ac.kr/korean/user/bbs/BMSR00047/list.do", "4500008", "한국어학과"),
    (
        "https://deptofenglish.khu.ac.kr/deptofenglish/user/bbs/BMSR00047/list.do",
        "2100009",
        "글로벌커뮤니케이션학부",
    ),
]
# Professor-list template (pfView('<professor_code>')); no offices.
DEPARTMENT_PROFESSOR_LISTS = [
    ("https://com.khu.ac.kr/zhongwen/user/professor/list.do", "2300008", "중국어학과"),
]
SEMINAR_CODE = "GEE1952"
SEMINAR_SECTION_WINDOW = 2
# Bigrams with these particles ("화와", "과목") say nothing about the subject.
BIGRAM_STOP_CHARACTERS = set("와과의및을를이은는")

NAME_PATTERN = re.compile(r'<div class="name">(.*?)</div>', re.DOTALL)
FIELD_PATTERN = r"{label}\s*(.*?)\s*(?=직위|이메일|연락처|연구실|홈페이지|담당과목|\||$)"
EMAIL_FIELD = re.compile(FIELD_PATTERN.format(label="이메일"))
OFFICE_FIELD = re.compile(FIELD_PATTERN.format(label="연구실"))
COURSES_FIELD = re.compile(FIELD_PATTERN.format(label="담당과목"))
TITLE_FIELD = re.compile(FIELD_PATTERN.format(label="직위"))
LIST_NAME_PATTERN = re.compile(r'<div class="name">\s*<strong>(.*?)</strong>', re.DOTALL)
LIST_CODE_PATTERN = re.compile(r"pfView\('(\d+)'\)")
LIST_ROW_PATTERN = re.compile(r"<li><span>(.*?)</span>\s*<span[^>]*>(.*?)</span>", re.DOTALL)
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


def bigrams(value: str) -> set[str]:
    words = re.findall(r"[가-힣]+", value)
    return {
        word[index : index + 2]
        for word in words
        for index in range(len(word) - 1)
        if not BIGRAM_STOP_CHARACTERS & set(word[index : index + 2])
    }


def room_number(value: str) -> str:
    match = ROOM_PATTERN.search(value)
    return match.group(1) if match else ""


def fetch_page(url: str, menu_no: str) -> str:
    query = {"menuNo": menu_no, "pageIndex": "1", "pageUnit": "100"}
    request = Request(f"{url}?{urlencode(query)}", headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")


def pick_email(value: str) -> str:
    # "naw3@naver.com/naw3@khu.ac.kr": prefer the official address.
    emails = [email.lower() for email in re.split(r"[\s/,]+", value) if valid_email(email)]
    official = [email for email in emails if email.endswith(OFFICIAL_DOMAIN)]
    return (official or emails or [""])[0]


def fetch_faculty() -> list[dict]:
    people: dict[tuple[str, str], dict] = {}

    def person(name: str, department: str) -> dict:
        return people.setdefault(
            (normalized_name(name), department),
            {
                "name": name,
                "department": department,
                "codes": set(),
                "email": "",
                "office": "",
                "courses": "",
                "department_email": False,
                "emeritus": False,
            },
        )

    boards = [(BOARD_URL, menu_no, department, False) for menu_no, department in BOARD_MENUS.items()]
    boards += [(url, menu_no, department, True) for url, menu_no, department in DEPARTMENT_BOARDS]
    for url, menu_no, department, is_department_site in boards:
        cards = 0
        for item in fetch_page(url, menu_no).split('<li class="item">')[1:]:
            name_match = NAME_PATTERN.search(item)
            if not name_match:
                continue
            # "문병순(학장)", "황수현(Soo-Hyun Hwang)(학과장)": titles follow the name.
            name = re.sub(r"\s*\(.*$", "", text(name_match.group(1))).strip(" |")
            card_text = text(item.split('<a href="javascript')[0])
            entry = person(name, department)
            entry["emeritus"] |= "명예" in field(TITLE_FIELD, card_text)
            # Department sites come last, so their values replace the board's.
            for key, pattern in (("office", OFFICE_FIELD), ("courses", COURSES_FIELD)):
                if value := field(pattern, card_text):
                    entry[key] = value
            if email := pick_email(field(EMAIL_FIELD, card_text)):
                entry["email"] = email
                entry["department_email"] = is_department_site
            cards += 1
        if not cards:
            raise SystemExit(f"No professors parsed from {url}?menuNo={menu_no}")

    for url, menu_no, department in DEPARTMENT_PROFESSOR_LISTS:
        cards = 0
        for item in fetch_page(url, menu_no).split('<li class="item">')[1:]:
            name_match = LIST_NAME_PATTERN.search(item)
            code_match = LIST_CODE_PATTERN.search(item)
            if not name_match or not code_match:
                continue
            entry = person(text(name_match.group(1)), department)
            entry["codes"].add(code_match.group(1))
            for label, value in LIST_ROW_PATTERN.findall(item):
                if re.sub(r"\s", "", text(label)) == "이메일" and (email := pick_email(text(value))):
                    entry["email"] = email
                    entry["department_email"] = True
            cards += 1
        if not cards:
            raise SystemExit(f"No professors parsed from {url}?menuNo={menu_no}")
    for entry in people.values():
        # "039716@khu.ac.kr": the address is the professor code.
        if code_match := re.fullmatch(r"(\d{6})@khu\.ac\.kr", entry["email"]):
            entry["codes"].add(code_match.group(1))
    return list(people.values())


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

    def direct_evidence(entry: dict[str, str], professor: dict[str, str]) -> str:
        if entry["email"] and professor["email"].strip().lower() == entry["email"]:
            return "email"
        room = room_number(entry["office"])
        if room and room == room_number(professor["office"]):
            return "office"
        listed = bigrams(entry["courses"])
        if any(bigrams(row["course_name"]) & listed for row in taught(professor)):
            return "courses"
        return ""

    faculty = fetch_faculty()
    candidates_by_entry = [
        (entry, rows_by_name.get(normalized_name(entry["name"]), [])) for entry in faculty
    ]
    confirmed: dict[str, dict[str, str]] = {}

    def evidence(entry: dict[str, str], professor: dict[str, str]) -> str:
        if found := direct_evidence(entry, professor):
            return found
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
        if entry["codes"]:
            candidates = [(row, "code") for row in rows if row["professor_code"] in entry["codes"]]
        else:
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
        label = f"{professor['professor_id']}/{professor['professor_code']}: {entry['department']} {entry['name']}"
        existing = professor["email"].strip()
        if valid_email(entry["email"]) and existing.lower() != entry["email"]:
            if not existing or entry["department_email"]:
                professor["email"] = entry["email"]
                filled_emails.append((label, existing, entry["email"]))
            else:
                conflicts.append((label, "email", existing, entry["email"]))
        existing_office = professor["office"].strip()
        if valid_office(entry["office"]):
            # The page is authoritative for offices: it replaces any other value.
            if existing_office != entry["office"]:
                professor["office"] = entry["office"]
                filled_offices.append((label, existing_office, entry["office"]))

    next_professor_id = max(int(professor["professor_id"]) for professor in professors) + 1
    added = []
    # Linked codes go first so that no stand-in takes one of them.
    for entry in sorted(unmatched, key=lambda entry: not entry["codes"]):
        if entry["emeritus"]:
            continue
        department_codes = [
            professor["professor_code"]
            for matched_entry, professor in matched
            if matched_entry["department"] == entry["department"]
        ] or [professor["professor_code"] for _, professor in matched]
        professor = {field_name: "" for field_name in fields}
        professor.update(
            professor_id=str(next_professor_id),
            professor_code=min(entry["codes"])
            if entry["codes"]
            else next_department_code(professors, department_codes),
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

    print(f"Faculty board professors: {len(faculty)}")
    print(f"Matched: {len(matched)}")
    print(f"Namesakes resolved: {len(namesakes)}")
    for entry, chosen, found, rows in namesakes:
        others = ", ".join(
            f"{row['professor_id']}({course_list(row)})" for row in rows if row is not chosen
        )
        print(
            f"  {entry['name']} [{entry['courses']}] -> {chosen['professor_id']}"
            f"({course_list(chosen)}; by {found}); not {others}"
        )
    print(f"Emails set: {len(filled_emails)}")
    for label, existing, value in filled_emails:
        print(f"  {label} {existing!r} -> {value!r}")
    print(f"Offices set from the board: {len(filled_offices)}")
    for label, existing, value in filled_offices:
        print(f"  {label} {existing!r} -> {value!r}")
    print(f"Existing values kept despite differing from the board: {len(conflicts)}")
    for label, field_name, existing, value in conflicts:
        print(f"  {label} {field_name} kept {existing!r}, board {value!r}")
    print(f"Name matches not confirmed or not unique (left unchanged): {len(rejected)}")
    for entry, rows, candidates in rejected:
        details = ", ".join(
            f"{row['professor_id']}/{row['professor_code']}({course_list(row)})" for row in rows
        )
        print(
            f"  {entry['department']} {entry['name']} [{entry['courses']}] "
            f"confirmed {len(candidates)}: {details}"
        )
    print(f"Added to professors.csv: {len(added)}")
    for entry, professor in added:
        source = "linked code" if entry["codes"] else "stand-in code"
        print(
            f"  {professor['professor_id']}/{professor['professor_code']} ({source}): "
            f"{entry['department']} {entry['name']} {professor['email']!r} {professor['office']!r}"
        )
    emeriti = [entry for entry in unmatched if entry["emeritus"]]
    print(f"명예교수 not added: {len(emeriti)}")
    for entry in emeriti:
        print(f"  {entry['department']} {entry['name']}")
    print(f"Output: {PROFESSORS_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
