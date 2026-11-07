---
this_file: src_docs/md/guide/first-document.md
---

# Assemble your first document

This tutorial creates its own two-page PDF, reorders it and saves a `.mcruft` folder.
Only the core install is required. Start in an empty working directory.

```bash
uv venv
source .venv/bin/activate
uv pip install mcruft
```

Save this as `first_document.py` and run `python first_document.py`:

```python
from pathlib import Path
from pypdf import PdfReader, PdfWriter
import mcruft

writer = PdfWriter()
writer.add_blank_page(width=300, height=200)
writer.add_blank_page(width=200, height=300)
with Path("input.pdf").open("wb") as stream:
    writer.write(stream)

doc = mcruft.open("input.pdf")
assert len(doc.pages) == 2
assert doc.pages[0].size == (300, 200)
doc.move_page(0, 1)
doc.meta["title"] = "First document"
saved = doc.save("first.mcruft")
assert Path("first.mcruft/manifest.json").is_file()

reopened = mcruft.open("first.mcruft")
assert reopened.pages[0].size == (200, 300)
report = reopened.export("result.pdf", policy="editable")
assert len(PdfReader("result.pdf").pages) == 2
print(report.outputs)
print(report.losses, report.warnings)
```

You now have `input.pdf`, the folder `first.mcruft` and `result.pdf`. The folder preserves
its source PDF; page ordering lives in the manifest. Open the output in your PDF viewer.

To assemble real material, call `doc.add_file("another.pdf")` before saving.
`doc.split()` returns one document per page; `mcruft.merge(documents)` concatenates them.
Indexes are zero-based. See [exporting](export.md) when adding images or slide decks.
