#!/usr/bin/env python3
"""Build official 2020-2026 CS/AI/SWCON graduation-requirement CSVs.

The numeric requirements and track conditions come from the curriculum PDFs
in raw_data/graduation_requirements. Existing ``공통`` requirement IDs remain
stable for compatibility. Track-specific rows are additional official views;
simulated students are not rewritten by this script.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent.parent
DATABASE_DIR = PROJECT_DIR / "processed_data" / "database_tables"
SIMULATED_DIR = PROJECT_DIR / "processed_data" / "simulated"
REPORT_PATH = PROJECT_DIR / "validation_report" / "graduation_requirement_coverage.csv"


@dataclass(frozen=True)
class Requirement:
    requirement_id: int
    department_id: int
    department: str
    year: int
    total: int
    basic: int
    required: int
    elective: int
    industry: int
    source_document: str
    track: str = "공통"
    track_condition: str | None = None
    common_requirement_id: int | None = None


# Existing 2022-2026 common IDs (1-15) remain unchanged. New common rows use
# IDs 16-19 so saved Gold SQL referring to the old IDs stays valid.
COMMON_REQUIREMENTS = [
    Requirement(1, 12, "인공지능학과", 2022, 130, 18, 45, 27, 10, "2022_software_convergence_college_curriculum.pdf"),
    Requirement(2, 12, "인공지능학과", 2023, 130, 18, 42, 27, 12, "2023_artificial_intelligence_curriculum.pdf"),
    Requirement(3, 12, "인공지능학과", 2024, 130, 18, 42, 27, 9, "2024_software_convergence_college_curriculum.pdf"),
    Requirement(4, 12, "인공지능학과", 2025, 130, 12, 42, 27, 9, "2025_software_convergence_college_curriculum.pdf"),
    Requirement(5, 12, "인공지능학과", 2026, 130, 12, 42, 27, 9, "2026_software_convergence_college_curriculum.pdf"),
    Requirement(6, 8, "소프트웨어융합학과", 2022, 130, 15, 37, 36, 10, "2022_software_convergence_college_curriculum.pdf"),
    Requirement(7, 8, "소프트웨어융합학과", 2023, 130, 15, 37, 36, 10, "2023_software_convergence_curriculum.pdf"),
    Requirement(8, 8, "소프트웨어융합학과", 2024, 130, 15, 37, 36, 10, "2024_software_convergence_college_curriculum.pdf"),
    Requirement(9, 8, "소프트웨어융합학과", 2025, 130, 15, 37, 36, 10, "2025_software_convergence_college_curriculum.pdf"),
    Requirement(10, 8, "소프트웨어융합학과", 2026, 130, 15, 37, 36, 10, "2026_software_convergence_college_curriculum.pdf"),
    Requirement(11, 11, "컴퓨터공학과", 2022, 140, 18, 48, 30, 12, "2022_software_convergence_college_curriculum.pdf"),
    Requirement(12, 11, "컴퓨터공학과", 2023, 140, 18, 45, 30, 12, "2023_computer_science_curriculum.pdf"),
    Requirement(13, 11, "컴퓨터공학과", 2024, 130, 15, 45, 27, 12, "2024_computer_science_curriculum.pdf"),
    Requirement(14, 11, "컴퓨터공학과", 2025, 130, 12, 42, 27, 12, "2025_software_convergence_college_curriculum.pdf"),
    Requirement(15, 11, "컴퓨터공학과", 2026, 130, 12, 39, 30, 12, "2026_software_convergence_college_curriculum.pdf"),
    Requirement(16, 8, "소프트웨어융합학과", 2020, 130, 15, 37, 36, 10, "2020_software_convergence_curriculum.pdf"),
    Requirement(17, 8, "소프트웨어융합학과", 2021, 130, 15, 37, 36, 10, "2021_software_convergence_curriculum.pdf"),
    Requirement(18, 11, "컴퓨터공학과", 2020, 140, 18, 45, 33, 12, "2020_computer_science_curriculum.pdf"),
    Requirement(19, 11, "컴퓨터공학과", 2021, 140, 18, 48, 30, 12, "2021_computer_science_curriculum.pdf"),
]

COMMON_BY_DEPARTMENT_YEAR = {
    (row.department_id, row.year): row for row in COMMON_REQUIREMENTS
}


def track_requirement(
    requirement_id: int,
    department_id: int,
    year: int,
    track: str,
    condition: str,
) -> Requirement:
    common = COMMON_BY_DEPARTMENT_YEAR[(department_id, year)]
    return Requirement(
        requirement_id, common.department_id, common.department, common.year,
        common.total, common.basic, common.required, common.elective,
        common.industry, common.source_document, track, condition,
        common.requirement_id,
    )


TRACK_REQUIREMENTS = [
    # AI curricula explicitly define research/industry tracks through 2024.
    track_requirement(20, 12, 2022, "연구트랙", "연구트랙선택 9학점 이수"),
    track_requirement(21, 12, 2022, "산학트랙", "산학트랙선택 9학점 이수"),
    track_requirement(22, 12, 2023, "연구트랙", "연구트랙선택 9학점 이수"),
    track_requirement(23, 12, 2023, "산학트랙", "산학트랙선택 9학점 이수"),
    track_requirement(24, 12, 2024, "연구트랙", "연구트랙선택 9학점 이수"),
    track_requirement(25, 12, 2024, "산학트랙", "산학트랙선택 9학점 이수"),
]


def add_swcon_tracks(start_id: int, year: int) -> list[Requirement]:
    if year == 2020:
        tracks = [
            ("게임콘텐츠트랙", "트랙필수·트랙선택 최소 27학점(9과목), 트랙필수 전 과목 이수"),
            ("데이터사이언스트랙", "트랙필수·트랙선택 최소 27학점(9과목), 트랙필수 전 과목 이수"),
            ("미래자동차·로봇트랙", "트랙필수·트랙선택 최소 27학점(9과목), 트랙필수 전 과목 이수"),
            ("융합리더트랙", "전공선택 최소 36학점(12과목) 이수"),
        ]
    else:
        robot_track = "미래자동차·로봇트랙" if year <= 2022 else "로봇·비전트랙"
        tracks = [
            ("게임콘텐츠트랙", "해당 트랙필수 교과목 전 과목 이수"),
            ("데이터사이언스트랙", "해당 트랙필수 교과목 전 과목 이수"),
            (robot_track, "해당 트랙필수 교과목 전 과목 이수"),
            ("융합리더트랙", "전공선택 최소 36학점(12과목) 이수"),
        ]
    return [
        track_requirement(start_id + offset, 8, year, track, condition)
        for offset, (track, condition) in enumerate(tracks)
    ]


for first_id, cohort_year in (
    (26, 2020), (30, 2021), (34, 2022), (38, 2023),
    (42, 2024), (46, 2025), (50, 2026),
):
    TRACK_REQUIREMENTS.extend(add_swcon_tracks(first_id, cohort_year))

REQUIREMENTS = COMMON_REQUIREMENTS + TRACK_REQUIREMENTS


# Rows explicitly marked as track-required in the official curriculum
# diagrams. Historical source names are retained because some course codes
# have since been renamed or reused in the current catalog.
TRACK_COURSES = [
    # 2020 SWCON curriculum, appendix pages 341, 343 and 345.
    (26, "SWCON211", "TRACK_REQUIRED", "게임프로그래밍입문", "2020_software_convergence_curriculum.pdf", 14),
    (26, "SWCON311", "TRACK_REQUIRED", "게임그래픽프로그래밍", "2020_software_convergence_curriculum.pdf", 14),
    (26, "DC318", "TRACK_REQUIRED", "게임디자인", "2020_software_convergence_curriculum.pdf", 14),
    (27, "SWCON321", "TRACK_REQUIRED", "데이터분석캡스톤디자인", "2020_software_convergence_curriculum.pdf", 16),
    (28, "SWCON332", "TRACK_REQUIRED", "미래자동차·로봇캡스톤디자인", "2020_software_convergence_curriculum.pdf", 18),
    # 2021 SWCON curriculum, appendix pages 310-312.
    (30, "SWCON211", "TRACK_REQUIRED", "게임프로그래밍입문", "2021_software_convergence_curriculum.pdf", 14),
    (30, "SWCON311", "TRACK_REQUIRED", "게임그래픽프로그래밍", "2021_software_convergence_curriculum.pdf", 14),
    (31, "SWCON321", "TRACK_REQUIRED", "인터넷분석과소셜네트워크디자인", "2021_software_convergence_curriculum.pdf", 15),
    (32, "SWCON332", "TRACK_REQUIRED", "미래자동차·로봇프로젝트디자인", "2021_software_convergence_curriculum.pdf", 16),
]


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def write_rows(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def build_verified_course_rows() -> tuple[list[dict], set[int]]:
    """Retain verified common required-course rows without track copying."""
    sources = read_rows(DATABASE_DIR / "requirement_courses.csv")
    sources += read_rows(SIMULATED_DIR / "requirement_courses.csv")
    common_selected: dict[tuple[int, str, int], dict] = {}

    for row in sources:
        old_requirement = int(row["requirement_id"])
        category = int(row["category_id"])
        if category not in {1, 2}:
            continue
        if old_requirement in {1, 2, 3, 4, 5, 7}:
            common_requirement = old_requirement
        elif old_requirement == 6:
            common_requirement = 7  # legacy 2023 SWCON track copy
        else:
            continue
        key = (common_requirement, row["course_code"], category)
        common_selected[key] = {
            "requirement_id": common_requirement,
            "course_code": row["course_code"],
            "category_id": category,
        }

    rows = []
    for row_id, key in enumerate(sorted(common_selected), start=1):
        rows.append({"requirement_course_id": row_id, **common_selected[key]})
    return rows, {int(row["requirement_id"]) for row in rows}


def build_track_course_rows() -> tuple[list[dict], set[int]]:
    rows = []
    for row_id, row in enumerate(TRACK_COURSES, start=1):
        requirement_id, course_code, course_type, source_name, source_document, source_page = row
        rows.append({
            "requirement_track_course_id": row_id,
            "requirement_id": requirement_id,
            "course_code": course_code,
            "course_type": course_type,
            "source_course_name": source_name,
            "source_document": source_document,
            "source_page": source_page,
        })
    return rows, {int(row["requirement_id"]) for row in rows}


def main() -> int:
    graduation_rows = [
        {
            "requirement_id": row.requirement_id,
            "department_id": row.department_id,
            "track": row.track,
            "cohort_start": row.year,
            "cohort_end": row.year,
            "total_credits": row.total,
        }
        for row in REQUIREMENTS
    ]

    category_rows = []
    category_row_id = 1
    for row in REQUIREMENTS:
        for category_id, minimum in ((1, row.basic), (2, row.required), (3, row.elective)):
            category_rows.append({
                "requirement_category_id": category_row_id,
                "requirement_id": row.requirement_id,
                "category_id": category_id,
                "min_credits": minimum,
                "min_areas": "",
                "per_area_min_credits": "",
            })
            category_row_id += 1

    other_rows = []
    other_id = 1
    for row in REQUIREMENTS:
        # Do not apply generic English-course, SW-education, thesis,
        # certification or multi-major rules to every cohort. Those conditions
        # require separate source-by-source normalization. Industry-credit and
        # track conditions are directly represented in the current sources.
        conditions = [("산학필수", f"{row.industry}학점 이상")]
        if row.track_condition:
            conditions.append(("트랙이수", row.track_condition))
        elif row.department_id == 8:
            conditions.append(("트랙이수", "소속 트랙의 공식 이수조건 충족"))
        elif row.department_id == 12 and row.year <= 2024:
            conditions.append(("트랙이수", "연구트랙 또는 산학트랙 중 하나를 선택하고 해당 트랙선택 9학점 이수"))
        for condition_type, condition in conditions:
            other_rows.append({
                "requirement_other_id": other_id,
                "requirement_id": row.requirement_id,
                "type": condition_type,
                "condition": condition,
            })
            other_id += 1

    course_rows, requirements_with_courses = build_verified_course_rows()
    track_course_rows, requirements_with_track_courses = build_track_course_rows()
    coverage_rows = [
        {
            "requirement_id": row.requirement_id,
            "department_id": row.department_id,
            "department": row.department,
            "track": row.track,
            "cohort_year": row.year,
            "summary_status": "verified_from_official_pdf",
            "required_course_status": (
                "normalized" if row.requirement_id in requirements_with_courses else "not_yet_normalized"
            ),
            "track_course_status": (
                "normalized_from_official_diagram"
                if row.requirement_id in requirements_with_track_courses
                else (
                    "not_applicable"
                    if row.track == "공통" or row.track == "융합리더트랙"
                    else "not_yet_normalized"
                )
            ),
            "other_condition_status": "industry_and_track_only",
            "source_document": row.source_document,
        }
        for row in REQUIREMENTS
    ]

    write_rows(DATABASE_DIR / "graduation_requirements.csv",
               ["requirement_id", "department_id", "track", "cohort_start", "cohort_end", "total_credits"],
               graduation_rows)
    write_rows(DATABASE_DIR / "requirement_categories.csv",
               ["requirement_category_id", "requirement_id", "category_id", "min_credits", "min_areas", "per_area_min_credits"],
               category_rows)
    write_rows(DATABASE_DIR / "requirement_courses.csv",
               ["requirement_course_id", "requirement_id", "course_code", "category_id"],
               course_rows)
    write_rows(DATABASE_DIR / "requirement_track_courses.csv",
               ["requirement_track_course_id", "requirement_id", "course_code", "course_type", "source_course_name", "source_document", "source_page"],
               track_course_rows)
    write_rows(DATABASE_DIR / "requirement_others.csv",
               ["requirement_other_id", "requirement_id", "type", "condition"],
               other_rows)
    write_rows(REPORT_PATH,
               ["requirement_id", "department_id", "department", "track", "cohort_year", "summary_status", "required_course_status", "track_course_status", "other_condition_status", "source_document"],
               coverage_rows)

    print(f"Graduation requirement sets: {len(graduation_rows)}")
    print(f"Common sets: {len(COMMON_REQUIREMENTS)}")
    print(f"Track-specific sets: {len(TRACK_REQUIREMENTS)}")
    print(f"Category thresholds: {len(category_rows)}")
    print(f"Verified required-course rows: {len(course_rows)}")
    print(f"Verified track-course rows: {len(track_course_rows)}")
    print(f"Other conditions: {len(other_rows)}")
    print(f"Coverage report: {REPORT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
