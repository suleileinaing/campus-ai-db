#!/usr/bin/env python3
"""Build official 2020-2026 Humanitas general-education requirements.

The values were manually verified from:
raw_data/graduation_requirements/general_edu_grad_req.pdf

The 2019-2023 rule applies to the database cohorts 2020-2023.  The
"2024 cohort and later" rule is bounded at 2026 because that is the current
data-collection scope.  Extend cohort_end after verifying later revisions.
"""

from __future__ import annotations

import csv
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_DIR / "processed_data" / "database_tables"
SOURCE_DOCUMENT = "raw_data/graduation_requirements/general_edu_grad_req.pdf"


REQUIREMENTS = [
    {
        "general_requirement_id": 1,
        "cohort_start": 2020,
        "cohort_end": 2023,
        "total_general_credits": 32,
        "source_document": SOURCE_DOCUMENT,
        "source_note": "2019학번부터 2023학번까지 기준 중 DB 적용 범위",
    },
    {
        "general_requirement_id": 2,
        "cohort_start": 2024,
        "cohort_end": 2026,
        "total_general_credits": 29,
        "source_document": SOURCE_DOCUMENT,
        "source_note": "2024학번 이후 기준 중 현재 DB 적용 범위",
    },
]

CATEGORIES = [
    # 2020-2023: 필수 17 + 배분 12 (7개 중 4개) + 자유 3 = 32.
    (1, 1, "CORE_REQUIRED", "필수교과", 17, "", ""),
    (2, 1, "DISTRIBUTION", "배분이수교과", 12, 4, 3),
    (3, 1, "FREE_ELECTIVE", "자유이수교과", 3, "", ""),
    # 2024-2026: 필수 17 + 배분 9 (5개 중 3개) + 자유 3 = 29.
    (4, 2, "CORE_REQUIRED", "필수교과", 17, "", ""),
    (5, 2, "DISTRIBUTION", "배분이수교과", 9, 3, 3),
    (6, 2, "FREE_ELECTIVE", "자유이수교과", 3, "", ""),
]

# Official 필수교과 combines source-site category 4 (기초교과/code 16)
# and category 11 (필수교과/code 14).  Distribution and free-elective
# requirements map to category 5 and category 6 respectively.
CATEGORY_MEMBERS = [
    (1, 4),
    (1, 11),
    (2, 5),
    (3, 6),
    (4, 4),
    (4, 11),
    (5, 5),
    (6, 6),
]


def write_csv(filename: str, fieldnames: list[str], rows: list[dict]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with (OUTPUT_DIR / filename).open(
        "w", encoding="utf-8-sig", newline=""
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    source_path = PROJECT_DIR / SOURCE_DOCUMENT
    if not source_path.is_file():
        raise FileNotFoundError(f"Official source PDF not found: {source_path}")

    category_rows = [
        {
            "general_requirement_category_id": row_id,
            "general_requirement_id": requirement_id,
            "requirement_code": code,
            "requirement_name": name,
            "min_credits": credits,
            "min_areas": min_areas,
            "per_area_min_credits": per_area,
        }
        for row_id, requirement_id, code, name, credits, min_areas, per_area
        in CATEGORIES
    ]
    member_rows = [
        {
            "general_requirement_category_id": requirement_category_id,
            "category_id": category_id,
        }
        for requirement_category_id, category_id in CATEGORY_MEMBERS
    ]

    write_csv(
        "general_education_requirements.csv",
        [
            "general_requirement_id",
            "cohort_start",
            "cohort_end",
            "total_general_credits",
            "source_document",
            "source_note",
        ],
        REQUIREMENTS,
    )
    write_csv(
        "general_education_requirement_categories.csv",
        [
            "general_requirement_category_id",
            "general_requirement_id",
            "requirement_code",
            "requirement_name",
            "min_credits",
            "min_areas",
            "per_area_min_credits",
        ],
        category_rows,
    )
    write_csv(
        "general_education_category_members.csv",
        ["general_requirement_category_id", "category_id"],
        member_rows,
    )
    print(f"General-education requirement sets: {len(REQUIREMENTS)}")
    print(f"General-education category thresholds: {len(category_rows)}")
    print(f"Source-category mappings: {len(member_rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
