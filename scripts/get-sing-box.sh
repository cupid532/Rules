#!/usr/bin/env bash
set -euo pipefail
VERSION="${SING_BOX_VERSION:-1.14.2}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="$ROOT/.tools"
case "$(uname -s)-$(uname -m)" in
  Darwin-arm64) NAME="sing-box-$VERSION-darwin-arm64";;
  Darwin-x86_64) NAME="sing-box-$VERSION-darwin-amd64";;
  Linux-x86_64) NAME="sing-box-$VERSION-linux-amd64";;
  Linux-aarch64) NAME="sing-box-$VERSION-linux-arm64";;
  *) echo "unsupported platform" >&2; exit 1;;
esac
URL="https://github.com/SagerNet/sing-box/releases/download/v$VERSION/$NAME.tar.gz"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
curl -fsSL -o "$TMP/sb.tar.gz" "$URL"
tar -xzf "$TMP/sb.tar.gz" -C "$TMP"
mkdir -p "$DEST"; install -m 0755 "$TMP/$NAME/sing-box" "$DEST/sing-box"
"$DEST/sing-box" version | head -1
