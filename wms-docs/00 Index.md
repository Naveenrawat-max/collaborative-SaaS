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
- Modules (draft): [[modules/01-tenancy-users]] · [[modules/02-master-data]] ·
  [[modules/03-vehicles-yard]] · [[modules/04-inbound-receiving]] ·
  [[modules/05-putaway]] · [[modules/06-inventory]] · [[modules/07-outbound]] ·
  [[modules/08-rfid]] · [[modules/09-integrations-labels]] ·
  [[modules/10-reporting-audit]]

## Decisions

- [[_meta/decisions/001-stack-django-react]] — Django + React + PostgreSQL (accepted)
- [[_meta/decisions/002-multi-tenancy]] — shared tables + `tenant_id` + RLS (**proposed**)
- [[_meta/decisions/000-template]] — copy this for new ADRs

## Specs

- [[specs/001-rfid-wms-pilot-design]] — **pilot goal, scope by phase, RFID design** (draft, under review)
- [[specs/000-template]] — copy this before building a feature

## Meta

- [[_meta/Conventions]] — how notes in this vault are written
