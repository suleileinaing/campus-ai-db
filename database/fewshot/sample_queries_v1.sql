-- 1. Who teaches a course in a specific semester?
SELECT
    o.year,
    o.semester,
    o.course_code,
    o.section,
    o.course_name,
    GROUP_CONCAT(p.name, ', ') AS professors
FROM course_offerings AS o
LEFT JOIN offering_professors AS op ON op.offering_id = o.offering_id
LEFT JOIN professors AS p ON p.professor_id = op.professor_id
WHERE o.course_code = 'CSE406'
  AND o.year = 2026
  AND o.semester = '2'
GROUP BY o.offering_id
ORDER BY o.section;

-- 2. What prerequisites apply to a course and admission year?
SELECT DISTINCT
    prerequisite_name,
    prerequisite_course_code,
    prerequisite_type,
    minimum_grade_code,
    prerequisite_group
FROM course_prerequisites
WHERE course_code = 'CSE203'
  AND (cohort_start IS NULL OR cohort_start <= 2026)
  AND (cohort_end IS NULL OR cohort_end >= 2026)
ORDER BY prerequisite_type, prerequisite_group, prerequisite_name;

-- 3. What is taught each week for one offering?
SELECT
    o.course_code,
    o.course_name,
    o.year,
    o.semester,
    o.section,
    w.week,
    w.date_range,
    w.topic_content,
    w.note
FROM course_offerings AS o
JOIN syllabi AS s ON s.offering_id = o.offering_id
JOIN syllabus_weekly_plans AS w ON w.syllabus_id = s.syllabus_id
WHERE o.course_code = 'CSE327'
  AND o.year = 2026
  AND o.semester = '2'
  AND o.section = '01'
ORDER BY w.week;

-- 4. Which classes begin Monday at 13:30 in a specific semester?
SELECT
    o.course_code,
    o.course_name,
    o.section,
    ts.day,
    ts.start_time,
    ts.end_time,
    ct.room_code
FROM course_offerings AS o
JOIN class_times AS ct ON ct.offering_id = o.offering_id
JOIN time_slots AS ts ON ts.time_slot_id = ct.time_slot_id
WHERE o.year = 2026
  AND o.semester = '2'
  AND ts.day = 'monday'
  AND ts.start_time = '13:30'
ORDER BY o.course_code, o.section;

-- 5. How is a course evaluated?
SELECT
    o.course_code,
    o.course_name,
    s.midterm_percentage,
    s.final_exam_percentage,
    s.assignment_percentage,
    s.presentation_percentage,
    s.attendance_percentage,
    s.other_percentage
FROM course_offerings AS o
JOIN syllabi AS s ON s.offering_id = o.offering_id
WHERE o.course_code = 'CSE327'
  AND o.year = 2026
  AND o.semester = '2'
  AND o.section = '01';

-- 6. Which textbook is used for a course?
SELECT
    o.course_code,
    o.course_name,
    t.sequence,
    t.title,
    t.author,
    t.publisher,
    t.isbn
FROM course_offerings AS o
JOIN syllabi AS s ON s.offering_id = o.offering_id
JOIN syllabus_textbooks AS t ON t.syllabus_id = s.syllabus_id
WHERE o.course_code = 'CSE327'
  AND o.year = 2026
  AND o.semester = '2'
  AND o.section = '01'
ORDER BY t.sequence;

-- 7. Which courses are marked as industry-required (산학필수)?
SELECT
    course_code,
    course_name,
    section,
    year,
    semester
FROM course_offerings
WHERE year = 2026
  AND semester = '2'
  AND industry_required = 1
ORDER BY course_code, section;

-- 8. How many credits has a student completed?
SELECT
    e.student_id,
    SUM(c.credits) AS completed_credits
FROM enrollments AS e
JOIN courses AS c ON c.course_code = e.course_code
WHERE e.student_id = 202210001
  AND e.status = '완료'
  AND e.retaken = 0
GROUP BY e.student_id;

-- 9. How many credits remain in each graduation category?
WITH applicable_requirement AS (
    SELECT gr.requirement_id
    FROM students AS st
    JOIN graduation_requirements AS gr
      ON gr.department_id = st.department_id
     AND gr.track = st.track
     AND gr.cohort_start <= st.admission_year
     AND (gr.cohort_end IS NULL OR gr.cohort_end >= st.admission_year)
    WHERE st.student_id = 202210001
),
earned AS (
    SELECT e.category_id, SUM(c.credits) AS earned_credits
    FROM enrollments AS e
    JOIN courses AS c ON c.course_code = e.course_code
    WHERE e.student_id = 202210001
      AND e.status = '완료'
      AND e.retaken = 0
    GROUP BY e.category_id
)
SELECT
    cc.category_name,
    rc.min_credits,
    COALESCE(earned.earned_credits, 0) AS earned_credits,
    MAX(rc.min_credits - COALESCE(earned.earned_credits, 0), 0)
        AS remaining_credits
FROM applicable_requirement AS ar
JOIN requirement_categories AS rc ON rc.requirement_id = ar.requirement_id
JOIN course_categories AS cc ON cc.category_id = rc.category_id
LEFT JOIN earned ON earned.category_id = rc.category_id
ORDER BY rc.requirement_category_id;

-- 10. Which required courses has a student not completed yet?
WITH applicable_requirement AS (
    SELECT gr.requirement_id
    FROM students AS st
    JOIN graduation_requirements AS gr
      ON gr.department_id = st.department_id
     AND gr.track = st.track
     AND gr.cohort_start <= st.admission_year
     AND (gr.cohort_end IS NULL OR gr.cohort_end >= st.admission_year)
    WHERE st.student_id = 202210001
)
SELECT rc.course_code, c.current_name, cc.category_name
FROM applicable_requirement AS ar
JOIN requirement_courses AS rc ON rc.requirement_id = ar.requirement_id
JOIN courses AS c ON c.course_code = rc.course_code
JOIN course_categories AS cc ON cc.category_id = rc.category_id
WHERE NOT EXISTS (
    SELECT 1
    FROM enrollments AS e
    WHERE e.student_id = 202210001
      AND e.course_code = rc.course_code
      AND e.status = '완료'
      AND e.retaken = 0
)
ORDER BY cc.category_name, rc.course_code;

-- 11. How much of the industry-required requirement has a student completed?
SELECT
    ro.condition AS requirement_condition,
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
WHERE st.student_id = 202210001
GROUP BY ro.requirement_other_id, ro.condition;
