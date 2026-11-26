# Text2SQL 평가 결과 (2026-11-09 17:23)

| 지표 | 값 |
|---|---|
| 평가 문항 수 | 36 |
| 실행 성공률(최종) | 34/36 (94.4%) |
| 실행 성공률(1차 시도) | 34/36 (94.4%) |
| 정답률 strict | 12/36 (33.3%) |
| 정답률 relaxed | 33/36 (91.7%) |
| 정답률 subset (정답 일부 컬럼 누락 허용) | 33/36 (91.7%) |
| 평균 토큰 | 4681.8 |
| 평균 응답시간(초) | 126.08 |

## 유형별

| 태그 | n | strict | relaxed | subset | 실행 성공 |
|---|---|---|---|---|---|
| answer | 34 | 10/34 (29.4%) | 31/34 (91.2%) | 31/34 (91.2%) | 34/34 (100.0%) |
| clarification_then_reference | 6 | 5/6 (83.3%) | 5/6 (83.3%) | 5/6 (83.3%) | 4/6 (66.7%) |
| clarify | 2 | 2/2 (100.0%) | 2/2 (100.0%) | 2/2 (100.0%) | 0/2 (0.0%) |
| cohort_reference_and_rule_comparison | 6 | 3/6 (50.0%) | 6/6 (100.0%) | 6/6 (100.0%) | 6/6 (100.0%) |
| course_reference_and_arithmetic | 12 | 0/12 (0.0%) | 12/12 (100.0%) | 12/12 (100.0%) | 12/12 (100.0%) |
| professor_reference_and_filter | 12 | 4/12 (33.3%) | 10/12 (83.3%) | 10/12 (83.3%) | 12/12 (100.0%) |
| turn1 | 12 | 5/12 (41.7%) | 12/12 (100.0%) | 12/12 (100.0%) | 10/12 (83.3%) |
| turn2 | 12 | 4/12 (33.3%) | 11/12 (91.7%) | 11/12 (91.7%) | 12/12 (100.0%) |
| turn3 | 12 | 3/12 (25.0%) | 10/12 (83.3%) | 10/12 (83.3%) | 12/12 (100.0%) |

## 진단 분포

| 진단 | 개수 |
|---|---|
| correct_extra_columns | 21 |
| correct | 10 |
| row_count_mismatch | 3 |
| correct_clarify | 2 |

## 정답 재검토가 필요한 문항

- D01-T1 (X): 2025학년도 2학기 SWCON253-01(기계학습) 담당 교수는 누구야? — 2025학년도 2학기 SWCON253-01(기계학습) 담당 교수 이름
- D01-T2 (X): 그 교수님이 같은 학기 컴퓨터공학과 개설목록에서 맡은 다른 과목의 코드와 분반은? 방금 과목 코드는 제외해줘. — 2025-2 컴퓨터공학과에서 김휘용 교수가 맡은 강좌 중 SWCON253를 제외한 과목코드·분반
- D01-T3 (X): 그중 전공필수인 강좌만 과목코드와 분반으로 알려줘. — 2025학년도 2학기 SWCON253-01(기계학습) 담당 교수의 다른 수업 중, 같은 학기 컴퓨터공학과 개설목록에서 전공필수인 강좌의 과목코드와 분반을 알려줘. 기준 과목의 다른 분반도 제외해줘.
- D02-T1 (X): 2026학년도 1학기 CSE304-01(알고리즘) 담당 교수는 누구야? — 2026학년도 1학기 CSE304-01(알고리즘) 담당 교수 이름
- D02-T2 (X): 그 교수님이 같은 학기 컴퓨터공학과 개설목록에서 맡은 다른 과목의 코드와 분반은? 방금 과목 코드는 제외해줘. — 2026-1 컴퓨터공학과에서 성무진 교수가 맡은 강좌 중 CSE304를 제외한 과목코드·분반
- D02-T3 (X): 그중 전공필수인 강좌만 과목코드와 분반으로 알려줘. — 2026학년도 1학기 CSE304-01(알고리즘) 담당 교수의 다른 수업 중, 같은 학기 컴퓨터공학과 개설목록에서 전공필수인 강좌의 과목코드와 분반을 알려줘. 기준 과목의 다른 분반도 제외해줘.
- D03-T1 (O): 2026학년도 1학기 AI4003-00(졸업논문(인공지능)) 담당 교수는 누구야? — 2026학년도 1학기 AI4003-00(졸업논문(인공지능)) 담당 교수 이름
- D03-T2 (X): 그 교수님이 같은 학기 인공지능학과 개설목록에서 맡은 다른 과목의 코드와 분반은? 방금 과목 코드는 제외해줘. — 2026-1 인공지능학과에서 김정욱 교수가 맡은 강좌 중 AI4003를 제외한 과목코드·분반
- D03-T3 (X): 그중 전공필수인 강좌만 과목코드와 분반으로 알려줘. — 2026학년도 1학기 AI4003-00(졸업논문(인공지능)) 담당 교수의 다른 수업 중, 같은 학기 인공지능학과 개설목록에서 전공필수인 강좌의 과목코드와 분반을 알려줘. 기준 과목의 다른 분반도 제외해줘.
- D04-T1 (O): 2026학년도 1학기 CSE423-00(정보보호) 담당 교수는 누구야? — 2026학년도 1학기 CSE423-00(정보보호) 담당 교수 이름
- D04-T2 (O): 그 교수님이 같은 학기 컴퓨터공학과 개설목록에서 맡은 다른 과목의 코드와 분반은? 방금 과목 코드는 제외해줘. — 2026-1 컴퓨터공학과에서 장대희 교수가 맡은 강좌 중 CSE423를 제외한 과목코드·분반
- D04-T3 (O): 그중 전공필수인 강좌만 과목코드와 분반으로 알려줘. — 2026학년도 1학기 CSE423-00(정보보호) 담당 교수의 다른 수업 중, 같은 학기 컴퓨터공학과 개설목록에서 전공필수인 강좌의 과목코드와 분반을 알려줘. 기준 과목의 다른 분반도 제외해줘.
- D05-T1 (X): 2025학년도 1학기 CSE406-01(캡스톤디자인)의 중간·기말고사 비율은 각각 얼마야? — 2025학년도 1학기 CSE406-01(캡스톤디자인) 중간·기말 비율
- D05-T2 (X): 그 두 시험 비율을 합치면 몇 퍼센트야? — 2025학년도 1학기 CSE406-01(캡스톤디자인) 중간·기말 비율 합계
- D05-T3 (X): 그 합계에서 2025학년도 2학기 CSE497-02(연구연수활동2(컴퓨터공학))의 두 시험 비율 합계를 빼면 몇 퍼센트포인트야? — 2025학년도 1학기 CSE406-01(캡스톤디자인) 시험 비율 합계에서 2025학년도 2학기 CSE497-02(연구연수활동2(컴퓨터공학)) 시험 비율 합계를 뺀 차이
- D06-T1 (X): 2026학년도 1학기 AI4003-00(졸업논문(인공지능))의 중간·기말고사 비율은 각각 얼마야? — 2026학년도 1학기 AI4003-00(졸업논문(인공지능)) 중간·기말 비율
- D06-T2 (X): 그 두 시험 비율을 합치면 몇 퍼센트야? — 2026학년도 1학기 AI4003-00(졸업논문(인공지능)) 중간·기말 비율 합계
- D06-T3 (X): 그 합계에서 2026학년도 1학기 EE209-01(논리회로)의 두 시험 비율 합계를 빼면 몇 퍼센트포인트야? — 2026학년도 1학기 AI4003-00(졸업논문(인공지능)) 시험 비율 합계에서 2026학년도 1학기 EE209-01(논리회로) 시험 비율 합계를 뺀 차이
- D07-T1 (X): 2025학년도 1학기 CSE405-00(졸업프로젝트)의 중간·기말고사 비율은 각각 얼마야? — 2025학년도 1학기 CSE405-00(졸업프로젝트) 중간·기말 비율
- D07-T2 (X): 그 두 시험 비율을 합치면 몇 퍼센트야? — 2025학년도 1학기 CSE405-00(졸업프로젝트) 중간·기말 비율 합계
- D07-T3 (X): 그 합계에서 2025학년도 2학기 CSE302-01(컴퓨터네트워크)의 두 시험 비율 합계를 빼면 몇 퍼센트포인트야? — 2025학년도 1학기 CSE405-00(졸업프로젝트) 시험 비율 합계에서 2025학년도 2학기 CSE302-01(컴퓨터네트워크) 시험 비율 합계를 뺀 차이
- D08-T1 (X): 2026학년도 1학기 IE419-00(서비스데이터사이언스)의 중간·기말고사 비율은 각각 얼마야? — 2026학년도 1학기 IE419-00(서비스데이터사이언스) 중간·기말 비율
- D08-T2 (X): 그 두 시험 비율을 합치면 몇 퍼센트야? — 2026학년도 1학기 IE419-00(서비스데이터사이언스) 중간·기말 비율 합계
- D08-T3 (X): 그 합계에서 2026학년도 1학기 SWCON321-02(데이터분석캡스톤디자인)의 두 시험 비율 합계를 빼면 몇 퍼센트포인트야? — 2026학년도 1학기 IE419-00(서비스데이터사이언스) 시험 비율 합계에서 2026학년도 1학기 SWCON321-02(데이터분석캡스톤디자인) 시험 비율 합계를 뺀 차이
- D09-T1 (O): 2023학번의 후마니타스 기본구조표상 총 교양 최소학점은? 면제·대체 예외는 제외해줘. — 2023학번 총 교양 최소학점
- D09-T2 (O): 그럼 2024학번은? — 2024학번의 기본구조표상 총 교양 최소학점, 면제·대체 예외 제외
- D09-T3 (O): 앞의 두 학번을 비교하면 몇 학점 줄어든 거야? — 2023학번 총 교양 최소학점에서 2024학번 총 교양 최소학점을 뺀 학점 차이
- D10-T1 (X): 2023학번의 후마니타스 기본구조표상 배분이수 최소학점은? 면제·대체 예외는 제외해줘. — 2023학번 배분이수 최소학점
- D10-T2 (X): 그럼 2024학번은? — 2024학번의 기본구조표상 배분이수 최소학점, 면제·대체 예외 제외
- D10-T3 (X): 앞의 두 학번을 비교하면 몇 학점 줄어든 거야? — 2023학번 배분이수 최소학점에서 2024학번 배분이수 최소학점을 뺀 학점 차이
- D11-T1 (O): 2026학년도 2학기 독립심화학습(인공지능)2(AI4007)에서 내가 듣는 분반의 교수를 한 명으로 알려줘. 내 분반은 아직 말하지 않았어. — 2026-2 AI4007 수강 분반 미지정
- D11-T2 (O): 08분반이야. — 2026학년도 2학기 AI4007-08(독립심화학습(인공지능)2) 담당 교수 이름
- D11-T3 (X): 그 교수님의 같은 학기 인공지능학과 다른 과목은? AI4007 과목 코드는 제외하고 코드·분반으로 알려줘. — 2026-2 인공지능학과에서 남기빈 교수가 담당하는 AI4007 이외 과목코드·분반
- D12-T1 (O): 2026학년도 2학기 객체지향프로그래밍(CSE103)에서 내가 듣는 분반의 교수를 한 명으로 알려줘. 내 분반은 아직 말하지 않았어. — 2026-2 CSE103 수강 분반 미지정
- D12-T2 (O): 00분반이야. — 2026학년도 2학기 CSE103-00(객체지향프로그래밍) 담당 교수 이름
- D12-T3 (O): 그 교수님의 같은 학기 소프트웨어융합학과 다른 과목은? CSE103 과목 코드는 제외하고 코드·분반으로 알려줘. — 2026-2 소프트웨어융합학과에서 이대호 교수가 담당하는 CSE103 이외 과목코드·분반

## 오답 목록

### D01-T1 — correct_extra_columns
질문: 2025학년도 2학기 SWCON253-01(기계학습) 담당 교수는 누구야?

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
SELECT p.name, p.professor_code, p.email, p.office
FROM course_offerings co
JOIN offering_professors op ON co.offering_id = op.offering_id
JOIN professors p ON op.professor_id = p.professor_id
WHERE co.year = 2025
  AND co.semester = '2'
  AND co.course_code = 'SWCON253'
  AND co.section = '01';
```
정답 컬럼: professor_name / 예측 컬럼: name, professor_code, email, office
정답 행 수: 1 / 예측 행 수: 1

### D01-T2 — correct_extra_columns
질문: 그 교수님이 같은 학기 컴퓨터공학과 개설목록에서 맡은 다른 과목의 코드와 분반은? 방금 과목 코드는 제외해줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
WITH target_professor AS (
    SELECT op.professor_id
    FROM course_offerings co
    JOIN offering_professors op ON co.offering_id = op.offering_id
    WHERE co.year = 2025
      AND co.semester = '2'
      AND co.course_code = 'SWCON253'
      AND co.section = '01'
)
SELECT DISTINCT co.course_code, co.section, co.course_name
FROM course_offerings co
JOIN offering_professors op ON co.offering_id = op.offering_id
JOIN course_offering_categories coc ON co.offering_id = coc.offering_id
JOIN departments d ON coc.department_id = d.department_id
WHERE co.year = 2025
  AND co.semester = '2'
  AND op.professor_id IN (SELECT professor_id FROM target_professor)
  AND d.name = '컴퓨터공학과'
  AND co.course_code != 'SWCON253'
ORDER BY co.course_code, co.section;
```
정답 컬럼: course_code, section / 예측 컬럼: course_code, section, course_name
정답 행 수: 1 / 예측 행 수: 1

### D01-T3 — correct_extra_columns
질문: 그중 전공필수인 강좌만 과목코드와 분반으로 알려줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
WITH target_professor AS (
    SELECT op.professor_id
    FROM course_offerings co
    JOIN offering_professors op ON co.offering_id = op.offering_id
    WHERE co.year = 2025
      AND co.semester = '2'
      AND co.course_code = 'SWCON253'
      AND co.section = '01'
)
SELECT DISTINCT co.course_code, co.section, co.course_name
FROM course_offerings co
JOIN offering_professors op ON co.offering_id = op.offering_id
JOIN course_offering_categories coc ON co.offering_id = coc.offering_id
JOIN departments d ON coc.department_id = d.department_id
JOIN course_categories cc ON coc.category_id = cc.category_id
WHERE co.year = 2025
  AND co.semester = '2'
  AND op.professor_id IN (SELECT professor_id FROM target_professor)
  AND d.name = '컴퓨터공학과'
  AND co.course_code != 'SWCON253'
  AND cc.category_name = '전공필수'
ORDER BY co.course_code, co.section;
```
정답 컬럼: course_code, section / 예측 컬럼: course_code, section, course_name
정답 행 수: 1 / 예측 행 수: 1

### D02-T1 — correct_extra_columns
질문: 2026학년도 1학기 CSE304-01(알고리즘) 담당 교수는 누구야?

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
SELECT p.name, p.email, p.office
FROM course_offerings co
JOIN offering_professors op ON co.offering_id = op.offering_id
JOIN professors p ON op.professor_id = p.professor_id
WHERE co.year = 2026 AND co.semester = '1' AND co.course_code = 'CSE304' AND co.section = '01';
```
정답 컬럼: professor_name / 예측 컬럼: name, email, office
정답 행 수: 1 / 예측 행 수: 1

### D02-T2 — correct_extra_columns
질문: 그 교수님이 같은 학기 컴퓨터공학과 개설목록에서 맡은 다른 과목의 코드와 분반은? 방금 과목 코드는 제외해줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
SELECT DISTINCT co.course_code, co.section, co.course_name
FROM course_offerings co
JOIN offering_professors op ON co.offering_id = op.offering_id
JOIN course_offering_categories coc ON co.offering_id = coc.offering_id
JOIN departments d ON coc.department_id = d.department_id
WHERE co.year = 2026 AND co.semester = '1'
  AND d.name = '컴퓨터공학과'
  AND co.course_code <> 'CSE304'
  AND op.professor_id IN (
      SELECT op2.professor_id
      FROM course_offerings co2
      JOIN offering_professors op2 ON co2.offering_id = op2.offering_id
      WHERE co2.year = 2026 AND co2.semester = '1' AND co2.course_code = 'CSE304' AND co2.section = '01'
  );
```
정답 컬럼: course_code, section / 예측 컬럼: course_code, section, course_name
정답 행 수: 3 / 예측 행 수: 3

### D02-T3 — correct_extra_columns
질문: 그중 전공필수인 강좌만 과목코드와 분반으로 알려줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
SELECT DISTINCT co.course_code, co.section, co.course_name
FROM course_offerings co
JOIN offering_professors op ON co.offering_id = op.offering_id
JOIN course_offering_categories coc ON co.offering_id = coc.offering_id
JOIN departments d ON coc.department_id = d.department_id
JOIN course_categories cc ON coc.category_id = cc.category_id
WHERE co.year = 2026 AND co.semester = '1'
  AND d.name = '컴퓨터공학과'
  AND cc.category_name = '전공필수'
  AND co.course_code <> 'CSE304'
  AND op.professor_id IN (
      SELECT op2.professor_id
      FROM course_offerings co2
      JOIN offering_professors op2 ON co2.offering_id = op2.offering_id
      WHERE co2.year = 2026 AND co2.semester = '1' AND co2.course_code = 'CSE304' AND co2.section = '01'
  );
```
정답 컬럼: course_code, section / 예측 컬럼: course_code, section, course_name
정답 행 수: 1 / 예측 행 수: 1

### D03-T2 — row_count_mismatch
질문: 그 교수님이 같은 학기 인공지능학과 개설목록에서 맡은 다른 과목의 코드와 분반은? 방금 과목 코드는 제외해줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
WITH target_professors AS (
    SELECT op.professor_id
    FROM course_offerings co
    JOIN offering_professors op ON co.offering_id = op.offering_id
    WHERE co.year = 2026
      AND co.semester = '1'
      AND co.course_code = 'AI4003'
      AND co.section = '00'
)
SELECT DISTINCT co.course_code, co.section
FROM course_offerings co
JOIN offering_professors op ON co.offering_id = op.offering_id
JOIN target_professors tp ON op.professor_id = tp.professor_id
JOIN courses c ON co.course_code = c.course_code
JOIN departments d ON c.department_id = d.department_id
WHERE co.year = 2026
  AND co.semester = '1'
  AND d.name = '인공지능학과'
  AND co.course_code != 'AI4003'
ORDER BY co.course_code, co.section;
```
정답 컬럼: course_code, section / 예측 컬럼: course_code, section
정답 행 수: 5 / 예측 행 수: 2

### D03-T3 — row_count_mismatch
질문: 그중 전공필수인 강좌만 과목코드와 분반으로 알려줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
WITH target_professors AS (
    SELECT op.professor_id
    FROM course_offerings co
    JOIN offering_professors op ON co.offering_id = op.offering_id
    WHERE co.year = 2026
      AND co.semester = '1'
      AND co.course_code = 'AI4003'
      AND co.section = '00'
)
SELECT DISTINCT co.course_code, co.section
FROM course_offerings co
JOIN offering_professors op ON co.offering_id = op.offering_id
JOIN target_professors tp ON op.professor_id = tp.professor_id
JOIN courses c ON co.course_code = c.course_code
JOIN departments d ON c.department_id = d.department_id
JOIN course_offering_categories coc ON co.offering_id = coc.offering_id AND coc.department_id = d.department_id
JOIN course_categories cc ON coc.category_id = cc.category_id
WHERE co.year = 2026
  AND co.semester = '1'
  AND d.name = '인공지능학과'
  AND co.course_code != 'AI4003'
  AND cc.category_name = '전공필수'
ORDER BY co.course_code, co.section;
```
정답 컬럼: course_code, section / 예측 컬럼: course_code, section
정답 행 수: 3 / 예측 행 수: 1

### D05-T1 — correct_extra_columns
질문: 2025학년도 1학기 CSE406-01(캡스톤디자인)의 중간·기말고사 비율은 각각 얼마야?

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
SELECT
    co.course_code,
    co.course_name,
    co.section,
    s.midterm_percentage,
    s.final_exam_percentage
FROM course_offerings AS co
JOIN syllabi AS s
    ON co.offering_id = s.offering_id
WHERE co.year = 2025
  AND co.semester = '1'
  AND co.course_code = 'CSE406'
  AND co.section = '01';
```
정답 컬럼: midterm_percentage, final_exam_percentage / 예측 컬럼: course_code, course_name, section, midterm_percentage, final_exam_percentage
정답 행 수: 1 / 예측 행 수: 1

### D05-T2 — correct_extra_columns
질문: 그 두 시험 비율을 합치면 몇 퍼센트야?

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
SELECT
    co.course_code,
    co.course_name,
    co.section,
    s.midterm_percentage,
    s.final_exam_percentage,
    COALESCE(s.midterm_percentage, 0) + COALESCE(s.final_exam_percentage, 0) AS total_exam_percentage
FROM course_offerings AS co
JOIN syllabi AS s
    ON co.offering_id = s.offering_id
WHERE co.year = 2025
  AND co.semester = '1'
  AND co.course_code = 'CSE406'
  AND co.section = '01';
```
정답 컬럼: exam_total / 예측 컬럼: course_code, course_name, section, midterm_percentage, final_exam_percentage, total_exam_percentage
정답 행 수: 1 / 예측 행 수: 1

### D05-T3 — correct_extra_columns
질문: 그 합계에서 2025학년도 2학기 CSE497-02(연구연수활동2(컴퓨터공학))의 두 시험 비율 합계를 빼면 몇 퍼센트포인트야?

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
WITH first_course AS (
    SELECT
        COALESCE(s.midterm_percentage, 0) + COALESCE(s.final_exam_percentage, 0) AS total_exam_percentage
    FROM course_offerings AS co
    JOIN syllabi AS s
        ON co.offering_id = s.offering_id
    WHERE co.year = 2025
      AND co.semester = '1'
      AND co.course_code = 'CSE406'
      AND co.section = '01'
),
second_course AS (
    SELECT
        COALESCE(s.midterm_percentage, 0) + COALESCE(s.final_exam_percentage, 0) AS total_exam_percentage
    FROM course_offerings AS co
    JOIN syllabi AS s
        ON co.offering_id = s.offering_id
    WHERE co.year = 2025
      AND co.semester = '2'
      AND co.course_code = 'CSE497'
      AND co.section = '02'
)
SELECT
    fc.total_exam_percentage AS cse406_total_exam_percentage,
    sc.total_exam_percentage AS cse497_total_exam_percentage,
    fc.total_exam_percentage - sc.total_exam_percentage AS percentage_point_difference
FROM first_course AS fc
CROSS JOIN second_course AS sc;
```
정답 컬럼: first_minus_second_pp / 예측 컬럼: cse406_total_exam_percentage, cse497_total_exam_percentage, percentage_point_difference
정답 행 수: 1 / 예측 행 수: 1

### D06-T1 — correct_extra_columns
질문: 2026학년도 1학기 AI4003-00(졸업논문(인공지능))의 중간·기말고사 비율은 각각 얼마야?

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
SELECT co.course_code, co.course_name, co.section, s.midterm_percentage, s.final_exam_percentage
FROM course_offerings co
JOIN syllabi s ON s.offering_id = co.offering_id
WHERE co.year = 2026
  AND co.semester = '1'
  AND co.course_code = 'AI4003'
  AND co.section = '00';
```
정답 컬럼: midterm_percentage, final_exam_percentage / 예측 컬럼: course_code, course_name, section, midterm_percentage, final_exam_percentage
정답 행 수: 1 / 예측 행 수: 1

### D06-T2 — correct_extra_columns
질문: 그 두 시험 비율을 합치면 몇 퍼센트야?

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
SELECT co.course_code, co.course_name, co.section, s.midterm_percentage, s.final_exam_percentage, COALESCE(s.midterm_percentage, 0) + COALESCE(s.final_exam_percentage, 0) AS exam_total_percentage
FROM course_offerings co
JOIN syllabi s ON s.offering_id = co.offering_id
WHERE co.year = 2026
  AND co.semester = '1'
  AND co.course_code = 'AI4003'
  AND co.section = '00';
```
정답 컬럼: exam_total / 예측 컬럼: course_code, course_name, section, midterm_percentage, final_exam_percentage, exam_total_percentage
정답 행 수: 1 / 예측 행 수: 1

### D06-T3 — correct_extra_columns
질문: 그 합계에서 2026학년도 1학기 EE209-01(논리회로)의 두 시험 비율 합계를 빼면 몇 퍼센트포인트야?

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
WITH first_course AS (
    SELECT COALESCE(s.midterm_percentage, 0) + COALESCE(s.final_exam_percentage, 0) AS total_exam_pct
    FROM course_offerings co
    JOIN syllabi s ON s.offering_id = co.offering_id
    WHERE co.year = 2026
      AND co.semester = '1'
      AND co.course_code = 'AI4003'
      AND co.section = '00'
),
second_course AS (
    SELECT COALESCE(s.midterm_percentage, 0) + COALESCE(s.final_exam_percentage, 0) AS total_exam_pct
    FROM course_offerings co
    JOIN syllabi s ON s.offering_id = co.offering_id
    WHERE co.year = 2026
      AND co.semester = '1'
      AND co.course_code = 'EE209'
      AND co.section = '01'
)
SELECT f.total_exam_pct AS first_exam_total,
       s.total_exam_pct AS second_exam_total,
       f.total_exam_pct - s.total_exam_pct AS exam_total_diff
FROM first_course f
CROSS JOIN second_course s;
```
정답 컬럼: first_minus_second_pp / 예측 컬럼: first_exam_total, second_exam_total, exam_total_diff
정답 행 수: 1 / 예측 행 수: 1

### D07-T1 — correct_extra_columns
질문: 2025학년도 1학기 CSE405-00(졸업프로젝트)의 중간·기말고사 비율은 각각 얼마야?

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
SELECT co.course_code, co.course_name, co.section, s.midterm_percentage, s.final_exam_percentage
FROM course_offerings co
JOIN syllabi s ON co.offering_id = s.offering_id
WHERE co.year = 2025
  AND co.semester = '1'
  AND co.course_code = 'CSE405'
  AND co.section = '00';
```
정답 컬럼: midterm_percentage, final_exam_percentage / 예측 컬럼: course_code, course_name, section, midterm_percentage, final_exam_percentage
정답 행 수: 1 / 예측 행 수: 1

### D07-T2 — correct_extra_columns
질문: 그 두 시험 비율을 합치면 몇 퍼센트야?

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
SELECT co.course_code, co.course_name, co.section, COALESCE(s.midterm_percentage, 0) + COALESCE(s.final_exam_percentage, 0) AS total_exam_percentage
FROM course_offerings co
JOIN syllabi s ON co.offering_id = s.offering_id
WHERE co.year = 2025
  AND co.semester = '1'
  AND co.course_code = 'CSE405'
  AND co.section = '00';
```
정답 컬럼: exam_total / 예측 컬럼: course_code, course_name, section, total_exam_percentage
정답 행 수: 1 / 예측 행 수: 1

### D07-T3 — correct_extra_columns
질문: 그 합계에서 2025학년도 2학기 CSE302-01(컴퓨터네트워크)의 두 시험 비율 합계를 빼면 몇 퍼센트포인트야?

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
WITH exam_cse405 AS (
    SELECT COALESCE(s.midterm_percentage, 0) + COALESCE(s.final_exam_percentage, 0) AS total_exam
    FROM course_offerings co
    JOIN syllabi s ON co.offering_id = s.offering_id
    WHERE co.year = 2025
      AND co.semester = '1'
      AND co.course_code = 'CSE405'
      AND co.section = '00'
),
exam_cse302 AS (
    SELECT COALESCE(s.midterm_percentage, 0) + COALESCE(s.final_exam_percentage, 0) AS total_exam
    FROM course_offerings co
    JOIN syllabi s ON co.offering_id = s.offering_id
    WHERE co.year = 2025
      AND co.semester = '2'
      AND co.course_code = 'CSE302'
      AND co.section = '01'
)
SELECT exam_cse405.total_exam AS cse405_total_exam,
       exam_cse302.total_exam AS cse302_total_exam,
       exam_cse405.total_exam - exam_cse302.total_exam AS percentage_point_diff
FROM exam_cse405, exam_cse302;
```
정답 컬럼: first_minus_second_pp / 예측 컬럼: cse405_total_exam, cse302_total_exam, percentage_point_diff
정답 행 수: 1 / 예측 행 수: 1

### D08-T1 — correct_extra_columns
질문: 2026학년도 1학기 IE419-00(서비스데이터사이언스)의 중간·기말고사 비율은 각각 얼마야?

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
SELECT
    co.course_code,
    co.section,
    co.course_name,
    s.midterm_percentage,
    s.final_exam_percentage
FROM course_offerings AS co
JOIN syllabi AS s ON s.offering_id = co.offering_id
WHERE co.year = 2026
  AND co.semester = '1'
  AND co.course_code = 'IE419'
  AND co.section = '00';
```
정답 컬럼: midterm_percentage, final_exam_percentage / 예측 컬럼: course_code, section, course_name, midterm_percentage, final_exam_percentage
정답 행 수: 1 / 예측 행 수: 1

### D08-T2 — correct_extra_columns
질문: 그 두 시험 비율을 합치면 몇 퍼센트야?

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
SELECT
    co.course_code,
    co.section,
    co.course_name,
    s.midterm_percentage,
    s.final_exam_percentage,
    COALESCE(s.midterm_percentage, 0) + COALESCE(s.final_exam_percentage, 0) AS exam_total_percentage
FROM course_offerings AS co
JOIN syllabi AS s ON s.offering_id = co.offering_id
WHERE co.year = 2026
  AND co.semester = '1'
  AND co.course_code = 'IE419'
  AND co.section = '00';
```
정답 컬럼: exam_total / 예측 컬럼: course_code, section, course_name, midterm_percentage, final_exam_percentage, exam_total_percentage
정답 행 수: 1 / 예측 행 수: 1

### D08-T3 — correct_extra_columns
질문: 그 합계에서 2026학년도 1학기 SWCON321-02(데이터분석캡스톤디자인)의 두 시험 비율 합계를 빼면 몇 퍼센트포인트야?

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
WITH ie AS (
    SELECT COALESCE(s.midterm_percentage, 0) + COALESCE(s.final_exam_percentage, 0) AS exam_total
    FROM course_offerings AS co
    JOIN syllabi AS s ON s.offering_id = co.offering_id
    WHERE co.year = 2026
      AND co.semester = '1'
      AND co.course_code = 'IE419'
      AND co.section = '00'
),
swcon AS (
    SELECT COALESCE(s.midterm_percentage, 0) + COALESCE(s.final_exam_percentage, 0) AS exam_total
    FROM course_offerings AS co
    JOIN syllabi AS s ON s.offering_id = co.offering_id
    WHERE co.year = 2026
      AND co.semester = '1'
      AND co.course_code = 'SWCON321'
      AND co.section = '02'
)
SELECT
    ie.exam_total AS ie419_exam_total,
    swcon.exam_total AS swcon321_exam_total,
    ie.exam_total - swcon.exam_total AS diff_percentage_points
FROM ie
CROSS JOIN swcon;
```
정답 컬럼: first_minus_second_pp / 예측 컬럼: ie419_exam_total, swcon321_exam_total, diff_percentage_points
정답 행 수: 1 / 예측 행 수: 1

### D10-T1 — correct_extra_columns
질문: 2023학번의 후마니타스 기본구조표상 배분이수 최소학점은? 면제·대체 예외는 제외해줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
SELECT gerc.min_credits, gerc.min_areas, gerc.per_area_min_credits
FROM general_education_requirements ger
JOIN general_education_requirement_categories gerc
  ON ger.general_requirement_id = gerc.general_requirement_id
WHERE ger.cohort_start <= 2023
  AND (ger.cohort_end IS NULL OR ger.cohort_end >= 2023)
  AND gerc.requirement_code = 'DISTRIBUTION';
```
정답 컬럼: distribution_credits / 예측 컬럼: min_credits, min_areas, per_area_min_credits
정답 행 수: 1 / 예측 행 수: 1

### D10-T2 — correct_extra_columns
질문: 그럼 2024학번은?

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
SELECT gerc.min_credits, gerc.min_areas, gerc.per_area_min_credits
FROM general_education_requirements ger
JOIN general_education_requirement_categories gerc
  ON ger.general_requirement_id = gerc.general_requirement_id
WHERE ger.cohort_start <= 2024
  AND (ger.cohort_end IS NULL OR ger.cohort_end >= 2024)
  AND gerc.requirement_code = 'DISTRIBUTION';
```
정답 컬럼: distribution_credits / 예측 컬럼: min_credits, min_areas, per_area_min_credits
정답 행 수: 1 / 예측 행 수: 1

### D10-T3 — correct_extra_columns
질문: 앞의 두 학번을 비교하면 몇 학점 줄어든 거야?

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
WITH c2023 AS (
  SELECT gerc.min_credits
  FROM general_education_requirements ger
  JOIN general_education_requirement_categories gerc
    ON ger.general_requirement_id = gerc.general_requirement_id
  WHERE ger.cohort_start <= 2023
    AND (ger.cohort_end IS NULL OR ger.cohort_end >= 2023)
    AND gerc.requirement_code = 'DISTRIBUTION'
),
c2024 AS (
  SELECT gerc.min_credits
  FROM general_education_requirements ger
  JOIN general_education_requirement_categories gerc
    ON ger.general_requirement_id = gerc.general_requirement_id
  WHERE ger.cohort_start <= 2024
    AND (ger.cohort_end IS NULL OR ger.cohort_end >= 2024)
    AND gerc.requirement_code = 'DISTRIBUTION'
)
SELECT c2023.min_credits AS credits_2023,
       c2024.min_credits AS credits_2024,
       (c2023.min_credits - c2024.min_credits) AS reduced_credits
FROM c2023, c2024;
```
정답 컬럼: credit_reduction / 예측 컬럼: credits_2023, credits_2024, reduced_credits
정답 행 수: 1 / 예측 행 수: 1

### D11-T3 — row_count_mismatch
질문: 그 교수님의 같은 학기 인공지능학과 다른 과목은? AI4007 과목 코드는 제외하고 코드·분반으로 알려줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
WITH target_prof AS (
    SELECT op.professor_id
    FROM course_offerings co
    JOIN offering_professors op ON co.offering_id = op.offering_id
    WHERE co.year = 2026
      AND co.semester = '2'
      AND co.course_code = 'AI4007'
      AND co.section = '08'
)
SELECT DISTINCT co.course_code, co.section
FROM course_offerings co
JOIN offering_professors op ON co.offering_id = op.offering_id
JOIN courses c ON co.course_code = c.course_code
JOIN departments d ON c.department_id = d.department_id
WHERE co.year = 2026
  AND co.semester = '2'
  AND op.professor_id IN (SELECT professor_id FROM target_prof)
  AND d.name = '인공지능학과'
  AND co.course_code != 'AI4007'
ORDER BY co.course_code, co.section
```
정답 컬럼: course_code, section / 예측 컬럼: course_code, section
정답 행 수: 2 / 예측 행 수: 0


## 진단 코드 설명

- correct: 결과 완전 일치 / correct_extra_columns: 컬럼이 더 있거나 컬럼 순서가 다름(relaxed 정답)
- missing_columns: 예측 값은 모두 맞지만 정답의 일부 컬럼이 빠짐(subset 정답, 사람이 확인)
- order_mismatch: 행 정렬만 다름(relaxed 정답) / row_count_mismatch: 행 수가 다름 / value_mismatch: 행 수는 같지만 값이 다름
- exec_fail:sqlite 실행 오류 / exec_fail:guard 안전장치에 의해 거부 / exec_fail:no_sql SQL 추출 실패
- exec_fail:timeout 시간 초과 / exec_fail:refused 거부하면 안 되는 질문을 거부
- correct_refusal: 거부가 정답인 문항을 거부·차단 / no_leak_but_not_refused: 거부는 안 했지만 결과 0행
- should_have_refused: 거부해야 하는데 결과를 돌려줌 / api_error ChatKHU 호출 실패 / gold_invalid 정답 SQL 문제
