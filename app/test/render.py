#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""The AXLink TNC screen as the LCD shows it, without a radio. The app's own C
code runs on the computer (host_tnc.c, which prints the drawing calls with
HOST_DRAW=1), and the firmware's drawing services with its own fonts
(../../af_lcd.py, as F4HWN's apps use it for their documentation) turn the
calls into an LCD-look PNG. The scenario: three frames from a placeholder
station, then one frame from the host; the left screen is taken while that
frame is on the air, the right one at the end. Placeholder callsigns only.

    python3 render.py OUT.png     (in a copy of App/apps: scripts/render-screens.sh)

Added for AXLink TNC (2026, TechnikWeber)."""
import os, shutil, struct, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(HERE)
APPS = os.path.dirname(APP)
sys.dont_write_bytecode = True
sys.path.insert(0, APPS)
sys.path.insert(0, os.path.join(APPS, "aprsrx", "test"))
from af_lcd import Lcd, png
from ax25 import build
from model_rx import channel, sine_wave

FEND = 0xC0

# ---- build the host harness, as test_tnc.py does ----
tmp = tempfile.mkdtemp()
api_h = os.path.join(APPS, "app_api.h")
subprocess.run([sys.executable, os.path.join(APP, "gen_assets.py"),
                os.path.join(tmp, "kisstnc_assets.bin"), os.path.join(tmp, "kisstnc_assets.h")],
               check=True, cwd=APP)
src = open(os.path.join(APP, "kisstnc_app.c")).read()
src = src.replace('__attribute__((section(".text.entry"),used))', "")
src = src.replace('#include "../app_api.h"', '#include "%s"' % api_h)
open(os.path.join(tmp, "app.c"), "w").write(src)
shutil.copy(os.path.join(HERE, "host_hw.h"), tmp)
h = open(os.path.join(HERE, "host_tnc.c")).read().replace('"../../app_api.h"', '"%s"' % api_h)
open(os.path.join(tmp, "host_tnc.c"), "w").write(h)
cc = shutil.which("clang") or shutil.which("gcc")
exe = os.path.join(tmp, "tnc")
subprocess.run([cc, "-O2", "-Wall", "-Wno-unused-function", "-I", tmp, "-o", exe,
                os.path.join(tmp, "host_tnc.c")], check=True)


def kiss(frame):
    return bytes([FEND, 0]) + frame.replace(b"\xdb", b"\xdb\xdd").replace(b"\xc0", b"\xdb\xdc") + bytes([FEND])


# ---- the scenario: placeholder callsigns only ----
adc = []
for i in range(3):
    adc += channel(sine_wave(build("N0CALL-9", info=">AXLink TNC test %d" % i)), "std", 0, 0, 0, i + 1)
host = kiss(build("N0CALL-1", dst="APZAXL", info=">from the host")[:-2])   # KISS carries no FCS
a, hb = os.path.join(tmp, "adc.bin"), os.path.join(tmp, "host.bin")
open(a, "wb").write(struct.pack("<%dH" % len(adc), *adc))
open(hb, "wb").write(host)
# The host's frame comes after the received ones (HOST_AT: from that ADC sample on).
out = subprocess.run([exe, os.path.join(tmp, "kisstnc_assets.bin"), a, hb],
                     env=dict(os.environ, HOST_DRAW="1", HOST_AT=str(len(adc))),
                     capture_output=True, text=True, check=True).stdout.splitlines()
shutil.rmtree(tmp)

# ---- replay the drawing calls; a screen ends with blit_full ----
screens, lcd, on_air = [], Lcd(), False
for line in out:
    if not line.startswith("DRAW "):
        continue
    op, _, rest = line[5:].partition(" ")
    if op == "CLEAR":
        lcd.fb = [bytearray(128) for _ in range(7)]
    elif op == "SCLEAR":
        lcd.status = bytearray(128)
    elif op == "BAT":
        lcd.battery()
    elif op == "N":
        start, end, ln, text = rest.split(" ", 3)
        lcd.print_normal(text, int(start), int(end), int(ln))
    elif op == "I":
        x, ln, sb, fill, end, text = rest.split(" ", 5)
        assert fill == "1", "af_lcd draws inverse text filled, as the app asks"
        lcd.print_inverse(text, int(x), int(ln), sb == "1", int(end))
        on_air |= text == "TX"                   # the state capsule while sending
    elif op == "BLIT":
        snap = Lcd()
        snap.status, snap.fb = bytearray(lcd.status), [bytearray(r) for r in lcd.fb]
        screens.append((on_air, snap))
        on_air = False

during = next((s for tx, s in screens if tx), None)
if during is None:
    sys.exit("no screen with the TX capsule: the scenario did not transmit")
png([during, screens[-1][1]], sys.argv[1], scale=4, cols=2)
print("wrote %s from %d screens" % (sys.argv[1], len(screens)))
