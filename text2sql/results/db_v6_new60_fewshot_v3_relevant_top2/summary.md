# Text2SQL 평가 결과 (2026-11-20 01:29)

| 지표 | 값 |
|---|---|
| 평가 문항 수 | 60 |
| 실행 성공률(최종) | 60/60 (100.0%) |
| 실행 성공률(1차 시도) | 60/60 (100.0%) |
| 정답률 strict | 43/60 (71.7%) |
| 정답률 relaxed | 50/60 (83.3%) |
| 정답률 subset (정답 일부 컬럼 누락 허용) | 50/60 (83.3%) |
| 평균 토큰 | 4727.5 |
| 총 토큰 | 283650 |
| 평균 응답시간(초) | 6.03 |

## 유형별

| 태그 | n | strict | relaxed | subset | 실행 성공 |
|---|---|---|---|---|---|
| student_life | 60 | 43/60 (71.7%) | 50/60 (83.3%) | 50/60 (83.3%) | 60/60 (100.0%) |
| 강의계획서 | 10 | 9/10 (90.0%) | 10/10 (100.0%) | 10/10 (100.0%) | 10/10 (100.0%) |
| 과제·프로젝트 | 6 | 1/6 (16.7%) | 2/6 (33.3%) | 2/6 (33.3%) | 6/6 (100.0%) |
| 교재·참고자료 | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| 면담·수업방식 | 5 | 3/5 (60.0%) | 5/5 (100.0%) | 5/5 (100.0%) | 5/5 (100.0%) |
| 수강 요건 | 4 | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) | 4/4 (100.0%) |
| 수강신청 | 9 | 5/9 (55.6%) | 6/9 (66.7%) | 6/9 (66.7%) | 9/9 (100.0%) |
| 시간표 | 8 | 6/8 (75.0%) | 7/8 (87.5%) | 7/8 (87.5%) | 8/8 (100.0%) |
| 시간표·강의실 | 8 | 6/8 (75.0%) | 6/8 (75.0%) | 6/8 (75.0%) | 8/8 (100.0%) |
| 자료 연결 | 6 | 5/6 (83.3%) | 6/6 (100.0%) | 6/6 (100.0%) | 6/6 (100.0%) |

## 진단 분포

| 진단 | 개수 |
|---|---|
| correct | 43 |
| correct_extra_columns | 7 |
| row_count_mismatch | 6 |
| value_mismatch | 4 |

## 정답 재검토가 필요한 문항

- N001 (O): 2026년 2학기 컴퓨터공학과 개설목록에서 컴퓨터네트워크(CSE302) 금요일 수업은 몇 시에 시작하고 어디로 가면 돼? — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N002 (O): 2026년 2학기 컴퓨터공학과 자료구조(CSE204) 듣고 싶은데, 금요일에는 학교에 못 가고 오전 수업도 어려워. 정규 수업이 전부 낮 12시 이후인 분반 번호가 뭐야? 정오 시작은 괜찮아. — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N003 (O): 화요일에 알바가 있어서 일찍 끝나는 분반으로 바꾸고 싶어. 2026년 2학기 컴퓨터공학과 객체지향프로그래밍(CSE103) 중 화요일에 가장 먼저 끝나는 분반과 끝나는 시간이 뭐야? 동률이면 다 알려줘. — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N004 (O): 2026년 2학기 컴퓨터공학과에서 데이터베이스 01분반(CSE305-01) 듣고 바로 컴퓨터네트워크 02분반(CSE302-02)으로 가야 해. 화요일에 앞 수업 끝나고 다음 수업 시작까지 몇 분 있어? — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N005 (X): 2026년 2학기 컴퓨터공학과 자료구조 02분반(CSE204-02)은 이미 시간표에 넣었어. 컴퓨터네트워크(CSE302) 중 정규 수업이 한 번도 겹치지 않는 분반을 전부 알려줘. — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N006 (O): 2026년 2학기 컴퓨터공학과 알고리즘 00분반(CSE304-00) 전에 월요일에 30분은 쉬고 싶어. 소프트웨어공학(CSE327) 중 월요일 수업을 그만큼 일찍 끝낼 수 있는 분반과 쉬는 시간을 알려줘. — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N007 (O): 2026년 2학기 컴퓨터공학과 월요일 논리회로 03분반(EE209-03) 다음에 운영체제 01분반(CSE301-01)을 들으려고 해. 두 수업 강의실 코드가 각각 뭐고, 사이에 몇 분 있어? — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N008 (X): 2026년 2학기 컴퓨터공학과 목요일에 컴퓨터구조 00분반(CSE203-00)이랑 데이터베이스 01분반(CSE305-01)을 들어. 시작이 빠른 순서대로 강좌코드·분반, 시작 시간, 강의실을 정리해 줘. — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N009 (X): 2026년 2학기 컴퓨터공학과 데이터베이스(CSE305) 두 분반 중 평소 온라인으로 듣는 게 어느 쪽인지 헷갈려. 분반별로 온라인인지 대면인지 알려줘. — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N010 (X): 2026년 2학기 소프트웨어융합학과 개설목록에서 웹/파이선프로그래밍(SWCON104)이랑 운영체제(CSE301) 중 정규 수업이 온라인으로 표시된 분반만 보고 싶어. 강좌코드·분반과 개설목록의 수강정원을 알려줘. — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N011 (O): 2026년 2학기 컴퓨터공학과 개설목록에서 컴퓨터구조(CSE203) 00분반이랑 01분반의 대상 학년과 개설목록 수강정원이 각각 어떻게 돼? — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N012 (O): 2026년 2학기 컴퓨터공학과 자료구조 02분반(CSE204-02)의 개설목록 수강정원은 00분반보다 몇 명 더 많아? — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N013 (O): 친구는 인공지능학과고 저는 소프트웨어융합학과예요. 2026년 2학기 데이터베이스 01분반(CSE305-01)이 양쪽 학과 개설목록에서 각각 전공필수인지 전공선택인지 알려 주세요. — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N014 (O): 2026년 2학기 컴퓨터공학과 객체지향프로그래밍(CSE103)을 듣는데 영어 부분강좌는 피하고 싶어. 영어강좌 표시가 없는 분반의 화요일 시작 시간도 같이 알려줘. — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N015 (X): 2026년 2학기 컴퓨터공학과 데이터베이스 00분반(CSE305-00)과 캡스톤디자인 01분반(CSE406-01) 둘 다 정규 수업시간 칸에 시간이 없는데, 각각 온라인 표기인지 시간 미기재인지 구분해 줘. — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N016 (O): 2026년에 컴퓨터공학과 운영체제(CSE301) 온라인 분반이 1학기와 2학기 중 언제 열렸어? 온라인으로 표시된 학기랑 분반 번호를 알려줘. — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N017 (X): 금요일에 학교에 못 가서 2026년 2학기 컴퓨터공학과 컴퓨터네트워크(CSE302) 다른 분반을 보려고 해. 금요일 수업이 없는 분반 중 개설목록 수강정원이 가장 큰 분반은? 같으면 모두 알려줘. — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N018 (O): 중고책 찾으려고 하는데, 2026년 1학기 자료구조 01분반(CSE204-01) 강의계획서 교재 1번의 제목과 ISBN을 알려줘. — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N019 (O): 2026년 1학기 운영체제 01분반(CSE301-01)을 예습하려고 해. 강의계획서 교재 1번의 판이 포함된 책 제목과 출판연도가 뭐야? — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N020 (O): 2025년 1학기 알고리즘 00분반(CSE304-00)에서 동적계획법을 처음 다루는 건 몇 주차야? — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N021 (O): 2026년 1학기 운영체제 01분반(CSE301-01)에서 Deadlocks를 강의계획서상 몇 주차에 다뤄? 해당 주차 날짜 범위도 알려줘. — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N022 (O): 2025년 2학기 컴퓨터네트워크 01분반(CSE302-01) 중간시험 보려면 뭘 준비하고 어디에 접속해야 해? 강의계획서 8주차 비고 기준으로 알려줘. — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N023 (O): 2026년 1학기 캡스톤디자인 01분반(CSE406-01)에서 최종보고서 작성·발표가 강의계획서에 처음 나오는 주차가 언제야? — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N024 (O): 2025년 2학기 블록체인 00분반(CSE442-00)에서 산업 전문가 특강을 들으려면 강의계획서상 몇 주차를 보면 돼? 특강이 나오는 주차를 전부 알려줘. — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N025 (X): 2025년 2학기 세계신화읽기 00분반(ELC281-00)은 추석 있는 6주차에 수업 일정이 어떻게 표시돼? 계획서에 적힌 두 날짜와 휴일 종류를 알려줘. — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N026 (O): 2026년 1학기 캡스톤디자인 01분반(CSE406-01) 준비물 사기 전에 확인하고 싶어. 강의계획서 교재란에 제목이 적힌 교재가 몇 권 있어? — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N027 (O): 2025년 2학기 컴퓨터네트워크 01분반(CSE302-01) 교수님께 질문하러 가려는데, 강의계획서에 적힌 연구실과 면담 방법이 뭐야? — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N028 (O): 2025년 2학기 컴퓨터공학과 개설목록의 컴퓨터네트워크 01분반(CSE302-01)은 수강정원이 몇 명이었고, 강의계획서 교재 1번 제목은 뭐였어? — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N029 (X): 2026년 1학기 컴퓨터공학과 자료구조 01분반(CSE204-01), 화요일 정규 수업은 몇 시에 어디서 듣고 4주차에는 어떤 단원을 공부해? — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N030 (O): 2025년 2학기 컴퓨터네트워크 01분반(CSE302-01)은 강의계획서에서 중간시험을 몇 주차에 보며, 교재 1번 ISBN은 뭐야? 교재 구매 전에 같이 확인하고 싶어. — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N031 (X): 2026년 2학기 컴퓨터공학과에서 소프트웨어공학(CSE327)이랑 논리회로(EE209)를 같이 담고 싶어. 금요일 수업이 없고, 둘 다 오후 5시까지 끝나면서 정규 수업끼리 안 겹치는 분반 조합을 전부 알려줘. — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N032 (X): 2026년 2학기 컴퓨터공학과 데이터베이스 01분반(CSE305-01) 때문에 학교에 가는 요일만 유지하고 싶어. 등교하는 요일을 늘리지 않고 시간도 안 겹치게 추가할 수 있는 컴퓨터네트워크(CSE302) 분반은 뭐야? — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N033 (O): 2026년 2학기 컴퓨터공학과 이산구조 01분반(CSE201-01)과 메타버스데이터처리 00분반(CSE430-00)을 둘 다 들으면, 수요일 첫 수업 시작부터 마지막 수업 끝까지 몇 분이야? 시작과 종료 시각도 알려줘. — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N034 (O): 2026년 2학기 컴퓨터공학과 자료구조(CSE204) 금요일에 몰아서 듣는 00분반하고 월·수 01분반의 주당 정규 수업시간을 비교하고 싶어. 개설목록 기준으로 분반별 총 몇 분이야? — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N035 (O): 2026년 2학기 금요일 B07에서 컴퓨터공학과 개설목록에 잡힌 수업이 뭐야? 개설목록 범위에서 강좌코드·분반과 사용 시간을 시작 순으로 알려줘. — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N036 (O): 2026년 2학기 소프트웨어융합학과 소프트웨어융합캡스톤디자인(SWCON401) 중 금요일 오후 3시에 시작하고 개설목록에 강의실까지 적힌 분반은 뭐야? 분반과 강의실 코드를 알려줘. — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N037 (O): 작년 자료 말고 2026년 1·2학기를 비교하고 싶어. 컴퓨터공학과 데이터베이스 01분반(CSE305-01) 목요일 수업 강의실이 학기별로 어디였어? — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N038 (O): 2026년 2학기 소프트웨어융합학과 데이터분석캡스톤디자인(SWCON321) 신청하려고 하는데 목요일에 밤 9시 넘어서 끝나는 분반을 피하고 싶어. 해당 분반 번호랑 종료 시각을 알려줘. — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N039 (O): 졸업논문도 학점이 들어가는지 헷갈려. 2026년 2학기 소프트웨어융합학과의 SWCON402-00과 인공지능학과의 AI4003-00은 개설목록상 각각 몇 학점이야? — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N040 (O): 2026년 2학기 소프트웨어융합캡스톤디자인 03분반(SWCON401-03) 들으려는데, 강의계획서 필수 선수과목 그룹 01에서 코드가 서로 다른 선택지는 몇 개고 그중 최소 몇 과목을 이수해야 해? — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N041 (O): 고급객체지향프로그래밍(CSE202)만 이수했다고 가정할게. 2026년 1학기 자료구조 02분반(CSE204-02) 강의계획서에서 2024학번 비ABEEK 기준 필수 선수과목 그룹 01의 과목 수 조건을 채워? 충족이면 1, 아니면 0으로 알려줘. — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N042 (O): 2026년 2학기 캡스톤디자인 14분반(CSE406-14) 강의계획서의 비ABEEK 필수 선수과목 그룹 01에는 어떤 과목 코드가 있고, 몇 학번부터 몇 학번까지 적용돼? — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N043 (O): 2026년 2학기 연구연수활동2 04분반(CSE497-04)과 독립심화학습2 02분반(CSE499-02) 계획서를 보니 교재가 겹치는 것 같아. ISBN이 같은 공통 교재의 제목과 ISBN을 알려줘. — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N044 (O): 2026년 2학기 연구연수활동2 04분반(CSE497-04)에서 교재 1번을 찾고 있어. 강의계획서 교재란 비고에 적힌 링크 주소만 알려줘. — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N045 (O): 2026년 2학기 데이터사이언스및시각화 00분반(SWCON425-00) 교재 목록에서 최근에 출판된 책부터 읽고 싶어. 출판연도가 기재된 책 중 가장 최근 책의 제목과 연도는 뭐야? 같은 연도면 모두 알려줘. — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N046 (O): 2026년 2학기 캡스톤디자인(CSE406) 05분반이랑 14분반 중 교수님과 Slack에서 면담 일정을 정한다고 명시한 분반은 어디야? — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N047 (O): 2026년 2학기 데이터사이언스및시각화(SWCON425-00)와 데이터분석캡스톤디자인(SWCON321-00)에 같은 면담 시간 안내가 적혀 있으면, 공통으로 적힌 안내를 알려줘. — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N048 (O): 2026년 2학기 소프트웨어융합학과 데이터사이언스및시각화(SWCON425-00), 목요일 수업 장소랑 교수님 찾아가는 연구실이 자꾸 헷갈려. 개설목록 강의실 코드와 계획서에 적힌 연구실을 각각 알려줘. — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N049 (X): 소프트웨어융합캡스톤디자인 03분반(SWCON401-03)은 2026년 1학기와 2학기 강의계획서에서 수업 운영 방식이 각각 어떻게 안내돼? — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N050 (O): 2026년 1학기 소프트웨어융합캡스톤디자인(SWCON401) 03분반과 05분반 중, 계획서 수업방법에 개별발표 표시가 있고 팀별발표 표시는 없는 분반이 있어? — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N051 (X): 2026년 1학기 회로와신호 00분반(SWCON254-00) 숙제 3번을 미리 챙기고 싶어. 강의계획서 비고에서 몇 주차에 공지되고 몇 주차에 제출하라고 적혀 있어? — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N052 (X): 2026년 2학기 로봇·비전캡스톤디자인 00분반(SWCON332-00)은 강의계획서에서 설계서와 최종 결과 보고서를 각각 몇 주차에 내? — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N053 (X): 2026년 2학기 소프트웨어융합캡스톤디자인(SWCON401-03)과 졸업논문(SWCON402-00)을 같이 하는데, 계획서상 캡스톤 최종 발표와 졸업논문 결과보고서 제출이 같은 주야? 과목별 해당 주차를 알려줘. — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N054 (X): 2026년 2학기 객체지향프로그래밍 01분반(CSE103-01)에서 코드 리뷰 발표평가가 있는 주차를 빼놓지 않으려고 해. 강의계획서에 발표평가가 적힌 주차와 날짜 범위를 전부 알려줘. — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N055 (X): 2026년 1학기 강화학습 00분반(SWCON495-00)은 공휴일 때문에 대면수업을 못 하면 어떻게 진행한다고 강의계획서 운영방식에 적혀 있어? — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N056 (O): 2026년 1학기 강화학습 00분반(SWCON495-00)에서 수업자료 외에 참고할 책을 찾고 있어. 계획서 교재란에 부교재로 표시된 항목의 번호와 제목을 알려줘. — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N057 (X): 2026년 1학기 게임인터랙티브테크놀로지 00분반(SWCON312-00)에서 프로젝트 팀원을 언제 알아봐야 해? 계획서에 팀 구성이 처음 나오는 주차의 날짜 범위와 그 주 발표 준비 내용을 알려줘. — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N058 (O): 2026년 2학기 데이터사이언스및시각화 00분반(SWCON425-00)에서 대규모 언어 모델을 다루는 주차를 모두 알려줘. 각 주차에 기말시험도 같이 적혀 있는지 1 또는 0으로 표시해 줘. — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N059 (O): 2026년 2학기 소프트웨어융합학과 데이터사이언스및시각화(SWCON425-00) 교수님께 수요일에 가려고 해. 개설목록에 수요일 정규수업이 있는지 1 또는 0으로, 강의계획서의 면담 안내는 그대로 알려줘. — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.
- N060 (O): 2026년 2학기 컴퓨터공학과 이산구조 00분반(CSE201-00) 월요일 수업 끝나고 질문하려고 해. 정규 수업 종료 시각과 강의계획서의 면담 안내를 같이 알려줘. — 원천 기록에서 정답 산출. 기준 SQL은 oracle 점검용.

## 오답 목록

### N005 — correct_extra_columns
질문: 2026년 2학기 컴퓨터공학과 자료구조 02분반(CSE204-02)은 이미 시간표에 넣었어. 컴퓨터네트워크(CSE302) 중 정규 수업이 한 번도 겹치지 않는 분반을 전부 알려줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
WITH anchor_slots AS (
    SELECT ts.day, ts.start_time, ts.end_time
    FROM course_offerings AS o
    JOIN class_times AS ct ON ct.offering_id = o.offering_id
    JOIN time_slots AS ts ON ts.time_slot_id = ct.time_slot_id
    WHERE o.year = 2026
      AND o.semester = '2'
      AND o.course_code = 'CSE204'
      AND o.section = '02'
      AND o.schedule_status = 'SCHEDULED'
)
SELECT DISTINCT candidate.course_code, candidate.section
FROM course_offerings AS candidate
WHERE candidate.year = 2026
  AND candidate.semester = '2'
  AND candidate.course_code = 'CSE302'
  AND candidate.schedule_status = 'SCHEDULED'
  AND EXISTS (
      SELECT 1
      FROM class_times AS candidate_ct
      WHERE candidate_ct.offering_id = candidate.offering_id
  )
  AND NOT EXISTS (
      SELECT 1
      FROM class_times AS candidate_ct
      JOIN time_slots AS candidate_ts
        ON candidate_ts.time_slot_id = candidate_ct.time_slot_id
      JOIN anchor_slots AS anchor
        ON anchor.day = candidate_ts.day
       AND candidate_ts.start_time < anchor.end_time
       AND candidate_ts.end_time > anchor.start_time
      WHERE candidate_ct.offering_id = candidate.offering_id
  )
ORDER BY candidate.section;
```
정답 컬럼: section / 예측 컬럼: course_code, section
정답 행 수: 2 / 예측 행 수: 2

### N008 — value_mismatch
질문: 2026년 2학기 컴퓨터공학과 목요일에 컴퓨터구조 00분반(CSE203-00)이랑 데이터베이스 01분반(CSE305-01)을 들어. 시작이 빠른 순서대로 강좌코드·분반, 시작 시간, 강의실을 정리해 줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
SELECT o.course_code,
       o.section,
       ts.start_time,
       ct.room_code
FROM course_offerings AS o
JOIN courses AS c ON c.course_code = o.course_code
JOIN departments AS d ON d.department_id = c.department_id
JOIN class_times AS ct ON ct.offering_id = o.offering_id
JOIN time_slots AS ts ON ts.time_slot_id = ct.time_slot_id
WHERE o.year = 2026
  AND o.semester = '2'
  AND d.name = '컴퓨터공학과'
  AND (o.course_code, o.section) IN (('CSE203', '00'), ('CSE305', '01'))
  AND ts.day = 'thursday'
ORDER BY ts.start_time;
```
정답 컬럼: course_section, start_time, room_code / 예측 컬럼: course_code, section, start_time, room_code
정답 행 수: 2 / 예측 행 수: 2

### N009 — value_mismatch
질문: 2026년 2학기 컴퓨터공학과 데이터베이스(CSE305) 두 분반 중 평소 온라인으로 듣는 게 어느 쪽인지 헷갈려. 분반별로 온라인인지 대면인지 알려줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
SELECT o.section,
       CASE o.delivery_mode
           WHEN 'ONLINE' THEN '온라인'
           WHEN 'OFFLINE' THEN '대면'
           WHEN 'HYBRID' THEN '온·오프라인'
           WHEN 'TBD' THEN '미정'
       END AS delivery_mode
FROM course_offerings AS o
WHERE o.year = 2026
  AND o.semester = '2'
  AND o.course_code = 'CSE305'
ORDER BY o.section;
```
정답 컬럼: section, delivery_mode / 예측 컬럼: section, delivery_mode
정답 행 수: 2 / 예측 행 수: 2

### N010 — row_count_mismatch
질문: 2026년 2학기 소프트웨어융합학과 개설목록에서 웹/파이선프로그래밍(SWCON104)이랑 운영체제(CSE301) 중 정규 수업이 온라인으로 표시된 분반만 보고 싶어. 강좌코드·분반과 개설목록의 수강정원을 알려줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
SELECT o.course_code || '-' || o.section AS course_section,
       o.capacity
FROM course_offerings AS o
WHERE o.year = 2026
  AND o.semester = '2'
  AND o.course_code IN ('SWCON104', 'CSE301')
  AND o.delivery_mode = 'ONLINE'
  AND o.schedule_status = 'SCHEDULED'
  AND EXISTS (
      SELECT 1
      FROM course_offering_categories AS oc
      JOIN departments AS d ON d.department_id = oc.department_id
      WHERE oc.offering_id = o.offering_id
        AND d.name = '소프트웨어융합학과'
  );
```
정답 컬럼: course_section, capacity / 예측 컬럼: course_section, capacity
정답 행 수: 2 / 예측 행 수: 0

### N015 — correct_extra_columns
질문: 2026년 2학기 컴퓨터공학과 데이터베이스 00분반(CSE305-00)과 캡스톤디자인 01분반(CSE406-01) 둘 다 정규 수업시간 칸에 시간이 없는데, 각각 온라인 표기인지 시간 미기재인지 구분해 줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
SELECT o.course_code || '-' || o.section AS course_section,
       o.delivery_mode,
       o.schedule_status,
       CASE
           WHEN o.delivery_mode = 'ONLINE' THEN '온라인 표기'
           WHEN NOT EXISTS (
               SELECT 1
               FROM class_times AS ct
               WHERE ct.offering_id = o.offering_id
           ) THEN '시간 미기재'
           ELSE '정규 수업시간 있음'
       END AS time_classification
FROM course_offerings AS o
WHERE o.year = 2026
  AND o.semester = '2'
  AND (o.course_code, o.section) IN (('CSE305', '00'), ('CSE406', '01'))
ORDER BY o.course_code, o.section;
```
정답 컬럼: course_section, schedule_status / 예측 컬럼: course_section, delivery_mode, schedule_status, time_classification
정답 행 수: 2 / 예측 행 수: 2

### N017 — value_mismatch
질문: 금요일에 학교에 못 가서 2026년 2학기 컴퓨터공학과 컴퓨터네트워크(CSE302) 다른 분반을 보려고 해. 금요일 수업이 없는 분반 중 개설목록 수강정원이 가장 큰 분반은? 같으면 모두 알려줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
WITH eligible AS (
    SELECT DISTINCT o.offering_id, o.course_code, o.section, o.capacity
    FROM course_offerings AS o
    JOIN course_offering_categories AS oc ON oc.offering_id = o.offering_id
    JOIN departments AS d ON d.department_id = oc.department_id
    WHERE o.year = 2026
      AND o.semester = '2'
      AND o.course_code = 'CSE302'
      AND d.name = '컴퓨터공학과'
      AND NOT EXISTS (
          SELECT 1
          FROM class_times AS ct
          JOIN time_slots AS ts ON ts.time_slot_id = ct.time_slot_id
          WHERE ct.offering_id = o.offering_id
            AND ts.day = 'friday'
      )
)
SELECT course_code || '-' || section AS course_section,
       capacity
FROM eligible
WHERE capacity = (SELECT MAX(capacity) FROM eligible)
ORDER BY course_section;
```
정답 컬럼: section, capacity / 예측 컬럼: course_section, capacity
정답 행 수: 2 / 예측 행 수: 2

### N025 — correct_extra_columns
질문: 2025년 2학기 세계신화읽기 00분반(ELC281-00)은 추석 있는 6주차에 수업 일정이 어떻게 표시돼? 계획서에 적힌 두 날짜와 휴일 종류를 알려줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
SELECT wp.date_range,
       wp.topic_content,
       wp.note
FROM course_offerings AS o
JOIN syllabi AS s ON s.offering_id = o.offering_id
JOIN syllabus_weekly_plans AS wp ON wp.syllabus_id = s.syllabus_id
WHERE o.year = 2025
  AND o.semester = '2'
  AND o.course_code = 'ELC281'
  AND o.section = '00'
  AND wp.week = 6;
```
정답 컬럼: topic_content / 예측 컬럼: date_range, topic_content, note
정답 행 수: 1 / 예측 행 수: 1

### N029 — correct_extra_columns
질문: 2026년 1학기 컴퓨터공학과 자료구조 01분반(CSE204-01), 화요일 정규 수업은 몇 시에 어디서 듣고 4주차에는 어떤 단원을 공부해?

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
SELECT DISTINCT ts.start_time,
       ts.end_time,
       ct.room_code,
       wp.topic_content
FROM course_offerings AS o
JOIN class_times AS ct ON ct.offering_id = o.offering_id
JOIN time_slots AS ts ON ts.time_slot_id = ct.time_slot_id
JOIN syllabi AS s ON s.offering_id = o.offering_id
JOIN syllabus_weekly_plans AS wp
  ON wp.syllabus_id = s.syllabus_id
WHERE o.year = 2026
  AND o.semester = '1'
  AND o.course_code = 'CSE204'
  AND o.section = '01'
  AND o.schedule_status = 'SCHEDULED'
  AND ts.day = 'tuesday'
  AND wp.week = 4
ORDER BY ts.start_time;
```
정답 컬럼: start_time, room_code, topic_content / 예측 컬럼: start_time, end_time, room_code, topic_content
정답 행 수: 1 / 예측 행 수: 1

### N031 — row_count_mismatch
질문: 2026년 2학기 컴퓨터공학과에서 소프트웨어공학(CSE327)이랑 논리회로(EE209)를 같이 담고 싶어. 금요일 수업이 없고, 둘 다 오후 5시까지 끝나면서 정규 수업끼리 안 겹치는 분반 조합을 전부 알려줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
WITH candidates AS (
    SELECT o.offering_id, o.course_code, o.section
    FROM course_offerings AS o
    JOIN courses AS c ON c.course_code = o.course_code
    JOIN departments AS d ON d.department_id = c.department_id
    WHERE o.year = 2026
      AND o.semester = '2'
      AND d.name = '컴퓨터공학과'
      AND o.course_code IN ('CSE327', 'EE209')
      AND o.schedule_status = 'SCHEDULED'
      AND EXISTS (
          SELECT 1
          FROM class_times AS ct
          WHERE ct.offering_id = o.offering_id
      )
      AND NOT EXISTS (
          SELECT 1
          FROM class_times AS ct
          JOIN time_slots AS ts ON ts.time_slot_id = ct.time_slot_id
          WHERE ct.offering_id = o.offering_id
            AND (ts.day = 'friday' OR ts.end_time > '17:00')
      )
)
SELECT cse.course_code || '-' || cse.section AS cse327_section,
       ee.course_code || '-' || ee.section AS ee209_section
FROM candidates AS cse
JOIN candidates AS ee
  ON cse.course_code = 'CSE327'
 AND ee.course_code = 'EE209'
WHERE NOT EXISTS (
    SELECT 1
    FROM class_times AS ct1
    JOIN time_slots AS ts1 ON ts1.time_slot_id = ct1.time_slot_id
    JOIN class_times AS ct2 ON ct2.offering_id = ee.offering_id
    JOIN time_slots AS ts2 ON ts2.time_slot_id = ct2.time_slot_id
    WHERE ct1.offering_id = cse.offering_id
      AND ts1.day = ts2.day
      AND ts1.start_time < ts2.end_time
      AND ts2.start_time < ts1.end_time
)
ORDER BY cse.section, ee.section;
```
정답 컬럼: software_section, logic_section / 예측 컬럼: cse327_section, ee209_section
정답 행 수: 4 / 예측 행 수: 0

### N032 — value_mismatch
질문: 2026년 2학기 컴퓨터공학과 데이터베이스 01분반(CSE305-01) 때문에 학교에 가는 요일만 유지하고 싶어. 등교하는 요일을 늘리지 않고 시간도 안 겹치게 추가할 수 있는 컴퓨터네트워크(CSE302) 분반은 뭐야?

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
WITH target_slots AS (
    SELECT ts.day, ts.start_time, ts.end_time
    FROM course_offerings AS o
    JOIN class_times AS ct ON ct.offering_id = o.offering_id
    JOIN time_slots AS ts ON ts.time_slot_id = ct.time_slot_id
    WHERE o.year = 2026
      AND o.semester = '2'
      AND o.course_code = 'CSE305'
      AND o.section = '01'
)
SELECT DISTINCT c.course_code || '-' || c.section AS course_section
FROM course_offerings AS c
WHERE c.year = 2026
  AND c.semester = '2'
  AND c.course_code = 'CSE302'
  AND EXISTS (
      SELECT 1
      FROM class_times AS ct
      WHERE ct.offering_id = c.offering_id
  )
  AND NOT EXISTS (
      SELECT 1
      FROM class_times AS ct
      JOIN time_slots AS ts ON ts.time_slot_id = ct.time_slot_id
      WHERE ct.offering_id = c.offering_id
        AND NOT EXISTS (
            SELECT 1
            FROM target_slots AS t
            WHERE t.day = ts.day
        )
  )
  AND NOT EXISTS (
      SELECT 1
      FROM class_times AS ct
      JOIN time_slots AS ts ON ts.time_slot_id = ct.time_slot_id
      JOIN target_slots AS t ON t.day = ts.day
      WHERE ct.offering_id = c.offering_id
        AND ts.start_time < t.end_time
        AND t.start_time < ts.end_time
  )
ORDER BY c.section;
```
정답 컬럼: section / 예측 컬럼: course_section
정답 행 수: 1 / 예측 행 수: 1

### N049 — correct_extra_columns
질문: 소프트웨어융합캡스톤디자인 03분반(SWCON401-03)은 2026년 1학기와 2학기 강의계획서에서 수업 운영 방식이 각각 어떻게 안내돼?

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
SELECT o.semester, s.operation_modes, s.operation_note
FROM course_offerings AS o
JOIN syllabi AS s ON s.offering_id = o.offering_id
WHERE o.year = 2026
  AND o.semester IN ('1', '2')
  AND o.course_code = 'SWCON401'
  AND o.section = '03'
ORDER BY o.semester;
```
정답 컬럼: semester, operation_modes / 예측 컬럼: semester, operation_modes, operation_note
정답 행 수: 2 / 예측 행 수: 2

### N051 — row_count_mismatch
질문: 2026년 1학기 회로와신호 00분반(SWCON254-00) 숙제 3번을 미리 챙기고 싶어. 강의계획서 비고에서 몇 주차에 공지되고 몇 주차에 제출하라고 적혀 있어?

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
SELECT wp.week, wp.note
FROM course_offerings AS o
JOIN syllabi AS s ON s.offering_id = o.offering_id
JOIN syllabus_weekly_plans AS wp ON wp.syllabus_id = s.syllabus_id
WHERE o.year = 2026
  AND o.semester = '1'
  AND o.course_code = 'SWCON254'
  AND o.section = '00'
  AND COALESCE(wp.note, '') LIKE '%숙제%'
  AND COALESCE(wp.note, '') LIKE '%3%'
ORDER BY wp.week;
```
정답 컬럼: notice_week, submission_week / 예측 컬럼: week, note
정답 행 수: 1 / 예측 행 수: 2

### N052 — row_count_mismatch
질문: 2026년 2학기 로봇·비전캡스톤디자인 00분반(SWCON332-00)은 강의계획서에서 설계서와 최종 결과 보고서를 각각 몇 주차에 내?

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
SELECT wp.week, wp.topic_content, wp.note
FROM course_offerings AS o
JOIN syllabi AS s ON s.offering_id = o.offering_id
JOIN syllabus_weekly_plans AS wp ON wp.syllabus_id = s.syllabus_id
WHERE o.year = 2026
  AND o.semester = '2'
  AND o.course_code = 'SWCON332'
  AND o.section = '00'
  AND (wp.topic_content LIKE '%설계서%'
       OR wp.note LIKE '%설계서%'
       OR wp.topic_content LIKE '%최종 결과 보고서%'
       OR wp.note LIKE '%최종 결과 보고서%')
ORDER BY wp.week;
```
정답 컬럼: design_submission_week, final_report_week / 예측 컬럼: week, topic_content, note
정답 행 수: 1 / 예측 행 수: 2

### N053 — row_count_mismatch
질문: 2026년 2학기 소프트웨어융합캡스톤디자인(SWCON401-03)과 졸업논문(SWCON402-00)을 같이 하는데, 계획서상 캡스톤 최종 발표와 졸업논문 결과보고서 제출이 같은 주야? 과목별 해당 주차를 알려줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
WITH target_offerings AS (
    SELECT o.offering_id, o.course_code, o.section
    FROM course_offerings AS o
    WHERE o.year = 2026
      AND o.semester = '2'
      AND (
          (o.course_code = 'SWCON401' AND o.section = '03')
          OR (o.course_code = 'SWCON402' AND o.section = '00')
      )
),
course_weeks AS (
    SELECT t.course_code,
           t.section,
           MIN(CASE
                   WHEN t.course_code = 'SWCON401'
                    AND (COALESCE(w.topic_content, '') || ' ' || COALESCE(w.note, ''))
                        LIKE '%최종%발표%'
                   THEN w.week
                   WHEN t.course_code = 'SWCON402'
                    AND (COALESCE(w.topic_content, '') || ' ' || COALESCE(w.note, ''))
                        LIKE '%결과보고서%제출%'
                   THEN w.week
               END) AS relevant_week
    FROM target_offerings AS t
    LEFT JOIN syllabi AS s ON s.offering_id = t.offering_id
    LEFT JOIN syllabus_weekly_plans AS w ON w.syllabus_id = s.syllabus_id
    GROUP BY t.course_code, t.section
)
SELECT MAX(CASE WHEN course_code = 'SWCON401' THEN relevant_week END) AS capstone_final_presentation_week,
       MAX(CASE WHEN course_code = 'SWCON402' THEN relevant_week END) AS thesis_result_report_submission_week,
       CASE
           WHEN MAX(CASE WHEN course_code = 'SWCON401' THEN relevant_week END) IS NULL
             OR MAX(CASE WHEN course_code = 'SWCON402' THEN relevant_week END) IS NULL
           THEN NULL
           WHEN MAX(CASE WHEN course_code = 'SWCON401' THEN relevant_week END)
              = MAX(CASE WHEN course_code = 'SWCON402' THEN relevant_week END)
           THEN 1
           ELSE 0
       END AS same_week
FROM course_weeks;
```
정답 컬럼: course_code, week / 예측 컬럼: capstone_final_presentation_week, thesis_result_report_submission_week, same_week
정답 행 수: 2 / 예측 행 수: 1

### N054 — row_count_mismatch
질문: 2026년 2학기 객체지향프로그래밍 01분반(CSE103-01)에서 코드 리뷰 발표평가가 있는 주차를 빼놓지 않으려고 해. 강의계획서에 발표평가가 적힌 주차와 날짜 범위를 전부 알려줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
SELECT DISTINCT wp.week, wp.date_range
FROM course_offerings AS o
JOIN syllabi AS s ON s.offering_id = o.offering_id
JOIN syllabus_weekly_plans AS wp ON wp.syllabus_id = s.syllabus_id
WHERE o.year = 2026
  AND o.semester = '2'
  AND o.course_code = 'CSE103'
  AND o.section = '01'
  AND (
      COALESCE(wp.topic_content, '') || ' ' || COALESCE(wp.note, '')
  ) LIKE '%코드 리뷰%'
  AND (
      COALESCE(wp.topic_content, '') || ' ' || COALESCE(wp.note, '')
  ) LIKE '%발표평가%'
ORDER BY wp.week;
```
정답 컬럼: week, date_range / 예측 컬럼: week, date_range
정답 행 수: 3 / 예측 행 수: 0

### N055 — correct_extra_columns
질문: 2026년 1학기 강화학습 00분반(SWCON495-00)은 공휴일 때문에 대면수업을 못 하면 어떻게 진행한다고 강의계획서 운영방식에 적혀 있어?

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
SELECT s.operation_modes, s.operation_note
FROM course_offerings AS o
JOIN syllabi AS s ON s.offering_id = o.offering_id
WHERE o.year = 2026
  AND o.semester = '1'
  AND o.course_code = 'SWCON495'
  AND o.section = '00';
```
정답 컬럼: operation_note / 예측 컬럼: operation_modes, operation_note
정답 행 수: 1 / 예측 행 수: 1

### N057 — correct_extra_columns
질문: 2026년 1학기 게임인터랙티브테크놀로지 00분반(SWCON312-00)에서 프로젝트 팀원을 언제 알아봐야 해? 계획서에 팀 구성이 처음 나오는 주차의 날짜 범위와 그 주 발표 준비 내용을 알려줘.

gold:
```sql
(gold_answer 사용)
```
pred:
```sql
WITH first_team_week AS (
    SELECT MIN(w.week) AS week
    FROM course_offerings AS o
    JOIN syllabi AS s ON s.offering_id = o.offering_id
    JOIN syllabus_weekly_plans AS w ON w.syllabus_id = s.syllabus_id
    WHERE o.year = 2026
      AND o.semester = '1'
      AND o.course_code = 'SWCON312'
      AND o.section = '00'
      AND (
          COALESCE(w.topic_content, '') LIKE '%팀 구성%'
          OR COALESCE(w.topic_content, '') LIKE '%팀원%'
          OR COALESCE(w.note, '') LIKE '%팀 구성%'
          OR COALESCE(w.note, '') LIKE '%팀원%'
      )
)
SELECT w.date_range, w.topic_content, w.note
FROM course_offerings AS o
JOIN syllabi AS s ON s.offering_id = o.offering_id
JOIN syllabus_weekly_plans AS w ON w.syllabus_id = s.syllabus_id
JOIN first_team_week AS f ON f.week = w.week
WHERE o.year = 2026
  AND o.semester = '1'
  AND o.course_code = 'SWCON312'
  AND o.section = '00';
```
정답 컬럼: date_range, topic_content / 예측 컬럼: date_range, topic_content, note
정답 행 수: 1 / 예측 행 수: 1


## 진단 코드 설명

- correct: 결과 완전 일치 / correct_extra_columns: 컬럼이 더 있거나 컬럼 순서가 다름(relaxed 정답)
- missing_columns: 예측 값은 모두 맞지만 정답의 일부 컬럼이 빠짐(subset 정답, 사람이 확인)
- order_mismatch: 행 정렬만 다름(relaxed 정답) / row_count_mismatch: 행 수가 다름 / value_mismatch: 행 수는 같지만 값이 다름
- exec_fail:sqlite 실행 오류 / exec_fail:guard 안전장치에 의해 거부 / exec_fail:no_sql SQL 추출 실패
- exec_fail:timeout 시간 초과 / exec_fail:refused 거부하면 안 되는 질문을 거부
- correct_refusal: 거부가 정답인 문항을 거부·차단 / no_leak_but_not_refused: 거부는 안 했지만 결과 0행
- should_have_refused: 거부해야 하는데 결과를 돌려줌 / api_error ChatKHU 호출 실패 / gold_invalid 정답 SQL 문제
