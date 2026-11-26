# Text2SQL 평가 결과 (2026-11-05 09:02)

| 지표 | 값 |
|---|---|
| 평가 문항 수 | 15 |
| 실행 성공률(최종) | 15/15 (100.0%) |
| 실행 성공률(1차 시도) | 15/15 (100.0%) |
| 정답률 strict | 10/15 (66.7%) |
| 정답률 relaxed | 11/15 (73.3%) |
| 정답률 subset (정답 일부 컬럼 누락 허용) | 11/15 (73.3%) |
| 평균 토큰 | 4282.3 |
| 평균 응답시간(초) | 7.83 |

## 유형별

| 태그 | n | strict | relaxed | subset | 실행 성공 |
|---|---|---|---|---|---|
| arithmetic_reasoning | 1 | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) |
| assignment_gap | 1 | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) |
| classification_aggregation | 1 | 0/1 (0.0%) | 0/1 (0.0%) | 0/1 (0.0%) | 1/1 (100.0%) |
| cross_rule_reasoning | 1 | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) |
| department_required_load | 1 | 0/1 (0.0%) | 0/1 (0.0%) | 0/1 (0.0%) | 1/1 (100.0%) |
| distribution_rule_application | 1 | 0/1 (0.0%) | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) |
| exam_change | 1 | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) |
| fixture_earned | 1 | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) |
| fixture_personalized | 1 | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) |
| general_cohort_difference | 1 | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) |
| general_cohort_rule | 1 | 0/1 (0.0%) | 0/1 (0.0%) | 0/1 (0.0%) | 1/1 (100.0%) |
| multi_document_multi_hop | 1 | 0/1 (0.0%) | 0/1 (0.0%) | 0/1 (0.0%) | 1/1 (100.0%) |
| multi_document_multi_hop_reasoning | 1 | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) |
| multi_document_reasoning | 2 | 2/2 (100.0%) | 2/2 (100.0%) | 2/2 (100.0%) | 2/2 (100.0%) |
| multi_hop | 2 | 2/2 (100.0%) | 2/2 (100.0%) | 2/2 (100.0%) | 2/2 (100.0%) |
| multi_hop_aggregation | 1 | 0/1 (0.0%) | 0/1 (0.0%) | 0/1 (0.0%) | 1/1 (100.0%) |
| official_public_facts | 12 | 8/12 (66.7%) | 8/12 (66.7%) | 8/12 (66.7%) | 12/12 (100.0%) |
| official_rule | 1 | 0/1 (0.0%) | 0/1 (0.0%) | 0/1 (0.0%) | 1/1 (100.0%) |
| official_rule_with_hypothetical_inputs | 2 | 1/2 (50.0%) | 2/2 (100.0%) | 2/2 (100.0%) | 2/2 (100.0%) |
| prof_credit_load | 1 | 0/1 (0.0%) | 0/1 (0.0%) | 0/1 (0.0%) | 1/1 (100.0%) |
| prof_future_other | 1 | 0/1 (0.0%) | 0/1 (0.0%) | 0/1 (0.0%) | 1/1 (100.0%) |
| prof_other_industry | 1 | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) |
| professor_assessment_filter | 1 | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) |
| professor_required_credit_chain | 1 | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) |
| rule_reasoning | 1 | 0/1 (0.0%) | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) |
| schedule_overlap | 1 | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) |
| simulated_student_fixture | 1 | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) |
| single_document | 1 | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) |
| teacher_credits | 1 | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) |
| temporal_reasoning | 1 | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) |
| weighted_exam_score | 1 | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) |

## 진단 분포

| 진단 | 개수 |
|---|---|
| correct | 10 |
| row_count_mismatch | 3 |
| value_mismatch | 1 |
| correct_extra_columns | 1 |

## 정답 재검토가 필요한 문항

- J001 (O): 2026학년도 2학기 SWCON331-00(로봇프로그래밍) 담당 교수의 다른 수업 중, 같은 학기 소프트웨어융합학과 기준 전공필수이면서 3학점인 강좌가 있어? 해당 과목코드·분반·학점을 모두 알려줘. 기준 과목의 다른 분반도 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J045 (O): 2026학년도 1학기 IE419-00(서비스데이터사이언스) 담당 교수의 다른 수업 중, 같은 학기 소프트웨어융합학과 개설목록에서 산학필수인 강좌의 과목코드와 분반을 알려줘. 기준 과목의 다른 분반도 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J005 (O): 2026학년도 2학기 SWCON331-00(로봇프로그래밍) 담당 교수의 같은 학기 다른 수업 중 소프트웨어융합학과 기준 전공필수이고, 공식 강의계획서에 과제 반영 비율이 30% 이상으로 기재된 강좌의 과목코드·분반·과제 비율을 알려줘. 기준 과목의 다른 분반도 제외하고, 미기재 비율은 0으로 보지 마. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J009 (O): 2026학년도 2학기 EE209-02(논리회로)의 담당 교수 이름과 학점을 알려줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J021 (O): 2025학년도 1학기 CSE406-01(캡스톤디자인)와 2026학년도 1학기 CSE406-01(캡스톤디자인)의 기말고사 비율을 순서대로 알려주고, 두 번째에서 첫 번째를 뺀 차이를 퍼센트포인트로 계산해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J025 (O): 2025학년도 1학기 CSE406-01(캡스톤디자인)와 2026학년도 1학기 AI4003-00(졸업논문(인공지능))의 과제보고서 비율을 순서대로 알려주고, 두 번째에서 첫 번째를 뺀 차이를 퍼센트포인트로 계산해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J059 (X): 2026학년도 1학기 AI4003-00(졸업논문(인공지능)) 담당 교수가 같은 학기 인공지능학과 개설목록에서 맡은 다른 과목의 분반 수와 개설학점 합계를 알려줘. 기준 과목 코드는 제외하고, 다른 분반은 각각 합산해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J064 (X): 2025학년도 2학기 CSE497-02(연구연수활동2(컴퓨터공학))의 담당 교수가 2026학년도 2학기 컴퓨터공학과 개설목록에서 맡은 다른 과목의 코드와 분반을 알려줘. 기준 과목 코드는 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J069 (O): 2026학년도 1학기 IE419-00(서비스데이터사이언스)와 2026학년도 1학기 SWCON104-01(웹/파이선프로그래밍)의 정규 수업시간이 일주일에 총 몇 분 겹쳐? 시험 일정은 제외하고 요일별 겹치는 구간만 합산해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J082 (X): 2025학년도 2학기 인공지능학과 원천 개설목록에서 전공필수로 분류된 강좌의 분반 수와 개설학점 합계를 알려줘. 분반별로 각각 계산해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J085 (O): 2025학년도 2학기 CSE406-01(캡스톤디자인)에서 중간고사 80점, 기말고사 90점(각 100점 만점)을 받았다고 가정하면 두 시험이 최종 100점에 기여하는 점수 합은? 다른 항목과 추가 보정은 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J089 (O): [가상 학생 202210001] 내 가상 수강이력에서 완료됐고 재수강으로 대체되지 않은 기록의 학점 합계는 얼마야? — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J095 (X): 2023학번 일반 신입학생의 후마니타스 기본구조표에서 총 교양학점, 배분이수 학점, 최소 영역 수, 영역당 학점은 각각 얼마야? 면제·대체·편입 예외는 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J097 (O): 2023학번과 2024학번 기본구조표를 비교하면 2024학번의 총 교양 최소학점과 배분이수 최소학점은 각각 몇 학점 줄었어? 면제·대체 예외는 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J098 (X): 2024학번 일반 신입학생이 배분이수 6학점을 취득했고, 영역당 3학점 기준을 채운 영역은 2개라고 가정하자. 기본구조표 기준 부족 학점·부족 영역 수와 두 조건 충족 여부(1/0)는? 편입·면제 예외는 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.

## 오답 목록

### J059 — row_count_mismatch
질문: 2026학년도 1학기 AI4003-00(졸업논문(인공지능)) 담당 교수가 같은 학기 인공지능학과 개설목록에서 맡은 다른 과목의 분반 수와 개설학점 합계를 알려줘. 기준 과목 코드는 제외하고, 다른 분반은 각각 합산해줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
WITH base_professors AS (
    SELECT DISTINCT op.professor_id
    FROM course_offerings AS base
    JOIN offering_professors AS op
      ON op.offering_id = base.offering_id
    WHERE base.course_code = 'AI4003'
      AND base.section = '00'
      AND base.year = 2026
      AND base.semester = '1'
)
SELECT
    c.course_code,
    co.course_name,
    COUNT(DISTINCT co.offering_id) AS section_count,
    SUM(co.credits) AS total_credits
FROM course_offerings AS co
JOIN courses AS c
  ON c.course_code = co.course_code
WHERE co.year = 2026
  AND co.semester = '1'
  AND c.department_id = 12
  AND co.course_code <> 'AI4003'
  AND EXISTS (
      SELECT 1
      FROM offering_professors AS op
      JOIN base_professors AS bp
        ON bp.professor_id = op.professor_id
      WHERE op.offering_id = co.offering_id
  )
GROUP BY c.course_code, co.course_name
```
정답 컬럼: offering_count, offering_credit_sum / 예측 컬럼: course_code, course_name, section_count, total_credits
정답 행 수: 1 / 예측 행 수: 2

### J064 — row_count_mismatch
질문: 2025학년도 2학기 CSE497-02(연구연수활동2(컴퓨터공학))의 담당 교수가 2026학년도 2학기 컴퓨터공학과 개설목록에서 맡은 다른 과목의 코드와 분반을 알려줘. 기준 과목 코드는 제외해줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
WITH target_professors AS (
    SELECT op.professor_id
    FROM course_offerings AS base
    JOIN offering_professors AS op
      ON op.offering_id = base.offering_id
    WHERE base.course_code = 'CSE497'
      AND base.section = '02'
      AND base.year = 2025
      AND base.semester = '2'
)
SELECT DISTINCT target.course_code, target.section
FROM course_offerings AS target
JOIN courses AS c
  ON c.course_code = target.course_code
JOIN departments AS d
  ON d.department_id = c.department_id
JOIN offering_professors AS op
  ON op.offering_id = target.offering_id
WHERE target.year = 2026
  AND target.semester = '2'
  AND d.name = '컴퓨터공학과'
  AND target.course_code <> 'CSE497'
  AND op.professor_id IN (SELECT professor_id FROM target_professors);
```
정답 컬럼: course_code, section / 예측 컬럼: course_code, section
정답 행 수: 4 / 예측 행 수: 3

### J082 — value_mismatch
질문: 2025학년도 2학기 인공지능학과 원천 개설목록에서 전공필수로 분류된 강좌의 분반 수와 개설학점 합계를 알려줘. 분반별로 각각 계산해줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
WITH qualifying_offerings AS (
    SELECT DISTINCT co.offering_id, co.credits
    FROM course_offerings AS co
    JOIN courses AS c
      ON c.course_code = co.course_code
    WHERE c.department_id = 12
      AND co.year = 2025
      AND co.semester = '2'
      AND EXISTS (
          SELECT 1
          FROM course_offering_categories AS coc
          JOIN course_categories AS cc
            ON cc.category_id = coc.category_id
          WHERE coc.offering_id = co.offering_id
            AND cc.category_name = '전공필수'
      )
)
SELECT COUNT(*) AS 분반수,
       COALESCE(SUM(credits), 0) AS 개설학점합계
FROM qualifying_offerings;
```
정답 컬럼: offering_count, offering_credit_sum / 예측 컬럼: 분반수, 개설학점합계
정답 행 수: 1 / 예측 행 수: 1

### J095 — row_count_mismatch
질문: 2023학번 일반 신입학생의 후마니타스 기본구조표에서 총 교양학점, 배분이수 학점, 최소 영역 수, 영역당 학점은 각각 얼마야? 면제·대체·편입 예외는 제외해줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
SELECT
    ger.total_general_credits AS total_general_credits,
    gerc.min_credits AS distribution_credits,
    gerc.min_areas AS minimum_areas,
    gerc.per_area_min_credits AS credits_per_area
FROM general_education_requirements AS ger
JOIN general_education_requirement_categories AS gerc
    ON gerc.general_requirement_id = ger.general_requirement_id
WHERE ger.cohort_start <= 2023
  AND (ger.cohort_end IS NULL OR ger.cohort_end >= 2023)
  AND ger.source_document LIKE '%후마니타스%'
  AND gerc.requirement_code = 'DISTRIBUTION';
```
정답 컬럼: total_general_credits, distribution_credits, min_areas, per_area_min_credits / 예측 컬럼: total_general_credits, distribution_credits, minimum_areas, credits_per_area
정답 행 수: 1 / 예측 행 수: 0

### J098 — correct_extra_columns
질문: 2024학번 일반 신입학생이 배분이수 6학점을 취득했고, 영역당 3학점 기준을 채운 영역은 2개라고 가정하자. 기본구조표 기준 부족 학점·부족 영역 수와 두 조건 충족 여부(1/0)는? 편입·면제 예외는 제외해줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
SELECT
    MAX(gc.min_credits - 6, 0) AS "부족_학점",
    MAX(COALESCE(gc.min_areas, 0) - 2, 0) AS "부족_영역_수",
    CASE WHEN 6 >= gc.min_credits THEN 1 ELSE 0 END AS "최소학점_충족",
    CASE WHEN gc.min_areas IS NULL OR 2 >= gc.min_areas THEN 1 ELSE 0 END AS "최소영역_충족"
FROM general_education_requirements AS gr
JOIN general_education_requirement_categories AS gc
    ON gc.general_requirement_id = gr.general_requirement_id
WHERE gr.cohort_start <= 2024
  AND (gr.cohort_end IS NULL OR gr.cohort_end >= 2024)
  AND gc.requirement_code = 'DISTRIBUTION';
```
정답 컬럼: remaining_credits, remaining_areas, meets_both / 예측 컬럼: 부족_학점, 부족_영역_수, 최소학점_충족, 최소영역_충족
정답 행 수: 1 / 예측 행 수: 1


## 진단 코드 설명

- correct: 결과 완전 일치 / correct_extra_columns: 컬럼이 더 있거나 컬럼 순서가 다름(relaxed 정답)
- missing_columns: 예측 값은 모두 맞지만 정답의 일부 컬럼이 빠짐(subset 정답, 사람이 확인)
- order_mismatch: 행 정렬만 다름(relaxed 정답) / row_count_mismatch: 행 수가 다름 / value_mismatch: 행 수는 같지만 값이 다름
- exec_fail:sqlite 실행 오류 / exec_fail:guard 안전장치에 의해 거부 / exec_fail:no_sql SQL 추출 실패
- exec_fail:timeout 시간 초과 / exec_fail:refused 거부하면 안 되는 질문을 거부
- correct_refusal: 거부가 정답인 문항을 거부·차단 / no_leak_but_not_refused: 거부는 안 했지만 결과 0행
- should_have_refused: 거부해야 하는데 결과를 돌려줌 / api_error ChatKHU 호출 실패 / gold_invalid 정답 SQL 문제
