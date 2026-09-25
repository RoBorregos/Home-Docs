import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "spotlights"))

import generate  # noqa: E402
import project  # noqa: E402
import render  # noqa: E402
import summarize  # noqa: E402
from render import Run  # noqa: E402

FIXTURE = json.loads((ROOT / "tests" / "fixtures" / "project_items.json").read_text())
CFG = {**generate.load_config(), "members": {"Fernando94654": "Fernando"}}
SPRINTS = project.parse_sprints(FIXTURE["fields"], "Sprint")
ITEMS = project.parse_items(FIXTURE["items"], "Sprint")
BOARD = {i.number: i for i in ITEMS}
TITLES = {s.start: s.title for s in SPRINTS}
S1, S2 = [s for s in SPRINTS if s.start in (date(2026, 8, 10), date(2026, 8, 31))]


def manipulation(sprint):
    return [i for i in ITEMS if i.sprint_start == sprint.start and i.values.get("Area") == "Manipulation"]


def page_with_plan(area, sprint, numbers):
    lines = [f"- **X** 💻 Task {n} ([#{n}](https://github.com/RoBorregos/home2/issues/{n}))" for n in numbers]
    page = render.skeleton(area, "https://example.com", CFG)
    return render.upsert(page, Run("plan", sprint), "### Sprint plan\n\n" + "\n".join(lines) + "\n")


class TestParsing:
    def test_board_is_read_as_sprints_and_issues(self):
        # Sprint titles repeat across years, so both "Sprint 1" survive
        assert [s.title for s in SPRINTS].count("Sprint 1") == 2
        assert SPRINTS == sorted(SPRINTS, key=lambda s: s.start)
        # Drafts and pull requests are not tasks; bot comments are not progress
        assert [i.number for i in ITEMS] == [1, 2, 3, 4, 5, 6]
        assert ITEMS[0].values["Status"] == "Done" and ITEMS[0].sprint_start == S2.start
        assert [c.author for c in ITEMS[0].comments] == ["Fernando94654"]


class TestRunSelection:
    def test_sprint_start_writes_results_and_plan(self):
        runs = generate.plan_runs(SPRINTS, date(2026, 8, 31))
        assert [(r.kind, r.sprint) for r in runs] == [("results", S1), ("plan", S2)]

    def test_week_window_is_the_sprint_week_whatever_the_run_weekday(self):
        monday, friday = generate.plan_runs(SPRINTS, date(2026, 9, 14)), generate.plan_runs(SPRINTS, date(2026, 9, 18))
        for (run,) in (monday, friday):
            assert (run.key, run.start, run.end) == ("week-2", date(2026, 9, 7), date(2026, 9, 14))

    def test_explicit_modes(self):
        day = date(2026, 9, 7)
        assert generate.plan_runs(SPRINTS, day, "plan") == [Run("plan", S2)]
        assert generate.plan_runs(SPRINTS, day, "results") == [Run("results", S1)]
        assert generate.plan_runs(SPRINTS, date(2026, 9, 1), "weekly") == []

    def test_backfill_covers_earlier_sections(self):
        runs = generate.backfill_runs(SPRINTS, date(2026, 9, 14))
        assert [(r.kind, r.sprint, r.week) for r in runs] == [("results", S1, 0), ("plan", S2, 0), ("week", S2, 1)]


class TestSections:
    def test_week_section(self):
        run, items = generate.week_run(S2, 1), manipulation(S2)
        body = render.section(run, items, CFG, {1: "Pick works."})
        assert "**Done this week:**" in body
        assert "- **Fernando** 💻 Pick &lt;cup&gt; & place (P0, [#1]" in body
        assert "🔍 Grasp research" in body
        assert "): Pick works." in body
        assert "**Not started:** 1 task." in body
        # Without a Gemini summary the bullet still says something
        assert "): 1 new comment" in render.section(run, items, CFG)

    def test_results_section(self):
        body = render.section(Run("results", S2), manipulation(S2), CFG, overview="Pick <done>, pour pending.")
        assert "**1/3 tasks done (33%)** · P0: 1/2.\n\nPick &lt;done&gt;, pour pending.\n\n**Done:**" in body
        assert "- **Unassigned** 💻 Pour (Todo, P0, [#3]" in body

    def test_empty_area(self):
        assert "_No tasks on the board" in render.section(Run("plan", S2), [], CFG)

    def test_hygiene_flags_missing_fields(self):
        problems = generate.hygiene(ITEMS, CFG)
        assert any("#3" in p and "no assignee" in p for p in problems)
        assert any("#4" in p and "no Area" in p for p in problems)


class TestResultsFromPlan:
    """Results come from the published plan, so a task moved to another sprint still counts."""

    def test_moved_task_still_counts(self):
        run = Run("results", S2)
        items, moved = generate.results_items(
            page_with_plan("Manipulation", S2, [1, 2, 3, 5]), run, manipulation(S2), BOARD, TITLES)
        assert [i.number for i in items] == [1, 2, 3, 5]
        assert moved == {5: "moved to Sprint 3"}

        body = render.section(run, items, CFG, moved=moved)
        assert "**1/4 tasks done (25%)**" in body
        assert "Teleoperation arm (Todo, P1, moved to Sprint 3, [#5]" in body

    def test_without_a_plan_block_falls_back_to_the_board(self):
        page = render.skeleton("Manipulation", "https://example.com", CFG)
        items, moved = generate.results_items(page, Run("results", S2), manipulation(S2), BOARD, TITLES)
        assert [i.number for i in items] == [1, 2, 3] and moved == {}

    def test_moved_task_finished_later_is_not_credited(self):
        # #6 was planned in Sprint 1, moved to Sprint 2 and only closed on 2026-09-25
        run = Run("results", S1)
        items, moved = generate.results_items(page_with_plan("Vision", S1, [6]), run, [], BOARD, TITLES)
        assert moved == {6: "moved to Sprint 2"}

        body = render.section(run, items, CFG, moved=moved)
        assert "**0/1 tasks done (0%)**" in body
        assert "**Carried over:**" in body and "Late merge (Done, moved to Sprint 2," in body


class TestSummaries:
    def test_null_answers_are_dropped(self, monkeypatch):
        # A model with nothing to say answers null; that must not reach the page as "None"
        monkeypatch.setattr(summarize, "ask", lambda prompt, models: {"12": None, "13": " Real progress. "})
        entries = [{"number": n, "title": "t", "comments": ["c"]} for n in (12, 13)]
        assert summarize.summarize(entries, []) == {13: "Real progress."}

        monkeypatch.setattr(summarize, "ask", lambda prompt, models: {"summary": None})
        assert summarize.sprint_summary("Vision", "Sprint 2", [{"title": "t"}], []) == ""


class TestUpsert:
    def build(self, runs):
        page = render.skeleton("Manipulation", "https://example.com", CFG)
        for run in runs:
            page = render.upsert(page, run, f"### {run.sprint.title} {run.key}\n")
        return page

    def test_order_and_idempotency(self):
        runs = [Run("plan", S1), generate.week_run(S2, 1), Run("results", S1), Run("plan", S2)]
        page = self.build(runs)
        headings = [line for line in page.splitlines() if line.startswith("#")]
        assert headings[1:] == [
            render.sprint_heading(S2), "### Sprint 2 plan", "### Sprint 2 week-1",
            render.sprint_heading(S1), "### Sprint 1 plan", "### Sprint 1 results",
        ]
        assert render.upsert(page, Run("plan", S2), "### Sprint 2 plan\n") == page
        assert "\n\n\n" not in page

    def test_replace_keeps_manual_notes(self):
        page = self.build([Run("plan", S2)]) + "\nManual video link.\n"
        page = render.upsert(page, Run("plan", S2), "### Updated plan\n")
        assert "### Updated plan" in page and "Manual video link." in page
        assert render.has_block(page, Run("plan", S2))
