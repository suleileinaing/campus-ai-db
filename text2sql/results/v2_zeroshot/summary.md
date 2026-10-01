# Text2SQL 평가 결과 (2026-10-02 01:03)

| 지표 | 값 |
|---|---|
| 평가 문항 수 | 16 |
| 실행 성공률(최종) | 16/16 (100.0%) |
| 실행 성공률(1차 시도) | 16/16 (100.0%) |
| 정답률 strict | 5/16 (31.2%) |
| 정답률 relaxed | 6/16 (37.5%) |
| 평균 토큰 | 3444.8 |
| 평균 응답시간(초) | 4.42 |

## 유형별

| 태그 | n | strict | relaxed | 실행 성공 |
|---|---|---|---|---|
| (태그 없음) | 16 | 5/16 (31.2%) | 6/16 (37.5%) | 16/16 (100.0%) |

## 진단 분포

| 진단 | 개수 |
|---|---|
| value_mismatch | 9 |
| correct | 5 |
| row_count_mismatch | 1 |
| order_mismatch | 1 |

## 오답 목록

### q004 — value_mismatch
질문: 내 학과·입학년도·트랙의 전공필수 최소학점과 DB 완료·미대체 수강기록 합계를 비교한 잔여학점 계산값은 얼마야?

gold:
```sql
WITH target AS (SELECT * FROM students WHERE student_id = 202210029)
,
applicable AS (
    SELECT gr.*
    FROM target AS st
    JOIN graduation_requirements AS gr
      ON gr.department_id = st.department_id
     AND gr.track = st.track
     AND gr.cohort_start <= st.admission_year
     AND (gr.cohort_end IS NULL OR gr.cohort_end >= st.admission_year)
)
,
earned AS (
    SELECT e.course_code, e.category_id, o.credits
    FROM enrollments AS e
    JOIN target AS st ON st.student_id = e.student_id
    JOIN course_offerings AS o
      ON o.offering_id = e.offering_id AND o.course_code = e.course_code
    WHERE e.status = '완료' AND e.retaken = 0
)

SELECT ar.requirement_id, rc.min_credits AS required_credits,
       COALESCE(SUM(e.credits), 0) AS earned_credits,
       MAX(rc.min_credits - COALESCE(SUM(e.credits), 0), 0) AS remaining_credits
FROM applicable AS ar
JOIN requirement_categories AS rc ON rc.requirement_id = ar.requirement_id
JOIN course_categories AS cc ON cc.category_id = rc.category_id
LEFT JOIN earned AS e ON e.category_id = rc.category_id
WHERE cc.category_code = '04'
GROUP BY ar.requirement_id, rc.requirement_category_id, rc.min_credits
ORDER BY ar.requirement_id;
```
pred:
```sql
WITH earned AS (
    SELECT COALESCE(SUM(co.credits), 0) AS earned_credits
    FROM enrollments AS e
    JOIN course_offerings AS co ON co.offering_id = e.offering_id
    JOIN course_categories AS cc ON cc.category_id = e.category_id
    WHERE e.student_id = 202210029
      AND e.status = '완료'
      AND e.retaken = 0
      AND cc.category_name = '전공필수'
)
SELECT
    rc.min_credits AS 전공필수_최소학점,
    earned.earned_credits AS 전공필수_취득학점,
    MAX(0, rc.min_credits - earned.earned_credits) AS 잔여학점
FROM students AS s
JOIN graduation_requirements AS gr
  ON gr.department_id = s.department_id
 AND gr.track = s.track
 AND gr.cohort_start <= s.admission_year
 AND (gr.cohort_end IS NULL OR gr.cohort_end >= s.admission_year)
JOIN requirement_categories AS rc ON rc.requirement_id = gr.requirement_id
JOIN course_categories AS cc ON cc.category_id = rc.category_id
CROSS JOIN earned
WHERE s.student_id = 202210029
  AND cc.category_name = '전공필수';
```

### q006 — value_mismatch
질문: 2025학년도 2학기에 내가 수강한 과목과 수강 상태를 알려줘.

gold:
```sql
WITH target AS (SELECT * FROM students WHERE student_id = 202210029)
SELECT o.course_code, o.course_name, o.section, e.status, e.grade
FROM enrollments AS e JOIN target AS st ON st.student_id = e.student_id
JOIN course_offerings AS o
  ON o.offering_id = e.offering_id AND o.course_code = e.course_code
WHERE o.year = 2025 AND o.semester = '2'
ORDER BY o.course_code, o.section, e.enrollment_id;
```
pred:
```sql
SELECT co.course_code, co.course_name, e.status
FROM enrollments AS e
JOIN course_offerings AS co ON co.offering_id = e.offering_id
WHERE e.student_id = 202210029
  AND co.year = 2025
  AND co.semester = '2';
```

### q007 — value_mismatch
질문: 2025학년도 2학기 내 수강과목의 DB 등록 교재와 강의계획서 등록 여부를 알려줘.

gold:
```sql
WITH target AS (SELECT * FROM students WHERE student_id = 202210029)
SELECT o.course_code, o.course_name, o.section,
       CASE WHEN sy.syllabus_id IS NULL THEN '강의계획서 미등록'
            WHEN t.textbook_id IS NULL THEN '교재 행 미등록'
            ELSE '교재 등록' END AS data_status,
       t.sequence, t.title, t.author, t.publisher, t.isbn
FROM enrollments AS e JOIN target AS st ON st.student_id = e.student_id
JOIN course_offerings AS o ON o.offering_id = e.offering_id
LEFT JOIN syllabi AS sy ON sy.offering_id = o.offering_id
LEFT JOIN syllabus_textbooks AS t ON t.syllabus_id = sy.syllabus_id
WHERE o.year = 2025 AND o.semester = '2'
ORDER BY o.course_code, o.section, t.sequence, t.textbook_id;
```
pred:
```sql
SELECT
    co.course_code,
    co.course_name,
    co.section,
    CASE
        WHEN sy.syllabus_id IS NOT NULL THEN '등록'
        ELSE '미등록'
    END AS 강의계획서_등록여부,
    st.title AS 교재명,
    st.author AS 저자,
    st.publisher AS 출판사,
    st.publication_year AS 출판연도,
    st.isbn AS ISBN
FROM enrollments AS e
JOIN course_offerings AS co
    ON co.offering_id = e.offering_id
LEFT JOIN syllabi AS sy
    ON sy.offering_id = co.offering_id
LEFT JOIN syllabus_textbooks AS st
    ON st.syllabus_id = sy.syllabus_id
WHERE e.student_id = 202210029
  AND co.year = 2025
  AND co.semester = '2'
ORDER BY co.course_code, co.section, st.sequence;
```

### q008 — row_count_mismatch
질문: DB에 저장된 내 전체 수강이력의 담당 교수와 등록된 연구실 정보를 알려줘.

gold:
```sql
WITH target AS (SELECT * FROM students WHERE student_id = 202210029)
SELECT DISTINCT p.professor_id, p.name AS professor_name,
       p.office AS registered_office
FROM enrollments AS e JOIN target AS st ON st.student_id = e.student_id
JOIN offering_professors AS op ON op.offering_id = e.offering_id
JOIN professors AS p ON p.professor_id = op.professor_id
ORDER BY p.professor_id;
```
pred:
```sql
SELECT
    co.year,
    co.semester,
    co.course_code,
    co.course_name,
    co.section,
    p.name AS professor_name,
    p.office
FROM enrollments AS e
JOIN course_offerings AS co
    ON co.offering_id = e.offering_id
LEFT JOIN offering_professors AS op
    ON op.offering_id = co.offering_id
LEFT JOIN professors AS p
    ON p.professor_id = op.professor_id
WHERE e.student_id = 202210029
ORDER BY
    co.year,
    CASE co.semester
        WHEN '1' THEN 1
        WHEN 'summer' THEN 2
        WHEN '2' THEN 3
        WHEN 'winter' THEN 4
    END,
    co.course_code,
    co.section,
    p.name;
```

### q009 — order_mismatch
질문: 내 DB의 완료·미대체 수강기록을 성적별로 몇 건씩 보유하고 있는지 알려줘.

gold:
```sql
WITH target AS (SELECT * FROM students WHERE student_id = 202210029)
SELECT e.grade, COUNT(*) AS course_count
FROM enrollments AS e JOIN target AS st ON st.student_id = e.student_id
WHERE e.status = '완료' AND e.retaken = 0
GROUP BY e.grade ORDER BY course_count DESC, e.grade;
```
pred:
```sql
SELECT grade, COUNT(*) AS record_count
FROM enrollments
WHERE student_id = 202210029
  AND status = '완료'
  AND retaken = 0
GROUP BY grade;
```

### q010 — value_mismatch
질문: 내가 재수강한 과목과 해당 재수강 성적을 알려줘.

gold:
```sql
WITH target AS (SELECT * FROM students WHERE student_id = 202210029)
SELECT e.course_code, o.course_name, o.year, o.semester, e.grade, e.status
FROM enrollments AS e JOIN target AS st ON st.student_id = e.student_id
JOIN course_offerings AS o ON o.offering_id = e.offering_id
WHERE e.is_retake = 1
ORDER BY e.course_code, o.year, o.semester, e.enrollment_id;
```
pred:
```sql
SELECT co.course_name, e.grade
FROM enrollments AS e
JOIN course_offerings AS co ON co.offering_id = e.offering_id
WHERE e.student_id = 202210029
  AND e.is_retake = 1;
```

### q012 — value_mismatch
질문: 내 학과·입학년도·트랙에 적용되는 졸업 총 이수학점은 몇 학점이야?

gold:
```sql
WITH target AS (SELECT * FROM students WHERE student_id = 202210029)
,
applicable AS (
    SELECT gr.*
    FROM target AS st
    JOIN graduation_requirements AS gr
      ON gr.department_id = st.department_id
     AND gr.track = st.track
     AND gr.cohort_start <= st.admission_year
     AND (gr.cohort_end IS NULL OR gr.cohort_end >= st.admission_year)
)

SELECT ar.requirement_id, d.name AS department_name, ar.track,
       ar.cohort_start, ar.cohort_end, ar.total_credits
FROM applicable AS ar JOIN departments AS d ON d.department_id = ar.department_id
ORDER BY ar.requirement_id;
```
pred:
```sql
SELECT gr.total_credits
FROM students AS s
JOIN graduation_requirements AS gr
  ON gr.department_id = s.department_id
 AND gr.track = s.track
 AND gr.cohort_start <= s.admission_year
 AND (gr.cohort_end IS NULL OR gr.cohort_end >= s.admission_year)
WHERE s.student_id = 202210029;
```

### q013 — value_mismatch
질문: DB에 등록된 내 학적 상태는 뭐야?

gold:
```sql
WITH target AS (SELECT * FROM students WHERE student_id = 202210029)
SELECT student_id, status FROM target;
```
pred:
```sql
SELECT status
FROM students
WHERE student_id = 202210029;
```

### q014 — value_mismatch
질문: DB에 등록된 내 추가전공 유형과 이름을 알려줘.

gold:
```sql
WITH target AS (SELECT * FROM students WHERE student_id = 202210029)
SELECT student_id, extra_track_type, extra_track_name FROM target;
```
pred:
```sql
SELECT extra_track_type, extra_track_name
FROM students
WHERE student_id = 202210029;
```

### q015 — value_mismatch
질문: DB에 등록된 내 소속 학과 이름과 코드는 뭐야?

gold:
```sql
WITH target AS (SELECT * FROM students WHERE student_id = 202210029)
SELECT st.student_id, d.department_id, d.code AS department_code,
       d.name AS department_name
FROM target AS st JOIN departments AS d ON d.department_id = st.department_id;
```
pred:
```sql
SELECT d.name, d.code
FROM students AS s
JOIN departments AS d ON d.department_id = s.department_id
WHERE s.student_id = 202210029;
```

### q016 — value_mismatch
질문: 내 입학년도 기준으로 SWCON201에 등록된 선수과목과 각 선수과목의 유효 이수기록을 보여줘.

gold:
```sql
WITH target AS (SELECT * FROM students WHERE student_id = 202210029)
SELECT cp.prerequisite_id, cp.prerequisite_course_code,
       cp.prerequisite_name, cp.prerequisite_type, cp.prerequisite_group,
       cp.minimum_required_count, cp.minimum_grade_code, cp.abeek_applicable,
       e.grade AS recorded_passing_grade,
       CASE WHEN e.enrollment_id IS NULL THEN '유효 이수기록 없음'
            ELSE '유효 이수기록 있음' END AS completion_record
FROM target AS st JOIN course_prerequisites AS cp
  ON cp.course_code = 'SWCON201'
 AND (cp.cohort_start IS NULL OR cp.cohort_start <= st.admission_year)
 AND (cp.cohort_end IS NULL OR cp.cohort_end >= st.admission_year)
LEFT JOIN enrollments AS e
  ON e.student_id = st.student_id
 AND e.course_code = cp.prerequisite_course_code
 AND e.status = '완료' AND e.retaken = 0
ORDER BY cp.prerequisite_id, e.enrollment_id;
```
pred:
```sql
WITH current_student AS (
    SELECT admission_year
    FROM students
    WHERE student_id = 202210029
),
valid_enrollments AS (
    SELECT e.course_code, co.year, co.semester, e.grade, co.credits
    FROM enrollments AS e
    JOIN course_offerings AS co ON co.offering_id = e.offering_id
    WHERE e.student_id = 202210029
      AND e.status = '완료'
      AND e.retaken = 0
)
SELECT
    cp.prerequisite_course_code,
    cp.prerequisite_name,
    cp.prerequisite_type,
    ve.year,
    ve.semester,
    ve.grade,
    ve.credits
FROM course_prerequisites AS cp
CROSS JOIN current_student AS s
LEFT JOIN valid_enrollments AS ve
    ON ve.course_code = cp.prerequisite_course_code
WHERE cp.course_code = 'SWCON201'
  AND (cp.cohort_start IS NULL OR cp.cohort_start <= s.admission_year)
  AND (cp.cohort_end IS NULL OR cp.cohort_end >= s.admission_year)
ORDER BY cp.prerequisite_id, ve.year, ve.semester;
```


## 진단 코드 설명

- correct: 결과 완전 일치 / correct_extra_columns: 컬럼이 더 있거나 컬럼 순서가 다름(relaxed 정답)
- order_mismatch: 행 정렬만 다름(relaxed 정답) / row_count_mismatch: 행 수가 다름 / value_mismatch: 행 수는 같지만 값이 다름
- exec_fail:sqlite 실행 오류 / exec_fail:guard 안전장치에 의해 거부 / exec_fail:no_sql SQL 추출 실패
- exec_fail:timeout 시간 초과 / exec_fail:refused 거부하면 안 되는 질문을 거부
- correct_refusal: 거부가 정답인 문항을 거부·차단 / no_leak_but_not_refused: 거부는 안 했지만 결과 0행
- should_have_refused: 거부해야 하는데 결과를 돌려줌 / api_error ChatKHU 호출 실패 / gold_invalid 정답 SQL 문제
