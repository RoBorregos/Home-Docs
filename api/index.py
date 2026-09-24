"""Vercel entrypoint.

Static hosts serve the built site and route /api/* to a function in this
directory, so the app is exposed here as well as in asgi.py at the root.
"""

import sys
from pathlib import Path

# The project root is not on sys.path when the host imports this file directly.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from chatbot.api import app

__all__ = ["app"]
