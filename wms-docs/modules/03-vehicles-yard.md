---
title: "Module 03 — Vehicles, gate & yard"
tags:
  - kind/doc
  - area/vehicles
  - status/draft
---

# Module 03 — Vehicles, gate & yard

Tracks every truck from arrival at the gate to departure, for **both** inbound and
outbound. It feeds [[modules/04-inbound-receiving]] (unload) and
[[modules/07-outbound]] (load).

- **Owner:** _TBD_ (proposed: dev A) · **Milestone:** M1 — see [[roadmap]]
- **Status:** draft scope

## In scope
- **Dock appointments**: book a time slot at a dock for an expected vehicle,
  linked to an ASN (inbound) or a shipment (outbound).
- **Gate-in**: record plate number, driver name and ID, carrier, seal number, and
  time. Match the vehicle to an appointment, or log it as a walk-in.
- **Yard**: vehicles waiting, with status (`arrived → waiting → at_dock →
  loading/unloading → done → departed`).
- **Dock assignment**: move a vehicle to a dock, mark the dock busy, release it when done.
- **Gate-out**: check paperwork and seal, record the departure time.
- Live board for managers: docks, yard queue, dwell times.

## RFID adds
Vehicle or trailer tags read at the gate for automatic gate-in/out; dock-door
portal reads confirm the vehicle is at the right dock — see [[modules/08-rfid]].

## Key entities
`Vehicle`, `Driver`, `DockAppointment`, `GateEvent`, `YardVisit`, `Dock` (from master data).

## Open questions
- Is a driver check-in kiosk or self-service needed?
- Is ANPR (number-plate camera) integration expected?
- Weighbridge integration?
