# 실행평가_15문항 zero-shot 모델 비교 (2026-11-05)

gold: text2sql/gold/실행평가_15문항.json / 문항표: O=strict, △=relaxed·subset만 정답, X=오답 / 최대비용=10k 토큰당 20 기준

| 모델 | n | strict | relaxed | subset | 재시도 | API오류 | 토큰 | 최대비용 | 평균지연(s) |
|---|---|---|---|---|---|---|---|---|---|
| gemini-4-argon | 15 | 11 | 14 | 14 | 0 | 0 | 67,290 | 135 | 9.2 |
| gemini-3.1-pro-preview | 15 | 12 | 13 | 13 | 0 | 0 | 68,172 | 136 | 16.9 |
| gemini-3.5-flash | 15 | 12 | 13 | 13 | 0 | 0 | 68,277 | 137 | 11.7 |
| gemini-3.5-flash-lite | 15 | 12 | 12 | 12 | 3 | 0 | 83,400 | 167 | 2.2 |
| claude-sonnet-5-5 | 15 | 12 | 12 | 12 | 0 | 0 | 122,136 | 244 | 5.2 |
| gpt-5.6-luna | 15 | 11 | 12 | 12 | 0 | 0 | 62,598 | 125 | 5.8 |
| gemini-3.6-flash | 15 | 11 | 12 | 12 | 0 | 0 | 68,199 | 136 | 12.5 |
| claude-sonnet-5 | 15 | 11 | 12 | 12 | 2 | 0 | 137,966 | 276 | 6.2 |
| gpt-6-luna | 15 | 10 | 11 | 11 | 0 | 0 | 64,235 | 128 | 7.8 |
| gpt-5.6-terra | 15 | 10 | 11 | 11 | 4 | 0 | 77,531 | 155 | 5.2 |
| gemini-3.8-flash | 15 | 9 | 10 | 10 | 0 | 0 | 68,263 | 137 | 15.6 |
| gemini-3.7-flash | 15 | 8 | 10 | 10 | 0 | 0 | 68,408 | 137 | 12.4 |
| gemini-3.1-flash-lite | 15 | 8 | 9 | 10 | 2 | 0 | 83,779 | 168 | 2.1 |
| claude-haiku-5-5 | 15 | 7 | 9 | 9 | 0 | 0 | 129,314 | 259 | 5.1 |
| claude-haiku-4-5-20251001 | 15 | 8 | 8 | 8 | 3 | 0 | 97,178 | 194 | 3.4 |

토큰 합계 1,266,746 / 최대비용 합계 2533

| 문항 | gemini-4-argon | gemini-3.1-pro-preview | gemini-3.5-flash | gemini-3.5-flash-lite | claude-sonnet-5-5 | gpt-5.6-luna | gemini-3.6-flash | claude-sonnet-5 | gpt-6-luna | gpt-5.6-terra | gemini-3.8-flash | gemini-3.7-flash | gemini-3.1-flash-lite | claude-haiku-5-5 | claude-haiku-4-5-20251001 | 정답 모델 수 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| J001 | △ | O | O | O | O | O | O | O | O | O | X | X | O | O | O | 13 |
| J005 | O | O | O | O | O | O | O | O | O | O | X | X | X | X | X | 10 |
| J009 | O | O | O | O | O | O | O | O | O | O | O | O | O | O | O | 15 |
| J021 | O | O | O | O | O | O | O | O | O | O | O | O | O | O | X | 14 |
| J025 | O | O | O | O | O | O | O | O | O | O | O | O | △ | O | O | 15 |
| J045 | O | O | O | O | O | O | O | O | O | O | O | O | O | O | O | 15 |
| J059 | O | X | O | X | X | X | X | X | X | X | X | X | X | X | X | 2 |
| J064 | O | O | X | X | X | X | X | X | X | X | X | X | O | X | X | 3 |
| J069 | O | O | O | O | O | O | O | O | O | O | O | O | O | X | O | 14 |
| J082 | O | X | X | X | X | X | X | X | X | X | X | X | X | X | X | 1 |
| J085 | △ | O | O | O | O | O | O | O | O | O | O | O | O | O | O | 15 |
| J089 | O | O | O | O | O | O | O | O | O | O | O | O | O | O | O | 15 |
| J095 | O | O | O | O | O | O | O | O | X | O | O | O | △ | X | O | 13 |
| J097 | X | O | O | O | O | O | O | O | O | X | △ | △ | X | △ | X | 11 |
| J098 | △ | △ | △ | O | O | △ | △ | △ | △ | △ | O | △ | X | △ | X | 13 |
