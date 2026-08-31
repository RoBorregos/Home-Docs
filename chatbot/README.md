# Docs chatbot

Semantic search and question answering over the MkDocs documentation in `docs/`.
Retrieval runs locally; only the written answer calls an external model.

## Architecture

```
docs/**/*.md
    │  chunker.py        split by heading, merge/split to size
    │  build_index.py    embed with all-MiniLM-L6-v2
    ▼
docs/assets/search/      index.json (metadata) + embeddings.bin (float32 matrix)
    │
    │  retrieval.py      dense + BM25, fused with RRF, historical docs demoted
    │  prompt.py         numbered excerpts, citation rules
    │  llm.py            Gemini Flash, with model fallback on 503
    ▼
api.py                   /search (fast) · /ask (answer) · /health
    ▲
    │  docs/assets/javascripts/chatbot.js
    └── widget: sources in ~100 ms, answer 4-35 s later
```

Two layers on purpose: if generation fails or the quota runs out, search keeps
working and the widget still shows the sources.

| File | Role |
|---|---|
| `chunker.py` | Markdown → 830 chunks with URL, heading path and year |
| `build_index.py` | Chunks → embeddings, writes the two artifacts |
| `retrieval.py` | Ranking: dense + BM25 + RRF + recency + one chunk per file |
| `prompt.py` | Builds the prompt; no LLM dependency, inspectable offline |
| `llm.py` | The only module that knows about Gemini |
| `api.py` | FastAPI wrapper over `Retriever` |
| `verify_index.py` | Checks the artifacts load and answer a query |
| `eval/` | 45-question golden set and the scoring harness |

## Setup

```bash
.venv/bin/pip install torch --index-url https://download.pytorch.org/whl/cpu
.venv/bin/pip install -r chatbot/requirements.txt
```

The CPU wheel is deliberate: the default one pulls ~2.5 GB of CUDA that 830
chunks do not need.

For answers, put a [Google AI Studio](https://aistudio.google.com/apikey) key in
`.env` at the repository root (already gitignored):

```
GEMINI_API_KEY=...
```

`llm.py` loads it on import, so no flags or exports are needed. Search works
without a key.

## Running locally

Build the index once, then start both servers in separate terminals:

```bash
.venv/bin/python -m chatbot.build_index                                    # ~25 s
HF_HUB_OFFLINE=1 .venv/bin/uvicorn chatbot.api:app --reload --port 8001    # backend
.venv/bin/python -m mkdocs serve                                           # docs on :8000
```

Open <http://127.0.0.1:8000> — the "Ask the docs" button appears only when the
backend answers `/health`, so the published site never shows a dead button.

`HF_HUB_OFFLINE=1` skips a model-update check that costs ~3.5 s per start.
Rebuild the index whenever the documentation changes.

## Other commands

```bash
.venv/bin/python -m chatbot.chunker              # chunk stats, no index needed
.venv/bin/python -m chatbot.verify_index         # artifacts load and rank correctly
.venv/bin/python -m chatbot.prompt "a question"  # the exact prompt, no API call
.venv/bin/python -m chatbot.eval.evaluate        # recall@k and MRR per configuration
.venv/bin/python -m chatbot.eval.answers         # citation validity and answer quality
```

```bash
curl -s -X POST localhost:8001/ask -H 'Content-Type: application/json' \
  -d '{"query":"how do I install and configure GPD?"}' | python -m json.tool
```

Drop the `| python -m json.tool` when debugging: it hides the real error if the
response is not JSON.

## Current numbers

Retrieval (`eval/evaluate.py`): **R@1 0.64 · R@3 0.89 · R@5 0.96 · MRR 0.777**.

Answers (`eval/answers.py`, one Gemini call per question): **100% answered ·
98% cited a source · 0% invented citations · 87% cited the expected document**.

The two disagree on `MAX_PER_SOURCE`, and the second wins. File-level recall
cannot see a second chunk from an already-counted file, but that chunk is often
what completes the answer: 87% against 73% at a cap of 1. Rerun both after
changing the chunker, the model, or any ranking parameter.

The golden set was written by reading the documentation, so it is a good tool for
comparing configurations and a poor estimate of real-world quality. Extend it
with questions the team actually asks.

## Tests

The repository's CI runs `pytest` from the root, and `pytest.ini` limits it to
`tests/` so these modules and their dependencies stay out of it.
