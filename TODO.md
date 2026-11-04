---
this_file: TODO.md
---

# Remaining publication work

- [x] Read `docs/handoffs/handoff-2026-10-26-0136.md` before resuming on 2026-10-27.
- [x] Run the publishing tool in preview mode against `.cache/publish-resume-0.1.2` and check the recorded artifact hashes.
- [x] Retry missing PhotoCraft and VectorCraft `0.1.2` wheels/sdists once with `--publish`; stop if PyPI still returns 429.
- [x] Verify all twelve `0.1.2` files against PyPI SHA-256 and update the handoff/status report.
- [x] Install `mcruft[engines]==0.1.2` from PyPI in a fresh environment outside the source workspace and verify engine entry points.
- [ ] Review the uncommitted root-install and recursive `all` changes for a separate stable release; do not overwrite `0.1.2` artifacts.
- [x] Include upstream licence/attribution files in all five CLI bundles and verify binary compatibility with their platform tags.
- [ ] Give `mcruft-pdfcraft-native` a real version (currently 0.0.0) and ship licence files (mcruft + pdfcraft/hayro) in its wheel.
- [ ] Prepare and publish the native abi3 wheel and five CLI bundles through the usual reviewed release workflow once project creation is available.
- [ ] Publish a new stable core/engine release containing the `all` extras; current `0.1.2` does not contain them.
- [ ] Verify a fresh registry-only `mcruft[all]` installation includes optional libraries, MCP, five working CLI bundles and the native engine.
- [x] Remove the temporary publishing-resume section from `AGENTS.md` (done 2026-11-04).
- [ ] Update release docs after the next stable release.
