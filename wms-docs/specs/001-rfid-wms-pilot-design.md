---
title: "Spec-001 — RFID WMS pilot: goal, scope and design"
tags:
  - kind/spec
  - area/product
  - status/current
---

# Spec-001 — RFID WMS pilot: goal, scope and design

The master design for the first release. It came out of a brainstorming session
on 2026-10-08, which researched how real RFID warehouses work (sources at the
bottom). Supersedes the "RFID optional" assumption in older notes. Status lives in
[[STATE]]; terms are in [[glossary]].

- **Owner:** team · **Status:** approved 2026-10-08
- **Decisions:** [[_meta/decisions/003-api-drf]], [[_meta/decisions/004-native-operator-app-trc-rfid]],
  [[_meta/decisions/005-tag-identity-epc-tid-qr]], [[_meta/decisions/006-own-warehouse-tenants-first]], plus
  [[_meta/decisions/001-stack-django-react]] and [[_meta/decisions/002-multi-tenancy]]

---

## 1. Understanding

**What the team said**
- Multi-tenant SaaS WMS with the roles `admin`, `manager`, `operator`.
- Vehicle inbound and outbound, plus the standard WMS flows.
- **RFID is mandatory.** The fallback for exceptions is a **QR code carrying both
  EPC and TID**.
- Tenants: **own-warehouse businesses first**. 3PL support (stock owned by many
  clients) comes later, without a rewrite.
- Handheld: **Chainway C72**, using the team's own library
  [trc-rfid](https://github.com/Naveenrawat-max/trc-rfid) (`rfid-scan` + `rfid-find`).
- Operator app: **native Android (Kotlin)**. Back office: **React web**. Backend:
  **Django + PostgreSQL**.
- First release target: a **pilot with a real customer**.

**Assumed (correct these if wrong)**
- Passive UHF Gen2 tags, on pallets and locations.
- One pilot tenant, one warehouse site, a few C72 handhelds.
- The warehouse has Wi-Fi coverage, with possible short drops.

## 2. Goal

> **Pilot go-live:** one real warehouse runs its daily inbound and outbound on our
> WMS with every pallet RFID-tagged. Trucks are checked in at the gate. Pallets are
> received, put away, picked and loaded by handheld RFID scans. Stock is accurate per
> location without paper count sheets.

### Success criteria
1. 4 consecutive weeks of live operation with no paper fallback.
2. 100% of pallets in the warehouse carry a tag registered in the WMS.
3. Location-level inventory accuracy of **≥ 99%** on an RFID cycle count.
4. **QR fallback < 2%** of transactions (a health indicator for the RFID setup).
5. Zero cross-tenant data access, proven by automated tests.

### What gets tagged
- **MVP:** pallets (also called LPNs) and storage locations.
- **Later:** cases and items (SGTIN-96). The data model allows them from the start.

## 3. Scope by phase

✅ MVP (pilot) · 🔜 Phase 2 · 🕐 Later · ❌ Not building

| Area | ✅ MVP | 🔜 Phase 2 | 🕐 Later | ❌ Not building |
|---|---|---|---|---|
| Tenancy and users | tenants, users, 3 roles, warehouse access, handheld login (username + PIN), audit log | — | SSO, multi-language | custom role builder |
| Master data | warehouse → zone → location (tagged), docks, items (SKU/GTIN, UoM, lot/expiry flag), suppliers/customers/carriers, `owner` field (defaults to the tenant), CSV import | — | — | pricing, costing |
| RFID foundation | **tag registry** (EPC + TID, lifecycle), **binding pre-encoded, pre-printed tags** to pallets and locations, **device registry**, **power profiles per task**, find-a-tag (`TagFinder`) | RFID printer encoding, vehicle tags at the gate | writing tags on the handheld (needs a new `rfid-write` package in trc-rfid), case/item tags | active tags, RTLS |
| Vehicles and yard | dock appointments (booked by a manager), gate-in/out (plate, driver, seal, times), yard status, dock assignment, dock board | — | carrier self-booking portal | weighbridge, ANPR |
| Inbound | ASN (manual or CSV), **RFID bulk receiving checked against the ASN**, blind receiving, discrepancies with reasons, quality hold | **dock portal: automatic receiving** | customer returns | EDI |
| Putaway | putaway task, simple suggestion (home location, otherwise first empty location in the zone), **confirm by reading the pallet tag + location tag** | — | — | slotting optimisation |
| Inventory | stock per location/lot/pallet, **single movement service**, RFID moves, adjustments with approval, **RFID cycle count** (zone read compared with expected), find-a-tag, holds, lot/expiry with FEFO | — | serial numbers | stock valuation |
| Outbound | orders (manual or CSV), FEFO allocation, order-by-order picking, **pick confirmed by RFID read**, building packed pallets, **load check: handheld read compared with the shipment**, dispatch with delivery note, gate-out | **dock portal: automatic load verification**, wave and batch picking | — | TMS, carrier rate shopping |
| Exceptions | full table in section 6; **QR (EPC+TID) fallback with a logged reason** | — | — | — |
| Integrations and labels | CSV import/export, PDF QR stickers (an on-site fallback label path) | REST API and webhooks for ERP | 3PL client portal | built-in ERP connectors |
| Reporting | stock on hand, movement history, receipts and shipments, count accuracy, **QR fallback rate** | dashboards, reader health | 3PL activity billing | custom report builder |
| Edge | — | **edge gateway** (Python + `sllurp`, LLRP readers), one dock portal, direction detection, stray-read filter, offline buffer | zone and shelf readers | robots, conveyors, AGVs |

## 4. Architecture

```
 Operator: Chainway C72                      Back office: desktop browser
 ┌───────────────────────────────┐           ┌───────────────────────┐
 │ Native Kotlin app (Compose)   │           │ React web app         │
 │  screens → domain logic       │           │ admin + manager       │
 │  trc-rfid: RfidScanner,       │           └──────────┬────────────┘
 │            TagFinder          │                      │
 │  QR via Keyboard Emulator     │                      │
 └──────────────┬────────────────┘                      │
                └────────── HTTPS JSON /api/v1 ─────────┘
                       Django + DRF, single movement service
                                    │
                                PostgreSQL
                                    ▲
        Phase 2: edge gateway (Python + sllurp, on-site mini-PC)
                 LLRP dock readers → filter → events → API
```

**Repo layout:** `backend/` (Django), `web/` (React), `android/` (Kotlin),
`gateway/` (Phase 2), `wms-docs/`.

### Operator app
- Depends on `com.github.Naveenrawat-max.trc-rfid:rfid-find:1.0.0` (pulls in
  `rfid-scan` and the Chainway SDK). There is **no vendor abstraction layer**,
  because there is only one vendor.
- The app's own logic consumes `Tag(epc, tid, rssi)` values. Unit tests and an
  emulator **replay mode** feed recorded `Tag` lists into the same handler, so no
  hardware is needed for development.
- **QR input:** Chainway Keyboard Emulator in QR-only mode (**RFID output off**,
  because two apps cannot own the UHF module) types the code into the app's
  focused input field.
- **Power profiles** set `scanner.power` per task. Starting values (tuned on site):

  | Task | Power |
  |---|---|
  | Single-pallet receive or putaway | 15 dBm |
  | Picking | 20 dBm |
  | Zone count | 30 dBm |

### Backend
- Django + DRF, tenant scoping per [[_meta/decisions/002-multi-tenancy]].
- **Every** stock change goes through the movement service: one transaction, row
  lock, never negative, and an append-only `Movement` record.

### Auth
- **Back office:** session login.
- **Handheld:**
  1. An admin registers the device to one warehouse.
  2. The operator logs in with username + PIN.
  3. The app receives a short-lived token.

## 5. RFID data flow and tag identity

### Rule: raw reads never reach the server
1. `RfidScanner.onTag` delivers raw reads, many per second per tag.
2. The app de-duplicates them per session by EPC, and attaches the TID as soon as one
   read delivers it (the same pairing `TagFinder` uses). It matches them **live** against the expected list (the ASN, pick list or
   shipment) and shows ✅ matched, ⚠ unexpected, ❌ missing.
3. The operator confirms. The app sends **one business transaction**, e.g.
   `POST /api/v1/receipts/{id}/confirm`:
   ```json
   { "txn_id": "uuid", "device_id": "C72-07",
     "tags": [{"epc": "3034…01", "tid": "E280…A1"}],
     "qr_fallbacks": [{"epc": "3034…02", "tid": "E280…B2", "reason": "tag_damaged"}] }
   ```
4. The server does everything in one DB transaction:
   1. Resolves tags in the registry, within the same tenant.
   2. Binds or creates pallets.
   3. Calls the movement service.
   4. Writes `Scan` records (`source = rfid | qr`).
   5. Returns a result per tag.
5. **Safe retry:** the same `txn_id` is applied only once. The device queues it
   and retries after a network drop.

The Phase 2 gateway follows the same rule: filter at the dock and send events, not
reads.

### Tag registry
`Tag(tenant, tid, epc, bound_type: pallet | location | vehicle, bound_id, status)`

| Rule | Detail |
|---|---|
| Identity | The **TID** (chip factory serial, cannot be rewritten). Unique per tenant. |
| Label ID | The **EPC**. Indexed, but not unique at DB level. If one EPC appears with two TIDs, it gets status `conflict`. |
| Matching | Match by EPC, because bulk reads at a distance often miss the TID. If the EPC is in `conflict`, require a close read (gets the TID) or a QR scan. |
| Lifecycle | `unassigned → bound → retired`. A damaged tag is retired, and its pallet is rebound to a new tag. |
| Writing tags | Not in the MVP; the WMS only reads and binds. If a tag must be written later, use SSCC-96 when the tenant has a GS1 company prefix, otherwise a private closed-loop scheme (to be decided in ADR-005). |

### Labels and QR
- **Format:** `E=<epc hex>;T=<tid hex>`, e.g.
  `E=3034257BF7194E4000000001;T=E2801160200074CF085C09A1`.
- **Source:** tag rolls bought **pre-encoded and pre-printed**. The supplier reads
  each chip's TID while encoding and prints a QR code with both EPC and TID.
- **If the supplier can't print the TID:** the first read on site, at binding
  time, prints a QR sticker from a PDF on a normal label printer (risk R3).

## 6. Exceptions

Every exception is shown on the handheld and logged. None is silently dropped.

| Case | Handling |
|---|---|
| Unknown tag (not in the registry) | Receiving: offer "bind to this pallet". Elsewhere: ⚠ shown, not booked. |
| Duplicate EPC (same EPC, different TID) | Blocked. Needs a close read (TID) or a QR scan. The registry marks the EPC `conflict` and the admin is alerted. |
| Unexpected tag (not on the ASN or pick list) | ⚠ shown. The operator deselects it, or a manager overrides with a reason. |
| Missing tag (expected, not read) | Re-scan → find with `TagFinder` → QR scan → or mark short with a reason. |
| Unreadable tag | QR fallback with a reason. The tag is flagged for replacement. |
| Stray reads (neighbouring pallets) | Low-power profile for the task. The operator confirms only the selected pallets. |
| Network drop | Queued on the device and retried with the same `txn_id`. A "pending sync" banner shows. |
| Stock conflict (moved or allocated by someone else meanwhile) | The server rejects that line with a reason, and the app shows it. |
| Reader unavailable (e.g. Keyboard Emulator owns the module) | "Reader unavailable" plus a reconnect button. trc-rfid auto-reconnects. |

## 7. Testing

- **Backend (pytest):**
  - a cross-tenant test per endpoint
  - movement service: never negative, all-or-nothing, a retried `txn_id` is applied once
  - duplicate-EPC handling
- **Android (JUnit):**
  - de-duplication, matching against expected lists, exception rules
  - inputs are recorded `Tag` lists
  - replay mode for demos
  - manual checklist on a physical C72 before each release
- **Web:** Playwright smoke tests of the main manager flows.
- **CI:** GitHub Actions runs backend tests, Android unit tests and lint on every PR.
- **Before go-live:**
  - site survey
  - power tuning per task
  - written tag-placement standard (outermost pallet face, fixed position)
  - tag tests on the customer's real products (metal and liquids especially)

## 8. Risks

| # | Risk | Mitigation |
|---|---|---|
| R1 | `readOnce()` / `readMemory()` in trc-rfid are not yet verified on a physical C72 | Verify on a device before building on them. The MVP only depends on `startScan` + `onTag`. |
| R2 | trc-rfid publicly redistributes the Chainway SDK | Confirm Chainway's licence terms for commercial SaaS use before the pilot. |
| R3 | The tag supplier can't print the TID in the QR code | Fallback: print the QR sticker on site at binding (PDF). |
| R4 | Stray reads and tags on metal or liquid products | Power profiles, placement standard, product tag tests before go-live. |
| R5 | Wi-Fi gaps between racks | Retry queue with `txn_id`. A site Wi-Fi survey is part of pilot prep. |
| R6 | 3PL requirements arriving later | `owner` field on stock from day one (ADR-006). |

## 9. Decisions to record (ADRs, written after approval)

| ADR | Decision |
|---|---|
| 003 | API layer: Django REST Framework |
| 004 | Operator app: native Kotlin on Chainway C72, using trc-rfid. Back office in React. |
| 005 | Tag identity: TID = identity, EPC = label ID. QR format `E=…;T=…`. EPC scheme only needed if we ever write tags. |
| 006 | Tenants: own-warehouse first. `owner` field on stock prepares for 3PL. |

## 10. Notes to update after approval

| File | Change |
|---|---|
| `AGENTS.md` | Rule 3: RFID mandatory, QR (EPC+TID) only for exceptions and always logged. PR checklist and spec template updated. |
| [[product]] | Goal, success criteria, phase table. Remove "optional". |
| [[architecture]] | Section 4 of this spec. |
| `modules/*` | `08-rfid` rewritten. RFID steps and exceptions added to inbound, putaway, inventory and outbound. |
| [[roadmap]] | RFID in from M1. M4 = gateway + dock portal. 3PL moved to Later. |
| [[roles-permissions]] | Tag binding, device registry, power profiles, duplicate-tag resolution. |
| [[non-functional]] | Native app (not a PWA), RFID and QR targets, retry queue. |
| [[glossary]] | TID, QR fallback, power profile, tag registry, pre-encoded roll. |

## Sources

[ShipBob RFID WMS guide](https://www.shipbob.com/blog/rfid-warehouse-management-system/) ·
[Inbound Logistics — 9 WMS must-haves](https://www.inboundlogistics.com/articles/9-wms-must-haves) ·
[RFID4U dock door portals](https://rfid4u.com/enabling-your-dock-doors-with-rfid/) ·
[Inbound Logistics — YMS](https://www.inboundlogistics.com/articles/say-yes-to-the-yms/) ·
[Atlas RFID — SGTIN-96](https://www.atlasrfidstore.com/rfid-insider/what-is-the-sgtin96/) ·
[GS1 RFID encoder API](https://rfidcoder.gs1.org/ui/apidoc) ·
[Datex — 3PL WMS](https://datexcorp.com/what-3pls-should-look-for-in-a-wms/) ·
[DecisionPoint — RFID pitfalls](https://www.decisionpt.com/resources/insights/rfid-implementation-pitfalls-warehouse-distribution-center/) ·
[CPCON — warehouse RFID deployment](https://cpcongroup.com/insights/article/warehouse-rfid-deployment/) ·
[trc-rfid](https://github.com/Naveenrawat-max/trc-rfid)
