---
title: "ADR-002 — Multi-tenancy model"
tags:
  - kind/decision
  - area/tenancy
  - status/accepted
---

# ADR-002 — Multi-tenancy model

- **Date:** 2026-10-08
- **Status:** accepted 2026-10-08 (team can still raise objections on PR #1)
- **Deciders:** Naveen, Harshit, Joseph

## Context
Every table depends on this choice, so it must be fixed first ([[STATE]] → Next up,
item 1). Tenant data must never leak (AGENTS.md invariant 1). Stack:
[[_meta/decisions/001-stack-django-react]].

## Options considered
1. **Shared tables + `tenant_id` column** on every tenant-owned model, scoped in
   Django by a tenant-aware model manager/middleware, **plus PostgreSQL row-level
   security as a backstop** (the DB session sets `app.tenant_id`, and policies
   filter on it).
   - Pro: one schema and one migration run; simple cross-tenant ops for us; scales
     to many tenants.
   - Con: every query must be scoped. RLS catches mistakes but adds setup (a
     non-superuser DB role, per-request `SET`).
2. **Schema per tenant** (`django-tenants`).
   - Pro: strong separation; a forgotten filter can't leak data.
   - Con: migrations run N times; harder reporting across tenants; heavier with
     many small tenants; ties us to the library.
3. **Database per tenant.**
   - Pro: maximum isolation.
   - Con: heavy operations. Overkill unless a customer contractually needs it.

## Decision
**Option 1**: a `tenant_id` foreign key on every tenant-owned model, a single
scoped base model/manager, and Postgres RLS as defense in depth. Revisit option 3
only for an enterprise customer who requires a dedicated DB.

## Consequences
- Every tenant-owned model inherits one base class. A raw `Model.objects` without
  scoping fails review.
- Unique constraints include the tenant (e.g. `unique(tenant, sku)`).
- Every endpoint gets a cross-tenant test (AGENTS.md section 7).
- The Django admin must also be tenant-scoped, or restricted to platform staff.
