"""Markdown rendering and in-place page updates for sprint spotlights."""

import re
from dataclasses import dataclass
from datetime import date, datetime, timedelta

from project import Item, Sprint

BLOCK_RE = re.compile(
    r"<!-- spotlight:(?P<sprint>\d{4}-\d{2}-\d{2}):(?P<key>[\w-]+) -->\r?\n.*?<!-- /spotlight -->\r?\n?",
    re.S,
)
SPRINT_RE = re.compile(r"^<!-- sprint:(?P<sprint>\d{4}-\d{2}-\d{2}) -->\r?$", re.M)

ACTIVE = ["Review", "Testing", "In Progress"]
NOT_STARTED = ["Todo", "Backlog"]


@dataclass(frozen=True)
class Run:
    kind: str  # plan | week | results
    sprint: Sprint
    week: int = 0
    start: date | None = None
    end: date | None = None  # exclusive

    @property
    def key(self) -> str:
        return f"week-{self.week}" if self.kind == "week" else self.kind


def block_order(key: str) -> int:
    if key == "plan":
        return 0
    if key == "results":
        return 1000
    return int(key.removeprefix("week-"))


def escape(text: str) -> str:
    # Only angle brackets: they would be parsed as raw HTML; a bare & renders fine
    return text.strip().replace("<", "&lt;").replace(">", "&gt;")


def span(start: date, end: date) -> str:
    return f"{start.isoformat()} → {(end - timedelta(days=1)).isoformat()}"


def in_window(run: Run, moment: datetime | None, cfg: dict) -> bool:
    return moment is not None and run.start <= moment.astimezone(cfg["tz"]).date() < run.end


# --- lines -------------------------------------------------------------------

def owners(item: Item, cfg: dict) -> str:
    names = [cfg["members"].get(login) or name or login for login, name in item.assignees]
    return ", ".join(f"**{escape(n)}**" for n in names) or "**Unassigned**"


def emoji(item: Item, cfg: dict) -> str:
    kind = item.values.get(cfg["fields"]["kind"], "").lower()
    return cfg["kinds"].get(kind, cfg["default_kind"])[0]


def line(item: Item, cfg: dict, status: bool = False, note: str | None = None,
         extra: str | None = None) -> str:
    meta = [
        item.values.get(cfg["fields"]["status"]) if status else None,
        item.values.get(cfg["fields"]["priority"]),
        extra,
        f"[#{item.number}]({item.url})",
    ]
    text = f"- {owners(item, cfg)} {emoji(item, cfg)} {escape(item.title)} ({', '.join(m for m in meta if m)})"
    return f"{text}: {escape(note)}" if note else text


def group(title: str, lines: list[str]) -> list[str]:
    return [f"**{title}:**", "", *lines, ""] if lines else []


def by_status(items: list[Item], cfg: dict, statuses: list[str]) -> list[str]:
    out = []
    for status in statuses:
        matching = [i for i in items if i.values.get(cfg["fields"]["status"]) == status]
        out += group(status, [line(i, cfg) for i in matching])
    return out


def status_order(items: list[Item], cfg: dict) -> list[Item]:
    order = {s: n for n, s in enumerate(cfg["statuses"])}
    return sorted(items, key=lambda i: (order.get(i.values.get(cfg["fields"]["status"]), 99), i.number))


# --- sections ----------------------------------------------------------------

def plan_section(run: Run, items: list[Item], cfg: dict) -> list[str]:
    out = ["### Sprint plan", "", f"{len(items)} tasks planned for this sprint.", ""]
    out += by_status(items, cfg, cfg["statuses"])
    no_status = [i for i in items if i.values.get(cfg["fields"]["status"]) not in cfg["statuses"]]
    out += group("No status", [line(i, cfg) for i in no_status])
    return out


def week_section(run: Run, items: list[Item], cfg: dict, summaries: dict[int, str]) -> list[str]:
    status = cfg["fields"]["status"]
    inside = lambda moment: in_window(run, moment, cfg)

    done = [i for i in items if i.values.get(status) == "Done" and inside(i.closed_at)]
    updated = [i for i in items if any(inside(c.created) for c in i.comments)]
    pending = [i for i in items if i.values.get(status, "Todo") in NOT_STARTED]

    out = [f"### Week {run.week} · {span(run.start, run.end)}", ""]
    out += group("Done this week", [line(i, cfg) for i in done])
    out += by_status(items, cfg, ACTIVE)
    notes = []
    for item in updated:
        count = sum(inside(c.created) for c in item.comments)
        notes.append(line(item, cfg, note=summaries.get(item.number) or f"{count} new comment{'s' * (count > 1)}"))
    out += group("Updates", notes)
    if pending:
        out += [f"**Not started:** {len(pending)} task{'s' * (len(pending) > 1)}.", ""]
    if len(out) == 2:
        out += ["_No activity recorded on the board this week._", ""]
    return out


def finished_in(item: Item, sprint: Sprint, cfg: dict, moved: dict[int, str]) -> bool:
    """Done on the board. A task that left the sprint counts only if it closed before the sprint did."""
    if item.values.get(cfg["fields"]["status"]) != "Done":
        return False
    if item.number not in moved or item.closed_at is None:
        return True
    return item.closed_at.astimezone(cfg["tz"]).date() < sprint.end


def results_section(run: Run, items: list[Item], cfg: dict, overview: str | None,
                    moved: dict[int, str]) -> list[str]:
    priority = cfg["fields"]["priority"]
    done = [i for i in items if finished_in(i, run.sprint, cfg, moved)]
    rest = status_order([i for i in items if i not in done], cfg)
    p0 = [i for i in items if i.values.get(priority) == "P0"]

    stats = f"**{len(done)}/{len(items)} tasks done ({round(100 * len(done) / len(items)) if items else 0}%)**"
    if p0:
        stats += f" · P0: {sum(i in done for i in p0)}/{len(p0)}"
    out = ["### Sprint results", "", f"{stats}.", ""]
    if overview:
        out += [escape(overview), ""]
    out += group("Done", [line(i, cfg) for i in done])
    out += group("Carried over", [line(i, cfg, status=True, extra=moved.get(i.number)) for i in rest])
    return out


def section(
    run: Run,
    items: list[Item],
    cfg: dict,
    summaries: dict[int, str] | None = None,
    overview: str | None = None,
    moved: dict[int, str] | None = None,
) -> str:
    items = sorted(items, key=lambda i: i.number)
    if run.kind == "plan":
        lines = plan_section(run, items, cfg)
    elif run.kind == "week":
        lines = week_section(run, items, cfg, summaries or {})
    else:
        lines = results_section(run, items, cfg, overview, moved or {})
    if not items:
        lines = lines[:2] + ["_No tasks on the board for this area in this sprint._", ""]
    return "\n".join(lines).rstrip() + "\n"


# --- page --------------------------------------------------------------------

def skeleton(area: str, board_url: str, cfg: dict) -> str:
    legend = [cfg["default_kind"], *cfg["kinds"].values()]
    return "\n".join([
        "# Sprints",
        "",
        f"Sprint spotlights for the {area} area, generated every week from the "
        f"[project board]({board_url}) and reviewed by the area PM before merging. Newest sprint first.",
        "",
        "Status legend:",
        "",
        *(f"- {icon} {label}" for icon, label in legend),
        "",
    ])


def normalise(page: str) -> str:
    """Hand edits and Windows checkouts can change the line endings the markers rely on."""
    return page.replace("\r\n", "\n").rstrip("\n") + "\n"


def sprint_heading(sprint: Sprint) -> str:
    return f"## {sprint.title} · {span(sprint.start, sprint.end)}"


ISSUE_RE = re.compile(r"\[#(\d+)\]")


def issue_numbers(text: str) -> list[int]:
    """The issues a rendered section links to, in order, without repeats."""
    return list(dict.fromkeys(int(n) for n in ISSUE_RE.findall(text)))


def block_body(page: str, sprint_start: date, key: str) -> str | None:
    sid = sprint_start.isoformat()
    for match in BLOCK_RE.finditer(page):
        if match["sprint"] == sid and match["key"] == key:
            return match.group(0)
    return None


def has_block(page: str, run: Run) -> bool:
    sid = run.sprint.start.isoformat()
    return any(m["sprint"] == sid and m["key"] == run.key for m in BLOCK_RE.finditer(page))


def upsert(page: str, run: Run, body: str) -> str:
    sid = run.sprint.start.isoformat()
    block = f"<!-- spotlight:{sid}:{run.key} -->\n\n{body.strip()}\n\n<!-- /spotlight -->\n"

    for match in BLOCK_RE.finditer(page):
        if match["sprint"] == sid and match["key"] == run.key:
            return page[:match.start()] + block + page[match.end():]

    sprints = [(m["sprint"], m.start()) for m in SPRINT_RE.finditer(page)]
    mine = next((pos for s, pos in sprints if s == sid), None)

    # New sprint: goes above the first older sprint (newest first)
    if mine is None:
        pos = next((p for s, p in sprints if s < sid), len(page))
        new = f"<!-- sprint:{sid} -->\n\n{sprint_heading(run.sprint)}\n\n{block}"
        tail = page[pos:]
        return page[:pos].rstrip("\n") + "\n\n" + new + ("\n" + tail if tail else "")

    # Existing sprint: keep blocks in plan -> weeks -> results order
    end = next((p for _, p in sprints if p > mine), len(page))
    for match in BLOCK_RE.finditer(page, mine, end):
        if block_order(match["key"]) > block_order(run.key):
            return page[:match.start()] + block + "\n" + page[match.start():]
    tail = page[end:]
    return page[:end].rstrip("\n") + "\n\n" + block + ("\n" + tail if tail else "")
