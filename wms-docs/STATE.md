---
title: "STATE — live project status"
tags:
  - kind/map
  - role/hub
  - status/current
---

# STATE — live project status

**Read this first, every session. Update it at every handoff** (procedure C2 in
`SKILL.md`). Each dev edits only their own lines, and the Log is append-only.

- **Version:** 0.1.0 (see `VERSION`)
- **Phase:** 0 — project setup. No application code yet.
- **Stack:** Django + React + PostgreSQL — [[_meta/decisions/001-stack-django-react]]

## Team and module ownership

| Dev | Owns modules | Current focus |
|---|---|---|
| Naveen | _TBD_ | — |
| Harshit | _TBD_ | — |
| Joseph | _TBD_ | — |

Proposed split (agree, then fill in the table above). Module names come from
[[product]]:
- **A**: inbound — vehicles, gate, dock, receiving, putaway
- **B**: inventory — locations, stock, moves, counts, RFID
- **C**: outbound — orders, picking, packing, loading — plus tenancy and auth

## In progress

_Nothing yet._ Format: `- <dev> · <branch> · <spec link> — status, exact next step`

## Next up (in order)

1. **Agree on ADR-002 multi-tenancy** → [[_meta/decisions/002-multi-tenancy]]. This blocks all models.
2. Assign module ownership (table above).
3. Define the role-permission matrix for admin, manager, and operator → in [[product]].
4. Confirm the API style (Django REST Framework?) and frontend tooling (Vite?) → write ADR-003.
5. Scaffold the Django project, React app, Postgres in docker-compose, and CI.
6. First spec: tenancy + users + roles.

## Open decisions

| Question | Options | Owner | Note |
|---|---|---|---|
| Tenancy model | shared tables + `tenant_id` + RLS / schema-per-tenant | all | [[_meta/decisions/002-multi-tenancy]] (proposed) |
| API layer | Django REST Framework / Django Ninja | backend | — |
| Frontend tooling | Vite + React / other | frontend | — |
| Background jobs | Celery / django-q2 / Dramatiq | backend | needed for imports, reports |
| RFID hardware and protocol | which readers; LLRP / vendor SDK / HTTP push | inventory owner | collect from first customer |
| Handheld devices | browser PWA on Android scanners / native | frontend | — |
| Hosting | — | devops | — |
| Code map in vault | `vaultify sync` layout once Django code exists | docs | see [[architecture]] |

## Blockers

_None._

## Known issues / requests to other owners

_None._

## Done

- 2026-10-08 — Project context scaffold: AGENTS.md, SKILL.md, the `wms-docs` vault, ADR-001, ADR-002 (proposed).

## Log (newest first)

- 2026-10-08 · setup · `chore/project-context` — Set up the shared-context system: rules for all agents (AGENTS.md), procedures (SKILL.md), this STATE file, product/architecture/glossary notes, ADR-001 (Django + React + Postgres), and ADR-002 tenancy (proposed). Next: agree on ADR-002 and module owners.
