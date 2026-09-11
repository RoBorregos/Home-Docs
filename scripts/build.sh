#!/usr/bin/env bash
# Build everything a deployment needs: the rendered site, the embedding model
# and the search index.
#
# Model and index are built here rather than committed, so no binaries live in
# git and no host has to download them at runtime.
set -euo pipefail

echo "==> mkdocs"
pip install --quiet -r requirements.txt
mkdocs build --strict

echo "==> chatbot dependencies"
pip install --quiet -r chatbot/requirements.txt

echo "==> embedding model + index"
python -m chatbot.build_index

echo "==> bundle contents"
du -sh chatbot/models chatbot/index site
