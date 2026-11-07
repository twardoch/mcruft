<!--
---
this_file: packages/mcruft_pdfcraft/README.md
---
-->

# mcruft-pdfcraft

Render PDF pages to PNG and extract pages through PdfCraft CLI; optionally extract and combine PDFs through the native binding. This package plugs into the [mcruft document API](https://code.twardoch.com/mcruft/).
Use the same Python API across engines and inspect each conversion's loss report.

## Install

Python 3.12 or later is required. Install the adapter with:

```bash
uv pip install mcruft-pdfcraft
```

Supply `pdfcraft-cli` 0.13.0 or later on `PATH`, or set
`MCRUFT_PDFCRAFT_CLI` to its executable path. For a self-contained installation
on macOS 11+ with Apple Silicon:

```bash
uv pip install 'mcruft-pdfcraft[all]'
```

The `bundled` extra installs only the CLI bundle; `all` installs every optional
component for this adapter. Bundles currently have macOS arm64 wheels only and
perform no runtime downloads. On other platforms, install the adapter and supply
a compatible CLI yourself.
`mcruft-pdfcraft[native]` installs the optional macOS arm64 Rust binding.


## Use

With `input.pdf` in the current directory and its parent directory writable:

```python
import mcruft

report = mcruft.convert("input.pdf", "pages.png", policy="fidelity")
print(report.engine)
print(report.outputs)
print(report.losses)
```

The router chooses an available engine by operation, format and policy; installing
this adapter does not force every route through it. Inspect the registry with
`mcruft.engines()`.

Choose `editable` to favour document structure or `fidelity` to favour appearance.
Routes that cannot honour the requested policy raise `UnsupportedRoute`.
PNG exports require `fidelity` and may create numbered files; use `report.outputs`
to find the actual paths.

## Limits and documentation

PNG output is rasterised. The native extra provides page operations, not the full PdfCraft application API. Installing an engine does not promise lossless round trips.
The package does not include the desktop editor.

- [Installation and platform support](https://code.twardoch.com/mcruft/)
- [Source and issue tracker](https://github.com/twardoch/mcruft)
- [Upstream PdfCraft](https://github.com/storytold/pdfcraft)

Licence: Apache-2.0. Upstream CLI licences are distributed with the separate binary wheel.
