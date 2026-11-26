"""API 없이 돌아가는 점검. 프로젝트 루트에서: python -m unittest text2sql.tests.test_offline -v"""

from __future__ import annotations

import csv
import json
import tempfile
import unittest
from pathlib import Path

from text2sql.answer import render_answer
from text2sql.answer_judge import find_leaks, judge_answer, parse_scores, run_answer_judge
from text2sql.sql_judge import backfill_reference_sql, judge_sql, parse_sql_verdict, relevant_schema, run_sql_judge
from text2sql.sql_judge import build_messages as build_sql_messages, constant_notes, is_pass as is_sql_pass
from text2sql.compare import compare_results, gold_is_ordered
from text2sql.config import PROJECT_DIR, TEXT2SQL_DIR
from text2sql.evaluate import evaluate
from text2sql.executor import SQLExecutor, extract_sql
from text2sql.gold_loader import load_gold
from text2sql.llm_judge import judge_record, parse_verdict, run_judge
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

class TestLLMJudge(unittest.TestCase):
    @staticmethod
    def rec(id_, strict, pred_rows, exec_ok=True):
        return {"id": id_, "question": f"{id_} 학점은?", "tags": ["t"], "strict": strict, "relaxed": strict,
                "diagnosis": "correct" if strict else "value_mismatch", "exec_ok": exec_ok,
                "exec_error_kind": None if exec_ok else "sqlite", "pred_sql": f"SELECT '{id_}'",
                "gold_columns": ["credits"], "gold_rows": [[3.0]],
                "pred_columns": ["학점"], "pred_rows": pred_rows}

    def test_parse_verdict(self):
        self.assertEqual(parse_verdict('{"verdict": 1, "reason": "같음"}'), (1, "같음"))
        self.assertEqual(parse_verdict('```json\n{"verdict": "0", "reason": "다름"}\n```'), (0, "다름"))
        for bad in ("정답입니다", '{"verdict": 2, "reason": ""}', "{verdict: 1}"):
            with self.assertRaises(ValueError):
                parse_verdict(bad)

    def test_retry_on_bad_format(self):
        r = judge_record(ScriptedLLM(["맞는 것 같아요", '{"verdict": 1, "reason": "3학점 일치"}']), self.rec("a", False, [["3학점"]]))
        self.assertEqual((r.verdict, r.status, r.reason), (1, "judged", "3학점 일치"))
        r = judge_record(ScriptedLLM(["몰라", "몰라"]), self.rec("a", False, [["3학점"]]))
        self.assertEqual((r.verdict, r.status), (None, "parse_error"))

    def test_exec_fail_skips_judge(self):
        r = judge_record(ScriptedLLM([]), self.rec("a", False, [], exec_ok=False))
        self.assertEqual((r.verdict, r.status), (0, "skipped:exec_fail"))

    def test_run_judge_compare_and_resume(self):
        recs = [self.rec("a", True, [[3]]), self.rec("b", False, [["3학점"]]), self.rec("c", False, [], exec_ok=False)]
        with tempfile.TemporaryDirectory() as d:
            out = Path(d)
            (out / "results.jsonl").write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in recs), encoding="utf-8")
            llm = ScriptedLLM(['{"verdict": 1, "reason": "일치"}', '{"verdict": 1, "reason": "표기만 다름"}'])
            s = run_judge(out, llm, "m")
            self.assertEqual(s["overall"], {"n": 3, "exec_strict": 1, "exec_relaxed": 1, "llm": 2})
            self.assertEqual(s["agreement"], {"both_correct": 1, "llm_only": 1, "both_wrong": 1})
            self.assertIn("표기만 다름", (out / "judge_summary.md").read_text(encoding="utf-8"))
            with (out / "judge_compare.csv").open(encoding="utf-8-sig", newline="") as f:
                self.assertEqual([r["agreement"] for r in csv.DictReader(f)], ["both_correct", "llm_only", "both_wrong"])
            s2 = run_judge(out, ScriptedLLM([]), "m")  # 이미 판정된 문항은 다시 부르지 않음
            self.assertEqual(s2["overall"], s["overall"])


class TestAnswerJudge(unittest.TestCase):
    @staticmethod
    def rec(id_, answer, strict=True, **kw):
        return {"id": id_, "question": f"{id_} 학점은?", "tags": ["t"], "strict": strict, "relaxed": strict,
                "exec_ok": True, "gold_columns": ["credits"], "gold_rows": [[3.0]],
                "pred_columns": ["credits"], "pred_rows": [[3.0]], "answer": answer, **kw}

    def test_find_leaks(self):
        self.assertEqual(find_leaks("3학점이에요."), [])
        leaks = find_leaks("결과 1건이에요.\n- course_code: CSE / {credits}")
        self.assertIn("이름:course_code", leaks)
        self.assertIn("틀:{credits}", leaks)
        self.assertIn("SQL:SELECT", find_leaks("SELECT 1 을 실행했어요"))
        self.assertEqual(find_leaks("snake_case_word 는 스키마에 없음"), [])

    def test_parse_scores(self):
        ok = '{"correctness": 5, "faithfulness": "4", "completeness": 4, "fluency": 3, "reason": "좋음"}'
        self.assertEqual(parse_scores(json.loads(ok))["faithfulness"], 4)
        for bad in ('{"correctness": 6, "faithfulness": 4, "completeness": 4, "fluency": 3}',
                    '{"correctness": 4.5, "faithfulness": 4, "completeness": 4, "fluency": 3}',
                    '{"correctness": 4}'):
            with self.assertRaises(ValueError):
                parse_scores(json.loads(bad))

    def test_judge_answer_pass_fail_and_skip(self):
        good = '{"correctness": 5, "faithfulness": 5, "completeness": 4, "fluency": 5, "reason": "정확"}'
        r = judge_answer(ScriptedLLM(["형식 틀림", good]), self.rec("a", "3학점이에요."))
        self.assertEqual((r["status"], r["passed"], r["correctness"]), ("judged", True, 5))
        r = judge_answer(ScriptedLLM([good]), self.rec("b", "credits_total 아니고 {credits}학점"))
        self.assertFalse(r["passed"])  # 점수는 높아도 내부 노출이면 탈락
        r = judge_answer(ScriptedLLM([]), self.rec("c", None))
        self.assertEqual(r["status"], "skipped:no_answer")

    def test_run_answer_judge_and_resume(self):
        recs = [self.rec("a", "3학점이에요."), self.rec("b", "2학점이에요.", strict=False), self.rec("c", None)]
        replies = ['{"correctness": 5, "faithfulness": 5, "completeness": 5, "fluency": 5, "reason": "정확"}',
                   '{"correctness": 1, "faithfulness": 5, "completeness": 5, "fluency": 5, "reason": "값이 다름"}']
        with tempfile.TemporaryDirectory() as d:
            out = Path(d)
            (out / "results.jsonl").write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in recs), encoding="utf-8")
            s = run_answer_judge(out, ScriptedLLM(replies), "m")
            self.assertEqual((s["overall"]["n"], s["overall"]["passed"], s["no_answer"]), (2, 1, ["c"]))
            self.assertEqual(s["overall"]["avg"]["correctness"], 3.0)
            self.assertIn("값이 다름", (out / "answer_judge.csv").read_text(encoding="utf-8-sig"))
            s2 = run_answer_judge(out, ScriptedLLM([]), "m")  # 이미 판정된 문항은 다시 부르지 않음
            self.assertEqual(s2["overall"], s["overall"])

    def test_evaluate_saves_answer(self):
        items = load_gold(TEAM_GOLD_V2)[12:13]
        reply = "```sql\nSELECT status FROM students WHERE student_id = 202210029\n```\nANSWER: 학적 상태는 {status}이에요."
        engine = Text2SQL(ScriptedLLM([reply]), PromptBuilder(use_fewshot=False, answer_template=True), SQLExecutor())
        with tempfile.TemporaryDirectory() as d:
            evaluate(items, engine, SQLExecutor(), Path(d), save_answers=True)
            rec = json.loads((Path(d) / "results.jsonl").read_text(encoding="utf-8").splitlines()[0])
        self.assertTrue(rec["answer"].startswith("학적 상태는 "))
        self.assertIn("reference_sql", rec)


class TestSQLJudge(unittest.TestCase):
    @staticmethod
    def rec(id_, pred_sql, strict=True, **kw):
        return {"id": id_, "question": "내 2024-1 수강 과목 수는?", "tags": ["t"], "student_id": 202210001,
                "strict": strict, "relaxed": strict, "diagnosis": "correct", "exec_ok": True,
                "gold_sql": "SELECT COUNT(*) FROM enrollments WHERE student_id = 202210001 AND year = 2024",
                "pred_sql": pred_sql, **kw}

    def test_relevant_schema_only_used_tables(self):
        s = relevant_schema("SELECT * FROM enrollments e JOIN course_offerings o USING (offering_id)")
        self.assertIn("CREATE TABLE enrollments", s)
        self.assertIn("CREATE TABLE course_offerings", s)
        self.assertNotIn("CREATE TABLE professors", s)

    def test_constant_notes(self):
        consts = {"course_offerings": [("campus", "국제")]}
        self.assertIn("course_offerings.campus = '국제'",
                      constant_notes("SELECT 1 FROM course_offerings o WHERE o.campus = '국제'", consts=consts))
        self.assertEqual(constant_notes("SELECT 1 FROM course_offerings", consts=consts), "")  # 조건에 안 쓰면 안 알림
        msg = build_sql_messages(self.rec("a", "SELECT COUNT(*) FROM enrollments WHERE student_id = 202210001"))[1]["content"]
        self.assertEqual(msg.count("정답 SQL:"), 1)

    def test_parse_and_pass(self):
        v = parse_sql_verdict({"logic": "1", "extra_condition": 0, "scope_ok": "null", "reason": "같음"})
        self.assertEqual((v["logic"], v["extra_condition"], v["scope_ok"]), (1, 0, None))
        self.assertTrue(is_sql_pass(v))
        self.assertFalse(is_sql_pass({**v, "scope_ok": 0}))
        self.assertFalse(is_sql_pass({**v, "extra_condition": 1}))
        with self.assertRaises(ValueError):
            parse_sql_verdict({"logic": 2, "extra_condition": 0})

    def test_skips(self):
        self.assertEqual(judge_sql(ScriptedLLM([]), self.rec("a", None))["status"], "skipped:no_pred_sql")
        self.assertEqual(judge_sql(ScriptedLLM([]), self.rec("b", "SELECT 1", gold_sql=None))["status"], "skipped:no_reference")
        self.assertEqual(judge_sql(ScriptedLLM([]), self.rec("c", "SELECT 1", expect_refusal=True))["status"], "skipped:refusal")

    def test_run_sql_judge_lucky_and_scope(self):
        recs = [
            self.rec("a", "SELECT COUNT(*) FROM enrollments WHERE student_id = 202210001"),  # 학기 조건 누락인데 결과는 같음
            self.rec("b", "SELECT COUNT(*) FROM enrollments WHERE student_id = 202210001 OR 1=1", strict=False),
            self.rec("c", "SELECT COUNT(*) FROM enrollments WHERE student_id = 202210001 AND year = 2024"),
        ]
        replies = ['{"logic": 0, "extra_condition": 0, "scope_ok": 1, "reason": "학기 조건 누락"}',
                   '{"logic": 0, "extra_condition": 0, "scope_ok": 0, "reason": "OR 1=1 로 전체 학생"}',
                   '{"logic": 1, "extra_condition": 0, "scope_ok": 1, "reason": "같음"}']
        with tempfile.TemporaryDirectory() as d:
            out = Path(d)
            (out / "results.jsonl").write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in recs), encoding="utf-8")
            s = run_sql_judge(out, ScriptedLLM(replies), "m")
            o = s["overall"]
            self.assertEqual((o["n"], o["passed"], o["lucky"], o["scope_violation"]), (3, 1, 1, 1))
            md = (out / "sql_judge_summary.md").read_text(encoding="utf-8")
            self.assertIn("우연히 맞음", md)
            self.assertIn("본인 학번 범위 위반", md)

    def test_backfill_reference_sql_from_gold(self):
        items = load_gold(TEXT2SQL_DIR / "gold" / "실행평가_15문항.json")[:1]
        recs = [{"id": items[0].id, "gold_sql": None}]
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "config.json").write_text(json.dumps({"gold": "text2sql/gold/실행평가_15문항.json"}), encoding="utf-8")
            backfill_reference_sql(recs, Path(d))
        self.assertEqual(recs[0]["reference_sql"], items[0].reference_sql)


class TestSearchRoute(unittest.TestCase):
    """숫자·조건 질문은 SQL, 강의계획서 본문 질문은 SEARCH → 검색(RAG)."""

    class FakeRetriever:
        def __init__(self):
            self.calls = []

        def search(self, query, courses):
            from text2sql.syllabus_rag import Hit
            self.calls.append((query, courses))
            return [Hit(0.7, "CSE406", "07", "캡스톤디자인", "[CSE406-07] 캡스톤디자인\n팀 프로젝트로 진행")]

        def answer(self, question, hits):
            from text2sql.chatkhu_client import LLMResponse
            return "네, CSE406-07은 팀 프로젝트로 진행해요.", LLMResponse(text="", model="m", prompt_tokens=100, completion_tokens=20)

    def test_search_line_routes_to_retriever(self):
        r = self.FakeRetriever()
        prompt = PromptBuilder(use_fewshot=False, answer_template=True, search=True)
        out = Text2SQL(ScriptedLLM(["SEARCH: [CSE406, 캡스톤디자인] 팀 프로젝트 진행 방식"]), prompt, SQLExecutor(),
                       retriever=r).ask("캡스톤디자인 팀플이야?")
        self.assertEqual(out.route, "search")
        self.assertEqual(r.calls, [("팀 프로젝트 진행 방식", ["CSE406", "캡스톤디자인"])])
        self.assertEqual(out.sources, ["CSE406-07"])
        self.assertIn("팀 프로젝트", out.answer)
        self.assertEqual(out.total_tokens, 120)
        self.assertEqual(len(out.attempts), 1)  # 검색은 SQL 수정 루프를 돌지 않음

    def test_sql_question_stays_sql(self):
        r = self.FakeRetriever()
        reply = "```sql\nSELECT 30 AS midterm_percentage\n```\nANSWER: 중간고사 비율은 {midterm_percentage}%예요."
        out = Text2SQL(ScriptedLLM([reply]), PromptBuilder(use_fewshot=False, answer_template=True, search=True),
                       SQLExecutor(), retriever=r).ask("중간고사 비율은?")
        self.assertEqual((out.route, out.answer, r.calls), ("sql", "중간고사 비율은 30%예요.", []))

    def test_search_without_retriever_and_empty_courses(self):
        out = Text2SQL(ScriptedLLM(["SEARCH: [] 파이썬 실습"]), PromptBuilder(use_fewshot=False), SQLExecutor()).ask("q")
        self.assertEqual(out.route, "search")
        self.assertIn("준비되지 않았어요", out.answer)
        r = self.FakeRetriever()
        Text2SQL(ScriptedLLM(["SEARCH: [] 파이썬 실습"]), PromptBuilder(use_fewshot=False), SQLExecutor(),
                 retriever=r).ask("q")
        self.assertEqual(r.calls, [("파이썬 실습", [])])

    def test_prompt_rules_only_when_enabled(self):
        self.assertIn("SEARCH:", PromptBuilder(use_fewshot=False, search=True).system_prompt())
        self.assertNotIn("SEARCH:", PromptBuilder(use_fewshot=False).system_prompt())  # 평가 프롬프트는 그대로

    def test_matches_course(self):
        from text2sql.syllabus_rag import matches_course
        self.assertTrue(matches_course("cse406", "CSE406", "07", "캡스톤디자인"))
        self.assertTrue(matches_course("CSE406-07", "CSE406", "07", "캡스톤디자인"))
        self.assertFalse(matches_course("CSE406-08", "CSE406", "07", "캡스톤디자인"))
        self.assertTrue(matches_course("캡스톤 디자인", "SWCON401", "00", "소프트웨어융합캡스톤디자인"))
        self.assertFalse(matches_course("딥러닝", "CSE406", "07", "캡스톤디자인"))

    def test_chunk_split_limit(self):
        from text2sql.syllabus_rag import _split
        parts = _split("가" * 1000 + "\n짧은 줄\n" + "나" * 50, 300)
        self.assertTrue(all(len(p) <= 300 for p in parts))
        self.assertEqual("".join(p.replace("\n", "") for p in parts), "가" * 1000 + "짧은 줄" + "나" * 50)


class TestAnswer(unittest.TestCase):
    """LLM 의 답변 틀에 결과를 로컬에서 채운다(결과 행은 LLM 에 보내지 않음)."""

    def test_single_row(self):
        self.assertEqual(render_answer("담당 교수님은 {professor_name} 교수님이에요.", ["professor_name"], [("김휘용",)]),
                         "담당 교수님은 김휘용 교수님이에요.")

    def test_repeat_rows_and_count(self):
        rows = [("CSE406", "06"), ("CSE495", "02")]
        self.assertEqual(render_answer("[[{course_code}-{section}]]로 {count}개예요.", ["course_code", "section"], rows),
                         "CSE406-06, CSE495-02로 2개예요.")

    def test_multi_row_column_joined_and_float(self):
        self.assertEqual(render_answer("{credits}학점", ["credits"], [(3.0,), (3.0,), (2.0,)]), "3, 2학점")

    def test_fallbacks(self):
        self.assertEqual(render_answer("{x}", ["a"], []), "조건에 맞는 결과가 없어요.")
        self.assertEqual(render_answer("{없는컬럼}", ["a"], [(1,)]), "결과는 1이에요.")
        self.assertEqual(render_answer(None, ["a", "b"], [(1, 2)]), "결과 1건이에요.\n- 1 / 2")  # 모르는 이름은 숨김

    def test_alias_typo_still_fills(self):
        # J098: 모델이 'AS credit_shortfall' 을 'AScredit_shortfall' 로 써서 틀을 못 채우던 문제
        cols = ["required_credits", "AScredit_shortfall", "is_satisfied"]
        out = render_answer("필요 {required_credits}학점, 부족 {credit_shortfall}학점, 충족 {is_satisfied}",
                            cols, [(9, 3, 0)])
        self.assertEqual(out, "필요 9학점, 부족 3학점, 충족 0")
        self.assertEqual(render_answer("{Professor_Name}", ["professor_name"], [("김",)]), "김")
        # 후보가 둘 이상이면 추측하지 않고 기본 문장으로
        self.assertNotIn("{", render_answer("{name}", ["professor_name", "course_name"], [("김", "캡스톤")]))

    def test_codes_shown_in_korean(self):
        self.assertEqual(render_answer("{course_name}({english_type})", ["course_name", "english_type"],
                                       [("고급딥러닝", "PARTIAL")]), "고급딥러닝(영어 일부 강의)")
        self.assertEqual(render_answer("{english_label}, {day}", ["english_label", "day"], [("NONE", "monday")]),
                         "해당 없음, 월요일")
        self.assertEqual(render_answer("{grade}", ["grade"], [("NONE",)]), "NONE")  # 뜻을 모르는 컬럼은 그대로

    def test_default_answer_hides_column_names(self):
        out = render_answer(None, ["required_credits", "per_area_min_credits", "AScredit_shortfall", "학점"],
                            [(9, 3, 3, 3)])
        self.assertEqual(out, "결과 1건이에요.\n- 필요 학점: 9 / 영역당 최소 학점: 3 / 3 / 학점: 3")
        self.assertEqual(find_leaks(out), [])

    def test_long_list_truncated(self):
        out = render_answer("[[{n}]]", ["n"], [(i,) for i in range(25)])
        self.assertTrue(out.endswith("외 5건"))

    def test_pipeline_answer(self):
        reply = "```sql\nSELECT 'CSE' AS code, 3 AS credits\n```\nANSWER: {code} 과목은 {credits}학점이에요."
        prompt = PromptBuilder(use_fewshot=False, answer_template=True)
        out = Text2SQL(ScriptedLLM([reply]), prompt, SQLExecutor()).ask("질문")
        self.assertTrue(out.result.ok)
        self.assertEqual(out.answer, "CSE 과목은 3학점이에요.")
        self.assertIn("ANSWER:", prompt.system_prompt())
        self.assertNotIn("ANSWER:", PromptBuilder(use_fewshot=False).system_prompt())  # 평가용 프롬프트는 그대로

    def test_template_kept_across_repair(self):
        replies = ["```sql\nSELECT nope FROM nowhere\n```\nANSWER: 값은 {v}예요.", "```sql\nSELECT 7 AS v\n```"]
        out = Text2SQL(ScriptedLLM(replies), PromptBuilder(use_fewshot=False), SQLExecutor()).ask("질문")
        self.assertEqual(len(out.attempts), 2)
        self.assertEqual(out.answer, "값은 7예요.")

    def test_clarify_and_refuse_answers(self):
        out = Text2SQL(ScriptedLLM(["CLARIFY: 몇 분반인가요?"]), PromptBuilder(use_fewshot=False), SQLExecutor()).ask("질문")
        self.assertEqual(out.answer, "몇 분반인가요?")
        out = Text2SQL(ScriptedLLM(["REFUSE: 타인 정보"]), PromptBuilder(use_fewshot=False), SQLExecutor()).ask("질문")
        self.assertIn("처리할 수 없어요", out.answer)
