#!/usr/bin/env bash
# this_file: publish-binary.sh
#
# Publish one binary wheel to PyPI without a token:
#   ./publish-binary.sh mcruft-deckcraft-bin 1.0.1     # bundles ~/bin/craft-cli/deckcraft-cli
#   ./publish-binary.sh mcruft-pdfcraft-native         # version from native/.../pyproject.toml
# Builds the macOS arm64 wheel here, attaches it to a draft GitHub release (no git tag),
# then dispatches .github/workflows/binaries.yml, which uploads it through Trusted
# Publishing and deletes the draft. The six pure packages use ./publish.sh instead.

set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

PKG="${1:?usage: $0 mcruft-<product>-bin VERSION | mcruft-pdfcraft-native}"
VER="${2:-}"
REPO="$(gh repo view --json nameWithOwner -q .nameWithOwner)"
OUT="$(mktemp -d)"
trap 'rm -rf "$OUT"' EXIT

case "$PKG" in
  mcruft-pdfcraft-native)
    manifest=native/mcruft_pdfcraft_native
    pinned="$(sed -n 's/^version = "\(.*\)"/\1/p' "$manifest/pyproject.toml" | head -n1)"
    if [[ -n "$VER" && "$VER" != "$pinned" ]]; then
      echo "error: $manifest/pyproject.toml pins $pinned; edit it to release $VER" >&2
      exit 1
    fi
    VER="$pinned"
    uvx maturin build --release -m "$manifest/Cargo.toml" -o "$OUT"
    ;;
  mcruft-*-bin)
    product="${PKG#mcruft-}"; product="${product%-bin}"
    [[ -n "$VER" ]] || { echo "error: give the version for $PKG" >&2; exit 1; }
    uv run python tools/bundle_cli.py "$product" --out "$OUT" --version "$VER"
    ;;
  *)
    echo "error: unknown binary package '$PKG'" >&2
    exit 1
    ;;
esac

if [[ ! "$VER" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "error: '$VER' is not MAJOR.MINOR.PATCH" >&2
  exit 1
fi
RELEASE="$PKG-v$VER"
ls "$OUT"/"${PKG//-/_}-$VER"-*.whl

gh release create "$RELEASE" "$OUT"/*.whl -R "$REPO" --draft --title "$RELEASE" \
  --notes "Staging for PyPI; deleted by binaries.yml after upload."
gh workflow run binaries.yml -R "$REPO" -f release="$RELEASE"
sleep 5
gh run list -R "$REPO" --workflow binaries.yml -L 1
echo "Follow it with: gh run watch -R $REPO"
