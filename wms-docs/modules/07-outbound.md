---
title: "Module 07 — Outbound"
tags:
  - kind/doc
  - area/outbound
  - status/draft
---

# Module 07 — Outbound

From customer order to goods on a departing truck, with **every pick and every
loaded pallet confirmed by RFID**.

- Allocates and picks from [[modules/06-inventory]].
- Loads vehicles managed by [[modules/03-vehicles-yard]].
- Tag rules: [[modules/08-rfid]].

- **Owner:** _TBD_ (proposed: dev C) · **Milestone:** M3 — see [[roadmap]]
- **Status:** draft scope (aligned with spec-001)

## In scope (MVP)
- **Orders:** created manually or imported from CSV
  ([[modules/09-integrations-labels]]).
  Statuses: `new → allocated → picking → packed → loaded → shipped`.
- **Allocation:** reserves available stock (FEFO for lot-tracked items) and flags shortages.
- **Picking:** order by order.
  1. Go to the location.
  2. Read the location tag + pallet tag (**`pick`** profile).
  3. The app checks the pallet is the allocated one.
  4. Confirm the qty.
- **Packing:** build an outbound pallet and **bind a new tag** to it, then print a
  packing list.
- **Load check:** at the truck, read every pallet (`single` profile, one pallet at
  a time, or a sweep). The app compares the reads with the shipment: ✅ all loaded ·
  ❌ missing · ⚠ wrong pallet.
- **Dispatch:** close the shipment, generate a delivery note, then gate-out.

## Exceptions and QR fallback
- Wrong pallet picked → blocked, with the allocated pallet's location shown.
- Unreadable tag at load → QR scan with a reason.
- Short pick → reason code; the order stays partly allocated.

## Phase 2
- Dock portal: automatic load verification as pallets pass the door.
- Wave and batch picking.

## Key entities
`Order`, `OrderLine`, `Allocation`, `PickTask`, `PackUnit`, `Shipment`, `Load`, `Tag`, `Scan`.

## Out of scope
Carrier rate shopping, route planning (TMS), billing.

## Open questions
- Partial shipments and backorders allowed in the pilot?
