"""Gemini client for the answering layer.

The only module that names the provider. Callers use generate() and
is_configured(); swapping providers means rewriting this file and nothing else.

Needs GEMINI_API_KEY in the environment. The module still imports without it, so
search keeps working when generation cannot.
"""

import os
import time
from pathlib import Path

import httpx
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

# --- model chain ------------------------------------------------------------

MODELS = [
    "gemini-3.5-flash-lite",
    "gemini-3.5-flash",
    "gemini-3.1-flash-lite",
]

# Failures worth retrying on the next model rather than surfacing to the user.
TRANSIENT = {"provider_error", "quota_exceeded", "timeout"}


# --- generation settings ----------------------------------------------------

# One deadline for the whole chain; must stay under the host's request cap.
REQUEST_BUDGET_MS = int(os.environ.get("REQUEST_BUDGET_MS", 90_000))

# An even slice each, so the last model still gets a real turn.
CALL_TIMEOUT_MS = REQUEST_BUDGET_MS // len(MODELS)

MAX_OUTPUT_TOKENS = 1500  # covers internal reasoning AND the visible answer
TEMPERATURE = 0.2


# --- failures ---------------------------------------------------------------

class LLMUnavailable(Exception):

    def __init__(self, reason: str, detail: str = ""):
        super().__init__(detail or reason)
        self.reason = reason


# --- client -----------------------------------------------------------------

def is_configured() -> bool:
    return bool(os.environ.get("GEMINI_API_KEY"))

_client: genai.Client | None = None

def client() -> genai.Client:
    global _client
    if _client is None:
        _client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    return _client

def classify(error: Exception) -> str:
    # By type: a client-side timeout has no response whose message we could read.
    if isinstance(error, httpx.TimeoutException):
        return "timeout"

    code = getattr(error, "code", None)
    if code == 429:
        return "quota_exceeded"
    if code == 504:
        return "timeout"   # gateway deadline, not a provider fault
    if isinstance(code, int) and 500 <= code < 600:
        return "provider_error"

    message = str(error).lower()
    if "429" in message or "quota" in message or "resource_exhausted" in message:
        return "quota_exceeded"
    if "timeout" in message or "deadline" in message:
        return "timeout"
    return "error"

# --- the call ---------------------------------------------------------------

def config_for(system: str, timeout_ms: int) -> types.GenerateContentConfig:
    """Per attempt, because the timeout shrinks as the shared budget is spent."""
    return types.GenerateContentConfig(
        system_instruction=system,
        max_output_tokens=MAX_OUTPUT_TOKENS,
        temperature=TEMPERATURE,
        http_options=types.HttpOptions(timeout=timeout_ms),
    )


def generate(system: str, user: str) -> str:
    if not is_configured():
        raise LLMUnavailable("not_configured", "GEMINI_API_KEY not set")

    deadline = time.monotonic() + REQUEST_BUDGET_MS / 1000
    last: LLMUnavailable | None = None

    for model in MODELS:
        remaining_ms = int((deadline - time.monotonic()) * 1000)
        if remaining_ms <= 0:
            # Surface the failure that spent the budget, not the budget itself.
            raise last or LLMUnavailable("timeout", "budget spent before any model answered")

        try:
            response = client().models.generate_content(
                model=model,
                contents=user,
                config=config_for(system, min(CALL_TIMEOUT_MS, remaining_ms)),
            )
            break
        except Exception as e:
            last = LLMUnavailable(classify(e), f"{model}: {e}")
            if last.reason not in TRANSIENT:
                raise last from e      # a bad request will fail on every model
    else:
        raise last                     # every model was busy or out of quota

    text = (response.text or "").strip()
    if not text:
        finish = response.candidates[0].finish_reason if response.candidates else None
        reason = "truncated" if finish and "MAX_TOKENS" in str(finish) else "empty_response"
        raise LLMUnavailable(reason, f"finish_reason={finish}")

    return text