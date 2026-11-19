-- Few-shot sample queries v3
-- v2의 21개 예시를 유지하고 DB v6 전체 테이블 및 오류 보완 예시 16개를 추가한다.
-- 평가셋의 질문과 정답 SQL을 복사하지 않는다.

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

-- 21. 2021학번 소프트웨어융합학과 데이터사이언스트랙의 트랙필수 과목코드와 당시 교육과정표의 과목명을 알려줘.
SELECT rtc.course_code, rtc.source_course_name
FROM graduation_requirements AS gr
JOIN requirement_track_courses AS rtc
  ON rtc.requirement_id = gr.requirement_id
WHERE gr.department_id = 8
  AND gr.cohort_start <= 2021
  AND (gr.cohort_end IS NULL OR gr.cohort_end >= 2021)
  AND gr.track = '데이터사이언스트랙'
  AND rtc.course_type = 'TRACK_REQUIRED'
ORDER BY rtc.course_code;

-- 22. 2025학년도 1학기 CSE203-00 컴퓨터구조의 담당 교수 이름과 화요일 수업 시작·종료 시간, 강의실을 알려줘.
SELECT DISTINCT p.name AS professor_name,
       ts.start_time,
       ts.end_time,
       ct.room_code
FROM course_offerings AS o
JOIN offering_professors AS op ON op.offering_id = o.offering_id
JOIN professors AS p ON p.professor_id = op.professor_id
JOIN class_times AS ct ON ct.offering_id = o.offering_id
JOIN time_slots AS ts ON ts.time_slot_id = ct.time_slot_id
WHERE o.year = 2025 AND o.semester = '1'
  AND o.course_code = 'CSE203' AND o.section = '00'
  AND ts.day = 'tuesday'
ORDER BY ts.start_time, p.name;

-- 23. 2025학년도 2학기 CSE305-02 데이터베이스의 과목 소속 학과와 학과별 개설목록 이수구분을 구분해서 알려줘.
SELECT owner.name AS course_department,
       listing.name AS offering_department,
       cc.category_name
FROM course_offerings AS o
JOIN courses AS c ON c.course_code = o.course_code
JOIN departments AS owner ON owner.department_id = c.department_id
JOIN course_offering_categories AS oc ON oc.offering_id = o.offering_id
JOIN departments AS listing ON listing.department_id = oc.department_id
JOIN course_categories AS cc ON cc.category_id = oc.category_id
WHERE o.year = 2025 AND o.semester = '2'
  AND o.course_code = 'CSE305' AND o.section = '02'
ORDER BY listing.name, cc.category_name;

-- 24. 2025학년도 2학기 소프트웨어융합학과 개설목록의 CSE305 온라인 분반을 과목코드-분반 형식으로 묶어 수강정원과 시간표 상태를 알려줘.
SELECT o.course_code || '-' || o.section AS course_section,
       o.capacity,
       o.schedule_status
FROM course_offerings AS o
JOIN course_offering_categories AS oc ON oc.offering_id = o.offering_id
JOIN departments AS d ON d.department_id = oc.department_id
WHERE o.year = 2025 AND o.semester = '2'
  AND o.course_code = 'CSE305'
  AND d.name = '소프트웨어융합학과'
  AND o.delivery_mode = 'ONLINE';

-- 25. 2025학년도 1학기 CSE203-02 컴퓨터구조의 중간고사, 기말고사, 과제 반영 비율만 알려줘.
SELECT s.midterm_percentage,
       s.final_exam_percentage,
       s.assignment_percentage
FROM course_offerings AS o
JOIN syllabi AS s ON s.offering_id = o.offering_id
WHERE o.year = 2025 AND o.semester = '1'
  AND o.course_code = 'CSE203' AND o.section = '02';

-- 26. 2020학년도 1학기 CSE201-01 이산구조에서 기말시험을 뜻하는 한국어 또는 영어 표현이 있는 주차와 주차 내용을 알려줘.
SELECT w.week, w.topic_content
FROM course_offerings AS o
JOIN syllabi AS s ON s.offering_id = o.offering_id
JOIN syllabus_weekly_plans AS w ON w.syllabus_id = s.syllabus_id
WHERE o.year = 2020 AND o.semester = '1'
  AND o.course_code = 'CSE201' AND o.section = '01'
  AND (
      COALESCE(w.topic_content, '') LIKE '%기말시험%'
      OR COALESCE(w.topic_content, '') LIKE '%기말고사%'
      OR LOWER(COALESCE(w.topic_content, '')) LIKE '%final exam%'
      OR COALESCE(w.note, '') LIKE '%기말시험%'
      OR COALESCE(w.note, '') LIKE '%기말고사%'
      OR LOWER(COALESCE(w.note, '')) LIKE '%final exam%'
  )
ORDER BY w.week;

-- 27. 2024학년도 1학기 SWCON367-01 지능형로봇의 중간발표와 최종발표가 처음 나오는 주차를 한 행으로 알려줘.
SELECT MIN(CASE
               WHEN COALESCE(w.topic_content, '') LIKE '%중간%발표%'
                 OR COALESCE(w.note, '') LIKE '%중간%발표%'
               THEN w.week
           END) AS mid_presentation_week,
       MIN(CASE
               WHEN COALESCE(w.topic_content, '') LIKE '%최종%발표%'
                 OR COALESCE(w.note, '') LIKE '%최종%발표%'
               THEN w.week
           END) AS final_presentation_week
FROM course_offerings AS o
JOIN syllabi AS s ON s.offering_id = o.offering_id
JOIN syllabus_weekly_plans AS w ON w.syllabus_id = s.syllabus_id
WHERE o.year = 2024 AND o.semester = '1'
  AND o.course_code = 'SWCON367' AND o.section = '01';

-- 28. 2020학년도 1학기 EE209-07 논리회로의 교재 제목에 부교재라고 표시된 항목 번호와 제목을 알려줘.
SELECT t.sequence, t.title
FROM course_offerings AS o
JOIN syllabi AS s ON s.offering_id = o.offering_id
JOIN syllabus_textbooks AS t ON t.syllabus_id = s.syllabus_id
WHERE o.year = 2020 AND o.semester = '1'
  AND o.course_code = 'EE209' AND o.section = '07'
  AND COALESCE(t.title, '') LIKE '%부교재%'
ORDER BY t.sequence;

-- 29. CSE203 컴퓨터구조의 선수과목이 논리회로라고 기록된 근거 강의계획서 중 2022학년도 자료의 학기와 분반을 알려줘.
SELECT DISTINCT o.semester, o.section
FROM course_prerequisites AS cp
JOIN prerequisite_sources AS ps ON ps.prerequisite_id = cp.prerequisite_id
JOIN syllabi AS s ON s.syllabus_id = ps.source_syllabus_id
JOIN course_offerings AS o ON o.offering_id = s.offering_id
WHERE cp.course_code = 'CSE203'
  AND cp.prerequisite_name = '논리회로'
  AND o.year = 2022
ORDER BY o.semester, o.section;

-- 30. 학생 202210034의 수강기록을 이수 상태별로 나누고 각 상태의 과목 수와 학점 합계를 알려줘.
SELECT e.status,
       COUNT(*) AS course_count,
       SUM(o.credits) AS total_credits
FROM students AS st
JOIN enrollments AS e ON e.student_id = st.student_id
JOIN course_offerings AS o ON o.offering_id = e.offering_id
WHERE st.student_id = 202210034
GROUP BY e.status
ORDER BY e.status;

-- 31. 2025학번 컴퓨터공학과 공통 졸업요건에서 영역별 최소학점과 산학필수 조건을 각각 알려줘.
SELECT '영역별 최소학점' AS requirement_type,
       cc.category_name AS requirement_name,
       CAST(rc.min_credits AS TEXT) || '학점' AS requirement_value
FROM graduation_requirements AS gr
JOIN departments AS d ON d.department_id = gr.department_id
JOIN requirement_categories AS rc ON rc.requirement_id = gr.requirement_id
JOIN course_categories AS cc ON cc.category_id = rc.category_id
WHERE d.name = '컴퓨터공학과'
  AND gr.track = '공통'
  AND 2025 BETWEEN gr.cohort_start AND COALESCE(gr.cohort_end, 9999)
UNION ALL
SELECT '기타 조건' AS requirement_type,
       ro.type AS requirement_name,
       ro.condition AS requirement_value
FROM graduation_requirements AS gr
JOIN departments AS d ON d.department_id = gr.department_id
JOIN requirement_others AS ro ON ro.requirement_id = gr.requirement_id
WHERE d.name = '컴퓨터공학과'
  AND gr.track = '공통'
  AND 2025 BETWEEN gr.cohort_start AND COALESCE(gr.cohort_end, 9999)
  AND ro.type = '산학필수'
ORDER BY requirement_type, requirement_name;

-- 32. 2023학번 소프트웨어융합학과 공통 졸업요건의 지정 필수과목 코드와 현재 과목명을 알려줘.
SELECT rc.course_code, c.current_name
FROM graduation_requirements AS gr
JOIN departments AS d ON d.department_id = gr.department_id
JOIN requirement_courses AS rc ON rc.requirement_id = gr.requirement_id
JOIN courses AS c ON c.course_code = rc.course_code
WHERE d.name = '소프트웨어융합학과'
  AND gr.track = '공통'
  AND 2023 BETWEEN gr.cohort_start AND COALESCE(gr.cohort_end, 9999)
ORDER BY rc.course_code;

-- 33. 졸업요건 충족 방법 중 대체과목과 마이크로디그리 방식의 대상과 상세 설명을 알려줘.
SELECT COALESCE(f.target_course_code, ro.type) AS target_name,
       f.method,
       CASE
           WHEN f.method = '마이크로디그리'
               THEN json_extract(f.detail_json, '$.options')
           ELSE json_extract(f.detail_json, '$.note')
       END AS detail
FROM requirement_fulfillment_options AS f
LEFT JOIN requirement_others AS ro
  ON ro.requirement_other_id = f.target_other_id
WHERE f.method IN ('대체과목', '마이크로디그리')
ORDER BY f.fulfillment_option_id;

-- 34. 2020학번 소프트웨어융합학과 미래자동차·로봇트랙의 트랙필수 과목코드와 교육과정표 과목명을 알려줘.
SELECT rtc.course_code, rtc.source_course_name
FROM graduation_requirements AS gr
JOIN departments AS d ON d.department_id = gr.department_id
JOIN requirement_track_courses AS rtc ON rtc.requirement_id = gr.requirement_id
WHERE d.name = '소프트웨어융합학과'
  AND gr.track = '미래자동차·로봇트랙'
  AND 2020 BETWEEN gr.cohort_start AND COALESCE(gr.cohort_end, 9999)
  AND rtc.course_type = 'TRACK_REQUIRED'
ORDER BY rtc.course_code;

-- 35. 2025학번 교양교육과정의 영역 코드별 최소학점과 연결된 실제 이수구분 이름을 알려줘.
SELECT gc.requirement_code,
       gc.min_credits,
       cc.category_name
FROM general_education_requirements AS gr
JOIN general_education_requirement_categories AS gc
  ON gc.general_requirement_id = gr.general_requirement_id
JOIN general_education_category_members AS gm
  ON gm.general_requirement_category_id = gc.general_requirement_category_id
JOIN course_categories AS cc ON cc.category_id = gm.category_id
WHERE 2025 BETWEEN gr.cohort_start AND COALESCE(gr.cohort_end, 9999)
ORDER BY gc.requirement_code, cc.category_name;

-- 36. 2025학년도 1학기 CSE406-09 캡스톤디자인에서 Slack으로 면담 일정을 정한다고 적힌 면담 안내만 알려줘.
SELECT s.consultation_time
FROM course_offerings AS o
JOIN syllabi AS s ON s.offering_id = o.offering_id
WHERE o.year = 2025 AND o.semester = '1'
  AND o.course_code = 'CSE406' AND o.section = '09'
  AND LOWER(COALESCE(s.consultation_time, '')) LIKE '%slack%';

-- 37. 2022학년도 2학기 AI1002-00 인공지능프로그래밍의 과목코드-분반, 요일, 시작·종료 시간만 알려줘.
SELECT o.course_code || '-' || o.section AS course_section,
       ts.day,
       ts.start_time,
       ts.end_time
FROM course_offerings AS o
JOIN class_times AS ct ON ct.offering_id = o.offering_id
JOIN time_slots AS ts ON ts.time_slot_id = ct.time_slot_id
WHERE o.year = 2022 AND o.semester = '2'
  AND o.course_code = 'AI1002' AND o.section = '00'
ORDER BY ts.day, ts.start_time;

-- 38. 단과대학별 학과 수와 트랙을 운영하는 학과 수를 알려줘.
SELECT college,
       COUNT(*) AS department_count,
       SUM(CASE WHEN has_track = 1 THEN 1 ELSE 0 END) AS track_department_count
FROM departments
GROUP BY college
ORDER BY college;

-- 39. 인공지능학과 소속 과목은 현재 과목 목록에 몇 개이고, 과목별 학점을 모두 합하면 몇 학점이야?
SELECT COUNT(*) AS course_count,
       SUM(c.credits) AS catalog_credit_sum
FROM courses AS c
JOIN departments AS d ON d.department_id = c.department_id
WHERE d.name = '인공지능학과';

-- 40. 2024학년도 2학기 AI3003-00 자연언어학습 담당 교수의 이름, 이메일과 연구실을 알려줘.
SELECT p.name, p.email, p.office
FROM course_offerings AS o
JOIN offering_professors AS op ON op.offering_id = o.offering_id
JOIN professors AS p ON p.professor_id = op.professor_id
WHERE o.year = 2024
  AND o.semester = '2'
  AND o.course_code = 'AI3003'
  AND o.section = '00';

-- 41. 2024학년도 2학기 AMTH1003-00 고급미분적분학을 공동 담당한 교수 이름을 알려줘.
SELECT p.name
FROM course_offerings AS o
JOIN offering_professors AS op ON op.offering_id = o.offering_id
JOIN professors AS p ON p.professor_id = op.professor_id
WHERE o.year = 2024
  AND o.semester = '2'
  AND o.course_code = 'AMTH1003'
  AND o.section = '00'
ORDER BY p.name;

-- 42. 2024학년도 2학기 AI1002-00 인공지능프로그래밍이 학과별 개설목록에서 어떤 이수구분으로 표시됐는지 학과와 함께 알려줘.
SELECT d.name AS classification_department,
       cc.category_name
FROM course_offerings AS o
JOIN course_offering_categories AS coc ON coc.offering_id = o.offering_id
JOIN departments AS d ON d.department_id = coc.department_id
JOIN course_categories AS cc ON cc.category_id = coc.category_id
WHERE o.year = 2024
  AND o.semester = '2'
  AND o.course_code = 'AI1002'
  AND o.section = '00'
ORDER BY d.name, cc.category_name;

-- 43. 2024학년도 2학기 인공지능학과 개설목록에서 이수구분별 강좌 수와 평균 수강정원을 알려줘.
SELECT cc.category_name,
       COUNT(DISTINCT o.offering_id) AS offering_count,
       ROUND(AVG(o.capacity), 1) AS average_capacity
FROM course_offerings AS o
JOIN course_offering_categories AS coc ON coc.offering_id = o.offering_id
JOIN departments AS d ON d.department_id = coc.department_id
JOIN course_categories AS cc ON cc.category_id = coc.category_id
WHERE o.year = 2024
  AND o.semester = '2'
  AND d.name = '인공지능학과'
GROUP BY cc.category_id, cc.category_name
ORDER BY cc.category_name;

-- 44. 학생들이 선택한 추가 이수과정 중 '없음'을 제외하고 유형과 과정명별 학생 수를 알려줘.
SELECT extra_track_type,
       extra_track_name,
       COUNT(*) AS student_count
FROM students
WHERE extra_track_type IS NOT NULL
  AND extra_track_type <> '없음'
GROUP BY extra_track_type, extra_track_name
ORDER BY extra_track_type, extra_track_name;

-- 45. 학생 202210034의 재수강 관련 기록에서 과목코드, 성적, 이수 상태, 재수강 여부와 대체 여부를 알려줘.
SELECT e.course_code,
       e.grade,
       e.status,
       e.is_retake,
       e.retaken
FROM enrollments AS e
WHERE e.student_id = 202210034
  AND (e.is_retake = 1 OR e.retaken = 1)
ORDER BY e.course_code, e.enrollment_id;

-- 46. 학생 202210029가 완료했고 대체되지 않은 과목을 이수구분별로 나누어 취득학점을 알려줘.
SELECT cc.category_name,
       SUM(o.credits) AS earned_credits
FROM enrollments AS e
JOIN course_offerings AS o ON o.offering_id = e.offering_id
JOIN course_categories AS cc ON cc.category_id = e.category_id
WHERE e.student_id = 202210029
  AND e.status = '완료'
  AND e.retaken = 0
GROUP BY cc.category_id, cc.category_name
ORDER BY cc.category_name;

-- 47. 컴퓨터공학과 공통 졸업요건에서 2022학번과 2025학번의 총 졸업학점을 각각 알려줘.
SELECT target.admission_year,
       gr.total_credits
FROM (SELECT 2022 AS admission_year UNION ALL SELECT 2025) AS target
JOIN departments AS d ON d.name = '컴퓨터공학과'
JOIN graduation_requirements AS gr
  ON gr.department_id = d.department_id
 AND gr.track = '공통'
 AND target.admission_year BETWEEN gr.cohort_start
                               AND COALESCE(gr.cohort_end, 9999)
ORDER BY target.admission_year;

-- 48. 2025학번 컴퓨터공학과 공통 졸업요건에서 전공선택 전체 최소학점과 산학필수 최소학점을 알려줘.
SELECT MAX(CASE WHEN cc.category_code = 'MAJOR_ELECTIVE'
                THEN rc.min_credits END) AS major_elective_credits,
       MAX(CASE WHEN ro.type = '산학필수'
                THEN CAST(REPLACE(ro.condition, '학점 이상', '') AS INTEGER) END)
           AS industry_required_credits
FROM graduation_requirements AS gr
JOIN departments AS d ON d.department_id = gr.department_id
LEFT JOIN requirement_categories AS rc ON rc.requirement_id = gr.requirement_id
LEFT JOIN course_categories AS cc ON cc.category_id = rc.category_id
LEFT JOIN requirement_others AS ro ON ro.requirement_id = gr.requirement_id
WHERE d.name = '컴퓨터공학과'
  AND gr.track = '공통'
  AND 2025 BETWEEN gr.cohort_start AND COALESCE(gr.cohort_end, 9999);

-- 49. 2024학번 인공지능학과 공통 졸업요건에 지정된 필수과목을 이수구분별로 몇 개씩 요구하는지 알려줘.
SELECT cc.category_name,
       COUNT(*) AS required_course_count
FROM graduation_requirements AS gr
JOIN departments AS d ON d.department_id = gr.department_id
JOIN requirement_courses AS rc ON rc.requirement_id = gr.requirement_id
JOIN course_categories AS cc ON cc.category_id = rc.category_id
WHERE d.name = '인공지능학과'
  AND gr.track = '공통'
  AND 2024 BETWEEN gr.cohort_start AND COALESCE(gr.cohort_end, 9999)
GROUP BY cc.category_id, cc.category_name
ORDER BY cc.category_name;

-- 50. AMTH1009 과목을 대신 인정받을 수 있는 방법과 그 상세 안내를 알려줘.
SELECT method,
       json_extract(detail_json, '$.note') AS detail
FROM requirement_fulfillment_options
WHERE target_type = 'COURSE'
  AND target_course_code = 'AMTH1009'
  AND method = '대체과목';

-- 51. 소프트웨어융합학과 데이터사이언스트랙에서 2020학번과 2021학번의 트랙필수 과목명 표기가 어떻게 달라졌는지 알려줘.
SELECT gr.cohort_start AS admission_year,
       rtc.course_code,
       rtc.source_course_name
FROM graduation_requirements AS gr
JOIN departments AS d ON d.department_id = gr.department_id
JOIN requirement_track_courses AS rtc ON rtc.requirement_id = gr.requirement_id
WHERE d.name = '소프트웨어융합학과'
  AND gr.track = '데이터사이언스트랙'
  AND gr.cohort_start IN (2020, 2021)
  AND rtc.course_type = 'TRACK_REQUIRED'
ORDER BY gr.cohort_start, rtc.course_code;

-- 52. 교양교육과정 버전별 적용 학번 범위와 총 교양 최소학점, 근거 문서를 알려줘.
SELECT cohort_start,
       cohort_end,
       total_general_credits,
       source_document
FROM general_education_requirements
ORDER BY cohort_start;

-- 53. 2025학번 교양교육과정에서 배분이수 영역에 포함되는 실제 이수구분 이름을 알려줘.
SELECT cc.category_name
FROM general_education_requirements AS gr
JOIN general_education_requirement_categories AS grc
  ON grc.general_requirement_id = gr.general_requirement_id
JOIN general_education_category_members AS gcm
  ON gcm.general_requirement_category_id = grc.general_requirement_category_id
JOIN course_categories AS cc ON cc.category_id = gcm.category_id
WHERE 2025 BETWEEN gr.cohort_start AND COALESCE(gr.cohort_end, 9999)
  AND grc.requirement_code = 'DISTRIBUTION'
ORDER BY cc.category_name;

-- 54. 2024학번에게 적용되는 CSE304 알고리즘의 필수 선수과목을 그룹별로 나누어 과목명과 최소 이수 과목 수를 알려줘.
SELECT cp.prerequisite_group,
       cp.prerequisite_name,
       cp.minimum_required_count
FROM course_prerequisites AS cp
WHERE cp.course_code = 'CSE304'
  AND cp.prerequisite_type = 'REQUIRED'
  AND 2024 BETWEEN COALESCE(cp.cohort_start, 0)
               AND COALESCE(cp.cohort_end, 9999)
ORDER BY cp.prerequisite_group, cp.prerequisite_name;

-- 55. CSE304 알고리즘의 선수과목 근거로 연결된 2023학년도 강의계획서의 학기와 분반을 알려줘.
SELECT DISTINCT o.semester,
       o.section
FROM course_prerequisites AS cp
JOIN prerequisite_sources AS ps ON ps.prerequisite_id = cp.prerequisite_id
JOIN syllabi AS s ON s.syllabus_id = ps.source_syllabus_id
JOIN course_offerings AS o ON o.offering_id = s.offering_id
WHERE cp.course_code = 'CSE304'
  AND o.year = 2023
ORDER BY o.semester, o.section;

-- 56. 2024학년도 2학기 AI1002-00 인공지능프로그래밍의 수업 운영방식과 수업방법 중 팀별발표 및 e-campus 활용 여부를 알려줘.
SELECT s.operation_modes,
       CASE WHEN EXISTS (
                SELECT 1 FROM json_each(s.teaching_methods_json)
                WHERE value = '팀별발표'
            ) THEN 1 ELSE 0 END AS uses_team_presentation,
       CASE WHEN EXISTS (
                SELECT 1 FROM json_each(s.teaching_methods_json)
                WHERE value = 'e-campus활용'
            ) THEN 1 ELSE 0 END AS uses_ecampus
FROM syllabi AS s
JOIN course_offerings AS o ON o.offering_id = s.offering_id
WHERE o.year = 2024
  AND o.semester = '2'
  AND o.course_code = 'AI1002'
  AND o.section = '00';

-- 57. 2024학년도 2학기 AI3008-00 설명및신뢰가능한AI의 모든 평가항목 반영 비율 합계는 몇 퍼센트야?
SELECT COALESCE(s.midterm_percentage, 0)
     + COALESCE(s.final_exam_percentage, 0)
     + COALESCE(s.assignment_percentage, 0)
     + COALESCE(s.presentation_percentage, 0)
     + COALESCE(s.attendance_percentage, 0)
     + COALESCE(s.other_percentage, 0) AS total_percentage
FROM syllabi AS s
JOIN course_offerings AS o ON o.offering_id = s.offering_id
WHERE o.year = 2024
  AND o.semester = '2'
  AND o.course_code = 'AI3008'
  AND o.section = '00';

-- 58. 2024학년도 2학기 AI3003-00 자연언어학습의 교재 1번 저자와 출판사를 알려줘.
SELECT t.author, t.publisher
FROM syllabus_textbooks AS t
JOIN syllabi AS s ON s.syllabus_id = t.syllabus_id
JOIN course_offerings AS o ON o.offering_id = s.offering_id
WHERE o.year = 2024
  AND o.semester = '2'
  AND o.course_code = 'AI3003'
  AND o.section = '00'
  AND t.sequence = 1;

-- 59. 2023학년도와 2024학년도 2학기 AI1002-00 인공지능프로그래밍에서 중간시험이 표시된 주차를 연도별로 알려줘.
SELECT o.year, w.week
FROM syllabus_weekly_plans AS w
JOIN syllabi AS s ON s.syllabus_id = w.syllabus_id
JOIN course_offerings AS o ON o.offering_id = s.offering_id
WHERE o.year IN (2023, 2024)
  AND o.semester = '2'
  AND o.course_code = 'AI1002'
  AND o.section = '00'
  AND (LOWER(w.topic_content) LIKE '%midterm%'
       OR w.topic_content LIKE '%중간%')
ORDER BY o.year, w.week;

-- 60. 2024학년도 1학기 AI1001-00 인공지능개론의 요일별 정규 수업시간을 분 단위로 합산해 알려줘.
SELECT ts.day,
       SUM((CAST(substr(ts.end_time, 1, 2) AS INTEGER) * 60
            + CAST(substr(ts.end_time, 4, 2) AS INTEGER))
           - (CAST(substr(ts.start_time, 1, 2) AS INTEGER) * 60
              + CAST(substr(ts.start_time, 4, 2) AS INTEGER))) AS total_minutes
FROM course_offerings AS o
JOIN class_times AS ct ON ct.offering_id = o.offering_id
JOIN time_slots AS ts ON ts.time_slot_id = ct.time_slot_id
WHERE o.year = 2024
  AND o.semester = '1'
  AND o.course_code = 'AI1001'
  AND o.section = '00'
GROUP BY ts.day
ORDER BY CASE ts.day
             WHEN '월' THEN 1 WHEN '화' THEN 2 WHEN '수' THEN 3
             WHEN '목' THEN 4 WHEN '금' THEN 5 ELSE 6
         END;
