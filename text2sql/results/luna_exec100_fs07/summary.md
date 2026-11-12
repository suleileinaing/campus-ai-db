# Text2SQL 평가 결과 (2026-11-05 19:10)

| 지표 | 값 |
|---|---|
| 평가 문항 수 | 100 |
| 실행 성공률(최종) | 100/100 (100.0%) |
| 실행 성공률(1차 시도) | 98/100 (98.0%) |
| 정답률 strict | 77/100 (77.0%) |
| 정답률 relaxed | 88/100 (88.0%) |
| 정답률 subset (정답 일부 컬럼 누락 허용) | 88/100 (88.0%) |
| 평균 토큰 | 5117.7 |
| 평균 응답시간(초) | 5.94 |

## 유형별

| 태그 | n | strict | relaxed | subset | 실행 성공 |
|---|---|---|---|---|---|
| arithmetic_reasoning | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| assignment_gap | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| assignment_min | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| assignment_ranking | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| attendance_gap | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| classification_aggregation | 4 | 0/4 (0.0%) | 0/4 (0.0%) | 0/4 (0.0%) | 4/4 (100.0%) |
| combined_exam_gap | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| common_instructor | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| cross_rule_reasoning | 1 | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) |
| department_required_load | 4 | 0/4 (0.0%) | 0/4 (0.0%) | 0/4 (0.0%) | 4/4 (100.0%) |
| distribution_rule_application | 3 | 0/3 (0.0%) | 3/3 (100.0%) | 3/3 (100.0%) | 3/3 (100.0%) |
| english_industry | 4 | 1/4 (25.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| exam_change | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| exam_threshold_set | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| fixture_earned | 2 | 2/2 (100.0%) | 2/2 (100.0%) | 2/2 (100.0%) | 2/2 (100.0%) |
| fixture_personalized | 6 | 6/6 (100.0%) | 6/6 (100.0%) | 6/6 (100.0%) | 6/6 (100.0%) |
| fixture_retake | 2 | 2/2 (100.0%) | 2/2 (100.0%) | 2/2 (100.0%) | 2/2 (100.0%) |
| fixture_status | 2 | 2/2 (100.0%) | 2/2 (100.0%) | 2/2 (100.0%) | 2/2 (100.0%) |
| general_cohort_difference | 1 | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) |
| general_cohort_rule | 2 | 2/2 (100.0%) | 2/2 (100.0%) | 2/2 (100.0%) | 2/2 (100.0%) |
| midterm_max | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| multi_document_multi_hop | 8 | 7/8 (87.5%) | 7/8 (87.5%) | 7/8 (87.5%) | 8/8 (100.0%) |
| multi_document_multi_hop_reasoning | 8 | 7/8 (87.5%) | 7/8 (87.5%) | 7/8 (87.5%) | 8/8 (100.0%) |
| multi_document_reasoning | 32 | 32/32 (100.0%) | 32/32 (100.0%) | 32/32 (100.0%) | 32/32 (100.0%) |
| multi_hop | 16 | 15/16 (93.8%) | 15/16 (93.8%) | 15/16 (93.8%) | 16/16 (100.0%) |
| multi_hop_aggregation | 4 | 0/4 (0.0%) | 1/4 (25.0%) | 1/4 (25.0%) | 4/4 (100.0%) |
| official_public_facts | 87 | 67/87 (77.0%) | 75/87 (86.2%) | 75/87 (86.2%) | 87/87 (100.0%) |
| official_rule | 2 | 2/2 (100.0%) | 2/2 (100.0%) | 2/2 (100.0%) | 2/2 (100.0%) |
| official_rule_with_hypothetical_inputs | 7 | 4/7 (57.1%) | 7/7 (100.0%) | 7/7 (100.0%) | 7/7 (100.0%) |
| prof_credit_load | 4 | 0/4 (0.0%) | 1/4 (25.0%) | 1/4 (25.0%) | 4/4 (100.0%) |
| prof_future_other | 4 | 3/4 (75.0%) | 3/4 (75.0%) | 3/4 (75.0%) | 4/4 (100.0%) |
| prof_other_3credit | 4 | 3/4 (75.0%) | 3/4 (75.0%) | 3/4 (75.0%) | 4/4 (100.0%) |
| prof_other_industry | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| prof_other_required | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| professor_assessment_filter | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| professor_assessment_ranking | 4 | 3/4 (75.0%) | 3/4 (75.0%) | 3/4 (75.0%) | 4/4 (100.0%) |
| professor_required_credit_chain | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| rule_reasoning | 3 | 0/3 (0.0%) | 3/3 (100.0%) | 3/3 (100.0%) | 3/3 (100.0%) |
| schedule_overlap | 4 | 1/4 (25.0%) | 2/4 (50.0%) | 2/4 (50.0%) | 4/4 (100.0%) |
| simulated_student_fixture | 6 | 6/6 (100.0%) | 6/6 (100.0%) | 6/6 (100.0%) | 6/6 (100.0%) |
| single_document | 8 | 2/8 (25.0%) | 8/8 (100.0%) | 8/8 (100.0%) | 8/8 (100.0%) |
| teacher_credits | 4 | 1/4 (25.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| temporal_reasoning | 4 | 1/4 (25.0%) | 2/4 (50.0%) | 2/4 (50.0%) | 4/4 (100.0%) |
| weighted_exam_score | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |

## 진단 분포

| 진단 | 개수 |
|---|---|
| correct | 77 |
| correct_extra_columns | 11 |
| row_count_mismatch | 10 |
| value_mismatch | 2 |

## 정답 재검토가 필요한 문항

- J001 (O): 2026학년도 2학기 SWCON331-00(로봇프로그래밍) 담당 교수의 다른 수업 중, 같은 학기 소프트웨어융합학과 기준 전공필수이면서 3학점인 강좌가 있어? 해당 과목코드·분반·학점을 모두 알려줘. 기준 과목의 다른 분반도 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J002 (O): 2026학년도 2학기 SWCON253-00(기계학습) 담당 교수의 다른 수업 중, 같은 학기 소프트웨어융합학과 기준 전공필수이면서 3학점인 강좌가 있어? 해당 과목코드·분반·학점을 모두 알려줘. 기준 과목의 다른 분반도 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J003 (O): 2026학년도 2학기 CSE304-00(알고리즘) 담당 교수의 다른 수업 중, 같은 학기 컴퓨터공학과 기준 전공필수이면서 3학점인 강좌가 있어? 해당 과목코드·분반·학점을 모두 알려줘. 기준 과목의 다른 분반도 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J004 (O): 2026학년도 2학기 SWCON253-02(기계학습) 담당 교수의 다른 수업 중, 같은 학기 컴퓨터공학과 기준 전공필수이면서 3학점인 강좌가 있어? 해당 과목코드·분반·학점을 모두 알려줘. 기준 과목의 다른 분반도 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J005 (O): 2026학년도 2학기 SWCON331-00(로봇프로그래밍) 담당 교수의 같은 학기 다른 수업 중 소프트웨어융합학과 기준 전공필수이고, 공식 강의계획서에 과제 반영 비율이 30% 이상으로 기재된 강좌의 과목코드·분반·과제 비율을 알려줘. 기준 과목의 다른 분반도 제외하고, 미기재 비율은 0으로 보지 마. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J006 (O): 2026학년도 2학기 SWCON253-00(기계학습) 담당 교수의 같은 학기 다른 수업 중 소프트웨어융합학과 기준 전공필수이고, 공식 강의계획서에 과제 반영 비율이 30% 이상으로 기재된 강좌의 과목코드·분반·과제 비율을 알려줘. 기준 과목의 다른 분반도 제외하고, 미기재 비율은 0으로 보지 마. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J007 (O): 2026학년도 2학기 CSE304-00(알고리즘) 담당 교수의 같은 학기 다른 수업 중 컴퓨터공학과 기준 전공필수이고, 공식 강의계획서에 과제 반영 비율이 30% 이상으로 기재된 강좌의 과목코드·분반·과제 비율을 알려줘. 기준 과목의 다른 분반도 제외하고, 미기재 비율은 0으로 보지 마. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J008 (O): 2026학년도 2학기 SWCON253-02(기계학습) 담당 교수의 같은 학기 다른 수업 중 컴퓨터공학과 기준 전공필수이고, 공식 강의계획서에 과제 반영 비율이 30% 이상으로 기재된 강좌의 과목코드·분반·과제 비율을 알려줘. 기준 과목의 다른 분반도 제외하고, 미기재 비율은 0으로 보지 마. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J009 (X): 2026학년도 2학기 EE209-02(논리회로)의 담당 교수 이름과 학점을 알려줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J010 (O): 2026학년도 2학기 EE209-02(논리회로)의 영어강좌 구분(영어전체/영어부분/해당없음)과 산학필수 여부(예/아니오)를 알려줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J011 (O): 2026학년도 1학기 SWCON367-01(게임콘텐츠캡스톤디자인) 담당 교수의 같은 학기 소프트웨어융합학과 개설목록 내 다른 3학점 강좌 중, 중간·기말 비율이 모두 기재된 강좌끼리 비교하면 시험 비율 합계가 가장 낮은 강좌는? 과목코드·분반·합계를 알려주고 동률은 모두 포함해줘. 기준 과목 코드는 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J012 (O): 2026학년도 1학기 CSE301-01(운영체제)의 담당 교수 이름과 학점을 알려줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J013 (X): 2026학년도 1학기 CSE301-01(운영체제)의 영어강좌 구분(영어전체/영어부분/해당없음)과 산학필수 여부(예/아니오)를 알려줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J014 (O): 2026학년도 1학기 SWCON366-00(3D데이터처리) 담당 교수의 같은 학기 소프트웨어융합학과 개설목록 내 다른 3학점 강좌 중, 중간·기말 비율이 모두 기재된 강좌끼리 비교하면 시험 비율 합계가 가장 낮은 강좌는? 과목코드·분반·합계를 알려주고 동률은 모두 포함해줘. 기준 과목 코드는 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J015 (X): 2025학년도 1학기 EE211-02(확률및랜덤변수)의 담당 교수 이름과 학점을 알려줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J016 (X): 2025학년도 1학기 EE211-02(확률및랜덤변수)의 영어강좌 구분(영어전체/영어부분/해당없음)과 산학필수 여부(예/아니오)를 알려줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J017 (O): 2026학년도 1학기 SWCON401-06(소프트웨어융합캡스톤디자인) 담당 교수의 같은 학기 소프트웨어융합학과 개설목록 내 다른 3학점 강좌 중, 중간·기말 비율이 모두 기재된 강좌끼리 비교하면 시험 비율 합계가 가장 낮은 강좌는? 과목코드·분반·합계를 알려주고 동률은 모두 포함해줘. 기준 과목 코드는 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J018 (X): 2026학년도 2학기 AI4007-07(독립심화학습(인공지능)2)의 담당 교수 이름과 학점을 알려줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J019 (X): 2026학년도 2학기 AI4007-07(독립심화학습(인공지능)2)의 영어강좌 구분(영어전체/영어부분/해당없음)과 산학필수 여부(예/아니오)를 알려줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J020 (X): 2026학년도 1학기 IE215-00(데이터사이언스) 담당 교수의 같은 학기 소프트웨어융합학과 개설목록 내 다른 3학점 강좌 중, 중간·기말 비율이 모두 기재된 강좌끼리 비교하면 시험 비율 합계가 가장 낮은 강좌는? 과목코드·분반·합계를 알려주고 동률은 모두 포함해줘. 기준 과목 코드는 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
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
- J042 (O): 2025학년도 1학기 SWCON103-00(디자인적사고)와 2026학년도 2학기 AI4007-02(독립심화학습(인공지능)2)의 출석 비율을 순서대로 알려주고, 두 번째에서 첫 번째를 뺀 차이를 퍼센트포인트로 계산해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
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
- J069 (X): 2026학년도 1학기 IE419-00(서비스데이터사이언스)와 2026학년도 1학기 SWCON104-01(웹/파이선프로그래밍)의 정규 수업시간이 일주일에 총 몇 분 겹쳐? 시험 일정은 제외하고 요일별 겹치는 구간만 합산해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J070 (O): 2025학년도 2학기 AI4007-00(독립심화학습(인공지능)2)와 2025학년도 2학기 SWCON401-08(소프트웨어융합캡스톤디자인)의 정규 수업시간이 일주일에 총 몇 분 겹쳐? 시험 일정은 제외하고 요일별 겹치는 구간만 합산해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J071 (X): 2025학년도 2학기 SWCON253-01(기계학습)와 2025학년도 2학기 CSE103-01(객체지향프로그래밍)의 정규 수업시간이 일주일에 총 몇 분 겹쳐? 시험 일정은 제외하고 요일별 겹치는 구간만 합산해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J072 (X): 2026학년도 1학기 CSE304-01(알고리즘)와 2026학년도 1학기 EE210-01(신호와시스템)의 정규 수업시간이 일주일에 총 몇 분 겹쳐? 시험 일정은 제외하고 요일별 겹치는 구간만 합산해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
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
- J096 (O): 2024학번 일반 신입학생의 후마니타스 기본구조표에서 총 교양학점, 배분이수 학점, 최소 영역 수, 영역당 학점은 각각 얼마야? 면제·대체·편입 예외는 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J097 (O): 2023학번과 2024학번 기본구조표를 비교하면 2024학번의 총 교양 최소학점과 배분이수 최소학점은 각각 몇 학점 줄었어? 면제·대체 예외는 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J098 (X): 2024학번 일반 신입학생이 배분이수 6학점을 취득했고, 영역당 3학점 기준을 채운 영역은 2개라고 가정하자. 기본구조표 기준 부족 학점·부족 영역 수와 두 조건 충족 여부(1/0)는? 편입·면제 예외는 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J099 (X): 2024학번 일반 신입학생이 배분이수 9학점을 취득했고, 영역당 3학점 기준을 채운 영역은 2개라고 가정하자. 기본구조표 기준 부족 학점·부족 영역 수와 두 조건 충족 여부(1/0)는? 편입·면제 예외는 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J100 (X): 2024학번 일반 신입학생이 배분이수 12학점을 취득했고, 영역당 3학점 기준을 채운 영역은 4개라고 가정하자. 기본구조표 기준 부족 학점·부족 영역 수와 두 조건 충족 여부(1/0)는? 편입·면제 예외는 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.

## 오답 목록

### J009 — correct_extra_columns
질문: 2026학년도 2학기 EE209-02(논리회로)의 담당 교수 이름과 학점을 알려줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
SELECT
    o.course_name,
    o.credits,
    GROUP_CONCAT(p.name, ', ') AS professors
FROM course_offerings AS o
LEFT JOIN offering_professors AS op ON op.offering_id = o.offering_id
LEFT JOIN professors AS p ON p.professor_id = op.professor_id
WHERE o.course_code = 'EE209'
  AND o.section = '02'
  AND o.year = 2026
  AND o.semester = '2'
GROUP BY o.offering_id;
```
정답 컬럼: professor_name, credits / 예측 컬럼: course_name, credits, professors
정답 행 수: 1 / 예측 행 수: 1

### J013 — correct_extra_columns
질문: 2026학년도 1학기 CSE301-01(운영체제)의 영어강좌 구분(영어전체/영어부분/해당없음)과 산학필수 여부(예/아니오)를 알려줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
SELECT
    course_code,
    course_name,
    CASE english_type
        WHEN 'FULL' THEN '영어전체'
        WHEN 'PARTIAL' THEN '영어부분'
        WHEN 'NONE' THEN '해당없음'
        ELSE english_type
    END AS english_course_type,
    CASE industry_required
        WHEN 1 THEN '예'
        WHEN 0 THEN '아니오'
    END AS industry_required
FROM course_offerings
WHERE course_code = 'CSE301'
  AND section = '01'
  AND year = 2026
  AND semester = '1';
```
정답 컬럼: english_classification, industry_required / 예측 컬럼: course_code, course_name, english_course_type, industry_required
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
    o.course_code,
    o.course_name,
    o.section,
    GROUP_CONCAT(p.name, ', ') AS professors,
    o.credits
FROM course_offerings AS o
LEFT JOIN offering_professors AS op ON op.offering_id = o.offering_id
LEFT JOIN professors AS p ON p.professor_id = op.professor_id
WHERE o.course_code = 'EE211'
  AND o.section = '02'
  AND o.year = 2025
  AND o.semester = '1'
GROUP BY o.offering_id;
```
정답 컬럼: professor_name, credits / 예측 컬럼: course_code, course_name, section, professors, credits
정답 행 수: 1 / 예측 행 수: 1

### J016 — correct_extra_columns
질문: 2025학년도 1학기 EE211-02(확률및랜덤변수)의 영어강좌 구분(영어전체/영어부분/해당없음)과 산학필수 여부(예/아니오)를 알려줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
SELECT
    o.course_code,
    o.course_name,
    o.section,
    CASE o.english_type
        WHEN 'FULL' THEN '영어전체'
        WHEN 'PARTIAL' THEN '영어부분'
        WHEN 'NONE' THEN '해당없음'
        WHEN 'SECOND_FOREIGN_LANGUAGE' THEN '제2외국어'
    END AS english_course_type,
    CASE o.industry_required
        WHEN 1 THEN '예'
        WHEN 0 THEN '아니오'
    END AS industry_required
FROM course_offerings AS o
WHERE o.course_code = 'EE211'
  AND o.section = '02'
  AND o.year = 2025
  AND o.semester = '1'
  AND o.course_name LIKE '%확률및랜덤변수%';
```
정답 컬럼: english_classification, industry_required / 예측 컬럼: course_code, course_name, section, english_course_type, industry_required
정답 행 수: 1 / 예측 행 수: 1

### J018 — correct_extra_columns
질문: 2026학년도 2학기 AI4007-07(독립심화학습(인공지능)2)의 담당 교수 이름과 학점을 알려줘.

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
LEFT JOIN offering_professors AS op ON op.offering_id = o.offering_id
LEFT JOIN professors AS p ON p.professor_id = op.professor_id
WHERE o.course_code = 'AI4007'
  AND o.section = '07'
  AND o.year = 2026
  AND o.semester = '2'
GROUP BY o.offering_id;
```
정답 컬럼: professor_name, credits / 예측 컬럼: course_name, credits, professor_names
정답 행 수: 1 / 예측 행 수: 1

### J019 — correct_extra_columns
질문: 2026학년도 2학기 AI4007-07(독립심화학습(인공지능)2)의 영어강좌 구분(영어전체/영어부분/해당없음)과 산학필수 여부(예/아니오)를 알려줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
SELECT
    course_code,
    course_name,
    section,
    CASE english_type
        WHEN 'FULL' THEN '영어전체'
        WHEN 'PARTIAL' THEN '영어부분'
        ELSE '해당없음'
    END AS 영어강좌_구분,
    CASE industry_required
        WHEN 1 THEN '예'
        ELSE '아니오'
    END AS 산학필수_여부
FROM course_offerings
WHERE year = 2026
  AND semester = '2'
  AND course_code = 'AI4007'
  AND section = '07';
```
정답 컬럼: english_classification, industry_required / 예측 컬럼: course_code, course_name, section, 영어강좌_구분, 산학필수_여부
정답 행 수: 1 / 예측 행 수: 1

### J020 — row_count_mismatch
질문: 2026학년도 1학기 IE215-00(데이터사이언스) 담당 교수의 같은 학기 소프트웨어융합학과 개설목록 내 다른 3학점 강좌 중, 중간·기말 비율이 모두 기재된 강좌끼리 비교하면 시험 비율 합계가 가장 낮은 강좌는? 과목코드·분반·합계를 알려주고 동률은 모두 포함해줘. 기준 과목 코드는 제외해줘.

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
    WHERE o.course_code = 'IE215'
      AND o.section = '00'
      AND o.year = 2026
      AND o.semester = '1'
),
eligible AS (
    SELECT
        o.offering_id,
        o.course_code,
        o.section,
        s.midterm_percentage + s.final_exam_percentage AS exam_total
    FROM course_offerings AS o
    JOIN courses AS c ON c.course_code = o.course_code
    JOIN syllabi AS s ON s.offering_id = o.offering_id
    WHERE o.year = 2026
      AND o.semester = '1'
      AND c.department_id = 8
      AND o.credits = 3
      AND o.course_code <> 'IE215'
      AND s.midterm_percentage IS NOT NULL
      AND s.final_exam_percentage IS NOT NULL
      AND EXISTS (
          SELECT 1
          FROM offering_professors AS op
          JOIN target_professors AS tp ON tp.professor_id = op.professor_id
          WHERE op.offering_id = o.offering_id
      )
)
SELECT
    course_code,
    section,
    exam_total
FROM eligible
WHERE exam_total = (SELECT MIN(exam_total) FROM eligible)
ORDER BY course_code, section;
```
정답 컬럼: course_code, section, exam_total_percentage / 예측 컬럼: course_code, section, exam_total
정답 행 수: 1 / 예측 행 수: 0

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
    o.course_code,
    o.section
FROM course_offerings AS o
JOIN courses AS c ON c.course_code = o.course_code
JOIN departments AS d ON d.department_id = c.department_id
JOIN offering_professors AS op ON op.offering_id = o.offering_id
WHERE o.year = 2026
  AND o.semester = '1'
  AND o.credits = 3
  AND d.name = '소프트웨어융합학과'
  AND o.course_code <> 'IE419'
  AND op.professor_id IN (SELECT professor_id FROM target_professors)
ORDER BY o.course_code, o.section;
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
    SELECT DISTINCT p.professor_id, p.professor_code, p.name
    FROM course_offerings AS target
    JOIN offering_professors AS op ON op.offering_id = target.offering_id
    JOIN professors AS p ON p.professor_id = op.professor_id
    WHERE target.course_code = 'IE419'
      AND target.section = '00'
      AND target.year = 2026
      AND target.semester = '1'
)
SELECT
    tp.professor_code,
    tp.name,
    COUNT(o.offering_id) AS other_section_count,
    COALESCE(SUM(o.credits), 0) AS total_offering_credits
FROM target_professors AS tp
LEFT JOIN offering_professors AS op ON op.professor_id = tp.professor_id
LEFT JOIN course_offerings AS o
    ON o.offering_id = op.offering_id
   AND o.year = 2026
   AND o.semester = '1'
   AND o.course_code <> 'IE419'
   AND EXISTS (
       SELECT 1
       FROM courses AS c
       JOIN departments AS d ON d.department_id = c.department_id
       WHERE c.course_code = o.course_code
         AND d.name = '소프트웨어융합학과'
   )
GROUP BY tp.professor_id, tp.professor_code, tp.name
ORDER BY tp.professor_code, tp.name;
```
정답 컬럼: offering_count, offering_credit_sum / 예측 컬럼: professor_code, name, other_section_count, total_offering_credits
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
    JOIN offering_professors AS op ON op.offering_id = target.offering_id
    JOIN professors AS p ON p.professor_id = op.professor_id
    WHERE target.course_code = 'CSE304'
      AND target.section = '01'
      AND target.year = 2026
      AND target.semester = '1'
)
SELECT
    tp.name AS professor_name,
    COUNT(DISTINCT o.offering_id) AS other_section_count,
    SUM(o.credits) AS total_credits
FROM target_professors AS tp
JOIN offering_professors AS op ON op.professor_id = tp.professor_id
JOIN course_offerings AS o ON o.offering_id = op.offering_id
JOIN courses AS c ON c.course_code = o.course_code
JOIN departments AS d ON d.department_id = c.department_id
WHERE o.year = 2026
  AND o.semester = '1'
  AND o.course_code <> 'CSE304'
  AND d.name = '컴퓨터공학과'
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
    SELECT DISTINCT op.professor_id
    FROM course_offerings AS o
    JOIN offering_professors AS op ON op.offering_id = o.offering_id
    WHERE o.course_code = 'AI4003'
      AND o.section = '00'
      AND o.year = 2026
      AND o.semester = '1'
)
SELECT
    p.name AS professor_name,
    COUNT(DISTINCT other_o.offering_id) AS other_section_count,
    SUM(other_o.credits) AS total_offering_credits
FROM target_professors AS tp
JOIN professors AS p ON p.professor_id = tp.professor_id
JOIN offering_professors AS other_op ON other_op.professor_id = tp.professor_id
JOIN course_offerings AS other_o ON other_o.offering_id = other_op.offering_id
JOIN courses AS c ON c.course_code = other_o.course_code
JOIN departments AS d ON d.department_id = c.department_id
WHERE other_o.year = 2026
  AND other_o.semester = '1'
  AND other_o.course_code <> 'AI4003'
  AND d.name = '인공지능학과'
GROUP BY p.professor_id, p.name
ORDER BY p.name;
```
정답 컬럼: offering_count, offering_credit_sum / 예측 컬럼: professor_name, other_section_count, total_offering_credits
정답 행 수: 1 / 예측 행 수: 1

### J061 — row_count_mismatch
질문: 2026학년도 1학기 CSE423-00(정보보호) 담당 교수가 같은 학기 컴퓨터공학과 개설목록에서 맡은 다른 과목의 분반 수와 개설학점 합계를 알려줘. 기준 과목 코드는 제외하고, 다른 분반은 각각 합산해줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
WITH target_professors AS (
    SELECT DISTINCT
        p.professor_id,
        p.name
    FROM course_offerings AS target
    JOIN offering_professors AS target_op
        ON target_op.offering_id = target.offering_id
    JOIN professors AS p
        ON p.professor_id = target_op.professor_id
    WHERE target.course_code = 'CSE423'
      AND target.section = '00'
      AND target.year = 2026
      AND target.semester = '1'
)
SELECT
    tp.name AS professor_name,
    o.course_code,
    o.course_name,
    COUNT(DISTINCT o.offering_id) AS section_count,
    SUM(o.credits) AS total_offering_credits
FROM target_professors AS tp
JOIN offering_professors AS op
    ON op.professor_id = tp.professor_id
JOIN course_offerings AS o
    ON o.offering_id = op.offering_id
JOIN courses AS c
    ON c.course_code = o.course_code
JOIN departments AS d
    ON d.department_id = c.department_id
WHERE o.year = 2026
  AND o.semester = '1'
  AND o.course_code <> 'CSE423'
  AND d.name = '컴퓨터공학과'
GROUP BY tp.professor_id, tp.name, o.course_code, o.course_name
ORDER BY tp.name, o.course_code;
```
정답 컬럼: offering_count, offering_credit_sum / 예측 컬럼: professor_name, course_code, course_name, section_count, total_offering_credits
정답 행 수: 1 / 예측 행 수: 2

### J064 — row_count_mismatch
질문: 2025학년도 2학기 CSE497-02(연구연수활동2(컴퓨터공학))의 담당 교수가 2026학년도 2학기 컴퓨터공학과 개설목록에서 맡은 다른 과목의 코드와 분반을 알려줘. 기준 과목 코드는 제외해줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
SELECT DISTINCT
    o.course_code,
    o.section
FROM course_offerings AS o
JOIN courses AS c ON c.course_code = o.course_code
JOIN departments AS d ON d.department_id = c.department_id
JOIN offering_professors AS op ON op.offering_id = o.offering_id
WHERE o.year = 2026
  AND o.semester = '2'
  AND d.name = '컴퓨터공학과'
  AND o.course_code <> 'CSE497'
  AND EXISTS (
      SELECT 1
      FROM course_offerings AS target
      JOIN offering_professors AS target_op
        ON target_op.offering_id = target.offering_id
      WHERE target.course_code = 'CSE497'
        AND target.section = '02'
        AND target.year = 2025
        AND target.semester = '2'
        AND target_op.professor_id = op.professor_id
  )
ORDER BY o.course_code, o.section;
```
정답 컬럼: course_code, section / 예측 컬럼: course_code, section
정답 행 수: 4 / 예측 행 수: 3

### J069 — row_count_mismatch
질문: 2026학년도 1학기 IE419-00(서비스데이터사이언스)와 2026학년도 1학기 SWCON104-01(웹/파이선프로그래밍)의 정규 수업시간이 일주일에 총 몇 분 겹쳐? 시험 일정은 제외하고 요일별 겹치는 구간만 합산해줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
WITH class_intervals AS (
    SELECT
        o.course_code,
        ts.day,
        CAST(substr(ts.start_time, 1, 2) AS INTEGER) * 60
            + CAST(substr(ts.start_time, 4, 2) AS INTEGER) AS start_minute,
        CAST(substr(ts.end_time, 1, 2) AS INTEGER) * 60
            + CAST(substr(ts.end_time, 4, 2) AS INTEGER) AS end_minute
    FROM course_offerings AS o
    JOIN class_times AS ct ON ct.offering_id = o.offering_id
    JOIN time_slots AS ts ON ts.time_slot_id = ct.time_slot_id
    WHERE o.year = 2026
      AND o.semester = '1'
      AND (
          (o.course_code = 'IE419' AND o.section = '00')
          OR
          (o.course_code = 'SWCON104' AND o.section = '01')
      )
),
overlaps AS (
    SELECT
        a.day,
        min(a.end_minute, b.end_minute) - max(a.start_minute, b.start_minute) AS overlap_minutes
    FROM class_intervals AS a
    JOIN class_intervals AS b
      ON b.day = a.day
     AND a.course_code = 'IE419'
     AND b.course_code = 'SWCON104'
    WHERE a.start_minute < b.end_minute
      AND b.start_minute < a.end_minute
),
daily AS (
    SELECT day, SUM(overlap_minutes) AS overlap_minutes
    FROM overlaps
    GROUP BY day
),
results AS (
    SELECT day, overlap_minutes FROM daily
    UNION ALL
    SELECT 'total', COALESCE(SUM(overlap_minutes), 0) FROM daily
)
SELECT day, overlap_minutes
FROM results
ORDER BY CASE day
    WHEN 'monday' THEN 1
    WHEN 'tuesday' THEN 2
    WHEN 'wednesday' THEN 3
    WHEN 'thursday' THEN 4
    WHEN 'friday' THEN 5
    WHEN 'saturday' THEN 6
    WHEN 'total' THEN 7
END;
```
정답 컬럼: weekly_overlap_minutes / 예측 컬럼: day, overlap_minutes
정답 행 수: 1 / 예측 행 수: 3

### J071 — correct_extra_columns
질문: 2025학년도 2학기 SWCON253-01(기계학습)와 2025학년도 2학기 CSE103-01(객체지향프로그래밍)의 정규 수업시간이 일주일에 총 몇 분 겹쳐? 시험 일정은 제외하고 요일별 겹치는 구간만 합산해줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
WITH overlaps AS (
    SELECT
        ts1.day,
        MAX(ts1.start_time, ts2.start_time) AS overlap_start,
        MIN(ts1.end_time, ts2.end_time) AS overlap_end
    FROM course_offerings AS o1
    JOIN class_times AS ct1 ON ct1.offering_id = o1.offering_id
    JOIN time_slots AS ts1 ON ts1.time_slot_id = ct1.time_slot_id
    JOIN course_offerings AS o2
      ON o2.course_code = 'CSE103'
     AND o2.section = '01'
     AND o2.year = 2025
     AND o2.semester = '2'
    JOIN class_times AS ct2 ON ct2.offering_id = o2.offering_id
    JOIN time_slots AS ts2
      ON ts2.time_slot_id = ct2.time_slot_id
     AND ts2.day = ts1.day
    WHERE o1.course_code = 'SWCON253'
      AND o1.section = '01'
      AND o1.year = 2025
      AND o1.semester = '2'
      AND MAX(ts1.start_time, ts2.start_time) < MIN(ts1.end_time, ts2.end_time)
),
overlap_minutes AS (
    SELECT
        day,
        overlap_start,
        overlap_end,
        (CAST(substr(overlap_end, 1, 2) AS INTEGER) * 60
         + CAST(substr(overlap_end, 4, 2) AS INTEGER))
        - (CAST(substr(overlap_start, 1, 2) AS INTEGER) * 60
         + CAST(substr(overlap_start, 4, 2) AS INTEGER)) AS minutes
    FROM overlaps
),
daily AS (
    SELECT
        day,
        GROUP_CONCAT(overlap_start || '–' || overlap_end, ', ') AS overlapping_intervals,
        SUM(minutes) AS minutes
    FROM (
        SELECT *
        FROM overlap_minutes
        ORDER BY day, overlap_start, overlap_end
    )
    GROUP BY day
)
SELECT
    COALESCE(SUM(minutes), 0) AS total_overlap_minutes,
    COALESCE(
        GROUP_CONCAT(day || ': ' || overlapping_intervals || ' (' || minutes || '분)', '; '),
        '겹치는 시간 없음'
    ) AS weekday_overlaps
FROM daily;
```
정답 컬럼: weekly_overlap_minutes / 예측 컬럼: total_overlap_minutes, weekday_overlaps
정답 행 수: 1 / 예측 행 수: 1

### J072 — row_count_mismatch
질문: 2026학년도 1학기 CSE304-01(알고리즘)와 2026학년도 1학기 EE210-01(신호와시스템)의 정규 수업시간이 일주일에 총 몇 분 겹쳐? 시험 일정은 제외하고 요일별 겹치는 구간만 합산해줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
WITH overlaps AS (
    SELECT
        t1.day,
        MIN(
            CAST(substr(t1.end_time, 1, 2) AS INTEGER) * 60
                + CAST(substr(t1.end_time, 4, 2) AS INTEGER),
            CAST(substr(t2.end_time, 1, 2) AS INTEGER) * 60
                + CAST(substr(t2.end_time, 4, 2) AS INTEGER)
        ) -
        MAX(
            CAST(substr(t1.start_time, 1, 2) AS INTEGER) * 60
                + CAST(substr(t1.start_time, 4, 2) AS INTEGER),
            CAST(substr(t2.start_time, 1, 2) AS INTEGER) * 60
                + CAST(substr(t2.start_time, 4, 2) AS INTEGER)
        ) AS overlap_minutes
    FROM course_offerings AS o1
    JOIN class_times AS ct1 ON ct1.offering_id = o1.offering_id
    JOIN time_slots AS t1 ON t1.time_slot_id = ct1.time_slot_id
    JOIN course_offerings AS o2
      ON o2.year = o1.year
     AND o2.semester = o1.semester
    JOIN class_times AS ct2 ON ct2.offering_id = o2.offering_id
    JOIN time_slots AS t2
      ON t2.time_slot_id = ct2.time_slot_id
     AND t2.day = t1.day
    WHERE o1.course_code = 'CSE304'
      AND o1.section = '01'
      AND o1.year = 2026
      AND o1.semester = '1'
      AND o2.course_code = 'EE210'
      AND o2.section = '01'
      AND t1.day IN ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday')
      AND (
          CAST(substr(t1.end_time, 1, 2) AS INTEGER) * 60
              + CAST(substr(t1.end_time, 4, 2) AS INTEGER)
      ) > (
          CAST(substr(t2.start_time, 1, 2) AS INTEGER) * 60
              + CAST(substr(t2.start_time, 4, 2) AS INTEGER)
      )
      AND (
          CAST(substr(t2.end_time, 1, 2) AS INTEGER) * 60
              + CAST(substr(t2.end_time, 4, 2) AS INTEGER)
      ) > (
          CAST(substr(t1.start_time, 1, 2) AS INTEGER) * 60
              + CAST(substr(t1.start_time, 4, 2) AS INTEGER)
      )
),
daily AS (
    SELECT day, SUM(overlap_minutes) AS overlap_minutes
    FROM overlaps
    GROUP BY day
)
SELECT
    CASE day
        WHEN 'monday' THEN '월요일'
        WHEN 'tuesday' THEN '화요일'
        WHEN 'wednesday' THEN '수요일'
        WHEN 'thursday' THEN '목요일'
        WHEN 'friday' THEN '금요일'
        WHEN 'saturday' THEN '토요일'
    END AS day,
    overlap_minutes,
    SUM(overlap_minutes) OVER () AS total_overlap_minutes
FROM daily
ORDER BY CASE day
    WHEN 'monday' THEN 1
    WHEN 'tuesday' THEN 2
    WHEN 'wednesday' THEN 3
    WHEN 'thursday' THEN 4
    WHEN 'friday' THEN 5
    WHEN 'saturday' THEN 6
END;
```
정답 컬럼: weekly_overlap_minutes / 예측 컬럼: day, overlap_minutes, total_overlap_minutes
정답 행 수: 1 / 예측 행 수: 2

### J081 — row_count_mismatch
질문: 2026학년도 1학기 소프트웨어융합학과 원천 개설목록에서 전공필수로 분류된 강좌의 분반 수와 개설학점 합계를 알려줘. 분반별로 각각 계산해줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
WITH eligible_offerings AS (
    SELECT DISTINCT
        o.offering_id,
        o.course_code,
        o.course_name,
        o.section,
        o.credits
    FROM course_offerings AS o
    JOIN course_offering_categories AS oc
        ON oc.offering_id = o.offering_id
    JOIN departments AS d
        ON d.department_id = oc.department_id
    JOIN course_categories AS cc
        ON cc.category_id = oc.category_id
    WHERE o.year = 2026
      AND o.semester = '1'
      AND d.name = '소프트웨어융합학과'
      AND cc.category_name = '전공필수'
)
SELECT
    course_code,
    course_name,
    COUNT(DISTINCT section) AS section_count,
    SUM(credits) AS total_credits
FROM eligible_offerings
GROUP BY course_code, course_name
ORDER BY course_code;
```
정답 컬럼: offering_count, offering_credit_sum / 예측 컬럼: course_code, course_name, section_count, total_credits
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
    o.course_code,
    o.course_name,
    COUNT(DISTINCT o.section) AS section_count,
    SUM(o.credits) AS total_offering_credits
FROM course_offerings AS o
WHERE o.year = 2025
  AND o.semester = '2'
  AND EXISTS (
      SELECT 1
      FROM course_offering_categories AS oc
      JOIN course_categories AS cc
        ON cc.category_id = oc.category_id
      JOIN departments AS d
        ON d.department_id = oc.department_id
      WHERE oc.offering_id = o.offering_id
        AND d.name = '인공지능학과'
        AND cc.category_name = '전공필수'
  )
GROUP BY o.course_code, o.course_name
ORDER BY o.course_code;
```
정답 컬럼: offering_count, offering_credit_sum / 예측 컬럼: course_code, course_name, section_count, total_offering_credits
정답 행 수: 1 / 예측 행 수: 12

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
        o.section,
        o.credits
    FROM course_offerings AS o
    JOIN course_offering_categories AS oc
        ON oc.offering_id = o.offering_id
    JOIN course_categories AS cc
        ON cc.category_id = oc.category_id
    WHERE o.year = 2025
      AND o.semester = '2'
      AND oc.department_id = 8
      AND cc.category_name = '전공필수'
)
SELECT
    section,
    COUNT(*) AS offering_count,
    SUM(credits) AS total_offering_credits
FROM classified_offerings
GROUP BY section
ORDER BY section;
```
정답 컬럼: offering_count, offering_credit_sum / 예측 컬럼: section, offering_count, total_offering_credits
정답 행 수: 1 / 예측 행 수: 9

### J084 — row_count_mismatch
질문: 2025학년도 1학기 컴퓨터공학과 원천 개설목록에서 전공필수로 분류된 강좌의 분반 수와 개설학점 합계를 알려줘. 분반별로 각각 계산해줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
SELECT
    o.course_code,
    o.course_name,
    COUNT(DISTINCT o.section) AS section_count,
    SUM(o.credits) AS total_offering_credits
FROM course_offerings AS o
JOIN courses AS c ON c.course_code = o.course_code
JOIN departments AS d ON d.department_id = c.department_id
WHERE d.name = '컴퓨터공학과'
  AND o.year = 2025
  AND o.semester = '1'
  AND EXISTS (
      SELECT 1
      FROM course_offering_categories AS oc
      JOIN course_categories AS cc ON cc.category_id = oc.category_id
      WHERE oc.offering_id = o.offering_id
        AND oc.department_id = d.department_id
        AND cc.category_name = '전공필수'
  )
GROUP BY o.course_code, o.course_name
ORDER BY o.course_code;
```
정답 컬럼: offering_count, offering_credit_sum / 예측 컬럼: course_code, course_name, section_count, total_offering_credits
정답 행 수: 1 / 예측 행 수: 11

### J098 — correct_extra_columns
질문: 2024학번 일반 신입학생이 배분이수 6학점을 취득했고, 영역당 3학점 기준을 채운 영역은 2개라고 가정하자. 기본구조표 기준 부족 학점·부족 영역 수와 두 조건 충족 여부(1/0)는? 편입·면제 예외는 제외해줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
SELECT
    requirement_name,
    min_credits,
    CASE WHEN min_credits > 6 THEN min_credits - 6 ELSE 0 END AS 부족_학점,
    min_areas,
    CASE
        WHEN min_areas IS NULL OR min_areas <= 2 THEN 0
        ELSE min_areas - 2
    END AS 부족_영역_수,
    CASE WHEN 6 >= min_credits THEN 1 ELSE 0 END AS 학점_조건_충족,
    CASE WHEN min_areas IS NULL OR 2 >= min_areas THEN 1 ELSE 0 END AS 영역_조건_충족
FROM general_education_requirements AS gr
JOIN general_education_requirement_categories AS gc
    ON gc.general_requirement_id = gr.general_requirement_id
WHERE gr.cohort_start <= 2024
  AND (gr.cohort_end IS NULL OR gr.cohort_end >= 2024)
  AND gc.requirement_code = 'DISTRIBUTION';
```
정답 컬럼: remaining_credits, remaining_areas, meets_both / 예측 컬럼: requirement_name, min_credits, 부족_학점, min_areas, 부족_영역_수, 학점_조건_충족, 영역_조건_충족
정답 행 수: 1 / 예측 행 수: 1

### J099 — correct_extra_columns
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
    CASE WHEN 9 >= gc.min_credits THEN 1 ELSE 0 END AS 학점_조건_충족,
    CASE WHEN 2 >= COALESCE(gc.min_areas, 0) THEN 1 ELSE 0 END AS 영역_조건_충족
FROM general_education_requirements AS gr
JOIN general_education_requirement_categories AS gc
    ON gc.general_requirement_id = gr.general_requirement_id
WHERE gr.cohort_start <= 2024
  AND (gr.cohort_end IS NULL OR gr.cohort_end >= 2024)
  AND gc.requirement_code = 'DISTRIBUTION';
```
정답 컬럼: remaining_credits, remaining_areas, meets_both / 예측 컬럼: min_credits, 부족_학점, min_areas, 부족_영역_수, 학점_조건_충족, 영역_조건_충족
정답 행 수: 1 / 예측 행 수: 1

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
    MAX(0, COALESCE(gc.min_areas, 0) - 4) AS 부족_영역_수,
    CASE WHEN 12 >= gc.min_credits THEN 1 ELSE 0 END AS 학점_조건_충족,
    CASE WHEN gc.min_areas IS NULL OR 4 >= gc.min_areas THEN 1 ELSE 0 END AS 영역_조건_충족
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
