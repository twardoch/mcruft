# this_file: tools/resume_publish.py
"""Preview or resume a stable six-package release; never build, bump, tag or push.

Default: inspect the existing 0.1.2 wheels/sdists and write a local JSON report.
Pass --publish only when ready to upload missing files. Supply UV_PUBLISH_TOKEN
or PYPI_TOKEN in the environment; credentials are never written to the report.
Binary/native releases are separate and deliberately outside this tool's scope.
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGES = (
    "mcruft",
    "mcruft-deckcraft",
    "mcruft-designcraft",
    "mcruft-pdfcraft",
    "mcruft-photocraft",
    "mcruft-vectorcraft",
)
# PyPI's JSON view can lag an accepted upload by a minute or more.
VERIFY_ATTEMPTS = 6
VERIFY_DELAY = 30


def remote_files(name: str, version: str) -> dict[str, str]:
    request = urllib.request.Request(
        f"https://pypi.org/pypi/{name}/{version}/json",
        headers={"User-Agent": "mcruft-release-resume", "Cache-Control": "no-cache"},
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            data = json.load(response)
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return {}
        raise
    return {file["filename"]: file["digests"]["sha256"] for file in data["urls"]}


def plan(dist: Path, version: str) -> dict:
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise ValueError("Use a stable X.Y.Z version, never a development/local version")
    expected = [
        (name, dist / f"{name.replace('-', '_')}-{version}{suffix}")
        for name in PACKAGES
        for suffix in ("-py3-none-any.whl", ".tar.gz")
    ]
    missing = [path.name for _, path in expected if not path.is_file()]
    if missing:
        raise ValueError(f"Missing release artifacts: {', '.join(missing)}")
    remote = {name: remote_files(name, version) for name in PACKAGES}
    files = []
    for name, path in expected:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        existing = remote[name].get(path.name)
        if existing is not None and existing != digest:
            raise ValueError(f"{path.name}: PyPI has a different SHA-256; do not overwrite")
        files.append(
            {
                "filename": path.name,
                "sha256": digest,
                "state": "published" if existing is not None else "pending",
            }
        )
    return {
        "version": version,
        "checked_at": datetime.now(UTC).isoformat(),
        "files": files,
    }


def publish(report: dict, dist: Path) -> int:
    pending = [file for file in report["files"] if file["state"] == "pending"]
    if not pending:
        return 0
    token = os.environ.get("UV_PUBLISH_TOKEN") or os.environ.get("PYPI_TOKEN")
    if not token:
        raise ValueError(
            "Set UV_PUBLISH_TOKEN or PYPI_TOKEN; no credential file is read automatically"
        )
    for file in pending:
        if hashlib.sha256((dist / file["filename"]).read_bytes()).hexdigest() != file["sha256"]:
            raise ValueError(
                f"{file['filename']}: changed since preflight; inspect before retrying"
            )
    result = subprocess.run(
        [
            "uv",
            "publish",
            "--no-config",
            "--trusted-publishing",
            "never",
            "--publish-url",
            "https://upload.pypi.org/legacy/",
            "--check-url",
            "https://pypi.org/simple/",
            *(str((dist / file["filename"]).resolve()) for file in pending),
        ],
        env={
            **os.environ,
            "UV_PUBLISH_TOKEN": token,
            "UV_HTTP_RETRIES": "0",
            "UV_HTTP_TIMEOUT": "60",
        },
        check=False,
    )
    return result.returncode


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", default="0.1.2")
    parser.add_argument("--dist", type=Path, default=ROOT / "dist")
    parser.add_argument("--report", type=Path, default=ROOT / ".cache/publish-resume.json")
    parser.add_argument(
        "--publish", action="store_true", help="Upload missing files once; stop on error"
    )
    args = parser.parse_args(argv)
    try:
        report = plan(args.dist, args.version)
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2) + "\n")
        for file in report["files"]:
            print(f"{file['state']:9} {file['filename']}", flush=True)
        if not args.publish:
            print("Preview only. No uploads attempted.")
            return 0
        code = publish(report, args.dist)
        report["upload_exit_code"] = code
        args.report.write_text(json.dumps(report, indent=2) + "\n")
        for attempt in range(1, VERIFY_ATTEMPTS + 1):
            verified = plan(args.dist, args.version)
            verified["upload_exit_code"] = code
            args.report.write_text(json.dumps(verified, indent=2) + "\n")
            pending = any(file["state"] == "pending" for file in verified["files"])
            if code or not pending or attempt == VERIFY_ATTEMPTS:
                break
            time.sleep(VERIFY_DELAY)
        if code:
            print(
                "Upload stopped. Read the uv error; respect Retry-After if provided.",
                file=sys.stderr,
            )
            return code
        if pending:
            raise ValueError("Upload returned success but PyPI does not yet confirm every file")
        print(f"All {len(verified['files'])} release files verified against PyPI SHA-256.")
        return 0
    except (ValueError, OSError, urllib.error.URLError) as error:
        print(f"Cannot resume: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
