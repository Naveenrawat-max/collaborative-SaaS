---
title: "Glossary"
tags:
  - kind/doc
  - area/domain
  - status/current
---

# Glossary

Use these names in models, fields, APIs and UI (AGENTS.md invariant 5). Add a
term here **before** using it in code. Scope context: [[product]].

| Term | Meaning | Code name |
|---|---|---|
| Tenant | A customer company using the platform; all its data is isolated | `Tenant` |
| Warehouse | A physical site belonging to a tenant | `Warehouse` |
| Zone | A section of a warehouse (e.g. cold, bulk, pick face) | `Zone` |
| Location | A storage position (bin, rack slot, floor spot) with a scannable code | `Location` |
| Dock | A door where vehicles load or unload | `Dock` |
| Yard | The area where vehicles wait before or after a dock | `Yard` |
| Item / SKU | A product type that is stocked | `Item` (field `sku`) |
| Lot / batch | A group of units produced together, often with an expiry date | `Lot` |
| LPN | License Plate Number — the ID of a pallet or container | `lpn` |
| UoM | Unit of measure (each, case, pallet) | `uom` |
| ASN | Advance Shipping Notice — what a supplier says is coming | `ASN` |
| Dock appointment | A booked time slot for a vehicle at a dock | `DockAppointment` |
| Gate-in / gate-out | A vehicle entering or leaving the site, with plate, driver, and timestamps | `GateEvent` |
| Receiving | Checking arrived goods against the ASN and recording them | `Receipt` |
| Putaway | Moving received goods into a storage location | `Putaway` |
| Stock | Quantity of an item (lot) at a location | `Stock` |
| Movement | An append-only record of a stock change (from, to, qty, who, when, why) | `Movement` |
| Adjustment | A stock correction with a reason code | `Adjustment` |
| Cycle count | Counting a subset of locations to verify stock | `CycleCount` |
| Order | A customer request to ship goods (outbound) | `Order` |
| Wave | A group of orders released for picking together | `Wave` |
| Pick | Taking goods from a location for an order | `Pick` |
| Pack | Putting picked goods into shipping units | `Pack` |
| Load / dispatch | Putting packed units on a vehicle and sending it | `Load` |
| Scan | A confirmed identification recorded by the server: RFID or QR fallback | `Scan` (field `source`: `rfid` or `qr`) |
| EPC | Electronic Product Code — the label ID written in a tag's EPC memory. It can be duplicated. | `epc` |
| TID | Tag Identifier — the chip's factory serial. Unique and can't be rewritten, so it is the tag's identity. | `tid` |
| Tag registry | Every known tag (TID + EPC) and what it is bound to | `Tag` |
| Binding | Linking a tag to a pallet, location or vehicle | `Tag.bound_type`, `Tag.bound_id` |
| Tag conflict | One EPC seen with two different TIDs. Blocks use until resolved. | `Tag.status = conflict` |
| Pre-encoded roll | Tags bought with unique EPCs already written and a QR (EPC+TID) printed | — |
| QR fallback | Scanning a label's QR (`E=<epc>;T=<tid>`) when the tag won't read. Always logged with a reason. | `Scan.source = qr` |
| Power profile | Reader output power per task (`single`, `pick`, `sweep`) | `PowerProfile` |
| Find-a-tag | Hot/cold search for one tag by signal strength (trc-rfid `TagFinder`) | — |
| Device | A registered Chainway C72 handheld | `Device` |
| Tag batch | One supplier roll of tags, checked by a bench sample before use | `TagBatch` |
| Tag intake | The bench check of a roll: chip read compared with the printed QR | `TagBatch.status` (`imported`, `accepted`, `quarantined`) |
| Verified tag | A tag whose chip was proven to match its QR or its registered pair | `Tag.verified_at` |
| Last-seen | The location and time of the last confirmed transaction that read a tag | `Tag.last_seen_location`, `Tag.last_seen_at` |
| Exception | A problem a manager must look at, raised by the server; one open case per problem | `ExceptionCase` (field `kind`) |
| Wrong location | A pallet read at one location while its stock is booked at another | `ExceptionCase.kind = wrong_location` |
| Hold escape | Held or quarantined stock showing up in a pick, load or non-quarantine move | `ExceptionCase.kind = hold_escape` |
| Stuck pallet | Stock on a staging or dock location longer than the warehouse threshold | `Warehouse.stuck_after_hours` (computed, not stored) |
| Retag | Replacing a damaged tag: retire the old one and bind the new one in one step | `POST /tags/retag` |
| Pack confirm | Reading the new tag on a built pallet and checking it against its shipment | `PackUnit` status `pack_confirmed` |
| Reader / antenna | Fixed RFID hardware for dock portals (Phase 2) | `RfidReader`, `RfidAntenna` |
