"""Hybrid retrieval over the documentation index.

Combines dense (embedding) and lexical (BM25) search with reciprocal rank
fusion, demotes historical documents, and caps results per source file.

Usage (from the repository root):
    .venv/bin/python -m chatbot.retrieval "how do I set up the arm?"
"""

import json
import math
import re
import sys
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
from chatbot import embedding

# Resolved from this file, not the working directory: retrieval.py is imported
# by the API, which may be started from anywhere.
REPO_ROOT = Path(__file__).resolve().parent.parent
INDEX_DIR = REPO_ROOT / "chatbot/index"
CANDIDATES = 50          # dense candidates entering the fusion
LEXICAL_CANDIDATES = 50  # BM25 candidates entering the fusion
LEXICAL_WEIGHT = 0.25    # measured optimum; at 1.0 BM25 drowns out the dense ranking
RRF_K = 60               # rank damping; 60 comes from the original RRF paper
HALF_LIFE_YEARS = 2      # a document this old scores half as much
MAX_PER_SOURCE = 2       # answer-level eval: 87% vs 73% at 1 (file-level recall cannot see this)

TOKEN = re.compile(r"[a-z0-9]+")

def tokenise(text: str) -> list[str]:
    """Lowercase and split on non-alphanumeric characters."""
    return TOKEN.findall(text.lower())

class BM25:
    """Lexical ranker over an inverted index.

    k1 controls how fast repeated terms stop adding value; b controls how much
    document length is discounted.
    """

    def __init__(self, documents: list[list[str]], k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.n_docs = len(documents)
        self.doc_len = np.array([len(doc) for doc in documents], dtype=np.float32)
        self.avg_len = float(self.doc_len.mean())

        # Inverted index: term -> {doc_id: how many times it occurs}
        self.postings: dict[str, dict[int, int]] = defaultdict(dict)
        for doc_id, tokens in enumerate(documents):
            for term, freq in Counter(tokens).items():
                self.postings[term][doc_id] = freq

        # Rare terms carry more signal: this is what lets "zed2" outweigh "the".
        self.idf = {
            term: math.log((self.n_docs - len(posting) + 0.5) / (len(posting) + 0.5) + 1)
            for term, posting in self.postings.items()
        }

    def scores(self, query_tokens: list[str]) -> np.ndarray:
        scores = np.zeros(self.n_docs, dtype=np.float32)
        for term in query_tokens:
            posting = self.postings.get(term)
            if not posting:
                continue
            idf = self.idf[term]
            for doc_id, freq in posting.items():
                length_norm = 1 - self.b + self.b * self.doc_len[doc_id] / self.avg_len
                scores[doc_id] += idf * (freq * (self.k1 + 1) / (freq + self.k1 * length_norm))

        return scores

def reciprocal_rank_fusion(
    rankings: list[list[int]],
    k: float = RRF_K,
    weights: list[float] | None = None,
) -> dict[int, float]:
    """Merge ranked lists by position rather than by score.

    Dense scores (~0.5) and BM25 scores (~12) live on different scales that
    shift per query, so normalising them is fragile. Ranks are scale-free.

    `weights` lets one ranker contribute less than another, which matters when
    a query has no distinctive terms and the lexical ranking is close to noise.
    """
    if weights is None:
        weights = [1.0] * len(rankings)

    fused: dict[int, float] = defaultdict(float)
    for ranking, weight in zip(rankings, weights):
        for rank, doc_id in enumerate(ranking):
            fused[doc_id] += weight / (k + rank + 1)

    return fused

def recency_weight(year: int | None, latest: int, half_life: float = HALF_LIFE_YEARS) -> float:
    """Demote dated documents. Undated ones live under development/ and are current."""
    if year is None:
        return 1.0
    return 0.5 ** ((latest - year) / half_life)


def cap_per_source(
    ranked: list[tuple[int, float]], chunks: list[dict], limit: int = MAX_PER_SOURCE
) -> list[tuple[int, float]]:
    """Keep at most `limit` chunks per source file, preserving order."""
    seen: Counter[str] = Counter()
    kept = []
    for doc_id, score in ranked:
        source = chunks[doc_id]["source"]
        if seen[source] >= limit:
            continue
        seen[source] += 1
        kept.append((doc_id, score))
    return kept

@dataclass
class Result:
    chunk: dict
    score: float
    dense_rank: int | None
    lexical_rank: int | None

class Retriever:
    """Loads the index once and answers many queries."""

    def __init__(self, index_dir: Path = INDEX_DIR):
        index = json.loads((index_dir / "index.json").read_text(encoding="utf-8"))
        raw = (index_dir / "embeddings.bin").read_bytes()

        self.chunks = index["chunks"]
        self.matrix = np.frombuffer(raw, dtype=np.float32).reshape(index["count"], index["dim"])
        self.bm25 = BM25([tokenise(chunk["text"]) for chunk in self.chunks])
        self.latest_year = max((c["year"] for c in self.chunks if c["year"]), default=0)

    def search(
        self,
        query: str,
        top_k: int = 5,
        *,
        use_dense: bool = True,
        lexical_weight: float = LEXICAL_WEIGHT,
        lexical_candidates: int = LEXICAL_CANDIDATES,
        half_life: float | None = HALF_LIFE_YEARS,
        max_per_source: int | None = MAX_PER_SOURCE,
    ) -> list[Result]:
        """Retrieve chunks for a query.

        The keyword arguments exist so the evaluation harness can ablate each
        stage; the defaults are the production configuration.
        """
        query_vector = embedding.encode_one(query)
        dense = self.matrix @ query_vector
        dense_ids = np.argsort(-dense)[:CANDIDATES].tolist() if use_dense else []

        # Skipped entirely at zero weight: scoring BM25 and discarding it costs
        # a full pass over the postings on every query.
        lexical_ids: list[int] = []
        if lexical_weight > 0:
            lexical = self.bm25.scores(tokenise(query))
            lexical_ids = [
                i for i in np.argsort(-lexical)[:lexical_candidates] if lexical[i] > 0
            ]

        fused = reciprocal_rank_fusion(
            [dense_ids, lexical_ids], weights=[1.0, lexical_weight]
        )

        weighted = [
            (
                doc_id,
                score
                * (
                    1.0
                    if half_life is None
                    else recency_weight(self.chunks[doc_id]["year"], self.latest_year, half_life)
                ),
            )
            for doc_id, score in fused.items()
        ]

        ranked = sorted(weighted, key=lambda item: -item[1])
        if max_per_source is not None:
            ranked = cap_per_source(ranked, self.chunks, max_per_source)

        dense_pos = {doc_id: r for r, doc_id in enumerate(dense_ids, 1)}
        lexical_pos = {doc_id: r for r, doc_id in enumerate(lexical_ids, 1)}

        return [
            Result(
                chunk=self.chunks[doc_id],
                score=score,
                dense_rank=dense_pos.get(doc_id),
                lexical_rank=lexical_pos.get(doc_id),
            )
            for doc_id, score in ranked[:top_k]
        ]

def main() -> None:
    query = " ".join(sys.argv[1:]) or "which camera does the robot use?"
    retriever = Retriever()

    print(f"Query: {query}\n")
    for rank, result in enumerate(retriever.search(query), 1):
        chunk = result.chunk
        year = f" [{chunk['year']}]" if chunk["year"] else ""
        origin = f"dense #{result.dense_rank or '-'}, bm25 #{result.lexical_rank or '-'}"
        print(f"{rank}. {result.score:.4f}  {chunk['source']}{year}")
        print(f"   {' > '.join(chunk['heading_path'])[:60]}")
        # print(f"   {chunk['text'].replace('\\n', ' ')}")
        print(f"   {origin}\n")


if __name__ == "__main__":
    main()