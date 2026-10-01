# Text2SQL (ChatKHU API)

자연어 질문을 ChatKHU API Gateway(OpenAI 호환)로 SQL 로 바꾸고, `database/campus_ai.db` 에서 읽기 전용으로 실행한 뒤 gold 질의셋과 실행 결과를 비교한다.

## 설치와 설정

```bash
pip install -r text2sql/requirements.txt
cp text2sql/.env.example text2sql/.env      # CHATKHU_API_KEY 입력 (.env 는 커밋되지 않음)
python -m text2sql.cli --list-models         # 쓸 수 있는 모델 이름 확인 → .env 의 CHATKHU_MODEL 에 입력
```

모든 명령은 **프로젝트 루트**(campus-ai-db/)에서 실행한다.

## 사용법

```bash
# API 없이 점검 (20개 테스트 + 정답 SQL 로 평가 코드 확인)
python -m unittest text2sql.tests.test_offline -v
python -m text2sql.evaluate --gold text2sql/gold/example_gold_from_samples.json --oracle

# 시스템 프롬프트 확인
python -m text2sql.cli --show-prompt

# 질문 하나 / 대화형
python -m text2sql.cli "2026년 2학기 월요일 13:30에 시작하는 수업"
python -m text2sql.cli --student-id 202210001 "내가 이수한 학점은?"
python -m text2sql.cli --student-id 202210001

# 평가 (크레딧 절약: --limit 3 으로 먼저 확인)
python -m text2sql.evaluate --gold text2sql/gold/gold_questions.json --run-name fewshot
python -m text2sql.evaluate --gold text2sql/gold/gold_questions.json --no-fewshot --run-name zeroshot
```

## 개인화 질의셋으로 평가 (공식: v2, 16문항)

`gold/personal_gold_v2.csv` 는 GitHub 최신 `database/campus_ai.db`(commit b8af8fc 이후, SHA-256 38fe5584…) 기준이다.
`git pull` 로 DB 를 최신으로 받은 뒤, `.env` 의 `TEXT2SQL_DB_PATH` 는 비워 둔다.

```bash
python -m text2sql.evaluate --gold text2sql/gold/personal_gold_v2.csv --oracle --run-name oracle   # 16/16 이어야 정상
python -m text2sql.evaluate --gold text2sql/gold/personal_gold_v2.csv --limit 3 --run-name smoke
python -m text2sql.evaluate --gold text2sql/gold/personal_gold_v2.csv --run-name v2_fewshot
python -m text2sql.evaluate --gold text2sql/gold/personal_gold_v2.csv --no-fewshot --run-name v2_zeroshot
```

- 정답 값은 행 단위 JSON(`[{"컬럼": 값}]`)이고, 평가는 정답 SQL 을 다시 실행한 결과로 비교한다.
- strict 는 gold 의 ORDER BY 순서까지, relaxed 는 행 순서·컬럼 순서·추가 컬럼을 무시한다.
- `gold/personal_gold_v1.*` 는 이전 통합 DB(학사일정·도서관 포함) 기준 21문항으로, 기록용이다.
  쓰려면 `TEXT2SQL_DB_PATH=database/campus_ai_integrated.db` 가 필요하다.

## 구성

| 파일 | 역할 |
|---|---|
| `config.py` | `.env` 로딩, 경로, 기본값 |
| `chatkhu_client.py` | ChatKHU 호출. temperature 미지원 모델이면 자동으로 빼고 재시도 |
| `prompt.py` | 스키마 + DB 에서 자동 추출한 값 형식 + 도메인 규칙 + few-shot(`sample_queries.sql`) |
| `executor.py` | SQL 추출, 조회문 검사, 읽기 전용 실행, 개인정보 테이블 범위 검사, 시간·행 수 제한 |
| `pipeline.py` | 생성 → 실행 → 오류 메시지로 자기수정(기본 2회) |
| `compare.py` | 실행 결과 비교 (strict / relaxed) |
| `gold_loader.py` | gold 질의셋(JSON/CSV) 로딩 |
| `evaluate.py` | 일괄 평가, `results/<run_name>/` 에 결과 저장 |
| `cli.py` | 단일 질문, 모델 목록, 프롬프트 미리보기 |

## gold 질의셋 형식

`gold/TEMPLATE.csv` 또는 `gold/example_gold_from_samples.json` 참고.

| 필드 | 필수 | 설명 |
|---|---|---|
| `id` | | 없으면 q001… 자동 |
| `question` | O | 자연어 질문 |
| `student_id` | | 개인화 질문일 때 로그인 학생 ID |
| `gold_sql` | △ | 정답 SQL. 있으면 DB 에서 실행해 정답 행을 만든다(권장) |
| `gold_answer` | △ | gold_sql 이 없을 때 정답 값. 스칼라, `[a,b]`(한 열), `[[a,b],[c,d]]`(여러 열) |
| `ordered` | | 순서까지 비교할지. 비우면 gold_sql 바깥 ORDER BY 유무로 판단 |
| `tags` | | 유형별 집계용. CSV 에선 `개인화;집계` |

`example_gold_from_samples.json` 은 `sample_queries.sql` 11개에 질문을 붙인 **동작 점검용**이다. 평가에 쓰면 few-shot 예시와 겹치므로, evaluate 는 gold SQL 과 같은 예시를 few-shot 에서 자동 제외한다.

## 평가 지표

- **실행 성공률**: 최종 / 1차 시도(자기수정 효과 비교)
- **strict**: 결과 행이 완전히 같음. gold 에 ORDER BY 가 있으면 순서도 비교. 1 과 1.0 은 같게, 실수는 소수 4자리.
- **relaxed**: 예측 결과에서 gold 컬럼에 대응하는 컬럼만 뽑았을 때 같음(컬럼 추가·순서 차이 허용)
- 결과 파일: `summary.md`(보고서용 표와 오답 목록), `results.csv`, `results.jsonl`(시도별 원문 포함), `system_prompt.txt`, `config.json`

## 개인정보 처리

- LLM 에는 스키마, 코드성 컬럼의 값 형식, 질문, 로그인 학생 ID, SQL 오류 메시지만 보낸다. **조회 결과 행은 보내지 않는다.**
- `students`, `enrollments` 를 읽는 쿼리는 로그인 학생 ID 가 있어야 하고, 다른 학생 ID 가 들어 있으면 거부한다. 이는 1차 방어선일 뿐이며 실제 서비스에선 백엔드 인가(README 다음 단계 7)가 필요하다.

## 팀과 정할 것

- "이번 학기" 기준은 `.env` 의 `TEXT2SQL_CURRENT_TERM`(기본 2026-2)으로 바꾼다.
- 스키마와 규칙은 연결한 DB 에 맞춰 자동으로 바뀐다(`academic_calendar`, `is_retake` 등은 있을 때만 프롬프트에 들어감).
- gold 질의가 나오면 오답 유형을 보고 `build_domain_rules` 를 보강한다. 이때 규칙을 특정 gold 문항 정답에 맞춰 쓰면 평가가 부풀려지므로, 일반 규칙으로만 추가한다.
