<!-- this_file: README.md -->

# mcruft

Assemble pages from PDFs, slide decks, vector artwork and images through one Python API.
Keep native source files, choose between editability and visual fidelity, and inspect
what each conversion loses.

[Documentation](https://code.twardoch.com/mcruft/) ·
[Python API](https://code.twardoch.com/mcruft/reference/api/) ·
[PyPI](https://pypi.org/project/mcruft/) ·
[Issues](https://github.com/twardoch/mcruft/issues)

## Install

Python 3.12 or later, in a virtual environment:

```bash
uv pip install mcruft                   # inspect and assemble PDFs; inspect PPTX/SVG/images
uv pip install 'mcruft[libs]'           # add PDF/SVG rendering and PSD inspection
uv pip install 'mcruft[engines]'        # five adapters; supply the product CLIs
uv pip install 'mcruft[all]==1.0.0'     # everything, including binaries (macOS arm64 only)
```

`pip install` accepts the same names. The core and adapters are pure Python.
The five bundled CLI wheels and native PDF binding currently support **macOS arm64 only**;
`[all]` fails to resolve elsewhere. On other platforms, install core or adapters and
provide compatible CLIs. Those product runtimes have not been tested here.
No package downloads a product binary at runtime.

## Assemble a document

```python
import mcruft

doc = mcruft.open("input.pdf")
doc.add_file("appendix.pdf")
doc.move_page(0, len(doc.pages) - 1)
doc.save("assembled.mcruft")
report = doc.export("assembled.pdf", policy="editable")
print(report.outputs)
for loss in report.losses:
    print(loss.kind, loss.detail)
```

This example needs only core. Pages are zero-based. A `.mcruft` file is a folder:
`manifest.json` orders page references, `assets/` preserves native files, `derived/`
holds generated edits, and `previews/` optionally holds single-page PDFs.

[Run the self-contained first-document tutorial](https://code.twardoch.com/mcruft/guide/first-document/).

## Convert with an explicit policy

```python
report = mcruft.convert("art.svg", "art.pdf", policy="editable")  # requires VectorCraft
report = mcruft.convert("art.svg", "art.png", policy="fidelity")  # resvg-py or VectorCraft
```

`editable` keeps usable structure where supported; `fidelity` prioritises appearance,
possibly outlining text or rasterising pages. Each operation returns a `Report` with
outputs, backend/version, losses and warnings. Unsupported routes raise `UnsupportedRoute`.
Neither policy promises a lossless round trip.

PDF fidelity exports use a VectorCraft outline pass, which can drop links, annotations
and forms. PNG only accepts fidelity. Image-based PPTX exports need DeckCraft and keep
appearance as slide-sized pictures. See the
[tested conversion matrix](https://code.twardoch.com/mcruft/reference/specification/#5-conversion-and-export-matrix-mvp).

## Choose an engine

| Adapter | Purpose |
| --- | --- |
| `mcruft-vectorcraft` | SVG/PDF/AI/vectorcraft conversion, text outlining |
| `mcruft-deckcraft` | PPTX/deckcraft conversion, PDF/PNG slides, decks from images |
| `mcruft-photocraft` | PNG/JPEG/PSD/pcraft conversion |
| `mcruft-pdfcraft` | PDF rendering/extraction, optional native page operations |
| `mcruft-designcraft` | IDML/designcraft exports (sample-based verification) |

Each adapter's `[bundled]` extra adds its `mcruft-<product>-bin` wheel. PdfCraft's
`[native]` extra adds `mcruft-pdfcraft-native`. Every distribution exposes `[all]`.
Bundle release versions describe packaging; embedded CLI versions retain upstream numbers.

```python
for engine in mcruft.engines():
    print(engine.name, engine.available, engine.version)
```

CLI lookup: `$MCRUFT_<PRODUCT>_CLI`, then bundled wheel, then `PATH`.
The router prefers verified capabilities, then native, library, CLI and MCP backends.
`engine.session()` exposes the product's MCP API with `mcruft[mcp]` installed.

## Scope

The MVP covers paged 2D documents and page-level editing handoffs. Frame editing,
frame write-back, video/audio processing and batch-2 products remain future work.
Reference-product file support is bounded by the engines, not full application compatibility.

## Develop

```bash
uv sync --locked --all-packages --all-extras
uv run ruff check .
uv run ruff format --check .
uv run pytest -q
./build.sh
```

`./install.sh` installs local engines and extras; it can use wheels in `dist/`.
`./build.sh` builds six pure-Python wheels and sdists. The native binding and licensed
CLI bundles have separate builders. See the
[development guide](https://code.twardoch.com/mcruft/development/).

Documentation source is `src_docs/md`, configured by `src_docs/mkdocs.yml`.
Pushes to main build ProperDocs + MaterialX into `docs/` and deploy GitHub Pages.
Release tags use hatch-vcs; `./release.sh [patch|minor|major]` gates and releases
through gitnextver. Publication requires configured credentials.

Licence: Apache-2.0. Bundled upstream code retains its own licences and attribution.
Product names describe the engines mcruft drives; they do not imply affiliation.
