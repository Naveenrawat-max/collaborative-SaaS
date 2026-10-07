---
title: "Module 07 — Outbound"
tags:
  - kind/doc
  - area/outbound
  - status/draft
---

# Module 07 — Outbound

From customer order to goods on a departing truck. It allocates and picks from
[[modules/06-inventory]], and loads vehicles managed by
[[modules/03-vehicles-yard]].

- **Owner:** _TBD_ (proposed: dev C) · **Milestone:** M3 — see [[roadmap]]
- **Status:** draft scope

## In scope
- **Orders**: create manually, import from CSV, or receive through the API
  ([[modules/09-integrations-labels]]). Lines: item, qty, requested lot (optional).
  Statuses: `new → allocated → picking → packed → loaded → shipped`.
- **Allocation**: reserve available stock (FEFO for lot-tracked items) and flag shortages.
- **Waves**: a manager groups orders and releases them as pick tasks.
- **Picking** on a handheld: go to the location → scan the location → scan the
  item/LPN → confirm qty. Handle short picks with a reason.
- **Packing**: put picked goods into shipping units (cartons or pallets with an
  LPN), and print a packing list and label.
- **Shipment and loading**: link packed units to a shipment and a vehicle/dock
  appointment, and scan each unit onto the truck.
- **Dispatch**: close the shipment, generate a delivery note, then gate-out.

## Non-RFID path
Scan the location, item, and LPN barcodes (default).

## RFID adds
Load verification: a dock portal reads all tagged units going onto the truck and
flags missing or wrong ones — see [[modules/08-rfid]].

## Key entities
`Order`, `OrderLine`, `Allocation`, `Wave`, `PickTask`, `PackUnit`, `Shipment`, `Load`.

## Out of scope (for now)
Carrier rate shopping, route planning (TMS), and billing.

## Open questions
- Pick strategies needed at the start: discrete order picking only, or batch/zone too?
- Partial shipments and backorders — allowed?
