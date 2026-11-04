# this_file: packages/mcruft/tests/test_resume_publish.py
import hashlib
import importlib.util
import io
import json
import urllib.error
from pathlib import Path
from types import SimpleNamespace

import pytest


@pytest.fixture
def tool():
    path = Path(__file__).resolve().parents[3] / "tools/resume_publish.py"
    spec = importlib.util.spec_from_file_location("resume_publish", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def artifacts(tmp_path, tool):
    for name in tool.PACKAGES:
        for suffix in ("-py3-none-any.whl", ".tar.gz"):
            (tmp_path / f"{name.replace('-', '_')}-0.1.2{suffix}").write_bytes(b"artifact")
    return tmp_path


def test_plan_skips_matching_remote_files(tool, artifacts, monkeypatch):
    digest = hashlib.sha256(b"artifact").hexdigest()
    monkeypatch.setattr(
        tool,
        "remote_files",
        lambda name, version: {p.name: digest for p in artifacts.glob("*.whl")},
    )
    report = tool.plan(artifacts, "0.1.2")
    assert sum(f["state"] == "published" for f in report["files"]) == 6
    assert sum(f["state"] == "pending" for f in report["files"]) == 6


def test_plan_refuses_hash_conflicts(tool, artifacts, monkeypatch):
    monkeypatch.setattr(
        tool,
        "remote_files",
        lambda name, version: {p.name: "wrong" for p in artifacts.glob("*.whl")},
    )
    with pytest.raises(ValueError, match="different SHA-256"):
        tool.plan(artifacts, "0.1.2")


@pytest.mark.parametrize("version", ["../0.1.2", "0.1.3.dev0+local", "", "0.1.2rc1"])
def test_plan_refuses_nonstable_versions(tool, tmp_path, version):
    with pytest.raises(ValueError, match="stable"):
        tool.plan(tmp_path, version)


def test_plan_refuses_incomplete_artifact_set(tool, artifacts):
    next(artifacts.glob("*.whl")).unlink()
    with pytest.raises(ValueError, match="Missing"):
        tool.plan(artifacts, "0.1.2")


def test_publish_calls_uv_once_without_automatic_retries(tool, artifacts, monkeypatch):
    monkeypatch.setattr(tool, "remote_files", lambda name, version: {})
    calls = []
    monkeypatch.setenv("PYPI_TOKEN", "test-token")
    monkeypatch.delenv("UV_PUBLISH_TOKEN", raising=False)

    def run(command, **kwargs):
        calls.append((command, kwargs))
        return SimpleNamespace(returncode=2)

    monkeypatch.setattr(tool.subprocess, "run", run)
    assert tool.publish(tool.plan(artifacts, "0.1.2"), artifacts) == 2
    assert len(calls) == 1
    command, options = calls[0]
    assert "--check-url" in command and "--no-config" in command
    assert "test-token" not in command
    assert options["env"]["UV_HTTP_RETRIES"] == "0"
    assert options["env"]["UV_PUBLISH_TOKEN"] == "test-token"


def test_preview_never_uploads_or_requires_credentials(tool, artifacts, tmp_path, monkeypatch):
    monkeypatch.setattr(tool, "remote_files", lambda name, version: {})
    monkeypatch.setattr(tool, "publish", lambda *args: pytest.fail("preview tried to publish"))
    assert tool.main(["--dist", str(artifacts), "--report", str(tmp_path / "report.json")]) == 0


@pytest.mark.parametrize("status", [404, 429])
def test_remote_files_treats_only_404_as_missing(tool, monkeypatch, status):
    def unavailable(*args, **kwargs):
        raise urllib.error.HTTPError("https://pypi.org", status, "failure", {}, None)

    monkeypatch.setattr(tool.urllib.request, "urlopen", unavailable)
    if status == 404:
        assert tool.remote_files("mcruft", "0.1.2") == {}
    else:
        with pytest.raises(urllib.error.HTTPError):
            tool.remote_files("mcruft", "0.1.2")


def test_remote_files_reads_pypi_digest(tool, monkeypatch):
    payload = {"urls": [{"filename": "test.whl", "digests": {"sha256": "digest"}}]}
    monkeypatch.setattr(
        tool.urllib.request,
        "urlopen",
        lambda *args, **kwargs: io.BytesIO(json.dumps(payload).encode()),
    )
    assert tool.remote_files("mcruft", "0.1.2") == {"test.whl": "digest"}


def test_publish_refuses_changed_artifacts(tool, artifacts, monkeypatch):
    monkeypatch.setattr(tool, "remote_files", lambda name, version: {})
    monkeypatch.setenv("UV_PUBLISH_TOKEN", "test-token")
    report = tool.plan(artifacts, "0.1.2")
    (artifacts / report["files"][0]["filename"]).write_bytes(b"changed")
    monkeypatch.setattr(tool.subprocess, "run", lambda *a, **kw: pytest.fail("upload started"))
    with pytest.raises(ValueError, match="changed since preflight"):
        tool.publish(report, artifacts)


def test_publish_refuses_missing_credentials(tool, artifacts, monkeypatch):
    monkeypatch.setattr(tool, "remote_files", lambda name, version: {})
    monkeypatch.delenv("UV_PUBLISH_TOKEN", raising=False)
    monkeypatch.delenv("PYPI_TOKEN", raising=False)
    with pytest.raises(ValueError, match="Set UV_PUBLISH_TOKEN"):
        tool.publish(tool.plan(artifacts, "0.1.2"), artifacts)


def test_main_records_partial_upload_failure(tool, artifacts, tmp_path, monkeypatch):
    monkeypatch.setattr(tool, "remote_files", lambda name, version: {})
    monkeypatch.setattr(tool, "publish", lambda *args: 2)
    report_path = tmp_path / "report.json"
    assert (
        tool.main(
            [
                "--dist",
                str(artifacts),
                "--report",
                str(report_path),
                "--publish",
            ]
        )
        == 2
    )
    assert json.loads(report_path.read_text())["upload_exit_code"] == 2


def test_main_when_pypi_json_lags_then_waits_and_verifies(tool, artifacts, tmp_path, monkeypatch):
    digest = hashlib.sha256(b"artifact").hexdigest()
    lagging_passes = 3  # preflight plan plus two post-upload checks see nothing
    calls = {"n": 0}

    def remote(name, version):
        calls["n"] += 1
        if calls["n"] <= lagging_passes * len(tool.PACKAGES):
            return {}
        stem = f"{name.replace('-', '_')}-{version}"
        return {f"{stem}-py3-none-any.whl": digest, f"{stem}.tar.gz": digest}

    sleeps = []
    monkeypatch.setattr(tool, "remote_files", remote)
    monkeypatch.setattr(tool, "publish", lambda *args: 0)
    monkeypatch.setattr(tool.time, "sleep", sleeps.append)
    args = ["--dist", str(artifacts), "--report", str(tmp_path / "r.json"), "--publish"]
    assert tool.main(args) == 0, "lagging PyPI JSON must not be reported as failure"
    assert len(sleeps) == 2, f"expected two waits before verification, got {sleeps}"


def test_main_when_pypi_never_confirms_then_fails_after_bounded_waits(
    tool, artifacts, tmp_path, monkeypatch
):
    sleeps = []
    monkeypatch.setattr(tool, "remote_files", lambda name, version: {})
    monkeypatch.setattr(tool, "publish", lambda *args: 0)
    monkeypatch.setattr(tool.time, "sleep", sleeps.append)
    args = ["--dist", str(artifacts), "--report", str(tmp_path / "r.json"), "--publish"]
    assert tool.main(args) == 1
    assert len(sleeps) == tool.VERIFY_ATTEMPTS - 1, "waits must be bounded"
