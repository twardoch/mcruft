<!--
---
this_file: packages/mcruft_photocraft/README.md
---
-->

# mcruft-photocraft

Inspect PSD/PhotoCraft images and convert PNG, JPEG, PSD and PhotoCraft files through the supported routes. This package plugs into the [mcruft document API](https://code.twardoch.com/mcruft/).
Use the same Python API across engines and inspect each conversion's loss report.

## Install

Python 3.12 or later is required. Install the adapter with:

```bash
uv pip install mcruft-photocraft
```

Supply `photocraft-cli` 0.15.1 or later on `PATH`, or set
`MCRUFT_PHOTOCRAFT_CLI` to its executable path. For a self-contained installation
on macOS 11+ with Apple Silicon:

```bash
uv pip install 'mcruft-photocraft[all]'
```

The `bundled` extra installs only the CLI bundle; `all` installs every optional
component for this adapter. Bundles currently have macOS arm64 wheels only and
perform no runtime downloads. On other platforms, install the adapter and supply
a compatible CLI yourself.

## Use

With `image.psd` in the current directory and its parent directory writable:

```python
import mcruft

report = mcruft.convert("image.psd", "image.png", policy="fidelity")
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

PNG/PDF exports flatten layers. Unsupported PSD effects and Photoshop round trips are not guaranteed. Installing an engine does not promise lossless round trips.
The package does not include the desktop editor.

- [Installation and platform support](https://code.twardoch.com/mcruft/)
- [Source and issue tracker](https://github.com/twardoch/mcruft)
- [Upstream PhotoCraft](https://github.com/storytold/photocraft)

Licence: Apache-2.0. Upstream CLI licences are distributed with the separate binary wheel.
