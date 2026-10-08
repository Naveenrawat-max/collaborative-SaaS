---
title: "Non-functional requirements"
tags:
  - kind/doc
  - area/architecture
  - status/current
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
- Raw reads never reach the server. The C72 app (and the Phase 2 gateway)
  de-duplicate them and send business transactions only.
- RFID cycle count of one zone (`sweep` profile): result on screen **< 2 s** after
  the operator stops scanning.

## RFID quality targets
- **QR fallback < 2%** of transactions. The rate is reported per site and per
  device ([[modules/10-reporting-audit]]).
- Every QR use and every exception is logged with a reason. Nothing is dropped silently.
- Power profiles per task, tuned per site before go-live ([[modules/08-rfid]]).

## Handheld UX
- Native Kotlin app on the Chainway C72
  ([[_meta/decisions/004-native-operator-app-trc-rfid]]). The hardware trigger
  starts and stops scanning.
- Live ✅ / ⚠ / ❌ list while scanning, with a clear error sound, vibration and colour.
- Large touch targets and as few screens per task as possible.
- **Network drops:** transactions queue on the device and retry with the same
  `txn_id`, and a "pending sync" banner shows. Full offline work (with conflict
  resolution) is out of scope for the pilot.

## Time, units, language
- Store timestamps in UTC; display them in the warehouse's timezone.
- Units per item with conversions ([[modules/02-master-data]]).
- English UI first. Prepare strings for translation (Django i18n plus a frontend i18n
  library) — confirm which languages are needed.

## Operations (proposed)
- Daily database backups, with a restore test each milestone.
- Health check endpoint and error tracking from M0.
- Environments: local (docker-compose), staging, production.
