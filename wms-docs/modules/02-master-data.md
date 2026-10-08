---
title: "Module 02 — Master data"
tags:
  - kind/doc
  - area/master-data
  - status/draft
---

# Module 02 — Master data

The reference data every flow uses: where things are stored, what is stored, and
who we deal with. Terms: [[glossary]]. Tenant-scoped per
[[_meta/decisions/002-multi-tenancy]].

- **Owner:** _TBD_ (proposed: dev B) · **Milestone:** M0 — see [[roadmap]]
- **Status:** draft scope

## In scope
- **Warehouse → Zone → Location** hierarchy. Each location has a code and an **RFID
  tag with a QR label**, bound during setup ([[modules/08-rfid]]), a type (rack, floor, dock, staging, quarantine), and optional capacity.
- **Docks** per warehouse (inbound, outbound, or both).
- **Items (SKUs)**: description, UoM, conversions (each/case/pallet), barcodes
  (GTIN/SKU codes for lookup), whether lot or expiry is tracked, dimensions and weight.
- **Partners**: suppliers, customers, carriers.
- Bulk import from CSV for locations and items.
- Initially managed through the Django admin. Proper screens come later.

## Out of scope (for now)
Pricing, cost, item images, kitting/BOM.

## Key entities
`Warehouse`, `Zone`, `Location`, `Dock`, `Item`, `ItemBarcode`, `UomConversion`, `Partner`.

## Used by
[[modules/03-vehicles-yard]], [[modules/04-inbound-receiving]],
[[modules/05-putaway]], [[modules/06-inventory]], [[modules/07-outbound]],
[[modules/08-rfid]].

## Open questions
- Location code format: tenant-defined, or a fixed pattern (e.g. `A-01-02-3`)?
- Do we need multiple owners of stock in one warehouse (3PL client ownership)?
