#!/usr/bin/env python3
"""Fill professor emails from the 소프트웨어융합학과 faculty page.

https://swcon.khu.ac.kr/swcon/user/professor/list.do?menuNo=21300009
Each card links to its professor code, so rows are matched by professor_code
and confirmed by name. The page publishes no offices; those are left unchanged.
An official khu.ac.kr address is preferred over any other address.
"""

from __future__ import annotations

import csv
import html
import re
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from enrich_professor_emails import OFFICIAL_DOMAIN, valid_email
from enrich_professor_offices import normalized_name


PROJECT_DIR = Path(__file__).resolve().parent.parent
PROFESSORS_PATH = PROJECT_DIR / "processed_data" / "website_tables" / "professors.csv"
FACULTY_URL = "https://swcon.khu.ac.kr/swcon/user/professor/list.do"
FACULTY_QUERY = {"menuNo": "21300009", "pageIndex": "1", "pageUnit": "100"}

COMMENT_PATTERN = re.compile(r"<!--.*?-->", re.DOTALL)
ITEM_PATTERN = re.compile(r'<li class="item">(.*?)</ul>', re.DOTALL)
NAME_PATTERN = re.compile(r'<div class="name">\s*<strong>(.*?)</strong>', re.DOTALL)
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


def fetch_faculty() -> list[dict[str, str]]:
    request = Request(
        f"{FACULTY_URL}?{urlencode(FACULTY_QUERY)}",
        headers={"User-Agent": "Mozilla/5.0"},
    )
    with urlopen(request, timeout=30) as response:
        page = response.read().decode("utf-8")
    page = COMMENT_PATTERN.sub("", page)

    faculty = []
    for item in ITEM_PATTERN.findall(page):
        name_match = NAME_PATTERN.search(item)
        code_match = CODE_PATTERN.search(item)
        if not name_match or not code_match:
            continue
        entry = {"name": text(name_match.group(1)), "code": code_match.group(1), "email": ""}
        for label, value in ROW_PATTERN.findall(item):
            if re.sub(r"\s", "", text(label)) == "이메일":
                entry["email"] = text(value).lower()
        faculty.append(entry)
    if not faculty:
        raise SystemExit(f"No professors parsed from {FACULTY_URL}")
    return faculty


def main() -> int:
    fields, professors = read_csv(PROFESSORS_PATH)
    if not {"professor_code", "name", "email"}.issubset(fields):
        raise SystemExit("professors.csv does not contain the required columns")
    rows_by_code = {}
    for professor in professors:
        rows_by_code.setdefault(professor["professor_code"], []).append(professor)

    faculty = fetch_faculty()
    changed = []
    kept_official = []
    unmatched = []
    for entry in faculty:
        rows = [
            professor
            for professor in rows_by_code.get(entry["code"], [])
            if normalized_name(professor["name"]) == normalized_name(entry["name"])
        ]
        if not rows:
            unmatched.append((entry["code"], entry["name"]))
            continue
        value = entry["email"]
        if not valid_email(value):
            continue
        for professor in rows:
            existing = professor["email"].strip()
            if existing == value:
                continue
            # The page is authoritative, except that a non-official address
            # never replaces an official one.
            if existing.lower().endswith(OFFICIAL_DOMAIN) and not value.endswith(
                OFFICIAL_DOMAIN
            ):
                kept_official.append((entry["code"], entry["name"], existing, value))
                continue
            professor["email"] = value
            changed.append((entry["code"], entry["name"], existing, value))

    temporary = PROFESSORS_PATH.with_suffix(".csv.tmp")
    with temporary.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(professors)
    temporary.replace(PROFESSORS_PATH)

    print(f"Faculty page professors: {len(faculty)}")
    print(f"Email values set from the page: {len(changed)}")
    for code, name, existing, value in changed:
        print(f"  {code}: {name} {existing!r} -> {value!r}")
    print(f"Official emails kept over non-official page values: {len(kept_official)}")
    for code, name, existing, value in kept_official:
        print(f"  {code}: {name} kept {existing!r}, page {value!r}")
    print(f"Not found in professors.csv: {len(unmatched)}")
    for code, name in unmatched:
        print(f"  {code}: {name}")
    print("Office values were left unchanged (not published on the page).")
    print(f"Output: {PROFESSORS_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
