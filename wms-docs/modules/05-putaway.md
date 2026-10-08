---
title: "Module 05 — Putaway"
tags:
  - kind/doc
  - area/putaway
  - status/draft
---

# Module 05 — Putaway

Moving received pallets from dock/staging into storage, **confirmed by reading
two tags**: the pallet's tag and the location's tag.

- Input comes from [[modules/04-inbound-receiving]].
- Every move writes a `Movement` record through [[modules/06-inventory]].

- **Owner:** _TBD_ (proposed: dev A) · **Milestone:** M1 — see [[roadmap]]
- **Status:** draft scope (aligned with spec-001)

## In scope (MVP)
- **Putaway tasks** are created when a receipt closes, one per pallet.
- **Location suggestion:** the item's fixed home location, otherwise the first
  empty location in the item's zone.
- Operator task list, and a progress view for managers.

## RFID putaway flow (handheld)
1. Read the pallet tag (**`single`** profile) → the app shows the suggested location.
2. Drive there and read the **location tag**.
3. If it matches → confirm. If it's a different location → the operator picks a
   reason (location full or blocked).
4. One transaction: `POST /api/v1/putaway-tasks/{id}/confirm` with a `txn_id`.

## Exceptions and QR fallback
- Location tag unreadable → scan the location's QR label, with a reason.
- Several pallet tags read → keep only the selected pallet; stray reads are ignored.

## Key entities
`PutawayTask`, `Movement`, `Location`, `Tag`.

## Out of scope (for now)
Slotting optimisation, capacity by volume and weight.

## Open questions
- Should suggestions respect location capacity from day one, or only "empty / not empty"?
