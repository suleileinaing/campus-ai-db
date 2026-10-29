# 실행 비교 vs LLM 채점 (2026-10-29 21:14)

judge 모델: `gpt-6-astra` / judge 토큰 합계: 55226

| 기준 | 정답률 |
|---|---|
| execution match (strict) | 96/100 (96.0%) |
| execution match (relaxed) | 96/100 (96.0%) |
| LLM-as-a-judge | 96/100 (96.0%) |

## 두 기준의 일치 (strict 기준)

| | LLM O | LLM X |
|---|---|---|
| 실행 O | 96 | 0 |
| 실행 X | 0 | 4 |

## 유형별

| 태그 | n | strict | relaxed | LLM |
|---|---|---|---|---|
| arithmetic_reasoning | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| assignment_gap | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| assignment_min | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| assignment_ranking | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| attendance_gap | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| classification_aggregation | 4 | 2/4 (50.0%) | 2/4 (50.0%) | 2/4 (50.0%) |
| combined_exam_gap | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| common_instructor | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| cross_rule_reasoning | 1 | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) |
| department_required_load | 4 | 2/4 (50.0%) | 2/4 (50.0%) | 2/4 (50.0%) |
| distribution_rule_application | 3 | 3/3 (100.0%) | 3/3 (100.0%) | 3/3 (100.0%) |
| english_industry | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| exam_change | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| exam_threshold_set | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| fixture_earned | 2 | 2/2 (100.0%) | 2/2 (100.0%) | 2/2 (100.0%) |
| fixture_personalized | 6 | 6/6 (100.0%) | 6/6 (100.0%) | 6/6 (100.0%) |
| fixture_retake | 2 | 2/2 (100.0%) | 2/2 (100.0%) | 2/2 (100.0%) |
| fixture_status | 2 | 2/2 (100.0%) | 2/2 (100.0%) | 2/2 (100.0%) |
| general_cohort_difference | 1 | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) |
| general_cohort_rule | 2 | 2/2 (100.0%) | 2/2 (100.0%) | 2/2 (100.0%) |
| midterm_max | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| multi_document_multi_hop | 8 | 7/8 (87.5%) | 7/8 (87.5%) | 7/8 (87.5%) |
| multi_document_multi_hop_reasoning | 8 | 8/8 (100.0%) | 8/8 (100.0%) | 8/8 (100.0%) |
| multi_document_reasoning | 32 | 32/32 (100.0%) | 32/32 (100.0%) | 32/32 (100.0%) |
| multi_hop | 16 | 16/16 (100.0%) | 16/16 (100.0%) | 16/16 (100.0%) |
| multi_hop_aggregation | 4 | 3/4 (75.0%) | 3/4 (75.0%) | 3/4 (75.0%) |
| official_public_facts | 87 | 83/87 (95.4%) | 83/87 (95.4%) | 83/87 (95.4%) |
| official_rule | 2 | 2/2 (100.0%) | 2/2 (100.0%) | 2/2 (100.0%) |
| official_rule_with_hypothetical_inputs | 7 | 7/7 (100.0%) | 7/7 (100.0%) | 7/7 (100.0%) |
| prof_credit_load | 4 | 3/4 (75.0%) | 3/4 (75.0%) | 3/4 (75.0%) |
| prof_future_other | 4 | 3/4 (75.0%) | 3/4 (75.0%) | 3/4 (75.0%) |
| prof_other_3credit | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| prof_other_industry | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| prof_other_required | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| professor_assessment_filter | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| professor_assessment_ranking | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| professor_required_credit_chain | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| rule_reasoning | 3 | 3/3 (100.0%) | 3/3 (100.0%) | 3/3 (100.0%) |
| schedule_overlap | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| simulated_student_fixture | 6 | 6/6 (100.0%) | 6/6 (100.0%) | 6/6 (100.0%) |
| single_document | 8 | 8/8 (100.0%) | 8/8 (100.0%) | 8/8 (100.0%) |
| teacher_credits | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| temporal_reasoning | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| weighted_exam_score | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
