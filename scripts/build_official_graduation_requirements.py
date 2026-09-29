#!/usr/bin/env python3
"""Build official 2022-2026 CS/AI/SWCON graduation-requirement CSVs.

The numeric requirements and other conditions come from the curriculum PDFs in
raw_data/graduation_requirements.  Course-level rows are retained only where a
previous PDF normalization produced a verified category-1/category-2 row.
"""

from __future__ import annotations

import csv
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent.parent
DATABASE_DIR = PROJECT_DIR / "processed_data" / "database_tables"
SIMULATED_DIR = PROJECT_DIR / "processed_data" / "simulated"
REPORT_PATH = PROJECT_DIR / "validation_report" / "graduation_requirement_coverage.csv"

# requirement_id, department_id, department, year, total, basic, required,
# elective, industry credits
REQUIREMENTS = [
    (1, 12, "인공지능학과", 2022, 130, 18, 45, 27, 10),
    (2, 12, "인공지능학과", 2023, 130, 18, 42, 27, 12),
    (3, 12, "인공지능학과", 2024, 130, 18, 42, 27, 9),
    (4, 12, "인공지능학과", 2025, 130, 12, 42, 27, 9),
    (5, 12, "인공지능학과", 2026, 130, 12, 42, 27, 9),
    (6, 8, "소프트웨어융합학과", 2022, 130, 15, 37, 36, 10),
    (7, 8, "소프트웨어융합학과", 2023, 130, 15, 37, 36, 10),
    (8, 8, "소프트웨어융합학과", 2024, 130, 15, 37, 36, 10),
    (9, 8, "소프트웨어융합학과", 2025, 130, 15, 37, 36, 10),
    (10, 8, "소프트웨어융합학과", 2026, 130, 15, 37, 36, 10),
    (11, 11, "컴퓨터공학과", 2022, 140, 18, 48, 30, 12),
    (12, 11, "컴퓨터공학과", 2023, 140, 18, 45, 30, 12),
    (13, 11, "컴퓨터공학과", 2024, 130, 15, 45, 27, 12),
    (14, 11, "컴퓨터공학과", 2025, 130, 12, 42, 27, 12),
    (15, 11, "컴퓨터공학과", 2026, 130, 12, 39, 30, 12),
]


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def write_rows(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_verified_course_rows() -> tuple[list[dict], set[int]]:
    """Keep only previously normalized, directly required major courses.

    AI rows exist for all five cohorts.  The 2023 SWCON track files repeat the
    same common category-1/category-2 courses; one copy is attached to the new
    common 2023 requirement.  Track electives are deliberately excluded.
    """
    sources = read_rows(DATABASE_DIR / "requirement_courses.csv")
    sources += read_rows(SIMULATED_DIR / "requirement_courses.csv")
    selected: dict[tuple[int, str, int], dict] = {}

    for row in sources:
        old_requirement = int(row["requirement_id"])
        category = int(row["category_id"])
        if category not in {1, 2}:
            continue
        if old_requirement in {1, 2, 3, 4, 5}:
            new_requirement = old_requirement
        elif old_requirement == 6:
            new_requirement = 7  # 2023 SWCON common rows from one track copy
        else:
            continue
        key = (new_requirement, row["course_code"], category)
        selected[key] = {
            "requirement_id": new_requirement,
            "course_code": row["course_code"],
            "category_id": category,
        }

    rows = []
    for row_id, key in enumerate(sorted(selected), start=1):
        row = selected[key]
        rows.append({"requirement_course_id": row_id, **row})
    return rows, {int(row["requirement_id"]) for row in rows}


def main() -> int:
    graduation_rows = [
        {
            "requirement_id": requirement_id,
            "department_id": department_id,
            "track": "공통",
            "cohort_start": year,
            "cohort_end": year,
            "total_credits": total,
        }
        for requirement_id, department_id, _, year, total, *_ in REQUIREMENTS
    ]

    category_rows = []
    category_row_id = 1
    for requirement_id, _, _, _, _, basic, required, elective, _ in REQUIREMENTS:
        for category_id, minimum in ((1, basic), (2, required), (3, elective)):
            category_rows.append(
                {
                    "requirement_category_id": category_row_id,
                    "requirement_id": requirement_id,
                    "category_id": category_id,
                    "min_credits": minimum,
                    "min_areas": "",
                    "per_area_min_credits": "",
                }
            )
            category_row_id += 1

    other_rows = []
    other_id = 1
    for requirement_id, department_id, _, year, _, _, _, _, industry in REQUIREMENTS:
        if department_id == 12:
            thesis = "캡스톤디자인·졸업프로젝트 이수 후 졸업논문(인공지능) 수강"
        elif department_id == 11:
            thesis = "졸업프로젝트 이수 후 졸업논문(컴퓨터공학) 수강"
        else:
            thesis = "소프트웨어융합캡스톤디자인 이수 후 졸업논문(소프트웨어융합) 수강 및 제출"

        conditions = [
            ("산학필수", f"{industry}학점 이상"),
            ("전공영어강좌", "3과목 이상"),
            ("SW교육", "6학점 (편입생 및 순수외국인 제외)"),
            ("졸업논문", thesis),
        ]
        if department_id == 8:
            conditions.append(("트랙별 필수", "소속 트랙의 지정 필수과목 충족"))
        if year == 2022:
            conditions.append(("졸업능력인증", "교육과정 PDF의 외국어 졸업능력인증 기준 충족"))
        if year == 2026:
            conditions.append(("다전공등", "다전공·부전공·마이크로디그리 중 1개 이상 필수"))

        for condition_type, condition in conditions:
            other_rows.append(
                {
                    "requirement_other_id": other_id,
                    "requirement_id": requirement_id,
                    "type": condition_type,
                    "condition": condition,
                }
            )
            other_id += 1

    course_rows, requirements_with_courses = build_verified_course_rows()
    coverage_rows = []
    for requirement_id, department_id, department, year, *_ in REQUIREMENTS:
        coverage_rows.append(
            {
                "requirement_id": requirement_id,
                "department_id": department_id,
                "department": department,
                "cohort_year": year,
                "summary_status": "verified_from_official_pdf",
                "required_course_status": (
                    "normalized" if requirement_id in requirements_with_courses else "not_yet_normalized"
                ),
                "source_directory": "raw_data/graduation_requirements",
            }
        )

    write_rows(
        DATABASE_DIR / "graduation_requirements.csv",
        ["requirement_id", "department_id", "track", "cohort_start", "cohort_end", "total_credits"],
        graduation_rows,
    )
    write_rows(
        DATABASE_DIR / "requirement_categories.csv",
        ["requirement_category_id", "requirement_id", "category_id", "min_credits", "min_areas", "per_area_min_credits"],
        category_rows,
    )
    write_rows(
        DATABASE_DIR / "requirement_courses.csv",
        ["requirement_course_id", "requirement_id", "course_code", "category_id"],
        course_rows,
    )
    write_rows(
        DATABASE_DIR / "requirement_others.csv",
        ["requirement_other_id", "requirement_id", "type", "condition"],
        other_rows,
    )
    write_rows(
        REPORT_PATH,
        ["requirement_id", "department_id", "department", "cohort_year", "summary_status", "required_course_status", "source_directory"],
        coverage_rows,
    )

    print(f"Graduation requirement sets: {len(graduation_rows)}")
    print(f"Category thresholds: {len(category_rows)}")
    print(f"Verified required-course rows: {len(course_rows)}")
    print(f"Other conditions: {len(other_rows)}")
    print(f"Coverage report: {REPORT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
