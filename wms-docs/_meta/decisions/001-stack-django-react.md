---
title: "ADR-001 — Stack: Django + React + PostgreSQL"
tags:
  - kind/decision
  - area/architecture
  - status/accepted
---

# ADR-001 — Stack: Django + React + PostgreSQL

- **Date:** 2026-10-08
- **Status:** accepted
- **Deciders:** team

## Context
Three developers are building a multi-tenant WMS with roles, transactional
inventory, vehicle flows, and RFID (made mandatory by [[specs/001-rfid-wms-pilot-design]]). We need one stack that every dev and
every AI agent can work in. Requirements: [[product]].

## Options considered
1. **Next.js + Supabase** — fastest MVP, tenant isolation via Postgres RLS, built-in
   realtime. Cons: business logic spreads across RLS policies, SQL functions, and
   edge functions; screens for master data must be built by hand.
2. **Django + React + PostgreSQL** — mature ORM and transactions, built-in auth and
   permissions, and a free admin panel for master data. Cons: two languages
   (Python + TypeScript); realtime needs extra setup.
3. **NestJS + React + PostgreSQL** — TypeScript everywhere, full control. Cons: we
   would build auth, roles, and tenancy ourselves — the most boilerplate.

## Decision
**Django backend + React frontend + PostgreSQL**, matching the team's strength in
Python. Django's admin covers master-data screens early. Atomic stock moves fit
`transaction.atomic` + `select_for_update`.

## Consequences
- Tenant isolation must be designed explicitly → [[_meta/decisions/002-multi-tenancy]].
- Still open (see [[STATE]]): API layer (DRF vs Ninja), frontend tooling, job
  queue, and realtime (Django Channels vs polling) for live dock and yard screens.
- The RFID listener is a separate process regardless of stack → [[architecture]].
