# Sprint spotlights

Generates each area's `docs/development/<area>/sprints.md` from the [Home2 project board](https://github.com/orgs/RoBorregos/projects/28). A GitHub Action runs it every Monday and opens a PR for the area PMs to review.

## What gets written

Sprints are 3-week iterations of the board's `Sprint` field, starting on Monday. The run date decides which sections are written:

| Run day | Sections |
|---|---|
| First week of a sprint | **Sprint results** of the sprint that just ended, then the **Sprint plan** of the new one |
| Day 7, day 14 | **Week N**: the last full week of the current sprint |
| Between sprints | Results of the last sprint only |

Each section lists the sprint's issues for that area:

- **Sprint plan**: every issue, grouped by Status.
- **Week N**: issues closed that week (*Done this week*), issues in Review / Testing / In Progress, *Updates* (issues with comments that week, one English sentence written by Gemini), and a count of issues not started.
- **Sprint results**: `done/total (%)`, P0 completion, the Done list, and the carried-over issues with their final status.

## Page format

```markdown
# Sprints
(intro + legend)

<!-- sprint:2026-08-31 -->
## Sprint 2 · 2026-08-31 → 2026-09-20

<!-- spotlight:2026-08-31:plan -->
### Sprint plan
...
<!-- /spotlight -->

<!-- spotlight:2026-08-31:week-1 -->
### Week 1 · 2026-08-31 → 2026-09-06
...
<!-- /spotlight -->

<!-- sprint:2026-08-10 -->
## Sprint 1 · 2026-08-10 → 2026-08-30
...
```

- Sprints are newest first. Inside a sprint the order is plan → weeks → results.
- Sprints are keyed by start date, not title: the board has a "Sprint 1" in 2025 and another in 2026.
- A run only replaces the content between its own markers. Text outside the markers (videos, notes) is never touched.
- Re-running for the same date gives the same page (Gemini wording may vary).
- **Backfill**: an `auto` run also writes earlier sections that are missing from a page: the plan and the past weeks of the current sprint, and the last sprint's results. Sections that already exist are not rewritten. This way a week is not lost when the previous PR was never merged.

## Files

| File | Role |
|---|---|
| `generate.py` | CLI entry point. Loads the config, fetches the board, decides which sections to write, and writes the pages and the PR report. |
| `project.py` | Read-only GraphQL client. Fetches the Sprint iterations and all board items (paginated), then parses issues into `Sprint`, `Item` and `Comment` dataclasses. Draft issues, PRs and bot comments are skipped. |
| `render.py` | Turns items into markdown sections and inserts or replaces the marker blocks in a page. Has no network access. |
| `summarize.py` | Sends the week's comments to Gemini and gets back one English sentence per issue. Tries each model in `gemini_models`; on failure, or without `GEMINI_API_KEY`, it returns nothing and the bullet says "N new comments". |
| `config.yml` | Board, field names, area → folder map, Kind → emoji, status order, member nicknames, Gemini models. |
| `requirements.txt` | Runtime dependencies (`pyyaml`, `google-genai`). |

Related files outside this folder:

- `.github/workflows/spotlights.yml`: the Monday cron and the manual trigger.
- `tests/spotlights_test.py` and `tests/fixtures/project_items.json`: offline tests.
- `docs/resources/pm/cadence.md`: the board conventions for PMs.

### How a run flows

```
generate.main()
 ├─ load_config()                      config.yml + timezone
 ├─ project.fetch()                    board URL, sprints, items (GraphQL)
 ├─ plan_runs() + backfill_runs()      which sections, from the run date and mode
 └─ for each section, for each area:
      ├─ filter items by Sprint start date + Area
      ├─ week_summaries() → summarize()        weekly sections only
      ├─ render.section()                      markdown body
      └─ render.upsert()                       write it into sprints.md
    then hygiene() + write_report()            PR description
```

## Running locally

`.env` at the repo root needs:

```bash
PROJECT_TOKEN="github_pat_..."   # required: read access to the org project and home2 issues
GEMINI_API_KEY="..."             # optional: without it, Updates say "N new comments"
```

```bash
set -a; . ./.env; set +a

# Preview only, nothing is written
.venv/bin/python scripts/spotlights/generate.py --dry-run

# Simulate another day / force a mode
.venv/bin/python scripts/spotlights/generate.py --date 2026-09-14 --dry-run
.venv/bin/python scripts/spotlights/generate.py --mode results --dry-run

# Write the pages, then check them
.venv/bin/python scripts/spotlights/generate.py
.venv/bin/mkdocs serve        # http://127.0.0.1:8000/development/manipulation/sprints/
.venv/bin/python -m pytest
```

Options:

| Flag | Default | Meaning |
|---|---|---|
| `--mode` | `auto` | `auto` (from the date, with backfill), `plan`, `weekly`, or `results` |
| `--date` | today in Monterrey | Run as if today were `YYYY-MM-DD` |
| `--dry-run` | off | Print sections instead of writing pages |
| `--report FILE` | none | Write the PR description (sections + board hygiene) to `FILE` |

## GitHub Action

`.github/workflows/spotlights.yml` runs every Monday at 06:00 UTC (00:00 Monterrey) and can be started from **Actions → Sprint spotlights → Run workflow** with `mode`, `date` and `dry_run`. It runs only on `RoBorregos/Home-Docs`, not on the preview fork.

Steps: install deps → generate → `pytest` (includes `mkdocs build --strict`) → open or update the PR on the `spotlights/auto` branch. The PR description lists the sections written and any board-hygiene problems. A dry run only writes to the job summary.

Each run rebuilds the PR from `main`, so merge it before the next Monday. Edits made on the PR branch are lost.

One-time setup:

1. Repo secret `PROJECT_TOKEN`: fine-grained PAT, owner RoBorregos, Projects read + Issues read on `home2`.
2. Repo secret `GEMINI_API_KEY`.
3. Settings → Actions → General → allow GitHub Actions to create and approve pull requests.

## Configuration

`config.yml`:

- `areas`: board Area option → docs folder. A new area needs an entry here. If that folder has a `.pages` file with an explicit `nav`, add `sprints.md` to it (as in `manipulation/.pages`).
- `kinds` / `default_kind`: board Kind option → `[emoji, legend label]`.
- `statuses`: display order of statuses in the plan and in the carried-over list.
- `members`: GitHub login → display name. Optional; the fallback is the GitHub profile name, then the login.
- `gemini_models`: tried in order when a model fails (e.g. a 503 "high demand").

## Board conventions

The output is only as good as the board. Every sprint issue needs **Area**, **Sprint**, **Status** and an **assignee**. Issues without an Area do not appear in the docs, and they are listed in the PR description. Set **Priority** and **Kind** when possible. Progress goes in **issue comments**; they become the weekly *Updates*.

## Troubleshooting

| Symptom | Cause |
|---|---|
| `PROJECT_TOKEN is not set` | `.env` not loaded into the shell, or the secret is missing |
| `GraphQL error ... Could not resolve to a ProjectV2` | The token has no access to the org project |
| `warning: <model> summary failed: 503 ...` | That Gemini model is overloaded; the next model is tried |
| `Nav entry "sprints.md" not found` | A `.pages` file lists `sprints.md` but the page was never generated |
| A deleted section comes back | Backfill re-adds missing sections of the current sprint and the last results |
