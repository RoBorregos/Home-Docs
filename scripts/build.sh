#!/usr/bin/env bash
# Build everything a deployment needs: the rendered site and the search index.
#
# Dependencies are expected to be installed already: hosts install them from
# requirements.txt themselves, and their Python is often not pip-writable.
#
# Model and index are built here rather than committed, so no binaries live in
# git and no host has to download them at runtime.
set -euo pipefail

# Run as modules: hosts install the entry-point scripts outside the PATH.
PYTHON="${PYTHON:-$(command -v python3 || command -v python)}"

echo "==> mkdocs"
"$PYTHON" -m mkdocs build --strict

echo "==> embedding model + index"
"$PYTHON" -m chatbot.build_index

echo "==> bundle contents"
du -sh chatbot/models chatbot/index site
