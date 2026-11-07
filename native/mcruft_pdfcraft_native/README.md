<!--
---
this_file: native/mcruft_pdfcraft_native/README.md
---
-->

# mcruft-pdfcraft-native

Count, extract and combine PDF pages through pinned PdfCraft Rust libraries.
This optional Python extension supplies mcruft's `pdfcraft-native` engine without
launching a CLI or downloading anything at runtime.

## Install

Python 3.12+, macOS 11+ and Apple Silicon are required for the published abi3 wheel:

```bash
uv pip install 'mcruft-pdfcraft[native]'
```

This installs the adapter as well as the extension. For the standalone binding:

```bash
uv pip install mcruft-pdfcraft-native
```

Linux, Windows and Intel macOS wheels are not provided. The `all` extra exists for
consistent installation across mcruft distributions and adds no dependencies.

## Use

The low-level API accepts string paths and zero-based page indexes. Output parent
directories must exist. Choose new output paths: the low-level writer overwrites
existing files. Malformed PDFs and I/O failures raise `RuntimeError`.

```python
import mcruft_pdfcraft_native as pdf

print(pdf.page_count("input.pdf"))
pdf.extract("input.pdf", [0], "first-page.pdf")
pdf.combine(["first-page.pdf", "appendix.pdf"], "combined.pdf")
```

For policy selection, capability routing and loss reports, use the
[mcruft document API](https://code.twardoch.com/mcruft/) with the
`mcruft-pdfcraft` adapter installed. The binding exposes these three page operations;
it does not expose the full PdfCraft editor or claim to preserve every PDF feature.

## Build from source

Install Rust and Python 3.12 or later, then run from this directory:

```bash
uvx maturin build --release
```

This extension is outside the uv Python workspace and is not built by `uv sync`.
PdfCraft engine crates are pinned to commit
`53199fb4fa36f3c95b539add6218c57aeb2f823c` (v0.13.0); UI, MCP and updater crates are
not linked. Building requires access to those sources and a native toolchain.

- [mcruft documentation](https://code.twardoch.com/mcruft/)
- [Source and issue tracker](https://github.com/twardoch/mcruft)
- [Upstream PdfCraft](https://github.com/storytold/pdfcraft)

Licence: Apache-2.0 AND (MIT OR Apache-2.0). The wheel includes mcruft, upstream
and linked dependency licences under `licenses/`.
