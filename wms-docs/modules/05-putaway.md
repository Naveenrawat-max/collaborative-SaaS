---
title: "Module 05 — Putaway"
tags:
  - kind/doc
  - area/putaway
  - status/draft
---

# Module 05 — Putaway

Moving received pallets from dock/staging into storage locations. Input comes from
[[modules/04-inbound-receiving]]; every move writes a `Movement` record in
[[modules/06-inventory]].

- **Owner:** _TBD_ (proposed: dev A) · **Milestone:** M1 — see [[roadmap]]
- **Status:** draft scope

## In scope
- **Putaway tasks** generated when a receipt closes (one per LPN or line).
- **Location suggestion**, simple to start: a fixed home location per item, else
  the first empty location in the item's zone.
- Operator flow: scan the LPN → see the suggested location → go → scan the location
  to confirm. Override with a reason if the location is full.
- Task list for operators, and a progress view for managers.

## Non-RFID path
Scan the LPN barcode and the location barcode (default).

## RFID adds
Automatic confirmation when a tagged pallet is read at a location or zone antenna
— see [[modules/08-rfid]].

## Key entities
`PutawayTask`, `Movement`, `Location`.

## Out of scope (for now)
Optimised slotting (velocity-based), capacity calculation by volume and weight.

## Open questions
- Should suggestions respect capacity from day one, or only "empty / not empty"?
