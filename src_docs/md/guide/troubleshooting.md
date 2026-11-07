---
this_file: src_docs/md/guide/troubleshooting.md
---

# Resolve installation and conversion errors

| Symptom | Check and action |
| --- | --- |
| No matching `*-bin` or native wheel | Bundles target macOS arm64 and Python 3.12+. Use core or `[engines]` on other platforms. |
| Engine listed as unavailable | Check its CLI override, bundled package and `PATH`; run the CLI's `--version`. |
| `EngineUnavailable` | Install the needed optional dependency or runtime. |
| `UnsupportedRoute` | Check the format pair and policy in the route matrix. Raster output requires fidelity. |
| `EngineFailed` | Read its command and stderr tail; verify the product version and input support. |
| `PackageError` | Check manifest paths, package contents and destination directory. |
| `UnsupportedSchema` | The manifest schema is newer or unknown; use a compatible mcruft release. |
| Hash warning on load | An asset changed. Review it, call `doc.refresh()` and save to update hashes. |
| PDF fidelity export unavailable | The outline pass needs VectorCraft even when basic PDF page assembly works. |

Print available backends:

```python
import mcruft

for engine in mcruft.engines():
    print(engine.name, engine.kind, engine.available, engine.version)
```

When reporting an issue, include Python/platform, package and CLI versions, operation,
policy, traceback and a shareable input that reproduces it. Remove private paths/content.
[Report an issue](https://github.com/twardoch/mcruft/issues).
