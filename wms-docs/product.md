---
title: "Product — what the WMS does"
tags:
  - kind/doc
  - area/product
  - status/draft
---

# Product — what the WMS does

A multi-tenant SaaS warehouse management system for businesses that run one or
more warehouses, with optional RFID. The live status is in [[STATE]]; the
vocabulary is in [[glossary]].

## Confirmed requirements

- **Multi-tenancy.** Many customer companies (tenants) on one deployment, fully
  isolated — see [[_meta/decisions/002-multi-tenancy]].
- **Roles:** `admin`, `manager`, `operator`.
- **Vehicle inbound and outbound.** Trucks arrive, are unloaded or loaded at docks, and leave.
- **Standard WMS functions** that an RFID-enabled business needs.
- **RFID is optional.** A tenant without RFID readers uses barcode or manual entry
  for every flow.

## Modules (draft — proposed scope, confirm with the team)

| # | Module | Covers | Milestone | Spec |
|---|---|---|---|---|
| 01 | [[modules/01-tenancy-users]] | tenants, users, roles, warehouse access | M0 | — |
| 02 | [[modules/02-master-data]] | warehouses, zones, locations, docks, items, partners | M0 | — |
| 03 | [[modules/03-vehicles-yard]] | appointments, gate-in/out, yard, dock assignment | M1 | — |
| 04 | [[modules/04-inbound-receiving]] | ASN, receiving, discrepancies, quality hold | M1 | — |
| 05 | [[modules/05-putaway]] | putaway tasks, location suggestion | M1 | — |
| 06 | [[modules/06-inventory]] | stock, movement service, moves, adjustments, counts, lots, holds | M1–M2 | — |
| 07 | [[modules/07-outbound]] | orders, allocation, waves, pick, pack, load, dispatch | M3 | — |
| 08 | [[modules/08-rfid]] | readers, gateway, tag binding, RFID use cases (optional) | M4 | — |
| 09 | [[modules/09-integrations-labels]] | CSV, REST API, webhooks, labels, documents | M1/M5 | — |
| 10 | [[modules/10-reporting-audit]] | audit log, dashboards, reports | M0/M5 | — |

Delivery order: [[roadmap]]. Quality targets for all modules: [[non-functional]].
Add the spec link to the table when a spec is written in `wms-docs/specs/`.

## Roles (draft — finalise the permission matrix before the first spec)

| Role | Scope | Typical actions |
|---|---|---|
| `admin` | the whole tenant | users and roles, warehouses, master data, tenant settings (e.g. RFID on/off) |
| `manager` | assigned warehouses | plan inbound/outbound, approve adjustments, view reports |
| `operator` | assigned warehouse, on a handheld | scan, receive, putaway, pick, pack, load, count |

Full capability matrix: [[roles-permissions]].

Open question: is there a platform-level super-admin (our team) above tenant
admins? → track in [[STATE]] under Open decisions.

## Out of scope (until decided otherwise)

Billing, accounting, transport management (route planning), and labour management.
