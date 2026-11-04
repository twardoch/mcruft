# this_file: packages/mcruft/tests/test_release_tooling.py
import builtins
import importlib
import os
import subprocess
from importlib.metadata import version
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
GUARD = ROOT / "lib/guard.sh"
MODULES = ["mcruft"] + [path.parent.name for path in (ROOT / "packages").glob("*/pyproject.toml")]


def test_installer_uses_system_editables_and_bypasses_exclusions(tmp_path):
    uv = tmp_path / "uv"
    uv.write_text('#!/bin/sh\nprintf "%s\\n" "$PWD" "$@"\n')
    uv.chmod(0o755)
    result = subprocess.run(
        ["bash", str(ROOT / "install.sh"), "--dry-run"],
        cwd=tmp_path,
        env={**os.environ, "PATH": f"{tmp_path}:{os.environ['PATH']}"},
        check=True,
        capture_output=True,
        text=True,
    )
    lines = result.stdout.splitlines()
    assert lines[0] == str(ROOT)
    assert lines[1:7] == ["pip", "install", "--system", "--upgrade", "-e", ".[all]"]
    assert "--no-config" in lines
    assert lines.count("-e") == 6
    assert ["--group", "dev"] == lines[lines.index("--group") : lines.index("--group") + 2]
    assert lines[-1] == "--dry-run"


@pytest.mark.parametrize("module", MODULES)
@pytest.mark.parametrize("fallback", [False, True])
def test_package_version_when_generated_or_missing_then_exposed(module, fallback, monkeypatch):
    package = importlib.import_module(module)
    if fallback:
        original_import = builtins.__import__

        def without_generated(name, *args, **kwargs):
            if name == "__version__":
                raise ImportError("simulate source checkout without generated version")
            return original_import(name, *args, **kwargs)

        monkeypatch.setattr(builtins, "__import__", without_generated)
    try:
        assert importlib.reload(package).__version__ == version(module.replace("_", "-"))
    finally:
        monkeypatch.undo()
        importlib.reload(package)


def test_guards_when_dirty_or_untagged_then_refuse(tmp_path):
    def git(*args):
        return subprocess.run(["git", *args], cwd=tmp_path, check=True, capture_output=True)

    def guard(name):
        return subprocess.run(
            ["bash", "-c", 'source "$1"; "$2"', "bash", str(GUARD), name],
            cwd=tmp_path,
            check=False,
            capture_output=True,
            text=True,
        )

    git("init")
    git(
        "-c",
        "user.name=Test",
        "-c",
        "user.email=test@example.invalid",
        "commit",
        "--allow-empty",
        "-m",
        "test",
    )
    assert guard("require_clean").returncode == 0
    assert guard("require_tagged_head").returncode != 0
    git("tag", "v1.2.3rc1")
    assert guard("require_tagged_head").returncode != 0
    git("tag", "v1.2.3")
    assert guard("require_tagged_head").stdout.strip() == "v1.2.3"
    (tmp_path / "dirty.txt").write_text("uncommitted")
    result = guard("require_clean")
    assert result.returncode != 0 and "?? dirty.txt" in result.stderr
