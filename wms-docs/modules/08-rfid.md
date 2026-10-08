---
title: "Module 08 — RFID foundation"
tags:
  - kind/doc
  - area/rfid
  - status/draft
---

# Module 08 — RFID foundation

RFID is **mandatory**. Every operator flow identifies pallets and locations by
their tags. This module owns everything the other modules rely on: the tag
registry, devices, and scan sessions.

Related notes:
- Design: [[specs/001-rfid-wms-pilot-design]]
- Identity rules: [[_meta/decisions/005-tag-identity-epc-tid-qr]]
- Handheld: [[_meta/decisions/004-native-operator-app-trc-rfid]]

- **Owner:** _TBD_ (proposed: dev B) · **Milestone:** M0–M1 — see [[roadmap]]
- **Status:** draft scope (aligned with spec-001)

## In scope (MVP)

**Tag registry** — `Tag(tenant, tid, epc, bound_type: pallet | location | vehicle, bound_id, status)`
- TID is the identity, EPC is the label ID.
- Lifecycle: `unassigned → bound → retired`, plus `conflict` when one EPC shows
  up with two TIDs.

**Tag intake**
- Tags come from the supplier as pre-encoded, pre-printed rolls.
- An optional CSV of EPC/TID pairs from the supplier is imported as `unassigned`.

**Binding**
- At receiving, the operator links the tag(s) on a pallet to that pallet.
- Location tags are bound once during warehouse setup.

**Device registry**
- Each C72 is registered to one warehouse by an admin, with an app version and a
  last-seen time.

**Power profiles** (`scanner.power` in trc-rfid, set per task)

| Profile | Start value | Use |
|---|---|---|
| `single` | 15 dBm | receive or putaway one pallet |
| `pick` | 20 dBm | picking |
| `sweep` | 30 dBm | zone count |

Values are tuned per site during the pilot.

**Find-a-tag** — hot/cold search with `TagFinder` (0–100 signal and *Very far …
Very close*), used for missing pallets.

**Scan records** — `Scan(tenant, device, user, tid, epc, source: rfid | qr, reason, txn_id, time)`
- Written by the server only when a business transaction is confirmed.
- Raw reads never reach the server.

**QR fallback**
- Format `E=<epc>;T=<tid>`, read through Keyboard Emulator in QR-only mode.
- Always logged with a reason.

## Phase 2 / Later
- **Phase 2:**
  - edge gateway (Python + `sllurp`, LLRP readers)
  - one dock portal with direction detection and stray-read filter
  - vehicle tags at the gate
  - RFID printer encoding
- **Later:**
  - tag writing on the handheld (a new `rfid-write` package in trc-rfid)
  - case and item tags (SGTIN-96)
  - zone and shelf readers

## Used by
[[modules/03-vehicles-yard]] (Phase 2 gate), [[modules/04-inbound-receiving]],
[[modules/05-putaway]], [[modules/06-inventory]], [[modules/07-outbound]].

## Open questions
- Which tag supplier is used, and can they print the TID into the QR code (spec risk R3)?
- Chainway SDK licence terms for commercial SaaS (spec risk R2).
- How long are `Scan` records retained?
