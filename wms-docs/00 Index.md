---
title: "wms-docs"
tags:
  - kind/map
  - role/entrypoint
---

# wms-docs — shared context for the WMS project

Vault root. Everything is reachable from here. Agent rules are in `AGENTS.md`, and
procedures are in `SKILL.md` (both at the repo root).

## Start here

- [[STATE]] — **live status**: who's on what, next steps, open decisions. Read it first.
- [[product]] — what we're building: modules, roles, scope
- [[architecture]] — how it fits together
- [[glossary]] — WMS terms and their code names

## Scope

- [[roadmap]] — milestones M0–M5 and who builds what
- [[roles-permissions]] — admin / manager / operator capability matrix
- [[non-functional]] — security, integrity, performance, handheld UX targets
- Modules: [[modules/01-tenancy-users]] · [[modules/02-master-data]] ·
  [[modules/03-vehicles-yard]] · [[modules/04-inbound-receiving]] ·
  [[modules/05-putaway]] · [[modules/06-inventory]] · [[modules/07-outbound]] ·
  [[modules/08-rfid]] · [[modules/09-integrations-labels]] ·
  [[modules/10-reporting-audit]]

## Decisions

- [[_meta/decisions/001-stack-django-react]] — Django + React + PostgreSQL (accepted)
- [[_meta/decisions/002-multi-tenancy]] — shared tables + `tenant_id` + RLS (accepted)
- [[_meta/decisions/003-api-drf]] — API layer: Django REST Framework (accepted)
- [[_meta/decisions/004-native-operator-app-trc-rfid]] — native Kotlin operator app on Chainway C72 + trc-rfid (accepted)
- [[_meta/decisions/005-tag-identity-epc-tid-qr]] — TID = identity, EPC = label ID, QR carries both (accepted)
- [[_meta/decisions/006-own-warehouse-tenants-first]] — own-warehouse tenants first, `owner` field for 3PL (accepted)
- [[_meta/decisions/000-template]] — copy this for new ADRs

## Specs

- [[specs/001-rfid-wms-pilot-design]] — **pilot goal, scope by phase, RFID design** (approved — the master design)
- [[specs/002-rfid-checks-and-exceptions]] — tag intake check, last-seen, wrong-location, hold escape, pack confirm, exception inbox (draft)
- [[specs/000-template]] — copy this before building a feature

## Plans

- [[plans/2026-10-08-m0-backend]] — M0 backend foundation: tenancy + RLS, master data, tag registry, C72 devices (draft)

## Meta

- [[_meta/Conventions]] — how notes in this vault are written
