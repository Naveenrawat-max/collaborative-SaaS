---
title: "Architecture"
tags:
  - kind/doc
  - area/architecture
  - status/draft
---

# Architecture

The stack is fixed by [[_meta/decisions/001-stack-django-react]]. Tenant isolation
follows [[_meta/decisions/002-multi-tenancy]]. Anything marked _TBD_ is listed in
[[STATE]] → Open decisions.

## Components

```
 Handheld (operator)      Web (admin / manager)
        \                      /
         React app (TBD tooling)
                  |
           HTTPS JSON API
                  |
        Django backend ── background worker (TBD)
                  |
             PostgreSQL
                  ^
     RFID gateway (optional, separate process)
     reader → gateway → API (as scan events)
```

- **Django backend** — all business logic, permissions, and tenant scoping. It is
  the single source of truth.
- **React app** — one app with role-based screens. Operator screens must work on
  handheld scanners (large touch targets, keyboard-wedge barcode input).
- **PostgreSQL** — one database. Stock changes are transactional and append a
  movement record (AGENTS.md invariant 4).
- **RFID gateway** — optional, because readers need an always-on listener. It turns
  tag reads into the **same scan events** a barcode scan produces, so business logic
  never knows whether a scan came from RFID, a barcode, or manual entry.

## Scan-source abstraction (why RFID stays optional)

Every operator flow consumes a generic *scan* (`identifier`, `source` =
`barcode|rfid|manual`, `device`, `timestamp`). RFID adds bulk reads and automation
on top. A tenant with RFID turned off loses no functionality.

## Repository layout (target — create as needed, not up front)

```
AGENTS.md  SKILL.md  VERSION       rules, procedures, version
backend/                           Django project
frontend/                          React app
tools/vaultify.py                  docs vault tooling
wms-docs/                          this vault
```

## Code map

Once code exists, decide how `tools/vaultify.py sync` generates code notes into
this vault (open item in [[STATE]]).
