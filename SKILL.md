# SKILL.md — capabilities and procedures for the WMS project

> Companion to `AGENTS.md`. AGENTS.md says **what** the rules are; this file says
> **how** to carry them out. Works with any agent — every step is a plain shell
> command or file edit, with no vendor-specific features.

Contents:
- **A.** Capability check — run at the start of every task
- **B.** Skill registry — which skill to use for which kind of work
- **C.** Procedures: start session · handoff · write ADR · write spec · open PR · parallel agents · safe publication / workstation profiles

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

**Mandatory for every agent, every task:** **karpathy-guidelines** and **ponytail**.
Load both and apply them actively. If either is missing, install it before doing
anything else:

| Agent | karpathy-guidelines | ponytail |
|---|---|---|
| Claude Code | `/plugin marketplace add forrestchang/andrej-karpathy-skills`, then `/plugin install andrej-karpathy-skills@karpathy-skills` | `/plugin marketplace add DietrichGebert/ponytail`, then `/plugin install ponytail@ponytail` |
| Grok Build | `grok plugin install https://github.com/forrestchang/andrej-karpathy-skills` | `grok plugin install https://github.com/DietrichGebert/ponytail` |
| Any other agent | Read the skill files in `forrestchang/andrej-karpathy-skills` and follow them | Read the skill files in `DietrichGebert/ponytail` and follow them |

Check with `grok inspect` (Grok) or `/plugin` (Claude). Grok also picks up plugins
already installed for Claude; `grok inspect` marks those `[claude]`.

**Allowlist for third-party skills** (humans maintain this list):
```
- obra/superpowers
- DietrichGebert/ponytail
- forrestchang/andrej-karpathy-skills
```
Before trusting any new skill, read its SKILL.md and scan it:
`grep -rInE "curl|wget|eval|base64|/dev/tcp|~/.ssh|\.env|token|secret|rm -rf" <dir>`.
If anything looks suspicious, don't run it — report it.

---

## B. Skill registry

| When the task is… | Use | Source |
|---|---|---|
| Planning a feature, writing a spec or plan, TDD, code review, debugging | **superpowers** (brainstorming, writing-plans, test-driven-development, systematic-debugging, requesting-code-review) | `obra/superpowers` |
| **Every task (mandatory)**: keeping code minimal, avoiding over-engineering | **ponytail** | `DietrichGebert/ponytail` |
| **Every task (mandatory)**: think before coding, simplicity, surgical changes, verifiable goals | **karpathy-guidelines** | `forrestchang/andrej-karpathy-skills` |
| Two agents building in parallel | C6 (Claude/Grok) or C7 + the Codex/Antigravity profile | in repo |
| Codex/Antigravity coordination, recovery and publishing | `.agents/skills/wms-collaboration/SKILL.md` | project-owned; procedures in `wms-docs/collaboration/` |
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
git status --short                         # preserve existing work first
git fetch origin --prune
# Select your existing feature worktree; inspect both diffs using C7 before integration.
```
Then read, in order:
1. `wms-docs/STATE.md` — what's in progress, who owns what, blockers
2. the spec for your task in `wms-docs/specs/`
3. the ADRs that spec links to

Use C7 to inspect divergence and integrate fetched commits. Use `git pull --ff-only`
only after checking the upstream and preserving local changes. Never rebase a
published branch or force-push it.

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
4. **Version the iteration**: serial changes bump `VERSION` (patch for fixes/docs,
   minor for features). Parallel feature branches defer the bump to DevOps at
   merge, per ADR-007; explain that exception in the PR.
5. **Sync the vault** if code changed: `python tools/vaultify.py sync wms-docs`
6. **Commit and push code and context together**, following C7 before the push
   and requiring the other agent's review in paired sessions:
   ```bash
   git add <named-task-paths>          # never stage another person's work
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

### C6. Parallel agents: lead and worker (ADR-007)
Use this when two agents (Claude Code as **lead**, Grok Build as **worker**) build
features of one platform at the same time. The full rules and the open pilot
questions are in `wms-docs/_meta/decisions/007-parallel-agents-claude-grok.md`.

**1. Set up once per machine**
```bash
# mailbox (gitignored) and worktree root, next to the repo
mkdir -p .agents/inbox/claude .agents/inbox/grok .agents/outbox/claude .agents/outbox/grok ../wms-wt
grok inspect            # must list this repo's AGENTS.md; if "Project trusted: no", trust the repo first
```
Start Grok in its own PowerShell tab, from the repo root, and leave it running:
```powershell
grok --sandbox <profile from ADR-007> --rules "You are the WORKER in SKILL.md C6. Read AGENTS.md and SKILL.md C6. After every task, check .agents/inbox/grok/ for the next brief."
```
Both agents run section A first, including the mandatory skills check (A3).

**2. Split the work (lead)**
- Pick features of **one platform** whose file sets don't overlap. If they overlap,
  split by platform instead.
- A feature that needs another feature's unfinished API is **not** parallel. Its
  contract comes first (AGENTS.md §6.4).
- Limit: at most 2 features per agent at a time (ADR-007).
- Create one branch and one worktree per feature:
  `git worktree add ../wms-wt/feat-<module>-<thing> -b feat/<module>-<thing> main`

**3. Write a task brief** to `.agents/inbox/<agent>/NNN-<slug>.md`. `NNN` counts up
per machine.
```markdown
# NNN — <feature>
- Branch / worktree: feat/<module>-<thing> · ../wms-wt/feat-<module>-<thing>
- Spec / plan task: <links, e.g. wms-docs/plans/… Task 12>
- Contract to build against: <api-contract section or schema>
- May change ONLY: <paths>
- Must NOT change: shared files (ADR-007 list) — ask the lead in your report
- Skills: karpathy-guidelines, ponytail (mandatory) + <others, e.g. superpowers:test-driven-development>
- Done when: <tests that must pass, exact commands>
```

**4. Build (each agent, in its own worktree)**
- Follow the plan task with TDD, and commit small (AGENTS.md §6.8).
- Never touch the main checkout or another agent's worktree.

**5. Report** to `.agents/outbox/<agent>/NNN-<slug>.report.md`:
```markdown
# NNN — report
- Branch @ commit: feat/<module>-<thing> @ <sha>
- Tests run + result: <command> → <N passed / failures>
- Skills applied: karpathy-guidelines, ponytail, …
- Shared-file requests for the lead: <none | path + exact change>
- Open risks: <what the reviewer should look at>
```

**6. Cross-review (the other agent)**
- Claude reviews Grok's branches with a review sub-agent; Grok reviews Claude's.
  The lead puts a review brief in the reviewer's inbox.
- The reviewer:
  - reads `git diff main...<branch>`
  - **runs the tests itself** in that worktree
  - checks the spec, the AGENTS.md invariants (tenant isolation, server-side roles, RFID rules, glossary names)
  - checks karpathy-guidelines (simple, surgical, verifiable) and ponytail (nothing that doesn't need to exist)
- The verdict goes to `.agents/outbox/<reviewer>/NNN-<slug>.review.md`:
  `APPROVE`, or `CHANGES` with one line per finding (`path:line — problem — fix`).
- `CHANGES` goes back to the author as `.agents/inbox/<author>/NNN-<slug>.fix.md`.
  After two rounds of fixes, the human decides.

**7. Integrate (lead)**
- Apply any shared-file requests on the feature branch.
- Update `wms-docs/STATE.md`.
- Run the full suite.
- Push, then open the PR (C5). DevOps merges it.
- In a parallel run, feature PRs don't bump `VERSION`; DevOps does it at merge time (ADR-007).
- Remove the worktree after the merge: `git worktree remove ../wms-wt/feat-<module>-<thing>`.


### C7. Safe publication and Codex/Antigravity profile

The shared publishing procedure is `wms-docs/collaboration/safe-publishing.md`.
Read it before every push: fetch and compare both diffs, integrate concurrent
work without dropping either feature, record conflict decisions, validate,
cross-review the final candidate, fetch again, and push without rewriting history.
A blocked review/integration means checkpoint locally and record the blocker.
Complete each reviewed iteration with its context and a branch push/PR.

On Harshit's workstation, use `wms-docs/collaboration/codex-antigravity.md` instead
of C6's Claude/Grok-specific commands. Codex is lead, Antigravity is worker and
reviewer. Keep C6's briefs, path ownership, isolated worktrees, cross-review and
two-round escalation. Skills/install provenance are in
`wms-docs/collaboration/skills.md`; the discoverable compact entrypoint is
`.agents/skills/wms-collaboration/SKILL.md`. Read those files explicitly if a
harness does not discover them. Reuse the saved exact Antigravity conversation,
verify its model with `agy models`, and enforce the Codex 90% / 40-minute reserve.
Runtime sessions and mailboxes are ignored; `.agents/skills/` is tracked.
Record iteration outcomes in `wms-docs/collaboration/iterations/` and link them
from STATE and the vault index. The PR holds final review SHA/verdict and checks.
