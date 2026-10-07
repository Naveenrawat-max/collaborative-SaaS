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
| Scan | Any identification event: barcode, RFID read, or manual entry | `Scan` (field `source`) |
| EPC | Electronic Product Code — the ID stored on an RFID tag | `epc` |
| Reader / antenna | RFID hardware; a reader has one or more antennas | `RfidReader`, `RfidAntenna` |
| Tag binding | Linking an EPC to an item, LPN, or location | `TagBinding` |
