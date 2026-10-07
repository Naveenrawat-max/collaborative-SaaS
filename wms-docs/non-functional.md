---
title: "Non-functional requirements"
tags:
  - kind/doc
  - area/architecture
  - status/draft
---

# Non-functional requirements

Qualities every module must meet, from M0 ([[roadmap]]). Numbers marked
_proposed_ are starting targets, not commitments — confirm them in [[STATE]] →
Open decisions. Architecture: [[architecture]].

## Security & isolation
- Tenant isolation per [[_meta/decisions/002-multi-tenancy]], with a cross-tenant
  test for every endpoint.
- Server-side permission checks per [[roles-permissions]].
- OWASP Top 10 basics: CSRF, input validation, no raw SQL from user input, rate
  limiting on login and the API.
- Secrets only in environment variables. No secrets in the repo, logs, or docs.
- Passwords use Django's default hasher. API keys are hashed at rest.

## Data integrity & audit
- Stock is changed only through the movement service: atomic, never negative,
  append-only `Movement` record ([[modules/06-inventory]]).
- An audit log for business records and security events ([[modules/10-reporting-audit]]).
- Soft-delete (or deactivate) master data that history refers to. Never hard-delete it.

## Performance (proposed)
- Handheld scan → response: **< 500 ms p95**. Operators scan all day, so slow scans cost money.
- List and report pages: **< 2 s p95** for one warehouse's data.
- RFID gateway: de-duplicate reads before calling the API, so the API sees events, not raw reads.

## Handheld UX
- Works in the browser on Android scanners (keyboard-wedge barcode input).
- Large touch targets, a minimal number of screens per task, clear error sound and colour.
- Open question: does the operator need **offline** use (poor Wi-Fi in racks)?
  That would be a big design change, so decide before M1.

## Time, units, language
- Store timestamps in UTC; display them in the warehouse's timezone.
- Units per item with conversions ([[modules/02-master-data]]).
- English UI first. Prepare strings for translation (Django i18n plus a frontend i18n
  library) — confirm which languages are needed.

## Operations (proposed)
- Daily database backups, with a restore test each milestone.
- Health check endpoint and error tracking from M0.
- Environments: local (docker-compose), staging, production.
