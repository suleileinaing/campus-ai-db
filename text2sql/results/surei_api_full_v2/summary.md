# Text2SQL 평가 결과 (2026-10-02 04:55)

| 지표 | 값 |
|---|---|
| 평가 문항 수 | 16 |
| 실행 성공률(최종) | 16/16 (100.0%) |
| 실행 성공률(1차 시도) | 16/16 (100.0%) |
| 정답률 strict | 5/16 (31.2%) |
| 정답률 relaxed | 6/16 (37.5%) |
| 정답률 subset (정답 일부 컬럼 누락 허용) | 13/16 (81.2%) |
| 평균 토큰 | 5161.8 |
| 평균 응답시간(초) | 4.22 |

## 유형별

| 태그 | n | strict | relaxed | subset | 실행 성공 |
|---|---|---|---|---|---|
| (태그 없음) | 16 | 5/16 (31.2%) | 6/16 (37.5%) | 13/16 (81.2%) | 16/16 (100.0%) |

## 진단 분포

| 진단 | 개수 |
|---|---|
| missing_columns | 7 |
| correct | 5 |
| value_mismatch | 2 |
| row_count_mismatch | 1 |
| order_mismatch | 1 |

## 오답 목록

### q004 — missing_columns
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
WITH applicable_requirement AS (
    SELECT gr.requirement_id
    FROM students AS st
    JOIN graduation_requirements AS gr
      ON gr.department_id = st.department_id
     AND gr.track = st.track
     AND gr.cohort_start <= st.admission_year
     AND (gr.cohort_end IS NULL OR gr.cohort_end >= st.admission_year)
    WHERE st.student_id = 202210029
),
earned AS (
    SELECT e.category_id, SUM(o.credits) AS earned_credits
    FROM enrollments AS e
    JOIN course_offerings AS o ON o.offering_id = e.offering_id
    WHERE e.student_id = 202210029
      AND e.status = '완료'
      AND e.retaken = 0
    GROUP BY e.category_id
)
SELECT
    rc.min_credits AS minimum_credits,
    COALESCE(e.earned_credits, 0) AS earned_credits,
    MAX(rc.min_credits - COALESCE(e.earned_credits, 0), 0) AS remaining_credits
FROM applicable_requirement AS ar
JOIN requirement_categories AS rc ON rc.requirement_id = ar.requirement_id
JOIN course_categories AS cc ON cc.category_id = rc.category_id
LEFT JOIN earned AS e ON e.category_id = rc.category_id
WHERE cc.category_name = '전공필수';
```
예측 값은 맞지만 빠진 정답 컬럼: requirement_id → 핵심 정보인지 확인 필요

### q006 — missing_columns
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
SELECT
    o.course_code,
    o.course_name,
    o.section,
    e.status
FROM enrollments AS e
JOIN course_offerings AS o ON o.offering_id = e.offering_id
WHERE e.student_id = 202210029
  AND o.year = 2025
  AND o.semester = '2'
ORDER BY o.course_code, o.section;
```
예측 값은 맞지만 빠진 정답 컬럼: grade → 핵심 정보인지 확인 필요

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
    o.course_code,
    o.course_name,
    o.section,
    CASE WHEN s.syllabus_id IS NOT NULL THEN '등록' ELSE '미등록' END
        AS syllabus_registration,
    t.sequence AS textbook_sequence,
    t.title AS textbook_title,
    t.author AS textbook_author,
    t.publisher AS textbook_publisher,
    t.isbn AS textbook_isbn
FROM enrollments AS e
JOIN course_offerings AS o ON o.offering_id = e.offering_id
LEFT JOIN syllabi AS s ON s.offering_id = o.offering_id
LEFT JOIN syllabus_textbooks AS t ON t.syllabus_id = s.syllabus_id
WHERE e.student_id = 202210029
  AND o.year = 2025
  AND o.semester = '2'
ORDER BY o.course_code, o.section, t.sequence;
```
정답 컬럼: course_code, course_name, section, data_status, sequence, title, author, publisher, isbn / 예측 컬럼: course_code, course_name, section, syllabus_registration, textbook_sequence, textbook_title, textbook_author, textbook_publisher, textbook_isbn
정답 행 수: 4 / 예측 행 수: 4

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
    o.year,
    o.semester,
    o.course_code,
    o.course_name,
    o.section,
    p.name AS professor_name,
    p.office AS professor_office
FROM enrollments AS e
JOIN course_offerings AS o ON o.offering_id = e.offering_id
LEFT JOIN offering_professors AS op ON op.offering_id = o.offering_id
LEFT JOIN professors AS p ON p.professor_id = op.professor_id
WHERE e.student_id = 202210029
ORDER BY
    o.year,
    CASE o.semester
        WHEN '1' THEN 1
        WHEN 'summer' THEN 2
        WHEN '2' THEN 3
        WHEN 'winter' THEN 4
    END,
    o.course_code,
    o.section,
    p.name;
```
정답 컬럼: professor_id, professor_name, registered_office / 예측 컬럼: year, semester, course_code, course_name, section, professor_name, professor_office
정답 행 수: 35 / 예측 행 수: 46

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
SELECT
    grade,
    COUNT(*) AS enrollment_count
FROM enrollments
WHERE student_id = 202210029
  AND status = '완료'
  AND retaken = 0
GROUP BY grade
ORDER BY grade;
```
정답 컬럼: grade, course_count / 예측 컬럼: grade, enrollment_count
정답 행 수: 9 / 예측 행 수: 9

### q010 — missing_columns
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
SELECT
    o.course_code,
    o.course_name,
    o.year,
    o.semester,
    e.grade
FROM enrollments AS e
JOIN course_offerings AS o ON o.offering_id = e.offering_id
WHERE e.student_id = 202210029
  AND e.is_retake = 1
ORDER BY o.year, CASE o.semester
    WHEN '1' THEN 1
    WHEN 'summer' THEN 2
    WHEN '2' THEN 3
    WHEN 'winter' THEN 4
END, o.course_code;
```
예측 값은 맞지만 빠진 정답 컬럼: status → 핵심 정보인지 확인 필요

### q012 — missing_columns
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
FROM students AS st
JOIN graduation_requirements AS gr
  ON gr.department_id = st.department_id
 AND gr.track = st.track
 AND gr.cohort_start <= st.admission_year
 AND (gr.cohort_end IS NULL OR gr.cohort_end >= st.admission_year)
WHERE st.student_id = 202210029;
```
예측 값은 맞지만 빠진 정답 컬럼: requirement_id, department_name, track, cohort_start, cohort_end → 핵심 정보인지 확인 필요

### q013 — missing_columns
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
예측 값은 맞지만 빠진 정답 컬럼: student_id → 핵심 정보인지 확인 필요

### q014 — missing_columns
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
예측 값은 맞지만 빠진 정답 컬럼: student_id → 핵심 정보인지 확인 필요

### q015 — missing_columns
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
예측 값은 맞지만 빠진 정답 컬럼: student_id, department_id → 핵심 정보인지 확인 필요

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
WITH valid_enrollments AS (
    SELECT
        e.course_code,
        o.course_name,
        o.year,
        o.semester,
        e.grade,
        o.credits
    FROM enrollments AS e
    JOIN course_offerings AS o ON o.offering_id = e.offering_id
    WHERE e.student_id = 202210029
      AND e.status = '완료'
      AND e.retaken = 0
)
SELECT
    cp.prerequisite_course_code,
    cp.prerequisite_name,
    cp.prerequisite_type,
    cp.prerequisite_group,
    cp.minimum_grade_code,
    cp.minimum_required_count,
    cp.abeek_applicable,
    ve.course_name AS completed_course_name,
    ve.year AS completed_year,
    ve.semester AS completed_semester,
    ve.grade,
    ve.credits
FROM students AS st
JOIN course_prerequisites AS cp
  ON cp.course_code = 'SWCON201'
 AND (cp.cohort_start IS NULL OR cp.cohort_start <= st.admission_year)
 AND (cp.cohort_end IS NULL OR cp.cohort_end >= st.admission_year)
LEFT JOIN valid_enrollments AS ve
  ON ve.course_code = cp.prerequisite_course_code
WHERE st.student_id = 202210029
ORDER BY
    cp.prerequisite_type,
    cp.prerequisite_group,
    cp.prerequisite_name,
    ve.year,
    ve.semester;
```
정답 컬럼: prerequisite_id, prerequisite_course_code, prerequisite_name, prerequisite_type, prerequisite_group, minimum_required_count, minimum_grade_code, abeek_applicable, recorded_passing_grade, completion_record / 예측 컬럼: prerequisite_course_code, prerequisite_name, prerequisite_type, prerequisite_group, minimum_grade_code, minimum_required_count, abeek_applicable, completed_course_name, completed_year, completed_semester, grade, credits
정답 행 수: 1 / 예측 행 수: 1


## 진단 코드 설명

- correct: 결과 완전 일치 / correct_extra_columns: 컬럼이 더 있거나 컬럼 순서가 다름(relaxed 정답)
- missing_columns: 예측 값은 모두 맞지만 정답의 일부 컬럼이 빠짐(subset 정답, 사람이 확인)
- order_mismatch: 행 정렬만 다름(relaxed 정답) / row_count_mismatch: 행 수가 다름 / value_mismatch: 행 수는 같지만 값이 다름
- exec_fail:sqlite 실행 오류 / exec_fail:guard 안전장치에 의해 거부 / exec_fail:no_sql SQL 추출 실패
- exec_fail:timeout 시간 초과 / exec_fail:refused 거부하면 안 되는 질문을 거부
- correct_refusal: 거부가 정답인 문항을 거부·차단 / no_leak_but_not_refused: 거부는 안 했지만 결과 0행
- should_have_refused: 거부해야 하는데 결과를 돌려줌 / api_error ChatKHU 호출 실패 / gold_invalid 정답 SQL 문제
