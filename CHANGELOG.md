---
this_file: CHANGELOG.md
---

# Changelog

## Unreleased

## v0.1.3 (2026-11-07)

- Publish all five licensed CLI bundles and the PdfCraft native binding to PyPI;
  verify every wheel against its preserved SHA-256 hash.
- `mcruft-pdfcraft-native` 0.1.0: real version and PEP 639 licence metadata; the wheel ships
  mcruft, PdfCraft and every linked crate's licence files (`native/.../licenses/`).
- CLI bundle wheels are built from the official release zips with their licence/attribution
  files (`--license-dir`); arm64 binaries verified against the `macosx_11_0` tag.
- Tests detect embedded fonts by parsing the PDF, not by grepping bytes: the native writer
  uses object streams, which hid `/FontFile2` from the byte search.
- Finish the `0.1.2` PyPI publication: PhotoCraft and VectorCraft wheels and sdists
  uploaded from the preserved artifacts; all twelve files verified by SHA-256, and a
  registry-only `mcruft[engines]==0.1.2` install registers all seven engine entry points
  (`pdfcraft-native` stays unavailable until its binding is published).
- Add a preview-first PyPI recovery tool with hash checks, duplicate skipping,
  explicit upload mode, bounded HTTP behavior and post-upload verification;
  preserve the `0.1.2` retry artifacts and document the next-session handoff.

- Add recursive `all` extras across core, engines, native binding and CLI bundles;
  include the PdfCraft native binding and bypass workspace wheel exclusions in
  the full installer.

- Make the repository root editable-installable as `mcruft`; install local engines,
  MCP/library extras and development tools system-wide through `install.sh`.

## v0.1.2 (2026-10-25)

- Rebuild editable workspace installs when the git commit or tags change (uv `cache-keys`), so local release gates see current hatch-vcs versions.

## v0.1.1 (2026-10-25)

- Add workspace build/install scripts, guarded GitHub/PyPI releases, CI and generated package versions.

- Add optional `pdf`, `svg`, `psd` and combined `libs` extras. Prefer tested library
  routes for PDF/SVG PNG rendering and PSD inspection; serialize PDFium calls, honour
  page selection/DPI, and report rasterization losses and SVG system-font dependence.

- Add the `mcruft[engines]` metapackage extra, which installs all five engine packages.

- Support PSD/pcraft PDF export and previews, report flattened layers, and expose
  matching PhotoCraft fidelity conversions.
- Fall back from whole-file conversion to same-policy page export with consistent
  single-page and numbered multi-page PNG outputs.
- Keep page owners alive and route PDF extraction/combination through the optional
  PdfCraft native adapter when installed.
- Include a redistribution NOTICE in every bundled CLI wheel and warn when upstream
  licence files were not supplied.
- Preserve changed working files across edit/inspection failures; register completed
  edits before inspection and propagate inspection errors with the old page size.
- Refuse editable PNG export, retain fixed-fidelity page rendering, and report an
  effects loss when raster rendering drops an ICC profile.
- Cover editable export fallback, fidelity route priority and the subsequent outline
  pass; remove unused conversion fakes from native-copy tests.
- Support raster pages in PDF exports/previews and DPI-aware PNG export; apply the
  requested-policy, editable-policy and single-page conversion fallbacks.
- Keep native editable assets and page indexes during edit handoffs; refresh edited
  page dimensions and refuse fidelity-only conversions.
- Refuse exports onto assets, stage PDF exports atomically, preserve render siblings,
  reject in-place conversion and report missing destination directories clearly.
- Normalize JPEG/TIFF aliases, validate missing deck images, declare direct PDF
  dependencies and add Apache-2.0 metadata to all six packages.
- Implement core conversion policies, ordered PDF/PNG/SVG/PPTX exports, page rendering,
  preview generation and page edit transactions on top of engine capabilities.
- Raise EngineUnavailable for unavailable pinned engines; expose VectorCraft paged PNG
  export with the standard output naming contract.
- Prefer SVG absolute dimensions over viewBox and support centimetre dimensions.
- Keep engine listing available when a product CLI fails its version check.
- Scaffold the mcruft Python workspace and five separately distributed product engines.
- Implement native-asset folder packages, document assembly, engine routing, format
  inspection, pypdf page operations and optional MCP sessions.
- Add an arm64 CLI wheel builder and pinned optional PdfCraft Rust binding.
- Cover package safety, engine selection, generated document fixtures and wheel hashes
  with offline tests. Product conversion adapters remain deferred to Task 6.
