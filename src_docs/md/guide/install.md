---
this_file: src_docs/md/guide/install.md
---

# Install mcruft

Use Python 3.12 or later. In an activated virtual environment:

```bash
uv pip install mcruft
python -c "import mcruft; print(mcruft.__version__)"
```

The core inspects PDF, PPTX, SVG and common raster images, and extracts/combines PDF pages
with pypdf. It needs no product CLI for those operations.

## Choose the extra you need

| Install | Adds | Platform |
| --- | --- | --- |
| `mcruft[libs]` | PDF rendering, SVG rendering, PSD inspection | Depends on library wheels |
| `mcruft[engines]` | All five product adapters, without binaries | Supply compatible CLIs |
| `mcruft[mcp]` | Python MCP SDK | Requires a product CLI for sessions |
| `mcruft[all]` | All adapters, libraries, MCP, five CLIs, native PDF binding | macOS arm64 |
| `mcruft-vectorcraft[bundled]` | One adapter with its CLI | macOS arm64 |

```bash
uv pip install 'mcruft[all]==1.0.0'
python -c "import mcruft; print([(e.name, e.available, e.version) for e in mcruft.engines()])"
```

`pip install` accepts the same package names. On Windows, use double quotes around extras.
No matching binary distribution on Linux, Windows or Intel macOS is expected for `[all]`;
use core or `[engines]` there. Those platforms' product runtimes have not been verified.

## Bring your own CLI

Each adapter looks for `$MCRUFT_<PRODUCT>_CLI`, then its bundled wheel, then `PATH`.
For example:

```bash
export MCRUFT_VECTORCRAFT_CLI=/absolute/path/to/vectorcraft-cli
uv pip install mcruft-vectorcraft
```

An unavailable engine can still appear in `mcruft.engines()`. Availability means a backend
was found, not that every format and policy is supported. See the [package reference](../reference/packages.md).
