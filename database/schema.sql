PRAGMA foreign_keys = ON;

CREATE TABLE departments (
    department_id INTEGER PRIMARY KEY,
    code TEXT NOT NULL UNIQUE,
    name TEXT,
    college TEXT,
    has_track INTEGER CHECK (has_track IN (0, 1) OR has_track IS NULL)
);

CREATE TABLE course_categories (
    category_id INTEGER PRIMARY KEY,
    category_code TEXT NOT NULL UNIQUE,
    category_name TEXT NOT NULL UNIQUE
);

CREATE TABLE professors (
    professor_id INTEGER PRIMARY KEY,
    department_id INTEGER REFERENCES departments(department_id),
    professor_code TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    email TEXT,
    office TEXT
);

CREATE TABLE students (
    student_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    department_id INTEGER NOT NULL REFERENCES departments(department_id),
    track TEXT NOT NULL,
    admission_year INTEGER NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('재학', '휴학', '졸업', '제적')),
    extra_track_type TEXT,
    extra_track_name TEXT
);

CREATE TABLE courses (
    course_code TEXT PRIMARY KEY,
    department_id INTEGER NOT NULL REFERENCES departments(department_id),
    current_name TEXT NOT NULL,
    credits INTEGER NOT NULL CHECK (credits >= 0)
);

CREATE TABLE course_offerings (
    offering_id INTEGER PRIMARY KEY,
    course_code TEXT NOT NULL REFERENCES courses(course_code),
    course_name TEXT NOT NULL,
    target_year INTEGER,
    year INTEGER NOT NULL,
    semester TEXT NOT NULL,
    section TEXT NOT NULL,
    campus TEXT,
    capacity INTEGER CHECK (capacity >= 0 OR capacity IS NULL),
    industry_required INTEGER NOT NULL CHECK (industry_required IN (0, 1)),
    english_type TEXT NOT NULL CHECK (english_type IN ('NONE', 'PARTIAL', 'FULL')),
    delivery_mode TEXT NOT NULL
        CHECK (delivery_mode IN ('OFFLINE', 'ONLINE', 'HYBRID', 'TBD')),
    schedule_status TEXT NOT NULL
        CHECK (schedule_status IN ('SCHEDULED', 'ASYNCHRONOUS', 'INTENSIVE', 'ROOM_ONLY', 'TBD')),
    schedule_note TEXT,
    UNIQUE (offering_id, course_code)
);

CREATE TABLE offering_professors (
    offering_id INTEGER NOT NULL REFERENCES course_offerings(offering_id),
    professor_id INTEGER NOT NULL REFERENCES professors(professor_id),
    PRIMARY KEY (offering_id, professor_id)
);

CREATE TABLE course_offering_categories (
    offering_category_id INTEGER PRIMARY KEY,
    offering_id INTEGER NOT NULL REFERENCES course_offerings(offering_id),
    department_id INTEGER REFERENCES departments(department_id),
    category_id INTEGER NOT NULL REFERENCES course_categories(category_id),
    display_name TEXT NOT NULL
);

CREATE UNIQUE INDEX uq_offering_category_department
    ON course_offering_categories(offering_id, department_id)
    WHERE department_id IS NOT NULL;
CREATE UNIQUE INDEX uq_offering_category_common
    ON course_offering_categories(offering_id)
    WHERE department_id IS NULL;

CREATE TABLE time_slots (
    time_slot_id INTEGER PRIMARY KEY,
    day TEXT NOT NULL,
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    UNIQUE (day, start_time, end_time)
);

CREATE TABLE class_times (
    class_time_id INTEGER PRIMARY KEY,
    offering_id INTEGER NOT NULL REFERENCES course_offerings(offering_id),
    time_slot_id INTEGER NOT NULL REFERENCES time_slots(time_slot_id),
    room_code TEXT,
    UNIQUE (offering_id, time_slot_id, room_code)
);

CREATE TABLE enrollments (
    enrollment_id INTEGER PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES students(student_id),
    offering_id INTEGER NOT NULL,
    course_code TEXT NOT NULL,
    category_id INTEGER NOT NULL REFERENCES course_categories(category_id),
    grade TEXT,
    status TEXT NOT NULL CHECK (status IN ('완료', '미이수', '재수강전')),
    is_retake INTEGER NOT NULL CHECK (is_retake IN (0, 1)),
    retaken INTEGER NOT NULL CHECK (retaken IN (0, 1)),
    FOREIGN KEY (offering_id, course_code)
        REFERENCES course_offerings(offering_id, course_code),
    UNIQUE (student_id, offering_id)
);

CREATE TABLE syllabi (
    syllabus_id INTEGER PRIMARY KEY,
    offering_id INTEGER NOT NULL UNIQUE REFERENCES course_offerings(offering_id),
    source_url TEXT NOT NULL,
    professor_office TEXT,
    personal_homepage TEXT,
    course_homepage TEXT,
    consultation_time TEXT,
    overview TEXT,
    objectives TEXT,
    operation_modes TEXT,
    operation_note TEXT,
    class_types_json TEXT NOT NULL
        CHECK (json_valid(class_types_json) AND json_type(class_types_json) = 'array'),
    class_type_note TEXT,
    teaching_methods_json TEXT NOT NULL
        CHECK (json_valid(teaching_methods_json) AND json_type(teaching_methods_json) = 'array'),
    teaching_method_note TEXT,
    additional_materials TEXT,
    other_weekly_content TEXT,
    assignments TEXT,
    course_notices TEXT,
    midterm_percentage REAL CHECK (midterm_percentage BETWEEN 0 AND 100),
    midterm_detail TEXT,
    final_exam_percentage REAL CHECK (final_exam_percentage BETWEEN 0 AND 100),
    final_exam_detail TEXT,
    assignment_percentage REAL CHECK (assignment_percentage BETWEEN 0 AND 100),
    assignment_detail TEXT,
    presentation_percentage REAL CHECK (presentation_percentage BETWEEN 0 AND 100),
    presentation_detail TEXT,
    attendance_percentage REAL CHECK (attendance_percentage BETWEEN 0 AND 100),
    attendance_detail TEXT,
    other_percentage REAL CHECK (other_percentage BETWEEN 0 AND 100),
    other_detail TEXT,
    extracted_at_utc TEXT NOT NULL
);

CREATE TABLE syllabus_chunks (
    chunk_id INTEGER PRIMARY KEY,
    syllabus_id INTEGER NOT NULL REFERENCES syllabi(syllabus_id),
    content TEXT NOT NULL,
    embedding TEXT,
    metadata TEXT CHECK (metadata IS NULL OR json_valid(metadata))
);

CREATE TABLE course_prerequisites (
    prerequisite_id INTEGER PRIMARY KEY,
    course_code TEXT NOT NULL REFERENCES courses(course_code),
    prerequisite_course_code TEXT,
    prerequisite_name TEXT NOT NULL,
    prerequisite_type TEXT NOT NULL
        CHECK (prerequisite_type IN ('REQUIRED', 'RECOMMENDED')),
    cohort_start INTEGER,
    cohort_end INTEGER,
    abeek_applicable INTEGER CHECK (abeek_applicable IN (0, 1) OR abeek_applicable IS NULL),
    prerequisite_group TEXT,
    minimum_grade_code TEXT,
    minimum_required_count INTEGER CHECK (minimum_required_count >= 0 OR minimum_required_count IS NULL),
    CHECK (cohort_end IS NULL OR cohort_start IS NULL OR cohort_start <= cohort_end)
);

CREATE TABLE prerequisite_sources (
    prerequisite_id INTEGER NOT NULL REFERENCES course_prerequisites(prerequisite_id),
    source_syllabus_id INTEGER NOT NULL REFERENCES syllabi(syllabus_id),
    PRIMARY KEY (prerequisite_id, source_syllabus_id)
);

CREATE TABLE syllabus_textbooks (
    textbook_id INTEGER PRIMARY KEY,
    syllabus_id INTEGER NOT NULL REFERENCES syllabi(syllabus_id),
    sequence INTEGER NOT NULL,
    title TEXT,
    author TEXT,
    publisher TEXT,
    publication_year TEXT,
    isbn TEXT,
    note TEXT,
    UNIQUE (syllabus_id, sequence)
);

CREATE TABLE syllabus_weekly_plans (
    weekly_plan_id INTEGER PRIMARY KEY,
    syllabus_id INTEGER NOT NULL REFERENCES syllabi(syllabus_id),
    week INTEGER NOT NULL CHECK (week BETWEEN 1 AND 16),
    date_range TEXT,
    topic_content TEXT,
    note TEXT,
    UNIQUE (syllabus_id, week)
);

CREATE TABLE graduation_requirements (
    requirement_id INTEGER PRIMARY KEY,
    department_id INTEGER NOT NULL REFERENCES departments(department_id),
    track TEXT NOT NULL,
    cohort_start INTEGER NOT NULL,
    cohort_end INTEGER,
    total_credits INTEGER NOT NULL CHECK (total_credits >= 0),
    CHECK (cohort_end IS NULL OR cohort_start <= cohort_end)
);

CREATE TABLE requirement_categories (
    requirement_category_id INTEGER PRIMARY KEY,
    requirement_id INTEGER NOT NULL REFERENCES graduation_requirements(requirement_id),
    category_id INTEGER NOT NULL REFERENCES course_categories(category_id),
    min_credits INTEGER NOT NULL CHECK (min_credits >= 0),
    min_areas INTEGER CHECK (min_areas >= 0 OR min_areas IS NULL),
    per_area_min_credits INTEGER
        CHECK (per_area_min_credits >= 0 OR per_area_min_credits IS NULL),
    UNIQUE (requirement_id, category_id)
);

CREATE TABLE requirement_courses (
    requirement_course_id INTEGER PRIMARY KEY,
    requirement_id INTEGER NOT NULL REFERENCES graduation_requirements(requirement_id),
    course_code TEXT NOT NULL REFERENCES courses(course_code),
    category_id INTEGER NOT NULL REFERENCES course_categories(category_id),
    UNIQUE (requirement_id, course_code, category_id)
);

CREATE TABLE requirement_others (
    requirement_other_id INTEGER PRIMARY KEY,
    requirement_id INTEGER NOT NULL REFERENCES graduation_requirements(requirement_id),
    type TEXT NOT NULL,
    condition TEXT NOT NULL
);

CREATE TABLE requirement_fulfillment_options (
    fulfillment_option_id INTEGER PRIMARY KEY,
    target_type TEXT NOT NULL CHECK (target_type IN ('COURSE', 'OTHER')),
    target_course_code TEXT REFERENCES courses(course_code),
    target_other_id INTEGER REFERENCES requirement_others(requirement_other_id),
    method TEXT NOT NULL,
    detail_json TEXT NOT NULL CHECK (json_valid(detail_json)),
    CHECK (
        (target_type = 'COURSE' AND target_course_code IS NOT NULL AND target_other_id IS NULL)
        OR
        (target_type = 'OTHER' AND target_course_code IS NULL AND target_other_id IS NOT NULL)
    )
);

CREATE INDEX idx_professors_department ON professors(department_id);
CREATE INDEX idx_students_department_cohort ON students(department_id, admission_year);
CREATE INDEX idx_courses_department ON courses(department_id);
CREATE INDEX idx_offerings_course_year_term
    ON course_offerings(course_code, year, semester);
CREATE INDEX idx_offering_professors_professor ON offering_professors(professor_id);
CREATE INDEX idx_offering_categories_department_category
    ON course_offering_categories(department_id, category_id);
CREATE INDEX idx_class_times_offering ON class_times(offering_id);
CREATE INDEX idx_enrollments_student_status ON enrollments(student_id, status);
CREATE INDEX idx_enrollments_course ON enrollments(course_code);
CREATE INDEX idx_prerequisites_target_cohort
    ON course_prerequisites(course_code, cohort_start, cohort_end);
CREATE INDEX idx_prerequisite_sources_syllabus ON prerequisite_sources(source_syllabus_id);
CREATE INDEX idx_textbooks_syllabus ON syllabus_textbooks(syllabus_id);
CREATE INDEX idx_weekly_plans_syllabus_week ON syllabus_weekly_plans(syllabus_id, week);
CREATE INDEX idx_syllabus_chunks_syllabus ON syllabus_chunks(syllabus_id);
CREATE INDEX idx_requirements_department_cohort
    ON graduation_requirements(department_id, cohort_start, cohort_end);
CREATE INDEX idx_requirement_categories_requirement
    ON requirement_categories(requirement_id, category_id);
CREATE INDEX idx_requirement_courses_requirement
    ON requirement_courses(requirement_id, course_code);
CREATE INDEX idx_requirement_others_requirement
    ON requirement_others(requirement_id, type);
