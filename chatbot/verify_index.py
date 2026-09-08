"""Check that the built index is loadable and answers a query.

Loads the artifacts from disk the way the browser will, then runs one search.

Usage (from the repository root):
    .venv/bin/python -m chatbot.verify_index
"""

import numpy as np
from chatbot import embedding
from chatbot.retrieval import load_index

QUERY = "which camera does the robot use?"
TOP_K = 3


def main() -> None:
    index, matrix = load_index()
    print(f"Loaded {matrix.shape[0]} x {matrix.shape[1]} ({index['model']})")
    print(f"First vector norm: {np.linalg.norm(matrix[0]):.4f} (expected 1.0)")

    query_vector = embedding.encode_one(QUERY)
    scores = matrix @ query_vector   # normalised vectors: dot product is cosine

    print(f"\nQuery: {QUERY}")
    for rank, i in enumerate(np.argsort(-scores)[:TOP_K], 1):
        chunk = index["chunks"][i]
        print(f"  {rank}. {scores[i]:.3f}  {chunk['source']}")


if __name__ == "__main__":
    main()
