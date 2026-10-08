---
title: "ADR-003 — API layer: Django REST Framework"
tags:
  - kind/decision
  - area/architecture
  - status/accepted
---

# ADR-003 — API layer: Django REST Framework

- **Date:** 2026-10-08
- **Status:** accepted (approved with [[specs/001-rfid-wms-pilot-design]])
- **Deciders:** team

## Context
Two clients use one JSON API: the native Kotlin operator app and the React back
office ([[architecture]]). The stack is Django ([[_meta/decisions/001-stack-django-react]]).

## Options considered
1. **Django REST Framework (DRF)** — the most widely used option; mature
   permissions, serializers, throttling, and huge agent/LLM familiarity.
   Con: more verbose and slower than newer options.
2. **Django Ninja** — type-hint based, fast, auto OpenAPI. Con: smaller ecosystem,
   and fewer ready-made patterns for per-object permissions.

## Decision
**DRF**, with all endpoints under `/api/v1/`. Its permission classes carry the
tenant and role checks (AGENTS.md invariants 1–2). The OpenAPI schema is generated
with `drf-spectacular`, so the Kotlin and React clients build against a published
contract (AGENTS.md rule 6.4).

## Consequences
- One base viewset scopes every queryset to the request's tenant.
- Business transactions (receipt confirm, pick confirm, load confirm) are explicit
  `POST` actions carrying a `txn_id` for safe retry, not generic CRUD.
