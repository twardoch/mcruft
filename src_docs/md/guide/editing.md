---
this_file: src_docs/md/guide/editing.md
---

# Edit a page in a specialist engine

`Page.edit_in()` prepares a native working file and registers changed content as a derived asset.
It does not launch a GUI or perform edits itself.

```python
import mcruft

doc = mcruft.open("image.png")
with doc.pages[0].edit_in("photocraft") as working_path:
    # Edit working_path with your editor, CLI or MCP client before leaving this block.
    print(working_path)
doc.save("edited.mcruft")
```

A page whose asset is already native to the chosen engine receives a copy of the whole
asset and retains its page index. Other sources need an editable conversion route;
otherwise `UnsupportedRoute` is raised. Changes become derived assets with provenance,
and stale previews are removed. Keep the context open until the external editor has saved.

This is page-level handoff. Frame-level changes and write-back into individual objects
are not implemented. To update hashes after separately editing packaged assets, use
`doc.refresh()`, inspect its report and save the document again.

If the context body fails, changed working files are preserved for recovery and the
document still references its previous asset. If post-edit inspection fails, the derived
edit is registered with the old page size and the inspection error propagates. Inspect
the document and working file before retrying or saving after an error.
