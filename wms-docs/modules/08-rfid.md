---
title: "Module 08 — RFID (optional)"
tags:
  - kind/doc
  - area/rfid
  - status/draft
---

# Module 08 — RFID (optional)

Adds automation on top of the barcode flows. It is never required: a tenant with
RFID turned off loses no functionality (AGENTS.md invariant 3). Design:
[[architecture]] → scan-source abstraction.

- **Owner:** _TBD_ (proposed: dev B) · **Milestone:** M4 — see [[roadmap]]
- **Status:** draft scope

## In scope
- **Tenant setting**: RFID on or off ([[modules/01-tenancy-users]]).
- **Hardware registry**: readers and antennas, mapped to a dock door, gate, zone,
  or handheld.
- **RFID gateway**: a separate always-on process that receives tag reads,
  de-duplicates them (the same EPC is read many times per second), and posts
  `Scan` events (`source=rfid`) to the API.
- **Tag binding**: link an EPC to an item, LPN, location, or vehicle — at
  receiving, labelling, or encoding time.
- **Use cases**:
  - Inbound portal read vs ASN → [[modules/04-inbound-receiving]]
  - Putaway confirmation → [[modules/05-putaway]]
  - Bulk cycle count → [[modules/06-inventory]]
  - Load verification → [[modules/07-outbound]]
  - Gate-in/out of vehicles → [[modules/03-vehicles-yard]]
- Read-event log, with retention limits.

## Out of scope (for now)
Encoding/printing RFID labels (needs an RFID printer — check with the first
customer), and real-time location systems (RTLS).

## Key entities
`RfidReader`, `RfidAntenna`, `TagBinding`, `Scan`.

## Open questions
- Which reader brands and models do target customers use (Zebra, Impinj…)?
- Protocol: LLRP, vendor SDK, or reader HTTP/MQTT push? → ADR needed.
- Does the gateway run in the cloud, or on-site (an edge box per warehouse)?
- Tag standard: SGTIN-96 EPC encoding, or tenant-specific?
