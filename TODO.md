---
this_file: TODO.md
---

# Remaining publication work

- [x] Read `docs/handoffs/handoff-2026-10-26-0136.md` before resuming on 2026-10-27.
- [x] Run the publishing tool in preview mode against `.cache/publish-resume-0.1.2` and check the recorded artifact hashes.
- [x] Retry missing PhotoCraft and VectorCraft `0.1.2` wheels/sdists once with `--publish`; stop if PyPI still returns 429.
- [x] Verify all twelve `0.1.2` files against PyPI SHA-256 and update the handoff/status report.
- [x] Install `mcruft[engines]==0.1.2` from PyPI in a fresh environment outside the source workspace and verify engine entry points.
- [x] Review the uncommitted root-install and recursive `all` changes for a separate stable release; do not overwrite `0.1.2` artifacts.
- [x] Include upstream licence/attribution files in all five CLI bundles and verify binary compatibility with their platform tags.
- [x] Give `mcruft-pdfcraft-native` a real version (currently 0.0.0) and ship licence files (mcruft + pdfcraft/hayro) in its wheel.
- [x] Prepare the native abi3 wheel (0.1.0, licensed) and five licensed CLI bundles; merged as PR #4 (`ae34507`).
- [x] Upload the four remaining new projects from `.cache/publish-new-0.1.3/`: PdfCraft/PhotoCraft/VectorCraft bins and PdfCraft native. Published 2026-11-07; all six binary/native hashes verified against PyPI JSON.
- [x] Platform scope decided: keep the hard failure off macOS arm64 (no silent drops); documented in README.
- [ ] Publish a new stable core/engine release containing the `all` extras; current `0.1.2` does not contain them.
- [ ] Verify a fresh registry-only `mcruft[all]` installation includes optional libraries, MCP, five working CLI bundles and the native engine.
- [x] Remove the temporary publishing-resume section from `AGENTS.md` (done 2026-11-04).
- [ ] Update release docs after the next stable release.
