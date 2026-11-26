# SQL 논리 LLM 채점 (2026-11-20 14:21)

judge 모델: `gpt-5.6-luna` / judge 토큰 합계: 165315

통과 기준: 정답 SQL 과 논리가 같음 + 질문에 없는 조건 없음 + 본인 학번 범위 지킴

| 지표 | 값 |
|---|---|
| SQL 논리 통과율 | 64/100 (64.0%) |
| 논리 일치 | 64/100 (64.0%) |
| (참고) 실행 결과 정답률 strict | 91/100 (91.0%) |
| 결과는 맞았지만 논리가 틀림(우연히 맞음) | 28 |
| 질문에 없는 조건 추가 | 0 |
| 본인 학번 범위 위반 | 0 |

## 유형별

| 태그 | n | 통과 | 논리 일치 | 실행 strict | 우연히 맞음 |
|---|---|---|---|---|---|
| arithmetic_reasoning | 4 | 0/4 (0.0%) | 0/4 (0.0%) | 0/4 (0.0%) | 0 |
| assignment_gap | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 0 |
| assignment_min | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 0 |
| assignment_ranking | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 0 |
| attendance_gap | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 0 |
| classification_aggregation | 4 | 0/4 (0.0%) | 0/4 (0.0%) | 4/4 (100.0%) | 4 |
| combined_exam_gap | 4 | 0/4 (0.0%) | 0/4 (0.0%) | 4/4 (100.0%) | 4 |
| common_instructor | 4 | 0/4 (0.0%) | 0/4 (0.0%) | 4/4 (100.0%) | 4 |
| cross_rule_reasoning | 1 | 0/1 (0.0%) | 0/1 (0.0%) | 0/1 (0.0%) | 0 |
| department_required_load | 4 | 0/4 (0.0%) | 0/4 (0.0%) | 4/4 (100.0%) | 4 |
| distribution_rule_application | 3 | 0/3 (0.0%) | 0/3 (0.0%) | 0/3 (0.0%) | 0 |
| english_industry | 4 | 0/4 (0.0%) | 0/4 (0.0%) | 4/4 (100.0%) | 4 |
| exam_change | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 0 |
| exam_threshold_set | 4 | 0/4 (0.0%) | 0/4 (0.0%) | 4/4 (100.0%) | 4 |
| fixture_earned | 2 | 2/2 (100.0%) | 2/2 (100.0%) | 2/2 (100.0%) | 0 |
| fixture_personalized | 6 | 6/6 (100.0%) | 6/6 (100.0%) | 6/6 (100.0%) | 0 |
| fixture_retake | 2 | 2/2 (100.0%) | 2/2 (100.0%) | 2/2 (100.0%) | 0 |
| fixture_status | 2 | 2/2 (100.0%) | 2/2 (100.0%) | 2/2 (100.0%) | 0 |
| general_cohort_difference | 1 | 0/1 (0.0%) | 0/1 (0.0%) | 0/1 (0.0%) | 0 |
| general_cohort_rule | 2 | 1/2 (50.0%) | 1/2 (50.0%) | 2/2 (100.0%) | 1 |
| midterm_max | 4 | 3/4 (75.0%) | 3/4 (75.0%) | 4/4 (100.0%) | 1 |
| multi_document_multi_hop | 8 | 4/8 (50.0%) | 4/8 (50.0%) | 8/8 (100.0%) | 4 |
| multi_document_multi_hop_reasoning | 8 | 7/8 (87.5%) | 7/8 (87.5%) | 7/8 (87.5%) | 1 |
| multi_document_reasoning | 32 | 23/32 (71.9%) | 23/32 (71.9%) | 32/32 (100.0%) | 9 |
| multi_hop | 16 | 16/16 (100.0%) | 16/16 (100.0%) | 16/16 (100.0%) | 0 |
| multi_hop_aggregation | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 0 |
| official_public_facts | 87 | 58/87 (66.7%) | 58/87 (66.7%) | 85/87 (97.7%) | 28 |
| official_rule | 2 | 1/2 (50.0%) | 1/2 (50.0%) | 2/2 (100.0%) | 1 |
| official_rule_with_hypothetical_inputs | 7 | 0/7 (0.0%) | 0/7 (0.0%) | 0/7 (0.0%) | 0 |
| prof_credit_load | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 0 |
| prof_future_other | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 0 |
| prof_other_3credit | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 0 |
| prof_other_industry | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 0 |
| prof_other_required | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 0 |
| professor_assessment_filter | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 0 |
| professor_assessment_ranking | 4 | 3/4 (75.0%) | 3/4 (75.0%) | 3/4 (75.0%) | 1 |
| professor_required_credit_chain | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 0 |
| rule_reasoning | 3 | 0/3 (0.0%) | 0/3 (0.0%) | 0/3 (0.0%) | 0 |
| schedule_overlap | 4 | 1/4 (25.0%) | 1/4 (25.0%) | 4/4 (100.0%) | 3 |
| simulated_student_fixture | 6 | 6/6 (100.0%) | 6/6 (100.0%) | 6/6 (100.0%) | 0 |
| single_document | 8 | 2/8 (25.0%) | 2/8 (25.0%) | 8/8 (100.0%) | 6 |
| teacher_credits | 4 | 2/4 (50.0%) | 2/4 (50.0%) | 4/4 (100.0%) | 2 |
| temporal_reasoning | 4 | 1/4 (25.0%) | 1/4 (25.0%) | 4/4 (100.0%) | 3 |
| weighted_exam_score | 4 | 0/4 (0.0%) | 0/4 (0.0%) | 0/4 (0.0%) | 0 |

## 결과는 맞았지만 논리가 틀림 — 실행 비교가 놓친 오답 (28개)

### J009 — 실행 진단 correct
질문: 2026학년도 2학기 EE209-02(논리회로)의 담당 교수 이름과 학점을 알려줘.

- 판정 이유: LEFT JOIN과 DISTINCT 누락으로 담당 교수 없는 행이나 중복 교수 행을 정답과 다르게 반환할 수 있다.

정답 SQL:
```sql
SELECT DISTINCT p.name AS professor_name,o.credits FROM course_offerings o JOIN offering_professors op ON op.offering_id=o.offering_id JOIN professors p ON p.professor_id=op.professor_id WHERE o.year=2026 AND o.semester='2' AND o.course_code='EE209' AND o.section='02' AND o.campus='국제';
```
모델 SQL:
```sql
SELECT p.name AS professor_name, co.credits
FROM course_offerings co
LEFT JOIN offering_professors op ON co.offering_id = op.offering_id
LEFT JOIN professors p ON op.professor_id = p.professor_id
WHERE co.year = 2026
  AND co.semester = '2'
  AND co.course_code = 'EE209'
  AND co.section = '02';
```

### J010 — 실행 진단 correct
질문: 2026학년도 2학기 EE209-02(논리회로)의 영어강좌 구분(영어전체/영어부분/해당없음)과 산학필수 여부(예/아니오)를 알려줘.

- 판정 이유: 제2외국어 유형을 해당없음이 아닌 별도 값으로 출력해 정답과 논리적으로 다르다.

정답 SQL:
```sql
SELECT CASE o.english_type WHEN 'FULL' THEN '영어전체' WHEN 'PARTIAL' THEN '영어부분' ELSE '해당없음' END AS english_classification,CASE WHEN o.industry_required=1 THEN '예' ELSE '아니오' END AS industry_required FROM course_offerings o WHERE o.year=2026 AND o.semester='2' AND o.course_code='EE209' AND o.section='02' AND o.campus='국제';
```
모델 SQL:
```sql
SELECT CASE co.english_type
           WHEN 'FULL' THEN '영어전체'
           WHEN 'PARTIAL' THEN '영어부분'
           WHEN 'SECOND_FOREIGN_LANGUAGE' THEN '제2외국어'
           ELSE '해당없음'
       END AS english_label,
       CASE co.industry_required
           WHEN 1 THEN '예'
           ELSE '아니오'
       END AS industry_label
FROM course_offerings co
WHERE co.year = 2026
  AND co.semester = '2'
  AND co.course_code = 'EE209'
  AND co.section = '02';
```

### J013 — 실행 진단 correct
질문: 2026학년도 1학기 CSE301-01(운영체제)의 영어강좌 구분(영어전체/영어부분/해당없음)과 산학필수 여부(예/아니오)를 알려줘.

- 판정 이유: 제2외국어 유형을 정답의 해당없음이 아닌 제2외국어로 출력해 논리적으로 다릅니다.

정답 SQL:
```sql
SELECT CASE o.english_type WHEN 'FULL' THEN '영어전체' WHEN 'PARTIAL' THEN '영어부분' ELSE '해당없음' END AS english_classification,CASE WHEN o.industry_required=1 THEN '예' ELSE '아니오' END AS industry_required FROM course_offerings o WHERE o.year=2026 AND o.semester='1' AND o.course_code='CSE301' AND o.section='01' AND o.campus='국제';
```
모델 SQL:
```sql
SELECT
    CASE english_type
        WHEN 'FULL' THEN '영어전체'
        WHEN 'PARTIAL' THEN '영어부분'
        WHEN 'NONE' THEN '해당없음'
        WHEN 'SECOND_FOREIGN_LANGUAGE' THEN '제2외국어'
        ELSE english_type
    END AS english_type_kr,
    CASE industry_required
        WHEN 1 THEN '예'
        WHEN 0 THEN '아니오'
    END AS industry_required_kr
FROM course_offerings
WHERE year = 2026
  AND semester = '1'
  AND course_code = 'CSE301'
  AND section = '01';
```

### J014 — 실행 진단 correct
질문: 2026학년도 1학기 SWCON366-00(3D데이터처리) 담당 교수의 같은 학기 소프트웨어융합학과 개설목록 내 다른 3학점 강좌 중, 중간·기말 비율이 모두 기재된 강좌끼리 비교하면 시험 비율 합계가 가장 낮은 강좌는? 과목코드·분반·합계를 알려주고 동률은 모두 포함해줘. 기준 과목 코드는 제외해줘.

- 판정 이유: 정답은 개설목록의 분류 학과가 A07337인 강좌만 포함하지만, 모델은 과목 소속 학과 조건까지 OR로 허용한다.

정답 SQL:
```sql
WITH anchor_prof AS (SELECT DISTINCT op.professor_id FROM course_offerings o JOIN offering_professors op ON op.offering_id=o.offering_id WHERE o.year=2026 AND o.semester='1' AND o.course_code='SWCON366' AND o.section='00' AND o.campus='국제'), candidates AS (SELECT DISTINCT o.course_code,o.section,s.midterm_percentage+s.final_exam_percentage AS exam_total_percentage FROM course_offerings o JOIN offering_professors op ON op.offering_id=o.offering_id JOIN anchor_prof ap ON ap.professor_id=op.professor_id JOIN course_offering_categories oc ON oc.offering_id=o.offering_id JOIN departments d ON d.department_id=oc.department_id JOIN course_categories cc ON cc.category_id=oc.category_id JOIN syllabi s ON s.offering_id=o.offering_id WHERE o.year=2026 AND o.semester='1' AND o.campus='국제' AND d.code='A07337' AND o.course_code<>'SWCON366' AND o.credits=3 AND s.midterm_percentage IS NOT NULL AND s.final_exam_percentage IS NOT NULL) SELECT course_code,section,exam_total_percentage FROM candidates WHERE exam_total_percentage=(SELECT MIN(exam_total_percentage) FROM candidates) ORDER BY course_code,section;
```
모델 SQL:
```sql
WITH target_prof AS (
    SELECT op.professor_id
    FROM course_offerings co
    JOIN offering_professors op ON co.offering_id = op.offering_id
    WHERE co.year = 2026
      AND co.semester = '1'
      AND co.course_code = 'SWCON366'
      AND co.section = '00'
),
candidate_offerings AS (
    SELECT DISTINCT
        co.offering_id,
        co.course_code,
        co.section,
        (s.midterm_percentage + s.final_exam_percentage) AS exam_total
    FROM course_offerings co
    JOIN offering_professors op ON co.offering_id = op.offering_id
    JOIN target_prof tp ON op.professor_id = tp.professor_id
    JOIN syllabi s ON co.offering_id = s.offering_id
    LEFT JOIN courses c ON co.course_code = c.course_code
    LEFT JOIN course_offering_categories coc ON co.offering_id = coc.offering_id
    WHERE co.year = 2026
      AND co.semester = '1'
      AND co.credits = 3
      AND co.course_code != 'SWCON366'
      AND s.midterm_percentage IS NOT NULL
      AND s.final_exam_percentage IS NOT NULL
      AND (c.department_id = 8 OR coc.department_id = 8)
)
SELECT
    course_code,
    section,
    exam_total
FROM candidate_offerings
WHERE exam_total = (SELECT MIN(exam_total) FROM candidate_offerings)
ORDER BY course_code, section;
```

### J015 — 실행 진단 correct
질문: 2025학년도 1학기 EE211-02(확률및랜덤변수)의 담당 교수 이름과 학점을 알려줘.

- 판정 이유: 정답의 DISTINCT가 빠져 중복 교수명·학점 행을 제거하지 못할 수 있다.

정답 SQL:
```sql
SELECT DISTINCT p.name AS professor_name,o.credits FROM course_offerings o JOIN offering_professors op ON op.offering_id=o.offering_id JOIN professors p ON p.professor_id=op.professor_id WHERE o.year=2025 AND o.semester='1' AND o.course_code='EE211' AND o.section='02' AND o.campus='국제';
```
모델 SQL:
```sql
SELECT p.name AS professor_name, co.credits
FROM course_offerings co
JOIN offering_professors op ON co.offering_id = op.offering_id
JOIN professors p ON op.professor_id = p.professor_id
WHERE co.year = 2025
  AND co.semester = '1'
  AND co.course_code = 'EE211'
  AND co.section = '02'
```

### J016 — 실행 진단 correct
질문: 2025학년도 1학기 EE211-02(확률및랜덤변수)의 영어강좌 구분(영어전체/영어부분/해당없음)과 산학필수 여부(예/아니오)를 알려줘.

- 판정 이유: 제2외국어 값에서 정답은 해당없음으로 분류하지만 모델은 제2외국어로 출력한다.

정답 SQL:
```sql
SELECT CASE o.english_type WHEN 'FULL' THEN '영어전체' WHEN 'PARTIAL' THEN '영어부분' ELSE '해당없음' END AS english_classification,CASE WHEN o.industry_required=1 THEN '예' ELSE '아니오' END AS industry_required FROM course_offerings o WHERE o.year=2025 AND o.semester='1' AND o.course_code='EE211' AND o.section='02' AND o.campus='국제';
```
모델 SQL:
```sql
SELECT
    CASE english_type
        WHEN 'FULL' THEN '영어전체'
        WHEN 'PARTIAL' THEN '영어부분'
        WHEN 'NONE' THEN '해당없음'
        WHEN 'SECOND_FOREIGN_LANGUAGE' THEN '제2외국어'
        ELSE english_type
    END AS english_type_kr,
    CASE industry_required
        WHEN 1 THEN '예'
        WHEN 0 THEN '아니오'
    END AS industry_required_kr
FROM course_offerings
WHERE year = 2025
  AND semester = '1'
  AND course_code = 'EE211'
  AND section = '02';
```

### J019 — 실행 진단 correct
질문: 2026학년도 2학기 AI4007-07(독립심화학습(인공지능)2)의 영어강좌 구분(영어전체/영어부분/해당없음)과 산학필수 여부(예/아니오)를 알려줘.

- 판정 이유: SECOND_FOREIGN_LANGUAGE일 때 정답은 해당없음이나 모델은 원문 값을 반환한다.

정답 SQL:
```sql
SELECT CASE o.english_type WHEN 'FULL' THEN '영어전체' WHEN 'PARTIAL' THEN '영어부분' ELSE '해당없음' END AS english_classification,CASE WHEN o.industry_required=1 THEN '예' ELSE '아니오' END AS industry_required FROM course_offerings o WHERE o.year=2026 AND o.semester='2' AND o.course_code='AI4007' AND o.section='07' AND o.campus='국제';
```
모델 SQL:
```sql
SELECT
    CASE english_type
        WHEN 'FULL' THEN '영어전체'
        WHEN 'PARTIAL' THEN '영어부분'
        WHEN 'NONE' THEN '해당없음'
        ELSE english_type
    END AS english_type_kr,
    CASE industry_required
        WHEN 1 THEN '예'
        WHEN 0 THEN '아니오'
    END AS industry_required_kr
FROM course_offerings
WHERE year = 2026
  AND semester = '2'
  AND course_code = 'AI4007'
  AND section = '07';
```

### J029 — 실행 진단 correct
질문: 2025학년도 1학기 EE211-02(확률및랜덤변수)와 2025학년도 1학기 CSE438-00(최신기술콜로키움1)의 중간·기말 비율 합계를 각각 구하고, 두 번째 합계에서 첫 번째 합계를 뺀 차이도 알려줘.

- 판정 이유: COALESCE로 중간·기말 비율이 NULL인 경우 정답의 NULL 결과를 0으로 바꿉니다.

정답 SQL:
```sql
SELECT ((SELECT s.midterm_percentage FROM course_offerings o JOIN syllabi s ON s.offering_id=o.offering_id WHERE o.year=2025 AND o.semester='1' AND o.course_code='EE211' AND o.section='02' AND o.campus='국제')+(SELECT s.final_exam_percentage FROM course_offerings o JOIN syllabi s ON s.offering_id=o.offering_id WHERE o.year=2025 AND o.semester='1' AND o.course_code='EE211' AND o.section='02' AND o.campus='국제')) AS first_exam_total,((SELECT s.midterm_percentage FROM course_offerings o JOIN syllabi s ON s.offering_id=o.offering_id WHERE o.year=2025 AND o.semester='1' AND o.course_code='CSE438' AND o.section='00' AND o.campus='국제')+(SELECT s.final_exam_percentage FROM course_offerings o JOIN syllabi s ON s.offering_id=o.offering_id WHERE o.year=2025 AND o.semester='1' AND o.course_code='CSE438' AND o.section='00' AND o.campus='국제')) AS second_exam_total,((SELECT s.midterm_percentage FROM course_offerings o JOIN syllabi s ON s.offering_id=o.offering_id WHERE o.year=2025 AND o.semester='1' AND o.course_code='CSE438' AND o.section='00' AND o.campus='국제')+(SELECT s.final_exam_percentage FROM course_offerings o JOIN syllabi s ON s.offering_id=o.offering_id WHERE o.year=2025 AND o.semester='1' AND o.course_code='CSE438' AND o.section='00' AND o.campus='국제'))-((SELECT s.midterm_percentage FROM course_offerings o JOIN syllabi s ON s.offering_id=o.offering_id WHERE o.year=2025 AND o.semester='1' AND o.course_code='EE211' AND o.section='02' AND o.campus='국제')+(SELECT s.final_exam_percentage FROM course_offerings o JOIN syllabi s ON s.offering_id=o.offering_id WHERE o.year=2025 AND o.semester='1' AND o.course_code='EE211' AND o.section='02' AND o.campus='국제')) AS second_minus_first_pp;
```
모델 SQL:
```sql
WITH exam_sums AS (
    SELECT
        MAX(CASE WHEN co.course_code = 'EE211' AND co.section = '02' THEN COALESCE(s.midterm_percentage, 0) + COALESCE(s.final_exam_percentage, 0) END) AS first_exam_sum,
        MAX(CASE WHEN co.course_code = 'CSE438' AND co.section = '00' THEN COALESCE(s.midterm_percentage, 0) + COALESCE(s.final_exam_percentage, 0) END) AS second_exam_sum
    FROM course_offerings co
    JOIN syllabi s ON s.offering_id = co.offering_id
    WHERE co.year = 2025
      AND co.semester = '1'
      AND ((co.course_code = 'EE211' AND co.section = '02') OR (co.course_code = 'CSE438' AND co.section = '00'))
)
SELECT
    first_exam_sum,
    second_exam_sum,
    second_exam_sum - first_exam_sum AS diff_exam_sum
FROM exam_sums;
```

### J030 — 실행 진단 correct
질문: 2026학년도 2학기 AI3003-00(자연언어학습)와 2025학년도 1학기 CSE428-00(컴퓨터그래픽스)의 중간·기말 비율 합계를 각각 구하고, 두 번째 합계에서 첫 번째 합계를 뺀 차이도 알려줘.

- 판정 이유: COALESCE로 NULL 비율을 0으로 처리해 정답 SQL의 NULL 전파 결과와 다를 수 있다.

정답 SQL:
```sql
SELECT ((SELECT s.midterm_percentage FROM course_offerings o JOIN syllabi s ON s.offering_id=o.offering_id WHERE o.year=2026 AND o.semester='2' AND o.course_code='AI3003' AND o.section='00' AND o.campus='국제')+(SELECT s.final_exam_percentage FROM course_offerings o JOIN syllabi s ON s.offering_id=o.offering_id WHERE o.year=2026 AND o.semester='2' AND o.course_code='AI3003' AND o.section='00' AND o.campus='국제')) AS first_exam_total,((SELECT s.midterm_percentage FROM course_offerings o JOIN syllabi s ON s.offering_id=o.offering_id WHERE o.year=2025 AND o.semester='1' AND o.course_code='CSE428' AND o.section='00' AND o.campus='국제')+(SELECT s.final_exam_percentage FROM course_offerings o JOIN syllabi s ON s.offering_id=o.offering_id WHERE o.year=2025 AND o.semester='1' AND o.course_code='CSE428' AND o.section='00' AND o.campus='국제')) AS second_exam_total,((SELECT s.midterm_percentage FROM course_offerings o JOIN syllabi s ON s.offering_id=o.offering_id WHERE o.year=2025 AND o.semester='1' AND o.course_code='CSE428' AND o.section='00' AND o.campus='국제')+(SELECT s.final_exam_percentage FROM course_offerings o JOIN syllabi s ON s.offering_id=o.offering_id WHERE o.year=2025 AND o.semester='1' AND o.course_code='CSE428' AND o.section='00' AND o.campus='국제'))-((SELECT s.midterm_percentage FROM course_offerings o JOIN syllabi s ON s.offering_id=o.offering_id WHERE o.year=2026 AND o.semester='2' AND o.course_code='AI3003' AND o.section='00' AND o.campus='국제')+(SELECT s.final_exam_percentage FROM course_offerings o JOIN syllabi s ON s.offering_id=o.offering_id WHERE o.year=2026 AND o.semester='2' AND o.course_code='AI3003' AND o.section='00' AND o.campus='국제')) AS second_minus_first_pp;
```
모델 SQL:
```sql
WITH target_offerings AS (
    SELECT
        co.year,
        co.semester,
        co.course_code,
        co.section,
        co.course_name,
        COALESCE(s.midterm_percentage, 0) + COALESCE(s.final_exam_percentage, 0) AS exam_sum
    FROM course_offerings co
    JOIN syllabi s ON s.offering_id = co.offering_id
    WHERE (co.year = 2026 AND co.semester = '2' AND co.course_code = 'AI3003' AND co.section = '00')
       OR (co.year = 2025 AND co.semester = '1' AND co.course_code = 'CSE428' AND co.section = '00')
)
SELECT
    a.exam_sum AS first_exam_sum,
    b.exam_sum AS second_exam_sum,
    b.exam_sum - a.exam_sum AS exam_sum_diff
FROM target_offerings a
CROSS JOIN target_offerings b
WHERE a.year = 2026 AND a.semester = '2' AND a.course_code = 'AI3003' AND a.section = '00'
  AND b.year = 2025 AND b.semester = '1' AND b.course_code = 'CSE428' AND b.section = '00';
```

### J031 — 실행 진단 correct
질문: 2025학년도 1학기 CSE496-06(연구연수활동1(컴퓨터공학))와 2025학년도 1학기 CSE304-00(알고리즘)의 중간·기말 비율 합계를 각각 구하고, 두 번째 합계에서 첫 번째 합계를 뺀 차이도 알려줘.

- 판정 이유: MAX와 COALESCE(널→0)를 사용해 정답의 단순 합계 및 널 처리와 달라질 수 있다.

정답 SQL:
```sql
SELECT ((SELECT s.midterm_percentage FROM course_offerings o JOIN syllabi s ON s.offering_id=o.offering_id WHERE o.year=2025 AND o.semester='1' AND o.course_code='CSE496' AND o.section='06' AND o.campus='국제')+(SELECT s.final_exam_percentage FROM course_offerings o JOIN syllabi s ON s.offering_id=o.offering_id WHERE o.year=2025 AND o.semester='1' AND o.course_code='CSE496' AND o.section='06' AND o.campus='국제')) AS first_exam_total,((SELECT s.midterm_percentage FROM course_offerings o JOIN syllabi s ON s.offering_id=o.offering_id WHERE o.year=2025 AND o.semester='1' AND o.course_code='CSE304' AND o.section='00' AND o.campus='국제')+(SELECT s.final_exam_percentage FROM course_offerings o JOIN syllabi s ON s.offering_id=o.offering_id WHERE o.year=2025 AND o.semester='1' AND o.course_code='CSE304' AND o.section='00' AND o.campus='국제')) AS second_exam_total,((SELECT s.midterm_percentage FROM course_offerings o JOIN syllabi s ON s.offering_id=o.offering_id WHERE o.year=2025 AND o.semester='1' AND o.course_code='CSE304' AND o.section='00' AND o.campus='국제')+(SELECT s.final_exam_percentage FROM course_offerings o JOIN syllabi s ON s.offering_id=o.offering_id WHERE o.year=2025 AND o.semester='1' AND o.course_code='CSE304' AND o.section='00' AND o.campus='국제'))-((SELECT s.midterm_percentage FROM course_offerings o JOIN syllabi s ON s.offering_id=o.offering_id WHERE o.year=2025 AND o.semester='1' AND o.course_code='CSE496' AND o.section='06' AND o.campus='국제')+(SELECT s.final_exam_percentage FROM course_offerings o JOIN syllabi s ON s.offering_id=o.offering_id WHERE o.year=2025 AND o.semester='1' AND o.course_code='CSE496' AND o.section='06' AND o.campus='국제')) AS second_minus_first_pp;
```
모델 SQL:
```sql
WITH exam_sums AS (
    SELECT
        MAX(CASE WHEN co.course_code = 'CSE496' AND co.section = '06' THEN COALESCE(s.midterm_percentage, 0) + COALESCE(s.final_exam_percentage, 0) END) AS first_exam_sum,
        MAX(CASE WHEN co.course_code = 'CSE304' AND co.section = '00' THEN COALESCE(s.midterm_percentage, 0) + COALESCE(s.final_exam_percentage, 0) END) AS second_exam_sum
    FROM course_offerings co
    JOIN syllabi s ON s.offering_id = co.offering_id
    WHERE co.year = 2025
      AND co.semester = '1'
      AND (
          (co.course_code = 'CSE496' AND co.section = '06')
          OR (co.course_code = 'CSE304' AND co.section = '00')
      )
)
SELECT
    first_exam_sum,
    second_exam_sum,
    second_exam_sum - first_exam_sum AS exam_sum_diff
FROM exam_sums;
```

### J032 — 실행 진단 correct
질문: 2025학년도 1학기 CSE405-00(졸업프로젝트)와 2026학년도 1학기 IE419-00(서비스데이터사이언스)의 중간·기말 비율 합계를 각각 구하고, 두 번째 합계에서 첫 번째 합계를 뺀 차이도 알려줘.

- 판정 이유: COALESCE로 NULL 비율을 0으로 처리해 정답의 NULL 전파 결과와 달라질 수 있다.

정답 SQL:
```sql
SELECT ((SELECT s.midterm_percentage FROM course_offerings o JOIN syllabi s ON s.offering_id=o.offering_id WHERE o.year=2025 AND o.semester='1' AND o.course_code='CSE405' AND o.section='00' AND o.campus='국제')+(SELECT s.final_exam_percentage FROM course_offerings o JOIN syllabi s ON s.offering_id=o.offering_id WHERE o.year=2025 AND o.semester='1' AND o.course_code='CSE405' AND o.section='00' AND o.campus='국제')) AS first_exam_total,((SELECT s.midterm_percentage FROM course_offerings o JOIN syllabi s ON s.offering_id=o.offering_id WHERE o.year=2026 AND o.semester='1' AND o.course_code='IE419' AND o.section='00' AND o.campus='국제')+(SELECT s.final_exam_percentage FROM course_offerings o JOIN syllabi s ON s.offering_id=o.offering_id WHERE o.year=2026 AND o.semester='1' AND o.course_code='IE419' AND o.section='00' AND o.campus='국제')) AS second_exam_total,((SELECT s.midterm_percentage FROM course_offerings o JOIN syllabi s ON s.offering_id=o.offering_id WHERE o.year=2026 AND o.semester='1' AND o.course_code='IE419' AND o.section='00' AND o.campus='국제')+(SELECT s.final_exam_percentage FROM course_offerings o JOIN syllabi s ON s.offering_id=o.offering_id WHERE o.year=2026 AND o.semester='1' AND o.course_code='IE419' AND o.section='00' AND o.campus='국제'))-((SELECT s.midterm_percentage FROM course_offerings o JOIN syllabi s ON s.offering_id=o.offering_id WHERE o.year=2025 AND o.semester='1' AND o.course_code='CSE405' AND o.section='00' AND o.campus='국제')+(SELECT s.final_exam_percentage FROM course_offerings o JOIN syllabi s ON s.offering_id=o.offering_id WHERE o.year=2025 AND o.semester='1' AND o.course_code='CSE405' AND o.section='00' AND o.campus='국제')) AS second_minus_first_pp;
```
모델 SQL:
```sql
WITH c1 AS (
    SELECT COALESCE(s.midterm_percentage, 0) + COALESCE(s.final_exam_percentage, 0) AS sum1
    FROM course_offerings co
    JOIN syllabi s ON co.offering_id = s.offering_id
    WHERE co.year = 2025 AND co.semester = '1' AND co.course_code = 'CSE405' AND co.section = '00'
),
c2 AS (
    SELECT COALESCE(s.midterm_percentage, 0) + COALESCE(s.final_exam_percentage, 0) AS sum2
    FROM course_offerings co
    JOIN syllabi s ON co.offering_id = s.offering_id
    WHERE co.year = 2026 AND co.semester = '1' AND co.course_code = 'IE419' AND co.section = '00'
)
SELECT c1.sum1, c2.sum2, (c2.sum2 - c1.sum1) AS diff
FROM c1 CROSS JOIN c2
```

### J033 — 실행 진단 correct
질문: 2026학년도 2학기 EE209-02(논리회로)와 2026학년도 1학기 CSE204-01(자료구조) 중 중간고사 비율이 더 큰 강좌의 과목코드·연도·학기·분반·비율을 알려줘. 같으면 둘 다 알려줘.

- 판정 이유: 정답의 다중 인자 MAX는 한 비율이 NULL이면 NULL을 반환하지만 모델의 집계 MAX는 NULL을 무시해 결과가 달라질 수 있다.

정답 SQL:
```sql
SELECT o.course_code,o.year,o.semester,o.section,s.midterm_percentage AS percentage FROM course_offerings o JOIN syllabi s ON s.offering_id=o.offering_id WHERE ((o.year=2026 AND o.semester='2' AND o.course_code='EE209' AND o.section='02' AND o.campus='국제') OR (o.year=2026 AND o.semester='1' AND o.course_code='CSE204' AND o.section='01' AND o.campus='국제')) AND s.midterm_percentage=MAX((SELECT s.midterm_percentage FROM course_offerings o JOIN syllabi s ON s.offering_id=o.offering_id WHERE o.year=2026 AND o.semester='2' AND o.course_code='EE209' AND o.section='02' AND o.campus='국제'),(SELECT s.midterm_percentage FROM course_offerings o JOIN syllabi s ON s.offering_id=o.offering_id WHERE o.year=2026 AND o.semester='1' AND o.course_code='CSE204' AND o.section='01' AND o.campus='국제')) ORDER BY o.course_code,o.year,o.semester,o.section;
```
모델 SQL:
```sql
WITH target AS (
    SELECT
        co.course_code,
        co.year,
        co.semester,
        co.section,
        s.midterm_percentage
    FROM course_offerings AS co
    JOIN syllabi AS s
        ON s.offering_id = co.offering_id
    WHERE (co.year = 2026 AND co.semester = '2' AND co.course_code = 'EE209' AND co.section = '02')
       OR (co.year = 2026 AND co.semester = '1' AND co.course_code = 'CSE204' AND co.section = '01')
)
SELECT
    course_code,
    year,
    semester,
    section,
    midterm_percentage
FROM target
WHERE midterm_percentage = (SELECT MAX(midterm_percentage) FROM target)
ORDER BY year, semester, course_code, section;
```

### J065 — 실행 진단 correct
질문: 2026학년도 1학기 IE419-00(서비스데이터사이언스)와 2025학년도 2학기 IE306-00(데이터마이닝)를 모두 담당한 교수 이름을 알려줘.

- 판정 이유: 두 과목 담당자를 올바르게 교집합하지만 DISTINCT가 없어 중복 교수명이 반환될 수 있다.

정답 SQL:
```sql
SELECT DISTINCT p.name AS professor_name FROM professors p WHERE p.professor_id IN(SELECT op.professor_id FROM course_offerings o JOIN offering_professors op ON op.offering_id=o.offering_id WHERE o.year=2026 AND o.semester='1' AND o.course_code='IE419' AND o.section='00' AND o.campus='국제') AND p.professor_id IN(SELECT op.professor_id FROM course_offerings o JOIN offering_professors op ON op.offering_id=o.offering_id WHERE o.year=2025 AND o.semester='2' AND o.course_code='IE306' AND o.section='00' AND o.campus='국제') ORDER BY p.name;
```
모델 SQL:
```sql
SELECT p.name AS professor_name
FROM professors p
JOIN offering_professors op1 ON p.professor_id = op1.professor_id
JOIN course_offerings co1 ON op1.offering_id = co1.offering_id
JOIN offering_professors op2 ON p.professor_id = op2.professor_id
JOIN course_offerings co2 ON op2.offering_id = co2.offering_id
WHERE co1.year = 2026 AND co1.semester = '1' AND co1.course_code = 'IE419' AND co1.section = '00'
  AND co2.year = 2025 AND co2.semester = '2' AND co2.course_code = 'IE306' AND co2.section = '00'
```

### J066 — 실행 진단 correct
질문: 2025학년도 2학기 AI4007-00(독립심화학습(인공지능)2)와 2026학년도 1학기 CSE204-01(자료구조)를 모두 담당한 교수 이름을 알려줘.

- 판정 이유: 두 조건을 모두 만족하지만 DISTINCT가 없어 여러 매칭 시 교수명이 중복될 수 있다.

정답 SQL:
```sql
SELECT DISTINCT p.name AS professor_name FROM professors p WHERE p.professor_id IN(SELECT op.professor_id FROM course_offerings o JOIN offering_professors op ON op.offering_id=o.offering_id WHERE o.year=2025 AND o.semester='2' AND o.course_code='AI4007' AND o.section='00' AND o.campus='국제') AND p.professor_id IN(SELECT op.professor_id FROM course_offerings o JOIN offering_professors op ON op.offering_id=o.offering_id WHERE o.year=2026 AND o.semester='1' AND o.course_code='CSE204' AND o.section='01' AND o.campus='국제') ORDER BY p.name;
```
모델 SQL:
```sql
SELECT p.name AS professor_name
FROM professors p
JOIN offering_professors op1 ON p.professor_id = op1.professor_id
JOIN course_offerings co1 ON op1.offering_id = co1.offering_id
JOIN offering_professors op2 ON p.professor_id = op2.professor_id
JOIN course_offerings co2 ON op2.offering_id = co2.offering_id
WHERE co1.year = 2025
  AND co1.semester = '2'
  AND co1.course_code = 'AI4007'
  AND co1.section = '00'
  AND co2.year = 2026
  AND co2.semester = '1'
  AND co2.course_code = 'CSE204'
  AND co2.section = '01';
```

### J067 — 실행 진단 correct
질문: 2025학년도 2학기 SWCON253-01(기계학습)와 2026학년도 2학기 CSE497-03(연구연수활동2(컴퓨터공학))를 모두 담당한 교수 이름을 알려줘.

- 판정 이유: 조건은 같지만 DISTINCT가 없어 동일 교수가 여러 행으로 중복 출력될 수 있다.

정답 SQL:
```sql
SELECT DISTINCT p.name AS professor_name FROM professors p WHERE p.professor_id IN(SELECT op.professor_id FROM course_offerings o JOIN offering_professors op ON op.offering_id=o.offering_id WHERE o.year=2025 AND o.semester='2' AND o.course_code='SWCON253' AND o.section='01' AND o.campus='국제') AND p.professor_id IN(SELECT op.professor_id FROM course_offerings o JOIN offering_professors op ON op.offering_id=o.offering_id WHERE o.year=2026 AND o.semester='2' AND o.course_code='CSE497' AND o.section='03' AND o.campus='국제') ORDER BY p.name;
```
모델 SQL:
```sql
SELECT p.name AS professor_name
FROM professors p
JOIN offering_professors op1 ON p.professor_id = op1.professor_id
JOIN course_offerings co1 ON op1.offering_id = co1.offering_id
JOIN offering_professors op2 ON p.professor_id = op2.professor_id
JOIN course_offerings co2 ON op2.offering_id = co2.offering_id
WHERE co1.year = 2025 AND co1.semester = '2' AND co1.course_code = 'SWCON253' AND co1.section = '01'
  AND co2.year = 2026 AND co2.semester = '2' AND co2.course_code = 'CSE497' AND co2.section = '03';
```

### J068 — 실행 진단 correct
질문: 2025학년도 1학기 CSE406-05(캡스톤디자인)와 2026학년도 2학기 SWCON313-00(가상현실)를 모두 담당한 교수 이름을 알려줘.

- 판정 이유: 두 과목을 모두 담당한 교수는 찾지만 DISTINCT가 없어 동일 교수명이 중복될 수 있다.

정답 SQL:
```sql
SELECT DISTINCT p.name AS professor_name FROM professors p WHERE p.professor_id IN(SELECT op.professor_id FROM course_offerings o JOIN offering_professors op ON op.offering_id=o.offering_id WHERE o.year=2025 AND o.semester='1' AND o.course_code='CSE406' AND o.section='05' AND o.campus='국제') AND p.professor_id IN(SELECT op.professor_id FROM course_offerings o JOIN offering_professors op ON op.offering_id=o.offering_id WHERE o.year=2026 AND o.semester='2' AND o.course_code='SWCON313' AND o.section='00' AND o.campus='국제') ORDER BY p.name;
```
모델 SQL:
```sql
SELECT p.name AS professor_name
FROM professors p
JOIN offering_professors op1 ON p.professor_id = op1.professor_id
JOIN course_offerings co1 ON op1.offering_id = co1.offering_id
JOIN offering_professors op2 ON p.professor_id = op2.professor_id
JOIN course_offerings co2 ON op2.offering_id = co2.offering_id
WHERE co1.year = 2025 AND co1.semester = '1' AND co1.course_code = 'CSE406' AND co1.section = '05'
  AND co2.year = 2026 AND co2.semester = '2' AND co2.course_code = 'SWCON313' AND co2.section = '00';
```

### J069 — 실행 진단 correct
질문: 2026학년도 1학기 IE419-00(서비스데이터사이언스)와 2026학년도 1학기 SWCON104-01(웹/파이선프로그래밍)의 정규 수업시간이 일주일에 총 몇 분 겹쳐? 시험 일정은 제외하고 요일별 겹치는 구간만 합산해줘.

- 판정 이유: 동일 시간대가 여러 강의실로 중복 등록되면 DISTINCT가 없어 겹침 시간이 중복 합산된다.

정답 SQL:
```sql
WITH a AS (SELECT DISTINCT t.day,t.start_time,t.end_time FROM course_offerings o JOIN class_times c ON c.offering_id=o.offering_id JOIN time_slots t ON t.time_slot_id=c.time_slot_id WHERE o.year=2026 AND o.semester='1' AND o.course_code='IE419' AND o.section='00' AND o.campus='국제'),b AS (SELECT DISTINCT t.day,t.start_time,t.end_time FROM course_offerings o JOIN class_times c ON c.offering_id=o.offering_id JOIN time_slots t ON t.time_slot_id=c.time_slot_id WHERE o.year=2026 AND o.semester='1' AND o.course_code='SWCON104' AND o.section='01' AND o.campus='국제') SELECT COALESCE(SUM(MAX(MIN((CAST(substr(a.end_time,1,2) AS INTEGER)*60+CAST(substr(a.end_time,4,2) AS INTEGER)),(CAST(substr(b.end_time,1,2) AS INTEGER)*60+CAST(substr(b.end_time,4,2) AS INTEGER)))-MAX((CAST(substr(a.start_time,1,2) AS INTEGER)*60+CAST(substr(a.start_time,4,2) AS INTEGER)),(CAST(substr(b.start_time,1,2) AS INTEGER)*60+CAST(substr(b.start_time,4,2) AS INTEGER))),0)),0) AS weekly_overlap_minutes FROM a JOIN b ON a.day=b.day;
```
모델 SQL:
```sql
WITH a AS (
  SELECT ts.day,
         CAST(substr(ts.start_time, 1, 2) AS INTEGER) * 60 + CAST(substr(ts.start_time, 4, 2) AS INTEGER) AS s,
         CAST(substr(ts.end_time, 1, 2) AS INTEGER) * 60 + CAST(substr(ts.end_time, 4, 2) AS INTEGER) AS e
  FROM course_offerings co
  JOIN class_times ct ON ct.offering_id = co.offering_id
  JOIN time_slots ts ON ts.time_slot_id = ct.time_slot_id
  WHERE co.year = 2026 AND co.semester = '1' AND co.course_code = 'IE419' AND co.section = '00'
),
b AS (
  SELECT ts.day,
         CAST(substr(ts.start_time, 1, 2) AS INTEGER) * 60 + CAST(substr(ts.start_time, 4, 2) AS INTEGER) AS s,
         CAST(substr(ts.end_time, 1, 2) AS INTEGER) * 60 + CAST(substr(ts.end_time, 4, 2) AS INTEGER) AS e
  FROM course_offerings co
  JOIN class_times ct ON ct.offering_id = co.offering_id
  JOIN time_slots ts ON ts.time_slot_id = ct.time_slot_id
  WHERE co.year = 2026 AND co.semester = '1' AND co.course_code = 'SWCON104' AND co.section = '01'
)
SELECT COALESCE(SUM(MAX(0, MIN(a.e, b.e) - MAX(a.s, b.s))), 0) AS overlap_minutes
FROM a
JOIN b ON a.day = b.day;
```

### J070 — 실행 진단 correct
질문: 2025학년도 2학기 AI4007-00(독립심화학습(인공지능)2)와 2025학년도 2학기 SWCON401-08(소프트웨어융합캡스톤디자인)의 정규 수업시간이 일주일에 총 몇 분 겹쳐? 시험 일정은 제외하고 요일별 겹치는 구간만 합산해줘.

- 판정 이유: DISTINCT가 없어 동일 시간대의 여러 강의실 행이 겹침 시간을 중복 합산할 수 있다.

정답 SQL:
```sql
WITH a AS (SELECT DISTINCT t.day,t.start_time,t.end_time FROM course_offerings o JOIN class_times c ON c.offering_id=o.offering_id JOIN time_slots t ON t.time_slot_id=c.time_slot_id WHERE o.year=2025 AND o.semester='2' AND o.course_code='AI4007' AND o.section='00' AND o.campus='국제'),b AS (SELECT DISTINCT t.day,t.start_time,t.end_time FROM course_offerings o JOIN class_times c ON c.offering_id=o.offering_id JOIN time_slots t ON t.time_slot_id=c.time_slot_id WHERE o.year=2025 AND o.semester='2' AND o.course_code='SWCON401' AND o.section='08' AND o.campus='국제') SELECT COALESCE(SUM(MAX(MIN((CAST(substr(a.end_time,1,2) AS INTEGER)*60+CAST(substr(a.end_time,4,2) AS INTEGER)),(CAST(substr(b.end_time,1,2) AS INTEGER)*60+CAST(substr(b.end_time,4,2) AS INTEGER)))-MAX((CAST(substr(a.start_time,1,2) AS INTEGER)*60+CAST(substr(a.start_time,4,2) AS INTEGER)),(CAST(substr(b.start_time,1,2) AS INTEGER)*60+CAST(substr(b.start_time,4,2) AS INTEGER))),0)),0) AS weekly_overlap_minutes FROM a JOIN b ON a.day=b.day;
```
모델 SQL:
```sql
WITH a AS (
    SELECT ts.day,
           CAST(SUBSTR(ts.start_time, 1, 2) AS INTEGER) * 60 + CAST(SUBSTR(ts.start_time, 4, 2) AS INTEGER) AS start_min,
           CAST(SUBSTR(ts.end_time, 1, 2) AS INTEGER) * 60 + CAST(SUBSTR(ts.end_time, 4, 2) AS INTEGER) AS end_min
    FROM course_offerings co
    JOIN class_times ct ON ct.offering_id = co.offering_id
    JOIN time_slots ts ON ts.time_slot_id = ct.time_slot_id
    WHERE co.year = 2025 AND co.semester = '2' AND co.course_code = 'AI4007' AND co.section = '00'
),
b AS (
    SELECT ts.day,
           CAST(SUBSTR(ts.start_time, 1, 2) AS INTEGER) * 60 + CAST(SUBSTR(ts.start_time, 4, 2) AS INTEGER) AS start_min,
           CAST(SUBSTR(ts.end_time, 1, 2) AS INTEGER) * 60 + CAST(SUBSTR(ts.end_time, 4, 2) AS INTEGER) AS end_min
    FROM course_offerings co
    JOIN class_times ct ON ct.offering_id = co.offering_id
    JOIN time_slots ts ON ts.time_slot_id = ct.time_slot_id
    WHERE co.year = 2025 AND co.semester = '2' AND co.course_code = 'SWCON401' AND co.section = '08'
)
SELECT COALESCE(SUM(MAX(0, MIN(a.end_min, b.end_min) - MAX(a.start_min, b.start_min))), 0) AS overlap_minutes
FROM a
JOIN b ON a.day = b.day;
```

### J071 — 실행 진단 correct
질문: 2025학년도 2학기 SWCON253-01(기계학습)와 2025학년도 2학기 CSE103-01(객체지향프로그래밍)의 정규 수업시간이 일주일에 총 몇 분 겹쳐? 시험 일정은 제외하고 요일별 겹치는 구간만 합산해줘.

- 판정 이유: DISTINCT가 없어 같은 시간대의 여러 강의실 행을 중복 합산할 수 있다.

정답 SQL:
```sql
WITH a AS (SELECT DISTINCT t.day,t.start_time,t.end_time FROM course_offerings o JOIN class_times c ON c.offering_id=o.offering_id JOIN time_slots t ON t.time_slot_id=c.time_slot_id WHERE o.year=2025 AND o.semester='2' AND o.course_code='SWCON253' AND o.section='01' AND o.campus='국제'),b AS (SELECT DISTINCT t.day,t.start_time,t.end_time FROM course_offerings o JOIN class_times c ON c.offering_id=o.offering_id JOIN time_slots t ON t.time_slot_id=c.time_slot_id WHERE o.year=2025 AND o.semester='2' AND o.course_code='CSE103' AND o.section='01' AND o.campus='국제') SELECT COALESCE(SUM(MAX(MIN((CAST(substr(a.end_time,1,2) AS INTEGER)*60+CAST(substr(a.end_time,4,2) AS INTEGER)),(CAST(substr(b.end_time,1,2) AS INTEGER)*60+CAST(substr(b.end_time,4,2) AS INTEGER)))-MAX((CAST(substr(a.start_time,1,2) AS INTEGER)*60+CAST(substr(a.start_time,4,2) AS INTEGER)),(CAST(substr(b.start_time,1,2) AS INTEGER)*60+CAST(substr(b.start_time,4,2) AS INTEGER))),0)),0) AS weekly_overlap_minutes FROM a JOIN b ON a.day=b.day;
```
모델 SQL:
```sql
WITH slot_a AS (
    SELECT ts.day,
           CAST(substr(ts.start_time, 1, 2) AS INTEGER) * 60 + CAST(substr(ts.start_time, 4, 2) AS INTEGER) AS s,
           CAST(substr(ts.end_time, 1, 2) AS INTEGER) * 60 + CAST(substr(ts.end_time, 4, 2) AS INTEGER) AS e
    FROM course_offerings co
    JOIN class_times ct ON ct.offering_id = co.offering_id
    JOIN time_slots ts ON ts.time_slot_id = ct.time_slot_id
    WHERE co.year = 2025 AND co.semester = '2' AND co.course_code = 'SWCON253' AND co.section = '01'
),
slot_b AS (
    SELECT ts.day,
           CAST(substr(ts.start_time, 1, 2) AS INTEGER) * 60 + CAST(substr(ts.start_time, 4, 2) AS INTEGER) AS s,
           CAST(substr(ts.end_time, 1, 2) AS INTEGER) * 60 + CAST(substr(ts.end_time, 4, 2) AS INTEGER) AS e
    FROM course_offerings co
    JOIN class_times ct ON ct.offering_id = co.offering_id
    JOIN time_slots ts ON ts.time_slot_id = ct.time_slot_id
    WHERE co.year = 2025 AND co.semester = '2' AND co.course_code = 'CSE103' AND co.section = '01'
)
SELECT COALESCE(SUM(MAX(0, MIN(a.e, b.e) - MAX(a.s, b.s))), 0) AS overlap_minutes
FROM slot_a a
JOIN slot_b b ON a.day = b.day;
```

### J073 — 실행 진단 correct
질문: 다음 세 강좌 중 중간·기말 비율 합계가 70% 이상인 강좌의 과목코드·연도·학기·분반·합계를 알려줘: 2025학년도 1학기 CSE406-01(캡스톤디자인), 2026학년도 1학기 AI4003-00(졸업논문(인공지능)), 2025학년도 1학기 CSE405-00(졸업프로젝트).

- 판정 이유: COALESCE로 NULL 비율을 0으로 처리해 정답과 다른 강좌가 포함될 수 있다.

정답 SQL:
```sql
SELECT o.course_code,o.year,o.semester,o.section,s.midterm_percentage+s.final_exam_percentage AS exam_total FROM course_offerings o JOIN syllabi s ON s.offering_id=o.offering_id WHERE ((o.year=2025 AND o.semester='1' AND o.course_code='CSE406' AND o.section='01' AND o.campus='국제') OR (o.year=2026 AND o.semester='1' AND o.course_code='AI4003' AND o.section='00' AND o.campus='국제') OR (o.year=2025 AND o.semester='1' AND o.course_code='CSE405' AND o.section='00' AND o.campus='국제')) AND s.midterm_percentage+s.final_exam_percentage>=70 ORDER BY o.course_code,o.year,o.semester,o.section;
```
모델 SQL:
```sql
SELECT
    co.course_code,
    co.year,
    co.semester,
    co.section,
    COALESCE(s.midterm_percentage, 0) + COALESCE(s.final_exam_percentage, 0) AS exam_total_percentage
FROM course_offerings co
JOIN syllabi s ON co.offering_id = s.offering_id
WHERE (
    (co.year = 2025 AND co.semester = '1' AND co.course_code = 'CSE406' AND co.section = '01')
    OR (co.year = 2026 AND co.semester = '1' AND co.course_code = 'AI4003' AND co.section = '00')
    OR (co.year = 2025 AND co.semester = '1' AND co.course_code = 'CSE405' AND co.section = '00')
)
AND (COALESCE(s.midterm_percentage, 0) + COALESCE(s.final_exam_percentage, 0)) >= 70
ORDER BY co.year, co.semester, co.course_code, co.section
```

### J075 — 실행 진단 correct
질문: 다음 세 강좌 중 중간·기말 비율 합계가 70% 이상인 강좌의 과목코드·연도·학기·분반·합계를 알려줘: 2026학년도 1학기 IE419-00(서비스데이터사이언스), 2025학년도 2학기 CSE497-02(연구연수활동2(컴퓨터공학)), 2026학년도 1학기 EE209-01(논리회로).

- 판정 이유: COALESCE로 결측 비율을 0으로 처리해 정답 SQL과 NULL 상황의 포함 결과가 달라진다.

정답 SQL:
```sql
SELECT o.course_code,o.year,o.semester,o.section,s.midterm_percentage+s.final_exam_percentage AS exam_total FROM course_offerings o JOIN syllabi s ON s.offering_id=o.offering_id WHERE ((o.year=2026 AND o.semester='1' AND o.course_code='IE419' AND o.section='00' AND o.campus='국제') OR (o.year=2025 AND o.semester='2' AND o.course_code='CSE497' AND o.section='02' AND o.campus='국제') OR (o.year=2026 AND o.semester='1' AND o.course_code='EE209' AND o.section='01' AND o.campus='국제')) AND s.midterm_percentage+s.final_exam_percentage>=70 ORDER BY o.course_code,o.year,o.semester,o.section;
```
모델 SQL:
```sql
SELECT co.course_code, co.year, co.semester, co.section,
       COALESCE(s.midterm_percentage, 0) + COALESCE(s.final_exam_percentage, 0) AS exam_total
FROM course_offerings co
JOIN syllabi s ON s.offering_id = co.offering_id
WHERE ((co.year = 2026 AND co.semester = '1' AND co.course_code = 'IE419' AND co.section = '00')
    OR (co.year = 2025 AND co.semester = '2' AND co.course_code = 'CSE497' AND co.section = '02')
    OR (co.year = 2026 AND co.semester = '1' AND co.course_code = 'EE209' AND co.section = '01'))
  AND COALESCE(s.midterm_percentage, 0) + COALESCE(s.final_exam_percentage, 0) >= 70
ORDER BY co.year, co.semester, co.course_code, co.section
```

### J077 — 실행 진단 correct
질문: 다음 세 강좌 중 중간·기말 비율 합계가 70% 이상인 강좌의 과목코드·연도·학기·분반·합계를 알려줘: 2025학년도 2학기 CSE302-01(컴퓨터네트워크), 2026학년도 1학기 SWCON321-02(데이터분석캡스톤디자인), 2026학년도 2학기 CSE406-16(캡스톤디자인).

- 판정 이유: COALESCE로 결측 비율을 0으로 처리해 한 비율이 NULL인 강좌를 잘못 포함할 수 있다.

정답 SQL:
```sql
SELECT o.course_code,o.year,o.semester,o.section,s.midterm_percentage+s.final_exam_percentage AS exam_total FROM course_offerings o JOIN syllabi s ON s.offering_id=o.offering_id WHERE ((o.year=2025 AND o.semester='2' AND o.course_code='CSE302' AND o.section='01' AND o.campus='국제') OR (o.year=2026 AND o.semester='1' AND o.course_code='SWCON321' AND o.section='02' AND o.campus='국제') OR (o.year=2026 AND o.semester='2' AND o.course_code='CSE406' AND o.section='16' AND o.campus='국제')) AND s.midterm_percentage+s.final_exam_percentage>=70 ORDER BY o.course_code,o.year,o.semester,o.section;
```
모델 SQL:
```sql
SELECT co.course_code, co.year, co.semester, co.section,
       COALESCE(s.midterm_percentage, 0) + COALESCE(s.final_exam_percentage, 0) AS exam_total_percentage
FROM course_offerings co
JOIN syllabi s ON s.offering_id = co.offering_id
WHERE ((co.year = 2025 AND co.semester = '2' AND co.course_code = 'CSE302' AND co.section = '01')
    OR (co.year = 2026 AND co.semester = '1' AND co.course_code = 'SWCON321' AND co.section = '02')
    OR (co.year = 2026 AND co.semester = '2' AND co.course_code = 'CSE406' AND co.section = '16'))
  AND COALESCE(s.midterm_percentage, 0) + COALESCE(s.final_exam_percentage, 0) >= 70
ORDER BY co.year, co.semester, co.course_code, co.section
```

### J079 — 실행 진단 correct
질문: 다음 세 강좌 중 중간·기말 비율 합계가 70% 이상인 강좌의 과목코드·연도·학기·분반·합계를 알려줘: 2025학년도 1학기 CSE327-00(소프트웨어공학), 2025학년도 1학기 CSE496-06(연구연수활동1(컴퓨터공학)), 2025학년도 1학기 CSE304-00(알고리즘).

- 판정 이유: NULL 비율을 0으로 대체해 한쪽 비율이 NULL인 강좌를 정답과 다르게 포함할 수 있다.

정답 SQL:
```sql
SELECT o.course_code,o.year,o.semester,o.section,s.midterm_percentage+s.final_exam_percentage AS exam_total FROM course_offerings o JOIN syllabi s ON s.offering_id=o.offering_id WHERE ((o.year=2025 AND o.semester='1' AND o.course_code='CSE327' AND o.section='00' AND o.campus='국제') OR (o.year=2025 AND o.semester='1' AND o.course_code='CSE496' AND o.section='06' AND o.campus='국제') OR (o.year=2025 AND o.semester='1' AND o.course_code='CSE304' AND o.section='00' AND o.campus='국제')) AND s.midterm_percentage+s.final_exam_percentage>=70 ORDER BY o.course_code,o.year,o.semester,o.section;
```
모델 SQL:
```sql
SELECT co.course_code,
       co.year,
       co.semester,
       co.section,
       COALESCE(s.midterm_percentage, 0) + COALESCE(s.final_exam_percentage, 0) AS exam_total_percentage
FROM course_offerings AS co
JOIN syllabi AS s ON s.offering_id = co.offering_id
WHERE co.year = 2025
  AND co.semester = '1'
  AND (
    (co.course_code = 'CSE327' AND co.section = '00')
    OR (co.course_code = 'CSE496' AND co.section = '06')
    OR (co.course_code = 'CSE304' AND co.section = '00')
  )
  AND (COALESCE(s.midterm_percentage, 0) + COALESCE(s.final_exam_percentage, 0)) >= 70
ORDER BY co.course_code, co.section;
```

### J081 — 실행 진단 correct
질문: 2026학년도 1학기 소프트웨어융합학과 원천 개설목록에서 전공필수로 분류된 강좌의 분반 수와 개설학점 합계를 알려줘. 분반별로 각각 계산해줘.

- 판정 이유: 동일 강좌에 분류 행이 여러 개면 모델은 학점을 중복 합산하지만 정답은 강좌별로 중복 제거한다.

정답 SQL:
```sql
SELECT COUNT(*) AS offering_count,COALESCE(SUM(z.credits),0) AS offering_credit_sum FROM (SELECT DISTINCT o.offering_id,o.credits FROM course_offerings o JOIN course_offering_categories oc ON oc.offering_id=o.offering_id JOIN departments d ON d.department_id=oc.department_id JOIN course_categories cc ON cc.category_id=oc.category_id WHERE o.year=2026 AND o.semester='1' AND o.campus='국제' AND d.code='A07337' AND cc.category_code='04') z;
```
모델 SQL:
```sql
SELECT
    COUNT(DISTINCT co.offering_id) AS offering_count,
    COALESCE(SUM(co.credits), 0) AS total_credits
FROM course_offerings co
JOIN course_offering_categories coc ON co.offering_id = coc.offering_id
JOIN departments d ON coc.department_id = d.department_id
JOIN course_categories cc ON coc.category_id = cc.category_id
WHERE co.year = 2026
  AND co.semester = '1'
  AND d.name = '소프트웨어융합학과'
  AND cc.category_name = '전공필수';
```

### J082 — 실행 진단 correct
질문: 2025학년도 2학기 인공지능학과 원천 개설목록에서 전공필수로 분류된 강좌의 분반 수와 개설학점 합계를 알려줘. 분반별로 각각 계산해줘.

- 판정 이유: 동일 강좌에 해당 분류 매핑이 여러 개면 중복 집계되어 정답의 DISTINCT와 달라진다.

정답 SQL:
```sql
SELECT COUNT(*) AS offering_count,COALESCE(SUM(z.credits),0) AS offering_credit_sum FROM (SELECT DISTINCT o.offering_id,o.credits FROM course_offerings o JOIN course_offering_categories oc ON oc.offering_id=o.offering_id JOIN departments d ON d.department_id=oc.department_id JOIN course_categories cc ON cc.category_id=oc.category_id WHERE o.year=2025 AND o.semester='2' AND o.campus='국제' AND d.code='A10628' AND cc.category_code='04') z;
```
모델 SQL:
```sql
SELECT COUNT(co.offering_id) AS offering_count, COALESCE(SUM(co.credits), 0) AS total_credits
FROM course_offerings co
JOIN course_offering_categories coc ON co.offering_id = coc.offering_id
JOIN departments d ON coc.department_id = d.department_id
JOIN course_categories cc ON coc.category_id = cc.category_id
WHERE co.year = 2025
  AND co.semester = '2'
  AND d.name = '인공지능학과'
  AND cc.category_name = '전공필수';
```

### J083 — 실행 진단 correct
질문: 2025학년도 2학기 소프트웨어융합학과 원천 개설목록에서 전공필수로 분류된 강좌의 분반 수와 개설학점 합계를 알려줘. 분반별로 각각 계산해줘.

- 판정 이유: 동일 강좌에 분류 행이 여러 개면 모델은 학점을 중복 합산하지만 정답은 강좌별로 중복을 제거한다.

정답 SQL:
```sql
SELECT COUNT(*) AS offering_count,COALESCE(SUM(z.credits),0) AS offering_credit_sum FROM (SELECT DISTINCT o.offering_id,o.credits FROM course_offerings o JOIN course_offering_categories oc ON oc.offering_id=o.offering_id JOIN departments d ON d.department_id=oc.department_id JOIN course_categories cc ON cc.category_id=oc.category_id WHERE o.year=2025 AND o.semester='2' AND o.campus='국제' AND d.code='A07337' AND cc.category_code='04') z;
```
모델 SQL:
```sql
SELECT
    COUNT(DISTINCT co.offering_id) AS offering_count,
    COALESCE(SUM(co.credits), 0) AS total_credits
FROM course_offerings co
JOIN course_offering_categories coc ON co.offering_id = coc.offering_id
JOIN departments d ON coc.department_id = d.department_id
JOIN course_categories cc ON coc.category_id = cc.category_id
WHERE co.year = 2025
  AND co.semester = '2'
  AND d.name = '소프트웨어융합학과'
  AND cc.category_name = '전공필수';
```

### J084 — 실행 진단 correct
질문: 2025학년도 1학기 컴퓨터공학과 원천 개설목록에서 전공필수로 분류된 강좌의 분반 수와 개설학점 합계를 알려줘. 분반별로 각각 계산해줘.

- 판정 이유: 분반별 강좌를 세어야 하나 DISTINCT가 없어 한 강좌에 여러 분류 행이 있으면 중복 집계된다.

정답 SQL:
```sql
SELECT COUNT(*) AS offering_count,COALESCE(SUM(z.credits),0) AS offering_credit_sum FROM (SELECT DISTINCT o.offering_id,o.credits FROM course_offerings o JOIN course_offering_categories oc ON oc.offering_id=o.offering_id JOIN departments d ON d.department_id=oc.department_id JOIN course_categories cc ON cc.category_id=oc.category_id WHERE o.year=2025 AND o.semester='1' AND o.campus='국제' AND d.code='A10627' AND cc.category_code='04') z;
```
모델 SQL:
```sql
SELECT
    COUNT(*) AS offering_count,
    COALESCE(SUM(co.credits), 0) AS total_credits
FROM course_offerings AS co
JOIN course_offering_categories AS coc
    ON coc.offering_id = co.offering_id
JOIN departments AS d
    ON d.department_id = coc.department_id
JOIN course_categories AS cc
    ON cc.category_id = coc.category_id
WHERE co.year = 2025
  AND co.semester = '1'
  AND d.name = '컴퓨터공학과'
  AND cc.category_name = '전공필수';
```

### J096 — 실행 진단 correct
질문: 2024학번 일반 신입학생의 후마니타스 기본구조표에서 총 교양학점, 배분이수 학점, 최소 영역 수, 영역당 학점은 각각 얼마야? 면제·대체·편입 예외는 제외해줘.

- 판정 이유: 모델은 cohort_end가 NULL인 범위까지 포함해 정답보다 다른 행을 조회할 수 있다.

정답 SQL:
```sql
SELECT gr.total_general_credits,rc.min_credits AS distribution_credits,rc.min_areas,rc.per_area_min_credits FROM general_education_requirements gr JOIN general_education_requirement_categories rc ON rc.general_requirement_id=gr.general_requirement_id WHERE 2024 BETWEEN gr.cohort_start AND gr.cohort_end AND rc.requirement_code='DISTRIBUTION';
```
모델 SQL:
```sql
SELECT
    ger.total_general_credits,
    gerc.min_credits,
    gerc.min_areas,
    gerc.per_area_min_credits
FROM general_education_requirements ger
JOIN general_education_requirement_categories gerc
    ON ger.general_requirement_id = gerc.general_requirement_id
WHERE ger.cohort_start <= 2024
  AND (ger.cohort_end IS NULL OR ger.cohort_end >= 2024)
  AND gerc.requirement_code = 'DISTRIBUTION'
```


## 결과는 틀렸지만 논리는 같다고 판정 — judge 오판인지 확인 (1개)

### J020 — 실행 진단 correct_extra_columns
질문: 2026학년도 1학기 IE215-00(데이터사이언스) 담당 교수의 같은 학기 소프트웨어융합학과 개설목록 내 다른 3학점 강좌 중, 중간·기말 비율이 모두 기재된 강좌끼리 비교하면 시험 비율 합계가 가장 낮은 강좌는? 과목코드·분반·합계를 알려주고 동률은 모두 포함해줘. 기준 과목 코드는 제외해줘.

- 판정 이유: 고정 캠퍼스 조건을 제외하면 대상 교수·학기·학과·학점·시험비율 조건과 최솟값 동률 처리가 정답과 같다.

정답 SQL:
```sql
WITH anchor_prof AS (SELECT DISTINCT op.professor_id FROM course_offerings o JOIN offering_professors op ON op.offering_id=o.offering_id WHERE o.year=2026 AND o.semester='1' AND o.course_code='IE215' AND o.section='00' AND o.campus='국제'), candidates AS (SELECT DISTINCT o.course_code,o.section,s.midterm_percentage+s.final_exam_percentage AS exam_total_percentage FROM course_offerings o JOIN offering_professors op ON op.offering_id=o.offering_id JOIN anchor_prof ap ON ap.professor_id=op.professor_id JOIN course_offering_categories oc ON oc.offering_id=o.offering_id JOIN departments d ON d.department_id=oc.department_id JOIN course_categories cc ON cc.category_id=oc.category_id JOIN syllabi s ON s.offering_id=o.offering_id WHERE o.year=2026 AND o.semester='1' AND o.campus='국제' AND d.code='A07337' AND o.course_code<>'IE215' AND o.credits=3 AND s.midterm_percentage IS NOT NULL AND s.final_exam_percentage IS NOT NULL) SELECT course_code,section,exam_total_percentage FROM candidates WHERE exam_total_percentage=(SELECT MIN(exam_total_percentage) FROM candidates) ORDER BY course_code,section;
```
모델 SQL:
```sql
WITH target_prof AS (
  SELECT DISTINCT op.professor_id
  FROM course_offerings co
  JOIN offering_professors op ON co.offering_id = op.offering_id
  WHERE co.year = 2026
    AND co.semester = '1'
    AND co.course_code = 'IE215'
    AND co.section = '00'
),
candidate_offerings AS (
  SELECT DISTINCT
    co.offering_id,
    co.course_code,
    co.section,
    co.course_name,
    s.midterm_percentage,
    s.final_exam_percentage,
    (s.midterm_percentage + s.final_exam_percentage) AS exam_total_percentage
  FROM course_offerings co
  JOIN offering_professors op ON co.offering_id = op.offering_id
  JOIN target_prof tp ON op.professor_id = tp.professor_id
  JOIN course_offering_categories coc ON co.offering_id = coc.offering_id
  JOIN departments d ON coc.department_id = d.department_id
  JOIN syllabi s ON co.offering_id = s.offering_id
  WHERE co.year = 2026
    AND co.semester = '1'
    AND d.name = '소프트웨어융합학과'
    AND co.credits = 3
    AND co.course_code <> 'IE215'
    AND s.midterm_percentage IS NOT NULL
    AND s.final_exam_percentage IS NOT NULL
)
SELECT
  course_code,
  section,
  course_name,
  midterm_percentage,
  final_exam_percentage,
  exam_total_percentage
FROM candidate_offerings
WHERE exam_total_percentage = (
  SELECT MIN(exam_total_percentage)
  FROM candidate_offerings
)
ORDER BY course_code, section;
```

