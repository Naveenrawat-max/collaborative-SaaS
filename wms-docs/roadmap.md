---
title: "Roadmap — milestones"
tags:
  - kind/map
  - area/product
  - status/draft
---

# Roadmap — milestones

Draft order of delivery. Each milestone ends with something demoable. Live
progress goes in [[STATE]], not here. Module details: [[product]].

| Milestone | Goal (demo at the end) | Modules | Proposed owner |
|---|---|---|---|
| **M0 Foundation** | Log in as admin/manager/operator of tenant X and see only tenant X's data | scaffold (Django, React, Postgres, docker-compose, CI), [[modules/01-tenancy-users]], [[modules/02-master-data]] (admin only), audit log | all — C leads tenancy |
| **M1 Inbound MVP** | Truck arrives → goods received by barcode → put away → stock visible | [[modules/03-vehicles-yard]], [[modules/04-inbound-receiving]], [[modules/05-putaway]], [[modules/06-inventory]] core, LPN labels (PDF), CSV import | A: vehicles, inbound, putaway · B: inventory core |
| **M2 Inventory operations** | Move, adjust, count, and hold stock with approvals | [[modules/06-inventory]] (moves, adjustments, cycle counts, lots/expiry, holds) | B |
| **M3 Outbound MVP** | Order → pick → pack → load → truck leaves | [[modules/07-outbound]], gate-out, delivery note | C |
| **M4 RFID** | The same flows with RFID: portal receiving, bulk count, load verification | [[modules/08-rfid]] + gateway | B |
| **M5 Integrations & reporting** | Customer ERP pushes orders through the API; manager dashboards | [[modules/09-integrations-labels]] (API, webhooks, ZPL), [[modules/10-reporting-audit]] | shared |

## Rules
- M0 cannot start modelling until [[_meta/decisions/002-multi-tenancy]] is accepted.
- In M1–M3, owners work in parallel on separate modules. They meet at the inventory
  movement-service contract, which B publishes first ([[modules/06-inventory]]).
- Every milestone ships with the non-RFID path. RFID only comes in M4.
- Non-functional targets apply from M0: [[non-functional]].
