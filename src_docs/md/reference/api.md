---
this_file: src_docs/md/reference/api.md
---

# Python API

All paths accept `str` or `pathlib.Path`. Page indexes are zero-based; page sizes and
bounding boxes are in points (1/72 inch), with the origin at the top-left and y down.

## Module functions

| Function | Result and behavior |
| --- | --- |
| `new(title="")` | Empty `Document`. |
| `open(path)` | Load a package folder or inspect a source file as a one-asset document. |
| `load(path)` | Load a `.mcruft` folder; validate schema/paths and warn on hash changes. |
| `merge(docs)` | New document with pages in document order and remapped asset/page identifiers. |
| `convert(src, dst, *, policy)` | Whole-file conversion, or same-policy page-export fallback; returns `Report`. |
| `convert_editable(src, dst)` | `convert(..., policy="editable")`. |
| `convert_fidelity(src, dst)` | `convert(..., policy="fidelity")`. |
| `engines()` | List of `EngineInfo` records, including unavailable engines. |
| `save(doc, path=None, *, previews=False)` | Package-save function used by `Document.save()`. |
| `refresh(doc)` | Recompute asset hashes and invalidate stale previews. |

## Document

| Member | Behavior |
| --- | --- |
| `meta` | Title, created and modified strings. |
| `assets` | Asset ID → `Asset` mapping. |
| `pages` | Ordered `Page` list. |
| `media` | Media references; no time-based processing in the MVP. |
| `path` | Saved folder path, or `None` before saving. |
| `add_file(path)` | Inspect and append all pages; returns added pages. |
| `remove_pages(indexes)` | Remove page references; raises `IndexError` for invalid indexes. |
| `move_page(i, to)` | Move a page; both indexes must exist. |
| `split()` | One new document per page, with source asset references. |
| `save(path=None, previews=False)` | Save package; a first save needs a path. Returns `Report`. |
| `refresh()` | Refresh hashes; returns `Report`. |
| `export(path, *, policy, pages=None, fonts=None, dpi=150)` | Export selected/all pages to PDF, PNG, one-page SVG or image-based PPTX. Returns `Report`. |

`fonts` accepts `embed` or `outline`; defaults follow the policy. PNG and PPTX rendering
need suitable available backends. A page selection is a list of zero-based indexes.

## Page and assets

`Page` has `id`, `size`, `source`, `preview` and `frames`.
`source` is `{"asset": asset_id, "index": native_page_index}`.
`page.render(path, dpi=150)` returns a fidelity `Report`.
`page.edit_in(engine)` is a synchronous context manager yielding a working `Path`.

`Asset` stores `id`, `path`, `media_type`, `sha256`, `role`, `derived_from` and `via`.
Roles are `source`, `derived` and `preview`. `Frame` and `Media` describe future-facing
model data; frame-level editing and time-based processing are outside the MVP.

## Reports and errors

`Report` fields: `op`, `policy`, `engine`, `engine_version`, `outputs`, `losses`, `warnings`.
`Loss` fields: `kind`, `detail`, optional `page`. Kinds are `raster`, `fonts`, `layout`,
`effects`, `media`, `unsupported`.

Catch `McruftError` for common handling, or its subclasses `UnsupportedRoute`,
`EngineUnavailable`, `EngineFailed`, `UnsupportedSchema`, `PackageError`.
CLI `EngineFailed` errors include the failing invocation and stderr. Native backend
failures can also raise `EngineFailed` without a CLI command. Standard filesystem,
index and parser exceptions may also propagate; the base class does not wrap every error.

## Engine extension points

`Engine`, `EngineInfo` and `Capability` are exported from `mcruft`.
Adapters register an engine in the `mcruft.engines` entry-point group.
Capabilities declare operation, source/target format, policy and verification provenance.
Available, verified routes win first; backend precedence is native, library, CLI, MCP.
See [the specification](specification.md#4-engines-and-routing) for the contract.
