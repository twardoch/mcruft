<!--
---
this_file: packages/mcruft_pdfcraft/BINARY_README.md
---
-->

# mcruft-pdfcraft-bin

The PdfCraft command-line engine bundled for mcruft on Apple Silicon.
Render PDF pages to PNG and extract pages through PdfCraft CLI; optionally extract and combine PDFs through the native binding.

## Install and use

Python 3.12+, macOS 11+ and arm64 are required. Install the adapter and its bundle together:

```bash
uv pip install 'mcruft-pdfcraft[bundled]'
```

mcruft discovers this wheel automatically. It contains `pdfcraft-cli` and its
upstream licence/attribution files; it downloads nothing at runtime and does not
include the desktop editor. The wheel does not add a shell command to `PATH`.
To locate and check the binary directly:

```python
import subprocess
from mcruft_pdfcraft_bin import BIN

subprocess.run([str(BIN), "--version"], check=True)
```

The Python distribution version identifies the bundle release. The embedded CLI
has its own upstream version, shown by `--version` and recorded in the wheel's
`NOTICE`. Linux, Windows and Intel macOS wheels are not provided.

PNG output is rasterised. The native extra provides page operations, not the full PdfCraft application API.

- [mcruft documentation](https://code.twardoch.com/mcruft/)
- [mcruft source and issues](https://github.com/twardoch/mcruft)
- [Upstream PdfCraft](https://github.com/storytold/pdfcraft)

The upstream binary is MIT OR Apache-2.0; see the wheel's `licenses/` and `NOTICE`.
