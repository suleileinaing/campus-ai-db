# Text2SQL 평가 결과 (2026-11-05 17:30)

| 지표 | 값 |
|---|---|
| 평가 문항 수 | 100 |
| 실행 성공률(최종) | 100/100 (100.0%) |
| 실행 성공률(1차 시도) | 100/100 (100.0%) |
| 정답률 strict | 82/100 (82.0%) |
| 정답률 relaxed | 87/100 (87.0%) |
| 정답률 subset (정답 일부 컬럼 누락 허용) | 87/100 (87.0%) |
| 평균 토큰 | 4211.2 |
| 평균 응답시간(초) | 5.34 |

## 유형별

| 태그 | n | strict | relaxed | subset | 실행 성공 |
|---|---|---|---|---|---|
| arithmetic_reasoning | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| assignment_gap | 4 | 3/4 (75.0%) | 3/4 (75.0%) | 3/4 (75.0%) | 4/4 (100.0%) |
| assignment_min | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| assignment_ranking | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| attendance_gap | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| classification_aggregation | 4 | 0/4 (0.0%) | 0/4 (0.0%) | 0/4 (0.0%) | 4/4 (100.0%) |
| combined_exam_gap | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| common_instructor | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| cross_rule_reasoning | 1 | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) |
| department_required_load | 4 | 0/4 (0.0%) | 0/4 (0.0%) | 0/4 (0.0%) | 4/4 (100.0%) |
| distribution_rule_application | 3 | 0/3 (0.0%) | 3/3 (100.0%) | 3/3 (100.0%) | 3/3 (100.0%) |
| english_industry | 4 | 3/4 (75.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| exam_change | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| exam_threshold_set | 4 | 3/4 (75.0%) | 3/4 (75.0%) | 3/4 (75.0%) | 4/4 (100.0%) |
| fixture_earned | 2 | 2/2 (100.0%) | 2/2 (100.0%) | 2/2 (100.0%) | 2/2 (100.0%) |
| fixture_personalized | 6 | 6/6 (100.0%) | 6/6 (100.0%) | 6/6 (100.0%) | 6/6 (100.0%) |
| fixture_retake | 2 | 2/2 (100.0%) | 2/2 (100.0%) | 2/2 (100.0%) | 2/2 (100.0%) |
| fixture_status | 2 | 2/2 (100.0%) | 2/2 (100.0%) | 2/2 (100.0%) | 2/2 (100.0%) |
| general_cohort_difference | 1 | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) |
| general_cohort_rule | 2 | 2/2 (100.0%) | 2/2 (100.0%) | 2/2 (100.0%) | 2/2 (100.0%) |
| midterm_max | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| multi_document_multi_hop | 8 | 7/8 (87.5%) | 7/8 (87.5%) | 7/8 (87.5%) | 8/8 (100.0%) |
| multi_document_multi_hop_reasoning | 8 | 7/8 (87.5%) | 7/8 (87.5%) | 7/8 (87.5%) | 8/8 (100.0%) |
| multi_document_reasoning | 32 | 30/32 (93.8%) | 30/32 (93.8%) | 30/32 (93.8%) | 32/32 (100.0%) |
| multi_hop | 16 | 14/16 (87.5%) | 14/16 (87.5%) | 14/16 (87.5%) | 16/16 (100.0%) |
| multi_hop_aggregation | 4 | 0/4 (0.0%) | 1/4 (25.0%) | 1/4 (25.0%) | 4/4 (100.0%) |
| official_public_facts | 87 | 72/87 (82.8%) | 74/87 (85.1%) | 74/87 (85.1%) | 87/87 (100.0%) |
| official_rule | 2 | 2/2 (100.0%) | 2/2 (100.0%) | 2/2 (100.0%) | 2/2 (100.0%) |
| official_rule_with_hypothetical_inputs | 7 | 4/7 (57.1%) | 7/7 (100.0%) | 7/7 (100.0%) | 7/7 (100.0%) |
| prof_credit_load | 4 | 0/4 (0.0%) | 1/4 (25.0%) | 1/4 (25.0%) | 4/4 (100.0%) |
| prof_future_other | 4 | 3/4 (75.0%) | 3/4 (75.0%) | 3/4 (75.0%) | 4/4 (100.0%) |
| prof_other_3credit | 4 | 3/4 (75.0%) | 3/4 (75.0%) | 3/4 (75.0%) | 4/4 (100.0%) |
| prof_other_industry | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| prof_other_required | 4 | 3/4 (75.0%) | 3/4 (75.0%) | 3/4 (75.0%) | 4/4 (100.0%) |
| professor_assessment_filter | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| professor_assessment_ranking | 4 | 3/4 (75.0%) | 3/4 (75.0%) | 3/4 (75.0%) | 4/4 (100.0%) |
| professor_required_credit_chain | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| rule_reasoning | 3 | 0/3 (0.0%) | 3/3 (100.0%) | 3/3 (100.0%) | 3/3 (100.0%) |
| schedule_overlap | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| simulated_student_fixture | 6 | 6/6 (100.0%) | 6/6 (100.0%) | 6/6 (100.0%) | 6/6 (100.0%) |
| single_document | 8 | 7/8 (87.5%) | 8/8 (100.0%) | 8/8 (100.0%) | 8/8 (100.0%) |
| teacher_credits | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| temporal_reasoning | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| weighted_exam_score | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |

## 진단 분포

| 진단 | 개수 |
|---|---|
| correct | 82 |
| row_count_mismatch | 12 |
| correct_extra_columns | 5 |
| value_mismatch | 1 |

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
- J012 (O): 2026학년도 1학기 CSE301-01(운영체제)의 담당 교수 이름과 학점을 알려줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J013 (O): 2026학년도 1학기 CSE301-01(운영체제)의 영어강좌 구분(영어전체/영어부분/해당없음)과 산학필수 여부(예/아니오)를 알려줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J014 (O): 2026학년도 1학기 SWCON366-00(3D데이터처리) 담당 교수의 같은 학기 소프트웨어융합학과 개설목록 내 다른 3학점 강좌 중, 중간·기말 비율이 모두 기재된 강좌끼리 비교하면 시험 비율 합계가 가장 낮은 강좌는? 과목코드·분반·합계를 알려주고 동률은 모두 포함해줘. 기준 과목 코드는 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J015 (O): 2025학년도 1학기 EE211-02(확률및랜덤변수)의 담당 교수 이름과 학점을 알려줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J016 (X): 2025학년도 1학기 EE211-02(확률및랜덤변수)의 영어강좌 구분(영어전체/영어부분/해당없음)과 산학필수 여부(예/아니오)를 알려줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J017 (O): 2026학년도 1학기 SWCON401-06(소프트웨어융합캡스톤디자인) 담당 교수의 같은 학기 소프트웨어융합학과 개설목록 내 다른 3학점 강좌 중, 중간·기말 비율이 모두 기재된 강좌끼리 비교하면 시험 비율 합계가 가장 낮은 강좌는? 과목코드·분반·합계를 알려주고 동률은 모두 포함해줘. 기준 과목 코드는 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J018 (O): 2026학년도 2학기 AI4007-07(독립심화학습(인공지능)2)의 담당 교수 이름과 학점을 알려줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J019 (O): 2026학년도 2학기 AI4007-07(독립심화학습(인공지능)2)의 영어강좌 구분(영어전체/영어부분/해당없음)과 산학필수 여부(예/아니오)를 알려줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J020 (X): 2026학년도 1학기 IE215-00(데이터사이언스) 담당 교수의 같은 학기 소프트웨어융합학과 개설목록 내 다른 3학점 강좌 중, 중간·기말 비율이 모두 기재된 강좌끼리 비교하면 시험 비율 합계가 가장 낮은 강좌는? 과목코드·분반·합계를 알려주고 동률은 모두 포함해줘. 기준 과목 코드는 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J021 (O): 2025학년도 1학기 CSE406-01(캡스톤디자인)와 2026학년도 1학기 CSE406-01(캡스톤디자인)의 기말고사 비율을 순서대로 알려주고, 두 번째에서 첫 번째를 뺀 차이를 퍼센트포인트로 계산해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J022 (O): 2025학년도 1학기 CSE406-01(캡스톤디자인)와 2026학년도 1학기 CSE406-06(캡스톤디자인)의 기말고사 비율을 순서대로 알려주고, 두 번째에서 첫 번째를 뺀 차이를 퍼센트포인트로 계산해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J023 (O): 2026학년도 2학기 CSE406-16(캡스톤디자인)와 2025학년도 2학기 CSE406-06(캡스톤디자인)의 기말고사 비율을 순서대로 알려주고, 두 번째에서 첫 번째를 뺀 차이를 퍼센트포인트로 계산해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J024 (O): 2026학년도 2학기 AI4007-01(독립심화학습(인공지능)2)와 2025학년도 2학기 AI4007-00(독립심화학습(인공지능)2)의 기말고사 비율을 순서대로 알려주고, 두 번째에서 첫 번째를 뺀 차이를 퍼센트포인트로 계산해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
- J025 (X): 2025학년도 1학기 CSE406-01(캡스톤디자인)와 2026학년도 1학기 AI4003-00(졸업논문(인공지능))의 과제보고서 비율을 순서대로 알려주고, 두 번째에서 첫 번째를 뺀 차이를 퍼센트포인트로 계산해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
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
- J058 (X): 2026학년도 1학기 AI4003-00(졸업논문(인공지능)) 담당 교수의 다른 수업 중, 같은 학기 인공지능학과 개설목록에서 전공필수인 강좌의 과목코드와 분반을 알려줘. 기준 과목의 다른 분반도 제외해줘. — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
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
- J073 (X): 다음 세 강좌 중 중간·기말 비율 합계가 70% 이상인 강좌의 과목코드·연도·학기·분반·합계를 알려줘: 2025학년도 1학기 CSE406-01(캡스톤디자인), 2026학년도 1학기 AI4003-00(졸업논문(인공지능)), 2025학년도 1학기 CSE405-00(졸업프로젝트). — 원천 정답 고정. 참조 SQL은 상세 파일 참조.
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

### J016 — correct_extra_columns
질문: 2025학년도 1학기 EE211-02(확률및랜덤변수)의 영어강좌 구분(영어전체/영어부분/해당없음)과 산학필수 여부(예/아니오)를 알려줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
SELECT
    course_name,
    section,
    CASE english_type
        WHEN 'FULL' THEN '영어전체'
        WHEN 'PARTIAL' THEN '영어부분'
        WHEN 'NONE' THEN '해당없음'
        WHEN 'SECOND_FOREIGN_LANGUAGE' THEN '제2외국어'
    END AS 영어강좌_구분,
    CASE industry_required
        WHEN 1 THEN '예'
        WHEN 0 THEN '아니오'
    END AS 산학필수_여부
FROM course_offerings
WHERE course_code = 'EE211'
  AND section = '02'
  AND year = 2025
  AND semester = '1';
```
정답 컬럼: english_classification, industry_required / 예측 컬럼: course_name, section, 영어강좌_구분, 산학필수_여부
정답 행 수: 1 / 예측 행 수: 1

### J020 — row_count_mismatch
질문: 2026학년도 1학기 IE215-00(데이터사이언스) 담당 교수의 같은 학기 소프트웨어융합학과 개설목록 내 다른 3학점 강좌 중, 중간·기말 비율이 모두 기재된 강좌끼리 비교하면 시험 비율 합계가 가장 낮은 강좌는? 과목코드·분반·합계를 알려주고 동률은 모두 포함해줘. 기준 과목 코드는 제외해줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
WITH base_offering AS (
    SELECT offering_id
    FROM course_offerings
    WHERE course_code = 'IE215'
      AND section = '00'
      AND year = 2026
      AND semester = '1'
),
base_professors AS (
    SELECT DISTINCT op.professor_id
    FROM base_offering AS b
    JOIN offering_professors AS op
      ON op.offering_id = b.offering_id
),
candidates AS (
    SELECT DISTINCT
        o.offering_id,
        o.course_code,
        o.section,
        s.midterm_percentage + s.final_exam_percentage AS exam_percentage_total
    FROM course_offerings AS o
    JOIN courses AS c
      ON c.course_code = o.course_code
    JOIN departments AS d
      ON d.department_id = c.department_id
    JOIN syllabi AS s
      ON s.offering_id = o.offering_id
    WHERE o.year = 2026
      AND o.semester = '1'
      AND o.credits = 3
      AND o.course_code <> 'IE215'
      AND d.name = '소프트웨어융합학과'
      AND s.midterm_percentage IS NOT NULL
      AND s.final_exam_percentage IS NOT NULL
      AND EXISTS (
          SELECT 1
          FROM offering_professors AS op
          JOIN base_professors AS bp
            ON bp.professor_id = op.professor_id
          WHERE op.offering_id = o.offering_id
      )
)
SELECT course_code, section, exam_percentage_total
FROM candidates
WHERE exam_percentage_total = (
    SELECT MIN(exam_percentage_total)
    FROM candidates
);
```
정답 컬럼: course_code, section, exam_total_percentage / 예측 컬럼: course_code, section, exam_percentage_total
정답 행 수: 1 / 예측 행 수: 0

### J025 — value_mismatch
질문: 2025학년도 1학기 CSE406-01(캡스톤디자인)와 2026학년도 1학기 AI4003-00(졸업논문(인공지능))의 과제보고서 비율을 순서대로 알려주고, 두 번째에서 첫 번째를 뺀 차이를 퍼센트포인트로 계산해줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
WITH
first_course AS (
    SELECT s.assignment_percentage
    FROM course_offerings AS o
    JOIN syllabi AS s ON s.offering_id = o.offering_id
    WHERE o.course_code = 'CSE406-01'
      AND o.year = 2025
      AND o.semester = '1'
      AND o.section = '01'
),
second_course AS (
    SELECT s.assignment_percentage
    FROM course_offerings AS o
    JOIN syllabi AS s ON s.offering_id = o.offering_id
    WHERE o.course_code = 'AI4003-00'
      AND o.year = 2026
      AND o.semester = '1'
      AND o.section = '00'
)
SELECT
    (SELECT assignment_percentage FROM first_course) AS first_assignment_percentage,
    (SELECT assignment_percentage FROM second_course) AS second_assignment_percentage,
    (SELECT assignment_percentage FROM second_course)
      - (SELECT assignment_percentage FROM first_course) AS difference_percentage_points;
```
정답 컬럼: first_percentage, second_percentage, second_minus_first_pp / 예측 컬럼: first_assignment_percentage, second_assignment_percentage, difference_percentage_points
정답 행 수: 1 / 예측 행 수: 1

### J046 — row_count_mismatch
질문: 2026학년도 1학기 IE419-00(서비스데이터사이언스) 담당 교수의 다른 수업 중, 같은 학기 소프트웨어융합학과 개설목록에서 3학점인 강좌의 과목코드와 분반을 알려줘. 기준 과목의 다른 분반도 제외해줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
WITH base_professors AS (
    SELECT op.professor_id
    FROM course_offerings AS base
    JOIN offering_professors AS op
      ON op.offering_id = base.offering_id
    WHERE base.course_code = 'IE419'
      AND base.section = '00'
      AND base.year = 2026
      AND base.semester = '1'
)
SELECT DISTINCT other.course_code, other.section
FROM course_offerings AS other
JOIN courses AS c
  ON c.course_code = other.course_code
JOIN departments AS d
  ON d.department_id = c.department_id
WHERE other.year = 2026
  AND other.semester = '1'
  AND other.credits = 3
  AND d.name = '소프트웨어융합학과'
  AND other.course_code <> 'IE419'
  AND EXISTS (
      SELECT 1
      FROM offering_professors AS op
      JOIN base_professors AS bp
        ON bp.professor_id = op.professor_id
      WHERE op.offering_id = other.offering_id
  );
```
정답 컬럼: course_code, section / 예측 컬럼: course_code, section
정답 행 수: 2 / 예측 행 수: 0

### J047 — row_count_mismatch
질문: 2026학년도 1학기 IE419-00(서비스데이터사이언스) 담당 교수가 같은 학기 소프트웨어융합학과 개설목록에서 맡은 다른 과목의 분반 수와 개설학점 합계를 알려줘. 기준 과목 코드는 제외하고, 다른 분반은 각각 합산해줘.

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
    WHERE target.course_code = 'IE419'
      AND target.section = '00'
      AND target.year = 2026
      AND target.semester = '1'
)
SELECT
    p.name AS professor_name,
    c.course_code,
    co.course_name,
    COUNT(DISTINCT co.offering_id) AS section_count,
    SUM(co.credits) AS total_credits
FROM course_offerings AS co
JOIN courses AS c
    ON c.course_code = co.course_code
JOIN departments AS d
    ON d.department_id = c.department_id
JOIN offering_professors AS op
    ON op.offering_id = co.offering_id
JOIN professors AS p
    ON p.professor_id = op.professor_id
JOIN target_professors AS tp
    ON tp.professor_id = p.professor_id
WHERE co.year = 2026
  AND co.semester = '1'
  AND d.name = '소프트웨어융합학과'
  AND co.course_code <> 'IE419'
GROUP BY p.professor_id, c.course_code, co.course_name
ORDER BY professor_name, c.course_code;
```
정답 컬럼: offering_count, offering_credit_sum / 예측 컬럼: professor_name, course_code, course_name, section_count, total_credits
정답 행 수: 1 / 예측 행 수: 0

### J057 — correct_extra_columns
질문: 2026학년도 1학기 CSE304-01(알고리즘) 담당 교수가 같은 학기 컴퓨터공학과 개설목록에서 맡은 다른 과목의 분반 수와 개설학점 합계를 알려줘. 기준 과목 코드는 제외하고, 다른 분반은 각각 합산해줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
WITH target_professors AS (
    SELECT DISTINCT op.professor_id
    FROM course_offerings AS co
    JOIN offering_professors AS op
      ON op.offering_id = co.offering_id
    WHERE co.course_code = 'CSE304'
      AND co.section = '01'
      AND co.year = 2026
      AND co.semester = '1'
)
SELECT
    p.name AS professor_name,
    COUNT(co.offering_id) AS section_count,
    SUM(co.credits) AS total_offering_credits
FROM target_professors AS tp
JOIN professors AS p
  ON p.professor_id = tp.professor_id
JOIN offering_professors AS op
  ON op.professor_id = tp.professor_id
JOIN course_offerings AS co
  ON co.offering_id = op.offering_id
JOIN courses AS c
  ON c.course_code = co.course_code
JOIN departments AS d
  ON d.department_id = c.department_id
WHERE co.year = 2026
  AND co.semester = '1'
  AND co.course_code <> 'CSE304'
  AND d.name = '컴퓨터공학과'
GROUP BY p.professor_id, p.name
```
정답 컬럼: offering_count, offering_credit_sum / 예측 컬럼: professor_name, section_count, total_offering_credits
정답 행 수: 1 / 예측 행 수: 1

### J058 — row_count_mismatch
질문: 2026학년도 1학기 AI4003-00(졸업논문(인공지능)) 담당 교수의 다른 수업 중, 같은 학기 인공지능학과 개설목록에서 전공필수인 강좌의 과목코드와 분반을 알려줘. 기준 과목의 다른 분반도 제외해줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
SELECT DISTINCT other.course_code, other.section
FROM course_offerings AS other
JOIN courses AS c
  ON c.course_code = other.course_code
JOIN departments AS d
  ON d.department_id = c.department_id
JOIN course_offering_categories AS occ
  ON occ.offering_id = other.offering_id
JOIN course_categories AS cc
  ON cc.category_id = occ.category_id
JOIN offering_professors AS op
  ON op.offering_id = other.offering_id
WHERE other.year = 2026
  AND other.semester = '1'
  AND d.name = '인공지능학과'
  AND cc.category_name = '전공필수'
  AND other.course_code <> 'AI4003'
  AND EXISTS (
      SELECT 1
      FROM course_offerings AS base
      JOIN offering_professors AS base_op
        ON base_op.offering_id = base.offering_id
      WHERE base.course_code = 'AI4003'
        AND base.section = '00'
        AND base.year = 2026
        AND base.semester = '1'
        AND base_op.professor_id = op.professor_id
  );
```
정답 컬럼: course_code, section / 예측 컬럼: course_code, section
정답 행 수: 3 / 예측 행 수: 1

### J059 — row_count_mismatch
질문: 2026학년도 1학기 AI4003-00(졸업논문(인공지능)) 담당 교수가 같은 학기 인공지능학과 개설목록에서 맡은 다른 과목의 분반 수와 개설학점 합계를 알려줘. 기준 과목 코드는 제외하고, 다른 분반은 각각 합산해줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
WITH target_professors AS (
    SELECT DISTINCT p.professor_id, p.professor_code, p.name
    FROM course_offerings AS target
    JOIN courses AS target_course
      ON target_course.course_code = target.course_code
    JOIN departments AS d
      ON d.department_id = target_course.department_id
    JOIN offering_professors AS op
      ON op.offering_id = target.offering_id
    JOIN professors AS p
      ON p.professor_id = op.professor_id
    WHERE target.course_code = 'AI4003-00'
      AND target.year = 2026
      AND target.semester = '1'
      AND d.name = '인공지능학과'
),
other_offerings AS (
    SELECT DISTINCT tp.professor_id, o.offering_id, o.credits
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
      AND o.course_code <> 'AI4003-00'
      AND d.name = '인공지능학과'
)
SELECT tp.professor_code,
       tp.name AS professor_name,
       COUNT(oo.offering_id) AS section_count,
       SUM(oo.credits) AS total_offering_credits
FROM target_professors AS tp
JOIN other_offerings AS oo
  ON oo.professor_id = tp.professor_id
GROUP BY tp.professor_id, tp.professor_code, tp.name;
```
정답 컬럼: offering_count, offering_credit_sum / 예측 컬럼: professor_code, professor_name, section_count, total_offering_credits
정답 행 수: 1 / 예측 행 수: 0

### J061 — row_count_mismatch
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
      AND target.section = '00'
      AND target.year = 2026
      AND target.semester = '1'
)
SELECT
    p.name AS professor_name,
    c.course_code,
    c.current_name AS course_name,
    COUNT(DISTINCT other.offering_id) AS section_count,
    SUM(other.credits) AS total_offering_credits
FROM target_professors AS tp
JOIN professors AS p
  ON p.professor_id = tp.professor_id
JOIN offering_professors AS op
  ON op.professor_id = tp.professor_id
JOIN course_offerings AS other
  ON other.offering_id = op.offering_id
JOIN courses AS c
  ON c.course_code = other.course_code
JOIN departments AS d
  ON d.department_id = c.department_id
WHERE other.year = 2026
  AND other.semester = '1'
  AND other.course_code <> 'CSE423'
  AND d.name = '컴퓨터공학과'
GROUP BY p.professor_id, p.name, c.course_code, c.current_name
ORDER BY p.name, c.course_code;
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
SELECT DISTINCT co.course_code, co.section
FROM course_offerings AS co
JOIN courses AS c ON c.course_code = co.course_code
JOIN departments AS d ON d.department_id = c.department_id
JOIN offering_professors AS op ON op.offering_id = co.offering_id
WHERE co.year = 2026
  AND co.semester = '2'
  AND d.name = '컴퓨터공학과'
  AND co.course_code <> 'CSE497'
  AND op.professor_id IN (
      SELECT base_op.professor_id
      FROM course_offerings AS base
      JOIN offering_professors AS base_op
        ON base_op.offering_id = base.offering_id
      WHERE base.course_code = 'CSE497'
        AND base.section = '02'
        AND base.year = 2025
        AND base.semester = '2'
  );
```
정답 컬럼: course_code, section / 예측 컬럼: course_code, section
정답 행 수: 4 / 예측 행 수: 3

### J073 — row_count_mismatch
질문: 다음 세 강좌 중 중간·기말 비율 합계가 70% 이상인 강좌의 과목코드·연도·학기·분반·합계를 알려줘: 2025학년도 1학기 CSE406-01(캡스톤디자인), 2026학년도 1학기 AI4003-00(졸업논문(인공지능)), 2025학년도 1학기 CSE405-00(졸업프로젝트).

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
SELECT
    co.course_code,
    co.year,
    co.semester,
    co.section,
    s.midterm_percentage + s.final_exam_percentage AS 합계
FROM course_offerings AS co
JOIN syllabi AS s
    ON s.offering_id = co.offering_id
WHERE (
        co.course_code = 'CSE406'
        AND co.year = 2025
        AND co.semester = '1'
        AND co.section = '01'
    )
    OR (
        co.course_code = 'AI4003'
        AND co.year = 2026
        AND co.semester = '1'
        AND co.section = '00'
    )
    OR (
        co.course_code = 'CSE405'
        AND co.year = 2025
        AND co.semester = '1'
        AND co.section = '00'
    )
    AND s.midterm_percentage + s.final_exam_percentage >= 70
```

### J081 — row_count_mismatch
질문: 2026학년도 1학기 소프트웨어융합학과 원천 개설목록에서 전공필수로 분류된 강좌의 분반 수와 개설학점 합계를 알려줘. 분반별로 각각 계산해줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
SELECT
    co.course_name,
    COUNT(DISTINCT co.offering_id) AS section_count,
    SUM(co.credits) AS total_offering_credits
FROM course_offerings AS co
JOIN courses AS c
    ON c.course_code = co.course_code
JOIN departments AS d
    ON d.department_id = c.department_id
JOIN course_offering_categories AS coc
    ON coc.offering_id = co.offering_id
JOIN course_categories AS cc
    ON cc.category_id = coc.category_id
WHERE d.name = '소프트웨어융합학과'
  AND co.year = 2026
  AND co.semester = '1'
  AND cc.category_name = '전공필수'
GROUP BY c.course_code, co.course_name
ORDER BY co.course_name;
```
정답 컬럼: offering_count, offering_credit_sum / 예측 컬럼: course_name, section_count, total_offering_credits
정답 행 수: 1 / 예측 행 수: 6

### J082 — row_count_mismatch
질문: 2025학년도 2학기 인공지능학과 원천 개설목록에서 전공필수로 분류된 강좌의 분반 수와 개설학점 합계를 알려줘. 분반별로 각각 계산해줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
WITH major_required_offerings AS (
    SELECT DISTINCT
        co.offering_id,
        co.course_code,
        co.course_name,
        co.section,
        co.credits
    FROM course_offerings AS co
    JOIN courses AS c
        ON c.course_code = co.course_code
    JOIN departments AS d
        ON d.department_id = c.department_id
    JOIN course_offering_categories AS coc
        ON coc.offering_id = co.offering_id
       AND coc.department_id = d.department_id
    JOIN course_categories AS cc
        ON cc.category_id = coc.category_id
    WHERE d.name = '인공지능학과'
      AND cc.category_name = '전공필수'
      AND co.year = 2025
      AND co.semester = '2'
)
SELECT
    course_code,
    course_name,
    COUNT(DISTINCT section) AS 분반_수,
    SUM(credits) AS 개설학점_합계
FROM major_required_offerings
GROUP BY course_code, course_name
ORDER BY course_code;
```
정답 컬럼: offering_count, offering_credit_sum / 예측 컬럼: course_code, course_name, 분반_수, 개설학점_합계
정답 행 수: 1 / 예측 행 수: 2

### J083 — row_count_mismatch
질문: 2025학년도 2학기 소프트웨어융합학과 원천 개설목록에서 전공필수로 분류된 강좌의 분반 수와 개설학점 합계를 알려줘. 분반별로 각각 계산해줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
WITH source_offerings AS (
    SELECT DISTINCT co.offering_id, co.section, co.credits
    FROM course_offerings AS co
    JOIN course_offering_categories AS coc
        ON coc.offering_id = co.offering_id
    JOIN course_categories AS cc
        ON cc.category_id = coc.category_id
    JOIN departments AS d
        ON d.department_id = coc.department_id
    WHERE co.year = 2025
      AND co.semester = '2'
      AND d.name = '소프트웨어융합학과'
      AND cc.category_name = '전공필수'
)
SELECT
    section,
    COUNT(*) AS offering_count,
    SUM(credits) AS total_credits
FROM source_offerings
GROUP BY section
ORDER BY section;
```
정답 컬럼: offering_count, offering_credit_sum / 예측 컬럼: section, offering_count, total_credits
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
    co.section,
    COUNT(DISTINCT co.offering_id) AS section_count,
    SUM(co.credits) AS total_credits
FROM course_offerings AS co
JOIN courses AS c
    ON c.course_code = co.course_code
JOIN departments AS d
    ON d.department_id = c.department_id
WHERE d.name = '컴퓨터공학과'
  AND co.year = 2025
  AND co.semester = '1'
  AND EXISTS (
      SELECT 1
      FROM course_offering_categories AS coc
      JOIN course_categories AS cc
          ON cc.category_id = coc.category_id
      WHERE coc.offering_id = co.offering_id
        AND cc.category_name = '전공필수'
  )
GROUP BY co.section
ORDER BY co.section;
```
정답 컬럼: offering_count, offering_credit_sum / 예측 컬럼: section, section_count, total_credits
정답 행 수: 1 / 예측 행 수: 13

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
    MAX(0, gc.min_areas - 2) AS 부족_영역_수,
    CASE WHEN 6 >= gc.min_credits THEN 1 ELSE 0 END AS 학점_기준_충족,
    CASE WHEN 2 >= gc.min_areas THEN 1 ELSE 0 END AS 영역_수_기준_충족
FROM general_education_requirements AS gr
JOIN general_education_requirement_categories AS gc
    ON gc.general_requirement_id = gr.general_requirement_id
WHERE gr.cohort_start <= 2024
  AND (gr.cohort_end IS NULL OR gr.cohort_end >= 2024)
  AND gc.requirement_code = 'DISTRIBUTION';
```
정답 컬럼: remaining_credits, remaining_areas, meets_both / 예측 컬럼: 부족_학점, 부족_영역_수, 학점_기준_충족, 영역_수_기준_충족
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
    max(0, gc.min_credits - 9) AS 부족_학점,
    max(0, gc.min_areas - 2) AS 부족_영역_수,
    CASE WHEN 9 >= gc.min_credits THEN 1 ELSE 0 END AS 최소_학점_충족,
    CASE WHEN 2 >= gc.min_areas THEN 1 ELSE 0 END AS 최소_영역_수_충족
FROM general_education_requirements AS gr
JOIN general_education_requirement_categories AS gc
    ON gc.general_requirement_id = gr.general_requirement_id
WHERE gr.cohort_start <= 2024
  AND (gr.cohort_end IS NULL OR gr.cohort_end >= 2024)
  AND gc.requirement_code = 'DISTRIBUTION';
```
정답 컬럼: remaining_credits, remaining_areas, meets_both / 예측 컬럼: 부족_학점, 부족_영역_수, 최소_학점_충족, 최소_영역_수_충족
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
    MAX(0, gec.min_credits - 12) AS 부족_학점,
    MAX(0, COALESCE(gec.min_areas, 0) - 4) AS 부족_영역_수,
    CASE WHEN 12 >= gec.min_credits THEN 1 ELSE 0 END AS 학점_조건_충족,
    CASE WHEN gec.min_areas IS NULL OR 4 >= gec.min_areas THEN 1 ELSE 0 END AS 영역_조건_충족
FROM general_education_requirements AS ger
JOIN general_education_requirement_categories AS gec
    ON gec.general_requirement_id = ger.general_requirement_id
WHERE ger.cohort_start <= 2024
  AND (ger.cohort_end IS NULL OR ger.cohort_end >= 2024)
  AND gec.requirement_code = 'DISTRIBUTION';
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
