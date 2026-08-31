"""Prompt construction for the answering layer.

Deliberately free of any LLM client: this module turns retrieval results into
two strings. That keeps the prompt reviewable in a diff, testable without an API
key, and unchanged if the provider is ever swapped.

Citations are numbers, never URLs. The model writes [2]; the caller maps 2 back
to results[1] and renders the link. Asking a model to reproduce a URL invites
mangled anchors and invented paths.

Usage (from the repository root) — prints the exact prompt for a question:
    .venv/bin/python -m chatbot.prompt "which camera does the robot use?"
"""

import sys

from chatbot.retrieval import Result

# Only bites if a caller raises top_k; excess is dropped from the lowest ranks.
MAX_CONTEXT_CHARS = 12000

SYSTEM_PROMPT = """\
You answer questions about the RoBorregos @Home robotics documentation, using \
only the excerpts supplied with each question.

Rules:

1. Ground every statement in the excerpts. If they do not contain the answer, \
say so plainly and suggest what the reader might look for instead. Never fill \
a gap with general robotics knowledge: the reader cannot tell which parts came \
from their documentation, and a confident wrong answer costs more than no answer.

2. Cite the excerpt behind each claim by its number, like [1] or [2][3]. Only \
cite numbers that appear in the excerpts you were given.

3. Excerpts marked "historical" describe how the project worked in a past year, \
not how it works today. If your answer rests on one, say so in the sentence \
itself ("as of 2023, ..."). When a current and a historical excerpt cover the \
same topic, prefer the current one.

4. Answer in the language of the question. Keep file names, node names and code \
identifiers exactly as the documentation spells them.

5. Be brief. Answer what was asked, usually in two or three sentences. Use a \
list only when the answer is genuinely a list.

6. Write the answer directly. Do not narrate your process — no "based on the \
provided context" or "the excerpts indicate". The citations already show where \
the information came from."""

USER_TEMPLATE = """\
Excerpts:

{context}

Question: {query}"""


def chunk_body(chunk: dict) -> str:
    """The chunk text without the breadcrumb the indexer prepended.

    The breadcrumb is shown on the excerpt's header line, so leaving it in the
    body would repeat it and spend tokens twice.
    """
    body = chunk["text"]
    breadcrumb = " > ".join(chunk["heading_path"])
    if breadcrumb and body.startswith(breadcrumb):
        body = body[len(breadcrumb):]
    return body.strip()


def freshness(chunk: dict) -> str:
    """How the excerpt should be trusted in time.

    A third of the corpus lives under docs/years/ and describes past states of
    the project. Retrieval already demotes it; this label is what stops the
    model from presenting it as current.
    """
    year = chunk.get("year")
    return f"historical: {year}" if year else "current"


def format_context(results: list[Result], max_chars: int = MAX_CONTEXT_CHARS) -> str:
    """Render the excerpts as a numbered block.

    Numbering is 1-based and follows ranking order, so citation [n] maps to
    results[n - 1].
    """
    entries: list[str] = []
    used = 0

    for number, result in enumerate(results, start=1):
        chunk = result.chunk
        header = (
            f"[{number}] {chunk['source']} — "
            f"{' > '.join(chunk['heading_path']) or chunk['source']} "
            f"({freshness(chunk)})"
        )
        entry = f"{header}\n{chunk_body(chunk)}"

        if used + len(entry) > max_chars and entries:
            break
        entries.append(entry)
        used += len(entry)

    return "\n\n".join(entries)


def build_prompt(query: str, results: list[Result]) -> tuple[str, str]:
    """Return (system_prompt, user_prompt) for the supplied question.

    Callers should not reach here with an empty `results`: with nothing to
    ground an answer in, there is no reason to spend a request.
    """
    return SYSTEM_PROMPT, USER_TEMPLATE.format(
        context=format_context(results), query=query
    )


def main() -> None:
    from chatbot.retrieval import Retriever

    query = " ".join(sys.argv[1:]) or "which camera does the robot use?"
    results = Retriever().search(query)

    system, user = build_prompt(query, results)
    print(f"=== SYSTEM ({len(system)} chars) ===\n{system}")
    print(f"\n=== USER ({len(user)} chars) ===\n{user}")
    print(f"\n=== total ~{(len(system) + len(user)) // 4} tokens ===")


if __name__ == "__main__":
    main()
