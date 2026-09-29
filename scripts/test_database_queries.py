#!/usr/bin/env python3
"""Run representative question-oriented checks against the CampusAI database."""

from __future__ import annotations

import sqlite3
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_DIR / "database" / "campus_ai.db"


TESTS = [
    (
        "course professor",
        """
        SELECT o.offering_id, p.name
        FROM course_offerings AS o
        JOIN offering_professors AS op ON op.offering_id = o.offering_id
        JOIN professors AS p ON p.professor_id = op.professor_id
        WHERE o.course_code = ? AND o.year = ? AND o.semester = ?
        """,
        ("CSE327", 2026, "2"),
    ),
    (
        "cohort-aware prerequisite",
        """
        SELECT DISTINCT prerequisite_name
        FROM course_prerequisites
        WHERE course_code = ?
          AND (cohort_start IS NULL OR cohort_start <= ?)
          AND (cohort_end IS NULL OR cohort_end >= ?)
        """,
        ("CSE203", 2026, 2026),
    ),
    (
        "weekly syllabus plan",
        """
        SELECT w.week, w.topic_content
        FROM course_offerings AS o
        JOIN syllabi AS s ON s.offering_id = o.offering_id
        JOIN syllabus_weekly_plans AS w ON w.syllabus_id = s.syllabus_id
        WHERE o.course_code = ? AND o.year = ? AND o.semester = ?
          AND o.section = ?
        ORDER BY w.week
        """,
        ("CSE327", 2026, "2", "01"),
    ),
    (
        "class-time search",
        """
        SELECT o.course_code, o.course_name, ct.room_code
        FROM course_offerings AS o
        JOIN class_times AS ct ON ct.offering_id = o.offering_id
        JOIN time_slots AS ts ON ts.time_slot_id = ct.time_slot_id
        WHERE o.year = ? AND o.semester = ?
          AND ts.day = ? AND ts.start_time = ?
        """,
        (2026, "2", "monday", "13:30"),
    ),
    (
        "evaluation method",
        """
        SELECT s.midterm_percentage, s.final_exam_percentage,
               s.assignment_percentage, s.presentation_percentage,
               s.attendance_percentage, s.other_percentage
        FROM course_offerings AS o
        JOIN syllabi AS s ON s.offering_id = o.offering_id
        WHERE o.course_code = ? AND o.year = ? AND o.semester = ?
          AND o.section = ?
        """,
        ("CSE327", 2026, "2", "01"),
    ),
    (
        "textbook",
        """
        SELECT t.title, t.author
        FROM course_offerings AS o
        JOIN syllabi AS s ON s.offering_id = o.offering_id
        JOIN syllabus_textbooks AS t ON t.syllabus_id = s.syllabus_id
        WHERE o.course_code = ? AND o.year = ? AND o.semester = ?
          AND o.section = ?
        """,
        ("CSE327", 2026, "2", "01"),
    ),
    (
        "industry-required courses",
        """
        SELECT course_code, course_name, section
        FROM course_offerings
        WHERE year = ? AND semester = ?
          AND industry_required = 1
        ORDER BY course_code, section
        """,
        (2026, "2"),
    ),
    (
        "student completed credits",
        """
        SELECT e.student_id, SUM(c.credits) AS completed_credits
        FROM enrollments AS e
        JOIN courses AS c ON c.course_code = e.course_code
        WHERE e.student_id = ?
          AND e.status = '완료'
          AND e.retaken = 0
        GROUP BY e.student_id
        HAVING SUM(c.credits) > 0
        """,
        (202210001,),
    ),
    (
        "student category progress",
        """
        WITH applicable_requirement AS (
            SELECT gr.requirement_id
            FROM students AS st
            JOIN graduation_requirements AS gr
              ON gr.department_id = st.department_id
             AND gr.track = st.track
             AND gr.cohort_start <= st.admission_year
             AND (gr.cohort_end IS NULL OR gr.cohort_end >= st.admission_year)
            WHERE st.student_id = ?
        ),
        earned AS (
            SELECT e.category_id, SUM(c.credits) AS earned_credits
            FROM enrollments AS e
            JOIN courses AS c ON c.course_code = e.course_code
            WHERE e.student_id = ?
              AND e.status = '완료'
              AND e.retaken = 0
            GROUP BY e.category_id
        )
        SELECT cc.category_name, rc.min_credits,
               COALESCE(earned.earned_credits, 0) AS earned_credits,
               MAX(rc.min_credits - COALESCE(earned.earned_credits, 0), 0)
                   AS remaining_credits
        FROM applicable_requirement AS ar
        JOIN requirement_categories AS rc ON rc.requirement_id = ar.requirement_id
        JOIN course_categories AS cc ON cc.category_id = rc.category_id
        LEFT JOIN earned ON earned.category_id = rc.category_id
        """,
        (202210001, 202210001),
    ),
    (
        "student unmet required courses",
        """
        WITH applicable_requirement AS (
            SELECT gr.requirement_id
            FROM students AS st
            JOIN graduation_requirements AS gr
              ON gr.department_id = st.department_id
             AND gr.track = st.track
             AND gr.cohort_start <= st.admission_year
             AND (gr.cohort_end IS NULL OR gr.cohort_end >= st.admission_year)
            WHERE st.student_id = ?
        )
        SELECT rc.course_code, c.current_name
        FROM applicable_requirement AS ar
        JOIN requirement_courses AS rc ON rc.requirement_id = ar.requirement_id
        JOIN courses AS c ON c.course_code = rc.course_code
        WHERE NOT EXISTS (
            SELECT 1
            FROM enrollments AS e
            WHERE e.student_id = ?
              AND e.course_code = rc.course_code
              AND e.status = '완료'
              AND e.retaken = 0
        )
        """,
        (202210001, 202210001),
    ),
    (
        "student industry-required progress",
        """
        SELECT ro.condition,
               COALESCE(SUM(CASE
                   WHEN e.status = '완료' AND e.retaken = 0
                   THEN c.credits ELSE 0 END), 0) AS earned_industry_credits
        FROM students AS st
        JOIN graduation_requirements AS gr
          ON gr.department_id = st.department_id
         AND gr.track = st.track
         AND gr.cohort_start <= st.admission_year
         AND (gr.cohort_end IS NULL OR gr.cohort_end >= st.admission_year)
        JOIN requirement_others AS ro
          ON ro.requirement_id = gr.requirement_id AND ro.type = '산학필수'
        LEFT JOIN enrollments AS e ON e.student_id = st.student_id
        LEFT JOIN course_offerings AS o
          ON o.offering_id = e.offering_id AND o.industry_required = 1
        LEFT JOIN courses AS c ON c.course_code = o.course_code
        WHERE st.student_id = ?
        GROUP BY ro.requirement_other_id, ro.condition
        """,
        (202210001,),
    ),
]


def main() -> int:
    if not DATABASE_PATH.is_file():
        raise FileNotFoundError(
            f"Database not found: {DATABASE_PATH}\n"
            "Run: python3 scripts/build_database.py"
        )

    connection = sqlite3.connect(f"file:{DATABASE_PATH}?mode=ro", uri=True)
    failures = 0
    try:
        integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
        if integrity != "ok":
            raise RuntimeError(f"Database integrity check failed: {integrity}")

        for name, sql, parameters in TESTS:
            count = len(connection.execute(sql, parameters).fetchall())
            status = "PASS" if count > 0 else "FAIL"
            failures += count == 0
            print(f"[{status}] {name}: {count} row(s)")
    finally:
        connection.close()

    if failures:
        print(f"Result: {failures} test(s) failed")
        return 1
    print(f"Result: all {len(TESTS)} tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
