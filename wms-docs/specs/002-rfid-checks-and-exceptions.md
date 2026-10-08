---
title: "Spec-002 — RFID checks and the exception inbox"
tags:
  - kind/spec
  - area/rfid
  - status/draft
---

# Spec-002 — RFID checks and the exception inbox

Adds five checks to the pilot design in [[specs/001-rfid-wms-pilot-design]]. It
does not replace it. These came from a review on 2026-10-09 of an external
feature list and the diagram `assets/wms-feature-architecture.svg`, compared
with spec-001 and modules 01–10. Terms are in [[glossary]]; status lives in [[STATE]].

- **Owner:** team · **Status:** draft 2026-10-09 (brainstormed, awaiting review)
- **Decisions it builds on:** [[_meta/decisions/002-multi-tenancy]], [[_meta/decisions/005-tag-identity-epc-tid-qr]]
- **Picture:** `wms-docs/assets/wms-feature-architecture.svg` (grey boxes = these checks)

## 1. Goal

Catch bad tags, misplaced pallets and wrong shipments **at the moment the
handheld already reads them**. No new screens for the operator, and no
background processes. The manager gets one inbox row per problem.

Success means, during the pilot:
- No pallet goes onto the floor with a tag whose chip doesn't match its QR.
- Every pallet has a last confirmed place and time.
- A pallet read away from its booked location shows up in the inbox the same
  minute. Nobody has to start a cycle count to find it.
- Every pallet that leaves passed a pack-station read against its shipment.

## 2. What changes, by milestone

| Milestone | Adds |
|---|---|
| **M0** | Tag fields `batch`, `verified_at`, `last_seen_*` · `TagBatch` · the `exceptions` app (kinds `tag_conflict`, `intake_failed`) · CSV import · sample checks · verify on first bind |
| **M1** | One confirm shape for every task · last-seen stamping · `wrong_location` · `hold_escape` · retag · `Warehouse.stuck_after_hours` and stuck rows · exception inbox (web) |
| **M2** | Find-a-tag starts from last-seen · count lines found elsewhere raise `wrong_location` |
| **M3** | Pack confirm · `pack_mismatch` · load refuses pallets that weren't pack-confirmed |
| **M4** | The dock portal sends the same confirm request. No new rules. |

## 3. Roles

| Action | admin | manager | operator |
|---|---|---|---|
| Create a tag batch, upload CSV | ✅ | ✅ | — |
| Bench sample / full check (C72 "Tag intake" screen) | ✅ | ✅ | — |
| See the exception inbox | ✅ all warehouses | ✅ own warehouses | — |
| Resolve or dismiss an exception | ✅ | ✅ | — |
| Retag a damaged tag | ✅ | ✅ | ✅ |
| See per-tag results on the handheld (⚠ booked at A-01-03) | ✅ | ✅ | ✅ |

All checks run on the server (AGENTS.md invariant 2).

## 4. Data

All new tables are tenant-owned: they inherit `TenantModel` and get `enable_rls()`.

**`Tag`** (`rfid` app), new fields:

| Field | Type | Meaning |
|---|---|---|
| `batch` | FK → `TagBatch`, null | the supplier roll the tag came from |
| `verified_at` | datetime, null | the chip was proven to match its QR (bench) or its registered pair (first close-read bind) |
| `last_seen_location` | FK → `Location`, null | where the last confirmed transaction saw it |
| `last_seen_at` | datetime, null | when |
| `last_seen_txn` | UUID, null | which `txn_id` |

**`TagBatch`** (`rfid` app), one supplier roll:
- `reference` (the roll or lot number printed by the supplier), `supplier` (FK → `Partner`, `kind=supplier`), `warehouse`
- `status`: `imported` → `accepted` | `quarantined`. A quarantined batch that has been fully checked becomes `accepted` with `full_check=true`.
- `sample_size` (default 20, or the whole roll if smaller), `checked`, `failed`, `full_check`
- `created_by`, `created_at`
- unique `(tenant, supplier, reference)`

**`ExceptionCase`** (new `exceptions` app). The class isn't called `Exception`, because that would shadow Python's built-in. The UI and API still say "exception".
- `kind`: `tag_conflict | intake_failed | wrong_location | hold_escape | pack_mismatch`
- `warehouse`, and whichever apply: `tag`, `pallet_id`, `batch`, `expected_location`, `seen_location`
- `txn_id` (the transaction that raised it, null for M0 kinds), `data` (JSON details, never secrets)
- `seen_count` (default 1), `first_seen_at`, `last_seen_at`
- `status`: `open` → `resolved`; `resolved_by`, `resolved_at`, `resolution` (`move_to_seen | dismissed | fixed`), `note`
- `key`: a string that names the problem, e.g. `wrong_location:pallet:42`, `tag_conflict:epc:3034…01` or `intake_failed:batch:5`.
- **One open case per problem:** a partial unique constraint on `(tenant, key)` where `status='open'`. If the same problem happens again, `seen_count` goes up instead of a new row being added.
  - It uses one `key` column rather than nullable FK columns, because Postgres treats NULLs as distinct in a unique constraint. Every row would count as unique and nothing would be deduplicated.

**`Warehouse`** (`tenancy` app): `stuck_after_hours`, a positive integer, default 4.

**Not stored:**
- **Stuck pallets.** They are worked out each time the inbox is read (section 8).
- **Returnable-pallet tracking.** Later (section 11).

## 5. Tag intake: bench check (M0)

Covers risk R3 in spec-001. It runs before any tag reaches the floor. Operators never do it.

1. **Create the batch** (web): supplier, roll reference, warehouse, and the supplier's CSV (`epc,tid` per line, hex).
   - Each row becomes a `Tag` with `status=unassigned` and `batch` set.
   - A **TID already registered** in this tenant: that row is rejected and listed back in the response.
   - An **EPC already used by another TID**: both tags go to `conflict` (ADR-005) and a `tag_conflict` case opens.
   - No CSV: the batch is created empty. Its tags register when they are first bound, and sample checks compare only chip against QR.
2. **Sample** (C72 "Tag intake" screen, power profile `single`, 15 dBm):
   - The user pulls about `sample_size` tags from the start, middle and end of the roll.
   - For each tag: read the chip (EPC + TID, close read), then scan its QR (Keyboard Emulator, QR only).
   - The app sends all the pairs at once in `POST /tag-batches/{id}/checks`.
3. **Judge each pair.** It passes only if:
   - the chip's EPC and TID equal the QR's EPC and TID
   - the pair is in this batch's CSV, if the batch has one
   - the TID doesn't belong to another batch
4. **All sample tags pass:** the batch becomes `accepted`, and the checked tags get `verified_at`.
5. **Any sample tag fails:**
   - The batch becomes `quarantined`, and one `intake_failed` case opens.
   - **No tag from this batch can be bound** until it has been checked individually on the same screen.
   - A tag that passes gets `verified_at`. A tag that fails is retired with the reason `failed_intake`.
   - Once every row has been checked, the batch becomes `accepted` with `full_check=true`.
6. **Accepted, but not sampled:** binding already needs a close read (ADR-005). At the first bind the server compares the chip with the registered pair and sets `verified_at`. A mismatch refuses the bind and opens `tag_conflict`.
7. **The supplier QR has no TID** (risk R3 actually happens): the batch is created `quarantined` and goes straight to a full check. Each tag that passes gets an `E=…;T=…` sticker printed from the PDF label path ([[modules/09-integrations-labels]]).

## 6. The confirm transaction (from M1)

Every handheld task, and later the dock portal, sends one request shape:

```json
{ "txn_id": "uuid", "device_id": 7,
  "task": "receive | putaway | move | pick | count | load | pack",
  "ref": {"type": "asn | putaway_task | pick_task | count | shipment", "id": 12},
  "location": {"epc": "…", "tid": "…"},
  "tags": [{"epc": "…", "tid": "…"}],
  "qr_fallbacks": [{"epc": "…", "tid": "…", "reason": "tag_damaged"}] }
```

- `location` is the location tag read during this transaction. For `receive` and `load` it may be left out; the server then uses the dock of the appointment or shipment.
- The portal (M4) sends its dock here.
- The endpoint for each task belongs to the module that owns the task, for example `POST /receipts/{id}/confirm`. All of them run the shared steps below.

Inside the request's single database transaction, after the tags are resolved (ADR-005), in this order:

1. **The task's own work:** binding, moving stock and writing `Movement` and `Scan` rows (spec-001 §5).
2. **Last-seen.** Every resolved tag gets `last_seen_location`, `last_seen_at = now` and `last_seen_txn`.
   - `putaway` and `move` stamp the **destination**.
   - `POST /tags/resolve` is a lookup and never stamps.
3. **Wrong location.** Applies to `pick`, `count` and `load`, the tasks that don't move the pallet themselves.
   - If a pallet is booked at A but was read at B, a `wrong_location` case opens with A, B, the tag and the `txn_id`.
   - **The line still applies:** a pick takes from the pallet that's physically there, and a count records it as found elsewhere.
   - **Stock is never moved automatically.**
   - The per-tag result shows `booked_at: "A-01-03"`.
4. **Hold escape.**
   - A pallet with stock on hold or quarantine that appears in a `pick` or `load`: **that line is refused** (`result: "on_hold"`), and a `hold_escape` case opens.
   - Moving held stock to any location whose type isn't `quarantine` is refused the same way. Moving it into quarantine is allowed.
   - The other lines of the transaction still commit.
5. **Duplicates.** If an open case already exists with the same `key`, the server updates its `seen_location` and `last_seen_at` and adds one to `seen_count`.

A repeated `txn_id` returns the saved result and runs none of these steps again (spec-001 §5).

## 7. Retag and pack confirm

**Retag (M1).** `POST /tags/retag` with `{txn_id, old: {epc, tid} | {qr}, new: {epc, tid}, reason}`.
- The old tag is usually read from its QR, because it is damaged. The new tag needs a close read, so its TID is present.
- In one transaction:
  - the old tag is retired with the reason
  - the new tag is bound to the same pallet or location
  - the new tag inherits the old tag's `last_seen_*`
  - one audit event is written
- The new tag must come from an `accepted` batch, or be verified as it is bound.
- On the handheld this is a single step: "Replace damaged tag".

**Pack confirm (M3, pallets only).**
- The rule: a pack tag is read **after it has been stuck on the built pallet**, never straight from the roll.
- The pack screen reads that one tag (`single` profile) and sends `task: "pack"` with `ref.type = "shipment"`.
- In one transaction, the server binds the tag to the pack unit and checks that the pack unit belongs to this shipment. The pack unit becomes `pack_confirmed`.
- If the tag is already bound to another pack unit or shipment, that line is refused and `pack_mismatch` opens.
- At `load`, a pallet whose pack unit isn't `pack_confirmed` is refused with `result: "not_pack_confirmed"`.

## 8. Exception inbox and stuck pallets (M1)

**Stuck.** When the inbox is read, stuck rows are worked out:
- pallets whose stock sits on a location of type `staging` or `dock`
- whose latest `Movement` is older than `Warehouse.stuck_after_hours`

They are shown with `kind: "stuck"`, have no id and can't be resolved. A row disappears once the pallet moves.

**Inbox (web):**
- One list per warehouse: open cases followed by stuck rows, newest first, filterable by `kind` and `status`.
- Managers see the warehouses they were granted; admins see all of them.

**Resolving a case:**
- **Move to seen location** (`wrong_location` only): one correcting move through the movement service, with reason `location_correction`, then the case is resolved. It refuses if that would move held stock outside quarantine.
- **Dismiss with a note** (any kind), e.g. "stray read, pallet is at A". A note is required.
- `fixed`: the server sets this itself when the underlying problem goes away. For example, a quarantined batch passes its full check, or a `tag_conflict` twin is retired.

**Alerting:** `intake_failed` and `tag_conflict` show a count badge on the inbox for admins. No email (Later).

## 9. Find-a-tag (M2)

- The tag response gains `last_seen: {location: {id, code}, at}`.
- The handheld shows "last seen at A-01-03, 2 h ago" first, then `TagFinder` guides by signal strength.
- If the pallet isn't there, the operator marks it missing with a reason, which goes through module 06's missing-pallet path. Last-seen is never cleared; it stays the last fact we have.

## 10. API contract

Same conventions as the M0 API contract: `/api/v1/`, no trailing slash, no DELETE.

| Endpoint | Roles | Request → response | Milestone |
|---|---|---|---|
| `POST /tag-batches` | admin, manager | multipart `{supplier, reference, warehouse, csv?}` → `{id, status, imported, rejected: [{line, reason}]}` | M0 |
| `GET /tag-batches` · `GET /tag-batches/{id}` | admin, manager | batch rows with `checked`, `failed`, `full_check` | M0 |
| `POST /tag-batches/{id}/checks` | admin, manager | `{txn_id, checks: [{chip: {epc, tid}, qr: "E=…;T=…"}]}` (1–500) → `{batch_status, results: [{tid, passed, reason?}]}` | M0 |
| `GET /exceptions?kind=&status=&warehouse=` | admin, manager | cases + stuck rows | M0 (cases), M1 (stuck) |
| `POST /exceptions/{id}/resolve` | admin, manager | `{action: "move_to_seen" \| "dismiss", note}` → case | M1 |
| `POST /tags/retag` | all | see section 7 → `{old_tag, new_tag}` | M1 |
| task confirms (owned by modules 04–07) | per module | section 6 shape → `{results: [{epc, tid, result, booked_at?, reason?}]}` | M1–M3 |
| `GET /tags`, `GET /tags/{id}` | admin, manager | gains `batch`, `verified_at`, `last_seen` | M0 |

Errors follow the M0 contract: `400` for a broken rule (with a message the operator can read), `403` for a role, `404` for a missing row or another tenant's row.

## 11. Out of scope

From the external review, and agreed on 2026-10-09:
- **Returnable pallets.** Later. Last-seen already holds the data the rule would need ("left on a load, not back after N days").
- **Carton and item tags.** Later, as in spec-001.
- **Forklift-mounted readers.** A stray read from the next aisle would move stock without anyone seeing it, so putaway stays a two-tag handheld confirm.
- **Writing tags.** ADR-005: the MVP only reads and binds.
- **Live floor map.** Passive door and handheld reads can't give shelf-level real-time positions; last-seen is the honest version.
- **Sensor tags, Kanban, IT-asset tracking, customer returns, slotting, stockout dashboards.**
- **Email alerts.** There's no email set up yet.

The read-rate risk R4 (metal, liquids, antenna placement) is still handled by power profiles, the tag-placement standard and the target of under 2% QR fallback. No module is added for it.

## 12. Acceptance criteria

M0:
- [ ] A CSV row whose TID is already registered is rejected and listed. The other rows import.
- [ ] A sample with one mismatched pair quarantines the batch and opens exactly one `intake_failed` case.
- [ ] A tag from a quarantined batch can't be bound until it passes an individual check.
- [ ] A batch whose rows have all been checked becomes `accepted` with `full_check=true`, and its `intake_failed` case becomes `fixed`.
- [ ] The first close-read bind of an unsampled tag sets `verified_at`. A chip that doesn't match its registered pair is refused and opens `tag_conflict`.
- [ ] Cross-tenant: tenant B can't list, check or read tenant A's batches or cases (404 or an empty list).

M1–M3:
- [ ] A pick from a pallet booked elsewhere applies, opens one `wrong_location` case and shows `booked_at`. A second pick from the same pallet only adds one to `seen_count`.
- [ ] A held pallet in a pick has its line refused, while the other lines in the same `txn_id` commit.
- [ ] "Move to seen location" writes exactly one `Movement` with reason `location_correction` and resolves the case.
- [ ] Dismissing without a note returns 400.
- [ ] A pallet on a staging location shows as stuck after `stuck_after_hours` and disappears after a move.
- [ ] Retag is all-or-nothing: if binding the new tag fails, the old tag is not retired.
- [ ] Load refuses a pallet that wasn't pack-confirmed. A pack read of a tag bound to another shipment opens `pack_mismatch`.
- [ ] Every confirm stamps `last_seen_*` on each tag it resolved. A replayed `txn_id` doesn't stamp again.
- [ ] Cross-tenant tests for every new endpoint.

## 13. Notes to update after approval

- [[modules/04-inbound-receiving]]: receive confirm uses the shared shape and stamps last-seen.
- [[modules/06-inventory]]: wrong-location from counts, hold escape, find-a-tag starting from last-seen, correcting movement reason.
- [[modules/07-outbound]]: pack confirm, the `pack_confirmed` status, load refusal.
- [[modules/08-rfid]]: tag intake, `TagBatch`, verification, retag, last-seen.
- [[modules/10-reporting-audit]]: exception inbox.
- [[glossary]]: Exception (case), TagBatch, last-seen, stuck, retag, pack confirm.
- [[roadmap]]: the milestone table in section 2.
- [[plans/2026-10-08-m0-backend]]: add the M0 rows from section 2.
- [[STATE]]: what's next.

## 14. Open questions

- Is a sample size of 20 right for the supplier's roll size? Confirm once the supplier is chosen (pilot prep, R3).
- Is the 4-hour stuck threshold right for the pilot site? It can be set per warehouse, so this is a tuning question, not a design one.
