<!--
---
this_file: packages/mcruft_photocraft/BINARY_README.md
---
-->

# mcruft-photocraft-bin

The PhotoCraft command-line engine bundled for mcruft on Apple Silicon.
Inspect PSD/PhotoCraft images and convert PNG, JPEG, PSD and PhotoCraft files through the supported routes.

## Install and use

Python 3.12+, macOS 11+ and arm64 are required. Install the adapter and its bundle together:

```bash
uv pip install 'mcruft-photocraft[bundled]'
```

mcruft discovers this wheel automatically. It contains `photocraft-cli` and its
upstream licence/attribution files; it downloads nothing at runtime and does not
include the desktop editor. The wheel does not add a shell command to `PATH`.
To locate and check the binary directly:

```python
import subprocess
from mcruft_photocraft_bin import BIN

subprocess.run([str(BIN), "--version"], check=True)
```

The Python distribution version identifies the bundle release. The embedded CLI
has its own upstream version, shown by `--version` and recorded in the wheel's
`NOTICE`. Linux, Windows and Intel macOS wheels are not provided.

PNG/PDF exports flatten layers. Unsupported PSD effects and Photoshop round trips are not guaranteed.

- [mcruft documentation](https://code.twardoch.com/mcruft/)
- [mcruft source and issues](https://github.com/twardoch/mcruft)
- [Upstream PhotoCraft](https://github.com/storytold/photocraft)

The upstream binary is MIT OR Apache-2.0; see the wheel's `licenses/` and `NOTICE`.
