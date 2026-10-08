---
title: "ADR-006 — Tenants: own-warehouse businesses first, 3PL-ready data model"
tags:
  - kind/decision
  - area/tenancy
  - status/accepted
---

# ADR-006 — Tenants: own-warehouse businesses first, 3PL-ready data model

- **Date:** 2026-10-08
- **Status:** accepted (approved with [[specs/001-rfid-wms-pilot-design]])
- **Deciders:** team

## Context
There are two kinds of possible tenants:
- **Own-warehouse businesses** (manufacturers, distributors), where all stock
  belongs to the tenant.
- **3PLs**, which store stock owned by many clients. They need stock separated per
  client, activity billing, and a client portal (research in the spec).

Tenant isolation itself is decided in [[_meta/decisions/002-multi-tenancy]].

## Options considered
1. **Own-warehouse only.** Simplest, but 3PL would mean a schema rewrite later.
2. **Full 3PL now.** Billing and the portal would double the scope before the pilot.
3. **Own-warehouse first, with an `owner` on stock from day one.**

## Decision
**Option 3.**
- `Stock`, `Movement`, `ASN` and `Order` carry an `owner` foreign key to `Partner`.
- `owner` defaults to the tenant's own partner record.
- No billing and no client portal until a 3PL customer is signed.

## Consequences
- Queries and reports group by owner from the start, so 3PL needs no migration of history.
- 3PL billing and the client portal stay under *Later* in [[roadmap]].
