#!/usr/bin/env python3
"""Reconstruct resumable syllabus-extraction files from canonical CSV tables.

The canonical database tables are committed, while the intermediate extraction
checkpoint is not.  This script seeds that checkpoint so
``extract_syllabus_data.py --resume`` skips syllabus pages already extracted.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from extract_syllabus_data import (
    DETAIL_FIELDS,
    EVALUATION_FIELDS,
    PREREQUISITE_FIELDS,
    REPORT_FIELDS,
    TEXTBOOK_FIELDS,
    WEEKLY_PLAN_FIELDS,
    write_csv_atomic,
)


PROJECT_DIR = Path(__file__).resolve().parent.parent
DATABASE_TABLES = PROJECT_DIR / "processed_data" / "database_tables"
WEBSITE_TABLES = PROJECT_DIR / "processed_data" / "website_tables"
DEFAULT_OUTPUT_DIR = PROJECT_DIR / "processed_data" / "syllabus_tables"

EVALUATION_COLUMNS = {
    "중간고사": ("midterm_percentage", "midterm_detail"),
    "기말고사": ("final_exam_percentage", "final_exam_detail"),
    "과제보고서": ("assignment_percentage", "assignment_detail"),
    "발표": ("presentation_percentage", "presentation_detail"),
    "출석": ("attendance_percentage", "attendance_detail"),
    "기타": ("other_percentage", "other_detail"),
}

RAW_ENGLISH_TYPES = {
    "NONE": "",
    "PARTIAL": "영어(부분)강좌",
    "FULL": "전체영어강좌",
}

OUTPUT_NAMES = (
    "syllabus_details.csv",
    "syllabus_prerequisites.csv",
    "syllabus_evaluations.csv",
    "syllabus_textbooks.csv",
    "syllabus_weekly_plans.csv",
    "extraction_report.csv",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Seed syllabus extraction checkpoints from canonical CSVs."
    )
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument(
        "--force",
        action="store_true",
        help="replace an existing extraction checkpoint",
    )
    return parser.parse_args()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        raise SystemExit(f"Required input not found: {path}")
    with path.open(encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def unique_index(
    rows: list[dict[str, str]], key: str, source: str
) -> dict[str, dict[str, str]]:
    index: dict[str, dict[str, str]] = {}
    for row in rows:
        value = row[key]
        if value in index:
            raise SystemExit(f"Duplicate {key} in {source}: {value}")
        index[value] = row
    return index


def url_metadata(url: str) -> tuple[str, str]:
    query = parse_qs(urlparse(url).query)
    return query.get("p_year", [""])[0], query.get("p_term", [""])[0]


def decode_json_list(value: str) -> str:
    if not value.strip():
        return ""
    parsed = json.loads(value)
    if not isinstance(parsed, list):
        raise SystemExit(f"Expected JSON array, got: {value!r}")
    return " | ".join(str(item).strip() for item in parsed if str(item).strip())


def combine_homepages(personal: str, course: str) -> str:
    personal = personal.strip()
    course = course.strip()
    if course:
        return f"[개인용] {personal} [수업용] {course}"
    return personal


def ensure_output_is_safe(output_dir: Path, force: bool) -> None:
    existing = [output_dir / name for name in OUTPUT_NAMES if (output_dir / name).exists()]
    if existing and not force:
        paths = "\n  ".join(str(path) for path in existing)
        raise SystemExit(
            "Extraction checkpoint already exists. Use --force only to replace it:\n"
            f"  {paths}"
        )


def main() -> int:
    args = parse_args()
    ensure_output_is_safe(args.output_dir, args.force)

    syllabi = read_csv(DATABASE_TABLES / "syllabi.csv")
    textbooks = read_csv(DATABASE_TABLES / "syllabus_textbooks.csv")
    weekly_plans = read_csv(DATABASE_TABLES / "syllabus_weekly_plans.csv")
    prerequisite_rules = read_csv(DATABASE_TABLES / "course_prerequisites.csv")
    prerequisite_sources = read_csv(DATABASE_TABLES / "prerequisite_sources.csv")
    offerings = unique_index(
        read_csv(WEBSITE_TABLES / "course_offerings.csv"),
        "offering_id",
        "course_offerings.csv",
    )
    courses = unique_index(
        read_csv(WEBSITE_TABLES / "courses.csv"), "course_code", "courses.csv"
    )
    rules = unique_index(
        prerequisite_rules, "prerequisite_id", "course_prerequisites.csv"
    )

    details: list[dict[str, str]] = []
    evaluations: list[dict[str, str]] = []
    raw_textbooks: list[dict[str, str]] = []
    raw_weekly_plans: list[dict[str, str]] = []
    raw_prerequisites: list[dict[str, str]] = []

    for syllabus in sorted(syllabi, key=lambda row: int(row["syllabus_id"])):
        offering = offerings.get(syllabus["offering_id"])
        if offering is None:
            raise SystemExit(
                f"Unknown offering_id for syllabus {syllabus['syllabus_id']}: "
                f"{syllabus['offering_id']}"
            )
        course = courses.get(offering["course_code"], {})
        year, term_code = url_metadata(syllabus["source_url"])
        english_type = offering.get("english_type", "").strip()
        if english_type not in RAW_ENGLISH_TYPES:
            raise SystemExit(
                f"Unsupported English type for offering {offering['offering_id']}: "
                f"{english_type!r}"
            )

        detail = {field: "" for field in DETAIL_FIELDS}
        detail.update(
            {
                "syllabus_id": syllabus["syllabus_id"],
                "offering_id": syllabus["offering_id"],
                "year": year,
                "term_code": term_code,
                "course_name": offering.get("course_name", "")
                or course.get("current_name", ""),
                "lecture_code": offering["course_code"],
                "credits_raw": offering.get("credits", ""),
                "professor_office": syllabus["professor_office"],
                "homepage": combine_homepages(
                    syllabus["personal_homepage"], syllabus["course_homepage"]
                ),
                "english_course": RAW_ENGLISH_TYPES[english_type],
                "consultation_time": syllabus["consultation_time"],
                "overview": syllabus["overview"],
                "objectives": syllabus["objectives"],
                "operation_modes": syllabus["operation_modes"],
                "operation_note": syllabus["operation_note"],
                "class_types": decode_json_list(syllabus["class_types_json"]),
                "class_type_note": syllabus["class_type_note"],
                "teaching_methods": decode_json_list(
                    syllabus["teaching_methods_json"]
                ),
                "teaching_method_note": syllabus["teaching_method_note"],
                "additional_materials": syllabus["additional_materials"],
                "other_weekly_content": syllabus["other_weekly_content"],
                "assignments": syllabus["assignments"],
                "course_notices": syllabus["course_notices"],
                "source_url": syllabus["source_url"],
                "extracted_at_utc": syllabus["extracted_at_utc"],
            }
        )
        details.append(detail)

        for item, (percentage_field, detail_field) in EVALUATION_COLUMNS.items():
            percentage = syllabus[percentage_field].strip()
            detail_value = syllabus[detail_field].strip()
            if percentage or detail_value:
                evaluations.append(
                    {
                        "evaluation_id": "",
                        "syllabus_id": syllabus["syllabus_id"],
                        "evaluation_item": item,
                        "percentage": percentage,
                        "detail": detail_value,
                    }
                )

    for row in sorted(textbooks, key=lambda item: int(item["textbook_id"])):
        raw_textbooks.append(
            {
                "textbook_id": "",
                "syllabus_id": row["syllabus_id"],
                "sequence": row["sequence"],
                "title": row["title"],
                "author": row["author"],
                "publisher": row["publisher"],
                "publication_year": row["publication_year"],
                "isbn": row["isbn"],
                "note": row["note"],
            }
        )

    for row in sorted(weekly_plans, key=lambda item: int(item["weekly_plan_id"])):
        raw_weekly_plans.append(
            {
                "weekly_plan_id": "",
                "syllabus_id": row["syllabus_id"],
                "week": row["week"],
                "date_range": row["date_range"],
                "topic_content": row["topic_content"],
                "note": row["note"],
            }
        )

    # Rule ordering preserves existing prerequisite IDs after rebuilding.
    for source in sorted(
        prerequisite_sources,
        key=lambda row: (int(row["prerequisite_id"]), int(row["source_syllabus_id"])),
    ):
        rule = rules.get(source["prerequisite_id"])
        if rule is None:
            raise SystemExit(
                "Unknown prerequisite_id in prerequisite_sources.csv: "
                f"{source['prerequisite_id']}"
            )
        raw_prerequisites.append(
            {
                "prerequisite_id": "",
                "syllabus_id": source["source_syllabus_id"],
                "prerequisite_type": rule["prerequisite_type"],
                "cohort_start": rule["cohort_start"],
                "cohort_end": rule["cohort_end"],
                "abeek_applicable": rule["abeek_applicable"],
                "prerequisite_group": rule["prerequisite_group"],
                "prerequisite_code": rule["prerequisite_course_code"],
                "prerequisite_name": rule["prerequisite_name"],
                "minimum_grade": rule["minimum_grade_code"],
                "minimum_required_count": rule["minimum_required_count"],
            }
        )

    prerequisite_counts = Counter(row["syllabus_id"] for row in raw_prerequisites)
    evaluation_counts = Counter(row["syllabus_id"] for row in evaluations)
    textbook_counts = Counter(row["syllabus_id"] for row in raw_textbooks)
    weekly_counts = Counter(row["syllabus_id"] for row in raw_weekly_plans)
    report: list[dict[str, str | int]] = []
    for detail in details:
        syllabus_id = detail["syllabus_id"]
        report.append(
            {
                "syllabus_id": syllabus_id,
                "offering_id": detail["offering_id"],
                "year": detail["year"],
                "term_code": detail["term_code"],
                "status": "extracted",
                "prerequisite_count": prerequisite_counts[syllabus_id],
                "evaluation_count": evaluation_counts[syllabus_id],
                "textbook_count": textbook_counts[syllabus_id],
                "weekly_plan_count": weekly_counts[syllabus_id],
                "error": "",
                "source_url": detail["source_url"],
            }
        )

    for index, row in enumerate(raw_prerequisites, 1):
        row["prerequisite_id"] = str(index)
    for index, row in enumerate(evaluations, 1):
        row["evaluation_id"] = str(index)
    for index, row in enumerate(raw_textbooks, 1):
        row["textbook_id"] = str(index)
    for index, row in enumerate(raw_weekly_plans, 1):
        row["weekly_plan_id"] = str(index)

    write_csv_atomic(args.output_dir / "syllabus_details.csv", DETAIL_FIELDS, details)
    write_csv_atomic(
        args.output_dir / "syllabus_prerequisites.csv",
        PREREQUISITE_FIELDS,
        raw_prerequisites,
    )
    write_csv_atomic(
        args.output_dir / "syllabus_evaluations.csv",
        EVALUATION_FIELDS,
        evaluations,
    )
    write_csv_atomic(
        args.output_dir / "syllabus_textbooks.csv", TEXTBOOK_FIELDS, raw_textbooks
    )
    write_csv_atomic(
        args.output_dir / "syllabus_weekly_plans.csv",
        WEEKLY_PLAN_FIELDS,
        raw_weekly_plans,
    )
    write_csv_atomic(args.output_dir / "extraction_report.csv", REPORT_FIELDS, report)

    print(f"Seeded extracted syllabi: {len(details)}")
    print(f"Seeded prerequisites: {len(raw_prerequisites)}")
    print(f"Seeded evaluations: {len(evaluations)}")
    print(f"Seeded textbooks: {len(raw_textbooks)}")
    print(f"Seeded weekly plans: {len(raw_weekly_plans)}")
    print(f"Output: {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
