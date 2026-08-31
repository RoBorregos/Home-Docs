# Docs chatbot

Semantic search and question answering over the MkDocs documentation in `docs/`.
Retrieval runs locally; only the written answer calls an external model.

## Architecture

```
docs/**/*.md
    │  chunker.py        split by heading, merge/split to size
    │  build_index.py    embed with all-MiniLM-L6-v2
    ▼
chatbot/index/           index.json (metadata) + embeddings.bin (float32 matrix)
    │
    │  retrieval.py      dense + BM25, fused with RRF, historical docs demoted
    │  prompt.py         numbered excerpts, citation rules
    │  llm.py            the LLM client, with model fallback when one is busy
    ▼
api.py                   /api/search (fast) · /api/ask (answer) · /api/health
    ▲                        an ASGI app; asgi.py exposes it for any host
    ▲
    │  docs/assets/javascripts/chatbot.js
    └── widget: sources in ~100 ms, answer 4-35 s later
```

Two layers on purpose: if generation fails or the quota runs out, search keeps
working and the widget still shows the sources.

| File | Role |
|---|---|
| `chunker.py` | Markdown → 830 chunks with URL, heading path and year |
| `embedding.py` | The embedding model (fastembed/ONNX), isolated in one function |
| `build_index.py` | Chunks → embeddings, writes the two artifacts |
| `retrieval.py` | Ranking: dense + BM25 + RRF + recency + one chunk per file |
| `prompt.py` | Builds the prompt; no LLM dependency, inspectable offline |
| `llm.py` | The only module that names a provider (currently Gemini) |
| `api.py` | FastAPI wrapper over `Retriever` |
| `verify_index.py` | Checks the artifacts load and answer a query |
| `eval/` | 45-question golden set and the scoring harness |

## Setup

```bash
.venv/bin/pip install -r chatbot/requirements.txt
```

fastembed runs the model through ONNX with no torch: 250 MB resident instead of
497 MB, which is what lets the API fit a serverless function.

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
curl -s -X POST localhost:8001/api/ask -H 'Content-Type: application/json' \
  -d '{"query":"how do I install and configure GPD?"}' | python -m json.tool
```

Drop the `| python -m json.tool` when debugging: it hides the real error if the
response is not JSON.

## Deployment

The API is a plain ASGI app exposed as `app` in `asgi.py`, so any host that runs
ASGI can serve it. Two things hold for every target:

- `scripts/build.sh` produces everything a deployment needs: the rendered site,
  the model in `chatbot/models/`, and the index in `chatbot/index/`. All three
  are gitignored, so no binaries live in the repository.
- `GEMINI_API_KEY` comes from the environment. Search works without it; only the
  written answer needs it.

Serving `/api/*` from the same origin as the docs removes the need for CORS. The
widget already assumes that: it calls `/api` in production and
`localhost:8001/api` when the page is served from localhost.

**Container** — works on Render, Fly, Railway, Cloud Run or a plain VM:

```bash
docker build -t home-docs-chatbot .
docker run -p 8000:8000 -e GEMINI_API_KEY=... home-docs-chatbot
```

**Vercel** — `vercel.json` is the adapter: it runs `scripts/build.sh`, serves
`site/` statically and routes `/api/*` to the function. It is the only
Vercel-specific file; nothing else in the repository refers to a platform.

## Tests

The repository's CI runs `pytest` from the root, and `pytest.ini` limits it to
`tests/` so these modules and their dependencies stay out of it.
