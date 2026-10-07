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

## Decisions

- [[_meta/decisions/001-stack-django-react]] — Django + React + PostgreSQL (accepted)
- [[_meta/decisions/002-multi-tenancy]] — shared tables + `tenant_id` + RLS (**proposed**)
- [[_meta/decisions/000-template]] — copy this for new ADRs

## Specs

- [[specs/000-template]] — copy this before building a feature

## Meta

- [[_meta/Conventions]] — how notes in this vault are written
