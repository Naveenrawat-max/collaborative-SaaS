---
title: "Module 06 — Inventory"
tags:
  - kind/doc
  - area/inventory
  - status/draft
---

# Module 06 — Inventory

The source of truth for what stock is where. Every other module changes stock
**only** through this module's movement service (AGENTS.md invariant 4).
Terms are in [[glossary]]; tags are in [[modules/08-rfid]].

- **Owner:** _TBD_ (proposed: dev B) · **Milestone:** M1 (core), M2 (operations) — see [[roadmap]]
- **Status:** draft scope (aligned with spec-001)

## In scope (MVP)
- **Stock** per tenant × owner × location × item × lot × pallet.
  - Statuses: `available`, `quarantine`, `damaged`, `allocated`.
  - `owner` per [[_meta/decisions/006-own-warehouse-tenants-first]].
- **Movement service:** one function every module calls.
  - Atomic: `transaction.atomic` + row lock.
  - Never lets stock go negative.
  - Always writes an append-only `Movement` record.
  - Applies a `txn_id` only once.
- **RFID move:** read the pallet tag, then the destination location tag, then confirm.
- **Adjustments** with reason codes. Above a threshold, a manager approves.
- **RFID cycle count:**
  1. A manager creates a count (by zone or location).
  2. The operator sweeps the zone (**`sweep`** profile, 30 dBm).
  3. The app compares the tags read with the expected pallets: ✅ found ·
     ❌ missing · ⚠ extra or misplaced.
  4. Variances go to the manager for approval, then an adjustment is posted.
- **Find-a-tag:** look for a missing pallet with `TagFinder` (hot/cold).
- **Lot and expiry** tracking where the item requires it; FEFO for allocation.
- **Holds:** block stock (by lot, location or item) from being picked.
- **Stock enquiry:** by item, location, pallet, lot, or tag.

## Exceptions and QR fallback
- Unreadable pallet tag during a count → find it, then QR scan with a reason,
  and the tag is flagged for replacement.
- Duplicate EPC → resolved by TID or QR ([[_meta/decisions/005-tag-identity-epc-tid-qr]]).

## Key entities
`Stock`, `Movement`, `Adjustment`, `CycleCount`, `CycleCountLine`, `Hold`, `Lot`, `LPN`.

## Used by
[[modules/04-inbound-receiving]], [[modules/05-putaway]], [[modules/07-outbound]],
[[modules/10-reporting-audit]].

## Open questions
- Serial-number tracking per unit → *Later*, unless the pilot customer needs it.
- Stock valuation → not building (quantities only).
