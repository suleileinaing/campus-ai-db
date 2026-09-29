Code number:

A07308 : 2020-1, College of Software Department of Computer Science and Engineering - Computer Science and Engineering

### 졸업요건 원본과 데이터 출처 구분

졸업요건에 사용한 교육과정 PDF 원본은 `raw_data/graduation_requirements/`에 보관한다. 파일명은 적용 연도와 학과 범위를 확인할 수 있도록 정리하였다.

- `2022_software_convergence_college_curriculum.pdf`: 2022년 컴퓨터공학과, 인공지능학과, 소프트웨어융합학과
- `2023_computer_science_curriculum.pdf`: 2023년 컴퓨터공학과
- `2023_artificial_intelligence_curriculum.pdf`: 2023년 인공지능학과
- `2023_software_convergence_curriculum.pdf`: 2023년 소프트웨어융합학과
- `2024_software_convergence_college_curriculum.pdf`: 2024년 세 학과 통합 자료
- `2024_computer_science_curriculum.pdf`: 2024년 컴퓨터공학과 별도 자료(통합 자료 교차 검증용)
- `2025_software_convergence_college_curriculum.pdf`: 2025년 세 학과 통합 자료
- `2026_software_convergence_college_curriculum.pdf`: 2026년 세 학과 통합 자료

PDF에서 직접 확인한 총 이수학점, 이수구분별 최소학점, 지정과목 및 기타 졸업조건은 `processed_data/database_tables/`의 실제 공개 데이터로 관리한다. 학생·수강내역과 아직 공식 근거로 확정하지 않은 대체 충족 방법은 `processed_data/simulated/`에 유지한다.

교양 이수구분(category 4 `필수교과`, 5 `배분이수`, 6 `자유이수`)의 최소학점은 현재 팀원이 작성한 시뮬레이션 데이터를 사용한다. 공식 전공 졸업요건과 출처가 섞이지 않도록 `processed_data/simulated/simulated_general_requirement_categories.csv`에 분리했으며, 모든 졸업요건 세트에 `필수교과 17학점`, `배분이수 9학점(3개 영역·영역당 3학점)`, `자유이수 3학점`을 임시 적용한다. 후마니타스 공식 교육과정 자료를 확인한 뒤 실제 학번별 기준으로 교체해야 한다.

현재 통합 DB에는 2022~2026학번의 컴퓨터공학과(CS), 인공지능학과(AI), 소프트웨어융합학과(SWCON) 공식 졸업요건 15세트가 들어 있다. 각 세트의 총 이수학점, 전공기초·전공필수·전공선택 최소학점 및 PDF에 명시된 기타 조건을 저장하며, `scripts/build_official_graduation_requirements.py`로 다시 생성할 수 있다. 지정과목은 PDF에서 과목 단위로 정규화가 완료된 학과·연도만 저장하며, 행이 없다는 사실을 "필수과목 없음"으로 해석하면 안 된다. 세부 정규화 범위는 `validation_report/graduation_requirement_coverage.csv`에서 확인한다.

현재는 출처와 적용 연도를 명확히 검증하기 위해 졸업요건을 학과·학번별 한 행씩 유지한다. 향후 모든 연도의 `requirement_courses` 지정과목 정규화가 완료되면 총학점, 이수구분별 최소학점, 지정과목 및 기타 조건이 모두 같은 연속 학번 구간을 확인하여 `cohort_start`와 `cohort_end` 범위 한 행으로 통합할 수 있다. 총학점만 같다는 이유로 서로 다른 교육과정을 합치지 않는다.

- PDF에 명시된 `산학필수`, `전공영어강좌`, `SW교육`, `졸업논문`, `TOPIK`, 추가 전공 이수 조건은 실제 `requirement_others` 데이터로 취급한다.
- 프로젝트가 가정한 대체과목, 외부성적 또는 임의의 충족 방법만 `requirement_fulfillment_options` 시뮬레이션 데이터로 취급한다.
- 시뮬레이션 충족 방법을 사용할 때는 대응하는 실제 `graduation_requirements.requirement_id` 또는 `requirement_others.requirement_other_id`와 일치시켜야 한다.
- 폴더 위치는 데이터의 출처를 구분하기 위한 것이며, SQLite로 적재한 후에는 PK/FK 관계로 무결성을 검증한다.


### 동일한 강의계획서 내용을 공유하는 여러 분반은 향후 콘텐츠 해시 기반 중복 제거를 통해 공통 syllabus content로 분리할 수 있다.  

### 평가항목은 강의계획서마다 고정된 6개 유형으로 구성되어 있어, 질의 단순화와 성적 계산 편의를 위해 syllabi 테이블의 개별 수치 및 설명 컬럼으로 비정규화하였다.  

### 강의계획서 정제 규칙

- 영어강좌 여부의 최종값은 `course_offerings.english_type`의 `NONE`, `PARTIAL`, `FULL`을 사용한다. 강의계획서 HTML 값은 최종 테이블에 중복 저장하지 않고 `validation_report/english_type_validation.csv`에서 비교·검증한다.
- 홈페이지는 `personal_homepage`와 `course_homepage`로 분리한다.
- 상담시간은 표현 방식이 다양하므로 `consultation_time` 원문을 유지한다.
- 수업유형과 수업방법은 각각 `class_types_json`, `teaching_methods_json` JSON 배열로 저장한다.

### 시뮬레이션 학생 데이터와 실제 강좌 연결

학생과 수강이력 자체는 개인화 질의 테스트를 위한 시뮬레이션 데이터이다. 전공과 교양 수강이력의 `offering_id`와 `course_code`는 모두 2020~2026년 수강신청 사이트에서 수집한 실제 개설강좌를 참조한다. 기존 simulated 교양 수강이력은 동일 연도·학기·이수구분 안에서 고정 seed(`20260929`)로 실제 강좌에 배정했으며, 결과는 `processed_data/simulated/enrollment_replacement_map.csv`에 기록하였다.

사용되지 않는 simulated course, offering, class time, professor 연결 데이터는 제거하였다. 대학영어의 legacy code `HC1201`도 실제 공개 과목코드 `GEC1403`으로 교체하였다.

현재 `syllabi` 및 관련 강의계획서 테이블에는 소프트웨어융합대학 전공 개설강좌의 강의계획서가 중심으로 저장되어 있으며, 시뮬레이션 교양 과목의 강의계획서는 아직 포함하지 않았다. 향후 후마니타스칼리지의 실제 교양 과목·개설강좌를 수집한 뒤 해당 `offering_id`를 기준으로 교양 강의계획서 링크, 상세정보, 교재, 주차별 계획 등을 추가할 예정이다. 따라서 현재 DB에서 교양 과목의 syllabus가 조회되지 않는 것을 "강의계획서 없음"으로 해석하면 안 된다.

### 현재 역할 범위

이 저장소에서 담당한 범위는 2020~2026년 소프트웨어융합대학 공개 강좌·강의계획서 조사 및 DB화, 공식 졸업요건 통합, 개인화 질의 예시 작성이다. `[질문 / 대상 학생 ID / 정답 SQL / 정답 값]` 형식의 gold question dataset 구축과 ChatKHU API 기반 Text2SQL 구현·평가는 다른 팀원의 담당 범위이므로 여기서는 구현하지 않는다.

### Text2SQL과 syllabus chunks 사용 범위

현재 `syllabus_chunks` 테이블은 향후 RAG 기능을 위해 스키마만 준비되어 있으며 데이터는 아직 없다. 이것은 gold question dataset 작성과 Text2SQL 구현을 시작하는 데 문제가 되지 않는다. 학점, 수업시간, 선수과목, 교재, 평가비율, 주차별 계획, 졸업요건처럼 이미 정형 테이블에 저장된 정보는 자연어 질문을 SQL로 변환하여 조회한다.

- **Text2SQL:** 정형 데이터로 답할 수 있는 질문에 사용한다. 예: 남은 졸업학점, 산학필수 과목, 선수과목, 특정 시간대 강좌, 교재 및 평가비율 조회.
- **RAG (`syllabus_chunks`):** 긴 강의계획서 원문에서 의미 기반 검색이나 설명·추천이 필요한 질문에 사용한다. 예: 프로젝트 중심 수업 추천, 노트북 필요 여부, 과제 내용 요약, 관심 분야와 관련된 수업 추천.
- **개인화 답변:** 필요하면 학생·수강이력의 SQL 결과와 syllabus RAG 검색 결과를 결합한다.

따라서 2단계 gold question dataset과 3단계 Text2SQL은 우선 정형 질의로 진행할 수 있다. Gold dataset에 의미 검색이 필요한 서술형 질문을 포함하거나 통합 AI가 해당 질문까지 답해야 할 때 syllabus 원문을 chunking하고 embedding을 생성한다.

### Validation report

`validation_report/`는 데이터베이스 테이블이 아니라 수집·변환 결과를 확인하기 위한 검증 자료이다.

- `english_type_validation.csv`: 수강신청 사이트와 강의계획서의 영어강좌 구분이 일치하는지 비교한다. 총 1,837건 중 1,832건이 일치하고, 5건은 사이트에서 `PARTIAL`이지만 강의계획서 값이 비어 있어 `CONFLICT`로 표시했다. 최종 DB는 수강신청 사이트 값을 사용한다.
- `graduation_requirement_coverage.csv`: 학과·학번별 졸업요건과 지정과목의 정규화 완료 여부를 표시한다. `not_yet_normalized`는 필수과목이 없다는 뜻이 아니라 아직 과목 단위 변환이 끝나지 않았다는 뜻이다.

### 배분이수 영역과 학과 코드 사용 원칙

경희대학교 수강신청 사이트의 공개 조직 메타데이터에서는 후마니타스 배분이수 영역을 학과/전공 코드와 동일한 구조로 제공한다. 예를 들어 `생명,우주,인간`, `분석,추론,논리`, `상징,문화,소통`, `사회,공동체,평화`, `지능,정보,미래`는 각각 별도의 조직 코드와 `departments.department_id`를 가진다. 따라서 이 프로젝트에서는 별도의 `areas` 및 `course_areas` 테이블을 만들지 않고, 배분이수 과목의 `courses.department_id`를 해당 배분이수 영역 식별자로 함께 사용한다.

졸업요건의 배분이수 충족 여부는 다음 조건을 모두 확인한다.

- `course_offering_categories.category_id`가 배분이수 category를 가리키는 이수 과목만 대상으로 한다.
- 이수한 배분이수 과목의 총 학점이 `requirement_categories.min_credits` 이상이어야 한다.
- 학점이 `per_area_min_credits` 이상인 서로 다른 `courses.department_id`의 수가 `min_areas` 이상이어야 한다.

현재 시뮬레이션 졸업요건의 `min_credits = 9`, `min_areas = 3`, `per_area_min_credits = 3`은 서로 다른 배분이수 영역 세 곳에서 각 3학점 이상, 총 9학점 이상을 이수해야 한다는 의미이다. 이 방식은 배분이수 과목 하나가 수강신청 사이트에서 하나의 후마니타스 영역/학과 코드에 속한다는 현재 데이터 조건을 전제로 한다.

### 학생 개인정보 접근 제어 원칙

강좌, 강의계획서, 교육과정 등 공개 학사 데이터와 달리 `students` 및 `enrollments`는 비공개 개인정보로 취급한다. 실제 서비스에서는 로그인한 학생이 자신의 정보만 조회할 수 있도록 백엔드에서 인증 및 권한 검사를 수행해야 한다. SQLite 데이터베이스 자체만으로는 사용자별 행 단위 접근 제어가 제공되지 않으므로, 데이터베이스 파일을 클라이언트나 ChatGPT API에 직접 노출하지 않는다.

- 로그인 후 검증된 세션 또는 토큰에서 `student_id`를 가져온다.
- 요청 URL이나 사용자 입력으로 전달된 `student_id`를 조회 권한의 근거로 사용하지 않는다.
- `/students/{student_id}/enrollments`보다 `/me/enrollments`, `/me/profile`, `/me/graduation-progress` 형태의 API를 사용한다.
- 모든 학생 개인화 SQL에는 백엔드가 확인한 `student_id` 조건을 적용한다.
- ChatGPT API에는 질문에 필요한 최소한의 조회 결과만 전달하고 학생 테이블 전체를 보내지 않는다.
- 학생용 권한과 관리자용 권한을 분리하고, 비밀번호 원문은 저장하지 않으며 안전한 password hash만 저장한다.
- 현재 `processed_data/simulated/students.csv`와 `processed_data/simulated/enrollments.csv`는 기능 검증을 위한 시뮬레이션 데이터이며 실제 학생 개인정보가 아니다.

예를 들어 로그인한 학생의 수강내역은 다음과 같이 백엔드에서 매개변수화된 SQL로 조회한다. 여기서 `?` 값은 사용자가 직접 입력한 학번이 아니라 인증된 세션에서 얻은 `student_id`이다.

```sql
SELECT
    e.course_code,
    c.current_name,
    e.grade,
    e.status
FROM enrollments AS e
JOIN courses AS c ON c.course_code = e.course_code
WHERE e.student_id = ?;
```
