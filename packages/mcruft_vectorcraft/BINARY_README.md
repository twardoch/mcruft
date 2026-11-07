<!--
---
this_file: packages/mcruft_vectorcraft/BINARY_README.md
---
-->

# mcruft-vectorcraft-bin

The VectorCraft command-line engine bundled for mcruft on Apple Silicon.
Convert SVG to PDF, PNG, AI or VectorCraft; import PDF as SVG; outline text in PDF/SVG exports.

## Install and use

Python 3.12+, macOS 11+ and arm64 are required. Install the adapter and its bundle together:

```bash
uv pip install 'mcruft-vectorcraft[bundled]'
```

mcruft discovers this wheel automatically. It contains `vectorcraft-cli` and its
upstream licence/attribution files; it downloads nothing at runtime and does not
include the desktop editor. The wheel does not add a shell command to `PATH`.
To locate and check the binary directly:

```python
import subprocess
from mcruft_vectorcraft_bin import BIN

subprocess.run([str(BIN), "--version"], check=True)
```

The Python distribution version identifies the bundle release. The embedded CLI
has its own upstream version, shown by `--version` and recorded in the wheel's
`NOTICE`. Linux, Windows and Intel macOS wheels are not provided.

PDF re-import for outlining can drop links, annotations and forms. Illustrator support covers declared routes, not every AI feature.

- [mcruft documentation](https://code.twardoch.com/mcruft/)
- [mcruft source and issues](https://github.com/twardoch/mcruft)
- [Upstream VectorCraft](https://github.com/storytold/vectorcraft)

The upstream binary is MIT OR Apache-2.0; see the wheel's `licenses/` and `NOTICE`.
