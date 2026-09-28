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

# Keep the downloader's chunk cache out of the project: it holds a second copy.
export HF_XET_CACHE="${TMPDIR:-/tmp}/hf-xet-cache"

echo "==> embedding model + index"
"$PYTHON" -m chatbot.build_index

# The hub cache keeps a second copy of every file (blobs, and the xet chunk cache
# when the host downloads through it). Only the snapshot is needed at runtime.
echo "==> flattening the model cache"
find chatbot/models -type l -exec sh -c 'cp --remove-destination "$(readlink -f "$1")" "$1"' _ {} \;
find chatbot/models -mindepth 1 -type f \
  ! -path '*/snapshots/*' ! -path '*/refs/*' ! -name files_metadata.json -delete
find chatbot/models -mindepth 1 -type d -empty -delete

echo "==> bundle contents"
du -sh chatbot/models/* chatbot/index site
