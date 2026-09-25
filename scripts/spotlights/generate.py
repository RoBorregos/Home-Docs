"""Generate per-area sprint spotlight pages from the GitHub project board."""

import argparse
import os
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import yaml

import project
import render
from render import Run
from summarize import sprint_summary, summarize

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent


def load_config(path: Path = HERE / "config.yml") -> dict:
    with open(path, encoding="utf-8") as file:
        cfg = yaml.safe_load(file)
    cfg["members"] = cfg.get("members") or {}
    cfg["tz"] = ZoneInfo(cfg["timezone"])
    return cfg


# --- which sections to write -------------------------------------------------

def current_sprint(sprints: list[project.Sprint], day: date) -> project.Sprint | None:
    return next((s for s in sprints if s.start <= day < s.end), None)


def last_finished(sprints: list[project.Sprint], day: date) -> project.Sprint | None:
    return max((s for s in sprints if s.end <= day), key=lambda s: s.end, default=None)


def week_run(sprint: project.Sprint, week: int) -> Run:
    start = sprint.start + timedelta(days=7 * (week - 1))
    return Run("week", sprint, week, start, min(start + timedelta(days=7), sprint.end))


def plan_runs(sprints: list[project.Sprint], day: date, mode: str = "auto") -> list[Run]:
    current, finished = current_sprint(sprints, day), last_finished(sprints, day)
    weeks = (day - current.start).days // 7 if current else 0

    if mode == "plan":
        target = current or next((s for s in sprints if s.start > day), None)
        return [Run("plan", target)] if target else []
    if mode == "weekly":
        return [week_run(current, weeks)] if weeks else []
    if mode == "results":
        return [Run("results", finished)] if finished else []

    runs = []
    # Results stay pending for the first week after a sprint closes
    if finished and (day - finished.end).days < 7:
        runs.append(Run("results", finished))
    if current:
        runs.append(week_run(current, weeks) if weeks else Run("plan", current))
    return runs


def backfill_runs(sprints: list[project.Sprint], day: date) -> list[Run]:
    """Earlier sections, written only where missing (e.g. last week's PR was never merged)."""
    current, finished = current_sprint(sprints, day), last_finished(sprints, day)
    runs = [Run("results", finished)] if finished else []
    if current:
        weeks = (day - current.start).days // 7
        runs += [Run("plan", current)] + [week_run(current, w) for w in range(1, weeks)] if weeks else []
    return [r for r in runs if r not in plan_runs(sprints, day)]


# --- output ------------------------------------------------------------------

def label(run: Run) -> str:
    if run.kind == "week":
        return f"{run.sprint.title} · week {run.week} ({render.span(run.start, run.end)})"
    return f"{run.sprint.title} · {'sprint plan' if run.kind == 'plan' else 'sprint results'}"


def week_summaries(run: Run, items: list[project.Item], cfg: dict) -> dict[int, str]:
    entries = [
        {
            "number": item.number,
            "title": item.title,
            "comments": [c.body for c in item.comments if render.in_window(run, c.created, cfg)],
        }
        for item in items
    ]
    return summarize([e for e in entries if e["comments"]], cfg["gemini_models"])


def sprint_overview(run: Run, area: str, items: list[project.Item], cfg: dict) -> str:
    whole_sprint = Run("results", run.sprint, start=run.sprint.start, end=run.sprint.end)
    tasks = []
    for item in items:
        notes = [c.body for c in item.comments if render.in_window(whole_sprint, c.created, cfg)]
        tasks.append({
            "title": item.title,
            "status": item.values.get(cfg["fields"]["status"], "No status"),
            "priority": item.values.get(cfg["fields"]["priority"], ""),
            "note": notes[-1] if notes else "",
        })
    return sprint_summary(area, run.sprint.title, tasks, cfg["gemini_models"])


def hygiene(items: list[project.Item], cfg: dict) -> list[str]:
    area_field = cfg["fields"]["area"]
    problems = []
    for item in sorted(items, key=lambda i: i.number):
        missing = []
        if item.values.get(area_field) not in cfg["areas"]:
            missing.append("no Area")
        if not item.assignees:
            missing.append("no assignee")
        if not item.values.get(cfg["fields"]["status"]):
            missing.append("no Status")
        if missing:
            problems.append(f"- [#{item.number}]({item.url}) {render.escape(item.title)}: {', '.join(missing)}")
    return problems


def write_report(path: Path, day: date, runs: list[Run], problems: list[str]) -> None:
    lines = [f"Automated sprint spotlights generated for {day.isoformat()}.", "", "**Sections:**", ""]
    lines += [f"- {label(r)}" for r in runs] or ["- none"]
    if problems:
        lines += ["", "**Board hygiene** (these issues are missing from, or unassigned in, the docs):", "", *problems]
    lines += [
        "",
        "Area PMs: review your area's `sprints.md` and merge before the next week run, "
        "which regenerates this PR. Add videos or notes after merging, outside the "
        "`<!-- spotlight -->` markers.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=["auto", "plan", "weekly", "results"], default="auto")
    parser.add_argument("--date", type=date.fromisoformat, help="run as if today were YYYY-MM-DD")
    parser.add_argument("--dry-run", action="store_true", help="print sections instead of writing pages")
    parser.add_argument("--report", type=Path, help="write a PR body summary to this file")
    args = parser.parse_args(argv)

    cfg = load_config()
    token = os.environ.get("PROJECT_TOKEN") or sys.exit("PROJECT_TOKEN is not set")
    day = args.date or datetime.now(cfg["tz"]).date()
    board_url, sprints, items = project.fetch(token, cfg["org"], cfg["project"], cfg["fields"]["sprint"])

    runs = plan_runs(sprints, day, args.mode)
    extra = backfill_runs(sprints, day) if args.mode == "auto" else []
    written, problems = [], []

    for run in extra + runs:
        in_sprint = [i for i in items if i.sprint_start == run.sprint.start]
        touched = False
        for area, folder in cfg["areas"].items():
            path = ROOT / folder / "sprints.md"
            page = path.read_text(encoding="utf-8") if path.exists() else render.skeleton(area, board_url, cfg)
            if run in extra and render.has_block(page, run):
                continue

            area_items = [i for i in in_sprint if i.values.get(cfg["fields"]["area"]) == area]
            summaries = week_summaries(run, area_items, cfg) if run.kind == "week" else {}
            overview = sprint_overview(run, area, area_items, cfg) if run.kind == "results" else None
            body = render.section(run, area_items, cfg, summaries, overview)
            touched = True
            if args.dry_run:
                print(f"<!-- {path.relative_to(ROOT)} -->\n\n{body}")
            else:
                path.write_text(render.upsert(page, run, body), encoding="utf-8")
        if touched:
            written.append(run)
            problems += [p for p in hygiene(in_sprint, cfg) if p not in problems]

    print(f"{day}: " + ("; ".join(label(r) for r in written) or "nothing to generate"))
    if args.report:
        write_report(args.report, day, written, problems)


if __name__ == "__main__":
    main()
