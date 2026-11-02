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

- [ ] Bench test with two UV-K1 on Labs v6.3.0: original KISS TNC against AXLink TNC, with
      AXLink (profiles `f4hwn-kisstnc` and `f4hwn-kisstnc-ackmode`).
- [x] First release with `AXLinkTNC.app` and its SHA-256 (v0.2.0-alpha.1, a prerelease: not
      yet run on a radio).
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

- [ ] When v7.0.0 is tagged: point the submodule at it, rebuild, check ABI and API level.
      The same app should load on Fusion v7 (ABI 1, overlay address `0x20000280`).
