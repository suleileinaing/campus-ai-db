# SQL 논리 LLM 채점 (2026-11-20 13:13)

judge 모델: `gpt-5.6-luna` / judge 토큰 합계: 24745

통과 기준: 정답 SQL 과 논리가 같음 + 질문에 없는 조건 없음 + 본인 학번 범위 지킴

| 지표 | 값 |
|---|---|
| SQL 논리 통과율 | 8/15 (53.3%) |
| 논리 일치 | 8/15 (53.3%) |
| (참고) 실행 결과 정답률 strict | 11/15 (73.3%) |
| 결과는 맞았지만 논리가 틀림(우연히 맞음) | 4 |
| 질문에 없는 조건 추가 | 0 |
| 본인 학번 범위 위반 | 0 |

## 유형별

| 태그 | n | 통과 | 논리 일치 | 실행 strict | 우연히 맞음 |
|---|---|---|---|---|---|
| arithmetic_reasoning | 1 | 0/1 (0.0%) | 0/1 (0.0%) | 0/1 (0.0%) | 0 |
| assignment_gap | 1 | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) | 0 |
| classification_aggregation | 1 | 0/1 (0.0%) | 0/1 (0.0%) | 1/1 (100.0%) | 1 |
| cross_rule_reasoning | 1 | 0/1 (0.0%) | 0/1 (0.0%) | 0/1 (0.0%) | 0 |
| department_required_load | 1 | 0/1 (0.0%) | 0/1 (0.0%) | 1/1 (100.0%) | 1 |
| distribution_rule_application | 1 | 0/1 (0.0%) | 0/1 (0.0%) | 0/1 (0.0%) | 0 |
| exam_change | 1 | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) | 0 |
| fixture_earned | 1 | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) | 0 |
| fixture_personalized | 1 | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) | 0 |
| general_cohort_difference | 1 | 0/1 (0.0%) | 0/1 (0.0%) | 0/1 (0.0%) | 0 |
| general_cohort_rule | 1 | 0/1 (0.0%) | 0/1 (0.0%) | 1/1 (100.0%) | 1 |
| multi_document_multi_hop | 1 | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) | 0 |
| multi_document_multi_hop_reasoning | 1 | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) | 0 |
| multi_document_reasoning | 2 | 2/2 (100.0%) | 2/2 (100.0%) | 2/2 (100.0%) | 0 |
| multi_hop | 2 | 2/2 (100.0%) | 2/2 (100.0%) | 1/2 (50.0%) | 0 |
| multi_hop_aggregation | 1 | 0/1 (0.0%) | 0/1 (0.0%) | 1/1 (100.0%) | 1 |
| official_public_facts | 12 | 7/12 (58.3%) | 7/12 (58.3%) | 10/12 (83.3%) | 4 |
| official_rule | 1 | 0/1 (0.0%) | 0/1 (0.0%) | 1/1 (100.0%) | 1 |
| official_rule_with_hypothetical_inputs | 2 | 0/2 (0.0%) | 0/2 (0.0%) | 0/2 (0.0%) | 0 |
| prof_credit_load | 1 | 0/1 (0.0%) | 0/1 (0.0%) | 1/1 (100.0%) | 1 |
| prof_future_other | 1 | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) | 0 |
| prof_other_industry | 1 | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) | 0 |
| professor_assessment_filter | 1 | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) | 0 |
| professor_required_credit_chain | 1 | 1/1 (100.0%) | 1/1 (100.0%) | 0/1 (0.0%) | 0 |
| rule_reasoning | 1 | 0/1 (0.0%) | 0/1 (0.0%) | 0/1 (0.0%) | 0 |
| schedule_overlap | 1 | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) | 0 |
| simulated_student_fixture | 1 | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) | 0 |
| single_document | 1 | 0/1 (0.0%) | 0/1 (0.0%) | 1/1 (100.0%) | 1 |
| teacher_credits | 1 | 0/1 (0.0%) | 0/1 (0.0%) | 1/1 (100.0%) | 1 |
| temporal_reasoning | 1 | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) | 0 |
| weighted_exam_score | 1 | 0/1 (0.0%) | 0/1 (0.0%) | 0/1 (0.0%) | 0 |

## 결과는 맞았지만 논리가 틀림 — 실행 비교가 놓친 오답 (4개)

### J009 — 실행 진단 correct
질문: 2026학년도 2학기 EE209-02(논리회로)의 담당 교수 이름과 학점을 알려줘.

- 판정 이유: LEFT JOIN으로 담당 교수가 없는 강의도 반환하고 DISTINCT가 없어 정답과 논리적으로 다를 수 있다.

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

### J059 — 실행 진단 correct
질문: 2026학년도 1학기 AI4003-00(졸업논문(인공지능)) 담당 교수가 같은 학기 인공지능학과 개설목록에서 맡은 다른 과목의 분반 수와 개설학점 합계를 알려줘. 기준 과목 코드는 제외하고, 다른 분반은 각각 합산해줘.

- 판정 이유: 과목 소속 학과 조건까지 OR로 포함해 정답의 개설목록 범위보다 넓어질 수 있다.

정답 SQL:
```sql
WITH anchor_prof AS (SELECT DISTINCT op.professor_id FROM course_offerings o JOIN offering_professors op ON op.offering_id=o.offering_id WHERE o.year=2026 AND o.semester='1' AND o.course_code='AI4003' AND o.section='00' AND o.campus='국제') SELECT COUNT(*) AS offering_count,COALESCE(SUM(z.credits),0) AS offering_credit_sum FROM (SELECT DISTINCT o.offering_id,o.credits FROM course_offerings o JOIN offering_professors op ON op.offering_id=o.offering_id JOIN anchor_prof ap ON ap.professor_id=op.professor_id JOIN course_offering_categories oc ON oc.offering_id=o.offering_id JOIN departments d ON d.department_id=oc.department_id JOIN course_categories cc ON cc.category_id=oc.category_id WHERE o.year=2026 AND o.semester='1' AND o.campus='국제' AND d.code='A10628' AND o.course_code<>'AI4003' AND (1=1)) z;
```
모델 SQL:
```sql
WITH target_professors AS (
    SELECT DISTINCT op.professor_id
    FROM course_offerings co
    JOIN offering_professors op ON co.offering_id = op.offering_id
    WHERE co.year = 2026
      AND co.semester = '1'
      AND co.course_code = 'AI4003'
      AND co.section = '00'
),
ai_offerings AS (
    SELECT DISTINCT co.offering_id, co.credits
    FROM course_offerings co
    JOIN offering_professors op ON co.offering_id = op.offering_id
    JOIN target_professors tp ON op.professor_id = tp.professor_id
    LEFT JOIN courses c ON co.course_code = c.course_code
    LEFT JOIN departments cd ON c.department_id = cd.department_id
    LEFT JOIN course_offering_categories coc ON co.offering_id = coc.offering_id
    LEFT JOIN departments ocd ON coc.department_id = ocd.department_id
    WHERE co.year = 2026
      AND co.semester = '1'
      AND co.course_code != 'AI4003'
      AND (cd.name = '인공지능학과' OR ocd.name = '인공지능학과')
)
SELECT COUNT(offering_id) AS section_count,
       COALESCE(SUM(credits), 0) AS total_credits
FROM ai_offerings;
```

### J082 — 실행 진단 correct
질문: 2025학년도 2학기 인공지능학과 원천 개설목록에서 전공필수로 분류된 강좌의 분반 수와 개설학점 합계를 알려줘. 분반별로 각각 계산해줘.

- 판정 이유: 동일 강좌에 분류 행이 여러 개면 SUM이 학점을 중복 합산해 정답과 다를 수 있다.

정답 SQL:
```sql
SELECT COUNT(*) AS offering_count,COALESCE(SUM(z.credits),0) AS offering_credit_sum FROM (SELECT DISTINCT o.offering_id,o.credits FROM course_offerings o JOIN course_offering_categories oc ON oc.offering_id=o.offering_id JOIN departments d ON d.department_id=oc.department_id JOIN course_categories cc ON cc.category_id=oc.category_id WHERE o.year=2025 AND o.semester='2' AND o.campus='국제' AND d.code='A10628' AND cc.category_code='04') z;
```
모델 SQL:
```sql
SELECT
  COUNT(DISTINCT co.offering_id) AS offering_count,
  COALESCE(SUM(co.credits), 0) AS total_credits
FROM course_offerings AS co
JOIN course_offering_categories AS coc
  ON co.offering_id = coc.offering_id
JOIN departments AS d
  ON coc.department_id = d.department_id
JOIN course_categories AS cc
  ON coc.category_id = cc.category_id
WHERE
  co.year = 2025
  AND co.semester = '2'
  AND d.name = '인공지능학과'
  AND cc.category_name = '전공필수';
```

### J095 — 실행 진단 correct
질문: 2023학번 일반 신입학생의 후마니타스 기본구조표에서 총 교양학점, 배분이수 학점, 최소 영역 수, 영역당 학점은 각각 얼마야? 면제·대체·편입 예외는 제외해줘.

- 판정 이유: 모델은 cohort_end가 NULL인 적용 범위도 포함해 정답의 BETWEEN 조건과 결과가 달라질 수 있다.

정답 SQL:
```sql
SELECT gr.total_general_credits,rc.min_credits AS distribution_credits,rc.min_areas,rc.per_area_min_credits FROM general_education_requirements gr JOIN general_education_requirement_categories rc ON rc.general_requirement_id=gr.general_requirement_id WHERE 2023 BETWEEN gr.cohort_start AND gr.cohort_end AND rc.requirement_code='DISTRIBUTION';
```
모델 SQL:
```sql
SELECT
    ger.total_general_credits,
    gerc.min_credits,
    gerc.min_areas,
    gerc.per_area_min_credits
FROM general_education_requirements AS ger
JOIN general_education_requirement_categories AS gerc
    ON ger.general_requirement_id = gerc.general_requirement_id
WHERE ger.cohort_start <= 2023
  AND (ger.cohort_end IS NULL OR ger.cohort_end >= 2023)
  AND gerc.requirement_code = 'DISTRIBUTION';
```


## 결과는 틀렸지만 논리는 같다고 판정 — judge 오판인지 확인 (1개)

### J001 — 실행 진단 correct_extra_columns
질문: 2026학년도 2학기 SWCON331-00(로봇프로그래밍) 담당 교수의 다른 수업 중, 같은 학기 소프트웨어융합학과 기준 전공필수이면서 3학점인 강좌가 있어? 해당 과목코드·분반·학점을 모두 알려줘. 기준 과목의 다른 분반도 제외해줘.

- 판정 이유: 기준 강좌 담당 교수의 동일 학기 강좌를 전공필수·3학점으로 정확히 제한했으며 추가 조건이 없다.

정답 SQL:
```sql
WITH anchor_prof AS (SELECT DISTINCT op.professor_id FROM course_offerings o JOIN offering_professors op ON op.offering_id=o.offering_id WHERE o.year=2026 AND o.semester='2' AND o.course_code='SWCON331' AND o.section='00' AND o.campus='국제') SELECT DISTINCT o.course_code,o.section,o.credits FROM course_offerings o JOIN offering_professors op ON op.offering_id=o.offering_id JOIN anchor_prof ap ON ap.professor_id=op.professor_id JOIN course_offering_categories oc ON oc.offering_id=o.offering_id JOIN departments d ON d.department_id=oc.department_id JOIN course_categories cc ON cc.category_id=oc.category_id WHERE o.year=2026 AND o.semester='2' AND o.campus='국제' AND d.code='A07337' AND o.course_code<>'SWCON331' AND cc.category_code='04' AND o.credits=3 ORDER BY o.course_code,o.section;
```
모델 SQL:
```sql
SELECT DISTINCT
    co.course_code,
    co.course_name,
    co.section,
    co.credits
FROM course_offerings AS co
JOIN offering_professors AS op
    ON co.offering_id = op.offering_id
JOIN course_offering_categories AS coc
    ON co.offering_id = coc.offering_id
JOIN departments AS d
    ON coc.department_id = d.department_id
JOIN course_categories AS cc
    ON coc.category_id = cc.category_id
WHERE co.year = 2026
  AND co.semester = '2'
  AND co.credits = 3
  AND co.course_code <> 'SWCON331'
  AND d.name = '소프트웨어융합학과'
  AND cc.category_name = '전공필수'
  AND op.professor_id IN (
      SELECT op_ref.professor_id
      FROM course_offerings AS co_ref
      JOIN offering_professors AS op_ref
          ON co_ref.offering_id = op_ref.offering_id
      WHERE co_ref.year = 2026
        AND co_ref.semester = '2'
        AND co_ref.course_code = 'SWCON331'
        AND co_ref.section = '00'
  )
ORDER BY co.course_code, co.section;
```

