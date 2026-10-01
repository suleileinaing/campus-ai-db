# CAMPUS AI 통합 데이터베이스

이 폴더는 팀원들이 동일한 스키마와 키를 사용하도록 공유하는 **단일 기준 데이터 패키지**이다. 자연어 질의를 SQL로 변환하는 Text2SQL 코드와 정답 질의셋은 이 폴더의 `database/campus_ai.db` 및 `database/schema.sql`을 기준으로 작성한다.

## 빠른 시작

프로젝트 루트에서 다음 명령을 실행한다.

```bash
python3 scripts/test_database_queries.py
```

CSV에서 SQLite DB를 다시 만들려면 다음을 실행한다.

```bash
python3 scripts/build_database.py
python3 scripts/test_database_queries.py
```

현재 검증 결과는 다음과 같다.

- SQLite integrity check: PASS
- Foreign-key check: PASS
- 수강내역과 실제 개설강좌의 과목코드 일치 검사: PASS
- 대표 SQL 질의: 11/11 PASS
- 졸업요건: CS/AI/SWCON 각 2022~2026학번, 총 15세트

## 폴더 구성

```text
CAMPUS AI Database/
├── database/
│   ├── campus_ai.db              # 팀에서 조회할 통합 SQLite DB
│   ├── schema.sql                # 테이블, 제약조건, 인덱스 정의
│   └── sample_queries.sql        # 대표 SQL 예시
├── processed_data/
│   ├── website_tables/           # 수강신청 사이트 기반 실제 공개 데이터
│   ├── database_tables/          # 강의계획서·졸업요건 정제 데이터
│   └── simulated/                # 학생/수강이력 및 임시 교양 데이터
├── raw_data/                     # 원본 공개 데이터와 근거 문서
├── scripts/                      # 수집·변환·DB 구축·검증 코드
├── validation_report/            # 추출 및 정합성 검증 결과
└── docs/school_qa_erd.mermaid    # 통합 ERD
```

## 테이블 설명

### 학과·교수·학생

| 테이블 | 설명 | 데이터 성격 |
|---|---|---|
| `departments` | 학과/전공 및 후마니타스 영역 코드 | 공개 데이터 |
| `professors` | 교수 코드, 이름, 소속, 연구실 | 공개 데이터 중심; 일부 simulated professor 포함 |
| `students` | 학번, 학과, 트랙, 입학연도, 상태 | 시뮬레이션·비공개 취급 |

### 과목·개설강좌

| 테이블 | 설명 | 주요 관계 |
|---|---|---|
| `courses` | 과목코드별 기준 과목명, 학점, 개설학과 | `course_code`가 PK |
| `course_offerings` | 연도·학기·분반별 실제 개설강좌 | 하나의 `course`에 여러 개설강좌 |
| `offering_professors` | 개설강좌와 담당 교수 연결; 팀티칭 지원 | 다대다 연결 테이블 |
| `course_categories` | 전공기초·전공필수·전공선택·교양 등의 코드 사전 | category 기준 테이블 |
| `course_offering_categories` | 학생 학과 기준으로 달라질 수 있는 개설강좌 이수구분 | 공통 분류는 `department_id=NULL` |
| `time_slots` | 요일·시작시간·종료시간의 중복 제거 사전 | 동일 시간대를 재사용 |
| `class_times` | 개설강좌의 시간대와 강의실 | 한 강좌에 여러 요일 가능 |

`course_offerings.credits`는 해당 학기 당시의 학점을 보존한다. `english_type`은 `NONE`, `PARTIAL`, `FULL`, `SECOND_FOREIGN_LANGUAGE` 중 하나이며, `industry_required`는 산학필수 여부를 `0/1`로 저장한다. 온라인·집중수업 등은 `delivery_mode`, `schedule_status`, `schedule_note`로 표현한다.

교강사 코드는 시기에 따라 서로 다른 이름에 사용된 사례가 있어 `professors`는 `professor_code` 하나가 아니라 `(professor_code, name)` 조합을 고유 기준으로 사용한다.

### 수강이력

| 테이블 | 설명 | 데이터 성격 |
|---|---|---|
| `enrollments` | 학생별 수강 과목, 성적, 완료 상태, 재수강 여부 | 시뮬레이션 |

수강이력은 가상 과목 ID가 아니라 가능한 경우 실제 수집한 `course_offerings.offering_id`에 연결했다. 현재 교양 수강이력 일부는 임시 simulated 교양 개설강좌를 참조한다.

### 강의계획서

| 테이블 | 설명 |
|---|---|
| `syllabi` | 강의계획서 URL, 수업개요·목표·방법·과제·평가비율 등 |
| `syllabus_textbooks` | 강의계획서별 교재; `sequence`는 교재 표시 순서 |
| `syllabus_weekly_plans` | 1~16주차별 날짜, 주제, 비고 |
| `syllabus_chunks` | 향후 RAG 검색용 텍스트 조각과 embedding; 현재 비어 있을 수 있음 |

내용을 공유하는 여러 분반은 현재 개설강좌별 syllabus row를 가지며, 향후 content hash로 공통 콘텐츠를 분리할 수 있다.

평가항목은 질의와 성적 계산을 단순화하기 위해 `syllabi`의 중간고사·기말고사·과제·발표·출석·기타 percentage/detail 컬럼으로 저장했다. 홈페이지는 `personal_homepage`와 `course_homepage`로 분리하고, 수업유형과 수업방법은 JSON 배열로 유지한다.

### 강의계획서 정제 규칙
- 영어강좌 여부의 최종값은 `course_offerings.english_type`의 `NONE`, `PARTIAL`, `FULL`을 사용한다. 강의계획서 HTML 값은 최종 테이블에 중복 저장하지 않고 `validation_report/english_type_validation.csv`에서 비교·검증한다.
- 홈페이지는 `personal_homepage`와 `course_homepage`로 분리한다.
- 상담시간은 표현 방식이 다양하므로 `consultation_time` 원문을 유지한다.
- 수업유형과 수업방법은 각각 `class_types_json`, `teaching_methods_json` JSON 배열로 저장한다.

### Text2SQL과 syllabus chunks 사용 범위

현재 `syllabus_chunks`는 향후 RAG 기능을 위해 스키마만 준비되어 있고 데이터는 아직 없다.

 Gold dataset에 의미 검색이 필요한 서술형 질문을 포함하거나 서비스가 해당 질문까지 답해야 하는 시점에 syllabus 원문을 chunking하고 embedding을 생성한다.

### 선수과목

| 테이블 | 설명 |
|---|---|
| `course_prerequisites` | 대상 과목의 선수/권장과목, 적용 학번 범위, 최소 성적, AND/OR 그룹 |
| `prerequisite_sources` | 선수과목 정보와 근거 강의계획서 연결 |

같은 선수과목 조건이 여러 강의계획서에 반복되어도 조건은 한 번만 저장하고, 여러 근거 syllabus를 `prerequisite_sources`로 연결한다. 따라서 학생에게 답변할 때 조건뿐 아니라 출처 URL도 제시할 수 있다.

### 졸업요건

| 테이블 | 설명 |
|---|---|
| `graduation_requirements` | 학과·트랙·입학연도별 총 졸업학점 |
| `requirement_categories` | 전공기초·전공필수·전공선택 등 이수구분별 최소학점 |
| `requirement_courses` | 해당 교육과정에서 지정된 필수 과목 |
| `requirement_others` | 산학필수, 영어강좌, SW교육, 졸업논문, 다전공 등의 조건 |
| `requirement_fulfillment_options` | 과목 대체·마이크로디그리 등 충족 방법; 현재 시뮬레이션 |

2022~2026년 컴퓨터공학과(CS), 인공지능학과(AI), 소프트웨어융합학과(SWCON)의 공식 PDF를 근거로 총 15개 졸업요건 세트를 저장했다. 총학점·이수구분별 최소학점·기타 조건은 공식 데이터이다. `requirement_courses`는 PDF에서 과목 단위 정규화가 완료된 학과·연도만 포함하므로, 행이 없다는 것을 "필수과목 없음"으로 해석하면 안 된다. 범위는 `validation_report/graduation_requirement_coverage.csv`에서 확인한다. [남음 과목들은 추후 추가될 예정이다]

교양 이수구분(category 4 `필수교과`, 5 `배분이수`, 6 `자유이수`)은 현재 시뮬레이션 데이터를 사용한다. `processed_data/simulated/simulated_general_requirement_categories.csv`에 분리하여 모든 졸업요건 세트에 `필수교과 17학점`, `배분이수 9학점(3개 영역·영역당 3학점)`, `자유이수 3학점`을 임시 적용했으며, 향후 후마니타스 공식 학번별 기준으로 교체한다.

현재는 출처와 적용 연도를 명확히 검증하기 위해 졸업요건을 학과·학번별 한 행씩 유지한다. 향후 모든 연도의 지정과목 정규화가 완료되면 총학점, 이수구분별 최소학점, 지정과목 및 기타 조건이 모두 같은 연속 학번 구간을 확인하여 `cohort_start`와 `cohort_end` 범위 한 행으로 통합할 수 있다. 총학점만 같은 경우에는 동일한 졸업요건으로 간주하지 않는다.

- PDF에 명시된 `산학필수`, `전공영어강좌`, `SW교육`, `졸업논문`, `TOPIK`, 추가 전공 이수 조건은 실제 `requirement_others` 데이터로 취급한다.
- 프로젝트가 가정한 대체과목, 외부성적 또는 임의의 충족 방법만 `requirement_fulfillment_options` 시뮬레이션 데이터로 취급한다.
- 시뮬레이션 충족 방법을 사용할 때는 대응하는 실제 `graduation_requirements.requirement_id` 또는 `requirement_others.requirement_other_id`와 일치시켜야 한다.
- 폴더 위치는 데이터의 출처를 구분하기 위한 것이며, SQLite로 적재한 후에는 PK/FK 관계로 무결성을 검증한다.


## 전체 테이블 구조

| 테이블 | 컬럼 |
|---|---|
| `departments` | `department_id`, `code`, `name`, `college`, `has_track `*(출처 확인 필요)* |
| `course_categories` | `category_id`, `category_code`, `category_name` |
| `professors` | `professor_id`, `department_id`, `professor_code`, `name`, `email`*(출처 확인 필요)*, `office` |
| `students` | `student_id`, `name`, `department_id`, `track`, `admission_year`, `status`, `extra_track_type`, `extra_track_name` |
| `courses` | `course_code`, `department_id`, `current_name`, `credits` |
| `course_offerings` | `offering_id`, `course_code`, `course_name`, `credits`, `target_year`, `year`, `semester`, `section`, `campus`, `capacity`, `industry_required`, `english_type`, `delivery_mode`, `schedule_status`, `schedule_note` |
| `offering_professors` | `offering_id`, `professor_id` |
| `course_offering_categories` | `offering_category_id`, `offering_id`, `department_id`*(학생의 전공)*, `category_id`, `display_name` |
| `time_slots` | `time_slot_id`, `day`, `start_time`, `end_time` |
| `class_times` | `class_time_id`, `offering_id`, `time_slot_id`, `room_code` |
| `enrollments` | `enrollment_id`, `student_id`, `offering_id`, `course_code`, `category_id`, `grade`, `status`, `is_retake`, `retaken` |
| `syllabi` | `syllabus_id`, `offering_id`, `source_url`, `professor_office`, `personal_homepage`, `course_homepage`, `consultation_time`, `overview`, `objectives`, `operation_modes`, `operation_note`, `class_types_json`, `class_type_note`, `teaching_methods_json`, `teaching_method_note`, `additional_materials`, `other_weekly_content`, `assignments`, `course_notices`, `midterm_percentage`, `midterm_detail`, `final_exam_percentage`, `final_exam_detail`, `assignment_percentage`, `assignment_detail`, `presentation_percentage`, `presentation_detail`, `attendance_percentage`, `attendance_detail`, `other_percentage`, `other_detail`, `extracted_at_utc` |
| `syllabus_chunks` | `chunk_id`, `syllabus_id`, `content`, `embedding`, `metadata` |
| `course_prerequisites` | `prerequisite_id`, `course_code`, `prerequisite_course_code`, `prerequisite_name`, `prerequisite_type`, `cohort_start`, `cohort_end`, `abeek_applicable`, `prerequisite_group`, `minimum_grade_code`, `minimum_required_count` |
| `prerequisite_sources` | `prerequisite_id`, `source_syllabus_id` |
| `syllabus_textbooks` | `textbook_id`, `syllabus_id`, `sequence`, `title`, `author`, `publisher`, `publication_year`, `isbn`, `note` |
| `syllabus_weekly_plans` | `weekly_plan_id`, `syllabus_id`, `week`, `date_range`, `topic_content`, `note` |
| `graduation_requirements` | `requirement_id`, `department_id`, `track`, `cohort_start`, `cohort_end`, `total_credits` |
| `requirement_categories` | `requirement_category_id`, `requirement_id`, `category_id`, `min_credits`, `min_areas`, `per_area_min_credits` |
| `requirement_courses` | `requirement_course_id`, `requirement_id`, `course_code`, `category_id` |
| `requirement_others` | `requirement_other_id`, `requirement_id`, `type`, `condition` |
| `requirement_fulfillment_options` | `fulfillment_option_id`, `target_type`, `target_course_code`, `target_other_id`, `method`, `detail_json` |

PK/FK, 자료형 및 제약조건은 `database/schema.sql`, 테이블 관계는 `docs/school_qa_erd.mermaid`에서 확인할 수 있다.

## 실제 데이터와 시뮬레이션 데이터

### 실제 공개 데이터

- 2020~2026년 소프트웨어융합대학, 후마니타스 교양 및 자연계열 강좌·개설정보
- 교수·수업시간·강의실·이수구분
- 10,718개 실제 개설강좌의 강의계획서 링크
- 이 중 1,837개 소프트웨어융합대학 강의계획서의 상세 추출 정보
- 강의계획서의 교재, 평가방법, 주차별 계획, 선수과목
- 2022~2026년 CS/AI/SWCON 공식 졸업요건

### 시뮬레이션 데이터

- `students`, `enrollments`
- 일부 교수 및 팀티칭 연결 보조 데이터
- 학생 수강이력 테스트용 임시 교양 과목과 교양 개설강좌
- 공식 근거가 아직 확정되지 않은 일부 대체 충족 방법

### 시뮬레이션 학생 데이터와 실제 강좌 연결

기존 simulated 교양 수강이력은 동일 연도·학기·이수구분 안에서 고정 seed(`20260929`)로 실제 강좌에 배정했으며, 결과는 `processed_data/simulated/enrollment_replacement_map.csv`에 기록하였다. 

실제 후마니타스 교양 개설강좌는 master table에 수집되어 있다. 다만 기존 시뮬레이션 학생의 수강이력은 임시 교양 과목코드와 개설강좌를 계속 참조하므로, 해당 simulated rows도 개인화 질의 테스트용으로 함께 유지한다. 전공 강좌는 시뮬레이션하지 않고 수강신청 사이트의 실제 개설강좌를 사용한다.

`processed_data/website_tables/syllabi.csv`에는 실제 강좌 10,718개의 강의계획서 링크가 있다. 현재 SQLite DB의 `syllabi` 및 관련 상세 테이블에는 먼저 추출한 소프트웨어융합대학 1,837개가 들어 있다. 후마니타스 교양 및 자연계열 강의계획서 상세정보는 추출 작업이 진행 중이다. 따라서 해당 강좌에서 syllabus 상세정보가 조회되지 않는 것은 강의계획서가 없다는 뜻이 아니라 **링크는 수집했지만 상세 추출이 아직 완료되지 않았다는 뜻**이다.

## 개인정보 및 조회 권한

`students`와 `enrollments`는 현재 가상 데이터이지만 실제 서비스에서는 개인정보로 취급한다.

- DB 파일을 브라우저나 ChatGPT API에 직접 노출하지 않는다.
- 실제 서비스에서는 백엔드의 로그인 세션을 통해 학생 본인 여부를 확인해야 한다.
## 데이터 수정 시 참고사항

- 테이블을 연결할 때는 기존 master CSV와 DB의 PK/FK를 기준으로 한다.
- CSV를 변경한 경우 `build_database.py`로 DB를 다시 생성한다.
- 실제 데이터와 simulated data의 출처를 구분하여 관리한다.
- 실제 학생 및 수강이력 데이터는 개인정보로 취급한다.

## Validation report

`validation_report/`는 DB에 적재되는 테이블이 아니라 수집·변환 결과를 확인하기 위한 검증 자료이다.

- `english_type_validation.csv`: 수강신청 사이트와 강의계획서의 영어강좌 구분을 비교한다. 1,837건 중 1,832건이 일치하며, 5건은 사이트가 `PARTIAL`이고 강의계획서 값이 비어 있어 `CONFLICT`로 표시했다. 최종 DB는 수강신청 사이트 값을 사용한다.
- `graduation_requirement_coverage.csv`: 학과·학번별 졸업요건과 지정과목의 정규화 완료 여부를 보여준다. `not_yet_normalized`는 필수과목이 없다는 의미가 아니다.

## 다음 단계

### 현재 완료된 범위

- 공개 강좌 및 강의계획서 수집·정제·DB화
- 공식 졸업요건 통합
- 공통 PK/FK 기반 단일 SQLite DB 구축
- 대표 SQL 및 integrity test 작성
- 개인화 질의 예시 작성

### 다음 단계

1. 실제 교양 개설강좌의 강의계획서와 교재·주차별 계획을 수집하여 연결한다.
2. 아직 과목 단위로 정규화되지 않은 졸업요건 지정과목을 PDF에서 추가 추출한다.
3. 전체 조건이 같은 연속 학번의 졸업요건을 `cohort_start`~`cohort_end` 범위로 통합한다.
4. `[질문 / 대상 학생 ID / 정답 SQL / 정답 값]` 형식으로 gold question dataset을 만든다.
5. ChatKHU API 기반 Text2SQL을 구현하고 gold SQL 결과와 비교한다.
6. 로그인 사용자 본인에게만 학생·수강이력 조회를 허용하는 backend authorization을 구현한다.
7. 강의계획서 chunk와 embedding을 생성하여 설명형 질문에 RAG를 결합한다.
8. 데이터 갱신일과 출처 URL을 관리하고 학기별 증분 수집을 자동화한다.

## 현재 DB 규모

| 항목 | 행 수 |
|---|---:|
| 강좌 개설 | 10,814 |
| 강의계획서 | 1,837 |
| 수업시간 | 18,587 |
| 선수과목 조건 | 416 |
| 주차별 계획 | 28,880 |
| 졸업요건 세트 | 15 |
| 시뮬레이션 학생 | 44 |
| 시뮬레이션 수강이력 | 1,188 |

행 수는 CSV를 다시 생성하거나 실제 교양 데이터를 추가하면 변경될 수 있다.