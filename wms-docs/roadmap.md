---
title: "Roadmap — milestones"
tags:
  - kind/map
  - area/product
  - status/current
---

# Roadmap — milestones

RFID is in from M1. M0–M3 together make the **pilot MVP**. M4–M5 are **Phase 2**.

- Scope per phase: [[specs/001-rfid-wms-pilot-design]] section 3
- Live progress: [[STATE]]

| Milestone | Demo at the end | Modules | Proposed owner |
|---|---|---|---|
| **M0 Foundation** | Log in to tenant X (web + C72) and see only tenant X's data. Locations are tagged and registered. A C72 is registered and reads tags in the app. | scaffold (`backend/`, `web/`, `android/`, Postgres in docker-compose, CI), [[modules/01-tenancy-users]], [[modules/02-master-data]], [[modules/08-rfid]] (registry, devices, power profiles), audit log | all — C leads tenancy, B leads RFID |
| **M1 Inbound by RFID** | Truck gated in → pallets received by RFID against the ASN → put away by pallet + location tag → stock visible per location | [[modules/03-vehicles-yard]], [[modules/04-inbound-receiving]], [[modules/05-putaway]], [[modules/06-inventory]] core (movement service), CSV import, QR stickers | A: yard, inbound, putaway · B: movement service |
| **M2 Inventory by RFID** | RFID cycle count of a zone with variances; find-a-tag; moves, adjustments, holds | [[modules/06-inventory]] operations | B |
| **M3 Outbound by RFID** → **pilot go-live** | Order → RFID pick → pack (new pallet tag) → RFID load check → dispatch → gate-out | [[modules/07-outbound]] | C |
| **M4 Dock portal** (Phase 2) | A pallet passes the dock door and is received or verified automatically | edge gateway, one LLRP portal, direction detection, stray-read filter | B |
| **M5 Integrations and dashboards** (Phase 2) | The customer's ERP pushes orders through the API; manager dashboards | [[modules/09-integrations-labels]] (API, webhooks), [[modules/10-reporting-audit]] | shared |

**Later** (not scheduled): 3PL billing and client portal, case/item tags, tag
writing, carrier self-booking, zone readers.

## Rules
- No models before [[_meta/decisions/002-multi-tenancy]] is accepted.
- B publishes the **movement service contract and the tag registry contract
  first** (M0/M1). A and C build against them.
- Every milestone ships its QR-fallback and exception paths ([[non-functional]]).
- Before go-live: site survey, power tuning, tag-placement standard, tag tests on
  the customer's products.
