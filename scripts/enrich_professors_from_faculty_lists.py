#!/usr/bin/env python3
"""Fill professor emails from KHU faculty list pages.

These college and department sites share one professor-list template whose
cards link to the professor code (pfView('...')), so rows are matched by
professor_code and confirmed by name. The pages (and their detail views)
publish no offices, so offices are left unchanged. A department site's email
replaces any existing value; a college site's email fills a blank email and a
differing one is reported. Department sites are read before college sites.
Listed professors missing from professors.csv (except 명예교수) are appended
with the source's department_id (blank when departments.csv has no matching
department).
"""

from __future__ import annotations

import csv
import html
import re
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from enrich_professor_emails import valid_email
from enrich_professor_offices import normalized_name


PROJECT_DIR = Path(__file__).resolve().parent.parent
PROFESSORS_PATH = PROJECT_DIR / "processed_data" / "website_tables" / "professors.csv"
# (label, list URL, query, department_id for appended professors, is a
# department site) — the pageIndex is added while paging. Departments missing
# from departments.csv get a blank department_id.
FACULTY_LISTS = [
    (
        "후마니타스칼리지 (국제캠퍼스)",
        "https://hc.khu.ac.kr/hc_kor/user/professor/list.do",
        {"menuNo": "4300024", "searchYn": "Y", "searchTab": "TAB_CAMPUS"},
        "",
        False,
    ),
    (
        "전자공학부",
        "https://ee.khu.ac.kr/ee25/user/professor/list.do",
        {"menuNo": "21700048"},
        "13",
        True,
    ),
    (
        "생체의공학과",
        "https://bme.khu.ac.kr/bme25/user/professor/list.do",
        {"menuNo": "21800009"},
        "",
        True,
    ),
    ("기계공학부", "https://me.khu.ac.kr/me_kor/user/professor/list.do", {"menuNo": "17300004"}, "2", True),
    ("산업경영공학과", "https://ie.khu.ac.kr/ie/user/professor/list.do", {"menuNo": "17400014"}, "3", True),
    ("원자력공학과", "https://ne.khu.ac.kr/ne/user/professor/list.do", {"menuNo": "17500020"}, "", True),
    (
        "화학공학과",
        "https://chemeng.khu.ac.kr/chemeng/user/professor/list.do",
        {"menuNo": "17600016"},
        "",
        True,
    ),
    ("신소재공학과", "https://mse.khu.ac.kr/amie/user/professor/list.do", {"menuNo": "17700014"}, "", True),
    (
        "사회기반시스템공학과",
        "https://civileng.khu.ac.kr/civileng/user/professor/list.do",
        {"menuNo": "17800014"},
        "",
        True,
    ),
    (
        "건축공학과",
        "https://archieng.khu.ac.kr/archieng/user/professor/list.do",
        {"menuNo": "17900014"},
        "",
        True,
    ),
    (
        "환경학및환경공학과",
        "https://env.khu.ac.kr/env/user/professor/list.do",
        {"menuNo": "18000014"},
        "",
        True,
    ),
    ("건축학과", "https://archi.khu.ac.kr/archi/user/professor/list.do", {"menuNo": "18100017"}, "", True),
    # The college list repeats its departments' professors.
    ("공과대학", "https://eng.khu.ac.kr/eng_kor/user/professor/list.do", {"menuNo": "17100026"}, "", False),
]
MAX_PAGES = 50

COMMENT_PATTERN = re.compile(r"<!--.*?-->", re.DOTALL)
NAME_PATTERN = re.compile(
    r'<div class="name">\s*<strong>(.*?)</strong>\s*(?:<span>(.*?)</span>)?', re.DOTALL
)
CODE_PATTERN = re.compile(r"pfView\('(\d+)'\)")
ROW_PATTERN = re.compile(r"<li><span>(.*?)</span>\s*<span[^>]*>(.*?)</span>", re.DOTALL)
TAG_PATTERN = re.compile(r"<[^>]+>")


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.is_file():
        raise SystemExit(f"Required input not found: {path}")
    with path.open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        return list(reader.fieldnames or []), list(reader)


def text(fragment: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(TAG_PATTERN.sub(" ", fragment))).strip()


def parse_cards(page: str) -> list[dict[str, str]]:
    cards = []
    for item in COMMENT_PATTERN.sub("", page).split('<li class="item">')[1:]:
        name_match = NAME_PATTERN.search(item)
        code_match = CODE_PATTERN.search(item)
        if not name_match or not code_match:
            continue
        entry = {
            "name": text(name_match.group(1)),
            "title": text(name_match.group(2) or ""),
            "code": code_match.group(1),
            "email": "",
        }
        for label, value in ROW_PATTERN.findall(item):
            if re.sub(r"\s", "", text(label)) == "이메일":
                entry["email"] = text(value).lower()
        cards.append(entry)
    return cards


def fetch_faculty(url: str, query: dict[str, str]) -> list[dict[str, str]]:
    faculty: dict[str, dict[str, str]] = {}
    for page_index in range(1, MAX_PAGES + 1):
        request = Request(
            f"{url}?{urlencode({**query, 'pageIndex': page_index})}",
            headers={"User-Agent": "Mozilla/5.0"},
        )
        with urlopen(request, timeout=30) as response:
            cards = parse_cards(response.read().decode("utf-8"))
        new_cards = [card for card in cards if card["code"] not in faculty]
        # Past the last page the site repeats it or returns no cards.
        if not new_cards:
            break
        for card in new_cards:
            faculty[card["code"]] = card
    if not faculty:
        raise SystemExit(f"No professors parsed from {url}")
    return list(faculty.values())


def main() -> int:
    fields, professors = read_csv(PROFESSORS_PATH)
    if not {"professor_id", "department_id", "professor_code", "name", "email", "office"}.issubset(
        fields
    ):
        raise SystemExit("professors.csv does not contain the required columns")
    rows_by_code: dict[str, list[dict[str, str]]] = {}
    for professor in professors:
        rows_by_code.setdefault(professor["professor_code"], []).append(professor)

    next_professor_id = max(int(professor["professor_id"]) for professor in professors) + 1

    for label, url, query, department_id, is_department_site in sorted(
        FACULTY_LISTS, key=lambda source: not source[4]
    ):
        faculty = fetch_faculty(url, query)
        filled = []
        conflicts = []
        added = []
        emeriti = []
        for entry in faculty:
            rows = [
                professor
                for professor in rows_by_code.get(entry["code"], [])
                if normalized_name(professor["name"]) == normalized_name(entry["name"])
            ]
            if not rows:
                if "명예" in entry["title"]:
                    emeriti.append(entry)
                    continue
                professor = {field: "" for field in fields}
                professor.update(
                    professor_id=str(next_professor_id),
                    department_id=department_id,
                    professor_code=entry["code"],
                    name=entry["name"],
                    email=entry["email"] if valid_email(entry["email"]) else "",
                )
                next_professor_id += 1
                professors.append(professor)
                rows_by_code.setdefault(entry["code"], []).append(professor)
                added.append(professor)
                continue
            if not valid_email(entry["email"]):
                continue
            for professor in rows:
                existing = professor["email"].strip()
                if existing.lower() == entry["email"]:
                    continue
                if not existing or is_department_site:
                    professor["email"] = entry["email"]
                    filled.append((entry["code"], entry["name"], existing, entry["email"]))
                else:
                    conflicts.append((entry["code"], entry["name"], existing, entry["email"]))

        print(f"[{label}] {url}")
        print(f"  Faculty page professors: {len(faculty)}")
        print(f"  Emails set: {len(filled)}")
        for code, name, existing, value in filled:
            print(f"    {code}: {name} {existing!r} -> {value!r}")
        print(f"  Existing emails kept despite differing from the page: {len(conflicts)}")
        for code, name, existing, value in conflicts:
            print(f"    {code}: {name} kept {existing!r}, page {value!r}")
        print(f"  Added to professors.csv: {len(added)}")
        for professor in added:
            print(
                f"    {professor['professor_id']}/{professor['professor_code']}: "
                f"{professor['name']} department_id={professor['department_id'] or '-'} "
                f"email={professor['email']!r}"
            )
        if emeriti:
            print(f"  명예교수 not added: {', '.join(entry['name'] for entry in emeriti)}")

    temporary = PROFESSORS_PATH.with_suffix(".csv.tmp")
    with temporary.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(professors)
    temporary.replace(PROFESSORS_PATH)

    print("Office values were left unchanged (not published on these pages).")
    print(f"Output: {PROFESSORS_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
