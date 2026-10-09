---
title: STATE — live project status
tags:
  - kind/map
  - role/hub
  - status/current
---

# STATE — live project status

**Read this first, every session. Update it at every handoff** (procedure C2 in
`SKILL.md`). Each dev edits only their own lines, and the Log is append-only.

- **Version:** 0.1.8 (see `VERSION`)
- **Phase:** 0 — project setup. No application code yet.
- **Master design:** [[specs/001-rfid-wms-pilot-design]] (approved 2026-10-08). RFID is mandatory, with a QR (EPC+TID) fallback.
- **Stack:** Django + DRF + PostgreSQL · React back office · native Kotlin app on Chainway C72 with trc-rfid.
  Decisions: [[_meta/decisions/001-stack-django-react]], [[_meta/decisions/003-api-drf]], [[_meta/decisions/004-native-operator-app-trc-rfid]]

## Team and module ownership

| Dev | Owns modules | Current focus |
|---|---|---|
| Naveen | _TBD_ | — |
| Harshit | _TBD_ | — |
| Joseph | _TBD_ | — |

Proposed split (agree, then fill in the table above). Details: [[roadmap]].
- **A**: modules 03 vehicles/yard, 04 inbound, 05 putaway
- **B**: modules 02 master data, 06 inventory, 08 RFID
- **C**: modules 01 tenancy/users, 07 outbound, 09 integrations
- Shared: module 10 reporting/audit

## Workstation profiles

- **Harshit:** Codex lead + Antigravity worker; [[collaboration/codex-antigravity]]. Runtime conversation ID is local; committed notes and PRs carry shared context. Other developers retain their chosen tools.

## In progress

_Nothing yet._ Format: `- <dev> · <branch> · <spec link> — status, exact next step`

## Next up (in order)

1. Pilot [[_meta/decisions/007-parallel-agents-claude-grok]]: one small feature per agent, answer its "Verify in the pilot" list, then accept or revise it.
2. Review and execute [[plans/2026-10-08-m0-backend]] on branch `feat/m0-backend` (PR #1 and #2 are merged).
3. Assign module ownership (table above).
4. Write the M0 web plan and the M0 Android plan, against `wms-docs/api-contract.md` (published by the backend plan's Task 15).
5. Pilot prep (non-code): choose the tag supplier (must print the TID in the QR, risk R3), confirm the Chainway SDK licence (R2), verify `readOnce()`/`readMemory()` on a real C72 (R1).

## Open decisions

| Question | Options | Owner | Note |
|---|---|---|---|
| Web tooling | Vite + React / other | frontend | — |
| Background jobs | Celery / django-q2 / Dramatiq | backend | needed for imports, reports |
| Tag supplier | must pre-encode and print QR with EPC + TID | RFID owner | spec risk R3 |
| Dock portal reader model (Phase 2) | LLRP fixed reader brand | RFID owner | [[modules/08-rfid]] |
| Hosting | — | devops | — |
| Code map in vault | `tools/codemap.py` wrapper → `wms-docs/_code/<folder>/` (proposed in the M0 backend plan, Task 11) | docs | see [[architecture]] |

Decided on 2026-10-08: tenancy = shared tables + `tenant_id` + RLS ([[_meta/decisions/002-multi-tenancy]]) · API = DRF ([[_meta/decisions/003-api-drf]]) · handheld = native Kotlin on C72 ([[_meta/decisions/004-native-operator-app-trc-rfid]]) · tag identity = TID + EPC with QR ([[_meta/decisions/005-tag-identity-epc-tid-qr]]) · tenants = own-warehouse first ([[_meta/decisions/006-own-warehouse-tenants-first]]).

## Blockers

_None._

## Known issues / requests to other owners

_None._

## Done

- 2026-10-09 · Harshit — Collaboration rules documented on `docs/codex-antigravity`: [[collaboration/iterations/001-collaboration-bootstrap]]. Shared-rule proposal awaits teammate approval/DevOps merge; final independent review and publication evidence are in that branch's PR.

- 2026-10-09 — Spec-002 approved and applied: modules 04/06/07/08/10, glossary, roadmap; M0 backend plan gained Tasks 10–13 (tag intake, exception cases).
- 2026-10-08 — ADR-002 (tenancy) accepted. M0 backend implementation plan written: [[plans/2026-10-08-m0-backend]].
- 2026-10-08 — Spec-001 approved. Notes aligned (RFID mandatory, QR fallback), ADR-003 to ADR-006 written.
- 2026-10-08 — Spec-001 drafted: RFID-mandatory pilot goal, phased scope, architecture (native C72 app + trc-rfid), tag identity (EPC+TID, QR fallback).
- 2026-10-08 — Draft scope: 10 module notes, roles-permissions matrix, roadmap M0–M5, non-functional requirements.
- 2026-10-08 — Project context scaffold: AGENTS.md, SKILL.md, the `wms-docs` vault, ADR-001, ADR-002 (proposed).

## Log (newest first)

- 2026-10-09 · Harshit · `docs/codex-antigravity` — Added [[_meta/decisions/008-codex-antigravity]], workstation profile, compact collaboration skill, installed mandatory/review skills, and safe publishing with comparison of concurrent changes. VERSION 0.1.8 is the serial docs-bootstrap bump; parallel features retain the DevOps-at-merge exception. Next: teammate approval, then one bounded worker implementation and reciprocal review. Existing team/module entries preserved.

- 2026-10-09 · setup · `docs/parallel-agents` — Wrote ADR-007 (proposed): Claude Code as lead, Grok Build as worker, one feature per branch and worktree, `.agents/` mailbox, cross-review before push, DevOps merges and bumps VERSION in parallel runs. Added SKILL.md C6 and made karpathy-guidelines + ponytail mandatory for every agent (AGENTS.md §3, §6.12, §7). Next: pilot one feature per agent.
- 2026-10-09 · setup · `chore/project-context` — Spec-002 approved. Notes updated per its §13. M0 backend plan now 15 tasks: new Tasks 10–13 add `TagBatch` + tag verification/last-seen fields, the `exceptions` app (`open_case`/`close_cases`, inbox API), supplier CSV import, bench checks with quarantine, and verification on first close-read bind. Next: team reviews the plan, then executes it on `feat/m0-backend`.
- 2026-10-09 · setup · `chore/project-context` — Brainstormed an external feature review (Grok + `assets/wms-feature-architecture.svg`). Wrote [[specs/002-rfid-checks-and-exceptions]] (draft): sampled tag intake per roll, last-seen on every confirm, wrong-location and hold-escape cases, stuck pallets, retag, pack confirm, exception inbox. Returnable pallets, forklift readers, carton tags stay out. Next: team reviews spec-002.
- 2026-10-08 · setup · `chore/project-context` — Accepted ADR-002. Wrote [[plans/2026-10-08-m0-backend]]: 11 TDD tasks for Django/DRF with forced Postgres RLS, users and roles, master data, tag registry (TID/EPC/QR), C72 device PIN login, power profiles, audit, CI. M0 is split into three plans: backend first, then web and Android against its published API contract. Next: team reviews the plan, then executes it on `feat/m0-backend`.
- 2026-10-08 · setup · `chore/project-context` — Spec-001 approved. Applied its section 10: AGENTS.md invariant 3 is now "RFID mandatory, QR only for exceptions", with a new `android` role. Rewrote product, architecture, roadmap (RFID from M1) and modules 04–08. Updated roles, non-functional, glossary, the spec template and the PR template. Added ADR-003 to ADR-006. Next: accept ADR-002, assign owners, write the M0 implementation plan.
- 2026-10-08 · setup · `chore/project-context` — Brainstormed with web research: RFID is now **mandatory**, with QR (EPC+TID) fallback; Chainway C72 + trc-rfid; native Kotlin operator app; own-warehouse tenants first. Wrote [[specs/001-rfid-wms-pilot-design]]. Older notes still say "RFID optional" until the spec is approved and section 10 is applied.
- 2026-10-08 · setup · `chore/project-context` — Added draft scope for every module (`modules/01–10`), [[roles-permissions]], [[roadmap]], and [[non-functional]]. Each module lists its open questions. Next: team reviews the scope and ADR-002 on PR #1.
- 2026-10-08 · setup · `chore/project-context` — Set up the shared-context system: rules for all agents (AGENTS.md), procedures (SKILL.md), this STATE file, product/architecture/glossary notes, ADR-001 (Django + React + Postgres), and ADR-002 tenancy (proposed). Next: agree on ADR-002 and module owners.
