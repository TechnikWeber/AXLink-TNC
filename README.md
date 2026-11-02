# AXLink TNC — a KISS TNC app for F4HWN radios

<p>
  <img alt="Status: alpha" src="https://img.shields.io/badge/status-alpha-orange">
  <a href="https://github.com/TechnikWeber/AXLink-TNC/actions/workflows/ci.yml"><img alt="tests" src="https://img.shields.io/github/actions/workflow/status/TechnikWeber/AXLink-TNC/ci.yml?branch=main&label=tests"></a>
  <img alt="Platform: UV-K1 | UV-K5 V3" src="https://img.shields.io/badge/platform-UV--K1%20%7C%20UV--K5%20V3-blue">
  <img alt="Firmware: F4HWN Labs v6.3.0" src="https://img.shields.io/badge/firmware-F4HWN%20Labs%20v6.3.0-blue">
  <img alt="Protocol: KISS" src="https://img.shields.io/badge/protocol-KISS-informational">
  <a href="LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/license-Apache--2.0-green"></a>
</p>

**The Quansheng UV-K1 / UV-K5 V3 as a KISS modem that keeps up with a host sending many
frames.**

A KISS TNC overlay app for the [F4HWN firmware](https://github.com/armel/uv-k1-k5v3-firmware-custom),
for hosts such as [AXLink](https://github.com/TechnikWeber/AXLink) (IPv4 over AX.25). It is
based on the **KISS TNC** app by Johan Denoyer F4WAT, with the demodulator and modulator of the
APRS apps by Armel F4HWN. It stays a standard KISS TNC: APRSdroid and any other KISS client work
as with the original.

> **Status: alpha.** Version 0.1 behaves like KISS TNC 0.9 from F4HWN v6.3.0; only the name
> (`AXLink TNC` in the Apps menu) and the on-screen title (`AXL TNC`) differ. The extensions
> below are in progress, see [TODO.md](TODO.md). Not released yet, not yet in the UV Studio
> Community tab, not yet run on a radio.

## Planned extensions

All of them are opt-in: a host that does not use them sees the original behaviour.

- **ACKMODE** (G8BPQ's KISS extension, command `0x0C`): the app echoes the host's tag once
  the frame has been sent, so the host knows when to send the next one.
- A counter for host frames dropped because another frame was waiting.
- Drop a frame that a USB re-enumeration cut off, instead of sending it truncated.
- Identification on request (e.g. KISS SetHardware `0x06`): name, version, maximum frame
  length, ACKMODE support.
- The RSSI of each received frame for the host.

Why: the original app holds one frame from the host and reads its 256-byte USB ring at
16 bytes per 10 ms. That suits APRSdroid (one frame per beacon) but not a host that carries
IP traffic. Flow control on the USB port itself is part of the resident firmware and cannot
be done in an app; it is discussed upstream in
[Discussion #764](https://github.com/armel/uv-k1-k5v3-firmware-custom/discussions/764).
Until then AXLink paces its writes, which works with this app and with the original.

## Runs on

| Firmware | Works | Why |
|---|---|---|
| F4HWN **Labs v6.3.0** (original) | yes | overlay-app platform, API level 3 |
| F4HWN **Fusion v7** (when released) | expected | ABI 1, same overlay address; rebuilt if v7 changes the ABI |
| Fusion v6.3, other v6.3 editions | no | no app loader |

The loader checks only the ABI, the API level, the capabilities and the link address; this
build has ABI 1, API level 3, capability serial and address `0x20000280`. No messenger and
no Multiboot are needed.

## Install

1. Run F4HWN Labs v6.3.0 on the radio.
2. In [UV Studio](https://armel.github.io/uvstudio/), open **Apps → Community → Install a
   .app**, choose `AXLinkTNC.app` and a free slot.
3. On the radio: `F` + `7`, select **AXLink TNC**, `MENU`.

Screen, keys and the USB-C connection are those of KISS TNC; see [app/README.md](app/README.md).
Use a clip-on ferrite at the radio end of the USB cable when transmitting.

## Build

```sh
git clone --recurse-submodules https://github.com/TechnikWeber/AXLink-TNC.git
cd AXLink-TNC
bash scripts/build.sh        # host tests, then dist/AXLinkTNC.app
```

Needs `arm-none-eabi-gcc` (F4HWN uses the ARM GNU Toolchain 13.3.rel1), `python3`, and `gcc`
or `clang` for the host tests. `firmware/` is the F4HWN repository as a submodule at the
release tag the app targets; the build uses a copy of `firmware/App/apps` and leaves the
submodule untouched.

## Taking the code into KISS TNC

`app/` keeps the file names of `App/apps/kisstnc` in the F4HWN firmware. The first commit is
the original app, unmodified; every change after it is a separate commit. A change can be
taken over with `git format-patch` / `git am` (strip the leading `app/`), or copied file by
file. No pull request is needed for that.

## Related

- [AXLink](https://github.com/TechnikWeber/AXLink): the host software (Go, GPL-3.0).
  `internal/sim/f4hwnkiss` is a behavioural model of this app used in its tests;
  `internal/pacing` and `internal/tnc` show how a host feeds it.
- [APRS messenger fork](https://github.com/TechnikWeber/uv-k1-k5v3-aprs-firmware): a
  separate firmware with background APRS messaging; not needed for this app.

## License

Apache License 2.0, like the original: [LICENSE](LICENSE), [NOTICE](NOTICE). Modified files
carry a notice.
