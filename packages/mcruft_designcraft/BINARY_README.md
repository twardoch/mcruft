<!--
---
this_file: packages/mcruft_designcraft/BINARY_README.md
---
-->

# mcruft-designcraft-bin

The DesignCraft command-line engine bundled for mcruft on Apple Silicon.
Inspect IDML/DesignCraft layouts, convert them to PDF or PPTX and render pages to PNG.

## Install and use

Python 3.12+, macOS 11+ and arm64 are required. Install the adapter and its bundle together:

```bash
uv pip install 'mcruft-designcraft[bundled]'
```

mcruft discovers this wheel automatically. It contains `designcraft-cli` and its
upstream licence/attribution files; it downloads nothing at runtime and does not
include the desktop editor. The wheel does not add a shell command to `PATH`.
To locate and check the binary directly:

```python
import subprocess
from mcruft_designcraft_bin import BIN

subprocess.run([str(BIN), "--version"], check=True)
```

The Python distribution version identifies the bundle release. The embedded CLI
has its own upstream version, shown by `--version` and recorded in the wheel's
`NOTICE`. Linux, Windows and Intel macOS wheels are not provided.

IDML support does not establish INDD support or full InDesign compatibility. Rendering requires the fonts used by the document.

- [mcruft documentation](https://code.twardoch.com/mcruft/)
- [mcruft source and issues](https://github.com/twardoch/mcruft)
- [Upstream DesignCraft](https://github.com/storytold/designcraft)

The upstream binary is MIT OR Apache-2.0; see the wheel's `licenses/` and `NOTICE`.
