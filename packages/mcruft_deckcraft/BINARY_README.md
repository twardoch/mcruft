<!--
---
this_file: packages/mcruft_deckcraft/BINARY_README.md
---
-->

# mcruft-deckcraft-bin

The DeckCraft command-line engine bundled for mcruft on Apple Silicon.
Convert PPTX and DeckCraft files, export slides as PDF/PNG and build image-based PPTX decks.

## Install and use

Python 3.12+, macOS 11+ and arm64 are required. Install the adapter and its bundle together:

```bash
uv pip install 'mcruft-deckcraft[bundled]'
```

mcruft discovers this wheel automatically. It contains `deckcraft-cli` and its
upstream licence/attribution files; it downloads nothing at runtime and does not
include the desktop editor. The wheel does not add a shell command to `PATH`.
To locate and check the binary directly:

```python
import subprocess
from mcruft_deckcraft_bin import BIN

subprocess.run([str(BIN), "--version"], check=True)
```

The Python distribution version identifies the bundle release. The embedded CLI
has its own upstream version, shown by `--version` and recorded in the wheel's
`NOTICE`. Linux, Windows and Intel macOS wheels are not provided.

PDF export may rasterise slide art. Image-based PPTX export preserves appearance but does not create editable slide objects.

- [mcruft documentation](https://code.twardoch.com/mcruft/)
- [mcruft source and issues](https://github.com/twardoch/mcruft)
- [Upstream DeckCraft](https://github.com/storytold/deckcraft)

The upstream binary is MIT OR Apache-2.0; see the wheel's `licenses/` and `NOTICE`.
