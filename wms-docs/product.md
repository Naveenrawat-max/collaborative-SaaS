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

| Module | Covers | Spec |
|---|---|---|
| Tenancy and users | tenants, users, roles, warehouse access | — |
| Master data | warehouses, zones, locations, SKUs/items, units, partners (suppliers, customers, carriers) | — |
| Vehicle inbound | gate-in, yard, dock appointment, unloading, ASN check, receiving | — |
| Putaway | suggested location, confirm move into storage | — |
| Inventory | stock per location/lot, moves, adjustments, cycle counts, movement history | — |
| Outbound | orders, wave/batch, picking, packing, loading, dispatch, gate-out | — |
| RFID (optional) | reader/antenna config, tag ↔ item/pallet binding, read events → transactions | — |
| Reporting | stock levels, throughput, dock utilisation, audit | — |

Add the spec link to the table when a spec is written in `wms-docs/specs/`.

## Roles (draft — finalise the permission matrix before the first spec)

| Role | Scope | Typical actions |
|---|---|---|
| `admin` | the whole tenant | users and roles, warehouses, master data, tenant settings (e.g. RFID on/off) |
| `manager` | assigned warehouses | plan inbound/outbound, approve adjustments, view reports |
| `operator` | assigned warehouse, on a handheld | scan, receive, putaway, pick, pack, load, count |

Open question: is there a platform-level super-admin (our team) above tenant
admins? → track in [[STATE]] under Open decisions.

## Out of scope (until decided otherwise)

Billing, accounting, transport management (route planning), and labour management.
