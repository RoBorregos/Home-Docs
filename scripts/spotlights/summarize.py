"""Short English summaries for the spotlights, via Gemini."""

import json
import os
import sys

MAX_COMMENT_CHARS = 1500
MAX_NOTE_CHARS = 300

WEEK_PROMPT = """You write progress notes for a robotics team's weekly report.
For each issue below, summarize what its comments from this week say was done,
found, or decided, in ONE English sentence of at most 25 words. The comments may
be in Spanish; always answer in English. Use only facts stated in the comments.
If the comments carry no progress information, use an empty string.

Return a JSON object mapping each issue number (as a string) to its sentence.

Issues:
"""

SPRINT_PROMPT = """You write the closing summary of one area's sprint for a robotics team.
Below are the sprint's planned tasks with their final status, priority, and latest note.
In 2 or 3 English sentences (at most 60 words total), state what the sprint set out to do,
what was actually delivered, and what is still pending, naming the most important items.
Notes may be in Spanish; always answer in English. Use only the facts given.

Return a JSON object: {"summary": "<text>"}.

Area: """


def ask(prompt: str, models: list[str]) -> dict:
    """Send a prompt that expects a JSON object; returns {} when Gemini is off or every model fails."""
    if not os.environ.get("GEMINI_API_KEY"):
        return {}

    # Lazy import so the generator runs without the SDK when summaries are off
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    config = types.GenerateContentConfig(
        response_mime_type="application/json",
        temperature=0.2,
        max_output_tokens=4096,
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
    )

    for model in models:
        try:
            response = client.models.generate_content(model=model, contents=prompt, config=config)
            return json.loads(response.text)
        except Exception as error:
            print(f"warning: {model} summary failed: {error}", file=sys.stderr)
    return {}


def summarize(entries: list[dict], models: list[str]) -> dict[int, str]:
    """entries: [{"number", "title", "comments": [str]}] -> {number: sentence}."""
    if not entries:
        return {}
    payload = [{**e, "comments": [c[:MAX_COMMENT_CHARS] for c in e["comments"]]} for e in entries]
    data = ask(WEEK_PROMPT + json.dumps(payload, ensure_ascii=False), models)
    try:
        # A model that has nothing to say answers null; only real strings become bullets
        return {int(k): v.strip() for k, v in data.items() if isinstance(v, str) and v.strip()}
    except (AttributeError, ValueError):
        return {}


def sprint_summary(area: str, sprint: str, tasks: list[dict], models: list[str]) -> str:
    """tasks: [{"title", "status", "priority", "note"}] -> short paragraph, or "" when unavailable."""
    if not tasks:
        return ""
    payload = [{**t, "note": (t.get("note") or "")[:MAX_NOTE_CHARS]} for t in tasks]
    data = ask(f"{SPRINT_PROMPT}{area} ({sprint})\nTasks:\n{json.dumps(payload, ensure_ascii=False)}", models)
    summary = data.get("summary") if isinstance(data, dict) else None
    return summary.strip() if isinstance(summary, str) else ""
