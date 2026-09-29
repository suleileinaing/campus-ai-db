#!/usr/bin/env python3
"""Build deduplicated prerequisite rules and their syllabus sources."""

from __future__ import annotations

import csv
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent.parent
EXTRACTED_PREREQUISITES = (
    PROJECT_DIR / "processed_data" / "syllabus_tables" / "syllabus_prerequisites.csv"
)
SYLLABI = PROJECT_DIR / "processed_data" / "database_tables" / "syllabi.csv"
COURSE_OFFERINGS = (
    PROJECT_DIR / "processed_data" / "website_tables" / "course_offerings.csv"
)
OUTPUT = (
    PROJECT_DIR / "processed_data" / "database_tables" / "course_prerequisites.csv"
)
SOURCES_OUTPUT = (
    PROJECT_DIR / "processed_data" / "database_tables" / "prerequisite_sources.csv"
)

FIELDS = [
    "prerequisite_id",
    "course_code",
    "prerequisite_course_code",
    "prerequisite_name",
    "prerequisite_type",
    "cohort_start",
    "cohort_end",
    "abeek_applicable",
    "prerequisite_group",
    "minimum_grade_code",
    "minimum_required_count",
]

SOURCE_FIELDS = ["prerequisite_id", "source_syllabus_id"]
RULE_FIELDS = [field for field in FIELDS if field != "prerequisite_id"]


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        raise SystemExit(f"Required input not found: {path}")
    with path.open(encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def unique_index(
    rows: list[dict[str, str]], key: str, source_name: str
) -> dict[str, dict[str, str]]:
    index: dict[str, dict[str, str]] = {}
    for row in rows:
        value = row[key]
        if value in index:
            raise SystemExit(f"Duplicate {key} in {source_name}: {value}")
        index[value] = row
    return index


def main() -> int:
    extracted = read_csv(EXTRACTED_PREREQUISITES)
    syllabi_by_id = unique_index(read_csv(SYLLABI), "syllabus_id", "syllabi.csv")
    offerings_by_id = unique_index(
        read_csv(COURSE_OFFERINGS), "offering_id", "course_offerings.csv"
    )

    output_rows = []
    source_rows = []
    rule_ids: dict[tuple[str, ...], int] = {}
    for row in extracted:
        syllabus = syllabi_by_id.get(row["syllabus_id"])
        if syllabus is None:
            raise SystemExit(
                f"Unknown syllabus_id in extracted prerequisites: {row['syllabus_id']}"
            )
        offering = offerings_by_id.get(syllabus["offering_id"])
        if offering is None:
            raise SystemExit(
                f"Unknown offering_id for syllabus {row['syllabus_id']}: "
                f"{syllabus['offering_id']}"
            )

        rule = {
            "course_code": offering["course_code"],
            "prerequisite_course_code": row["prerequisite_code"],
            "prerequisite_name": row["prerequisite_name"],
            "prerequisite_type": row["prerequisite_type"],
            "cohort_start": row["cohort_start"],
            "cohort_end": row["cohort_end"],
            "abeek_applicable": row["abeek_applicable"],
            "prerequisite_group": row["prerequisite_group"],
            "minimum_grade_code": row["minimum_grade"],
            "minimum_required_count": row["minimum_required_count"],
        }
        rule_key = tuple(rule[field] for field in RULE_FIELDS)
        prerequisite_id = rule_ids.get(rule_key)
        if prerequisite_id is None:
            prerequisite_id = len(output_rows) + 1
            rule_ids[rule_key] = prerequisite_id
            output_rows.append({"prerequisite_id": prerequisite_id, **rule})
        source_rows.append(
            {
                "prerequisite_id": prerequisite_id,
                "source_syllabus_id": row["syllabus_id"],
            }
        )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    temporary = OUTPUT.with_suffix(".csv.tmp")
    with temporary.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(output_rows)
    temporary.replace(OUTPUT)

    sources_temporary = SOURCES_OUTPUT.with_suffix(".csv.tmp")
    with sources_temporary.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=SOURCE_FIELDS)
        writer.writeheader()
        writer.writerows(source_rows)
    sources_temporary.replace(SOURCES_OUTPUT)

    print(f"Unique prerequisite rules: {len(output_rows)}")
    print(f"Prerequisite source links: {len(source_rows)}")
    print(f"Outputs: {OUTPUT}, {SOURCES_OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
