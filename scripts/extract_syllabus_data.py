#!/usr/bin/env python3
"""Extract structured data from public KHU syllabus HTML pages."""

from __future__ import annotations

import argparse
import csv
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlparse
from urllib.request import Request, urlopen

try:
    from bs4 import BeautifulSoup
except ImportError as error:  # pragma: no cover - environment-specific
    raise SystemExit(
        "BeautifulSoup is required. Install it with: python3 -m pip install beautifulsoup4"
    ) from error


PROJECT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = PROJECT_DIR / "processed_data" / "website_tables" / "syllabi.csv"
DEFAULT_OUTPUT_DIR = PROJECT_DIR / "processed_data" / "syllabus_tables"
USER_AGENT = (
    "Mozilla/5.0 (compatible; CampusAI-Capstone/1.0; "
    "+public-academic-data-research)"
)

DETAIL_FIELDS = [
    "syllabus_id", "offering_id", "year", "term_code", "course_name",
    "lecture_code", "professor_name", "professor_office", "course_category",
    "department", "credits_raw", "class_time_room", "homepage",
    "english_course", "consultation_time", "overview", "objectives",
    "operation_modes", "operation_note", "class_types", "class_type_note",
    "teaching_methods", "teaching_method_note", "additional_materials",
    "other_weekly_content", "assignments", "course_notices", "source_url",
    "extracted_at_utc",
]
PREREQUISITE_FIELDS = [
    "prerequisite_id",
    "syllabus_id",
    "prerequisite_type",
    "cohort_start",
    "cohort_end",
    "abeek_applicable",
    "prerequisite_group",
    "prerequisite_code",
    "prerequisite_name",
    "minimum_grade",
    "minimum_required_count",
]
EVALUATION_FIELDS = [
    "evaluation_id", "syllabus_id", "evaluation_item", "percentage", "detail",
]
TEXTBOOK_FIELDS = [
    "textbook_id", "syllabus_id", "sequence", "title", "author", "publisher",
    "publication_year", "isbn", "note",
]
WEEKLY_PLAN_FIELDS = [
    "weekly_plan_id", "syllabus_id", "week", "date_range", "topic_content", "note",
]
REPORT_FIELDS = [
    "syllabus_id", "offering_id", "year", "term_code", "status",
    "prerequisite_count", "evaluation_count", "textbook_count",
    "weekly_plan_count", "error", "source_url",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract normalized CSV tables from public KHU syllabus HTML."
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument(
        "--limit", type=int, default=5,
        help="number of evenly spaced syllabi to extract (default: 5)",
    )
    parser.add_argument(
        "--all", action="store_true", help="extract every matching syllabus"
    )
    parser.add_argument("--years", nargs="+", type=int, metavar="YEAR")
    parser.add_argument(
        "--term-codes", nargs="+", choices=("10", "15", "20", "25"),
        metavar="TERM_CODE",
    )
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--delay", type=float, default=1.0)
    return parser.parse_args()


def validate_args(args: argparse.Namespace) -> None:
    if not args.input.is_file():
        raise SystemExit(f"Input CSV not found: {args.input}")
    if args.limit <= 0:
        raise SystemExit("--limit must be greater than zero")
    if args.timeout <= 0:
        raise SystemExit("--timeout must be greater than zero")
    if args.delay < 0:
        raise SystemExit("--delay must be zero or greater")


def clean_text(element) -> str:
    if element is None:
        return ""
    return "\n".join(
        part.strip() for part in element.stripped_strings if part.strip()
    )


def direct_cells(row) -> list:
    return row.find_all(["th", "td"], recursive=False)


def section_table(soup: BeautifulSoup, heading: str):
    header = next(
        (h for h in soup.find_all(["h2", "h3"]) if clean_text(h) == heading),
        None,
    )
    return header.find_next("table") if header else None


def key_value_table(table) -> dict[str, str]:
    values: dict[str, str] = {}
    if table is None:
        return values
    for row in table.find_all("tr"):
        cells = direct_cells(row)
        index = 0
        while index + 1 < len(cells):
            if cells[index].name == "th" and cells[index + 1].name == "td":
                key = clean_text(cells[index]).replace("\n", " ")
                values[key] = clean_text(cells[index + 1])
                index += 2
            else:
                index += 1
    return values


def selected_labels(labels: list[str], marker_cells: list) -> list[str]:
    selected = []
    for label, cell in zip(labels, marker_cells):
        marker = clean_text(cell)
        if marker and marker not in {"0", "0%", "-"}:
            selected.append(label)
    return selected


def parse_operation_modes(table) -> tuple[str, str]:
    if table is None:
        return "", ""
    rows = table.find_all("tr")
    if len(rows) < 3:
        return "", ""
    first_headers = [clean_text(cell) for cell in direct_cells(rows[0])]
    second_headers = [clean_text(cell) for cell in direct_cells(rows[1])]
    labels = ([first_headers[1]] if len(first_headers) > 1 else []) + second_headers
    markers = [cell for cell in direct_cells(rows[2]) if cell.name == "td"]
    note = ""
    for row in rows[3:]:
        cells = direct_cells(row)
        if cells and clean_text(cells[0]) == "추가설명" and len(cells) > 1:
            note = clean_text(cells[1])
    return " | ".join(selected_labels(labels, markers)), note


def parse_class_types(table) -> tuple[str, str]:
    if table is None:
        return "", ""
    rows = table.find_all("tr")
    if len(rows) < 2:
        return "", ""
    labels = [clean_text(cell) for cell in direct_cells(rows[0])][1:]
    markers = [cell for cell in direct_cells(rows[1]) if cell.name == "td"]
    note = ""
    for row in rows[2:]:
        cells = direct_cells(row)
        if cells and clean_text(cells[0]) == "수업유형 추가설명" and len(cells) > 1:
            note = clean_text(cells[1])
    return " | ".join(selected_labels(labels, markers)), note


def parse_teaching_methods(table) -> tuple[str, str]:
    if table is None:
        return "", ""
    rows = table.find_all("tr")
    selected: list[str] = []
    if len(rows) >= 2:
        labels = [clean_text(cell) for cell in direct_cells(rows[0])][1:]
        markers = [cell for cell in direct_cells(rows[1]) if cell.name == "td"]
        selected.extend(selected_labels(labels, markers))
    if len(rows) >= 4:
        labels = [clean_text(cell) for cell in direct_cells(rows[2])]
        markers = [cell for cell in direct_cells(rows[3]) if cell.name == "td"]
        selected.extend(selected_labels(labels, markers))
    note = ""
    for row in rows[4:]:
        cells = direct_cells(row)
        if cells and clean_text(cells[0]) == "수업진행 추가설명" and len(cells) > 1:
            note = clean_text(cells[1])
    return " | ".join(dict.fromkeys(label for label in selected if label)), note


def parse_cohort_range(value: str) -> tuple[str, str]:
    """Convert 적용학번 text such as '2003 ~ 2020' into range endpoints."""
    years = re.findall(r"(?:19|20)\d{2}", value)
    if not years:
        return "", ""
    if "~" not in value:
        return years[0], years[0]
    stripped = value.strip()
    start = years[0] if not stripped.startswith("~") else ""
    end = years[-1] if not stripped.endswith("~") else ""
    return start, end


def split_prerequisite_course(value: str) -> tuple[str, str]:
    """Return a course code/name pair while preserving name-only entries."""
    normalized = value.replace("\n", " ").strip()
    match = re.match(
        r"^(?P<name>.+?)\((?P<code>[A-Za-z][A-Za-z0-9-]*)\)$", normalized
    )
    if match:
        return match.group("code"), match.group("name").strip()
    return "", normalized


def prerequisite_row(
    syllabus_id: str,
    prerequisite_type: str,
    course_value: str,
    context: dict[str, str],
    minimum_grade: str = "",
) -> dict[str, str] | None:
    code, name = split_prerequisite_course(course_value)
    if not name and not code:
        return None
    return {
        "syllabus_id": syllabus_id,
        "prerequisite_type": prerequisite_type,
        "cohort_start": context.get("cohort_start", ""),
        "cohort_end": context.get("cohort_end", ""),
        "abeek_applicable": context.get("abeek_applicable", ""),
        "prerequisite_group": context.get("prerequisite_group", ""),
        "prerequisite_code": code,
        "prerequisite_name": name,
        "minimum_grade": minimum_grade,
        "minimum_required_count": context.get("minimum_required_count", ""),
    }


def parse_prerequisites(table, syllabus_id: str) -> list[dict[str, str]]:
    if table is None or "조회된 데이터가 존재하지 않습니다" in clean_text(table):
        return []

    results: list[dict[str, str]] = []
    context: dict[str, str] = {}
    rows = table.find_all("tr")
    for row in rows[1:]:
        cells = direct_cells(row)
        if not cells:
            continue
        label = clean_text(cells[0]).replace("\n", " ")

        if cells[0].name == "th" and label == "추천 선수 과목":
            recommended = clean_text(cells[-1]).replace("\n", " ").strip()
            if recommended:
                matches = list(
                    re.finditer(
                        r"([^,;/]+?)\(([A-Za-z][A-Za-z0-9-]*)\)", recommended
                    )
                )
                if matches:
                    for match in matches:
                        row_data = prerequisite_row(
                            syllabus_id,
                            "RECOMMENDED",
                            f"{match.group(1).strip()}({match.group(2)})",
                            {},
                        )
                        if row_data:
                            results.append(row_data)
                else:
                    row_data = prerequisite_row(
                        syllabus_id, "RECOMMENDED", recommended, {}
                    )
                    if row_data:
                        results.append(row_data)
            continue

        values = [clean_text(cell).replace("\n", " ").strip() for cell in cells]
        # A new required-prerequisite group has six data cells. Rowspans make
        # continuation rows contain only course and grade cells.
        if len(values) >= 6:
            cohort_start, cohort_end = parse_cohort_range(values[-6])
            context = {
                "cohort_start": cohort_start,
                "cohort_end": cohort_end,
                "abeek_applicable": values[-5],
                "prerequisite_group": values[-4],
                "minimum_required_count": values[-1],
            }
            course_value = values[-3]
            minimum_grade = values[-2]
        elif len(values) == 4 and context:
            # A new prerequisite subgroup can begin while cohort and ABEEK
            # cells are still carried by rowspans from an earlier row.
            context["prerequisite_group"] = values[0]
            context["minimum_required_count"] = values[3]
            course_value = values[1]
            minimum_grade = values[2]
        elif len(values) >= 2 and context:
            course_value = values[-2]
            minimum_grade = values[-1]
        else:
            continue

        row_data = prerequisite_row(
            syllabus_id, "REQUIRED", course_value, context, minimum_grade
        )
        if row_data:
            results.append(row_data)

    unique: dict[tuple[str, ...], dict[str, str]] = {}
    for row in results:
        key = tuple(row[field] for field in PREREQUISITE_FIELDS if field != "prerequisite_id")
        unique[key] = row
    return list(unique.values())


def parse_evaluations(table, syllabus_id: str) -> list[dict[str, str | int]]:
    results = []
    if table is None:
        return results
    for row in table.find_all("tr")[1:]:
        cells = direct_cells(row)
        if len(cells) < 2:
            continue
        item = clean_text(cells[0])
        percentage_text = clean_text(cells[1])
        match = re.search(r"-?\d+(?:\.\d+)?", percentage_text)
        if not item or not match:
            continue
        percentage = float(match.group())
        results.append(
            {
                "syllabus_id": syllabus_id,
                "evaluation_item": item,
                "percentage": int(percentage) if percentage.is_integer() else percentage,
                "detail": clean_text(cells[2]) if len(cells) > 2 else "",
            }
        )
    return results


def parse_textbooks(table, syllabus_id: str) -> tuple[list[dict[str, str]], str]:
    results = []
    additional = ""
    if table is None:
        return results, additional
    for row in table.find_all("tr")[1:]:
        cells = direct_cells(row)
        if not cells:
            continue
        sequence_index = 0
        label = clean_text(cells[sequence_index])
        if label == "추가문헌 및 자료":
            additional = clean_text(cells[-1]) if len(cells) > 1 else ""
            continue
        # The first textbook row also contains the row-spanning
        # "교재 및 참고자료" header before its sequence number.
        if not label.isdigit() and len(cells) > 1 and clean_text(cells[1]).isdigit():
            sequence_index = 1
            label = clean_text(cells[sequence_index])
        if not label.isdigit():
            continue
        values = [clean_text(cell) for cell in cells[sequence_index + 1:sequence_index + 7]]
        values += [""] * (6 - len(values))
        if not any(values):
            continue
        results.append(
            {
                "syllabus_id": syllabus_id,
                "sequence": label,
                "title": values[0],
                "author": values[1],
                "publisher": values[2],
                "publication_year": values[3],
                "isbn": values[4],
                "note": values[5],
            }
        )
    return results, additional


def parse_weekly_plans(
    table, syllabus_id: str
) -> tuple[list[dict[str, str | int]], dict[str, str]]:
    plans = []
    extras = {"기타": "", "과제": "", "수업 안내사항": ""}
    if table is None:
        return plans, extras
    for row in table.find_all("tr")[1:]:
        cells = direct_cells(row)
        if not cells:
            continue
        label = clean_text(cells[0])
        week_match = re.fullmatch(r"(\d+)주", label)
        if week_match and len(cells) >= 4:
            date_range = clean_text(cells[1])
            topic_content = clean_text(cells[2])
            note = clean_text(cells[3])
            # Do not create placeholder rows when the syllabus provides no
            # information for a week. Absence is represented by no row.
            if not any((date_range, topic_content, note)):
                continue
            plans.append(
                {
                    "syllabus_id": syllabus_id,
                    "week": int(week_match.group(1)),
                    "date_range": date_range,
                    "topic_content": topic_content,
                    "note": note,
                }
            )
        elif label in extras and len(cells) > 1:
            extras[label] = clean_text(cells[1])
    return plans, extras


def parse_syllabus_html(
    html: str, source_row: dict[str, str]
) -> tuple[dict, list[dict], list[dict], list[dict], list[dict]]:
    soup = BeautifulSoup(html, "html.parser")
    if "강의계획서" not in clean_text(soup) or section_table(soup, "기본정보") is None:
        raise ValueError("response is not a recognizable KHU syllabus page")

    basic = key_value_table(section_table(soup, "기본정보"))
    overview = key_value_table(section_table(soup, "수업개요 및 목표"))
    operation_modes, operation_note = parse_operation_modes(
        section_table(soup, "수업운영방식")
    )
    class_types, class_type_note = parse_class_types(
        section_table(soup, "수업유형 및 방법")
    )
    methods_table = section_table(soup, "수업유형 및 방법")
    if methods_table is not None:
        methods_table = methods_table.find_next("table")
    teaching_methods, teaching_method_note = parse_teaching_methods(methods_table)

    textbooks, additional_materials = parse_textbooks(
        section_table(soup, "교재 및 참고자료"), source_row["syllabus_id"]
    )
    weekly_plans, weekly_extras = parse_weekly_plans(
        section_table(soup, "주별강의내용"), source_row["syllabus_id"]
    )
    prerequisites = parse_prerequisites(
        section_table(soup, "선수과목"), source_row["syllabus_id"]
    )
    evaluations = parse_evaluations(
        section_table(soup, "평가방법"), source_row["syllabus_id"]
    )

    details = {
        "syllabus_id": source_row["syllabus_id"],
        "offering_id": source_row["offering_id"],
        "year": source_row["year"],
        "term_code": source_row["term_code"],
        "course_name": basic.get("강좌명", ""),
        "lecture_code": basic.get("학수번호", ""),
        "professor_name": basic.get("교강사명", ""),
        "professor_office": basic.get("사무실/연구실", ""),
        "course_category": basic.get("이수구분", ""),
        "department": basic.get("개설학과", ""),
        "credits_raw": basic.get("학점", ""),
        "class_time_room": basic.get("강의시간 강의실", ""),
        "homepage": basic.get("홈페이지", ""),
        "english_course": basic.get("영어강좌여부", ""),
        "consultation_time": basic.get("면담시간", ""),
        "overview": overview.get("수업개요", ""),
        "objectives": overview.get("수업목표", ""),
        "operation_modes": operation_modes,
        "operation_note": operation_note,
        "class_types": class_types,
        "class_type_note": class_type_note,
        "teaching_methods": teaching_methods,
        "teaching_method_note": teaching_method_note,
        "additional_materials": additional_materials,
        "other_weekly_content": weekly_extras["기타"],
        "assignments": weekly_extras["과제"],
        "course_notices": weekly_extras["수업 안내사항"],
        "source_url": source_row["source_url"],
        "extracted_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    return details, prerequisites, evaluations, textbooks, weekly_plans


def url_metadata(url: str) -> tuple[str, str]:
    query = parse_qs(urlparse(url).query)
    return query.get("p_year", [""])[0], query.get("p_term", [""])[0]


def load_candidates(args: argparse.Namespace) -> list[dict[str, str]]:
    with args.input.open(encoding="utf-8-sig", newline="") as file:
        rows = list(csv.DictReader(file))
    required = {"syllabus_id", "offering_id", "source_url"}
    missing = required.difference(rows[0] if rows else {})
    if missing:
        raise SystemExit(f"Input CSV is missing columns: {sorted(missing)}")
    allowed_years = {str(year) for year in args.years or []}
    allowed_terms = set(args.term_codes or [])
    candidates = []
    for row in rows:
        year, term_code = url_metadata(row["source_url"])
        if allowed_years and year not in allowed_years:
            continue
        if allowed_terms and term_code not in allowed_terms:
            continue
        candidates.append({**row, "year": year, "term_code": term_code})
    return candidates


def evenly_spaced_sample(rows: list[dict[str, str]], limit: int) -> list[dict[str, str]]:
    if len(rows) <= limit:
        return rows
    if limit == 1:
        return [rows[0]]
    indexes = {
        round(index * (len(rows) - 1) / (limit - 1)) for index in range(limit)
    }
    return [rows[index] for index in sorted(indexes)]


def fetch_html(url: str, timeout: float) -> str:
    request = Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.8",
            "Referer": "https://sugang.khu.ac.kr/",
        },
    )
    with urlopen(request, timeout=timeout) as response:
        raw = response.read()
        charset = response.headers.get_content_charset() or "utf-8"
    return raw.decode(charset, errors="replace")


def write_csv_atomic(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def assign_ids(rows: list[dict], id_field: str) -> None:
    for index, row in enumerate(rows, 1):
        row[id_field] = index


def main() -> int:
    args = parse_args()
    validate_args(args)
    candidates = load_candidates(args)
    if not candidates:
        raise SystemExit("No syllabus links match the selected filters")
    selected = candidates if args.all else evenly_spaced_sample(candidates, args.limit)
    print(f"Extracting {len(selected)} of {len(candidates)} matching syllabi")

    details: list[dict] = []
    prerequisites: list[dict] = []
    evaluations: list[dict] = []
    textbooks: list[dict] = []
    weekly_plans: list[dict] = []
    report: list[dict] = []

    for index, row in enumerate(selected, 1):
        report_row = {
            "syllabus_id": row["syllabus_id"], "offering_id": row["offering_id"],
            "year": row["year"], "term_code": row["term_code"],
            "status": "failed", "prerequisite_count": 0,
            "evaluation_count": 0, "textbook_count": 0,
            "weekly_plan_count": 0, "error": "", "source_url": row["source_url"],
        }
        try:
            parsed = parse_syllabus_html(fetch_html(row["source_url"], args.timeout), row)
            detail, prereq_rows, evaluation_rows, textbook_rows, weekly_rows = parsed
            details.append(detail)
            prerequisites.extend(prereq_rows)
            evaluations.extend(evaluation_rows)
            textbooks.extend(textbook_rows)
            weekly_plans.extend(weekly_rows)
            report_row.update(
                status="extracted",
                prerequisite_count=len(prereq_rows),
                evaluation_count=len(evaluation_rows),
                textbook_count=len(textbook_rows),
                weekly_plan_count=len(weekly_rows),
            )
        except (HTTPError, URLError, TimeoutError, OSError, ValueError) as error:
            report_row["error"] = str(error)
            print(f"[{index}/{len(selected)}] syllabus {row['syllabus_id']}: ERROR {error}")
        else:
            print(f"[{index}/{len(selected)}] syllabus {row['syllabus_id']}: extracted")
        report.append(report_row)
        if index < len(selected) and args.delay:
            time.sleep(args.delay)

    assign_ids(prerequisites, "prerequisite_id")
    assign_ids(evaluations, "evaluation_id")
    assign_ids(textbooks, "textbook_id")
    assign_ids(weekly_plans, "weekly_plan_id")
    write_csv_atomic(args.output_dir / "syllabus_details.csv", DETAIL_FIELDS, details)
    write_csv_atomic(
        args.output_dir / "syllabus_prerequisites.csv", PREREQUISITE_FIELDS, prerequisites
    )
    write_csv_atomic(
        args.output_dir / "syllabus_evaluations.csv", EVALUATION_FIELDS, evaluations
    )
    write_csv_atomic(args.output_dir / "syllabus_textbooks.csv", TEXTBOOK_FIELDS, textbooks)
    write_csv_atomic(
        args.output_dir / "syllabus_weekly_plans.csv", WEEKLY_PLAN_FIELDS, weekly_plans
    )
    write_csv_atomic(args.output_dir / "extraction_report.csv", REPORT_FIELDS, report)

    failed = sum(row["status"] == "failed" for row in report)
    print(f"Extracted syllabi: {len(details)}")
    print(f"Failed: {failed}")
    print(f"Output: {args.output_dir}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
