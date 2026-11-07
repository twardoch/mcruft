<!--
---
this_file: packages/mcruft_designcraft/README.md
---
-->

# mcruft-designcraft

Inspect IDML/DesignCraft layouts, convert them to PDF or PPTX and render pages to PNG. This package plugs into the [mcruft document API](https://code.twardoch.com/mcruft/).
Use the same Python API across engines and inspect each conversion's loss report.

## Install

Python 3.12 or later is required. Install the adapter with:

```bash
uv pip install mcruft-designcraft
```

Supply `designcraft-cli` 0.12.0 or later on `PATH`, or set
`MCRUFT_DESIGNCRAFT_CLI` to its executable path. For a self-contained installation
on macOS 11+ with Apple Silicon:

```bash
uv pip install 'mcruft-designcraft[all]'
```

The `bundled` extra installs only the CLI bundle; `all` installs every optional
component for this adapter. Bundles currently have macOS arm64 wheels only and
perform no runtime downloads. On other platforms, install the adapter and supply
a compatible CLI yourself.

## Use

With `layout.idml` in the current directory and its parent directory writable:

```python
import mcruft

report = mcruft.convert("layout.idml", "layout.pdf", policy="editable")
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

IDML support does not establish INDD support or full InDesign compatibility. Rendering requires the fonts used by the document. Installing an engine does not promise lossless round trips.
The package does not include the desktop editor.

- [Installation and platform support](https://code.twardoch.com/mcruft/)
- [Source and issue tracker](https://github.com/twardoch/mcruft)
- [Upstream DesignCraft](https://github.com/storytold/designcraft)

Licence: Apache-2.0. Upstream CLI licences are distributed with the separate binary wheel.
