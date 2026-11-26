# Text2SQL 평가 결과 (2026-11-20 14:41)

| 지표 | 값 |
|---|---|
| 평가 문항 수 | 11 |
| 실행 성공률(최종) | 11/11 (100.0%) |
| 실행 성공률(1차 시도) | 11/11 (100.0%) |
| 정답률 strict | 9/11 (81.8%) |
| 정답률 relaxed | 11/11 (100.0%) |
| 정답률 subset (정답 일부 컬럼 누락 허용) | 11/11 (100.0%) |
| 평균 토큰 | 4824.0 |
| 평균 응답시간(초) | 8.6 |

## 유형별

| 태그 | n | strict | relaxed | subset | 실행 성공 |
|---|---|---|---|---|---|
| arithmetic_reasoning | 2 | 0/2 (0.0%) | 2/2 (100.0%) | 2/2 (100.0%) | 2/2 (100.0%) |
| combined_exam_gap | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| exam_threshold_set | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| midterm_max | 1 | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) |
| multi_document_reasoning | 9 | 9/9 (100.0%) | 9/9 (100.0%) | 9/9 (100.0%) | 9/9 (100.0%) |
| official_public_facts | 9 | 9/9 (100.0%) | 9/9 (100.0%) | 9/9 (100.0%) | 9/9 (100.0%) |
| official_rule_with_hypothetical_inputs | 2 | 0/2 (0.0%) | 2/2 (100.0%) | 2/2 (100.0%) | 2/2 (100.0%) |
| weighted_exam_score | 2 | 0/2 (0.0%) | 2/2 (100.0%) | 2/2 (100.0%) | 2/2 (100.0%) |

## 진단 분포

| 진단 | 개수 |
|---|---|
| correct | 9 |
| correct_extra_columns | 2 |

## 정답 재검토가 필요한 문항

- J029 (O): 2025학년도 1학기 EE211-02(확률및랜덤변수)와 2025학년도 1학기 CSE438-00(최신기술콜로키움1)의 중간·기말 비율 합계를 각각 구하고, 두 번째 합계에서 첫 번째 합계를 뺀 차이도 알려줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J030 (O): 2026학년도 2학기 AI3003-00(자연언어학습)와 2025학년도 1학기 CSE428-00(컴퓨터그래픽스)의 중간·기말 비율 합계를 각각 구하고, 두 번째 합계에서 첫 번째 합계를 뺀 차이도 알려줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J031 (O): 2025학년도 1학기 CSE496-06(연구연수활동1(컴퓨터공학))와 2025학년도 1학기 CSE304-00(알고리즘)의 중간·기말 비율 합계를 각각 구하고, 두 번째 합계에서 첫 번째 합계를 뺀 차이도 알려줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J032 (O): 2025학년도 1학기 CSE405-00(졸업프로젝트)와 2026학년도 1학기 IE419-00(서비스데이터사이언스)의 중간·기말 비율 합계를 각각 구하고, 두 번째 합계에서 첫 번째 합계를 뺀 차이도 알려줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J033 (O): 2026학년도 2학기 EE209-02(논리회로)와 2026학년도 1학기 CSE204-01(자료구조) 중 중간고사 비율이 더 큰 강좌의 과목코드·연도·학기·분반·비율을 알려줘. 같으면 둘 다 알려줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J073 (O): 다음 세 강좌 중 중간·기말 비율 합계가 70% 이상인 강좌의 과목코드·연도·학기·분반·합계를 알려줘: 2025학년도 1학기 CSE406-01(캡스톤디자인), 2026학년도 1학기 AI4003-00(졸업논문(인공지능)), 2025학년도 1학기 CSE405-00(졸업프로젝트). — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J075 (O): 다음 세 강좌 중 중간·기말 비율 합계가 70% 이상인 강좌의 과목코드·연도·학기·분반·합계를 알려줘: 2026학년도 1학기 IE419-00(서비스데이터사이언스), 2025학년도 2학기 CSE497-02(연구연수활동2(컴퓨터공학)), 2026학년도 1학기 EE209-01(논리회로). — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J077 (O): 다음 세 강좌 중 중간·기말 비율 합계가 70% 이상인 강좌의 과목코드·연도·학기·분반·합계를 알려줘: 2025학년도 2학기 CSE302-01(컴퓨터네트워크), 2026학년도 1학기 SWCON321-02(데이터분석캡스톤디자인), 2026학년도 2학기 CSE406-16(캡스톤디자인). — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J079 (O): 다음 세 강좌 중 중간·기말 비율 합계가 70% 이상인 강좌의 과목코드·연도·학기·분반·합계를 알려줘: 2025학년도 1학기 CSE327-00(소프트웨어공학), 2025학년도 1학기 CSE496-06(연구연수활동1(컴퓨터공학)), 2025학년도 1학기 CSE304-00(알고리즘). — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J086 (X): 2026학년도 1학기 CSE438-00(최신기술콜로키움1)에서 중간고사 80점, 기말고사 90점(각 100점 만점)을 받았다고 가정하면 두 시험이 최종 100점에 기여하는 점수 합은? 다른 항목과 추가 보정은 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J087 (X): 2025학년도 2학기 AI4007-00(독립심화학습(인공지능)2)에서 중간고사 80점, 기말고사 90점(각 100점 만점)을 받았다고 가정하면 두 시험이 최종 100점에 기여하는 점수 합은? 다른 항목과 추가 보정은 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.

## 오답 목록

### J086 — correct_extra_columns
질문: 2026학년도 1학기 CSE438-00(최신기술콜로키움1)에서 중간고사 80점, 기말고사 90점(각 100점 만점)을 받았다고 가정하면 두 시험이 최종 100점에 기여하는 점수 합은? 다른 항목과 추가 보정은 제외해줘.

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
    (80.0 * s.midterm_percentage / 100.0) + (90.0 * s.final_exam_percentage / 100.0) AS exam_contribution_score
FROM course_offerings co
JOIN syllabi s ON co.offering_id = s.offering_id
WHERE co.year = 2026
  AND co.semester = '1'
  AND co.course_code = 'CSE438'
  AND co.section = '00';
```
정답 컬럼: exam_contribution_points / 예측 컬럼: course_code, section, course_name, midterm_percentage, final_exam_percentage, exam_contribution_score
정답 행 수: 1 / 예측 행 수: 1

### J087 — correct_extra_columns
질문: 2025학년도 2학기 AI4007-00(독립심화학습(인공지능)2)에서 중간고사 80점, 기말고사 90점(각 100점 만점)을 받았다고 가정하면 두 시험이 최종 100점에 기여하는 점수 합은? 다른 항목과 추가 보정은 제외해줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
SELECT
  s.midterm_percentage,
  s.final_exam_percentage,
  ROUND((80 * s.midterm_percentage + 90 * s.final_exam_percentage) / 100.0, 2) AS expected_score
FROM course_offerings AS co
JOIN syllabi AS s
  ON s.offering_id = co.offering_id
WHERE co.year = 2025
  AND co.semester = '2'
  AND co.course_code = 'AI4007'
  AND co.section = '00'
```
정답 컬럼: exam_contribution_points / 예측 컬럼: midterm_percentage, final_exam_percentage, expected_score
정답 행 수: 1 / 예측 행 수: 1


## 진단 코드 설명

- correct: 결과 완전 일치 / correct_extra_columns: 컬럼이 더 있거나 컬럼 순서가 다름(relaxed 정답)
- missing_columns: 예측 값은 모두 맞지만 정답의 일부 컬럼이 빠짐(subset 정답, 사람이 확인)
- order_mismatch: 행 정렬만 다름(relaxed 정답) / row_count_mismatch: 행 수가 다름 / value_mismatch: 행 수는 같지만 값이 다름
- exec_fail:sqlite 실행 오류 / exec_fail:guard 안전장치에 의해 거부 / exec_fail:no_sql SQL 추출 실패
- exec_fail:timeout 시간 초과 / exec_fail:refused 거부하면 안 되는 질문을 거부
- correct_refusal: 거부가 정답인 문항을 거부·차단 / no_leak_but_not_refused: 거부는 안 했지만 결과 0행
- should_have_refused: 거부해야 하는데 결과를 돌려줌 / api_error ChatKHU 호출 실패 / gold_invalid 정답 SQL 문제
