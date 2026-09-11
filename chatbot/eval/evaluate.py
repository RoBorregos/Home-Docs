"""Measure retrieval quality against the golden set.

Reports recall@k and MRR for several configurations so that tuning decisions
rest on numbers rather than on a single hand-picked query.

Usage (from the repository root):
    .venv/bin/python -m chatbot.eval.evaluate          # compare configurations
    .venv/bin/python -m chatbot.eval.evaluate --misses # show failing queries
"""

import sys
from dataclasses import dataclass
from pathlib import Path

import yaml

from chatbot.retrieval import Retriever

GOLDEN_SET = Path(__file__).parent / "golden_set.yaml"
CUTOFFS = (1, 3, 5)
TOP_K = max(CUTOFFS)


@dataclass
class Scorecard:
    name: str
    recall: dict[int, float]
    mrr: float
    misses: list[tuple[str, list[str]]]


def first_hit_rank(sources: list[str], expected: list[str]) -> int | None:
    """Rank (1-based) of the first retrieved source that is expected."""
    for rank, source in enumerate(sources, start=1):
        if source in expected:
            return rank
    return None


def evaluate(retriever: Retriever, cases: list[dict], name: str, **options) -> Scorecard:
    hits = {k: 0 for k in CUTOFFS}
    reciprocal_ranks = []
    misses: list[tuple[str, list[str]]] = []

    for case in cases:
        results = retriever.search(case["query"], top_k=TOP_K, **options)

        # Recall is measured per source file, which is what the golden set names.
        sources: list[str] = []
        for result in results:
            if result.chunk["source"] not in sources:
                sources.append(result.chunk["source"])

        rank = first_hit_rank(sources, case["expect"])
        reciprocal_ranks.append(1 / rank if rank else 0.0)
        for k in CUTOFFS:
            if rank and rank <= k:
                hits[k] += 1
        if rank is None:
            misses.append((case["query"], sources[:3]))

    total = len(cases)
    return Scorecard(
        name=name,
        recall={k: hits[k] / total for k in CUTOFFS},
        mrr=sum(reciprocal_ranks) / total,
        misses=misses,
    )


def configurations() -> list[tuple[str, dict]]:
    """Baselines, then the lexical weight and candidate count swept.

    Everything below the baselines holds recency and the cap fixed, so any
    difference is attributable to how much BM25 is allowed to contribute.
    """
    base = dict(half_life=2, max_per_source=1)
    configs: list[tuple[str, dict]] = [
        ("dense only", dict(lexical_weight=0, half_life=None, max_per_source=None)),
        ("lexical only", dict(use_dense=False, lexical_weight=1.0,
                              half_life=None, max_per_source=None)),
        ("dense + recency + cap", dict(base, lexical_weight=0)),
    ]

    for weight in (0.15, 0.25, 0.5, 0.75, 1.0):
        configs.append((f"  + bm25 w={weight}", dict(base, lexical_weight=weight)))

    for n in (5, 10, 20):
        configs.append(
            (f"  + bm25 w=0.5 top{n}", dict(base, lexical_weight=0.5, lexical_candidates=n))
        )
    return configs


def main() -> None:
    cases = yaml.safe_load(GOLDEN_SET.read_text(encoding="utf-8"))
    retriever = Retriever()

    print(f"{len(cases)} queries\n")
    header = f"{'configuration':<24}" + "".join(f"{'R@' + str(k):>8}" for k in CUTOFFS) + f"{'MRR':>8}"
    print(header)
    print("-" * len(header))

    scorecards = []
    for name, options in configurations():
        card = evaluate(retriever, cases, name, **options)
        scorecards.append(card)
        row = "".join(f"{card.recall[k]:>8.2f}" for k in CUTOFFS)
        print(f"{card.name:<24}{row}{card.mrr:>8.3f}")

    best = max(scorecards, key=lambda c: c.mrr)
    print(f"\nBest MRR: {best.name} ({best.mrr:.3f})")

    if "--misses" in sys.argv:
        print(f"\nQueries {best.name} never answered ({len(best.misses)}):")
        for query, got in best.misses:
            print(f"\n  {query}")
            for source in got:
                print(f"    got: {source}")


if __name__ == "__main__":
    main()
