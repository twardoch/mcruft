---
this_file: src_docs/md/reference/packages.md
---

# Packages and engines

All twelve distributions use release version **1.0.0**. Adapter versions describe mcruft's
integration; bundled CLI executable versions remain the upstream versions shown below.
The core and adapters require Python 3.12+. Bundles/native wheels target macOS arm64.

| Distribution | Purpose | Runtime / extra |
| --- | --- | --- |
| [mcruft](https://pypi.org/project/mcruft/) | Document API, package I/O, native-format library engine | `engines`, `libs`, `pdf`, `svg`, `psd`, `mcp`, `all` |
| [mcruft-vectorcraft](https://pypi.org/project/mcruft-vectorcraft/) | SVG/PDF/AI/vectorcraft adapter and outlining | VectorCraft CLI; `bundled`, `all` |
| [mcruft-deckcraft](https://pypi.org/project/mcruft-deckcraft/) | PPTX/deckcraft conversion, slide rendering, image decks | DeckCraft CLI; `bundled`, `all` |
| [mcruft-photocraft](https://pypi.org/project/mcruft-photocraft/) | PNG/JPEG/PSD/pcraft conversion | PhotoCraft CLI; `bundled`, `all` |
| [mcruft-pdfcraft](https://pypi.org/project/mcruft-pdfcraft/) | PDF rendering/extraction; native engine registration | PdfCraft CLI; `bundled`, `native`, `all` |
| [mcruft-designcraft](https://pypi.org/project/mcruft-designcraft/) | IDML/designcraft export | DesignCraft CLI; `bundled`, `all` |
| [mcruft-vectorcraft-bin](https://pypi.org/project/mcruft-vectorcraft-bin/) | Bundled VectorCraft CLI | Upstream 0.16.0; `all` |
| [mcruft-deckcraft-bin](https://pypi.org/project/mcruft-deckcraft-bin/) | Bundled DeckCraft CLI | Upstream 0.10.0; `all` |
| [mcruft-photocraft-bin](https://pypi.org/project/mcruft-photocraft-bin/) | Bundled PhotoCraft CLI | Upstream 0.15.1; `all` |
| [mcruft-pdfcraft-bin](https://pypi.org/project/mcruft-pdfcraft-bin/) | Bundled PdfCraft CLI | Upstream 0.13.0; `all` |
| [mcruft-designcraft-bin](https://pypi.org/project/mcruft-designcraft-bin/) | Bundled DesignCraft CLI | Upstream 0.12.0; `all` |
| [mcruft-pdfcraft-native](https://pypi.org/project/mcruft-pdfcraft-native/) | PyO3 PDF page count, extraction and combination | CPython 3.12+ abi3; `all` |

The native binding is registered by `mcruft-pdfcraft`; installing the binding alone does
not install the unified engine adapter. CLI wheels provide an importable `BIN` path,
not shell console scripts. Adapters locate that path automatically.

The DesignCraft routes were exercised with generated sample documents; arbitrary IDML
compatibility is unverified. AI support is bounded by VectorCraft's importer. Adobe,
Microsoft and other reference-product names describe file compatibility goals; they do
not imply complete application compatibility or affiliation.

For every route's policy and evidence level, use the [conversion matrix](specification.md#5-conversion-and-export-matrix-mvp).
