"""Build the search index: embed documentation chunks and write the artifacts.

Usage (from the repository root):
    .venv/bin/python -m chatbot.build_index

Outputs:
    chatbot/index/index.json      chunk metadata
    chatbot/index/embeddings.bin  raw float32 matrix (N x DIM)
"""

import json
from dataclasses import asdict
from pathlib import Path

import numpy as np

from chatbot import embedding
from chatbot.chunker import Chunk, chunk_file

DOCS_ROOT = Path("docs")
OUT_DIR = Path("chatbot/index")


def collect_chunks(docs_root: Path) -> list[Chunk]:
    """Walk the documentation tree in a deterministic order."""
    chunks: list[Chunk] = []
    for path in sorted(docs_root.rglob("*.md")):
        chunks.extend(chunk_file(path, docs_root))
    return chunks


def embed(chunks: list[Chunk]) -> np.ndarray:
    """Encode chunk texts into a normalised float32 matrix."""
    return embedding.encode([chunk.text for chunk in chunks])


def write_artifacts(out_dir: Path, chunks: list[Chunk], matrix: np.ndarray) -> None:
    """Write chunk metadata and the embedding matrix as a matched pair."""
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "embeddings.bin").write_bytes(matrix.tobytes())

    # The header lets a reader reject a stale index instead of trusting it.
    index = {
        "model": embedding.MODEL_NAME,
        "dim": int(matrix.shape[1]),
        "count": len(chunks),
        "chunks": [asdict(chunk) for chunk in chunks],
    }
    (out_dir / "index.json").write_text(
        json.dumps(index, ensure_ascii=False), encoding="utf-8"
    )


def main() -> None:
    chunks = collect_chunks(DOCS_ROOT)
    if not chunks:
        raise SystemExit(f"No chunks found under {DOCS_ROOT}/")

    print(f"Embedding {len(chunks)} chunks with {embedding.MODEL_NAME}...")
    matrix = embed(chunks)
    write_artifacts(OUT_DIR, chunks, matrix)

    written = ("index.json", "embeddings.bin")
    size_kb = sum((OUT_DIR / name).stat().st_size for name in written) / 1024
    print(f"Wrote {len(chunks)} x {matrix.shape[1]} to {OUT_DIR}/ ({size_kb:.0f} KB)")


if __name__ == "__main__":
    main()
