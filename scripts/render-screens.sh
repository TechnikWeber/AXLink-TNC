#!/usr/bin/env bash
# Renders the app's screen as the radio's LCD shows it, without a radio: the
# app's own code runs on the computer and the firmware's drawing services with
# its fonts (App/apps/af_lcd.py) draw the picture (app/test/render.py).
#
#   bash scripts/render-screens.sh        writes docs/images/screen.png
#
# Needs python3 and gcc or clang. Works on a copy of firmware/App/apps.
set -euo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
FW="$ROOT/firmware"
if [[ ! -f "$FW/App/apps/af_lcd.py" ]]; then
    git -C "$ROOT" submodule update --init --depth 1 firmware
fi
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
mkdir -p "$WORK/App" "$ROOT/docs/images"
cp -r "$FW/App/apps" "$WORK/App/apps"
cp "$FW/App/font.c" "$WORK/App/font.c"          # af_lcd.py reads the fonts from ../font.c
cp -r "$ROOT/app" "$WORK/App/apps/axlinktnc"
python3 "$WORK/App/apps/axlinktnc/test/render.py" "$ROOT/docs/images/screen.png"
