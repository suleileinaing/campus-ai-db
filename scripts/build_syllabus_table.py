#!/usr/bin/env python3
"""Build the canonical database-ready syllabi table from extracted data."""

from __future__ import annotations

import csv
import json
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent.parent
BASE_SYLLABI = PROJECT_DIR / "processed_data" / "website_tables" / "syllabi.csv"
EXTRACTED_DETAILS = (
    PROJECT_DIR / "processed_data" / "syllabus_tables" / "syllabus_details.csv"
)
EXTRACTED_EVALUATIONS = (
    PROJECT_DIR / "processed_data" / "syllabus_tables" / "syllabus_evaluations.csv"
)
COURSE_OFFERINGS = (
    PROJECT_DIR / "processed_data" / "website_tables" / "course_offerings.csv"
)
OUTPUT = PROJECT_DIR / "processed_data" / "database_tables" / "syllabi.csv"
ENGLISH_VALIDATION_OUTPUT = (
    PROJECT_DIR / "validation_report" / "english_type_validation.csv"
)

HTML_ENGLISH_TYPES = {
    "": "NONE",
    "영어(부분)강좌": "PARTIAL",
    "전체영어강좌": "FULL",
}

ENGLISH_VALIDATION_FIELDS = [
    "syllabus_id",
    "offering_id",
    "course_code",
    "year",
    "semester",
    "section",
    "website_english_type",
    "syllabus_english_type",
    "raw_syllabus_value",
    "status",
]

EVALUATION_COLUMNS = {
    "중간고사": ("midterm_percentage", "midterm_detail"),
    "기말고사": ("final_exam_percentage", "final_exam_detail"),
    "과제보고서": ("assignment_percentage", "assignment_detail"),
    "발표": ("presentation_percentage", "presentation_detail"),
    "출석": ("attendance_percentage", "attendance_detail"),
    "기타": ("other_percentage", "other_detail"),
}

FIELDS = [
    "syllabus_id",
    "offering_id",
    "source_url",
    "professor_office",
    "personal_homepage",
    "course_homepage",
    "consultation_time",
    "overview",
    "objectives",
    "operation_modes",
    "operation_note",
    "class_types_json",
    "class_type_note",
    "teaching_methods_json",
    "teaching_method_note",
    "additional_materials",
    "other_weekly_content",
    "assignments",
    "course_notices",
    "midterm_percentage",
    "midterm_detail",
    "final_exam_percentage",
    "final_exam_detail",
    "assignment_percentage",
    "assignment_detail",
    "presentation_percentage",
    "presentation_detail",
    "attendance_percentage",
    "attendance_detail",
    "other_percentage",
    "other_detail",
    "extracted_at_utc",
]


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


def split_homepage(value: str) -> tuple[str, str]:
    personal_label = "[개인용]"
    course_label = "[수업용]"
    if personal_label not in value or course_label not in value:
        return value.strip(), ""
    personal_part, course_part = value.split(course_label, 1)
    personal = personal_part.split(personal_label, 1)[1].strip()
    return personal, course_part.strip()


def multi_value_json(value: str) -> str:
    values = [item.strip() for item in value.split("|") if item.strip()]
    return json.dumps(values, ensure_ascii=False)


def main() -> int:
    base_rows = read_csv(BASE_SYLLABI)
    detail_rows = read_csv(EXTRACTED_DETAILS)
    evaluation_rows = read_csv(EXTRACTED_EVALUATIONS)
    offerings_by_id = unique_index(
        read_csv(COURSE_OFFERINGS), "offering_id", "course_offerings.csv"
    )
    base_by_id = {row["syllabus_id"]: row for row in base_rows}
    evaluations_by_syllabus: dict[str, dict[str, dict[str, str]]] = {}

    for evaluation in evaluation_rows:
        item = evaluation["evaluation_item"]
        if item not in EVALUATION_COLUMNS:
            raise SystemExit(f"Unsupported evaluation item: {item}")
        syllabus_evaluations = evaluations_by_syllabus.setdefault(
            evaluation["syllabus_id"], {}
        )
        if item in syllabus_evaluations:
            raise SystemExit(
                f"Duplicate evaluation item for syllabus "
                f"{evaluation['syllabus_id']}: {item}"
            )
        syllabus_evaluations[item] = evaluation

    if len(base_by_id) != len(base_rows):
        raise SystemExit("Duplicate syllabus_id values found in website syllabi.csv")
    if len({row["syllabus_id"] for row in detail_rows}) != len(detail_rows):
        raise SystemExit("Duplicate syllabus_id values found in syllabus_details.csv")
    if set(base_by_id) != {row["syllabus_id"] for row in detail_rows}:
        raise SystemExit("The base and extracted syllabus_id sets do not match")

    output_rows = []
    english_validation_rows = []
    for detail in sorted(detail_rows, key=lambda row: int(row["syllabus_id"])):
        base = base_by_id[detail["syllabus_id"]]
        offering = offerings_by_id.get(base["offering_id"])
        if offering is None:
            raise SystemExit(
                f"Unknown offering_id for syllabus {detail['syllabus_id']}: "
                f"{base['offering_id']}"
            )
        if base["offering_id"] != detail["offering_id"]:
            raise SystemExit(
                f"Offering mismatch for syllabus {detail['syllabus_id']}: "
                f"{base['offering_id']} != {detail['offering_id']}"
            )
        if base["source_url"] != detail["source_url"]:
            raise SystemExit(
                f"Source URL mismatch for syllabus {detail['syllabus_id']}"
            )
        output = {
            field: (
                base[field]
                if field in {"syllabus_id", "offering_id", "source_url"}
                else detail.get(field, "")
            )
            for field in FIELDS
        }
        personal_homepage, course_homepage = split_homepage(detail["homepage"])
        output["personal_homepage"] = personal_homepage
        output["course_homepage"] = course_homepage
        output["class_types_json"] = multi_value_json(detail["class_types"])
        output["teaching_methods_json"] = multi_value_json(
            detail["teaching_methods"]
        )
        for item, (percentage_column, detail_column) in EVALUATION_COLUMNS.items():
            evaluation = evaluations_by_syllabus.get(detail["syllabus_id"], {}).get(item)
            if evaluation is not None:
                output[percentage_column] = evaluation["percentage"]
                output[detail_column] = evaluation["detail"]
        output_rows.append(output)

        raw_english = detail["english_course"].strip()
        syllabus_english = HTML_ENGLISH_TYPES.get(raw_english, "UNKNOWN")
        website_english = offering["english_type"].strip()
        status = (
            "UNKNOWN_HTML_VALUE"
            if syllabus_english == "UNKNOWN"
            else "MATCH" if syllabus_english == website_english else "CONFLICT"
        )
        english_validation_rows.append(
            {
                "syllabus_id": detail["syllabus_id"],
                "offering_id": base["offering_id"],
                "course_code": offering["course_code"],
                "year": offering["year"],
                "semester": offering["semester"],
                "section": offering["section"],
                "website_english_type": website_english,
                "syllabus_english_type": syllabus_english,
                "raw_syllabus_value": raw_english,
                "status": status,
            }
        )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    temporary = OUTPUT.with_suffix(".csv.tmp")
    with temporary.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(output_rows)
    temporary.replace(OUTPUT)

    ENGLISH_VALIDATION_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    validation_temporary = ENGLISH_VALIDATION_OUTPUT.with_suffix(".csv.tmp")
    with validation_temporary.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=ENGLISH_VALIDATION_FIELDS)
        writer.writeheader()
        writer.writerows(english_validation_rows)
    validation_temporary.replace(ENGLISH_VALIDATION_OUTPUT)

    print(f"Canonical syllabi: {len(output_rows)}")
    print(
        "English-type conflicts: "
        f"{sum(row['status'] != 'MATCH' for row in english_validation_rows)}"
    )
    print(f"Output: {OUTPUT}")
    print(f"Validation: {ENGLISH_VALIDATION_OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
