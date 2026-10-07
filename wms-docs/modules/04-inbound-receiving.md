---
title: "Module 04 — Inbound & receiving"
tags:
  - kind/doc
  - area/inbound
  - status/draft
---

# Module 04 — Inbound & receiving

Getting goods from a supplier's truck into the warehouse's books. It starts when
[[modules/03-vehicles-yard]] puts the vehicle at a dock, and ends by handing
pallets to [[modules/05-putaway]].

- **Owner:** _TBD_ (proposed: dev A) · **Milestone:** M1 — see [[roadmap]]
- **Status:** draft scope

## In scope
- **ASN**: create manually, import from CSV, or receive through the API
  ([[modules/09-integrations-labels]]). Lines: item, expected qty, lot/expiry.
- **Receiving** on a handheld: scan the ASN or vehicle → scan the item → enter or
  confirm qty → lot/expiry if tracked → assign or print an **LPN** label.
- **Blind receiving** (no ASN) for walk-in deliveries.
- **Discrepancies**: over, short, or damaged quantities, with a reason code and photo (optional).
- **Quality hold**: received stock can go to a quarantine location or status.
- Close the receipt → stock is created at the dock/staging location with a `Movement` record.

## Non-RFID path
Barcode scan of the item and LPN, or manual entry of the SKU and qty. This is the default.

## RFID adds
Bulk read of all tags on a pallet passing a dock portal, compared automatically
against the ASN — see [[modules/08-rfid]].

## Key entities
`ASN`, `ASNLine`, `Receipt`, `ReceiptLine`, `Discrepancy`, `LPN`.

## Open questions
- Is a receiving tolerance (e.g. ±2% accepted without manager approval) needed?
- Cross-docking (inbound goes straight to outbound) — now or later?
- Returns (customer returns inbound) — separate flow?
