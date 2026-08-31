"""Gemini client for the answering layer.

The only module that names the provider. Callers use generate() and
is_configured(); swapping providers means rewriting this file and nothing else.

Needs GEMINI_API_KEY in the environment. The module still imports without it, so
search keeps working when generation cannot.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

# --- model chain ------------------------------------------------------------

MODELS = [
    "gemini-3.5-flash",       # ~4.6s, primary
    "gemini-3.5-flash-lite",  # ~1.1s, faster, used when the primary is busy
    "gemini-3.1-flash-lite",  # last resort
]

# Failures worth retrying on the next model rather than surfacing to the user.
TRANSIENT = {"provider_error", "quota_exceeded", "timeout"}


# --- generation settings ----------------------------------------------------

TIMEOUT_MS = 60_000  # 60s: a thinking model over ~1.3k tokens of context
                     # needs far longer than a trivial prompt suggests
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

def generate(system: str, user: str) -> str:
    if not is_configured():
        raise LLMUnavailable("GEMINI_API_KEY not set")

    config = types.GenerateContentConfig(
        system_instruction=system,
        max_output_tokens=MAX_OUTPUT_TOKENS,
        temperature=TEMPERATURE,
        http_options=types.HttpOptions(timeout=TIMEOUT_MS),
    )

    last: LLMUnavailable | None = None
    for model in MODELS:
        try:
            response = client().models.generate_content(
                model=model, contents=user, config=config
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