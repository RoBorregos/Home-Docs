"""ASGI entrypoint.

A standard ASGI application named `app` at the project root, which is what every
host looks for — uvicorn, gunicorn, Docker, or a platform that autodetects one.
Keeping it here means no deployment target needs its own configuration to find it.

    uvicorn asgi:app --port 8001
"""

from chatbot.api import app

__all__ = ["app"]
