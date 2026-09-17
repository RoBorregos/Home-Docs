"""Measure the answering layer against the golden set.

Retrieval metrics stop at "was the right document retrieved". This asks the
harder question: did the model actually use it, and cite it honestly.

Usage (from the repository root):
    .venv/bin/python -m chatbot.eval.answers                  # all 45, cap=1
    .venv/bin/python -m chatbot.eval.answers --cap 2          # compare the cap
    .venv/bin/python -m chatbot.eval.answers --limit 10       # quick pass
    .venv/bin/python -m chatbot.eval.answers --show           # print each answer

Costs one LLM call per question, so a full run spends ~45 of the daily quota.
"""

import re
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml

from chatbot import llm
from chatbot.prompt import build_prompt
from chatbot.retrieval import Retriever

GOLDEN_SET = Path(__file__).parent / "golden_set.yaml"
CITATION = re.compile(r"\[\s*(\d+(?:\s*,\s*\d+)*)\s*\]")
TOP_K = 5


@dataclass
class Outcome:
    query: str
    answer: str | None
    reason: str | None
    cited: list[int]
    invalid: list[int]
    hit: bool          # an expected source is among the cited chunks


def cited_numbers(answer: str) -> list[int]:
    """Every citation number in the answer, deduplicated, in order."""
    numbers: list[int] = []
    for match in CITATION.finditer(answer):
        for raw in match.group(1).split(","):
            number = int(raw.strip())
            if number not in numbers:
                numbers.append(number)
    return numbers


def run_case(retriever: Retriever, case: dict, cap: int | None) -> Outcome:
    results = retriever.search(case["query"], top_k=TOP_K, max_per_source=cap)
    if not results:
        return Outcome(case["query"], None, "no_results", [], [], False)

    try:
        answer = llm.generate(*build_prompt(case["query"], results))
    except llm.LLMUnavailable as error:
        return Outcome(case["query"], None, error.reason, [], [], False)

    cited = cited_numbers(answer)
    invalid = [n for n in cited if not 1 <= n <= len(results)]
    sources = {results[n - 1].chunk["source"] for n in cited if 1 <= n <= len(results)}
    return Outcome(
        query=case["query"],
        answer=answer,
        reason=None,
        cited=cited,
        invalid=invalid,
        hit=bool(sources & set(case["expect"])),
    )


def report(outcomes: list[Outcome], show: bool) -> None:
    total = len(outcomes)
    answered = [o for o in outcomes if o.answer]
    errored = [o for o in outcomes if o.answer is None]
    uncited = [o for o in answered if not o.cited]
    invalid = [o for o in answered if o.invalid]
    hits = [o for o in answered if o.hit]

    def line(label: str, group: list, note: str = "") -> None:
        print(f"  {label:<22} {len(group):>3} / {total}  {len(group) / total:>5.0%}  {note}")

    print(f"\n{total} questions\n")
    line("answered", answered)
    line("failed", errored, "quota, timeout or no results")
    line("cited a source", [o for o in answered if o.cited])
    line("no citation", uncited, "refusal or ungrounded claim")
    line("invented a citation", invalid, "out of range")
    print()
    line("cited the EXPECTED doc", hits, "end-to-end quality")

    if errored:
        reasons = sorted({o.reason for o in errored})
        print(f"\n  failure reasons: {', '.join(reasons)}")

    if uncited:
        print("\n  answers without a citation:")
        for outcome in uncited[:5]:
            print(f"    - {outcome.query}")

    if invalid:
        print("\n  invented citations:")
        for outcome in invalid:
            print(f"    - {outcome.query}  cited {outcome.invalid}")

    if show:
        for outcome in outcomes:
            print(f"\n{'=' * 70}\nQ: {outcome.query}")
            print(outcome.answer or f"(no answer: {outcome.reason})")


def main() -> None:
    cap = int(sys.argv[sys.argv.index("--cap") + 1]) if "--cap" in sys.argv else 1
    limit = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else None

    cases = yaml.safe_load(GOLDEN_SET.read_text(encoding="utf-8"))[:limit]
    retriever = Retriever()

    print(f"model={llm.MODELS[0]}  max_per_source={cap}  questions={len(cases)}")
    outcomes = []
    for index, case in enumerate(cases, 1):
        outcomes.append(run_case(retriever, case, cap))
        print(f"\r  {index}/{len(cases)}", end="", flush=True)

    report(outcomes, show="--show" in sys.argv)


if __name__ == "__main__":
    main()
