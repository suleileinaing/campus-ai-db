#!/usr/bin/env python3
"""Fill professor emails from already-extracted public syllabus fields.

The syllabus "이메일" field is hidden behind login on public pages, so emails
are collected only where instructors wrote them into free-text fields
(office, homepages, consultation time).
"""

from __future__ import annotations

import csv
import re
from collections import defaultdict
from pathlib import Path
from urllib.parse import parse_qs, urlparse


PROJECT_DIR = Path(__file__).resolve().parent.parent
PROFESSORS_PATH = PROJECT_DIR / "processed_data" / "website_tables" / "professors.csv"
OFFERING_PROFESSORS_PATH = (
    PROJECT_DIR / "processed_data" / "website_tables" / "offering_professors.csv"
)
SYLLABI_PATH = PROJECT_DIR / "processed_data" / "database_tables" / "syllabi.csv"
TERM_ORDER = {"10": 1, "15": 2, "20": 3, "25": 4}

# An official khu.ac.kr address always wins; otherwise earlier fields describe
# the instructor more directly than later ones.
EMAIL_FIELDS = (
    "professor_office",
    "personal_homepage",
    "consultation_time",
    "course_homepage",
)
EMAIL_PATTERN = re.compile(
    r"(?<![A-Za-z0-9._%+])[A-Za-z0-9][A-Za-z0-9._%+-]*"
    r"@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}"
)
# An email introduced as a teaching assistant's is not the professor's.
ASSISTANT_CONTEXT = re.compile(r"조교|\bT\.?A\b|assistant", re.IGNORECASE)
OFFICIAL_DOMAIN = "@khu.ac.kr"


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.is_file():
        raise SystemExit(f"Required input not found: {path}")
    with path.open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        return list(reader.fieldnames or []), list(reader)


def url_value(url: str, key: str) -> str:
    return parse_qs(urlparse(url).query).get(key, [""])[0]


def term_key(url: str) -> tuple[int, int]:
    return int(url_value(url, "p_year") or 0), TERM_ORDER.get(
        url_value(url, "p_term"), 0
    )


def normalized_name(value: str) -> str:
    return re.sub(r"\s+", "", value).casefold()


def valid_email(value: str) -> bool:
    return bool(EMAIL_PATTERN.fullmatch(value.strip()))


def extract_emails(text: str) -> list[str]:
    emails = []
    for match in EMAIL_PATTERN.finditer(text):
        if ASSISTANT_CONTEXT.search(text[max(0, match.start() - 30):match.start()]):
            continue
        email = match.group().rstrip(".").lower()
        if email not in emails:
            emails.append(email)
    return emails


def syllabus_owner(
    syllabus: dict[str, str],
    text: str,
    offering_professors: dict[str, list[dict[str, str]]],
) -> dict[str, str] | None:
    """Return the professor an email in this syllabus field belongs to."""
    professors = offering_professors.get(syllabus["offering_id"], [])
    if len(professors) == 1:
        professor = professors[0]
        code = url_value(syllabus["source_url"], "p_teach")
        return professor if not code or professor["professor_code"] == code else None
    # Team-taught syllabi often carry a co-instructor's contact, so attribute
    # the email only when the text names exactly one of the instructors.
    compact_text = normalized_name(text)
    named = [
        professor
        for professor in professors
        if normalized_name(professor["name"]) in compact_text
    ]
    return named[0] if len(named) == 1 else None


def main() -> int:
    fields, professors = read_csv(PROFESSORS_PATH)
    _, offering_rows = read_csv(OFFERING_PROFESSORS_PATH)
    syllabus_fields, syllabi = read_csv(SYLLABI_PATH)
    if not {"professor_id", "professor_code", "name", "email"}.issubset(fields):
        raise SystemExit("professors.csv does not contain the required columns")
    if not {"offering_id", "source_url", *EMAIL_FIELDS}.issubset(syllabus_fields):
        raise SystemExit("syllabi.csv does not contain the required columns")

    professors_by_id = {row["professor_id"]: row for row in professors}
    offering_professors: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in offering_rows:
        professor = professors_by_id.get(row["professor_id"])
        if professor is not None:
            offering_professors[row["offering_id"]].append(professor)

    # professor_id -> email -> [best field rank, syllabus count, latest term]
    candidates: dict[str, dict[str, list]] = defaultdict(dict)
    unattributed = 0
    for syllabus in syllabi:
        term = term_key(syllabus["source_url"])
        seen_in_syllabus: set[tuple[str, str]] = set()
        for rank, field in enumerate(EMAIL_FIELDS):
            text = syllabus[field]
            emails = extract_emails(text)
            if not emails:
                continue
            owner = syllabus_owner(syllabus, text, offering_professors)
            if owner is None:
                unattributed += len(emails)
                continue
            for email in emails:
                stats = candidates[owner["professor_id"]].setdefault(
                    email, [rank, 0, term]
                )
                stats[0] = min(stats[0], rank)
                stats[2] = max(stats[2], term)
                if (owner["professor_id"], email) not in seen_in_syllabus:
                    seen_in_syllabus.add((owner["professor_id"], email))
                    stats[1] += 1

    # The same person may hold several professor codes, but an address claimed
    # by differently named professors cannot be attributed safely.
    names_by_email: dict[str, set[str]] = defaultdict(set)
    for professor_id, emails in candidates.items():
        for email in emails:
            names_by_email[email].add(
                normalized_name(professors_by_id[professor_id]["name"])
            )
    conflicting = {email for email, names in names_by_email.items() if len(names) > 1}

    filled = 0
    preserved = 0
    multiple = []
    missing = []
    for professor in professors:
        options = {
            email: stats
            for email, stats in candidates.get(professor["professor_id"], {}).items()
            if email not in conflicting
        }
        existing_email = professor["email"].strip()
        # An official address replaces an existing personal one.
        if valid_email(existing_email) and (
            existing_email.lower().endswith(OFFICIAL_DOMAIN)
            or not any(email.endswith(OFFICIAL_DOMAIN) for email in options)
        ):
            professor["email"] = existing_email
            preserved += 1
            continue

        if not options:
            professor["email"] = ""
            missing.append((professor["professor_code"], professor["name"]))
            continue
        ranked = sorted(
            options,
            key=lambda email: (
                not email.endswith(OFFICIAL_DOMAIN),
                options[email][0],
                -options[email][1],
                tuple(-part for part in options[email][2]),
                email,
            ),
        )
        professor["email"] = ranked[0]
        filled += 1
        if len(ranked) > 1:
            multiple.append((professor["professor_code"], professor["name"], ranked))

    temporary = PROFESSORS_PATH.with_suffix(".csv.tmp")
    with temporary.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(professors)
    temporary.replace(PROFESSORS_PATH)

    print(f"Professors: {len(professors)}")
    print(f"Existing valid emails preserved: {preserved}")
    print(f"Previously blank/invalid emails populated: {filled}")
    print(f"Unattributed team-taught syllabus emails: {unattributed}")
    print(f"Emails rejected as shared by different names: {len(conflicting)}")
    for email in sorted(conflicting):
        print(f"  {email}")
    print(f"Professors with several candidate emails (first chosen): {len(multiple)}")
    for code, name, ranked in multiple:
        print(f"  {code}: {name} -> {', '.join(ranked)}")
    non_official = [
        (professor["professor_code"], professor["name"], professor["email"])
        for professor in professors
        if professor["email"] and not professor["email"].lower().endswith(OFFICIAL_DOMAIN)
    ]
    print(f"Professors without an official {OFFICIAL_DOMAIN} email: {len(non_official)}")
    for code, name, email in non_official:
        print(f"  {code}: {name} -> {email}")
    print(f"Email unavailable: {len(missing)}")
    print("Office values were left unchanged.")
    print(f"Output: {PROFESSORS_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
