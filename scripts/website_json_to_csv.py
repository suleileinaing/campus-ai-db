#!/usr/bin/env python3
"""Convert KHU public course-list JSON files into ERD-aligned CSV tables."""

import csv
import json
import re
from pathlib import Path
from urllib.parse import urlencode


PROJECT_DIR = Path(__file__).resolve().parent.parent
INPUT_DIR = PROJECT_DIR / "raw_data" / "course_lists"
OUTPUT_DIR = PROJECT_DIR / "processed_data" / "website_tables"

FILE_PATTERN = re.compile(
    r"^(?P<year>\d{4})-(?P<semester>[^_]+)_(?P<major>[^_]+)_raw\.json$"
)
TIME_PATTERN = re.compile(
    r"^(?P<day>[월화수목금토일])\s+"
    r"(?P<start>\d{2}:\d{2})-(?P<end>\d{2}:\d{2})\s+"
    r"\((?P<room>.*)\)$"
)
TIME_WITHOUT_DAY_PATTERN = re.compile(
    r"^(?P<start>\d{2}:\d{2})-(?P<end>\d{2}:\d{2})\s+"
    r"\((?P<room>.*)\)$"
)
ROOM_WITHOUT_TIME_PATTERN = re.compile(r"^-\s*\((?P<room>[^()]+)\)$")
DAY_WITHOUT_TIME_PATTERN = re.compile(r"^[월화수목금토일]\s+-\s*\(\)$")

DAY_NAMES = {
    "월": "monday",
    "화": "tuesday",
    "수": "wednesday",
    "목": "thursday",
    "금": "friday",
    "토": "saturday",
    "일": "sunday",
}

ENGLISH_TYPE_NAMES = {
    "": "NONE",
    "영어(부분)": "PARTIAL",
    "영어": "FULL",
}

TERM_CODES = {
    "1": "10",
    "2": "20",
    "summer": "15",
    "winter": "25",
    "10": "10",
    "20": "20",
    "15": "15",
    "25": "25",
}

CATEGORY_NAMES = {
    "00": ("기타", "구분없음"),
    "04": ("전공", "전공필수"),
    "05": ("전공", "전공선택"),
    "06": ("교직", "교직"),
    "08": ("기타", "자유선택"),
    "10": ("기타", "공통과목"),
    "11": ("전공", "전공기초"),
    "12": ("전공", "전공공통"),
    "13": ("기타", "공통필수"),
    "20": ("교직", "교직전선"),
    "41": ("기타", "선수과목"),
    "43": ("기타", "논문지도과목"),
    "61": ("기타", "외국어대체"),
    "66": ("기타", "논문대체"),
    "95": ("기타", "과정구분없음"),
}

CATEGORY_DEFINITIONS = [
    {"category_id": 1, "category_code": "11", "category_name": "전공기초"},
    {"category_id": 2, "category_code": "04", "category_name": "전공필수"},
    {"category_id": 3, "category_code": "05", "category_name": "전공선택"},
    {"category_id": 4, "category_code": "16", "category_name": "필수교과"},
    {"category_id": 5, "category_code": "15", "category_name": "배분이수"},
    {"category_id": 6, "category_code": "17", "category_name": "자유이수"},
    {"category_id": 7, "category_code": "08", "category_name": "자유선택"},
    {"category_id": 8, "category_code": "24", "category_name": "미확인 코드 24"},
    {"category_id": 9, "category_code": "25", "category_name": "미확인 코드 25"},
]
CATEGORY_ID_BY_CODE = {
    row["category_code"]: row["category_id"] for row in CATEGORY_DEFINITIONS
}

DEPARTMENT_METADATA = {
    "A04675": ("영미어문", "외국어대학"),
    "A04764": ("기계공학과", "공과대학"),
    "A04840": ("산업경영공학과", "공과대학"),
    "A05129": ("전자공학과", "전자정보대학"),
    "A05280": ("산업디자인학과", "예술·디자인대학"),
    "A05289": ("디지털콘텐츠학과", "예술·디자인대학"),
    "A05420": ("전공기초(수학)", "자연계열"),
    "A07337": ("소프트웨어융합학과", "소프트웨어융합대학"),
    "A07346": ("소프트웨어융합학과", "소프트웨어융합대학"),
    "A10626": ("컴퓨터공학부", "소프트웨어융합대학"),
    "A10627": ("컴퓨터공학과", "소프트웨어융합대학"),
    "A10628": ("인공지능학과", "소프트웨어융합대학"),
    "A10979": ("전자공학부", "전자정보대학"),
    "A11164": ("전자공학과", "전자정보대학"),
    "A11167": ("지능로봇공학전공", "공과대학"),
    "A11169": ("기계공학전공", "공과대학"),
}

DEPARTMENT_CODE_ALIASES = {
    "A07308": "A10627",
    "A07333": "A10627",
}


def clean(value) -> str:
    """Return a trimmed string for nullable website values."""
    return "" if value is None else str(value).strip()


def normalize_department_code(value) -> str:
    """Map confirmed historical organization codes to one logical department."""
    code = clean(value)
    return DEPARTMENT_CODE_ALIASES.get(code, code)


def professor_identity(row: dict) -> tuple[str, str] | None:
    """Return a real professor code/name pair, excluding website placeholders."""
    code = clean(row.get("teach_cd"))
    name = clean(row.get("teach_na"))
    if not code or code.upper() == "NONE" or name in {"", ".", ".."}:
        return None
    return code, name


def read_source_files() -> list[tuple[Path, int, str, str, list[dict]]]:
    sources = []
    for path in sorted(INPUT_DIR.glob("*_raw.json")):
        match = FILE_PATTERN.match(path.name)
        if not match:
            print(f"Warning: skipped unexpected filename: {path.name}")
            continue

        with path.open(encoding="utf-8") as file:
            payload = json.load(file)
        rows = payload.get("rows")
        if not isinstance(rows, list):
            raise ValueError(f"{path.name}: top-level 'rows' must be an array")

        year = int(match.group("year"))
        semester = match.group("semester")
        major = match.group("major")
        if semester not in TERM_CODES:
            raise ValueError(f"{path.name}: unsupported semester label: {semester}")
        sources.append((path, year, semester, major, rows))
    return sources


def parse_credits(raw_value: object) -> int:
    value = float(clean(raw_value))
    if not value.is_integer():
        raise ValueError(f"Non-integer credit value found: {raw_value!r}")
    return int(value)


def parse_section(row: dict) -> str:
    display = clean(row.get("lecture_cd_disp"))
    if "-" in display:
        return display.rsplit("-", 1)[1]

    lecture_code = clean(row.get("lecture_cd"))
    course_code = clean(row.get("subjt_cd"))
    if lecture_code.startswith(course_code):
        return lecture_code[len(course_code) :]
    return ""


def timetable_entries(raw_value: object) -> list[str]:
    """Split the website timetable field into non-empty entries."""
    value = clean(raw_value)
    if not value:
        return []
    return [
        entry.strip()
        for entry in re.split(r"(?i)<br\s*/?>", value)
        if entry.strip()
    ]


def parse_class_times(
    raw_value: object, semester: str = ""
) -> tuple[list[dict], list[str]]:
    parsed = []
    warnings = []
    for entry in timetable_entries(raw_value):
        match = TIME_PATTERN.match(entry)
        if match:
            parsed.append(
                {
                    "day": DAY_NAMES[match.group("day")],
                    "start_time": match.group("start"),
                    "end_time": match.group("end"),
                    "room_code": (
                        "ONLINE"
                        if "온라인" in match.group("room")
                        else match.group("room").strip()
                    ),
                }
            )
            continue

        time_only = TIME_WITHOUT_DAY_PATTERN.match(entry)
        if time_only and semester in {"summer", "winter"}:
            room = time_only.group("room").strip()
            for day in ("monday", "tuesday", "wednesday", "thursday", "friday"):
                parsed.append(
                    {
                        "day": day,
                        "start_time": time_only.group("start"),
                        "end_time": time_only.group("end"),
                        "room_code": room,
                    }
                )
            continue

        # These are valid non-standard schedules represented on the offering
        # itself, not malformed class-time rows.
        if (
            "온라인" in entry
            or entry in {"- ()", "미정"}
            or DAY_WITHOUT_TIME_PATTERN.match(entry)
            or "SW예비대학" in entry
            or "sw예비대학" in entry
            or ROOM_WITHOUT_TIME_PATTERN.match(entry)
        ):
            continue

        warnings.append(entry)
    return parsed, warnings


def determine_delivery_mode(grouped_rows: list[tuple]) -> str:
    """Classify an offering as OFFLINE, ONLINE, HYBRID, or TBD."""
    has_online = False
    has_offline = False

    for _, _, _, _, row in grouped_rows:
        timetable = clean(row.get("timetable"))
        if "온라인" in timetable:
            has_online = True

        parsed_times, _ = parse_class_times(timetable, grouped_rows[0][2])
        if any(meeting["room_code"] != "ONLINE" for meeting in parsed_times):
            has_offline = True
        if any(
            (match := ROOM_WITHOUT_TIME_PATTERN.match(entry))
            and "예비대학" not in match.group("room")
            and "온라인" not in match.group("room")
            for entry in timetable_entries(timetable)
        ):
            has_offline = True

    if has_online and has_offline:
        return "HYBRID"
    if has_online:
        return "ONLINE"
    if has_offline:
        return "OFFLINE"
    return "TBD"


def determine_schedule_status(grouped_rows: list[tuple]) -> str:
    """Describe whether an offering has a usable or special schedule."""
    semester = grouped_rows[0][2]
    entries = {
        entry
        for _, _, _, _, row in grouped_rows
        for entry in timetable_entries(row.get("timetable"))
    }

    if any(
        TIME_WITHOUT_DAY_PATTERN.match(entry)
        for entry in entries
    ) and semester in {"summer", "winter"}:
        return "INTENSIVE"

    parsed = [
        meeting
        for _, _, _, _, row in grouped_rows
        for meeting in parse_class_times(row.get("timetable"), semester)[0]
    ]
    if parsed:
        return "SCHEDULED"
    if any("온라인" in entry for entry in entries):
        return "ASYNCHRONOUS"
    if any(
        (match := ROOM_WITHOUT_TIME_PATTERN.match(entry))
        and "예비대학" not in match.group("room")
        and "온라인" not in match.group("room")
        for entry in entries
    ):
        return "ROOM_ONLY"
    return "TBD"


def make_schedule_note(grouped_rows: list[tuple]) -> str:
    """Keep unusual source timetable text that cannot live in class_times."""
    notes = {
        entry
        for _, _, _, _, row in grouped_rows
        for entry in timetable_entries(row.get("timetable"))
        if not TIME_PATTERN.match(entry)
    }
    return " | ".join(sorted(notes))


def is_industry_required(grouped_rows: list[tuple]) -> bool:
    """Return whether any source note marks the offering as 산학필수."""
    return any(
        re.search(r"산학\s*필수", clean(row.get("bigo"))) is not None
        for _, _, _, _, row in grouped_rows
    )


def determine_english_type(grouped_rows: list[tuple]) -> str:
    """Normalize the website English-course label to NONE/PARTIAL/FULL."""
    raw_values = {
        clean(row.get("eng_yn_nm")) for _, _, _, _, row in grouped_rows
    }
    unknown = raw_values.difference(ENGLISH_TYPE_NAMES)
    if unknown:
        raise ValueError(f"Unsupported eng_yn_nm values: {sorted(unknown)!r}")
    normalized = {ENGLISH_TYPE_NAMES[value] for value in raw_values}
    if "FULL" in normalized:
        return "FULL"
    if "PARTIAL" in normalized:
        return "PARTIAL"
    return "NONE"


def make_syllabus_url(row: dict, year: int, semester: str) -> str:
    params = {
        "attribute": "lectPlan",
        "p_year": year,
        "p_term": TERM_CODES[semester],
        "p_teach": clean(row.get("teach_cd")),
        "p_code": clean(row.get("lecture_cd")),
        "p_subjt": clean(row.get("subjt_cd")),
        "lang": "ko",
        "loginYn": "N",
        "schedule_cd": "hakbu",
    }
    return "https://sugang.khu.ac.kr/core?" + urlencode(params)


def write_csv(filename: str, fieldnames: list[str], rows: list[dict]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / filename
    with path.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    sources = read_source_files()
    if not sources:
        raise SystemExit(f"No valid raw JSON files found in {INPUT_DIR}")

    warnings = []
    all_records = []
    for path, year, semester, major, rows in sources:
        for row in rows:
            all_records.append((path, year, semester, major, row))

    department_codes = sorted(
        {
            normalize_department_code(code)
            for _, _, _, major, row in all_records
            for code in (major, clean(row.get("class_cd")))
            if code
        }
    )
    department_ids = {code: index for index, code in enumerate(department_codes, 1)}

    professor_codes = sorted(
        {
            identity[0]
            for _, _, _, _, row in all_records
            if (identity := professor_identity(row)) is not None
        }
    )
    professor_ids = {code: index for index, code in enumerate(professor_codes, 1)}

    departments = []
    for code in department_codes:
        department_name, college_name = DEPARTMENT_METADATA.get(code, ("", ""))
        departments.append(
            {
                "department_id": department_ids[code],
                "code": code,
                "name": department_name,
                "college": college_name,
                "has_track": "",
            }
        )

    offering_groups = {}
    for path, year, semester, major, row in all_records:
        lecture_code = clean(row.get("lecture_cd"))
        if not lecture_code:
            warnings.append(f"{path.name}: skipped row without lecture_cd: {row!r}")
            continue
        offering_key = (year, semester, lecture_code)
        offering_groups.setdefault(offering_key, []).append(
            (path, year, semester, major, row)
        )

    professor_data = {}
    course_data = {}
    offerings = []
    offering_professors = []
    offering_categories = []
    class_times = []
    syllabi = []

    next_offering_id = 1
    next_class_time_id = 1
    next_syllabus_id = 1
    next_offering_category_id = 1

    for offering_key in sorted(offering_groups):
        grouped_rows = offering_groups[offering_key]
        own_department_rows = [
            record
            for record in grouped_rows
            if normalize_department_code(record[3])
            == normalize_department_code(record[4].get("class_cd"))
        ]
        canonical_candidates = own_department_rows or grouped_rows
        canonical_record = next(
            (
                record
                for record in canonical_candidates
                if professor_identity(record[4]) is not None
            ),
            canonical_candidates[0],
        )
        path, year, semester, major, row = canonical_record

        department_code = normalize_department_code(
            clean(row.get("class_cd")) or major
        )
        course_code = clean(row.get("subjt_cd"))

        if not course_code:
            warnings.append(f"{path.name}: skipped row without subjt_cd: {row!r}")
            continue
        offering_professor_codes = set()
        for _, _, _, source_major, source_row in grouped_rows:
            identity = professor_identity(source_row)
            if identity is None:
                continue
            professor_code, professor_name = identity
            source_department_code = normalize_department_code(
                clean(source_row.get("class_cd")) or source_major
            )
            previous = professor_data.get(professor_code)
            current = {
                "professor_id": professor_ids[professor_code],
                "department_id": department_ids[source_department_code],
                "professor_code": professor_code,
                "name": professor_name,
                "email": "",
                "office": "",
            }
            if previous and previous["name"] != professor_name:
                warnings.append(
                    f"Professor code {professor_code} has multiple names: "
                    f"{previous['name']!r}, {professor_name!r}"
                )
            professor_data.setdefault(professor_code, current)
            offering_professor_codes.add(professor_code)

        for professor_code in sorted(offering_professor_codes):
            offering_professors.append(
                {
                    "offering_id": next_offering_id,
                    "professor_id": professor_ids[professor_code],
                }
            )

        course_names = {
            clean(source_row.get("subjt_name"))
            for _, _, _, _, source_row in grouped_rows
            if clean(source_row.get("subjt_name"))
        }
        canonical_course_name = min(course_names, key=lambda name: (len(name), name))

        current_course = {
            "course_code": course_code,
            "department_id": department_ids[department_code],
            "current_name": canonical_course_name,
            "credits": parse_credits(row.get("unit_num")),
        }
        previous_course = course_data.get(course_code)
        if (
            previous_course
            and previous_course["credits"] != current_course["credits"]
        ):
            warnings.append(
                f"Course {course_code} has conflicting credit values: "
                f"{previous_course['credits']} vs {current_course['credits']}"
            )
        course_data[course_code] = current_course

        offering_id = next_offering_id
        next_offering_id += 1
        offerings.append(
            {
                "offering_id": offering_id,
                "course_code": course_code,
                "course_name": canonical_course_name,
                "target_year": clean(row.get("lect_grade")),
                "year": year,
                "semester": semester,
                "section": parse_section(row),
                "campus": clean(row.get("campus_nm")),
                "capacity": row.get("asign_pcnt", ""),
                "industry_required": int(is_industry_required(grouped_rows)),
                "english_type": determine_english_type(grouped_rows),
                "delivery_mode": determine_delivery_mode(grouped_rows),
                "schedule_status": determine_schedule_status(grouped_rows),
                "schedule_note": make_schedule_note(grouped_rows),
            }
        )

        major_rows = {}
        for source_path, _, _, source_major, source_row in grouped_rows:
            normalized_major = normalize_department_code(source_major)
            major_rows.setdefault(normalized_major, []).append(
                (source_path, source_row)
            )

        for source_major in sorted(major_rows):
            source_rows = major_rows[source_major]
            category_variants = {
                clean(source_row.get("field_gb")) for _, source_row in source_rows
            }
            if len(category_variants) > 1:
                warnings.append(
                    f"{offering_key}: category differs within major {source_major}: "
                    f"{sorted(category_variants)!r}"
                )
            source_category_code = sorted(category_variants)[0]
            if source_category_code not in CATEGORY_ID_BY_CODE:
                raise ValueError(
                    f"No category_id for source code {source_category_code!r} "
                    f"in {offering_key}"
                )
            display_names = {
                clean(source_row.get("subjt_name"))
                for _, source_row in source_rows
                if clean(source_row.get("subjt_name"))
            }
            display_name = max(display_names, key=lambda name: (len(name), name))
            offering_categories.append(
                {
                    "offering_category_id": next_offering_category_id,
                    "offering_id": offering_id,
                    "department_id": department_ids[source_major],
                    "category_id": CATEGORY_ID_BY_CODE[source_category_code],
                    "display_name": display_name,
                }
            )
            next_offering_category_id += 1

        meeting_keys = set()
        unparsed_entries = set()
        for source_path, _, _, _, source_row in grouped_rows:
            parsed_times, unparsed_times = parse_class_times(
                source_row.get("timetable"), semester
            )
            for invalid in unparsed_times:
                unparsed_entries.add(
                    (
                        source_path.name,
                        clean(source_row.get("lecture_cd_disp")),
                        invalid,
                    )
                )
            for meeting in parsed_times:
                meeting_keys.add(
                    (
                        meeting["day"],
                        meeting["start_time"],
                        meeting["end_time"],
                        meeting["room_code"],
                    )
                )

        for source_name, lecture_display, invalid in sorted(unparsed_entries):
            warnings.append(
                f"{source_name}: {lecture_display} "
                f"has unparsed timetable entry {invalid!r}"
            )

        for day, start_time, end_time, room_code in sorted(meeting_keys):
            class_times.append(
                {
                    "class_time_id": next_class_time_id,
                    "offering_id": offering_id,
                    "day": day,
                    "start_time": start_time,
                    "end_time": end_time,
                    "room_code": room_code,
                }
            )
            next_class_time_id += 1

        syllabi.append(
            {
                "syllabus_id": next_syllabus_id,
                "offering_id": offering_id,
                "source_url": make_syllabus_url(row, year, semester),
                "objectives": "",
                "eval_method": "",
                "textbook": "",
                "weekly_plan": "",
            }
        )
        next_syllabus_id += 1

    time_slot_keys = sorted(
        {
            (
                meeting["day"],
                meeting["start_time"],
                meeting["end_time"],
            )
            for meeting in class_times
        }
    )

    time_slot_ids = {
        slot: index
        for index, slot in enumerate(time_slot_keys, 1)
    }

    time_slots = [
        {
            "time_slot_id": time_slot_ids[slot],
            "day": slot[0],
            "start_time": slot[1],
            "end_time": slot[2],
        }
        for slot in time_slot_keys
    ]
    
    normalized_class_times = [
    {
        "class_time_id": index,
        "offering_id": meeting["offering_id"],
        "time_slot_id": time_slot_ids[
            (
                meeting["day"],
                meeting["start_time"],
                meeting["end_time"],
            )
        ],
        "room_code": meeting["room_code"],
    }
    for index, meeting in enumerate(class_times, 1)
    ]

    write_csv(
        "departments.csv",
        ["department_id", "code", "name", "college", "has_track"],
        departments,
    )
    write_csv(
        "professors.csv",
        ["professor_id", "department_id", "professor_code", "name", "email", "office"],
        [professor_data[code] for code in sorted(professor_data)],
    )
    write_csv(
        "courses.csv",
        [
            "course_code",
            "department_id",
            "current_name",
            "credits",
        ],
        [course_data[code] for code in sorted(course_data)],
    )
    write_csv(
        "course_offerings.csv",
        [
            "offering_id",
            "course_code",
            "course_name",
            "target_year",
            "year",
            "semester",
            "section",
            "campus",
            "capacity",
            "industry_required",
            "english_type",
            "delivery_mode",
            "schedule_status",
            "schedule_note",
        ],
        offerings,
    )
    write_csv(
        "offering_professors.csv",
        ["offering_id", "professor_id"],
        offering_professors,
    )
    write_csv(
        "course_categories.csv",
        ["category_id", "category_code", "category_name"],
        CATEGORY_DEFINITIONS,
    )
    write_csv(
        "course_offering_categories.csv",
        [
            "offering_category_id",
            "offering_id",
            "department_id",
            "category_id",
            "display_name",
        ],
        offering_categories,
    )
    write_csv(
        "time_slots.csv",
        ["time_slot_id", "day", "start_time", "end_time"],
        time_slots,
    )
    write_csv(
        "class_times.csv",
        ["class_time_id", "offering_id", "time_slot_id", "room_code"],
        normalized_class_times,
    )
    write_csv(
        "syllabi.csv",
        ["syllabus_id", "offering_id", "source_url", "objectives", "eval_method", "textbook", "weekly_plan"],
        syllabi,
    )

    warning_path = OUTPUT_DIR / "conversion_warnings.txt"
    warning_path.write_text("\n".join(warnings) + ("\n" if warnings else ""), encoding="utf-8")

    print(f"Source files: {len(sources)}")
    print(f"Raw course rows: {len(all_records)}")
    print(f"Departments: {len(departments)}")
    print(f"Professors: {len(professor_data)}")
    print(f"Courses: {len(course_data)}")
    print(f"Unique offerings: {len(offerings)}")
    print(f"Offering-professor links: {len(offering_professors)}")
    print(f"Offering-major categories: {len(offering_categories)}")
    print(f"Time slots: {len(time_slots)}")
    print(f"Class-time links: {len(normalized_class_times)}")
    print(f"Syllabus links: {len(syllabi)}")
    print(f"Warnings: {len(warnings)}")
    print(f"Output: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
