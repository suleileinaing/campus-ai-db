-- 1. 2024학년도 2학기 AI1002-00 인공지능프로그래밍과 CSE203-00 컴퓨터구조를 모두 담당한 교수 이름을 알려줘.
SELECT p.name
FROM professors AS p
WHERE p.professor_id IN (
    SELECT op.professor_id
    FROM course_offerings AS o
    JOIN offering_professors AS op ON op.offering_id = o.offering_id
    WHERE o.year = 2024 AND o.semester = '2'
      AND o.course_code = 'AI1002' AND o.section = '00'
    INTERSECT
    SELECT op.professor_id
    FROM course_offerings AS o
    JOIN offering_professors AS op ON op.offering_id = o.offering_id
    WHERE o.year = 2024 AND o.semester = '2'
      AND o.course_code = 'CSE203' AND o.section = '00'
)
ORDER BY p.name;

-- 2. 2024학년도 2학기 AI1002-00 인공지능프로그래밍의 요일, 시작·종료 시간과 강의실을 알려줘.
SELECT ts.day, ts.start_time, ts.end_time, ct.room_code
FROM course_offerings AS o
JOIN class_times AS ct ON ct.offering_id = o.offering_id
JOIN time_slots AS ts ON ts.time_slot_id = ct.time_slot_id
WHERE o.year = 2024 AND o.semester = '2'
  AND o.course_code = 'AI1002' AND o.section = '00'
ORDER BY ts.day, ts.start_time, ct.room_code;

-- 3. 2024학년도 2학기 AI1002-00 인공지능프로그래밍의 영어강좌 구분을 영어전체·영어부분·해당없음으로, 산학필수 여부를 예·아니오로 알려줘.
SELECT CASE o.english_type
           WHEN 'FULL' THEN '영어전체'
           WHEN 'PARTIAL' THEN '영어부분'
           ELSE '해당없음'
       END AS english_course_type,
       CASE o.industry_required
           WHEN 1 THEN '예'
           ELSE '아니오'
       END AS industry_required
FROM course_offerings AS o
WHERE o.year = 2024 AND o.semester = '2'
  AND o.course_code = 'AI1002' AND o.section = '00';

-- 4. 2022학번과 2024학번의 교양 기본구조를 비교하면 2024학번의 총 교양 최소학점과 배분이수 최소학점은 각각 몇 학점 줄었어?
WITH cohort_requirements AS (
    SELECT 2022 AS admission_year,
           gr.total_general_credits,
           gc.min_credits AS distribution_credits
    FROM general_education_requirements AS gr
    JOIN general_education_requirement_categories AS gc
      ON gc.general_requirement_id = gr.general_requirement_id
     AND gc.requirement_code = 'DISTRIBUTION'
    WHERE 2022 BETWEEN gr.cohort_start AND COALESCE(gr.cohort_end, 9999)
    UNION ALL
    SELECT 2024 AS admission_year,
           gr.total_general_credits,
           gc.min_credits AS distribution_credits
    FROM general_education_requirements AS gr
    JOIN general_education_requirement_categories AS gc
      ON gc.general_requirement_id = gr.general_requirement_id
     AND gc.requirement_code = 'DISTRIBUTION'
    WHERE 2024 BETWEEN gr.cohort_start AND COALESCE(gr.cohort_end, 9999)
)
SELECT MAX(CASE WHEN admission_year = 2022 THEN total_general_credits END)
         - MAX(CASE WHEN admission_year = 2024 THEN total_general_credits END)
           AS total_general_credit_reduction,
       MAX(CASE WHEN admission_year = 2022 THEN distribution_credits END)
         - MAX(CASE WHEN admission_year = 2024 THEN distribution_credits END)
           AS distribution_credit_reduction
FROM cohort_requirements;

-- 5. 2024학년도 2학기 AI3008-00 설명및신뢰가능한AI의 중간고사와 기말고사 반영 비율은 각각 몇 퍼센트야?
SELECT s.midterm_percentage, s.final_exam_percentage
FROM course_offerings AS o
JOIN syllabi AS s ON s.offering_id = o.offering_id
WHERE o.year = 2024 AND o.semester = '2'
  AND o.course_code = 'AI3008' AND o.section = '00';

-- 6. 2024학번 학생에게 적용되는 CSE204 자료구조의 필수 선수과목 이름과 최소 성적 기준을 알려줘.
SELECT DISTINCT cp.prerequisite_name, cp.minimum_grade_code
FROM course_prerequisites AS cp
WHERE cp.course_code = 'CSE204'
  AND cp.prerequisite_type = 'REQUIRED'
  AND (cp.cohort_start IS NULL OR cp.cohort_start <= 2024)
  AND (cp.cohort_end IS NULL OR cp.cohort_end >= 2024)
ORDER BY cp.prerequisite_name;

-- 7. 2024학년도 2학기 인공지능학과 개설목록에서 AI1002 각 분반에 적용된 이수구분을 알려줘.
SELECT o.section, cc.category_name
FROM course_offerings AS o
JOIN course_offering_categories AS oc ON oc.offering_id = o.offering_id
JOIN departments AS d ON d.department_id = oc.department_id
JOIN course_categories AS cc ON cc.category_id = oc.category_id
WHERE o.year = 2024 AND o.semester = '2'
  AND o.course_code = 'AI1002'
  AND d.name = '인공지능학과'
ORDER BY o.section;

-- 8. 2024학년도 2학기 인공지능학과 개설목록에서 전공선택으로 분류된 강좌의 분반 수와 개설학점 합계를 알려줘.
SELECT COUNT(DISTINCT o.offering_id) AS section_count,
       SUM(o.credits) AS total_credits
FROM course_offerings AS o
JOIN course_offering_categories AS oc ON oc.offering_id = o.offering_id
JOIN departments AS d ON d.department_id = oc.department_id
JOIN course_categories AS cc ON cc.category_id = oc.category_id
WHERE o.year = 2024 AND o.semester = '2'
  AND d.name = '인공지능학과'
  AND cc.category_name = '전공선택';

-- 9. 2024학년도 2학기 AI3008-00 설명및신뢰가능한AI에서 중간고사 75점, 기말고사 85점을 받았다면 두 시험이 최종 100점에 기여하는 점수 합은 얼마야? 다른 항목은 제외해줘.
SELECT ROUND(
           75 * s.midterm_percentage / 100.0
         + 85 * s.final_exam_percentage / 100.0,
           2
       ) AS exam_contribution_points
FROM course_offerings AS o
JOIN syllabi AS s ON s.offering_id = o.offering_id
WHERE o.year = 2024 AND o.semester = '2'
  AND o.course_code = 'AI3008' AND o.section = '00';

-- 10. 2024학년도 2학기 CSE302-02 컴퓨터네트워크 담당 교수가 같은 학기 인공지능학과 개설목록에서 맡은 다른 과목의 분반 수와 개설학점 합계를 알려줘. CSE302의 다른 분반도 제외해줘.
WITH anchor_professors AS (
    SELECT DISTINCT op.professor_id
    FROM course_offerings AS o
    JOIN offering_professors AS op ON op.offering_id = o.offering_id
    WHERE o.year = 2024 AND o.semester = '2'
      AND o.course_code = 'CSE302' AND o.section = '02'
), target_offerings AS (
    SELECT DISTINCT o.offering_id, o.credits
    FROM course_offerings AS o
    JOIN offering_professors AS op ON op.offering_id = o.offering_id
    JOIN anchor_professors AS ap ON ap.professor_id = op.professor_id
    JOIN course_offering_categories AS oc ON oc.offering_id = o.offering_id
    JOIN departments AS d ON d.department_id = oc.department_id
    WHERE o.year = 2024 AND o.semester = '2'
      AND d.name = '인공지능학과'
      AND o.course_code <> 'CSE302'
)
SELECT COUNT(*) AS section_count, SUM(credits) AS total_credits
FROM target_offerings;

-- 11. 2024학년도 2학기 AI4001-00 캡스톤디자인 담당 교수가 같은 학기 컴퓨터공학과 개설목록에서 맡은 다른 과목의 코드와 분반을 알려줘. AI4001의 다른 분반도 제외해줘.
WITH anchor_professors AS (
    SELECT DISTINCT op.professor_id
    FROM course_offerings AS o
    JOIN offering_professors AS op ON op.offering_id = o.offering_id
    WHERE o.year = 2024 AND o.semester = '2'
      AND o.course_code = 'AI4001' AND o.section = '00'
)
SELECT DISTINCT o.course_code, o.section
FROM course_offerings AS o
JOIN offering_professors AS op ON op.offering_id = o.offering_id
JOIN anchor_professors AS ap ON ap.professor_id = op.professor_id
JOIN course_offering_categories AS oc ON oc.offering_id = o.offering_id
JOIN departments AS d ON d.department_id = oc.department_id
WHERE o.year = 2024 AND o.semester = '2'
  AND d.name = '컴퓨터공학과'
  AND o.course_code <> 'AI4001'
ORDER BY o.course_code, o.section;

-- 12. 2024학년도 2학기 CSE302-02 컴퓨터네트워크 담당 교수의 다른 수업 중, 같은 학기 인공지능학과 기준 전공필수이면서 3학점인 강좌의 과목코드, 분반과 학점을 알려줘. CSE302의 다른 분반도 제외해줘.
WITH anchor_professors AS (
    SELECT DISTINCT op.professor_id
    FROM course_offerings AS o
    JOIN offering_professors AS op ON op.offering_id = o.offering_id
    WHERE o.year = 2024 AND o.semester = '2'
      AND o.course_code = 'CSE302' AND o.section = '02'
)
SELECT DISTINCT o.course_code, o.section, o.credits
FROM course_offerings AS o
JOIN offering_professors AS op ON op.offering_id = o.offering_id
JOIN anchor_professors AS ap ON ap.professor_id = op.professor_id
JOIN course_offering_categories AS oc ON oc.offering_id = o.offering_id
JOIN departments AS d ON d.department_id = oc.department_id
JOIN course_categories AS cc ON cc.category_id = oc.category_id
WHERE o.year = 2024 AND o.semester = '2'
  AND d.name = '인공지능학과'
  AND cc.category_name = '전공필수'
  AND o.credits = 3
  AND o.course_code <> 'CSE302'
ORDER BY o.course_code, o.section;

-- 13. 로그인 학생 202210029가 완료했고 재수강으로 대체되지 않은 과목의 총 이수학점은 얼마야?
SELECT COALESCE(SUM(o.credits), 0) AS completed_credits
FROM enrollments AS e
JOIN course_offerings AS o ON o.offering_id = e.offering_id
WHERE e.student_id = 202210029
  AND e.status = '완료' AND e.retaken = 0;

-- 14. 로그인 학생 202210029의 수강기록을 상태별로 나눠 각 기록 수를 알려줘.
SELECT e.status, COUNT(*) AS enrollment_count
FROM enrollments AS e
WHERE e.student_id = 202210029
GROUP BY e.status
ORDER BY e.status;

-- 15. 로그인 학생 202210029가 완료한 과목 중 가장 낮은 성적을 받은 과목명과 성적을 알려줘. 동률은 모두 포함해줘.
WITH graded AS (
    SELECT o.course_name, e.grade,
           CASE e.grade
               WHEN 'F' THEN 0 WHEN 'D-' THEN 1 WHEN 'D0' THEN 2 WHEN 'D+' THEN 3
               WHEN 'C-' THEN 4 WHEN 'C0' THEN 5 WHEN 'C+' THEN 6
               WHEN 'B-' THEN 7 WHEN 'B0' THEN 8 WHEN 'B+' THEN 9
               WHEN 'A-' THEN 10 WHEN 'A0' THEN 11 WHEN 'A+' THEN 12
           END AS grade_rank
    FROM enrollments AS e
    JOIN course_offerings AS o ON o.offering_id = e.offering_id
    WHERE e.student_id = 202210029
      AND e.status = '완료' AND e.retaken = 0
      AND e.grade IS NOT NULL
)
SELECT course_name, grade
FROM graded
WHERE grade_rank = (SELECT MIN(grade_rank) FROM graded)
ORDER BY course_name;

-- 16. 로그인 학생 202210029에게 적용되는 전공 졸업요건의 총 이수학점은 얼마야?
SELECT gr.total_credits
FROM students AS st
JOIN graduation_requirements AS gr
  ON gr.department_id = st.department_id
 AND gr.track = st.track
 AND gr.cohort_start <= st.admission_year
 AND (gr.cohort_end IS NULL OR gr.cohort_end >= st.admission_year)
WHERE st.student_id = 202210029;

-- 17. 로그인 학생 202210029의 졸업요건 영역별 최소학점, 이수학점과 잔여학점을 알려줘.
WITH applicable_requirement AS (
    SELECT gr.requirement_id
    FROM students AS st
    JOIN graduation_requirements AS gr
      ON gr.department_id = st.department_id
     AND gr.track = st.track
     AND gr.cohort_start <= st.admission_year
     AND (gr.cohort_end IS NULL OR gr.cohort_end >= st.admission_year)
    WHERE st.student_id = 202210029
), earned AS (
    SELECT e.category_id, SUM(o.credits) AS earned_credits
    FROM enrollments AS e
    JOIN course_offerings AS o ON o.offering_id = e.offering_id
    WHERE e.student_id = 202210029
      AND e.status = '완료' AND e.retaken = 0
    GROUP BY e.category_id
)
SELECT cc.category_name, rc.min_credits,
       COALESCE(en.earned_credits, 0) AS earned_credits,
       MAX(rc.min_credits - COALESCE(en.earned_credits, 0), 0) AS remaining_credits
FROM applicable_requirement AS ar
JOIN requirement_categories AS rc ON rc.requirement_id = ar.requirement_id
JOIN course_categories AS cc ON cc.category_id = rc.category_id
LEFT JOIN earned AS en ON en.category_id = rc.category_id
ORDER BY rc.requirement_category_id;

-- 18. 로그인 학생 202210034가 아직 완료하지 않은 지정 필수과목의 과목코드와 과목명을 알려줘.
WITH applicable_requirement AS (
    SELECT gr.requirement_id
    FROM students AS st
    JOIN graduation_requirements AS gr
      ON gr.department_id = st.department_id
     AND gr.track = st.track
     AND gr.cohort_start <= st.admission_year
     AND (gr.cohort_end IS NULL OR gr.cohort_end >= st.admission_year)
    WHERE st.student_id = 202210034
)
SELECT DISTINCT rc.course_code, c.current_name
FROM applicable_requirement AS ar
JOIN requirement_courses AS rc ON rc.requirement_id = ar.requirement_id
JOIN courses AS c ON c.course_code = rc.course_code
WHERE NOT EXISTS (
    SELECT 1 FROM enrollments AS e
    WHERE e.student_id = 202210034
      AND e.course_code = rc.course_code
      AND e.status = '완료' AND e.retaken = 0
)
ORDER BY rc.course_code;

-- 19. 2022학번 일반 신입학생이 배분이수 9학점을 취득했고 영역당 3학점 기준을 채운 영역이 2개라면, 부족 학점, 부족 영역 수와 두 조건 충족 여부를 알려줘.
WITH distribution_rule AS (
    SELECT gc.min_credits, gc.min_areas
    FROM general_education_requirements AS gr
    JOIN general_education_requirement_categories AS gc
      ON gc.general_requirement_id = gr.general_requirement_id
     AND gc.requirement_code = 'DISTRIBUTION'
    WHERE 2022 BETWEEN gr.cohort_start AND COALESCE(gr.cohort_end, 9999)
), earned AS (
    SELECT 9 AS earned_credits, 2 AS completed_areas
)
SELECT MAX(dr.min_credits - e.earned_credits, 0) AS remaining_credits,
       MAX(dr.min_areas - e.completed_areas, 0) AS remaining_areas,
       CASE WHEN e.earned_credits >= dr.min_credits
                  AND e.completed_areas >= dr.min_areas
            THEN 1 ELSE 0 END AS meets_both
FROM distribution_rule AS dr
CROSS JOIN earned AS e;

-- 20. 로그인 학생 202210029가 2025학년도 2학기에 수강한 과목 중 교재가 등록된 과목의 과목코드와 교재 제목을 알려줘.
SELECT DISTINCT o.course_code, t.title
FROM enrollments AS e
JOIN course_offerings AS o ON o.offering_id = e.offering_id
JOIN syllabi AS s ON s.offering_id = o.offering_id
JOIN syllabus_textbooks AS t ON t.syllabus_id = s.syllabus_id
WHERE e.student_id = 202210029
  AND o.year = 2025 AND o.semester = '2'
ORDER BY o.course_code, t.sequence;
