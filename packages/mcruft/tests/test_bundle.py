# this_file: packages/mcruft/tests/test_bundle.py
import base64
import csv
import hashlib
import importlib.util
import io
import subprocess
import sys
import zipfile
from email.parser import Parser
from pathlib import Path

import pytest


@pytest.mark.parametrize("with_licenses", [False, True])
@pytest.mark.parametrize("version", [None, "1.0.0"])
def test_bundle_when_fake_binary_then_valid_wheel_and_record(
    tmp_path, monkeypatch, capsys, with_licenses, version
):
    tool = Path(__file__).resolve().parents[3] / "tools/bundle_cli.py"
    spec = importlib.util.spec_from_file_location("bundle_cli", tool)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    monkeypatch.setattr(module.shutil, "which", lambda name: None)
    binary = tmp_path / "pdfcraft-cli"
    binary.write_text('#!/bin/sh\necho "pdfcraft-cli 0.13.0"\n')
    binary.chmod(0o755)
    licenses = tmp_path / "licenses"
    licenses.mkdir()
    (licenses / "LICENSE").write_text("Test license")
    wheel = module.bundle(
        "pdfcraft",
        binary,
        tmp_path,
        license_dir=licenses if with_licenses else None,
        version=version,
    )
    warning = capsys.readouterr().err
    assert ("warning" in warning.lower() and "license-dir" in warning) == (not with_licenses)
    expected_version = version or "0.13.0"
    assert wheel.name == f"mcruft_pdfcraft_bin-{expected_version}-py3-none-macosx_11_0_arm64.whl"
    with zipfile.ZipFile(wheel) as archive:
        info = f"mcruft_pdfcraft_bin-{expected_version}.dist-info"
        for name, digest, size in csv.reader(io.StringIO(archive.read(f"{info}/RECORD").decode())):
            if digest:
                data = archive.read(name)
                actual = (
                    base64.urlsafe_b64encode(hashlib.sha256(data).digest()).rstrip(b"=").decode()
                )
                assert digest == "sha256=" + actual
                assert int(size) == len(data)
        assert "Root-Is-Purelib: false" in archive.read(f"{info}/WHEEL").decode()
        assert "Provides-Extra: all" in archive.read(f"{info}/METADATA").decode()
        assert "Name: mcruft-pdfcraft-bin" in archive.read(f"{info}/METADATA").decode()
        metadata = Parser().parsestr(archive.read(f"{info}/METADATA").decode())
        assert metadata["Version"] == expected_version
        assert metadata["Summary"] == "Bundled pdfcraft-cli for mcruft on macOS arm64"
        assert metadata["License-Expression"] == "MIT OR Apache-2.0"
        assert metadata["Description-Content-Type"] == "text/markdown"
        assert "Documentation, https://code.twardoch.com/mcruft/" in metadata.get_all("Project-URL")
        assert "# mcruft-pdfcraft-bin" in metadata.get_payload()
        assert "uv pip install" in metadata.get_payload()
        notice = archive.read(f"{info}/NOTICE").decode()
        for expected in (
            "pdfcraft",
            "0.13.0",
            "https://github.com/storytold/pdfcraft",
            "MIT OR Apache-2.0",
            "redistributed unmodified apart from lipo thinning",
        ):
            assert expected in notice
        if with_licenses:
            assert archive.read(f"{info}/licenses/LICENSE") == b"Test license"
        assert (
            archive.getinfo("mcruft_pdfcraft_bin/bin/pdfcraft-cli").external_attr >> 16 & 0o777
            == 0o755
        )
        archive.extractall(tmp_path / "installed")
    # zipfile extraction drops executable permissions; importing the module repairs them.
    init = tmp_path / "installed/mcruft_pdfcraft_bin/__init__.py"
    check = subprocess.run(
        [
            sys.executable,
            "-c",
            (
                f"import runpy, subprocess; ns=runpy.run_path({str(init)!r}); "
                'subprocess.run([str(ns["BIN"]), "--version"], check=True)'
            ),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "0.13.0" in check.stdout


@pytest.mark.parametrize("version", ["../1.0.0", "1.0.0\nName: other", "01.0.0", "1.0", "1.0.0rc1"])
def test_bundle_when_invalid_release_version_then_refuses_before_running_binary(tmp_path, version):
    tool = Path(__file__).resolve().parents[3] / "tools/bundle_cli.py"
    spec = importlib.util.spec_from_file_location("bundle_cli", tool)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    with pytest.raises(ValueError, match="stable MAJOR.MINOR.PATCH"):
        module.bundle("pdfcraft", tmp_path / "missing", version=version)
