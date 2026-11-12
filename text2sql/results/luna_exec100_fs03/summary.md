# Text2SQL 평가 결과 (2026-11-05 18:09)

| 지표 | 값 |
|---|---|
| 평가 문항 수 | 100 |
| 실행 성공률(최종) | 100/100 (100.0%) |
| 실행 성공률(1차 시도) | 99/100 (99.0%) |
| 정답률 strict | 82/100 (82.0%) |
| 정답률 relaxed | 88/100 (88.0%) |
| 정답률 subset (정답 일부 컬럼 누락 허용) | 88/100 (88.0%) |
| 평균 토큰 | 4598.9 |
| 평균 응답시간(초) | 6.21 |

## 유형별

| 태그 | n | strict | relaxed | subset | 실행 성공 |
|---|---|---|---|---|---|
| arithmetic_reasoning | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| assignment_gap | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| assignment_min | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| assignment_ranking | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| attendance_gap | 4 | 3/4 (75.0%) | 3/4 (75.0%) | 3/4 (75.0%) | 4/4 (100.0%) |
| classification_aggregation | 4 | 0/4 (0.0%) | 0/4 (0.0%) | 0/4 (0.0%) | 4/4 (100.0%) |
| combined_exam_gap | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| common_instructor | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| cross_rule_reasoning | 1 | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) |
| department_required_load | 4 | 0/4 (0.0%) | 0/4 (0.0%) | 0/4 (0.0%) | 4/4 (100.0%) |
| distribution_rule_application | 3 | 0/3 (0.0%) | 2/3 (66.7%) | 2/3 (66.7%) | 3/3 (100.0%) |
| english_industry | 4 | 3/4 (75.0%) | 3/4 (75.0%) | 3/4 (75.0%) | 4/4 (100.0%) |
| exam_change | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| exam_threshold_set | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| fixture_earned | 2 | 2/2 (100.0%) | 2/2 (100.0%) | 2/2 (100.0%) | 2/2 (100.0%) |
| fixture_personalized | 6 | 6/6 (100.0%) | 6/6 (100.0%) | 6/6 (100.0%) | 6/6 (100.0%) |
| fixture_retake | 2 | 2/2 (100.0%) | 2/2 (100.0%) | 2/2 (100.0%) | 2/2 (100.0%) |
| fixture_status | 2 | 2/2 (100.0%) | 2/2 (100.0%) | 2/2 (100.0%) | 2/2 (100.0%) |
| general_cohort_difference | 1 | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) |
| general_cohort_rule | 2 | 1/2 (50.0%) | 1/2 (50.0%) | 1/2 (50.0%) | 2/2 (100.0%) |
| midterm_max | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| multi_document_multi_hop | 8 | 7/8 (87.5%) | 7/8 (87.5%) | 7/8 (87.5%) | 8/8 (100.0%) |
| multi_document_multi_hop_reasoning | 8 | 8/8 (100.0%) | 8/8 (100.0%) | 8/8 (100.0%) | 8/8 (100.0%) |
| multi_document_reasoning | 32 | 31/32 (96.9%) | 31/32 (96.9%) | 31/32 (96.9%) | 32/32 (100.0%) |
| multi_hop | 16 | 15/16 (93.8%) | 15/16 (93.8%) | 15/16 (93.8%) | 16/16 (100.0%) |
| multi_hop_aggregation | 4 | 0/4 (0.0%) | 2/4 (50.0%) | 2/4 (50.0%) | 4/4 (100.0%) |
| official_public_facts | 87 | 72/87 (82.8%) | 76/87 (87.4%) | 76/87 (87.4%) | 87/87 (100.0%) |
| official_rule | 2 | 1/2 (50.0%) | 1/2 (50.0%) | 1/2 (50.0%) | 2/2 (100.0%) |
| official_rule_with_hypothetical_inputs | 7 | 4/7 (57.1%) | 6/7 (85.7%) | 6/7 (85.7%) | 7/7 (100.0%) |
| prof_credit_load | 4 | 0/4 (0.0%) | 2/4 (50.0%) | 2/4 (50.0%) | 4/4 (100.0%) |
| prof_future_other | 4 | 3/4 (75.0%) | 3/4 (75.0%) | 3/4 (75.0%) | 4/4 (100.0%) |
| prof_other_3credit | 4 | 3/4 (75.0%) | 3/4 (75.0%) | 3/4 (75.0%) | 4/4 (100.0%) |
| prof_other_industry | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| prof_other_required | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| professor_assessment_filter | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| professor_assessment_ranking | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| professor_required_credit_chain | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| rule_reasoning | 3 | 0/3 (0.0%) | 2/3 (66.7%) | 2/3 (66.7%) | 3/3 (100.0%) |
| schedule_overlap | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| simulated_student_fixture | 6 | 6/6 (100.0%) | 6/6 (100.0%) | 6/6 (100.0%) | 6/6 (100.0%) |
| single_document | 8 | 5/8 (62.5%) | 7/8 (87.5%) | 7/8 (87.5%) | 8/8 (100.0%) |
| teacher_credits | 4 | 2/4 (50.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| temporal_reasoning | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| weighted_exam_score | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |

## 진단 분포

| 진단 | 개수 |
|---|---|
| correct | 82 |
| row_count_mismatch | 9 |
| correct_extra_columns | 6 |
| value_mismatch | 3 |

## 정답 재검토가 필요한 문항

- J001 (O): 2026학년도 2학기 SWCON331-00(로봇프로그래밍) 담당 교수의 다른 수업 중, 같은 학기 소프트웨어융합학과 기준 전공필수이면서 3학점인 강좌가 있어? 해당 과목코드·분반·학점을 모두 알려줘. 기준 과목의 다른 분반도 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J002 (O): 2026학년도 2학기 SWCON253-00(기계학습) 담당 교수의 다른 수업 중, 같은 학기 소프트웨어융합학과 기준 전공필수이면서 3학점인 강좌가 있어? 해당 과목코드·분반·학점을 모두 알려줘. 기준 과목의 다른 분반도 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J003 (O): 2026학년도 2학기 CSE304-00(알고리즘) 담당 교수의 다른 수업 중, 같은 학기 컴퓨터공학과 기준 전공필수이면서 3학점인 강좌가 있어? 해당 과목코드·분반·학점을 모두 알려줘. 기준 과목의 다른 분반도 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J004 (O): 2026학년도 2학기 SWCON253-02(기계학습) 담당 교수의 다른 수업 중, 같은 학기 컴퓨터공학과 기준 전공필수이면서 3학점인 강좌가 있어? 해당 과목코드·분반·학점을 모두 알려줘. 기준 과목의 다른 분반도 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J005 (O): 2026학년도 2학기 SWCON331-00(로봇프로그래밍) 담당 교수의 같은 학기 다른 수업 중 소프트웨어융합학과 기준 전공필수이고, 공식 강의계획서에 과제 반영 비율이 30% 이상으로 기재된 강좌의 과목코드·분반·과제 비율을 알려줘. 기준 과목의 다른 분반도 제외하고, 미기재 비율은 0으로 보지 마. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J006 (O): 2026학년도 2학기 SWCON253-00(기계학습) 담당 교수의 같은 학기 다른 수업 중 소프트웨어융합학과 기준 전공필수이고, 공식 강의계획서에 과제 반영 비율이 30% 이상으로 기재된 강좌의 과목코드·분반·과제 비율을 알려줘. 기준 과목의 다른 분반도 제외하고, 미기재 비율은 0으로 보지 마. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J007 (O): 2026학년도 2학기 CSE304-00(알고리즘) 담당 교수의 같은 학기 다른 수업 중 컴퓨터공학과 기준 전공필수이고, 공식 강의계획서에 과제 반영 비율이 30% 이상으로 기재된 강좌의 과목코드·분반·과제 비율을 알려줘. 기준 과목의 다른 분반도 제외하고, 미기재 비율은 0으로 보지 마. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J008 (O): 2026학년도 2학기 SWCON253-02(기계학습) 담당 교수의 같은 학기 다른 수업 중 컴퓨터공학과 기준 전공필수이고, 공식 강의계획서에 과제 반영 비율이 30% 이상으로 기재된 강좌의 과목코드·분반·과제 비율을 알려줘. 기준 과목의 다른 분반도 제외하고, 미기재 비율은 0으로 보지 마. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J009 (O): 2026학년도 2학기 EE209-02(논리회로)의 담당 교수 이름과 학점을 알려줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J010 (O): 2026학년도 2학기 EE209-02(논리회로)의 영어강좌 구분(영어전체/영어부분/해당없음)과 산학필수 여부(예/아니오)를 알려줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J011 (O): 2026학년도 1학기 SWCON367-01(게임콘텐츠캡스톤디자인) 담당 교수의 같은 학기 소프트웨어융합학과 개설목록 내 다른 3학점 강좌 중, 중간·기말 비율이 모두 기재된 강좌끼리 비교하면 시험 비율 합계가 가장 낮은 강좌는? 과목코드·분반·합계를 알려주고 동률은 모두 포함해줘. 기준 과목 코드는 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J012 (X): 2026학년도 1학기 CSE301-01(운영체제)의 담당 교수 이름과 학점을 알려줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J013 (O): 2026학년도 1학기 CSE301-01(운영체제)의 영어강좌 구분(영어전체/영어부분/해당없음)과 산학필수 여부(예/아니오)를 알려줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J014 (O): 2026학년도 1학기 SWCON366-00(3D데이터처리) 담당 교수의 같은 학기 소프트웨어융합학과 개설목록 내 다른 3학점 강좌 중, 중간·기말 비율이 모두 기재된 강좌끼리 비교하면 시험 비율 합계가 가장 낮은 강좌는? 과목코드·분반·합계를 알려주고 동률은 모두 포함해줘. 기준 과목 코드는 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J015 (X): 2025학년도 1학기 EE211-02(확률및랜덤변수)의 담당 교수 이름과 학점을 알려줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J016 (O): 2025학년도 1학기 EE211-02(확률및랜덤변수)의 영어강좌 구분(영어전체/영어부분/해당없음)과 산학필수 여부(예/아니오)를 알려줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J017 (O): 2026학년도 1학기 SWCON401-06(소프트웨어융합캡스톤디자인) 담당 교수의 같은 학기 소프트웨어융합학과 개설목록 내 다른 3학점 강좌 중, 중간·기말 비율이 모두 기재된 강좌끼리 비교하면 시험 비율 합계가 가장 낮은 강좌는? 과목코드·분반·합계를 알려주고 동률은 모두 포함해줘. 기준 과목 코드는 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J018 (O): 2026학년도 2학기 AI4007-07(독립심화학습(인공지능)2)의 담당 교수 이름과 학점을 알려줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J019 (X): 2026학년도 2학기 AI4007-07(독립심화학습(인공지능)2)의 영어강좌 구분(영어전체/영어부분/해당없음)과 산학필수 여부(예/아니오)를 알려줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J020 (O): 2026학년도 1학기 IE215-00(데이터사이언스) 담당 교수의 같은 학기 소프트웨어융합학과 개설목록 내 다른 3학점 강좌 중, 중간·기말 비율이 모두 기재된 강좌끼리 비교하면 시험 비율 합계가 가장 낮은 강좌는? 과목코드·분반·합계를 알려주고 동률은 모두 포함해줘. 기준 과목 코드는 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J021 (O): 2025학년도 1학기 CSE406-01(캡스톤디자인)와 2026학년도 1학기 CSE406-01(캡스톤디자인)의 기말고사 비율을 순서대로 알려주고, 두 번째에서 첫 번째를 뺀 차이를 퍼센트포인트로 계산해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J022 (O): 2025학년도 1학기 CSE406-01(캡스톤디자인)와 2026학년도 1학기 CSE406-06(캡스톤디자인)의 기말고사 비율을 순서대로 알려주고, 두 번째에서 첫 번째를 뺀 차이를 퍼센트포인트로 계산해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J023 (O): 2026학년도 2학기 CSE406-16(캡스톤디자인)와 2025학년도 2학기 CSE406-06(캡스톤디자인)의 기말고사 비율을 순서대로 알려주고, 두 번째에서 첫 번째를 뺀 차이를 퍼센트포인트로 계산해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J024 (O): 2026학년도 2학기 AI4007-01(독립심화학습(인공지능)2)와 2025학년도 2학기 AI4007-00(독립심화학습(인공지능)2)의 기말고사 비율을 순서대로 알려주고, 두 번째에서 첫 번째를 뺀 차이를 퍼센트포인트로 계산해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J025 (O): 2025학년도 1학기 CSE406-01(캡스톤디자인)와 2026학년도 1학기 AI4003-00(졸업논문(인공지능))의 과제보고서 비율을 순서대로 알려주고, 두 번째에서 첫 번째를 뺀 차이를 퍼센트포인트로 계산해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J026 (O): 2025학년도 2학기 CSE302-01(컴퓨터네트워크)와 2026학년도 1학기 SWCON321-02(데이터분석캡스톤디자인)의 과제보고서 비율을 순서대로 알려주고, 두 번째에서 첫 번째를 뺀 차이를 퍼센트포인트로 계산해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J027 (O): 2025학년도 1학기 CSE450-00(모바일/웹서비스프로그래밍)와 2025학년도 2학기 CSE406-06(캡스톤디자인)의 과제보고서 비율을 순서대로 알려주고, 두 번째에서 첫 번째를 뺀 차이를 퍼센트포인트로 계산해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J028 (O): 2025학년도 2학기 CSE403-00(졸업논문(컴퓨터공학전공))와 2025학년도 1학기 AI1001-00(인공지능개론)의 과제보고서 비율을 순서대로 알려주고, 두 번째에서 첫 번째를 뺀 차이를 퍼센트포인트로 계산해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J029 (O): 2025학년도 1학기 EE211-02(확률및랜덤변수)와 2025학년도 1학기 CSE438-00(최신기술콜로키움1)의 중간·기말 비율 합계를 각각 구하고, 두 번째 합계에서 첫 번째 합계를 뺀 차이도 알려줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J030 (O): 2026학년도 2학기 AI3003-00(자연언어학습)와 2025학년도 1학기 CSE428-00(컴퓨터그래픽스)의 중간·기말 비율 합계를 각각 구하고, 두 번째 합계에서 첫 번째 합계를 뺀 차이도 알려줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J031 (O): 2025학년도 1학기 CSE496-06(연구연수활동1(컴퓨터공학))와 2025학년도 1학기 CSE304-00(알고리즘)의 중간·기말 비율 합계를 각각 구하고, 두 번째 합계에서 첫 번째 합계를 뺀 차이도 알려줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J032 (O): 2025학년도 1학기 CSE405-00(졸업프로젝트)와 2026학년도 1학기 IE419-00(서비스데이터사이언스)의 중간·기말 비율 합계를 각각 구하고, 두 번째 합계에서 첫 번째 합계를 뺀 차이도 알려줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J033 (O): 2026학년도 2학기 EE209-02(논리회로)와 2026학년도 1학기 CSE204-01(자료구조) 중 중간고사 비율이 더 큰 강좌의 과목코드·연도·학기·분반·비율을 알려줘. 같으면 둘 다 알려줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J034 (O): 2026학년도 2학기 EE211-00(확률및랜덤변수)와 2026학년도 2학기 AI4007-00(독립심화학습(인공지능)2) 중 중간고사 비율이 더 큰 강좌의 과목코드·연도·학기·분반·비율을 알려줘. 같으면 둘 다 알려줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J035 (O): 2026학년도 2학기 SWCON401-02(소프트웨어융합캡스톤디자인)와 2026학년도 1학기 CSE301-01(운영체제) 중 중간고사 비율이 더 큰 강좌의 과목코드·연도·학기·분반·비율을 알려줘. 같으면 둘 다 알려줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J036 (O): 2025학년도 1학기 EE211-02(확률및랜덤변수)와 2025학년도 1학기 CSE438-00(최신기술콜로키움1) 중 중간고사 비율이 더 큰 강좌의 과목코드·연도·학기·분반·비율을 알려줘. 같으면 둘 다 알려줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J037 (O): 2026학년도 2학기 AI3100-00(몰입심화학습(AI로봇))와 2025학년도 2학기 ELC281-00(세계신화읽기) 중 과제 비율이 더 작은 강좌의 과목코드·연도·학기·분반·비율을 알려줘. 같으면 둘 다 알려줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J038 (O): 2025학년도 1학기 ME380-03(시스템동역학)와 2026학년도 2학기 AI4007-08(독립심화학습(인공지능)2) 중 과제 비율이 더 작은 강좌의 과목코드·연도·학기·분반·비율을 알려줘. 같으면 둘 다 알려줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J039 (O): 2025학년도 2학기 CSE406-03(캡스톤디자인)와 2025학년도 2학기 CSE442-00(블록체인) 중 과제 비율이 더 작은 강좌의 과목코드·연도·학기·분반·비율을 알려줘. 같으면 둘 다 알려줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J040 (O): 2026학년도 1학기 CSE0001-00(소프트웨어가치탐구)와 2025학년도 1학기 CSE204-00(자료구조) 중 과제 비율이 더 작은 강좌의 과목코드·연도·학기·분반·비율을 알려줘. 같으면 둘 다 알려줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J041 (O): 2025학년도 2학기 CSE103-00(객체지향프로그래밍)와 2026학년도 1학기 CSE406-06(캡스톤디자인)의 출석 비율을 순서대로 알려주고, 두 번째에서 첫 번째를 뺀 차이를 퍼센트포인트로 계산해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J042 (X): 2025학년도 1학기 SWCON103-00(디자인적사고)와 2026학년도 2학기 AI4007-02(독립심화학습(인공지능)2)의 출석 비율을 순서대로 알려주고, 두 번째에서 첫 번째를 뺀 차이를 퍼센트포인트로 계산해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J043 (O): 2025학년도 2학기 CSE302-01(컴퓨터네트워크)와 2026학년도 1학기 SWCON321-02(데이터분석캡스톤디자인)의 출석 비율을 순서대로 알려주고, 두 번째에서 첫 번째를 뺀 차이를 퍼센트포인트로 계산해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J044 (O): 2026학년도 2학기 SWCON401-02(소프트웨어융합캡스톤디자인)와 2026학년도 1학기 CSE301-01(운영체제)의 출석 비율을 순서대로 알려주고, 두 번째에서 첫 번째를 뺀 차이를 퍼센트포인트로 계산해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J045 (O): 2026학년도 1학기 IE419-00(서비스데이터사이언스) 담당 교수의 다른 수업 중, 같은 학기 소프트웨어융합학과 개설목록에서 산학필수인 강좌의 과목코드와 분반을 알려줘. 기준 과목의 다른 분반도 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J046 (X): 2026학년도 1학기 IE419-00(서비스데이터사이언스) 담당 교수의 다른 수업 중, 같은 학기 소프트웨어융합학과 개설목록에서 3학점인 강좌의 과목코드와 분반을 알려줘. 기준 과목의 다른 분반도 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J047 (X): 2026학년도 1학기 IE419-00(서비스데이터사이언스) 담당 교수가 같은 학기 소프트웨어융합학과 개설목록에서 맡은 다른 과목의 분반 수와 개설학점 합계를 알려줘. 기준 과목 코드는 제외하고, 다른 분반은 각각 합산해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J048 (O): 2025학년도 2학기 SWCON253-01(기계학습) 담당 교수의 다른 수업 중, 같은 학기 컴퓨터공학과 개설목록에서 전공필수인 강좌의 과목코드와 분반을 알려줘. 기준 과목의 다른 분반도 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J049 (O): 2025학년도 2학기 SWCON253-01(기계학습) 담당 교수의 다른 수업 중, 같은 학기 컴퓨터공학과 개설목록에서 산학필수인 강좌의 과목코드와 분반을 알려줘. 기준 과목의 다른 분반도 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J050 (O): 2025학년도 2학기 SWCON253-01(기계학습) 담당 교수의 다른 수업 중, 같은 학기 컴퓨터공학과 개설목록에서 3학점인 강좌의 과목코드와 분반을 알려줘. 기준 과목의 다른 분반도 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J051 (O): 2025학년도 2학기 SWCON253-01(기계학습)의 담당 교수가 2026학년도 2학기 컴퓨터공학과 개설목록에서 맡은 다른 과목의 코드와 분반을 알려줘. 기준 과목 코드는 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J052 (O): 2025학년도 1학기 CSE406-05(캡스톤디자인) 담당 교수의 다른 수업 중, 같은 학기 컴퓨터공학과 개설목록에서 산학필수인 강좌의 과목코드와 분반을 알려줘. 기준 과목의 다른 분반도 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J053 (O): 2025학년도 1학기 CSE406-05(캡스톤디자인) 담당 교수의 다른 수업 중, 같은 학기 컴퓨터공학과 개설목록에서 3학점인 강좌의 과목코드와 분반을 알려줘. 기준 과목의 다른 분반도 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J054 (O): 2026학년도 1학기 CSE304-01(알고리즘) 담당 교수의 다른 수업 중, 같은 학기 컴퓨터공학과 개설목록에서 전공필수인 강좌의 과목코드와 분반을 알려줘. 기준 과목의 다른 분반도 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J055 (O): 2026학년도 1학기 CSE304-01(알고리즘) 담당 교수의 다른 수업 중, 같은 학기 컴퓨터공학과 개설목록에서 산학필수인 강좌의 과목코드와 분반을 알려줘. 기준 과목의 다른 분반도 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J056 (O): 2026학년도 1학기 CSE304-01(알고리즘) 담당 교수의 다른 수업 중, 같은 학기 컴퓨터공학과 개설목록에서 3학점인 강좌의 과목코드와 분반을 알려줘. 기준 과목의 다른 분반도 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J057 (X): 2026학년도 1학기 CSE304-01(알고리즘) 담당 교수가 같은 학기 컴퓨터공학과 개설목록에서 맡은 다른 과목의 분반 수와 개설학점 합계를 알려줘. 기준 과목 코드는 제외하고, 다른 분반은 각각 합산해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J058 (O): 2026학년도 1학기 AI4003-00(졸업논문(인공지능)) 담당 교수의 다른 수업 중, 같은 학기 인공지능학과 개설목록에서 전공필수인 강좌의 과목코드와 분반을 알려줘. 기준 과목의 다른 분반도 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J059 (X): 2026학년도 1학기 AI4003-00(졸업논문(인공지능)) 담당 교수가 같은 학기 인공지능학과 개설목록에서 맡은 다른 과목의 분반 수와 개설학점 합계를 알려줘. 기준 과목 코드는 제외하고, 다른 분반은 각각 합산해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J060 (O): 2026학년도 1학기 CSE423-00(정보보호) 담당 교수의 다른 수업 중, 같은 학기 컴퓨터공학과 개설목록에서 전공필수인 강좌의 과목코드와 분반을 알려줘. 기준 과목의 다른 분반도 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J061 (X): 2026학년도 1학기 CSE423-00(정보보호) 담당 교수가 같은 학기 컴퓨터공학과 개설목록에서 맡은 다른 과목의 분반 수와 개설학점 합계를 알려줘. 기준 과목 코드는 제외하고, 다른 분반은 각각 합산해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J062 (O): 2025학년도 1학기 SWCON253-00(기계학습)의 담당 교수가 2026학년도 1학기 소프트웨어융합학과 개설목록에서 맡은 다른 과목의 코드와 분반을 알려줘. 기준 과목 코드는 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J063 (O): 2025학년도 1학기 CSE423-00(정보보호)의 담당 교수가 2026학년도 1학기 컴퓨터공학과 개설목록에서 맡은 다른 과목의 코드와 분반을 알려줘. 기준 과목 코드는 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J064 (X): 2025학년도 2학기 CSE497-02(연구연수활동2(컴퓨터공학))의 담당 교수가 2026학년도 2학기 컴퓨터공학과 개설목록에서 맡은 다른 과목의 코드와 분반을 알려줘. 기준 과목 코드는 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J065 (O): 2026학년도 1학기 IE419-00(서비스데이터사이언스)와 2025학년도 2학기 IE306-00(데이터마이닝)를 모두 담당한 교수 이름을 알려줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J066 (O): 2025학년도 2학기 AI4007-00(독립심화학습(인공지능)2)와 2026학년도 1학기 CSE204-01(자료구조)를 모두 담당한 교수 이름을 알려줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J067 (O): 2025학년도 2학기 SWCON253-01(기계학습)와 2026학년도 2학기 CSE497-03(연구연수활동2(컴퓨터공학))를 모두 담당한 교수 이름을 알려줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J068 (O): 2025학년도 1학기 CSE406-05(캡스톤디자인)와 2026학년도 2학기 SWCON313-00(가상현실)를 모두 담당한 교수 이름을 알려줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J069 (O): 2026학년도 1학기 IE419-00(서비스데이터사이언스)와 2026학년도 1학기 SWCON104-01(웹/파이선프로그래밍)의 정규 수업시간이 일주일에 총 몇 분 겹쳐? 시험 일정은 제외하고 요일별 겹치는 구간만 합산해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J070 (O): 2025학년도 2학기 AI4007-00(독립심화학습(인공지능)2)와 2025학년도 2학기 SWCON401-08(소프트웨어융합캡스톤디자인)의 정규 수업시간이 일주일에 총 몇 분 겹쳐? 시험 일정은 제외하고 요일별 겹치는 구간만 합산해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J071 (O): 2025학년도 2학기 SWCON253-01(기계학습)와 2025학년도 2학기 CSE103-01(객체지향프로그래밍)의 정규 수업시간이 일주일에 총 몇 분 겹쳐? 시험 일정은 제외하고 요일별 겹치는 구간만 합산해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J072 (O): 2026학년도 1학기 CSE304-01(알고리즘)와 2026학년도 1학기 EE210-01(신호와시스템)의 정규 수업시간이 일주일에 총 몇 분 겹쳐? 시험 일정은 제외하고 요일별 겹치는 구간만 합산해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J073 (O): 다음 세 강좌 중 중간·기말 비율 합계가 70% 이상인 강좌의 과목코드·연도·학기·분반·합계를 알려줘: 2025학년도 1학기 CSE406-01(캡스톤디자인), 2026학년도 1학기 AI4003-00(졸업논문(인공지능)), 2025학년도 1학기 CSE405-00(졸업프로젝트). — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J074 (O): 이 세 강좌 중 과제 비율이 가장 낮은 강좌의 과목코드·연도·학기·분반·과제 비율을 알려줘. 동률은 모두 포함해줘: 2025학년도 1학기 CSE406-01(캡스톤디자인), 2026학년도 1학기 AI4003-00(졸업논문(인공지능)), 2025학년도 1학기 CSE405-00(졸업프로젝트). — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J075 (O): 다음 세 강좌 중 중간·기말 비율 합계가 70% 이상인 강좌의 과목코드·연도·학기·분반·합계를 알려줘: 2026학년도 1학기 IE419-00(서비스데이터사이언스), 2025학년도 2학기 CSE497-02(연구연수활동2(컴퓨터공학)), 2026학년도 1학기 EE209-01(논리회로). — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J076 (O): 이 세 강좌 중 과제 비율이 가장 낮은 강좌의 과목코드·연도·학기·분반·과제 비율을 알려줘. 동률은 모두 포함해줘: 2026학년도 1학기 IE419-00(서비스데이터사이언스), 2025학년도 2학기 CSE497-02(연구연수활동2(컴퓨터공학)), 2026학년도 1학기 EE209-01(논리회로). — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J077 (O): 다음 세 강좌 중 중간·기말 비율 합계가 70% 이상인 강좌의 과목코드·연도·학기·분반·합계를 알려줘: 2025학년도 2학기 CSE302-01(컴퓨터네트워크), 2026학년도 1학기 SWCON321-02(데이터분석캡스톤디자인), 2026학년도 2학기 CSE406-16(캡스톤디자인). — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J078 (O): 이 세 강좌 중 과제 비율이 가장 낮은 강좌의 과목코드·연도·학기·분반·과제 비율을 알려줘. 동률은 모두 포함해줘: 2025학년도 2학기 CSE302-01(컴퓨터네트워크), 2026학년도 1학기 SWCON321-02(데이터분석캡스톤디자인), 2026학년도 2학기 CSE406-16(캡스톤디자인). — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J079 (O): 다음 세 강좌 중 중간·기말 비율 합계가 70% 이상인 강좌의 과목코드·연도·학기·분반·합계를 알려줘: 2025학년도 1학기 CSE327-00(소프트웨어공학), 2025학년도 1학기 CSE496-06(연구연수활동1(컴퓨터공학)), 2025학년도 1학기 CSE304-00(알고리즘). — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J080 (O): 이 세 강좌 중 과제 비율이 가장 낮은 강좌의 과목코드·연도·학기·분반·과제 비율을 알려줘. 동률은 모두 포함해줘: 2025학년도 1학기 CSE327-00(소프트웨어공학), 2025학년도 1학기 CSE496-06(연구연수활동1(컴퓨터공학)), 2025학년도 1학기 CSE304-00(알고리즘). — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J081 (X): 2026학년도 1학기 소프트웨어융합학과 원천 개설목록에서 전공필수로 분류된 강좌의 분반 수와 개설학점 합계를 알려줘. 분반별로 각각 계산해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J082 (X): 2025학년도 2학기 인공지능학과 원천 개설목록에서 전공필수로 분류된 강좌의 분반 수와 개설학점 합계를 알려줘. 분반별로 각각 계산해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J083 (X): 2025학년도 2학기 소프트웨어융합학과 원천 개설목록에서 전공필수로 분류된 강좌의 분반 수와 개설학점 합계를 알려줘. 분반별로 각각 계산해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J084 (X): 2025학년도 1학기 컴퓨터공학과 원천 개설목록에서 전공필수로 분류된 강좌의 분반 수와 개설학점 합계를 알려줘. 분반별로 각각 계산해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J085 (O): 2025학년도 2학기 CSE406-01(캡스톤디자인)에서 중간고사 80점, 기말고사 90점(각 100점 만점)을 받았다고 가정하면 두 시험이 최종 100점에 기여하는 점수 합은? 다른 항목과 추가 보정은 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J086 (O): 2026학년도 1학기 CSE438-00(최신기술콜로키움1)에서 중간고사 80점, 기말고사 90점(각 100점 만점)을 받았다고 가정하면 두 시험이 최종 100점에 기여하는 점수 합은? 다른 항목과 추가 보정은 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J087 (O): 2025학년도 2학기 AI4007-00(독립심화학습(인공지능)2)에서 중간고사 80점, 기말고사 90점(각 100점 만점)을 받았다고 가정하면 두 시험이 최종 100점에 기여하는 점수 합은? 다른 항목과 추가 보정은 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J088 (O): 2025학년도 2학기 SWCON201-00(오픈소스SW개발방법및도구)에서 중간고사 80점, 기말고사 90점(각 100점 만점)을 받았다고 가정하면 두 시험이 최종 100점에 기여하는 점수 합은? 다른 항목과 추가 보정은 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J089 (O): [가상 학생 202210001] 내 가상 수강이력에서 완료됐고 재수강으로 대체되지 않은 기록의 학점 합계는 얼마야? — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J090 (O): [가상 학생 202210002] 내 가상 수강이력 중 재수강으로 대체된 과거 기록은 몇 건이야? — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J091 (O): [가상 학생 202310003] 내 가상 수강이력을 완료·미이수 등 기록된 상태별로 나눠 각각 몇 건인지 알려줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J092 (O): [가상 학생 202510004] 내 가상 수강이력에서 완료됐고 재수강으로 대체되지 않은 기록의 학점 합계는 얼마야? — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J093 (O): [가상 학생 202410005] 내 가상 수강이력 중 재수강으로 대체된 과거 기록은 몇 건이야? — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J094 (O): [가상 학생 202410006] 내 가상 수강이력을 완료·미이수 등 기록된 상태별로 나눠 각각 몇 건인지 알려줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J095 (O): 2023학번 일반 신입학생의 후마니타스 기본구조표에서 총 교양학점, 배분이수 학점, 최소 영역 수, 영역당 학점은 각각 얼마야? 면제·대체·편입 예외는 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J096 (X): 2024학번 일반 신입학생의 후마니타스 기본구조표에서 총 교양학점, 배분이수 학점, 최소 영역 수, 영역당 학점은 각각 얼마야? 면제·대체·편입 예외는 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J097 (O): 2023학번과 2024학번 기본구조표를 비교하면 2024학번의 총 교양 최소학점과 배분이수 최소학점은 각각 몇 학점 줄었어? 면제·대체 예외는 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J098 (X): 2024학번 일반 신입학생이 배분이수 6학점을 취득했고, 영역당 3학점 기준을 채운 영역은 2개라고 가정하자. 기본구조표 기준 부족 학점·부족 영역 수와 두 조건 충족 여부(1/0)는? 편입·면제 예외는 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J099 (X): 2024학번 일반 신입학생이 배분이수 9학점을 취득했고, 영역당 3학점 기준을 채운 영역은 2개라고 가정하자. 기본구조표 기준 부족 학점·부족 영역 수와 두 조건 충족 여부(1/0)는? 편입·면제 예외는 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J100 (X): 2024학번 일반 신입학생이 배분이수 12학점을 취득했고, 영역당 3학점 기준을 채운 영역은 4개라고 가정하자. 기본구조표 기준 부족 학점·부족 영역 수와 두 조건 충족 여부(1/0)는? 편입·면제 예외는 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.

## 오답 목록

### J012 — correct_extra_columns
질문: 2026학년도 1학기 CSE301-01(운영체제)의 담당 교수 이름과 학점을 알려줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
SELECT
    o.course_name,
    o.credits,
    GROUP_CONCAT(p.name, ', ') AS professor_names
FROM course_offerings AS o
LEFT JOIN offering_professors AS op
    ON op.offering_id = o.offering_id
LEFT JOIN professors AS p
    ON p.professor_id = op.professor_id
WHERE o.course_code = 'CSE301'
  AND o.year = 2026
  AND o.semester = '1'
  AND o.section = '01'
GROUP BY o.offering_id;
```
정답 컬럼: professor_name, credits / 예측 컬럼: course_name, credits, professor_names
정답 행 수: 1 / 예측 행 수: 1

### J015 — correct_extra_columns
질문: 2025학년도 1학기 EE211-02(확률및랜덤변수)의 담당 교수 이름과 학점을 알려줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
SELECT
    o.course_name,
    GROUP_CONCAT(p.name, ', ') AS professor_names,
    o.credits
FROM course_offerings AS o
LEFT JOIN offering_professors AS op ON op.offering_id = o.offering_id
LEFT JOIN professors AS p ON p.professor_id = op.professor_id
WHERE o.course_code = 'EE211'
  AND o.section = '02'
  AND o.year = 2025
  AND o.semester = '1'
  AND o.course_name LIKE '%확률및랜덤변수%'
GROUP BY o.offering_id;
```
정답 컬럼: professor_name, credits / 예측 컬럼: course_name, professor_names, credits
정답 행 수: 1 / 예측 행 수: 1

### J019 — row_count_mismatch
질문: 2026학년도 2학기 AI4007-07(독립심화학습(인공지능)2)의 영어강좌 구분(영어전체/영어부분/해당없음)과 산학필수 여부(예/아니오)를 알려줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
SELECT
    CASE o.english_type
        WHEN 'FULL' THEN '영어전체'
        WHEN 'PARTIAL' THEN '영어부분'
        WHEN 'NONE' THEN '해당없음'
        WHEN 'SECOND_FOREIGN_LANGUAGE' THEN '제2외국어'
    END AS 영어강좌_구분,
    CASE o.industry_required
        WHEN 1 THEN '예'
        WHEN 0 THEN '아니오'
    END AS 산학필수_여부
FROM course_offerings AS o
WHERE o.course_code = 'AI4007-07'
  AND o.section = '07'
  AND o.year = 2026
  AND o.semester = '2';
```
정답 컬럼: english_classification, industry_required / 예측 컬럼: 영어강좌_구분, 산학필수_여부
정답 행 수: 1 / 예측 행 수: 0

### J042 — value_mismatch
질문: 2025학년도 1학기 SWCON103-00(디자인적사고)와 2026학년도 2학기 AI4007-02(독립심화학습(인공지능)2)의 출석 비율을 순서대로 알려주고, 두 번째에서 첫 번째를 뺀 차이를 퍼센트포인트로 계산해줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
WITH first_course AS (
    SELECT MAX(s.attendance_percentage) AS attendance_percentage
    FROM course_offerings AS o
    JOIN syllabi AS s ON s.offering_id = o.offering_id
    WHERE o.course_code = 'SWCON103-00'
      AND o.year = 2025
      AND o.semester = '1'
      AND o.course_name LIKE '%디자인적사고%'
),
second_course AS (
    SELECT MAX(s.attendance_percentage) AS attendance_percentage
    FROM course_offerings AS o
    JOIN syllabi AS s ON s.offering_id = o.offering_id
    WHERE o.course_code = 'AI4007-02'
      AND o.year = 2026
      AND o.semester = '2'
      AND o.course_name LIKE '%독립심화학습(인공지능)2%'
)
SELECT
    first_course.attendance_percentage AS first_attendance_percentage,
    second_course.attendance_percentage AS second_attendance_percentage,
    second_course.attendance_percentage - first_course.attendance_percentage
        AS difference_percentage_points
FROM first_course
CROSS JOIN second_course;
```
정답 컬럼: first_percentage, second_percentage, second_minus_first_pp / 예측 컬럼: first_attendance_percentage, second_attendance_percentage, difference_percentage_points
정답 행 수: 1 / 예측 행 수: 1

### J046 — row_count_mismatch
질문: 2026학년도 1학기 IE419-00(서비스데이터사이언스) 담당 교수의 다른 수업 중, 같은 학기 소프트웨어융합학과 개설목록에서 3학점인 강좌의 과목코드와 분반을 알려줘. 기준 과목의 다른 분반도 제외해줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
WITH target_professors AS (
    SELECT op.professor_id
    FROM course_offerings AS o
    JOIN offering_professors AS op ON op.offering_id = o.offering_id
    WHERE o.course_code = 'IE419'
      AND o.section = '00'
      AND o.year = 2026
      AND o.semester = '1'
)
SELECT DISTINCT
    other.course_code,
    other.section
FROM course_offerings AS other
JOIN courses AS c ON c.course_code = other.course_code
JOIN departments AS d ON d.department_id = c.department_id
JOIN offering_professors AS op ON op.offering_id = other.offering_id
WHERE op.professor_id IN (SELECT professor_id FROM target_professors)
  AND other.year = 2026
  AND other.semester = '1'
  AND other.credits = 3
  AND d.name = '소프트웨어융합학과'
  AND other.course_code <> 'IE419'
ORDER BY other.course_code, other.section;
```
정답 컬럼: course_code, section / 예측 컬럼: course_code, section
정답 행 수: 2 / 예측 행 수: 0

### J047 — value_mismatch
질문: 2026학년도 1학기 IE419-00(서비스데이터사이언스) 담당 교수가 같은 학기 소프트웨어융합학과 개설목록에서 맡은 다른 과목의 분반 수와 개설학점 합계를 알려줘. 기준 과목 코드는 제외하고, 다른 분반은 각각 합산해줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
WITH target_professors AS (
    SELECT DISTINCT p.professor_id, p.name
    FROM course_offerings AS target
    JOIN offering_professors AS target_op
      ON target_op.offering_id = target.offering_id
    JOIN professors AS p
      ON p.professor_id = target_op.professor_id
    WHERE target.course_code = 'IE419'
      AND target.section = '00'
      AND target.year = 2026
      AND target.semester = '1'
)
SELECT
    tp.name AS professor_name,
    COUNT(DISTINCT o.offering_id) AS section_count,
    COALESCE(SUM(o.credits), 0) AS total_credits
FROM target_professors AS tp
LEFT JOIN offering_professors AS op
  ON op.professor_id = tp.professor_id
LEFT JOIN course_offerings AS o
  ON o.offering_id = op.offering_id
 AND o.year = 2026
 AND o.semester = '1'
 AND o.course_code <> 'IE419'
LEFT JOIN courses AS c
  ON c.course_code = o.course_code
 AND c.department_id = 8
WHERE o.offering_id IS NULL
   OR c.course_code IS NOT NULL
GROUP BY tp.professor_id, tp.name
ORDER BY tp.name;
```
정답 컬럼: offering_count, offering_credit_sum / 예측 컬럼: professor_name, section_count, total_credits
정답 행 수: 1 / 예측 행 수: 1

### J057 — correct_extra_columns
질문: 2026학년도 1학기 CSE304-01(알고리즘) 담당 교수가 같은 학기 컴퓨터공학과 개설목록에서 맡은 다른 과목의 분반 수와 개설학점 합계를 알려줘. 기준 과목 코드는 제외하고, 다른 분반은 각각 합산해줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
WITH target_professors AS (
    SELECT DISTINCT p.professor_id, p.name
    FROM course_offerings AS target
    JOIN offering_professors AS target_op
        ON target_op.offering_id = target.offering_id
    JOIN professors AS p
        ON p.professor_id = target_op.professor_id
    WHERE target.course_code = 'CSE304'
      AND target.section = '01'
      AND target.year = 2026
      AND target.semester = '1'
)
SELECT
    tp.name AS professor_name,
    COUNT(o.offering_id) AS other_section_count,
    COALESCE(SUM(o.credits), 0) AS total_credits
FROM target_professors AS tp
LEFT JOIN offering_professors AS op
    ON op.professor_id = tp.professor_id
LEFT JOIN course_offerings AS o
    ON o.offering_id = op.offering_id
   AND o.year = 2026
   AND o.semester = '1'
   AND o.course_code <> 'CSE304'
LEFT JOIN courses AS c
    ON c.course_code = o.course_code
LEFT JOIN departments AS d
    ON d.department_id = c.department_id
   AND d.name = '컴퓨터공학과'
WHERE o.offering_id IS NULL
   OR d.department_id IS NOT NULL
GROUP BY tp.professor_id, tp.name
ORDER BY tp.name;
```
정답 컬럼: offering_count, offering_credit_sum / 예측 컬럼: professor_name, other_section_count, total_credits
정답 행 수: 1 / 예측 행 수: 1

### J059 — value_mismatch
질문: 2026학년도 1학기 AI4003-00(졸업논문(인공지능)) 담당 교수가 같은 학기 인공지능학과 개설목록에서 맡은 다른 과목의 분반 수와 개설학점 합계를 알려줘. 기준 과목 코드는 제외하고, 다른 분반은 각각 합산해줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
WITH target_professors AS (
    SELECT DISTINCT p.professor_id, p.name
    FROM course_offerings AS o
    JOIN offering_professors AS op ON op.offering_id = o.offering_id
    JOIN professors AS p ON p.professor_id = op.professor_id
    WHERE o.course_code = 'AI4003'
      AND o.section = '00'
      AND o.year = 2026
      AND o.semester = '1'
),
other_offerings AS (
    SELECT DISTINCT
        tp.professor_id,
        o.offering_id,
        o.credits
    FROM target_professors AS tp
    JOIN offering_professors AS op ON op.professor_id = tp.professor_id
    JOIN course_offerings AS o ON o.offering_id = op.offering_id
    JOIN courses AS c ON c.course_code = o.course_code
    JOIN departments AS d ON d.department_id = c.department_id
    WHERE o.year = 2026
      AND o.semester = '1'
      AND o.course_code <> 'AI4003'
      AND d.name = '인공지능학과'
)
SELECT
    tp.name AS professor_name,
    COUNT(oo.offering_id) AS other_section_count,
    COALESCE(SUM(oo.credits), 0) AS total_credits
FROM target_professors AS tp
LEFT JOIN other_offerings AS oo ON oo.professor_id = tp.professor_id
GROUP BY tp.professor_id, tp.name
ORDER BY tp.name;
```
정답 컬럼: offering_count, offering_credit_sum / 예측 컬럼: professor_name, other_section_count, total_credits
정답 행 수: 1 / 예측 행 수: 1

### J061 — correct_extra_columns
질문: 2026학년도 1학기 CSE423-00(정보보호) 담당 교수가 같은 학기 컴퓨터공학과 개설목록에서 맡은 다른 과목의 분반 수와 개설학점 합계를 알려줘. 기준 과목 코드는 제외하고, 다른 분반은 각각 합산해줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
WITH target_professors AS (
    SELECT DISTINCT op.professor_id
    FROM course_offerings AS target
    JOIN offering_professors AS op
        ON op.offering_id = target.offering_id
    WHERE target.course_code = 'CSE423'
      AND target.year = 2026
      AND target.semester = '1'
      AND target.section = '00'
)
SELECT
    p.name AS professor_name,
    COUNT(DISTINCT o.offering_id) AS other_section_count,
    COALESCE(SUM(o.credits), 0) AS total_credits
FROM target_professors AS tp
JOIN professors AS p
    ON p.professor_id = tp.professor_id
LEFT JOIN offering_professors AS op
    ON op.professor_id = tp.professor_id
LEFT JOIN course_offerings AS o
    ON o.offering_id = op.offering_id
   AND o.year = 2026
   AND o.semester = '1'
   AND o.course_code <> 'CSE423'
LEFT JOIN courses AS c
    ON c.course_code = o.course_code
LEFT JOIN departments AS d
    ON d.department_id = c.department_id
   AND d.name = '컴퓨터공학과'
WHERE o.offering_id IS NULL
   OR d.department_id IS NOT NULL
GROUP BY p.professor_id, p.name
ORDER BY p.name;
```
정답 컬럼: offering_count, offering_credit_sum / 예측 컬럼: professor_name, other_section_count, total_credits
정답 행 수: 1 / 예측 행 수: 1

### J064 — row_count_mismatch
질문: 2025학년도 2학기 CSE497-02(연구연수활동2(컴퓨터공학))의 담당 교수가 2026학년도 2학기 컴퓨터공학과 개설목록에서 맡은 다른 과목의 코드와 분반을 알려줘. 기준 과목 코드는 제외해줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
WITH source_professors AS (
    SELECT DISTINCT op.professor_id
    FROM course_offerings AS o
    JOIN offering_professors AS op ON op.offering_id = o.offering_id
    WHERE o.year = 2025
      AND o.semester = '2'
      AND o.course_code = 'CSE497'
      AND o.section = '02'
)
SELECT DISTINCT
    o.course_code,
    o.section
FROM course_offerings AS o
JOIN courses AS c ON c.course_code = o.course_code
JOIN departments AS d ON d.department_id = c.department_id
JOIN offering_professors AS op ON op.offering_id = o.offering_id
JOIN source_professors AS sp ON sp.professor_id = op.professor_id
WHERE o.year = 2026
  AND o.semester = '2'
  AND d.name = '컴퓨터공학과'
  AND o.course_code <> 'CSE497'
ORDER BY o.course_code, o.section;
```
정답 컬럼: course_code, section / 예측 컬럼: course_code, section
정답 행 수: 4 / 예측 행 수: 3

### J081 — row_count_mismatch
질문: 2026학년도 1학기 소프트웨어융합학과 원천 개설목록에서 전공필수로 분류된 강좌의 분반 수와 개설학점 합계를 알려줘. 분반별로 각각 계산해줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
WITH target_offerings AS (
    SELECT DISTINCT
        o.offering_id,
        o.course_code,
        o.course_name,
        o.credits,
        o.section
    FROM course_offerings AS o
    JOIN course_offering_categories AS oc
      ON oc.offering_id = o.offering_id
    JOIN departments AS d
      ON d.department_id = oc.department_id
    JOIN course_categories AS cc
      ON cc.category_id = oc.category_id
    WHERE d.name = '소프트웨어융합학과'
      AND cc.category_name = '전공필수'
      AND o.year = 2026
      AND o.semester = '1'
)
SELECT
    course_code,
    course_name,
    COUNT(DISTINCT section) AS section_count,
    SUM(credits) AS total_offering_credits
FROM target_offerings
GROUP BY course_code, course_name
ORDER BY course_code;
```
정답 컬럼: offering_count, offering_credit_sum / 예측 컬럼: course_code, course_name, section_count, total_offering_credits
정답 행 수: 1 / 예측 행 수: 11

### J082 — row_count_mismatch
질문: 2025학년도 2학기 인공지능학과 원천 개설목록에서 전공필수로 분류된 강좌의 분반 수와 개설학점 합계를 알려줘. 분반별로 각각 계산해줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
SELECT
    c.course_code,
    o.course_name,
    COUNT(DISTINCT o.section) AS section_count,
    SUM(o.credits) AS total_offering_credits
FROM course_offerings AS o
JOIN courses AS c
    ON c.course_code = o.course_code
JOIN departments AS d
    ON d.department_id = c.department_id
WHERE d.name = '인공지능학과'
  AND o.year = 2025
  AND o.semester = '2'
  AND EXISTS (
      SELECT 1
      FROM course_offering_categories AS coc
      JOIN course_categories AS cc
          ON cc.category_id = coc.category_id
      WHERE coc.offering_id = o.offering_id
        AND cc.category_name = '전공필수'
  )
GROUP BY c.course_code, o.course_name
ORDER BY c.course_code;
```
정답 컬럼: offering_count, offering_credit_sum / 예측 컬럼: course_code, course_name, section_count, total_offering_credits
정답 행 수: 1 / 예측 행 수: 2

### J083 — row_count_mismatch
질문: 2025학년도 2학기 소프트웨어융합학과 원천 개설목록에서 전공필수로 분류된 강좌의 분반 수와 개설학점 합계를 알려줘. 분반별로 각각 계산해줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
WITH classified_offerings AS (
    SELECT DISTINCT
        o.offering_id,
        o.course_code,
        o.course_name,
        o.section,
        o.credits
    FROM course_offerings AS o
    JOIN courses AS c ON c.course_code = o.course_code
    JOIN departments AS d ON d.department_id = c.department_id
    JOIN course_offering_categories AS oc ON oc.offering_id = o.offering_id
    JOIN course_categories AS cc ON cc.category_id = oc.category_id
    WHERE d.name = '소프트웨어융합학과'
      AND oc.department_id = d.department_id
      AND cc.category_name = '전공필수'
      AND o.year = 2025
      AND o.semester = '2'
)
SELECT
    course_code,
    course_name,
    COUNT(DISTINCT section) AS section_count,
    SUM(credits) AS total_offered_credits
FROM classified_offerings
GROUP BY course_code, course_name
ORDER BY course_code;
```
정답 컬럼: offering_count, offering_credit_sum / 예측 컬럼: course_code, course_name, section_count, total_offered_credits
정답 행 수: 1 / 예측 행 수: 7

### J084 — row_count_mismatch
질문: 2025학년도 1학기 컴퓨터공학과 원천 개설목록에서 전공필수로 분류된 강좌의 분반 수와 개설학점 합계를 알려줘. 분반별로 각각 계산해줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
WITH classified_offerings AS (
    SELECT DISTINCT
        o.offering_id,
        o.section,
        o.credits
    FROM course_offerings AS o
    JOIN courses AS c ON c.course_code = o.course_code
    JOIN departments AS d ON d.department_id = c.department_id
    JOIN course_offering_categories AS oc ON oc.offering_id = o.offering_id
    JOIN course_categories AS cc ON cc.category_id = oc.category_id
    WHERE d.name = '컴퓨터공학과'
      AND cc.category_name = '전공필수'
      AND o.year = 2025
      AND o.semester = '1'
)
SELECT
    section,
    COUNT(*) AS course_count,
    SUM(credits) AS total_credits
FROM classified_offerings
GROUP BY section
ORDER BY section;
```
정답 컬럼: offering_count, offering_credit_sum / 예측 컬럼: section, course_count, total_credits
정답 행 수: 1 / 예측 행 수: 13

### J096 — row_count_mismatch
질문: 2024학번 일반 신입학생의 후마니타스 기본구조표에서 총 교양학점, 배분이수 학점, 최소 영역 수, 영역당 학점은 각각 얼마야? 면제·대체·편입 예외는 제외해줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
SELECT
    r.total_general_credits,
    c.min_credits AS distribution_min_credits,
    c.min_areas AS distribution_min_areas,
    c.per_area_min_credits AS distribution_per_area_min_credits
FROM general_education_requirements AS r
JOIN general_education_requirement_categories AS c
    ON c.general_requirement_id = r.general_requirement_id
WHERE r.cohort_start <= 2024
  AND (r.cohort_end IS NULL OR r.cohort_end >= 2024)
  AND r.source_document LIKE '%후마니타스%'
  AND c.requirement_code = 'DISTRIBUTION';
```
정답 컬럼: total_general_credits, distribution_credits, min_areas, per_area_min_credits / 예측 컬럼: total_general_credits, distribution_min_credits, distribution_min_areas, distribution_per_area_min_credits
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
    MAX(0, gc.min_credits - 6) AS 부족_학점,
    MAX(0, COALESCE(gc.min_areas, 0) - 2) AS 부족_영역_수,
    CASE WHEN 6 >= gc.min_credits THEN 1 ELSE 0 END AS 학점_조건_충족,
    CASE WHEN gc.min_areas IS NULL OR 2 >= gc.min_areas THEN 1 ELSE 0 END AS 영역_조건_충족
FROM general_education_requirements AS gr
JOIN general_education_requirement_categories AS gc
    ON gc.general_requirement_id = gr.general_requirement_id
WHERE gr.cohort_start <= 2024
  AND (gr.cohort_end IS NULL OR gr.cohort_end >= 2024)
  AND gc.requirement_code = 'DISTRIBUTION';
```
정답 컬럼: remaining_credits, remaining_areas, meets_both / 예측 컬럼: 부족_학점, 부족_영역_수, 학점_조건_충족, 영역_조건_충족
정답 행 수: 1 / 예측 행 수: 1

### J099 — row_count_mismatch
질문: 2024학번 일반 신입학생이 배분이수 9학점을 취득했고, 영역당 3학점 기준을 채운 영역은 2개라고 가정하자. 기본구조표 기준 부족 학점·부족 영역 수와 두 조건 충족 여부(1/0)는? 편입·면제 예외는 제외해줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
SELECT
    gc.min_credits,
    MAX(0, gc.min_credits - 9) AS 부족_학점,
    gc.min_areas,
    MAX(0, COALESCE(gc.min_areas, 0) - 2) AS 부족_영역_수,
    CASE WHEN 9 >= gc.min_credits THEN 1 ELSE 0 END AS 학점조건_충족,
    CASE WHEN gc.min_areas IS NULL OR 2 >= gc.min_areas THEN 1 ELSE 0 END AS 영역조건_충족
FROM general_education_requirements AS gr
JOIN general_education_requirement_categories AS gc
    ON gc.general_requirement_id = gr.general_requirement_id
WHERE gr.cohort_start <= 2024
  AND (gr.cohort_end IS NULL OR gr.cohort_end >= 2024)
  AND gr.source_document LIKE '%기본구조표%'
  AND gc.requirement_code = 'DISTRIBUTION';
```
정답 컬럼: remaining_credits, remaining_areas, meets_both / 예측 컬럼: min_credits, 부족_학점, min_areas, 부족_영역_수, 학점조건_충족, 영역조건_충족
정답 행 수: 1 / 예측 행 수: 0

### J100 — correct_extra_columns
질문: 2024학번 일반 신입학생이 배분이수 12학점을 취득했고, 영역당 3학점 기준을 채운 영역은 4개라고 가정하자. 기본구조표 기준 부족 학점·부족 영역 수와 두 조건 충족 여부(1/0)는? 편입·면제 예외는 제외해줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
SELECT
    MAX(0, gc.min_credits - 12) AS 부족_학점,
    CASE
        WHEN gc.min_areas IS NULL THEN 0
        ELSE MAX(0, gc.min_areas - 4)
    END AS 부족_영역_수,
    CASE WHEN 12 >= gc.min_credits THEN 1 ELSE 0 END AS 학점_조건_충족,
    CASE
        WHEN (gc.min_areas IS NULL OR 4 >= gc.min_areas)
         AND (gc.per_area_min_credits IS NULL OR 3 >= gc.per_area_min_credits)
        THEN 1
        ELSE 0
    END AS 영역_조건_충족
FROM general_education_requirements AS gr
JOIN general_education_requirement_categories AS gc
    ON gc.general_requirement_id = gr.general_requirement_id
WHERE gr.cohort_start <= 2024
  AND (gr.cohort_end IS NULL OR gr.cohort_end >= 2024)
  AND gc.requirement_code = 'DISTRIBUTION';
```
정답 컬럼: remaining_credits, remaining_areas, meets_both / 예측 컬럼: 부족_학점, 부족_영역_수, 학점_조건_충족, 영역_조건_충족
정답 행 수: 1 / 예측 행 수: 1


## 진단 코드 설명

- correct: 결과 완전 일치 / correct_extra_columns: 컬럼이 더 있거나 컬럼 순서가 다름(relaxed 정답)
- missing_columns: 예측 값은 모두 맞지만 정답의 일부 컬럼이 빠짐(subset 정답, 사람이 확인)
- order_mismatch: 행 정렬만 다름(relaxed 정답) / row_count_mismatch: 행 수가 다름 / value_mismatch: 행 수는 같지만 값이 다름
- exec_fail:sqlite 실행 오류 / exec_fail:guard 안전장치에 의해 거부 / exec_fail:no_sql SQL 추출 실패
- exec_fail:timeout 시간 초과 / exec_fail:refused 거부하면 안 되는 질문을 거부
- correct_refusal: 거부가 정답인 문항을 거부·차단 / no_leak_but_not_refused: 거부는 안 했지만 결과 0행
- should_have_refused: 거부해야 하는데 결과를 돌려줌 / api_error ChatKHU 호출 실패 / gold_invalid 정답 SQL 문제
