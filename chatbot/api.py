"""HTTP API for documentation search.

A thin layer over Retriever: it owns no ranking logic of its own.

Usage (from the repository root):
    .venv/bin/uvicorn chatbot.api:app --reload --port 8001

Routes live under /api so the static site and this function can share a
domain on Vercel, which removes the need for CORS in production.

Port 8001 because `mkdocs serve` already occupies 8000.
"""

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from chatbot import llm
from chatbot.prompt import build_prompt
from chatbot.retrieval import Result, Retriever

log = logging.getLogger(__name__)

SNIPPET_CHARS = 300

# localhost and 127.0.0.1 are distinct origins: allowing only one breaks CORS.
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

# Loaded once at import: building the index takes seconds, too slow per request.
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


@app.get("/api/health")
def health() -> dict:
    """Liveness probe. The widget calls this before rendering its button."""
    return {"status": "ok", "chunks": len(retriever.chunks)}


@app.post("/api/search", response_model=SearchResponse)
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

def to_hit(result: Result) -> SearchHit:
    return SearchHit(
        url=result.chunk["url"],
        breadcrumb=" > ".join(result.chunk["heading_path"]),
        source=result.chunk["source"],
        snippet=snippet_of(result.chunk),
        year=result.chunk["year"],
        score=round(result.score, 5),
    )

class AskRequest(BaseModel):
    query: str = Field(min_length=1, max_length=500)
    top_k: int = Field(default=5, ge=1, le=20)

class AskResponse(BaseModel):
    query:str
    answer:str | None
    reason: str | None
    results: list[SearchHit]

@app.post("/api/ask", response_model=AskResponse)
def ask(request: AskRequest) -> AskResponse:
    results = retriever.search(request.query, top_k=request.top_k)

    if not results:
        return AskResponse(
            query=request.query,
            answer=None,
            reason="no_results",
            results=[],
        )

    hits = [to_hit(result) for result in results]

    try:
        system, user = build_prompt(request.query, results)
        answer = llm.generate(system, user)
    except llm.LLMUnavailable as e:
        # The client only sees `reason`; keep the provider's message here.
        log.warning("generation failed (%s): %s", e.reason, e)
        return AskResponse(
            query=request.query,
            answer=None,
            reason=e.reason,
            results=hits,
        )

    return AskResponse(
        query=request.query,
        answer=answer,
        reason=None,
        results=hits,
    )