#!/usr/bin/env bash
# Builds AXLink TNC against the F4HWN firmware in firmware/ (a submodule at a
# release tag): runs the host tests, then packs dist/AXLinkTNC.app.
#
#   bash scripts/build.sh
#
# Needs arm-none-eabi-gcc on the PATH (F4HWN uses the ARM GNU Toolchain
# 13.3.rel1), python3 and gcc or clang. The submodule is not modified: the
# build works on a copy of firmware/App/apps in build/.
set -euo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
FW="$ROOT/firmware"
if [[ ! -f "$FW/App/apps/app_api.h" ]]; then
    git -C "$ROOT" submodule update --init --depth 1 firmware
fi
command -v arm-none-eabi-gcc >/dev/null || { echo "arm-none-eabi-gcc not on the PATH" >&2; exit 2; }

rm -rf "$ROOT/build"
mkdir -p "$ROOT/build" "$ROOT/dist"
cp -r "$FW/App/apps" "$ROOT/build/apps"
APP_DIR="$ROOT/build/apps/axlinktnc"
cp -r "$ROOT/app" "$APP_DIR"

echo "firmware: $(git -C "$FW" describe --tags --always)  toolchain: $(arm-none-eabi-gcc -dumpversion)"
echo "host tests:"
(cd "$APP_DIR" && python3 test/test_tnc.py)
echo "app:"
(cd "$APP_DIR" && bash build.sh)
cp "$APP_DIR/AXLinkTNC.app" "$ROOT/dist/"
(cd "$ROOT/dist" && sha256sum AXLinkTNC.app > AXLinkTNC.app.sha256)
cat "$ROOT/dist/AXLinkTNC.app.sha256"
