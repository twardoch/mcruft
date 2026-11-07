---
this_file: src_docs/md/guide/mcp.md
---

# Use an engine over MCP

Install `mcruft[mcp]` and an engine adapter with a compatible CLI. MCP sessions expose the
product's own tool API; they do not add conversion capabilities to the unified router.

```python
import asyncio
from pathlib import Path
from mcruft_vectorcraft import engine


async def main():
    root = Path("work").resolve()
    root.mkdir(exist_ok=True)
    async with await engine.session(read_root=root, write_root=root) as session:
        # Use a tool name and arguments documented by your installed product version.
        # result = await session.call(tool_name, arguments)
        print("VectorCraft MCP session ready")


asyncio.run(main())
```

The read/write roots constrain the product server's filesystem access. VectorCraft gets
`--headless`; other launch details vary by product. Open, call and close the session in
the same asyncio task. `call(tool, args)` returns the SDK's tool result, which the caller
must inspect for tool-level errors. Sessions close automatically when their context exits.
