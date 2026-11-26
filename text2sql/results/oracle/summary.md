# Text2SQL 평가 결과 (2026-10-15 22:28)

| 지표 | 값 |
|---|---|
| 평가 문항 수 | 16 |
| 실행 성공률(최종) | 16/16 (100.0%) |
| 실행 성공률(1차 시도) | 16/16 (100.0%) |
| 정답률 strict | 16/16 (100.0%) |
| 정답률 relaxed | 16/16 (100.0%) |
| 정답률 subset (정답 일부 컬럼 누락 허용) | 16/16 (100.0%) |
| 평균 토큰 | 0 |
| 평균 응답시간(초) | 0 |

## 유형별

| 태그 | n | strict | relaxed | subset | 실행 성공 |
|---|---|---|---|---|---|
| (태그 없음) | 16 | 16/16 (100.0%) | 16/16 (100.0%) | 16/16 (100.0%) | 16/16 (100.0%) |

## 진단 분포

| 진단 | 개수 |
|---|---|
| correct | 16 |

## 진단 코드 설명

- correct: 결과 완전 일치 / correct_extra_columns: 컬럼이 더 있거나 컬럼 순서가 다름(relaxed 정답)
- missing_columns: 예측 값은 모두 맞지만 정답의 일부 컬럼이 빠짐(subset 정답, 사람이 확인)
- order_mismatch: 행 정렬만 다름(relaxed 정답) / row_count_mismatch: 행 수가 다름 / value_mismatch: 행 수는 같지만 값이 다름
- exec_fail:sqlite 실행 오류 / exec_fail:guard 안전장치에 의해 거부 / exec_fail:no_sql SQL 추출 실패
- exec_fail:timeout 시간 초과 / exec_fail:refused 거부하면 안 되는 질문을 거부
- correct_refusal: 거부가 정답인 문항을 거부·차단 / no_leak_but_not_refused: 거부는 안 했지만 결과 0행
- should_have_refused: 거부해야 하는데 결과를 돌려줌 / api_error ChatKHU 호출 실패 / gold_invalid 정답 SQL 문제
