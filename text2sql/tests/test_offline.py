"""API 없이 돌아가는 점검. 프로젝트 루트에서: python -m unittest text2sql.tests.test_offline -v"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from text2sql.compare import compare_results, gold_is_ordered
from text2sql.config import PROJECT_DIR, TEXT2SQL_DIR
from text2sql.evaluate import evaluate
from text2sql.executor import SQLExecutor, extract_sql
from text2sql.gold_loader import load_gold
from text2sql.pipeline import Text2SQL
from text2sql.prompt import PromptBuilder
from text2sql.tests.mock_llm import BrokenThenFixedLLM, OracleLLM, ScriptedLLM

EXAMPLE_GOLD = TEXT2SQL_DIR / "gold" / "example_gold_from_samples.json"
ME, OTHER = 202210001, 202210002


class TestExtract(unittest.TestCase):
    def test_variants(self):
        self.assertEqual(extract_sql("```sql\nSELECT 1\n```"), "SELECT 1")
        self.assertEqual(extract_sql("답:\n```\nSELECT 2;\n```"), "SELECT 2;")
        self.assertEqual(extract_sql("쿼리는 SELECT 3 입니다"), "SELECT 3 입니다")
        self.assertIsNone(extract_sql("모르겠어요"))


class TestGuard(unittest.TestCase):
    ex = SQLExecutor()

    def assertRejected(self, sql, sid=None):
        r = self.ex.run(sql, student_id=sid)
        self.assertFalse(r.ok, sql)
        self.assertEqual(r.error_kind, "guard", r.error)

    def test_write_and_multi_statement_rejected(self):
        self.assertRejected("UPDATE courses SET credits = 0")
        self.assertRejected("SELECT 1; DROP TABLE courses")
        self.assertRejected("PRAGMA table_info(courses)")
        self.assertRejected("ATTACH DATABASE 'x.db' AS x")

    def test_semicolon_inside_string_ok(self):
        self.assertTrue(self.ex.run("SELECT 'a;b' AS v").ok)

    def test_with_cte_ok(self):
        r = self.ex.run("WITH x AS (SELECT course_code FROM courses LIMIT 2) SELECT * FROM x")
        self.assertTrue(r.ok, r.error)
        self.assertEqual(len(r.rows), 2)

    def test_personal_tables_need_login(self):
        self.assertRejected("SELECT COUNT(*) FROM enrollments")
        self.assertRejected(f"SELECT * FROM students WHERE student_id = {ME}")  # 로그인 없음

    def test_other_student_rejected(self):
        self.assertRejected(f"SELECT * FROM enrollments WHERE student_id = {OTHER}", ME)
        self.assertRejected("SELECT * FROM enrollments", ME)  # 학생 조건 없음

    def test_own_student_ok(self):
        r = self.ex.run(f"SELECT COUNT(*) FROM enrollments WHERE student_id = {ME}", ME)
        self.assertTrue(r.ok, r.error)

    def test_personal_table_via_subquery_detected(self):
        self.assertRejected("SELECT course_code FROM courses WHERE course_code IN (SELECT course_code FROM enrollments)")

    def test_sqlite_error_reported(self):
        r = self.ex.run("SELECT no_such_col FROM courses")
        self.assertFalse(r.ok)
        self.assertEqual(r.error_kind, "sqlite")

    def test_row_limit(self):
        r = SQLExecutor(row_limit=5).run("SELECT offering_id FROM course_offerings")
        self.assertTrue(r.truncated)
        self.assertEqual(len(r.rows), 5)


class TestCompare(unittest.TestCase):
    def test_strict_and_unordered(self):
        self.assertTrue(compare_results([(1, "a"), (2, "b")], [(2, "b"), (1, "a")], ordered=False).strict)
        self.assertFalse(compare_results([(1, "a"), (2, "b")], [(2, "b"), (1, "a")], ordered=True).strict)

    def test_float_int(self):
        self.assertTrue(compare_results([(3,)], [(3.0,)], ordered=False).strict)

    def test_relaxed_extra_and_reordered_columns(self):
        c = compare_results([("CSE101", 3)], [("자료구조", 3, "CSE101")], ordered=False)
        self.assertFalse(c.strict)
        self.assertTrue(c.relaxed)
        self.assertEqual(c.diagnosis, "correct_extra_columns")

    def test_duplicates_matter(self):
        self.assertFalse(compare_results([(1,), (1,)], [(1,)], ordered=False).relaxed)

    def test_order_detection(self):
        self.assertTrue(gold_is_ordered("SELECT a FROM t ORDER BY a"))
        self.assertFalse(gold_is_ordered("SELECT a FROM (SELECT a FROM t ORDER BY a)"))


class TestPipeline(unittest.TestCase):
    def setUp(self):
        self.items = load_gold(EXAMPLE_GOLD)
        self.prompt = PromptBuilder(use_fewshot=False)

    def test_prompt_has_no_student_names(self):
        import sqlite3
        conn = sqlite3.connect(str(PROJECT_DIR / "database" / "campus_ai.db"))
        names = [r[0] for r in conn.execute("SELECT name FROM students")]
        text = PromptBuilder().system_prompt()
        self.assertFalse([n for n in names if n in text])

    def test_repair_loop(self):
        answers = {i.question: i.gold_sql for i in self.items if "course_name" in i.gold_sql}
        q = next(iter(answers))
        out = Text2SQL(BrokenThenFixedLLM(answers), self.prompt, SQLExecutor()).ask(q)
        self.assertEqual(len(out.attempts), 2)
        self.assertFalse(out.attempts[0].ok)
        self.assertTrue(out.result.ok)

    def test_gives_up_after_max_repairs(self):
        llm = ScriptedLLM(["모르겠어요"] * 3)
        out = Text2SQL(llm, self.prompt, SQLExecutor(), max_repairs=2).ask("아무 질문")
        self.assertEqual(len(out.attempts), 3)
        self.assertEqual(out.result.error_kind, "no_sql")

    def test_oracle_eval_is_perfect(self):
        llm = OracleLLM({i.question: i.gold_sql for i in self.items})
        with tempfile.TemporaryDirectory() as d:
            s = evaluate(self.items, Text2SQL(llm, self.prompt, SQLExecutor()), SQLExecutor(), Path(d))
            self.assertEqual(s["overall"]["strict"], len(self.items))
            self.assertTrue((Path(d) / "summary.md").exists())
            lines = (Path(d) / "results.jsonl").read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(lines), len(self.items))
            json.loads(lines[0])

    def test_csv_template_loads(self):
        items = load_gold(TEXT2SQL_DIR / "gold" / "TEMPLATE.csv")
        self.assertEqual(items[1].student_id, ME)
        self.assertEqual(items[1].answer_rows(), [(123,)])
        self.assertEqual(items[1].tags, ["개인화", "집계"])


if __name__ == "__main__":
    unittest.main()


INTEGRATED_DB = PROJECT_DIR / "database" / "campus_ai_integrated.db"
TEAM_GOLD_CSV = TEXT2SQL_DIR / "gold" / "personal_gold_v1.csv"
TEAM_GOLD_JSON = TEXT2SQL_DIR / "gold" / "personal_gold_v1.json"


@unittest.skipUnless(INTEGRATED_DB.exists(), "통합 DB 없음")
class TestTeamGold(unittest.TestCase):
    def setUp(self):
        self.ex = SQLExecutor(db_path=INTEGRATED_DB)

    def test_korean_csv_headers(self):
        items = load_gold(TEAM_GOLD_CSV)
        self.assertEqual(len(items), 21)
        self.assertEqual(items[0].student_id, 202210029)
        self.assertIsNone(items[18].student_id)  # '-' → 로그인 없음
        self.assertTrue(items[20].expect_refusal)
        self.assertIsNone(items[20].gold_sql)

    def test_prompt_adapts_to_integrated_db(self):
        text = PromptBuilder(db_path=INTEGRATED_DB).system_prompt()
        self.assertIn("academic_calendar", text)
        self.assertIn("is_retake", text)
        self.assertNotIn("syllabus_chunks", text)

    def test_refusal_scoring(self):
        items = [i for i in load_gold(TEAM_GOLD_JSON) if i.expect_refusal]
        prompt = PromptBuilder(use_fewshot=False, db_path=INTEGRATED_DB)
        cases = {
            "REFUSE: 다른 학생 정보": "correct_refusal:refused",
            "```sql\nSELECT e.grade FROM enrollments e JOIN students s ON s.student_id = e.student_id "
            "WHERE s.name LIKE '김%'\n```": "correct_refusal:guard",
            "```sql\nSELECT e.grade FROM enrollments e WHERE e.student_id = 202210029 AND 1 = 0\n```":
                "no_leak_but_not_refused",
        }
        for reply, expected in cases.items():
            engine = Text2SQL(ScriptedLLM([reply] * 3), prompt, self.ex, max_repairs=0)
            with tempfile.TemporaryDirectory() as d:
                evaluate(items, engine, self.ex, Path(d))
                rec = json.loads((Path(d) / "results.jsonl").read_text(encoding="utf-8").splitlines()[0])
            self.assertEqual(rec["diagnosis"], expected, reply)

    def test_oracle_team_gold(self):
        items = load_gold(TEAM_GOLD_JSON)
        llm = OracleLLM({i.question: (None if i.expect_refusal else i.gold_sql) for i in items})
        prompt = PromptBuilder(use_fewshot=False, db_path=INTEGRATED_DB)
        with tempfile.TemporaryDirectory() as d:
            s = evaluate(items, Text2SQL(llm, prompt, self.ex), self.ex, Path(d))
        self.assertEqual(s["overall"]["strict"], 21)


TEAM_GOLD_V2 = TEXT2SQL_DIR / "gold" / "personal_gold_v2.csv"


class TestTeamGoldV2(unittest.TestCase):
    """GitHub 최신 DB(campus_ai.db) 기준 16문항."""

    def test_answers_match_db(self):
        ex = SQLExecutor()
        items = load_gold(TEAM_GOLD_V2)
        self.assertEqual(len(items), 16)
        for it in items:
            res = ex.run(it.gold_sql, it.student_id, enforce_scope=False)
            self.assertTrue(res.ok, f"{it.id}: {res.error}")
            self.assertTrue(compare_results(it.answer_rows(), res.rows, ordered=False).strict, it.id)

    def test_order_only_counts_in_strict(self):
        c = compare_results([(1,), (2,)], [(2,), (1,)], ordered=True)
        self.assertFalse(c.strict)
        self.assertTrue(c.relaxed)
        self.assertEqual(c.diagnosis, "order_mismatch")


class TestSubset(unittest.TestCase):
    def test_missing_id_column(self):
        c = compare_results([(202210029, "재학")], [("재학",)], ordered=False, gold_columns=["student_id", "status"])
        self.assertFalse(c.relaxed)
        self.assertTrue(c.subset)
        self.assertEqual(c.missing_columns, ["student_id"])

    def test_wrong_value_not_subset(self):
        c = compare_results([(202210029, "재학")], [("휴학",)], ordered=False)
        self.assertFalse(c.subset)

    def test_subset_ignores_duplicate_rows(self):
        gold = [(1, "김교수", "101호"), (2, "김교수", "101호"), (3, "이교수", "202호")]
        c = compare_results(gold, [("김교수", "101호"), ("이교수", "202호")], ordered=False)
        self.assertTrue(c.subset)

    def test_rescore_roundtrip(self):
        items = load_gold(TEAM_GOLD_V2)[12:13]  # 학적 상태
        llm = ScriptedLLM(["```sql\nSELECT status FROM students WHERE student_id = 202210029\n```"])
        with tempfile.TemporaryDirectory() as d:
            s = evaluate(items, Text2SQL(llm, PromptBuilder(use_fewshot=False), SQLExecutor()), SQLExecutor(), Path(d))
        self.assertEqual((s["overall"]["relaxed"], s["overall"]["subset"]), (0, 1))