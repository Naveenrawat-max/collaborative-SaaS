# SKILL.md — capabilities and procedures for the WMS project

> Companion to `AGENTS.md`. AGENTS.md says **what** the rules are; this file says
> **how** to carry them out. Works with any agent — every step is a plain shell
> command or file edit, with no vendor-specific features.

Contents:
- **A.** Capability check — run at the start of every task
- **B.** Skill registry — which skill to use for which kind of work
- **C.** Procedures: start session · handoff · write ADR · write spec · open PR

---

## A. Capability check (start of every task, and again on every role change)

**1. Inventory** what you already have:
```bash
# agent skill dirs (whichever exist for your harness)
ls -1 .claude/skills ~/.claude/skills ~/.codex/skills ~/.gemini/extensions .cursor 2>/dev/null
# toolchain for this stack
for t in python python3 uv pip node npm pnpm docker psql git gh; do
  command -v "$t" >/dev/null && printf "%-8s %s\n" "$t" "$(command -v $t)"; done
# project manifests (read, don't install yet)
cat VERSION pyproject.toml requirements*.txt package.json 2>/dev/null
```
Write one line: `INVENTORY: <what's present>`.

**2. Gap analysis.** List what the task needs minus what's present. If nothing is
missing, write `SKILLS: sufficient` and continue.

**3. Fill gaps.** Use section B for skills. For packages, use the project's own
package manager and lockfile only (once it exists). Install only what the gap
needs. If something isn't on the allowlist (below), **stop and ask the human**.

**Allowlist for third-party skills** (humans maintain this list):
```
- obra/superpowers
- DietrichGebert/ponytail
```
Before trusting any new skill, read its SKILL.md and scan it:
`grep -rInE "curl|wget|eval|base64|/dev/tcp|~/.ssh|\.env|token|secret|rm -rf" <dir>`.
If anything looks suspicious, don't run it — report it.

---

## B. Skill registry

| When the task is… | Use | Source |
|---|---|---|
| Planning a feature, writing a spec or plan, TDD, code review, debugging | **superpowers** (brainstorming, writing-plans, test-driven-development, systematic-debugging, requesting-code-review) | `obra/superpowers` |
| Keeping code minimal, avoiding over-engineering | **ponytail** | `DietrichGebert/ponytail` |
| Docs vault notes | Section 8 of `AGENTS.md` + `tools/vaultify.py` | in repo |
| _Django / DRF patterns_ | _<add a vetted skill>_ | _<source>_ |
| _PostgreSQL schema, indexes, row-level security_ | _<add a vetted skill>_ | _<source>_ |
| _Security review_ | _<add a vetted skill>_ | _<source>_ |
| _React UI_ | _<add a vetted skill>_ | _<source>_ |

Italic rows are placeholders, not real skills. Fill them in once the team has
vetted one, and add the source to the allowlist.

If your agent has no skill system, follow the same steps by hand: plan before
coding, write the test first, and find the root cause before fixing a bug.

---

## C. Procedures

### C1. Start a session
```bash
git checkout <your-branch> && git pull
git fetch origin && git rebase origin/main      # stay current with teammates
```
Then read, in order:
1. `wms-docs/STATE.md` — what's in progress, who owns what, blockers
2. the spec for your task in `wms-docs/specs/`
3. the ADRs that spec links to

Then post your classification (AGENTS.md section 4) before writing code.

### C2. Handoff (end of every session, or when the human says "handoff")
This is how context reaches the other two devs. Do all six steps:

1. **Update `wms-docs/STATE.md`**:
   - Move finished items to **Done**, with the PR or commit.
   - Update your line under **In progress**: what's half-done and the exact next step.
   - Add new blockers, known issues, and requests for other module owners.
   - Append one entry to **Log** (newest first):
     `- YYYY-MM-DD · <dev> · <branch> — <what changed, why, what's next>`
2. **Write an ADR** for any decision made this session (C3).
3. **Update the spec** if behavior differs from what it says.
4. **Bump `VERSION`**: patch for fixes and docs, minor for features.
5. **Sync the vault** if code changed: `python tools/vaultify.py sync wms-docs`
6. **Commit and push code and context together:**
   ```bash
   git add -A
   git status                       # check: no .env, no secrets, no stray files
   git commit -m "<type>(<scope>): <summary>"
   git push -u origin HEAD
   ```

Commit types: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`.
Don't add AI attribution trailers.

### C3. Write an ADR (architecture decision record)
Write one when you choose between real alternatives: a library, a data-model
shape, a tenancy approach, or an API convention.
1. Copy `wms-docs/_meta/decisions/000-template.md` to `NNN-short-slug.md`, using the
   next free number.
2. Fill in Context, Options, Decision, and Consequences. Set `status/proposed`.
3. Link it from `wms-docs/00 Index.md` → Decisions, and from the notes it affects.
4. When the team agrees in the PR, change the tag to `status/accepted`. Never
   delete an ADR — supersede it with a new one and link the two.

### C4. Write a spec (before coding a feature)
1. Copy `wms-docs/specs/000-template.md` to `NNN-module-feature.md`.
2. Fill in the goal, roles, flow, data, API contract, acceptance criteria, and the
   RFID flow with its exceptions and QR fallback.
3. Link it from `00 Index.md` → Specs, and from `STATE.md` → In progress.
4. Get a teammate's 👍 on the spec PR, or in the feature PR if it's small.

### C5. Open a PR
```bash
gh pr create --base main --fill      # the template adds the context checklist
```
Every item on the PR checklist must be ticked, or explained if it doesn't apply.
