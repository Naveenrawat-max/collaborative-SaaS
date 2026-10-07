---
title: "Roles & permissions matrix"
tags:
  - kind/doc
  - area/tenancy
  - status/draft
---

# Roles & permissions matrix

Draft. **Agree on it before the first spec** ([[STATE]] → Next up). Enforced on the
server (AGENTS.md invariant 2). Implemented in [[modules/01-tenancy-users]].

`✅` allowed · `👁` view only · `⚠` needs manager approval above a threshold · `—` not allowed.
Managers and operators are limited to the warehouses they are assigned to.

| Capability | admin | manager | operator |
|---|---|---|---|
| Manage users, roles, warehouse access | ✅ | — | — |
| Tenant settings (RFID on/off, timezone, units) | ✅ | — | — |
| Master data: warehouses, zones, locations, docks | ✅ | 👁 | — |
| Master data: items, partners | ✅ | ✅ | 👁 |
| RFID hardware registry | ✅ | 👁 | — |
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
| Create or import orders, release waves | ✅ | ✅ | — |
| Pick, pack, load | ✅ | ✅ | ✅ |
| Dispatch shipment | ✅ | ✅ | — |
| Reports and dashboards | ✅ | ✅ (own warehouses) | — |
| Audit log | ✅ | — | — |
| API keys and webhooks | ✅ | — | — |

## Platform staff (us)
Not a tenant role. Creates tenants and supports customers. Proposed: Django admin
with `is_staff`, every access audited. Open question tracked in
[[modules/01-tenancy-users]].
