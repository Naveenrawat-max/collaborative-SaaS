# AGENTS.md — WMS project rules for every AI agent

> **Binding for every agent and harness**: Claude Code, Codex, Cursor, Copilot,
> Gemini, Antigravity, Grok, or anything else. Read this file fully before acting.
> Only a direct instruction from a human in chat overrides it.
>
> `CLAUDE.md` and `GEMINI.md` only import this file. **Never put rules there** —
> put them here so every agent sees the same thing.

## 1. What we are building

**wms** — a multi-tenant SaaS **Warehouse Management System**, built by three
developers (Naveen, Harshit, Joseph), each working with their own AI agent.

- **Multi-tenant**: many customer companies on one deployment, fully isolated.
- **User roles**: `admin`, `manager`, `operator`.
- **Vehicle inbound and outbound**: trucks arriving and leaving the warehouse.
- **Standard WMS flows**: receiving, putaway, inventory, picking, packing, shipping.
- **RFID is mandatory**: every pallet and location is tagged, and operators use
  Chainway C72 handhelds. A QR code (EPC + TID) is the fallback for exceptions only.

Details live in the docs vault: `wms-docs/product.md`.

**Stack:**
- Backend: Django + DRF + PostgreSQL
- Back office (admin, manager): React web app
- Operators: native Kotlin app on Chainway C72, using
  [trc-rfid](https://github.com/Naveenrawat-max/trc-rfid)

See ADR-001, ADR-003 and ADR-004 in `wms-docs/_meta/decisions/`. Master design:
`wms-docs/specs/001-rfid-wms-pilot-design.md`.

## 2. Where context lives (the core rule)

**If something is not committed to this repo, your teammates and their agents
cannot see it.** Chat history, agent memory, and private config files stay on one
machine. So:

- Every decision, spec, and status change goes into `wms-docs/` and is
  **committed together with the code it describes**.
- Never rely on "I told the agent last session". Write it down in the vault.

| File | Purpose | Who updates it |
|---|---|---|
| `AGENTS.md` (this file) | Rules: what agents must and must not do | Changed by team agreement only, through a PR |
| `SKILL.md` | Capabilities and step-by-step procedures (start, handoff, ADR, spec) | When a procedure changes |
| `wms-docs/STATE.md` | **Live status**: done, in progress, next, blockers | Every session, through a handoff |
| `wms-docs/product.md` | What the product does: modules, roles, scope | When scope changes |
| `wms-docs/modules/` | Scope of each module: in/out of scope, entities, flows, open questions | When a module's scope changes |
| `wms-docs/roadmap.md` | Milestones M0–M5, delivery order | When the plan changes |
| `wms-docs/roles-permissions.md` | admin / manager / operator capability matrix | When permissions change |
| `wms-docs/non-functional.md` | Security, integrity, performance, UX targets | When targets change |
| `wms-docs/architecture.md` | How the system is built | When the structure changes |
| `wms-docs/glossary.md` | WMS terms — use these names in code | When a new term appears |
| `wms-docs/_meta/decisions/` | ADRs: why we chose X over Y | Whenever a decision is made |
| `wms-docs/specs/` | One spec per feature, written **before** coding | Before and during a feature |

## 3. Session protocol (every agent, every time)

**Start of a session**, before writing any code:
1. `git pull` on your branch, and rebase on `main` if it moved.
2. Read `wms-docs/STATE.md`, the spec for your task, and any ADRs it links to.
3. Run the capability check in `SKILL.md`.
4. State your classification (see section 4).

**End of a session** (or when the human says "handoff"): run the **Handoff
procedure** in `SKILL.md`. It updates `STATE.md`, then commits and pushes code and
context together. **A session that changed code but not `STATE.md` is not finished.**

## 4. Classify, then work one role at a time

Before coding, write one line, e.g.
`CLASSIFICATION: full-stack (touches → database, backend, frontend, testing)`

| Domain | Owns | Never touches |
|---|---|---|
| `database` | models, migrations, indexes, constraints, tenant scoping | UI, HTTP views |
| `backend` | API endpoints, business logic, permissions, background jobs | UI; does not redesign the schema |
| `frontend` | React back office UI, client state | server logic, DB, secrets |
| `android` | Kotlin operator app, trc-rfid usage, scan sessions | server logic, DB, secrets |
| `testing` | unit, integration, and e2e tests | production code |
| `security` | authn/authz, tenant isolation, input validation, secrets — **a gate** | building features |
| `performance` | profiling, N+1 queries, caching | new features |
| `devops` | CI, Docker, environment config, deploy | business logic |
| `docs` | `wms-docs/` notes, ADRs, specs, STATE | code behavior |

**Multi-domain tasks** run in this order, one role per pass. Announce each pass:
`>>> ENTER backend ROLE` … `>>> EXIT backend ROLE`
```
database → backend → frontend / android → testing [GATE] → security [GATE] → performance → docs
```
Each role ends with a HANDOFF block, and the next role builds against its
**Contract** line only:
```
### HANDOFF — <domain>
- Produced:      <files changed>
- Contract:      <schema / API shape / props others depend on>
- Assumptions:   <what the next role must honor>
- Do NOT change: <what downstream treats as fixed>
- Open risks:    <what testing/security must check>
```

## 5. Product invariants (never break these)

1. **Tenant isolation.** No tenant can ever read or write another tenant's data.
   Every tenant-owned row is scoped to a tenant. The mechanism is defined in
   ADR-002 (`wms-docs/_meta/decisions/002-multi-tenancy.md`). Every new endpoint
   needs a test proving cross-tenant access fails.
2. **Roles are enforced on the server.** Hiding a button in the UI is not
   authorization.
3. **RFID is mandatory; QR only for exceptions.**
   - Every flow (receive, putaway, move, pick, count, load) identifies pallets
     and locations by RFID.
   - The QR label (`E=<epc>;T=<tid>`) is used only when a tag fails, and every
     QR use is logged with a reason.
   - Raw tag reads never reach the server. The app sends one business
     transaction with a `txn_id`.
   - A tag's identity is its TID (ADR-005).
4. **Stock changes are atomic and audited.** Every inventory change is one
   database transaction plus an append-only movement record (who, what, when,
   from, to, qty). Stock is never edited in place without a movement record.
5. **Use glossary names.** Name models and fields with the terms in
   `wms-docs/glossary.md` (e.g. `ASN`, `putaway`, `location`), not synonyms.

## 6. Collaboration rules (three devs, many agents)

1. **Never push directly to `main`.** Branch → PR → at least one teammate approves
   → merge. Branch names: `feat/<module>-<thing>`, `fix/...`, `chore/...`, `docs/...`.
2. **Code and context ship in the same PR.** A PR that changes behavior without
   updating its spec, ADR, or `STATE.md` is incomplete (see the PR template).
3. **Stay in your module.** Module ownership is listed in `STATE.md`. To change
   another dev's module, file it in `STATE.md` → *Requests* or open a GitHub issue.
4. **Contract-first.** Never build a consumer (UI) before the provider (API, schema)
   has published its contract.
5. **No scope creep.** Do only the task at hand. Log unrelated findings in
   `STATE.md` → *Known issues*; don't fix them in the same pass.
6. **Never invent** APIs, columns, settings, or env vars. If it isn't in the repo,
   it doesn't exist yet.
7. **Secrets never** go into code, docs, logs, or commits. Use env vars, and keep
   placeholders in `.env.example`.
8. **Small commits.** Many focused commits, not one giant diff.
9. **Version every change.** Bump the version in `VERSION` (semver) with each
   change — patch for fixes, minor for features. Tag releases `v<version>`. Once
   `pyproject.toml` / `package.json` exist, keep their versions equal to `VERSION`.
10. **No AI attribution.** No `Co-Authored-By: <AI>` trailers and no "Generated
    with …" lines in commits, PRs, or docs. Commits are authored by the developer.
11. **Merge conflicts in `STATE.md`**: keep both sides. Each dev edits only their
    own lines, and log entries are append-only.

## 7. Gates — when a task is done

- [ ] Classification stated; each touched domain handled in its own pass.
- [ ] Tests pass (including the cross-tenant test for new endpoints).
- [ ] Security pass done: no unresolved critical or high findings.
- [ ] Lint and typecheck clean (once tooling exists).
- [ ] Spec, ADR, and `STATE.md` updated in the same branch.
- [ ] `VERSION` bumped.
- [ ] Vault notes follow section 8; `python tools/vaultify.py sync` run if code changed.

## 8. Docs vault rules (`wms-docs/` is an Obsidian vault)

The folder is named `<project>-docs` so several open vaults stay distinguishable.
Opening it in Obsidian is optional — it is plain markdown.

1. **Frontmatter on line 1**, with `title` and `tags`
   (`kind/` doc|map|decision|spec, `area/` module, `status/` draft|current|stale).
2. **No orphans.** Every note links to another note with `[[wikilinks]]` and is
   reachable from `wms-docs/00 Index.md`.
3. **One idea per note.** Split long notes and link the halves.
4. **Be concrete.** Give paths, commands, and real values. Avoid vague prose.
5. **Decisions** go in `wms-docs/_meta/decisions/NNN-slug.md` (template: `000-template.md`).
6. **Never hand-edit** between `vaultify:auto` markers. Sync overwrites them.
7. **Every source file** starts with a docstring or header comment saying what it is for.

## 9. Agent-specific files

| Agent | Reads | Notes |
|---|---|---|
| Codex, Cursor, Copilot, Antigravity, most others | `AGENTS.md` | Native |
| Claude Code | `CLAUDE.md` → imports `@AGENTS.md` | `/handoff` command in `.claude/commands/` |
| Gemini CLI | `GEMINI.md` → imports `@AGENTS.md` | |
| Anything else | Point it at `AGENTS.md` explicitly | |

Personal, uncommitted overrides (`CLAUDE.local.md`, `.claude/settings.local.json`)
are gitignored. Never put project knowledge there.
