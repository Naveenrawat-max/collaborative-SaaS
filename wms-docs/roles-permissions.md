---
title: "Roles & permissions matrix"
tags:
  - kind/doc
  - area/tenancy
  - status/current
---

# Roles & permissions matrix

Aligned with [[specs/001-rfid-wms-pilot-design]]. Confirm it with the team before the
first feature spec ([[STATE]]). Enforced on the
server (AGENTS.md invariant 2). Implemented in [[modules/01-tenancy-users]].

`✅` allowed · `👁` view only · `⚠` needs manager approval above a threshold · `—` not allowed.
Managers and operators are limited to the warehouses they are assigned to.

| Capability | admin | manager | operator |
|---|---|---|---|
| Manage users, roles, warehouse access | ✅ | — | — |
| Tenant settings (timezone, units) | ✅ | — | — |
| Master data: warehouses, zones, locations, docks | ✅ | 👁 | — |
| Bind location tags (warehouse setup) | ✅ | ✅ | — |
| Master data: items, partners | ✅ | ✅ | 👁 |
| Register C72 devices to a warehouse | ✅ | 👁 | — |
| Power profiles (dBm per task) | ✅ | ✅ | — |
| Import supplier tag lists (EPC/TID CSV) | ✅ | ✅ | — |
| Bind tags to pallets (receiving, packing) | ✅ | ✅ | ✅ |
| Resolve tag conflicts (duplicate EPC), retire tags | ✅ | ✅ | — |
| Use the QR fallback (with a reason) | ✅ | ✅ | ✅ |
| Find-a-tag | ✅ | ✅ | ✅ |
| Dock appointments | ✅ | ✅ | 👁 |
| Gate-in / gate-out | ✅ | ✅ | ✅ |
| Create or import ASNs | ✅ | ✅ | — |
| Receive goods | ✅ | ✅ | ✅ |
| Approve receiving discrepancies | ✅ | ✅ | — |
| Putaway / internal moves | ✅ | ✅ | ✅ |
| Stock adjustments | ✅ | ✅ | ⚠ (request only) |
| Create cycle counts / approve variances | ✅ | ✅ | — |
| Perform counts | ✅ | ✅ | ✅ |
| Holds (block/unblock stock) | ✅ | ✅ | — |
| Create or import orders | ✅ | ✅ | — |
| Pick, pack, load | ✅ | ✅ | ✅ |
| Dispatch shipment | ✅ | ✅ | — |
| Reports and dashboards | ✅ | ✅ (own warehouses) | — |
| Audit log | ✅ | — | — |
| API keys and webhooks | ✅ | — | — |

## Platform staff (us)
Not a tenant role. Creates tenants and supports customers. Proposed: Django admin
with `is_staff`, every access audited. Open question tracked in
[[modules/01-tenancy-users]].
