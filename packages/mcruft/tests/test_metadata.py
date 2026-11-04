# this_file: packages/mcruft/tests/test_metadata.py
import tomllib
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]


@pytest.mark.parametrize(
    "path", [ROOT / "pyproject.toml", *sorted((ROOT / "packages").glob("*/pyproject.toml"))]
)
def test_package_declares_apache_license(path):
    assert tomllib.loads(path.read_text())["project"].get("license") == "Apache-2.0"


@pytest.mark.parametrize("product", ["vectorcraft", "pdfcraft"])
def test_product_declares_direct_pdf_dependency(product):
    path = ROOT / "packages" / f"mcruft_{product}" / "pyproject.toml"
    assert "pypdf" in tomllib.loads(path.read_text())["project"]["dependencies"]


def test_root_is_installable_core_project():
    config = tomllib.loads((ROOT / "pyproject.toml").read_text())
    assert config["project"]["name"] == "mcruft"
    assert config["build-system"]["build-backend"] == "hatchling.build"


@pytest.mark.parametrize(
    "path",
    [
        ROOT / "pyproject.toml",
        *sorted(ROOT.glob("packages/*/pyproject.toml")),
        *sorted(ROOT.glob("native/*/pyproject.toml")),
    ],
)
def test_all_extra_covers_every_optional_dependency(path):
    project = tomllib.loads(path.read_text())["project"]
    extras = project["optional-dependencies"]
    assert "all" in extras

    def expand(name):
        result = set()
        for dependency in extras[name]:
            if dependency.startswith(project["name"] + "["):
                for extra in dependency.split("[", 1)[1].rstrip("]").split(","):
                    result.update(expand(extra))
            else:
                result.add(dependency.removesuffix("[all]"))
        return result

    expected = set().union(*(expand(name) for name in extras if name != "all"))
    assert expand("all") >= expected
