# SQL 논리 LLM 채점 (2026-11-20 14:41)

judge 모델: `gpt-5.6-luna` / judge 토큰 합계: 19360

통과 기준: 정답 SQL 과 논리가 같음 + 질문에 없는 조건 없음 + 본인 학번 범위 지킴

| 지표 | 값 |
|---|---|
| SQL 논리 통과율 | 10/11 (90.9%) |
| 논리 일치 | 10/11 (90.9%) |
| (참고) 실행 결과 정답률 strict | 9/11 (81.8%) |
| 결과는 맞았지만 논리가 틀림(우연히 맞음) | 0 |
| 질문에 없는 조건 추가 | 0 |
| 본인 학번 범위 위반 | 0 |

## 유형별

| 태그 | n | 통과 | 논리 일치 | 실행 strict | 우연히 맞음 |
|---|---|---|---|---|---|
| arithmetic_reasoning | 2 | 1/2 (50.0%) | 1/2 (50.0%) | 0/2 (0.0%) | 0 |
| combined_exam_gap | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 0 |
| exam_threshold_set | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 0 |
| midterm_max | 1 | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) | 0 |
| multi_document_reasoning | 9 | 9/9 (100.0%) | 9/9 (100.0%) | 9/9 (100.0%) | 0 |
| official_public_facts | 9 | 9/9 (100.0%) | 9/9 (100.0%) | 9/9 (100.0%) | 0 |
| official_rule_with_hypothetical_inputs | 2 | 1/2 (50.0%) | 1/2 (50.0%) | 0/2 (0.0%) | 0 |
| weighted_exam_score | 2 | 1/2 (50.0%) | 1/2 (50.0%) | 0/2 (0.0%) | 0 |

## 결과는 틀렸지만 논리는 같다고 판정 — judge 오판인지 확인 (1개)

### J086 — 실행 진단 correct_extra_columns
질문: 2026학년도 1학기 CSE438-00(최신기술콜로키움1)에서 중간고사 80점, 기말고사 90점(각 100점 만점)을 받았다고 가정하면 두 시험이 최종 100점에 기여하는 점수 합은? 다른 항목과 추가 보정은 제외해줘.

- 판정 이유: 과목·학기·분반 조건과 시험 반영점수 계산이 정답과 논리적으로 같고 추가 조건이 없다.

정답 SQL:
```sql
SELECT ROUND((s.midterm_percentage*80+s.final_exam_percentage*90)/100.0,4) AS exam_contribution_points FROM course_offerings o JOIN syllabi s ON s.offering_id=o.offering_id WHERE o.year=2026 AND o.semester='1' AND o.course_code='CSE438' AND o.section='00' AND o.campus='국제';
```
모델 SQL:
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

