"""Check that the built index is loadable and answers a query.

Loads the artifacts from disk the way the browser will, then runs one search.

Usage (from the repository root):
    .venv/bin/python -m chatbot.verify_index
"""

import json
from pathlib import Path

import numpy as np
from chatbot import embedding

INDEX_DIR = Path("docs/assets/search")
QUERY = "which camera does the robot use?"
TOP_K = 3


def load_index(index_dir: Path) -> tuple[dict, np.ndarray]:
    """Read the metadata and the embedding matrix, failing loudly if they disagree."""
    index = json.loads((index_dir / "index.json").read_text(encoding="utf-8"))
    raw = (index_dir / "embeddings.bin").read_bytes()

    expected = index["count"] * index["dim"] * 4
    if len(raw) != expected:
        raise SystemExit(
            f"Stale index: embeddings.bin is {len(raw)} bytes, "
            f"expected {expected}. Rerun build_index.py."
        )

    matrix = np.frombuffer(raw, dtype=np.float32).reshape(index["count"], index["dim"])
    return index, matrix


def main() -> None:
    index, matrix = load_index(INDEX_DIR)
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
