---
title: "Product — what the WMS does"
tags:
  - kind/doc
  - area/product
  - status/current
---

# Product — what the WMS does

A multi-tenant SaaS warehouse management system **built around RFID**. Every
pallet and every location carries a UHF tag, and operators work with Chainway C72
handhelds.

- Full design and phase table: [[specs/001-rfid-wms-pilot-design]]
- Live status: [[STATE]]
- Vocabulary: [[glossary]]

## Goal (pilot)

> One real warehouse runs its daily inbound and outbound on our WMS with every
> pallet RFID-tagged. Trucks are checked in at the gate. Pallets are received, put
> away, picked and loaded by handheld RFID scans. Stock is accurate per location
> without paper count sheets.

**Success criteria**
1. 4 weeks live with no paper fallback.
2. 100% of pallets tagged and registered.
3. Location accuracy of **≥ 99%** on an RFID cycle count.
4. **QR fallback < 2%** of transactions.
5. Zero cross-tenant access, proven by tests.

## Confirmed requirements
- **Multi-tenancy**, fully isolated ([[_meta/decisions/002-multi-tenancy]]).
  Tenants are own-warehouse businesses first, with a 3PL-ready `owner` field
  ([[_meta/decisions/006-own-warehouse-tenants-first]]).
- **Roles:** `admin`, `manager`, `operator` ([[roles-permissions]]).
- **Vehicle inbound and outbound** through gate, yard and dock.
- **RFID is mandatory.** A QR code with EPC + TID is only for exceptions, and it is
  always logged ([[_meta/decisions/005-tag-identity-epc-tid-qr]]).
- **Hardware:** Chainway C72 with the team's trc-rfid library
  ([[_meta/decisions/004-native-operator-app-trc-rfid]]).

## Modules

| # | Module | Covers | Milestone | Spec |
|---|---|---|---|---|
| 01 | [[modules/01-tenancy-users]] | tenants, users, roles, warehouse access, handheld login | M0 | — |
| 02 | [[modules/02-master-data]] | warehouses, zones, tagged locations, docks, items, partners | M0 | — |
| 03 | [[modules/03-vehicles-yard]] | appointments, gate-in/out, yard, dock assignment | M1 | — |
| 04 | [[modules/04-inbound-receiving]] | ASN, RFID receiving, discrepancies, quality hold | M1 | — |
| 05 | [[modules/05-putaway]] | putaway tasks, confirmation by pallet tag + location tag | M1 | — |
| 06 | [[modules/06-inventory]] | stock, movement service, RFID moves, RFID counts, find-a-tag, holds | M1–M2 | — |
| 07 | [[modules/07-outbound]] | orders, allocation, RFID pick, pack, RFID load check, dispatch | M3 | — |
| 08 | [[modules/08-rfid]] | tag registry, binding, devices, power profiles, QR fallback | M0–M1 | — |
| 09 | [[modules/09-integrations-labels]] | CSV import/export, QR stickers, API and webhooks (Phase 2) | M1 / M5 | — |
| 10 | [[modules/10-reporting-audit]] | audit log, reports, QR fallback rate, dashboards | M0 / M5 | — |

Add the spec link to the table when a feature spec is written in `wms-docs/specs/`.
Delivery order: [[roadmap]]. Quality targets: [[non-functional]].

## Roles

| Role | Scope | Typical actions |
|---|---|---|
| `admin` | the whole tenant | users, devices, warehouses, locations and their tags, settings |
| `manager` | assigned warehouses | plan inbound/outbound, approve adjustments and counts, resolve tag conflicts, reports |
| `operator` | assigned warehouse, on a C72 | RFID receive, putaway, move, count, pick, pack, load |

Full matrix: [[roles-permissions]]. Open question: is there a platform super-admin
above tenant admins? It is tracked in [[modules/01-tenancy-users]].

## Out of scope
Billing, accounting, transport management (route planning), labour management,
robots/automation. 3PL billing and the client portal come *Later*.
