---
this_file: src_docs/md/index.md
---

# mcruft

Assemble pages from PDFs, slide decks, vector artwork and images through one Python API.
Keep native source files in a `.mcruft` folder, choose how to convert them, and inspect what each operation loses.

```python
import mcruft

doc = mcruft.open("input.pdf")
doc.move_page(0, len(doc.pages) - 1)
doc.save("reordered.mcruft")
report = doc.export("reordered.pdf", policy="editable")
print(report.outputs, report.losses)
```

[Install mcruft](guide/install.md), then [assemble your first document](guide/first-document.md).
The tutorial uses the core package alone. Add engines when you need rendering or conversions.

## Find your way

- **Learn:** [first document](guide/first-document.md) and [conversion policies](explanation/policies.md).
- **Do:** [convert and export](guide/export.md), [edit pages](guide/editing.md), [use MCP](guide/mcp.md), [resolve errors](guide/troubleshooting.md).
- **Look up:** [Python API](reference/api.md), [packages and engines](reference/packages.md), [format and route specification](reference/specification.md).
- **Contribute:** [development and releases](development/index.md), [research archive](research/index.md).

## What ships

The core and five engine adapters are pure Python and require Python 3.12 or later.
Five separate CLI bundles and the PdfCraft native binding currently ship for **macOS arm64 only**.
Nothing downloads a product binary at runtime. `mcruft[all]` requires that platform;
other platforms can install core or engine adapters and supply compatible CLIs themselves.

The MVP supports paged documents. Frame editing, video/audio processing, batch-2 products,
and faithful Office round trips remain future work. A successful conversion is not a promise
that every source feature survived: always read its report.
