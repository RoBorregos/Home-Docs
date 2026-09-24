"""Request limits for the answering endpoint.

Retrieval stays open; only generation is limited, because every generated
answer spends a daily quota shared by the whole team that one loop can exhaust.

State lives in the process. A container enforces these exactly; several
serverless instances each enforce their own share, so treat this as a brake on
runaway scripts and casual abuse, not as a security boundary. Stopping a
distributed flood is the edge firewall's job.
"""

import os
import time
from collections import deque
from datetime import date

PER_CLIENT_REQUESTS = 10
PER_CLIENT_WINDOW_S = 60

# Depends on the provider plan, so it comes from the environment.
DAILY_ANSWERS = int(os.environ.get("DAILY_ANSWERS", 400))

# Bounds memory when addresses rotate faster than their windows expire.
MAX_TRACKED_CLIENTS = 10_000


class RateLimiter:
    """A sliding window per client, under a global daily ceiling."""

    def __init__(
        self,
        per_client: int = PER_CLIENT_REQUESTS,
        window_s: float = PER_CLIENT_WINDOW_S,
        daily: int = DAILY_ANSWERS,
    ):
        self.per_client = per_client
        self.window_s = window_s
        self.daily = daily
        self._seen: dict[str, deque[float]] = {}
        self._day = date.today()
        self._today = 0

    @property
    def answers_today(self) -> int:
        self._roll_day()
        return self._today

    def check(self, client: str) -> str | None:
        """Return the reason to refuse, or None to allow and count the request."""
        self._roll_day()
        if self._today >= self.daily:
            return "daily_cap"

        now = time.monotonic()
        hits = self._seen.setdefault(client, deque())
        while hits and now - hits[0] > self.window_s:
            hits.popleft()

        if len(hits) >= self.per_client:
            return "rate_limited"

        if len(self._seen) > MAX_TRACKED_CLIENTS:
            self._evict(now)

        hits.append(now)
        self._today += 1
        return None

    def _roll_day(self) -> None:
        """Reset the daily count when the date changes."""
        today = date.today()
        if today != self._day:
            self._day, self._today = today, 0

    def _evict(self, now: float) -> None:
        """Forget clients whose window has fully expired."""
        stale = [
            client
            for client, hits in self._seen.items()
            if not hits or now - hits[-1] > self.window_s
        ]
        for client in stale:
            del self._seen[client]
