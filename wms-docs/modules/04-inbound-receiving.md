---
title: "Module 04 — Inbound & receiving"
tags:
  - kind/doc
  - area/inbound
  - status/draft
---

# Module 04 — Inbound & receiving

Getting goods from a supplier's truck into the warehouse's books **by RFID**.

- Starts when [[modules/03-vehicles-yard]] puts the vehicle at a dock.
- Ends by handing tagged pallets to [[modules/05-putaway]].
- Tags and scan rules: [[modules/08-rfid]].

- **Owner:** _TBD_ (proposed: dev A) · **Milestone:** M1 — see [[roadmap]]
- **Status:** draft scope (aligned with spec-001 and spec-002)

## In scope (MVP)
- **ASN:** created manually or imported from CSV
  ([[modules/09-integrations-labels]]). Lines hold item, expected qty, lot/expiry,
  and owner.
- **Blind receiving** (no ASN) for walk-in deliveries.
- **Discrepancies** (over, short, damaged), each with a reason code.
- **Quality hold:** received stock can go to quarantine status.
- **Close receipt:** stock is booked at the dock/staging location through the
  movement service ([[modules/06-inventory]]).

## RFID receiving flow (handheld)
1. Pick the ASN or vehicle on the C72.
2. Pull the trigger to start a scan with the **`single`** power profile.
3. Live list: ✅ known tag on this ASN · ⚠ unexpected · 🆕 unknown tag (offer to bind).
4. For each new pallet: enter item, qty and lot, then **bind the tag** to a new pallet.
5. Confirm. The app sends one transaction:
   `POST /api/v1/receipts/{id}/confirm` with a `txn_id`, using the shared confirm
   shape from [[specs/002-rfid-checks-and-exceptions]] §6 (`task: "receive"`, no `location` needed: the server uses the
   appointment's dock).
6. The server stamps every pallet tag's last-seen at that dock.
7. Only verified tags can be bound: the tag's roll must be `accepted`, or the close read
   at bind time must match its registered EPC/TID ([[specs/002-rfid-checks-and-exceptions]] §5).

## Exceptions and QR fallback
- **Unreadable tag:** scan the label's QR code (`E=…;T=…`) and pick a reason.
  The tag is flagged for replacement.
- **Duplicate EPC (conflict):** close read for the TID, or a QR scan.
- **Missing pallet vs ASN:** re-scan → mark short with a reason.
- **Tag from a quarantined roll:** binding is refused until the tag passes an individual intake check.
- Full table: [[specs/001-rfid-wms-pilot-design]] section 6.

## Phase 2
A dock portal reads every pallet passing the door and checks it against the ASN
automatically (edge gateway).

## Key entities
`ASN`, `ASNLine`, `Receipt`, `ReceiptLine`, `Discrepancy`, `LPN` (pallet), `Tag`, `Scan`.

## Open questions
- Receiving tolerance (e.g. ±2% accepted without manager approval)?
- Customer returns → *Later*; cross-docking → not in the pilot.
