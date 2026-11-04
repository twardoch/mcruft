#!/usr/bin/env bash
# this_file: install.sh
# Install the core, local engines, optional libraries and development tools system-wide.
set -euo pipefail
cd "$(dirname "$0")"
if [[ -d dist ]]; then
  set -- --find-links dist "$@"
fi
uv pip install --system --upgrade -e '.[all]' --no-config \
  -e packages/mcruft_vectorcraft -e packages/mcruft_deckcraft \
  -e packages/mcruft_photocraft -e packages/mcruft_pdfcraft \
  -e packages/mcruft_designcraft --group dev "$@"
