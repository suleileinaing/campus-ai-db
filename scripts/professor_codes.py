"""Stand-in professor codes for faculty whose site publishes no code.

Real codes are six-digit numbers. A stand-in continues the department's own
numbering: one past the highest real code among that department's
professors, skipping any code professors.csv already uses.
"""

from __future__ import annotations


def is_real_code(code: str) -> bool:
    return code.isdigit() and len(code) == 6


def next_department_code(professors: list[dict[str, str]], department_codes: list[str]) -> str:
    real_codes = [int(code) for code in department_codes if is_real_code(code)]
    if not real_codes:
        raise ValueError("No real professor code to continue from")
    used = {professor["professor_code"] for professor in professors}
    number = max(real_codes) + 1
    while f"{number:06d}" in used:
        number += 1
    return f"{number:06d}"
