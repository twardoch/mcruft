---
this_file: src_docs/md/guide/export.md
---

# Convert and export documents

Whole-file conversion chooses an available engine for one format pair and policy:

```python
import mcruft

report = mcruft.convert("art.svg", "art.pdf", policy="editable")
for loss in report.losses:
    print(loss.kind, loss.detail, loss.page)
for warning in report.warnings:
    print(warning)
```

SVG to PDF requires VectorCraft. `convert_editable(src, dst)` and
`convert_fidelity(src, dst)` are convenience functions for the two policies.

## Select and combine pages

```python
doc = mcruft.open("deck.pptx")
doc.add_file("appendix.pdf")
report = doc.export("selected.pdf", policy="editable", pages=[0, 2])
```

PDF assembly preserves page order. PPTX exports need DeckCraft. For fidelity PDF export,
the outline pass additionally needs VectorCraft and can drop links, forms and annotations.
The core can assemble PDF pages alone with `policy="editable"`.

## Render images and image-based slides

```python
report = doc.export("pages.png", policy="fidelity", dpi=150)
# pages-0000.png, pages-0001.png, ...
report = doc.pages[0].render("first-page.png", dpi=150)
report = doc.export("slides.pptx", policy="fidelity")
```

PNG is a raster output: `policy="editable"` raises `UnsupportedRoute`.
PDF rendering needs pypdfium2 (`mcruft[pdf]`) or a suitable product engine;
SVG rendering can use resvg-py (`mcruft[svg]`). Image-based PPTX export needs DeckCraft
and a rendering route for every page. It does not reconstruct editable slide objects.

`convert()` writes a single-page image exactly to its destination; for multiple pages,
its export fallback writes numbered siblings. Inspect `report.outputs` for actual paths.
The destination directory must exist. Exports refuse to overwrite the document's assets.
See the [route matrix](../reference/specification.md#5-conversion-and-export-matrix-mvp)
for verified routes and their limits.
