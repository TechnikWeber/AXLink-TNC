# AXLink TNC: open points

## Extensions (one commit each, with host tests)

- [x] ACKMODE (KISS command `0x0C`): the 2-byte tag kept with the waiting frame,
      `C0 0C hi lo C0` once it has left the TNC (host-tested).
- [x] Count host frames dropped while another frame waits (in `lost N`, host-tested).
- [x] Drop a frame cut off by a USB re-enumeration or a lapped ring instead of sending it
      truncated (host-tested).
- [ ] Identification on request (KISS SetHardware `0x06`): name, version, maximum frame,
      ACKMODE.
- [ ] RSSI of each received frame to the host.
- [ ] Optional: read more than 16 bytes per 10 ms poll, if the sampling loop allows it.
- [ ] Follow the DCD-over-KISS extension discussed by M0LTE and the NinoTNC designer once it
      is settled, rather than an own format.

## Tests and release

- [ ] Photos or UV Studio screen captures from a radio after the bench test, next to the
      rendered screen in the README.

- [ ] Bench test with two UV-K1 on Fusion v7 or the APRS messenger v0.4.0-beta.1: original
      KISS TNC against AXLink TNC, with
      AXLink (profiles `f4hwn-kisstnc` and `f4hwn-kisstnc-ackmode`).
- [x] First release with `AXLinkTNC.app` (in a zip) and its SHA-256 (v0.2.0-alpha.1, a
      prerelease: not yet run on a radio).
- [ ] A release without "alpha" after the bench test.
- [ ] **Entry in the UV Studio Community tab**, after the bench test: Apps → Community →
      Propose an app, with the app running on a radio (UV Studio captures its screen), a
      one-sentence English description (at most 140 characters). The name "AXLink TNC" is
      free; "KISS TNC+" would not be (names are compared as lower-case letters and digits).
- [ ] Reply in [Discussion #764](https://github.com/armel/uv-k1-k5v3-firmware-custom/discussions/764)
      once the extensions are built and tested. What we told them, and what to tell them next
      time, is kept in AXLink's
      [docs/upstream/README.md](https://github.com/TechnikWeber/AXLink/blob/main/docs/upstream/README.md).

## F4HWN v7

- [x] The submodule points at v7.0.0. Built against it, `AXLinkTNC.app` v0.2.0-alpha.1 is
      byte-identical to the release (ABI 1, API level 3 of v7's 4, overlay address
      `0x20000280`): it loads on Fusion v7 and on the APRS messenger v0.4.0-beta.1 by the
      loader's checks (2026-11-19; not yet on a radio).
- [x] As KISS TNC 1.0 of v7: the setting is staged after each key, so it survives a switch-off
      inside the app (v7 starts the app again at the next power-on).
- [x] Released with that change as v0.2.0-alpha.2 (2026-11-19).
