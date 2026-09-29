#!/usr/bin/env python3
"""Build an integrity-checked SQLite database from public and simulated CSVs."""

from __future__ import annotations

import argparse
import csv
import sqlite3
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent.parent
SCHEMA_PATH = PROJECT_DIR / "database" / "schema.sql"
DEFAULT_OUTPUT = PROJECT_DIR / "database" / "campus_ai.db"
WEBSITE_TABLES = PROJECT_DIR / "processed_data" / "website_tables"
DATABASE_TABLES = PROJECT_DIR / "processed_data" / "database_tables"
SIMULATED_TABLES = PROJECT_DIR / "processed_data" / "simulated"

# Repeated table names mean append. Generated simulated IDs do not overlap the
# public-data IDs, so both sources can coexist in the same normalized tables.
IMPORTS = [
    ("departments", WEBSITE_TABLES / "departments.csv"),
    ("course_categories", WEBSITE_TABLES / "course_categories.csv"),
    ("professors", WEBSITE_TABLES / "professors.csv"),
    ("professors", SIMULATED_TABLES / "simulated_professors.csv"),
    ("students", SIMULATED_TABLES / "students.csv"),
    ("courses", WEBSITE_TABLES / "courses.csv"),
    ("courses", DATABASE_TABLES / "supplemental_courses.csv"),
    ("courses", SIMULATED_TABLES / "general_courses.csv"),
    ("course_offerings", WEBSITE_TABLES / "course_offerings.csv"),
    ("course_offerings", SIMULATED_TABLES / "general_course_offerings.csv"),
    ("offering_professors", WEBSITE_TABLES / "offering_professors.csv"),
    ("offering_professors", SIMULATED_TABLES / "simulated_offering_professors.csv"),
    ("course_offering_categories", WEBSITE_TABLES / "course_offering_categories.csv"),
    (
        "course_offering_categories",
        SIMULATED_TABLES / "general_course_offering_categories.csv",
    ),
    ("time_slots", WEBSITE_TABLES / "time_slots.csv"),
    ("time_slots", SIMULATED_TABLES / "simulated_time_slots.csv"),
    ("class_times", WEBSITE_TABLES / "class_times.csv"),
    ("class_times", SIMULATED_TABLES / "simulated_class_times.csv"),
    ("syllabi", DATABASE_TABLES / "syllabi.csv"),
    ("course_prerequisites", DATABASE_TABLES / "course_prerequisites.csv"),
    ("prerequisite_sources", DATABASE_TABLES / "prerequisite_sources.csv"),
    ("syllabus_textbooks", DATABASE_TABLES / "syllabus_textbooks.csv"),
    ("syllabus_weekly_plans", DATABASE_TABLES / "syllabus_weekly_plans.csv"),
    ("graduation_requirements", DATABASE_TABLES / "graduation_requirements.csv"),
    ("requirement_categories", DATABASE_TABLES / "requirement_categories.csv"),
    (
        "requirement_categories",
        SIMULATED_TABLES / "simulated_general_requirement_categories.csv",
    ),
    ("requirement_courses", DATABASE_TABLES / "requirement_courses.csv"),
    ("requirement_others", DATABASE_TABLES / "requirement_others.csv"),
    (
        "requirement_fulfillment_options",
        SIMULATED_TABLES / "requirement_fulfillment_options.csv",
    ),
    ("enrollments", SIMULATED_TABLES / "enrollments.csv"),
]

INTEGER_COLUMNS = {
    "department_id", "professor_id", "credits", "offering_id", "target_year",
    "year", "capacity", "category_id", "offering_category_id", "time_slot_id",
    "class_time_id", "student_id", "admission_year", "enrollment_id",
    "syllabus_id", "prerequisite_id", "cohort_start", "cohort_end",
    "minimum_required_count", "source_syllabus_id", "textbook_id", "sequence",
    "weekly_plan_id", "week", "requirement_id", "total_credits",
    "requirement_category_id", "min_credits", "min_areas",
    "per_area_min_credits", "requirement_course_id", "requirement_other_id",
    "fulfillment_option_id", "target_other_id",
}
REAL_COLUMNS = {
    "midterm_percentage", "final_exam_percentage", "assignment_percentage",
    "presentation_percentage", "attendance_percentage", "other_percentage",
}
BOOLEAN_COLUMNS = {
    "has_track", "abeek_applicable", "industry_required", "is_retake", "retaken",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build the CampusAI SQLite database from processed CSV tables."
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def convert_value(column: str, value: str):
    value = value.strip()
    if value == "":
        return None
    if column in BOOLEAN_COLUMNS:
        normalized = value.upper()
        if normalized in {"1", "TRUE", "Y", "YES"}:
            return 1
        if normalized in {"0", "FALSE", "N", "NO"}:
            return 0
        raise ValueError(f"Unsupported boolean value for {column}: {value!r}")
    if column in INTEGER_COLUMNS:
        return int(value)
    if column in REAL_COLUMNS:
        return float(value)
    return value


def load_csv(path: Path) -> tuple[list[str], list[tuple]]:
    if not path.is_file():
        raise FileNotFoundError(f"Required CSV not found: {path}")
    with path.open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        if not reader.fieldnames:
            raise ValueError(f"CSV has no header: {path}")
        columns = reader.fieldnames
        rows = [
            tuple(convert_value(column, row[column]) for column in columns)
            for row in reader
        ]
    return columns, rows


def import_table(connection: sqlite3.Connection, table: str, path: Path) -> int:
    columns, rows = load_csv(path)
    database_columns = {
        row[1] for row in connection.execute(f'PRAGMA table_info("{table}")')
    }
    if set(columns) != database_columns:
        missing = sorted(database_columns.difference(columns))
        extra = sorted(set(columns).difference(database_columns))
        raise ValueError(
            f"{table} ({path.name}): CSV/schema column mismatch; "
            f"missing={missing}, extra={extra}"
        )
    quoted_columns = ", ".join(f'"{column}"' for column in columns)
    placeholders = ", ".join("?" for _ in columns)
    connection.executemany(
        f'INSERT INTO "{table}" ({quoted_columns}) VALUES ({placeholders})', rows
    )
    return len(rows)


def validate_enrollment_course_consistency(connection: sqlite3.Connection) -> None:
    mismatches = connection.execute(
        """
        SELECT e.enrollment_id, e.course_code, o.course_code
        FROM enrollments AS e
        JOIN course_offerings AS o ON o.offering_id = e.offering_id
        WHERE e.course_code <> o.course_code
        LIMIT 10
        """
    ).fetchall()
    if mismatches:
        raise ValueError(f"Enrollment/offering course mismatch: {mismatches}")


def build_database(output: Path) -> dict[str, int]:
    if not SCHEMA_PATH.is_file():
        raise FileNotFoundError(f"Schema not found: {SCHEMA_PATH}")
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(output.suffix + ".tmp")
    if temporary.exists():
        temporary.unlink()

    counts: dict[str, int] = defaultdict(int)
    connection = sqlite3.connect(temporary)
    try:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
        with connection:
            for table, path in IMPORTS:
                counts[table] += import_table(connection, table, path)

        validate_enrollment_course_consistency(connection)
        foreign_key_errors = connection.execute("PRAGMA foreign_key_check").fetchall()
        if foreign_key_errors:
            raise ValueError(f"Foreign-key check failed: {foreign_key_errors[:10]}")
        integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
        if integrity != "ok":
            raise ValueError(f"SQLite integrity check failed: {integrity}")
        connection.execute("ANALYZE")
        connection.commit()
    except Exception:
        connection.close()
        if temporary.exists():
            temporary.unlink()
        raise
    else:
        connection.close()

    temporary.replace(output)
    return dict(counts)


def main() -> int:
    args = parse_args()
    counts = build_database(args.output)
    print(f"Built at: {datetime.now(timezone.utc).isoformat()}")
    for table, count in counts.items():
        print(f"{table}: {count}")
    print(f"Database: {args.output.resolve()}")
    print("Enrollment/offering course check: PASS")
    print("Foreign-key check: PASS")
    print("Integrity check: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
