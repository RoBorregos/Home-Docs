"""The embedding model, isolated behind one function.

fastembed runs the ONNX export of all-MiniLM-L6-v2 with no torch and no
transformers: 243 MB resident against 497 MB for the PyTorch stack, which is
what makes the service fit a 512 MB host.

Its vectors are identical to sentence-transformers' (cosine 1.000000 on the same
text), so an index built with either backend is readable by the other.
"""

import os
from pathlib import Path

import numpy as np
from fastembed import TextEmbedding

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Kept inside the project so the build can download it once and ship it in the
# deployment bundle; a serverless filesystem is read-only except /tmp.
CACHE_DIR = Path(os.environ.get("FASTEMBED_CACHE", Path(__file__).resolve().parent / "models"))

_model: TextEmbedding | None = None


def model() -> TextEmbedding:
    """Built on first use; loading costs a couple of seconds."""
    global _model
    if _model is None:
        _model = TextEmbedding(MODEL_NAME, cache_dir=str(CACHE_DIR))
    return _model


def encode(texts: list[str]) -> np.ndarray:
    """Encode texts into a normalised float32 matrix (n_texts x 384)."""
    return np.asarray(list(model().embed(texts)), dtype=np.float32)


def encode_one(text: str) -> np.ndarray:
    """Encode a single string into a 384-vector."""
    return encode([text])[0]
