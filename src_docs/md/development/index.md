---
this_file: src_docs/md/development/index.md
---

# Development and releases

Clone [twardoch/mcruft](https://github.com/twardoch/mcruft), then:

```bash
uv sync --locked --all-packages --all-extras
uv run ruff check .
uv run ruff format --check .
uv run pytest -q
./build.sh
```

Product tests use real CLIs when available and write into temporary directories.
The core build makes six wheels and six sdists. Native and binary artifacts are separate;
they are not rebuilt by the Linux release workflow.

## Documentation

Authored Markdown lives in `src_docs/md`; `src_docs/mkdocs.yml` configures ProperDocs and
MaterialX. The compiled dependency set is `src_docs/requirements.txt`.

```bash
uv venv .cache/docs
uv pip install --python .cache/docs/bin/python -r src_docs/requirements.txt
.cache/docs/bin/properdocs build --strict -f src_docs/mkdocs.yml
.cache/docs/bin/properdocs serve -f src_docs/mkdocs.yml
```

The strict build writes static output to `docs/`. Every push to main runs the documentation
workflow, commits that generated folder, and deploys the same output to GitHub Pages.
Pull requests build without publishing. Generated output is not the editing source.

## Releases

The six pure-Python packages derive their version from Git tags through hatch-vcs.
`./release.sh major` runs the gates, stamps the changelog and uses gitnextver to commit,
tag and push. `./publish.sh` builds and publishes a tagged release; a tag push also triggers
the hosted release workflow when its PyPI token is configured.

To release all twelve distributions, prepare the five licensed CLI bundles using
`tools/bundle_cli.py --version 1.0.0`, and build the native binding with maturin on macOS
arm64. Package versions can differ from the embedded upstream CLI version, recorded in
NOTICE. Preserve upstream licence files with `--license-dir`. Inspect metadata, hashes
and an isolated install before publication. Never overwrite a published version's bytes.

`tools/resume_publish.py` previews hash-checked recovery for the six core/engine packages;
it does not build native or CLI artifacts. Stop on a registry rate limit and preserve
exact artifacts for a later attempt.

See [agent workflow](../workflow.md) and the repository's `AGENTS.md` for contribution rules.
