---
title: "ADR-005 — Tag identity: TID + EPC, QR fallback carries both"
tags:
  - kind/decision
  - area/rfid
  - status/accepted
---

# ADR-005 — Tag identity: TID + EPC, QR fallback carries both

- **Date:** 2026-10-08
- **Status:** accepted (approved with [[specs/001-rfid-wms-pilot-design]])
- **Deciders:** team

## Context
- Pallets and locations carry passive UHF tags (see [[modules/08-rfid]]).
- Tags are bought **pre-encoded and pre-printed**, and the WMS only reads them
  ([[_meta/decisions/004-native-operator-app-trc-rfid]]).
- The EPC (the ID written in the tag) can be duplicated by a supplier mistake or a
  cloned tag. The TID (the chip's factory serial) is unique and can't be rewritten.
- Reads at a distance often get the EPC without the TID.
- A fallback is needed for tags that won't read.

## Options considered
1. **EPC only.** Simple, but duplicate EPCs go undetected.
2. **TID only.** Unique, but bulk reads at a distance often miss the TID.
3. **TID = identity, EPC = label ID, both stored.**

## Decision
**Option 3.**

**Registry**
- `Tag(tenant, tid, epc, bound_type, bound_id, status)`.
- `unique(tenant, tid)`. The EPC is indexed but not unique.
- An EPC seen with two different TIDs gets status `conflict`.

**Matching**
- Match by EPC.
- If the EPC is in `conflict`, require a close read (which gets the TID) or a QR scan.

**QR fallback**
- Every label carries a QR code: `E=<epc hex>;T=<tid hex>`, e.g.
  `E=3034257BF7194E4000000001;T=E2801160200074CF085C09A1`.
- Every QR use is logged with a reason (`tag_damaged`, `no_read`, `conflict`).
- QR is never a normal path: the QR fallback rate is a success metric (< 2%).

**Writing tags (not in the MVP)**
- If the WMS ever writes tags: use SSCC-96 when the tenant has a GS1 company
  prefix, otherwise a private closed-loop scheme. Decide that in a new ADR then.

## Consequences
- Supplier requirement: read each chip's TID during encoding and print it in the QR.
- If the supplier can't do that, print the QR as a PDF sticker on site at binding
  time (spec risk R3).
- Tag lifecycle: `unassigned → bound → retired`.
- A damaged tag is retired, and its pallet is rebound to a new tag.
