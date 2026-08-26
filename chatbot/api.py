"""HTTP API for documentation search.

A thin layer over Retriever: it owns no ranking logic of its own.

Usage (from the repository root):
    .venv/bin/uvicorn chatbot.api:app --reload --port 8001

Port 8001 because `mkdocs serve` already occupies 8000.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from chatbot.retrieval import Retriever

SNIPPET_CHARS = 300

# Both spellings are distinct origins to a browser, and mkdocs serve prints the
# 127.0.0.1 one while people usually type localhost. Allowing only one is a
# classic afternoon lost to CORS.
ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app = FastAPI(title="Home-Docs search", docs_url="/docs")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

# Loaded once at import time: building the BM25 index and loading the embedding
# model takes seconds, which would be unusable per request.
retriever = Retriever()


class SearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=500)
    top_k: int = Field(default=5, ge=1, le=20)


class SearchHit(BaseModel):
    url: str
    breadcrumb: str
    source: str
    snippet: str
    year: int | None
    score: float


class SearchResponse(BaseModel):
    query: str
    results: list[SearchHit]


def snippet_of(chunk: dict) -> str:
    """Trim a chunk for display.

    Done server-side so a search does not ship five full 2 KB chunks over the
    wire to render 300 characters. The breadcrumb is stripped because the UI
    already shows it as its own line.
    """
    body = chunk["text"]
    breadcrumb = " > ".join(chunk["heading_path"])
    if breadcrumb and body.startswith(breadcrumb):
        body = body[len(breadcrumb):]

    body = " ".join(body.split())
    if len(body) <= SNIPPET_CHARS:
        return body
    return body[:SNIPPET_CHARS].rsplit(" ", 1)[0] + "..."


@app.get("/health")
def health() -> dict:
    """Liveness probe. The widget calls this before rendering its button."""
    return {"status": "ok", "chunks": len(retriever.chunks)}


@app.post("/search", response_model=SearchResponse)
def search(request: SearchRequest) -> SearchResponse:
    results = retriever.search(request.query, top_k=request.top_k)
    return SearchResponse(
        query=request.query,
        results=[
            SearchHit(
                url=result.chunk["url"],
                breadcrumb=" > ".join(result.chunk["heading_path"]),
                source=result.chunk["source"],
                snippet=snippet_of(result.chunk),
                year=result.chunk["year"],
                score=round(result.score, 5),
            )
            for result in results
        ],
    )
