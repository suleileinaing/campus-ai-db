#!/usr/bin/env python3
"""Fill and add professors from the 예술·디자인대학 faculty pages.

The college's professor list (and.khu.ac.kr) links every full-time
professor's code. Department pages are preferred where they list a person:

* professor lists (with codes): 산업디자인학과, 시각디자인학과, 디지털콘텐츠학과;
* boards (no codes, but 연구실): 환경조경디자인학과 (only "/ Faculty" cards,
  not adjunct, instructor or retired), 연극영화학과;
* 포스트모던음악학과's own site (khupmm.ac.kr): each full-time professor's
  profile page (교수/부교수/조교수, not 객원·겸임 or 강사) lists an email and
  sometimes the office right after it.

Board cards get their code from the college list by name. Rows are matched by
professor_code and name, or by name alone (if unique) for a person no page
links a code for. A department page's email and office replace the
existing values; an email listed only on the college list fills a blank email
and a differing one is reported. Listed professors missing from
professors.csv (except 명예교수) are appended with their code, or, when no page
links one, a stand-in professor_code continuing their department's numbering
(professor_codes.py). Department ids come from departments.csv where the
department exists there.
"""

from __future__ import annotations

import csv
import html
import re
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from enrich_professor_emails import OFFICIAL_DOMAIN, valid_email
from enrich_professor_offices import normalized_name, valid_office
from enrich_professors_from_faculty_lists import fetch_faculty
from professor_codes import next_department_code


PROJECT_DIR = Path(__file__).resolve().parent.parent
PROFESSORS_PATH = PROJECT_DIR / "processed_data" / "website_tables" / "professors.csv"
COLLEGE_LIST = ("https://and.khu.ac.kr/and_kor/user/professor/list.do", {"menuNo": "14900047"})
# (department, list URL, query, department_id or "")
DEPARTMENT_LISTS = [
    ("산업디자인학과", "https://id.khu.ac.kr/id_kor/user/professor/list.do", {"menuNo": "19700039"}, "5"),
    ("시각디자인학과", "https://vd.khu.ac.kr/vd/user/professor/list.do", {"menuNo": "15300009"}, ""),
    ("디지털콘텐츠학과", "https://com.khu.ac.kr/dc/user/professor/list.do", {"menuNo": "15400011"}, "6"),
]
DEPARTMENT_BOARDS = [
    ("환경조경디자인학과", "https://la.khu.ac.kr/la/user/bbs/BMSR00047/list.do", "19600007", ""),
    ("연극영화학과", "https://ft.khu.ac.kr/ft/user/bbs/BMSR00047/list.do", "15700013", ""),
]

PMM_SITE = "https://www.khupmm.ac.kr"
PMM_FACULTY_PATH = "/%EA%B5%90%EC%88%98%EC%A7%84-faculty"
PMM_DEPARTMENT = "포스트모던음악학과"
PMM_ITEM_PATTERN = re.compile(
    r'<a href="(/[^"]+/view/\d+)"[^>]*>.*?<p class="figure caption"[^>]*>(.*?)</p>', re.DOTALL
)
PMM_FULL_TIME_TITLES = {"교수", "부교수", "조교수"}
EMAIL_PATTERN = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
# "han@khu.ac.kr | , 예술디자인대학관 B128"
PMM_OFFICE_PATTERN = re.compile(r"[가-힣]+관\s*[A-Z]?\d+(?:-\d+)?호?")
NAME_PATTERN = re.compile(r'<div class="name">(.*?)</div>', re.DOTALL)
FIELD_PATTERN = r"{label}\s*(.*?)\s*(?=전공분야|분야|연구실|이메일|전화번호|연락처|학력|연구분야|연구소|홈페이지|$)"
EMAIL_FIELD = re.compile(FIELD_PATTERN.format(label="이메일"))
OFFICE_FIELD = re.compile(FIELD_PATTERN.format(label="연구실"))
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


def fetch_board(url: str, menu_no: str) -> list[dict[str, str]]:
    query = {"menuNo": menu_no, "pageIndex": "1", "pageUnit": "100"}
    request = Request(f"{url}?{urlencode(query)}", headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=60) as response:
        page = response.read().decode("utf-8")
    cards = []
    for item in page.split('<li class="item">')[1:]:
        name_match = NAME_PATTERN.search(item)
        if not name_match:
            continue
        card_text = text(item.split('<a href="javascript')[0])
        # "김신원 Shinwon Kim / Faculty", "김학민 | Kim Hak Min", "강성규, Sungkyu Kang"
        name = re.match(r"[가-힣]+", text(name_match.group(1)))
        if not name:
            continue
        role = re.search(r"/\s*(Faculty|Adjunct|Instructor|Retired)\b", card_text)
        email = field(EMAIL_FIELD, card_text).lower()
        cards.append(
            {
                "name": name.group(),
                "role": role.group(1) if role else "",
                "emeritus": "명예" in card_text.split("분야")[0],
                "email": email if valid_email(email) else "",
                "office": field(OFFICE_FIELD, card_text),
            }
        )
    if not cards:
        raise SystemExit(f"No professors parsed from {url}?menuNo={menu_no}")
    return cards


def fetch_url(url: str) -> str:
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=60) as response:
        return response.read().decode("utf-8")


def page_segments(page: str) -> list[str]:
    page = re.sub(r"<script.*?</script>|<style.*?</style>", "", page, flags=re.DOTALL)
    segments = (text(segment) for segment in TAG_PATTERN.split(page))
    return [segment for segment in segments if segment.strip(" ,‌")]


def fetch_pmm_faculty() -> list[dict[str, str]]:
    faculty = []
    for path, caption in PMM_ITEM_PATTERN.findall(fetch_url(PMM_SITE + PMM_FACULTY_PATH)):
        # "홍성규 교수<br />팝작곡" (HTML-escaped in the caption)
        heading = html.unescape(caption).split("<br")[0].strip()
        name, _, title = heading.partition(" ")
        if title.strip() not in PMM_FULL_TIME_TITLES:
            continue
        segments = page_segments(fetch_url(PMM_SITE + path))
        email = office = ""
        for index, segment in enumerate(segments):
            if match := EMAIL_PATTERN.search(segment):
                email = match.group().lower()
                following = segments[index + 1] if index + 1 < len(segments) else ""
                if office_match := PMM_OFFICE_PATTERN.search(following):
                    office = office_match.group()
                break
        faculty.append({"name": name, "email": email, "office": office})
    if not faculty:
        raise SystemExit(f"No full-time professors parsed from {PMM_SITE}{PMM_FACULTY_PATH}")
    return faculty


def main() -> int:
    fields, professors = read_csv(PROFESSORS_PATH)
    if not {"professor_id", "department_id", "professor_code", "name", "email", "office"}.issubset(
        fields
    ):
        raise SystemExit("professors.csv does not contain the required columns")

    people: dict[str, dict] = {}

    def person(name: str) -> dict:
        return people.setdefault(
            normalized_name(name),
            {
                "name": name,
                "code": "",
                "department": "",
                "department_id": "",
                "email": "",
                "department_email": False,
                "office": "",
                "emeritus": False,
            },
        )

    url, query = COLLEGE_LIST
    for card in fetch_faculty(url, query):
        entry = person(card["name"])
        entry["code"] = card["code"]
        if valid_email(card["email"]):
            entry["email"] = card["email"]
    for department, url, query, department_id in DEPARTMENT_LISTS:
        for card in fetch_faculty(url, query):
            entry = person(card["name"])
            entry["code"] = entry["code"] or card["code"]
            entry["department"] = entry["department"] or department
            entry["department_id"] = entry["department_id"] or department_id
            if valid_email(card["email"]):
                entry["email"] = card["email"]
                entry["department_email"] = True
    skipped_roles = []
    for department, url, menu_no, department_id in DEPARTMENT_BOARDS:
        for card in fetch_board(url, menu_no):
            if card["role"] and card["role"] != "Faculty":
                skipped_roles.append((department, card["name"], card["role"]))
                continue
            entry = person(card["name"])
            entry["department"] = entry["department"] or department
            entry["department_id"] = entry["department_id"] or department_id
            entry["emeritus"] |= card["emeritus"]
            if card["email"]:
                entry["email"] = card["email"]
                entry["department_email"] = True
            if valid_office(card["office"]):
                entry["office"] = card["office"]

    for card in fetch_pmm_faculty():
        entry = person(card["name"])
        entry["department"] = entry["department"] or PMM_DEPARTMENT
        if valid_email(card["email"]):
            entry["email"] = card["email"]
            entry["department_email"] = True
        if valid_office(card["office"]):
            entry["office"] = card["office"]

    rows_by_key = {
        (professor["professor_code"], normalized_name(professor["name"])): professor
        for professor in professors
    }
    rows_by_code: dict[str, list[dict[str, str]]] = {}
    rows_by_name: dict[str, list[dict[str, str]]] = {}
    for professor in professors:
        rows_by_code.setdefault(professor["professor_code"], []).append(professor)
        rows_by_name.setdefault(normalized_name(professor["name"]), []).append(professor)

    changes = []
    conflicts = []
    code_reused = []
    pending = []
    for entry in people.values():
        professor = rows_by_key.get((entry["code"], normalized_name(entry["name"])))
        namesakes = rows_by_name.get(normalized_name(entry["name"]), [])
        if not entry["code"] and len(namesakes) == 1:
            professor = namesakes[0]
        if professor is None:
            if entry["code"] in rows_by_code:
                code_reused.append(entry)
            pending.append(entry)
            continue
        label = f"{professor['professor_id']}/{professor['professor_code']}: {entry['name']}"
        existing = professor["email"].strip()
        if entry["email"] and existing.lower() != entry["email"]:
            if not existing or entry["department_email"]:
                professor["email"] = entry["email"]
                changes.append((label, "email", existing, entry["email"]))
            else:
                conflicts.append((label, "email", existing, entry["email"]))
        existing_office = professor["office"].strip()
        if entry["office"] and existing_office != entry["office"]:
            professor["office"] = entry["office"]
            changes.append((label, "office", existing_office, entry["office"]))

    next_professor_id = max(int(professor["professor_id"]) for professor in professors) + 1
    added = []
    emeriti = []
    # Linked codes go first so that no stand-in takes one of them.
    for entry in sorted(pending, key=lambda entry: not entry["code"]):
        if entry["emeritus"]:
            emeriti.append(entry)
            continue
        code = entry["code"]
        if not code:
            department_codes = [
                other["code"]
                for other in people.values()
                if other["code"] and other["department"] == entry["department"]
            ] or [other["code"] for other in people.values() if other["code"]]
            code = next_department_code(professors, department_codes)
        professor = {field_name: "" for field_name in fields}
        professor.update(
            professor_id=str(next_professor_id),
            department_id=entry["department_id"],
            professor_code=code,
            name=entry["name"],
            email=entry["email"],
            office=entry["office"],
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

    print(f"예술·디자인대학 professors: {len(people)}")
    print(f"Values set: {len(changes)}")
    for label, field_name, existing, value in changes:
        print(f"  {label} {field_name} {existing!r} -> {value!r}")
    print(f"Existing emails kept despite differing from the college list: {len(conflicts)}")
    for label, field_name, existing, value in conflicts:
        print(f"  {label} {field_name} kept {existing!r}, list {value!r}")
    print(f"Codes already used under another name: {len(code_reused)}")
    for entry in code_reused:
        others = ", ".join(row["name"] for row in rows_by_code[entry["code"]])
        print(f"  {entry['code']}: {entry['name']} (csv: {others})")
    print(f"Added to professors.csv: {len(added)}")
    for entry, professor in added:
        source = "linked code" if entry["code"] else "stand-in code"
        print(
            f"  {professor['professor_id']}/{professor['professor_code']} ({source}): "
            f"{entry['department'] or '-'} {entry['name']} {professor['email']!r} {professor['office']!r}"
        )
    print(f"명예교수 not added: {len(emeriti)}")
    for entry in emeriti:
        print(f"  {entry['department']} {entry['name']}")
    print(f"Adjunct/instructor/retired board cards skipped: {len(skipped_roles)}")
    print(f"Output: {PROFESSORS_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
