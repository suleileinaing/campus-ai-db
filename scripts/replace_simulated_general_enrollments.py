#!/usr/bin/env python3
"""Replace simulated general-course offerings in enrollments with real offerings.

The assignment is deterministic: candidates must match year, semester, and the
same semantic general-education category. A fixed seed makes reruns auditable.
"""

from __future__ import annotations

import csv
import random
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WEBSITE = ROOT / "processed_data" / "website_tables"
SIMULATED = ROOT / "processed_data" / "simulated"
SEED = 20260929

ENROLLMENT_FIELDS = [
    "enrollment_id", "student_id", "offering_id", "course_code",
    "category_id", "grade", "status", "is_retake", "retaken",
]
MAP_FIELDS = [
    "source_course_code", "source_course_name", "source_offering_id",
    "source_year", "source_semester", "target_course_code",
    "target_course_name", "target_offering_id", "target_year",
    "target_semester", "target_category_id", "affected_enrollment_count",
    "duplicate_risk_count", "replacement_reason",
]

# Codes 16 and 14 are both labelled 필수교과 in the public category table.
EQUIVALENT_CATEGORIES = {"4": {"4", "11"}, "5": {"5"}, "6": {"6"}}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def main() -> None:
    enrollments = read_csv(SIMULATED / "enrollments.csv")
    simulated_courses = {
        row["course_code"]: row for row in read_csv(SIMULATED / "general_courses.csv")
    }
    simulated_offerings = {
        row["offering_id"]: row
        for row in read_csv(SIMULATED / "general_course_offerings.csv")
    }
    simulated_categories = {
        row["offering_id"]: row
        for row in read_csv(SIMULATED / "general_course_offering_categories.csv")
    }
    real_courses = {
        row["course_code"]: row for row in read_csv(WEBSITE / "courses.csv")
    }
    real_offerings = {
        row["offering_id"]: row
        for row in read_csv(WEBSITE / "course_offerings.csv")
    }
    real_category_rows = read_csv(WEBSITE / "course_offering_categories.csv")

    categories_by_offering: dict[str, set[str]] = defaultdict(set)
    for row in real_category_rows:
        categories_by_offering[row["offering_id"]].add(row["category_id"])

    affected_by_source: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in enrollments:
        if row["offering_id"] in simulated_offerings:
            affected_by_source[row["offering_id"]].append(row)

    if not affected_by_source:
        print("No enrollments reference simulated general-course offerings; no changes made.")
        return

    occupied_by_student: dict[str, set[str]] = defaultdict(set)
    for row in enrollments:
        if row["offering_id"] not in simulated_offerings:
            occupied_by_student[row["student_id"]].add(row["offering_id"])

    candidates_by_key: dict[tuple[str, str, str], list[tuple[dict[str, str], str]]] = defaultdict(list)
    for offering_id, offering in real_offerings.items():
        for source_category, allowed in EQUIVALENT_CATEGORIES.items():
            matching = sorted(categories_by_offering[offering_id] & allowed, key=int)
            if matching:
                candidates_by_key[(offering["year"], offering["semester"], source_category)].append(
                    (offering, matching[0])
                )

    rng = random.Random(SEED)
    used_targets: set[str] = set()
    assignment: dict[str, tuple[dict[str, str], str]] = {}

    for source_id in sorted(affected_by_source, key=int):
        source = simulated_offerings[source_id]
        source_category = simulated_categories[source_id]["category_id"]
        key = (source["year"], source["semester"], source_category)
        candidates = list(candidates_by_key[key])
        rng.shuffle(candidates)
        students = {row["student_id"] for row in affected_by_source[source_id]}

        valid = [
            candidate
            for candidate in candidates
            if candidate[0]["offering_id"] not in used_targets
            and all(candidate[0]["offering_id"] not in occupied_by_student[s] for s in students)
        ]
        if not valid:
            valid = [
                candidate
                for candidate in candidates
                if all(candidate[0]["offering_id"] not in occupied_by_student[s] for s in students)
            ]
        if not valid:
            raise ValueError(f"No safe real offering candidate for simulated offering {source_id}")

        target, target_category = valid[0]
        assignment[source_id] = (target, target_category)
        used_targets.add(target["offering_id"])
        for student_id in students:
            occupied_by_student[student_id].add(target["offering_id"])

    updated = []
    for row in enrollments:
        source_id = row["offering_id"]
        if source_id in assignment:
            target, target_category = assignment[source_id]
            row = dict(row)
            row["offering_id"] = target["offering_id"]
            row["course_code"] = target["course_code"]
            row["category_id"] = target_category
        updated.append(row)

    duplicates = Counter((row["student_id"], row["offering_id"]) for row in updated)
    duplicate_rows = [key for key, count in duplicates.items() if count > 1]
    if duplicate_rows:
        raise ValueError(f"Duplicate student/offering rows after replacement: {duplicate_rows[:10]}")

    mapping_rows = []
    for source_id in sorted(assignment, key=int):
        source = simulated_offerings[source_id]
        target, target_category = assignment[source_id]
        mapping_rows.append({
            "source_course_code": source["course_code"],
            "source_course_name": simulated_courses[source["course_code"]]["current_name"],
            "source_offering_id": source_id,
            "source_year": source["year"],
            "source_semester": source["semester"],
            "target_course_code": target["course_code"],
            "target_course_name": real_courses[target["course_code"]]["current_name"],
            "target_offering_id": target["offering_id"],
            "target_year": target["year"],
            "target_semester": target["semester"],
            "target_category_id": target_category,
            "affected_enrollment_count": str(len(affected_by_source[source_id])),
            "duplicate_risk_count": "0",
            "replacement_reason": f"deterministic random assignment; same year/semester/category; seed={SEED}",
        })

    write_csv(SIMULATED / "enrollments.csv", ENROLLMENT_FIELDS, updated)
    write_csv(SIMULATED / "enrollment_replacement_map.csv", MAP_FIELDS, mapping_rows)

    print(f"Simulated offerings replaced: {len(assignment)}")
    print(f"Enrollments updated: {sum(len(rows) for rows in affected_by_source.values())}")
    print(f"Unique target offerings: {len({row['target_offering_id'] for row in mapping_rows})}")
    print("Duplicate student/offering rows: 0")


if __name__ == "__main__":
    main()
