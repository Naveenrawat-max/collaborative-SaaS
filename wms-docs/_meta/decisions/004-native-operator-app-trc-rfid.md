---
title: "ADR-004 — Operator app: native Kotlin on Chainway C72 with trc-rfid"
tags:
  - kind/decision
  - area/rfid
  - status/accepted
---

# ADR-004 — Operator app: native Kotlin on Chainway C72 with trc-rfid

- **Date:** 2026-10-08
- **Status:** accepted (approved with [[specs/001-rfid-wms-pilot-design]])
- **Deciders:** team

## Context
RFID is mandatory ([[specs/001-rfid-wms-pilot-design]]). Operators use
**Chainway C72** UHF handhelds. A browser can't drive the C72's RFID module, so a
web app or PWA is not an option for operators. The team already maintains
[trc-rfid](https://github.com/Naveenrawat-max/trc-rfid): `rfid-scan` (scanning
EPC+TID+RSSI) and `rfid-find` (hot/cold finding with `TagFinder`).

## Options considered
1. **Capacitor app** — React UI inside a WebView, plus a Kotlin plugin per vendor.
   One UI codebase, but adds a bridge and a WebView on a scanning device.
2. **Native Kotlin operator app + React web back office** — full SDK control and
   the best scan performance, at the cost of two UI codebases.
3. **Vendor keyboard-wedge mode** — no tag control or bulk reads. Rejected.

## Decision
**Option 2.** The operator app (`android/`) is native Kotlin with Jetpack Compose.
It depends directly on `com.github.Naveenrawat-max.trc-rfid:rfid-find:1.0.0`.
There is **no vendor abstraction layer**, because there is one vendor (Chainway).
Admins and managers use the React web app (`web/`).

## Consequences
- The app's own logic consumes `trc.rfid.scan.Tag` values. Tests and the emulator
  replay mode feed recorded `Tag` lists, so no hardware is needed for development.
- QR input comes through Chainway Keyboard Emulator in QR-only mode, with its
  **RFID output off**, because two apps cannot own the UHF module.
- Tag writing is not available (trc-rfid only reads). If needed later, it becomes a
  new `rfid-write` package in trc-rfid.
- Risks: `readOnce()` / `readMemory()` are not yet verified on a physical C72.
  The Chainway SDK licence must be confirmed for commercial use (spec risks R1, R2).
- A second handheld vendor would need a new ADR.
