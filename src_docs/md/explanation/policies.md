---
this_file: src_docs/md/explanation/policies.md
---

# Editability, fidelity and native assets

`editable` preserves usable structure where the backend supports it. Text may remain
selectable and fonts embedded, but slide artwork can be rasterised. `fidelity` prioritises
appearance and can outline text or turn pages into pictures. Neither policy guarantees
an exact round trip. Unsupported combinations fail explicitly.

Every conversion returns a `Report`: output paths, backend/version, warnings and losses.
A loss can describe rasterisation, font changes, layout, effects, media or unsupported
features. Read it before accepting generated material. A route with no reported loss is
not proof that arbitrary inputs preserve all features.

## Why a folder package?

A `.mcruft` folder stores native assets alongside a JSON manifest of ordered page references.
It avoids inventing a replacement for PDF, PPTX, SVG or PSD. Several document pages can
point into one source file. Split and merge change those references; export performs the
actual conversion. Optional single-page PDF previews help readers inspect the package.

Assets are copied when saved and are not rewritten by ordinary saves. Derived edits retain
provenance. Hashes detect changes but are not authentication. Manifest paths must stay
inside the package; absolute paths, parent traversal and symlinks are rejected.

Frames and time-based media appear in the model for later work. Frames are empty in the
MVP and are not persisted by manifest schema 1. The [specification](../reference/specification.md)
records the precise package layout and tested conversion boundaries.
