---
title: "Spec-000 — template"
tags:
  - kind/spec
  - status/template
---

# Spec-NNN — <module>: <feature>

Copy this file to `NNN-module-feature.md` **before** coding. Process: SKILL.md → C4.
Terms come from [[glossary]]; scope from [[product]].

- **Owner:** <dev>
- **Status:** draft | agreed | building | done
- **Branch / PR:** <link>
- **ADRs:** <links>

## Goal
One or two sentences: who needs what, and why.

## Roles
Which of admin / manager / operator can do what in this feature.

## Flow
Numbered steps as the user experiences them (handheld or web).

## Non-RFID path
How every step works with barcode or manual entry (required — AGENTS.md invariant 3).

## Data
Models and fields added or changed (tenant-scoped). Movement records written.

## API contract
`METHOD /path` → request / response shape, errors, permissions.

## Acceptance criteria
- [ ] Testable statement…
- [ ] Cross-tenant access is rejected.

## Open questions
