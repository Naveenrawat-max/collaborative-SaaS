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
Terms: [[glossary]].

- **Owner:** _TBD_ (proposed: dev B) · **Milestone:** M1 (core), M2 (operations) — see [[roadmap]]
- **Status:** draft scope

## In scope
- **Stock** per tenant × location × item × lot (× LPN), with statuses: `available`,
  `quarantine`, `damaged`, `allocated`.
- **Movement service**: one function every module calls. It is atomic
  (`transaction.atomic` + row lock), never lets stock go negative, and always
  writes an append-only `Movement` record.
- **Internal moves**: an operator moves stock or an LPN from location A to B.
- **Adjustments** with reason codes. Above a threshold, a manager must approve.
- **Cycle counts**: a manager creates a count (by zone or location), the operator
  counts blind, variances go to manager approval, then an adjustment is posted.
- **Lot and expiry tracking** where the item requires it; FEFO for picking.
- **Holds**: block stock (by lot, location, or item) from being picked.
- Stock enquiry: by item, location, LPN, or lot.

## RFID adds
Fast cycle counts by bulk read; continuous location tracking with fixed readers
— see [[modules/08-rfid]].

## Key entities
`Stock`, `Movement`, `Adjustment`, `CycleCount`, `CycleCountLine`, `Hold`, `Lot`, `LPN`.

## Used by
[[modules/04-inbound-receiving]], [[modules/05-putaway]], [[modules/07-outbound]],
[[modules/10-reporting-audit]].

## Open questions
- Serial-number tracking (per unit) — needed by any target customer?
- Is stock valuation needed, or quantities only? (Proposed: quantities only.)
