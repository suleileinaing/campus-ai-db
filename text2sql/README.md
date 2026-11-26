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
python -m text2sql.cli --debug "..."          # 자연어 답변과 함께 SQL·결과 표도 출력

# 평가 (크레딧 절약: --limit 3 으로 먼저 확인)
python -m text2sql.evaluate --gold text2sql/gold/gold_questions.json --run-name fewshot
python -m text2sql.evaluate --gold text2sql/gold/gold_questions.json --no-fewshot --run-name zeroshot

# 모델 바꿔 가며 비교 (.env 를 고치지 않고 --model 로 지정, --run-name 을 비우면 모델 이름으로 폴더 생성)
python -m text2sql.evaluate --gold text2sql/gold/gold_questions.json --model <모델명> --limit 3
```

PowerShell 에서 여러 모델을 차례로 돌리기:

```powershell
foreach ($m in "모델A", "모델B") { python -m text2sql.evaluate --gold text2sql/gold/gold_questions.json --no-fewshot --model $m --llm-judge --judge-model 모델C }
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

### LLM-as-a-judge (의미 기준 채점)

실행 비교는 글자 단위라서 의미는 맞지만 형식이 다른 답('03' 과 3, 컬럼 구성 등)을 오답으로 처리한다.
`llm_judge.py` 는 이미 돌린 결과(`results.jsonl`)의 문항마다 [질문 + 정답 표 + 예측 SQL 실행 결과 표] 를
ChatKHU 에 보내 `{"verdict": 1|0, "reason": "..."}` 로 판정받는다.

```bash
python -m text2sql.llm_judge --run exec100_zeroshot      # 기존 결과를 채점(SQL 생성은 다시 안 함)
python -m text2sql.evaluate --gold ... --llm-judge       # 평가 직후 바로 채점
```

- 결과: `judge_summary.md`(두 기준 정답률, 일치표, 유형별, 기준이 갈린 문항), `judge_compare.csv`(문항별 나란히 비교), `judge.jsonl`(judge 원문 포함)
- judge 모델은 `.env` 의 `CHATKHU_JUDGE_MODEL`(비우면 `CHATKHU_MODEL`), temperature 0. `--judge-model` 로 덮어쓸 수 있다. 생성 모델과 같은 모델이면 자기 답에 후한 경향이 있을 수 있다.
- SQL 실행 실패 문항은 judge 를 부르지 않고 0. 중간에 끊기면 다시 실행할 때 판정 안 된 문항만 채점한다(`--force` 로 전부 다시).

### SQL 논리 채점 (`sql_judge.py`)

결과 표만 비교하면 테스트 DB 에서 우연히 결과가 같은 틀린 SQL(조건 누락 등)을 정답으로 처리한다.
`sql_judge` 는 [질문 + 관련 테이블 스키마 + 정답 SQL + 모델 SQL + 로그인 학번] 을 보내
`logic`(논리 일치), `extra_condition`(질문에 없는 조건), `scope_ok`(본인 학번 범위) 를 판정받는다.
정답 SQL 은 `gold_sql`, 없으면 `reference_sql` 을 쓴다(예전 결과는 `config.json` 의 gold 파일에서 채움).

```bash
python -m text2sql.sql_judge --run exec15_zeroshot_gemini-4-argon   # 기존 결과를 채점(SQL 생성은 다시 안 함)
```

- 결과: `sql_judge_summary.md`(통과율, 우연히 맞은 문항, 범위 위반, 질문에 없는 조건), `sql_judge.csv`, `sql_judge.jsonl`

### 자연어 답변 채점 (`answer_judge.py`)

챗봇이 사용자에게 보여 준 최종 답변을 정확성·충실성·완결성·자연스러움 1~5점으로 매긴다.
SQL·테이블/컬럼 이름·채우지 못한 `{틀}` 노출은 LLM 없이 로컬 규칙으로 검사한다.
통과 = 정확성·충실성·완결성 모두 4점 이상 + 노출 없음. 답변이 필요하므로 `--answers` 로 다시 생성해야 한다.

```bash
python -m text2sql.evaluate --gold text2sql/gold/실행평가_15문항.json --no-fewshot --model gemini-4-argon \
    --judge-model claude-sonnet-5-5 --answers --answer-judge --sql-judge --run-name answers15_argon
python -m text2sql.answer_judge --run answers15_argon                # 이미 생성한 결과만 다시 채점
```

- 결과: `answer_judge_summary.md`(통과율, 항목별 평균, SQL 은 맞았는데 답변이 탈락한 문항, 노출), `answer_judge.csv`, `answer_judge.jsonl`
- `--answers` 는 서비스(`cli`)와 같은 프롬프트(답변 틀 규칙 포함)로 생성하므로 SQL 정답률이 기존 결과와 조금 다를 수 있다.

## 개인정보 처리

- LLM 에는 스키마, 코드성 컬럼의 값 형식, 질문, 로그인 학생 ID, SQL 오류 메시지만 보낸다. **조회 결과 행은 보내지 않는다.**
  - 자연어 답변(`cli`)도 같은 원칙을 따른다. LLM 은 SQL 과 함께 값 자리만 비운 답변 틀(`ANSWER: 담당 교수님은 {professor_name} 교수님이에요.`)을 내고, 값은 `answer.py` 가 로컬에서 채운다.
  - 대화형 모드는 앞 턴의 질문과 모델 응답(SQL·답변 틀)만 다음 턴에 넘긴다.
  - 예외: 평가용 `llm_judge`·`answer_judge` 는 채점을 위해 정답·예측 결과 행을 보낸다. 실제 학생 데이터가 든 DB 로는 돌리지 말고 가상 학생(fixture) 질의셋에만 쓴다.
- `students`, `enrollments` 를 읽는 쿼리는 로그인 학생 ID 가 있어야 하고, 다른 학생 ID 가 들어 있으면 거부한다. 이는 1차 방어선일 뿐이며 실제 서비스에선 백엔드 인가(README 다음 단계 7)가 필요하다.

## 팀과 정할 것

- "이번 학기" 기준은 `.env` 의 `TEXT2SQL_CURRENT_TERM`(기본 2026-2)으로 바꾼다.
- 스키마와 규칙은 연결한 DB 에 맞춰 자동으로 바뀐다(`academic_calendar`, `is_retake` 등은 있을 때만 프롬프트에 들어감).
- gold 질의가 나오면 오답 유형을 보고 `build_domain_rules` 를 보강한다. 이때 규칙을 특정 gold 문항 정답에 맞춰 쓰면 평가가 부풀려지므로, 일반 규칙으로만 추가한다.

## 웹 데모 (`web/`)

```bash
python -m text2sql.web.server            # http://127.0.0.1:8000  (--port, --no-rag, --session-min)
```

- 표준 라이브러리 `http.server` 만 사용합니다(추가 설치 없음). 화면은 `web/static/` 의 HTML/CSS/JS.
- 조회 결과 행은 브라우저로만 보내고 LLM 에는 보내지 않습니다.
- **로그인은 데모용**: DB 에 비밀번호가 없어 학번만 맞으면 통과합니다. 실서비스는 학교 인증이 필요합니다.
- 세션 만료 시 서버가 401 `{expired: true}` 를 보내고 대화 기록을 지우며, 화면은 개인 답변을 지우고 재로그인을 안내합니다.
- '멈추기'는 브라우저 요청만 끊습니다. 이미 보낸 LLM 호출은 서버에서 끝까지 진행됩니다(크레딧 차감).

### RCP(학생 클라우드) VM 배포

```bash
# VM(Ubuntu 22.04) 안에서
sudo apt update && sudo apt install -y python3-venv git
git clone https://github.com/suleileinaing/campus-ai-db.git && cd campus-ai-db
python3 -m venv .venv && .venv/bin/pip install -r text2sql/requirements.txt
nano text2sql/.env                      # API 키 등 .env 내용을 붙여 넣기(깃에 올리지 않음)
# rag_index 는 깃에 없으므로 내 PC 에서 scp 로 복사: text2sql/rag_index/syllabus_2026-2.sqlite
sudo cp text2sql/web/deploy/campus-ai.service /etc/systemd/system/
sudo systemctl daemon-reload && sudo systemctl enable --now campus-ai
curl -s localhost/api/status            # {"rag": true, ...} 이면 성공
```

- 외부 주소는 RCP 콘솔의 **App routing** 에서 서브도메인을 등록해 연결합니다. App routing 은 VM 의 **80번 포트**로 연결되므로 서버도 80번에서 켭니다(현재 https://campus-ai.apps.khu-return.com).
- 하루 질문 한도: 전체 `WEB_DAILY_LIMIT`(기본 300), 접속 주소당 `WEB_IP_DAILY_LIMIT`(기본 40). 넘으면 429 와 안내 문구.
- 로그 보기: `journalctl -u campus-ai -f`
- 코드 갱신: `git pull && sudo systemctl restart campus-ai`
