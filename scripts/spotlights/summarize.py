"""One-line English summaries of issue comments, via Gemini."""

import json
import os
import sys

MAX_COMMENT_CHARS = 1500

PROMPT = """You write progress notes for a robotics team's weekly report.
For each issue below, summarize what its comments from this week say was done,
found, or decided, in ONE English sentence of at most 25 words. The comments may
be in Spanish; always answer in English. Use only facts stated in the comments.
If the comments carry no progress information, use an empty string.

Return a JSON object mapping each issue number (as a string) to its sentence.

Issues:
"""


def summarize(entries: list[dict], models: list[str]) -> dict[int, str]:
    """entries: [{"number", "title", "comments": [str]}] -> {number: sentence}."""
    if not entries or not os.environ.get("GEMINI_API_KEY"):
        return {}

    # Lazy import so the generator runs without the SDK when summaries are off
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    payload = [
        {**e, "comments": [c[:MAX_COMMENT_CHARS] for c in e["comments"]]} for e in entries
    ]
    config = types.GenerateContentConfig(
        response_mime_type="application/json",
        temperature=0.2,
        max_output_tokens=4096,
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
    )

    for model in models:
        try:
            response = client.models.generate_content(
                model=model,
                contents=PROMPT + json.dumps(payload, ensure_ascii=False),
                config=config,
            )
            data = json.loads(response.text)
            return {int(k): str(v).strip() for k, v in data.items() if str(v).strip()}
        except Exception as error:
            print(f"warning: {model} summary failed: {error}", file=sys.stderr)
    return {}
