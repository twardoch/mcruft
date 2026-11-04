---
this_file: WORK.md
---

# Work status

## 0.1.3 preparation and new-project upload (2026-11-04)

- PR #4 (squash `ae34507` on main): root metadata + `all` extras, licensed CLI bundles,
  native 0.1.0 with 112 licence files (incl. portable-atomic after review), bounded
  post-upload wait in `resume_publish.py`, PDF-parsing font check. CI and Sourcery green;
  4 Sourcery findings fixed, 4 local-attacker hardening findings declined.
- Gates: ruff clean; 204 passed both without and with the native binding installed.
- New-project upload, one attempt (`UV_HTTP_RETRIES=0`): `mcruft-deckcraft-bin` 0.10.0 and
  `mcruft-designcraft-bin` 0.12.0 published, SHA-256 verified. Then HTTP 429 "Too many new
  projects created". PdfCraft/PhotoCraft/VectorCraft bins and native are absent. Stopped.
- **0.1.3 not tagged or published**, since `mcruft[all]` would not resolve yet. The exact
  wheels are preserved in `.cache/publish-new-0.1.3/` with `upload.sha256`.
- Rate-limit observation, not a promise: both sessions got 429 right after the 4th new project
  in a short window. If that holds, the four remaining fit in one later attempt.
- `dist/`: the stale unlicensed native 0.0.0 wheel is replaced by the 0.1.0 one.
- **Next upload** (`.cache/` exists only on this machine; `resume_publish.py` covers only the six
  pure-Python packages, so use plain uv). Load credentials as in
  `docs/handoffs/handoff-2026-10-26-0136.md` §6, never printing them, then:

  ```bash
  cd .cache/publish-new-0.1.3 && shasum -a 256 -c upload.sha256
  UV_HTTP_RETRIES=0 uv publish --no-config --check-url https://pypi.org/simple/ \ --publish-url https://upload.pypi.org/legacy/ *.whl
  ```

  `--check-url` skips the two live wheels (and pdfcraft-bin, if uv's "Uploaded" line before
  the 429 was real). Stop on 429. Verify all six hashes against PyPI JSON afterwards.
- **Guard:** do not run `release.sh` or `publish.sh` until all four verify on PyPI. Pushing the
  tag triggers `release.yml`, which publishes core 0.1.3 with an `all` extra pointing at them.

## 0.1.2 PyPI publication finished (2026-11-04)

- Preview against `.cache/publish-resume-0.1.2`: 8 published, 4 pending; all 12 local
  SHA-256 hashes match `docs/handoffs/pypi-0.1.2-artifacts.json`.
- One `--publish` run uploaded the PhotoCraft and VectorCraft wheels and sdists with no
  429. The tool's immediate post-upload check exited 1 ("PyPI does not yet confirm every
  file"); a preview about 60 s later confirmed all 12 files by SHA-256 (PyPI JSON lag).
  Snapshot: `docs/handoffs/pypi-0.1.2-status-20261104.json`.
- Registry-only check in a fresh Python 3.12 venv outside the checkout
  (`--no-config`, PyPI index only): six distributions at 0.1.2; `mcruft.engines`
  entry points register deckcraft, designcraft, lib, pdfcraft, pdfcraft_native, photocraft
  and vectorcraft. `mcruft.engines()` reports `pdfcraft-native` as available=False (binding not
  published); the five CLI engines are available only because the CLIs are on this machine's PATH.
- No code changed, so tests were not rerun. No commit, tag, push or version bump.
- CLI bundles rebuilt with licences: each binary taken from the official
  `craft-maccli/<app>-cli-<ver>-macos-universal.zip` (byte-identical to the PATH binary), with
  the zip's other files (LICENSE-MIT/APACHE, NOTICE, OFL font licences, third-party `licenses/`,
  ASSETS.md, README) passed as `--license-dir`. 6–24 licence files per wheel, 30–52 MB.
  All five thinned to arm64; `vtool` shows minos 11.0, matching `macosx_11_0_arm64`. Installed
  into a fresh venv: each `--version` runs, `uv pip check` passes. Copies replace the
  unlicensed test wheels in `dist/`. Not published.
- Native wheel `mcruft_pdfcraft_native-0.0.0-cp312-abi3-macosx_11_0_arm64.whl` is not
  publishable: version 0.0.0 and no licence files.
- Gates after the doc edits: ruff clean, 202 passed.
- Next (TODO.md): native package version/licences, the native/binary distributions, then a
  new stable release with the `all` extras.

## Publishing tool and next-session handoff (2026-10-26)

- Added `tools/resume_publish.py`, using only the standard library and existing
  uv CLI. Preview is the default. It covers the six stable pure-Python package
  wheels/sdists, checks existing PyPI SHA-256, rejects conflicts/incomplete sets,
  skips completed files and requires explicit `--publish` plus environment-only
  credentials for one upload invocation. HTTP retries are disabled; file hashes
  are checked again before upload and PyPI is checked afterward.
- Preserved all twelve original 0.1.2 artifacts under
  `.cache/publish-resume-0.1.2` without replacing any different existing bytes.
  `docs/handoffs/pypi-0.1.2-artifacts.json` records their hashes. This protects
  the retry set from `build.sh`, which removes and recreates `dist/`.
- Added detailed `docs/handoffs/handoff-2026-10-26-0136.md`, a live status snapshot,
  `TODO.md`, PLAN/SPEC/README updates and temporary routing in `AGENTS.md`.
  `CLAUDE.md` already includes `AGENTS.md`, so both agent entry points find it.
- New tests first failed because the tool did not exist. All 15 focused tests
  now pass: preview, hash matching/conflicts, stable-version checks, incomplete
  artifacts, HTTP 404 vs 429, credentials, changed bytes and upload failures.
- Final full suite: 202 passed in 31.26s; Ruff check/format passed. Live preview
  confirmed eight published files and four pending, without uploading anything.
- No further publish attempts, background jobs, scheduled tasks, version changes,
  commits, tags or pushes. Tomorrow's first action is a fresh preview of the
  preserved artifacts; do not assume that midnight resets a rate limit.

## PyPI retry (2026-10-26)

- Checked live PyPI JSON: four existing 0.1.2 wheels match local SHA-256;
  PhotoCraft, VectorCraft, five binary packages and the native package return 404.
- Retried existing 0.1.2 artifacts with `uv publish --check-url` and
  `UV_HTTP_RETRIES=0`. Duplicate wheels were skipped. Creating `mcruft-photocraft`
  still failed with HTTP 429: `Too many new projects created`.
- Published the four source archives for existing projects: mcruft, DeckCraft,
  DesignCraft and PdfCraft. Verified all eight wheel/sdist hashes against PyPI JSON.
- Warehouse source defaults: project creation 20/user/hour and 40/IP/hour,
  with separate attempt limits and configurable account/deployment overrides.
  These defaults do not establish this account's live quota or reset time;
  uv's error output did not expose a reset deadline.
- PhotoCraft and VectorCraft remain unpublished; no further new-project attempts,
  version bumps, rebuilds, binary uploads, commits, tags or pushes were performed.
  The unpublished `all`-extra changes remain separate from published 0.1.2 artifacts.
- Verification report: `/tmp/mcruft-pypi-retry-20261026.json`.
  No code changed, so no code tests were rerun.

## Root editable install and complete extras (2026-10-25)

- Promoted core metadata to the workspace root; kept its sources in
  `packages/mcruft/src`. Updated workspace discovery, version generation and
  metadata tests. All six wheels and sdists build, including wheels from sdists.
- Added recursive `all` extras to core and engines, a PdfCraft `native` extra,
  and empty `all` extras on native/binary distributions that have no optional deps.
- `install.sh` installs six local editables system-wide with `.[all]` and dev
  tools, searches existing `dist/` wheels, and passes `--no-config` so uv workspace
  exclusions cannot suppress the native extension or bundled CLI wheels.
- Verified the original root install command with `--dry-run`. Installed
  `mcruft[all]` from real local wheels into a clean Python 3.13 environment,
  then ran the installer against that environment via `--python`. Verified six
  editable distributions, all five bundled CLI versions, optional module imports,
  native-engine discovery and `uv pip check` (55 packages compatible).
- Tests: initial regression failed for missing root project metadata; final full
  suite passed 187 tests. After adding automatic dist lookup, the affected
  installer/metadata/bundle tests passed all 32 cases. Ruff and bash syntax pass.
- Built native abi3 and five CLI wheels, retained local copies in ignored `dist/`
  for installation. Bundles include NOTICE but were built without upstream licence
  files; these local test artifacts were not published.
- System Python was not modified. Registry-only installation still requires
  publication of all distributions; binary bundles currently target macOS arm64.

## Release tooling (2026-10-25)

- Used the existing clean `release-tooling` branch at `main`/`v0.1.0` (`f9ebd84`).
  Added six package descriptions, ignored hatch-vcs version files and version exports
  with metadata fallbacks; no generated version file is tracked.
- Added executable build/install/release/publish scripts, shared guards, CI and release
  workflows. Releases stamp the changelog before gitnextver; publishing checks archive
  metadata against the tag and loads credentials only when explicitly run.
- Fresh-clone testing exposed the old `.cache/pytest` basetemp setting: pytest failed
  without its parent directory. Removed the override to use pytest's default temp path.
- `uv sync --all-packages --all-extras` and version imports passed. `./build.sh` produced
  six wheels and six sdists, each wheel containing `__version__.py`; build left porcelain
  status unchanged. Uncommitted local builds correctly carry a development version.
- Baseline: 165 tests passed. Final gates: Ruff clean, 69 files formatted, **178 passed**.
  `bash -n`, ShellCheck, actionlint and `git diff --check` passed.
- End-to-end release ran only in a throwaway clone with a local bare origin and stubbed
  `gh`: dirty-tree refusal passed; real gitnextver committed, tagged and pushed `v0.1.1`
  there; changelog stamping, 12 release archives at `0.1.1` and clean-tree checks passed.
  Existing-release upload and version-mismatch refusal also passed. No real repository
  commit/tag/push, live release, publish, vendor edit or credential-file read occurred.
- Sandbox-only uv cache/tool directories were redirected to `/tmp`; logs are
  `/tmp/mcruft-release-transcript.log`, `/tmp/mcruft-build.log` and
  `/tmp/mcruft-release-gates.log`. Hosted workflows and authenticated uploads are untested.

## Optional native-format libraries (2026-10-25)

- Added core-only `pdf`, `svg`, `psd` and combined `libs` extras; `engines` still
  installs only product packages. Updated uv.lock and the spec, README and dependency list.
- LibEngine delegates optional PDF rendering, SVG rendering and PSD inspection to
  three small modules. Capabilities use `find_spec` and include package versions;
  verified library routes win over CLI routes without router changes.
- PDFium import, document/page/bitmap operations and cleanup share a module lock.
  SVG uses zoom = dpi/96 with the parser fixed at 96 dpi, avoiding double scaling
  physical units. PSD resolution is 16.16 fixed-point; missing metadata means 72 dpi.
- Baseline: 139 tests passed. Before implementation, the new tests had 9 expected
  failures (missing routes and CLI selection). Focused tests now pass all 25 cases:
  page ordering/names, multiple DPIs, PSD resolution/fallback, verified routing,
  absent modules, invalid page selections/DPI and PDFium lock coverage.
- Public API checks passed: multi-page PDF conversion to numbered PNGs, SVG
  `Page.render` at 96 dpi, and opening a PSD all use the library engine.
- Final gates: `uv lock` and `uv sync --all-packages --all-extras` succeeded;
  `uv run ruff check .` passed; `uv run ruff format --check .` reported 68 files
  already formatted; `uv run pytest -q` finished with **164 passed in 30.18s**.
  Used `UV_CACHE_DIR=/tmp/mcruft-uv-cache` because the default cache is outside the sandbox.
  No product packages or vendor files edited; no commit made.

## Done (MVP, branch `mvp`)

PLAN.md Tasks 1–6 are complete. Each code task passed an independent review, and the branch
passed a whole-branch review followed by one fix wave.

- **Gates:** `uv run ruff check .` and `uv run ruff format --check .` are clean. `uv run pytest -q`
  gives 138 passed and 1 skipped (the optional MCP SDK test), run against the installed ArtCraft
  CLIs: vectorcraft 0.16.0, deckcraft 0.10.0, photocraft 0.15.1, pdfcraft 0.13.0 and
  designcraft 0.12.0.
- **End-to-end checks:**
  - A document built from pptx, svg and png pages saves with previews and reloads.
  - It exports to PDF under both policies (fonts are embedded in editable and outlined in
    fidelity), and to PNG and PPTX.
  - Split, merge and both convert variants work.
- **Bundled CLI wheels:** all five products build arm64 wheels of 29–51 MB, each with a NOTICE.
  They install and run `--version`. The VectorCraft one was also found without `PATH`.
- **Metapackage:** `mcruft[engines]`, built from wheels into a clean venv, registers all seven
  engines.
- **Native binding:** `maturin build` produces an abi3 wheel. Once it is installed, the router
  sends PDF page extraction and combination to `pdfcraft-native`.

## Next

- Task 7 (publish): `mvp` is pushed as PR #1. The slop-clean pass was skipped. Merging to main and uploading to PyPI need an owner
  decision.
- Deferred minors: see the review notes summarised in the project CHANGELOG. They include:
  - Losses are not attributed to pages.
  - Some raw library errors are not wrapped in `McruftError`.
  - `engines()` checks CLIs one after another.
  - The outline pass fails on an empty document.
- Batch 2 products and the time-based media operations (SPEC §8).
