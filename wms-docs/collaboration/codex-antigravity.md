---
title: "Codex and Antigravity — Harshit's workstation"
tags:
  - kind/doc
  - area/process
  - status/current
---

# Codex and Antigravity — Harshit's workstation

Human-authorized on 2026-10-09. This workstation uses **Codex as lead** and
**Antigravity as worker**. Other developers choose their own agents; all follow
`AGENTS.md`, `SKILL.md`, the product invariants, and the same review gates.
This profile extends [[_meta/decisions/007-parallel-agents-claude-grok]] without
replacing the Claude/Grok profile. Decision: [[_meta/decisions/008-codex-antigravity]].

## Start and recover context

1. Read `AGENTS.md`, `SKILL.md`, [[STATE]], this note, and the current task's spec.
2. Read [[collaboration/skills]] and load the mandatory skills. Read only the
   task-relevant module, ADRs and changed contracts after this initial context.
3. Inspect Git status, branches and worktrees. Fetch remote changes and follow
   [[collaboration/safe-publishing]] before integrating them. Never overwrite
   unrelated local work or start a second worker on an already active task.
4. Read the latest committed iteration under `wms-docs/collaboration/iterations/`
   and the task's PR. Restore the worker conversation from the local session
   file; its ID is a convenience, never the source of project knowledge.
5. Check usage, announce classification, and assign one bounded task at a time.

## Ownership and review

- Codex writes briefs, owns shared files, integrates work, resolves conflicts,
  records durable context, pushes reviewed feature branches and opens PRs.
- Antigravity implements its assigned paths and reviews Codex's work. Codex
  reviews Antigravity's work. Neither approves its own change.
- Use one branch and worktree per feature under `../wms-wt/`. A reviewer uses
  its own detached review worktree at the candidate commit. The main checkout
  is an anchor for runtime mailboxes, not a place to edit feature files.
- Shared files remain lead-owned as listed in AGENTS.md §6.12. The worker asks
  for shared changes in its report; it does not edit them implicitly.
- Each brief names branch, worktree, spec, contract, allowed paths, forbidden
  paths, acceptance checks and expected report path. Start with one active
  worker task; use ADR-007's larger concurrency only after its pilot succeeds.
- A review names base and candidate commit IDs, checks the full diff and connected
  contracts, independently runs relevant checks, and returns `APPROVE` or
  `CHANGES` with concrete findings. Docs changes use link, whitespace and skill
  validation; application tests are required when application behavior changes.
- A change, conflict resolution or merge after review invalidates approval for
  the changed candidate. Review that final candidate before pushing. After two
  unsuccessful fix/review rounds, involve the human as SKILL.md C6 requires.
- An unavailable reviewer means work can be prepared and locally checkpointed,
  but cannot be pushed. Do not replace cross-review with self-approval.
- Teammate approval and DevOps merge into `main` remain separate requirements.

## Communicate with Antigravity

Verified on this PC with `agy --help` and `agy models` on 2026-10-09:
`--conversation`, `--print`, `--output-format json`, `--model`, `--sandbox`,
`--add-dir`, and `--mode plan` are available. Recheck help after CLI upgrades.

PowerShell examples (run from the main checkout):
```powershell
Set-Location 'D:\New Project\Chats\Collaborative SaaS'
agy
# Resume the exact saved conversation; do not use --continue when other chats exist.
agy --conversation '<saved-conversation-id>'
# Send a bounded read-only review prompt and capture its result.
$brief = Get-Content -LiteralPath '.agents/inbox/antigravity/NNN-review.md' -Raw
agy --conversation '<saved-conversation-id>' --model gemini-3.8-flash-high --sandbox --mode plan --add-dir '<review-worktree>' --output-format json --print $brief
```

For the first noninteractive turn omit `--conversation`; save the ID returned
by the CLI in `.agents/session-codex-antigravity.json`, together with project
root, worker model, active task/branch/worktree, and last report path. Do not
invent an ID or assume the CLI's JSON field names; inspect the actual response.
Never store credentials or full transcripts in this file or in committed notes.
If resuming fails, record the reason, start one replacement conversation and
bootstrap from the committed notes, then update the local ID.

Mailbox paths: `.agents/inbox/codex/`, `.agents/inbox/antigravity/`,
`.agents/outbox/codex/`, `.agents/outbox/antigravity/`. Runtime files are ignored;
`.agents/skills/` is tracked. An inbox file does not wake the worker: Codex must
explicitly invoke `agy` with the brief, then read its report. Never launch duplicate
turns on the same conversation. For implementation use the verified CLI edit mode
and the assigned worktree only; retain sandbox and permissions. No permission-
bypass flags or speculative bridge daemon. Native skill discovery is optional:
explicit reads of the installed skill files satisfy the other-agent procedure.

## Worker model

Use **Gemini 3.8 Flash (High)**, exact verified ID `gemini-3.8-flash-high`.
At session start inspect `agy models`. The user authorizes a newer available
Gemini Flash **High** version when it supersedes this one. Compare numeric
versions and verify the exact ID; do not infer a model from its name alone,
choose Pro/Claude, change reasoning tier, or select an unavailable model.
Record any upgrade and its evidence in the next committed iteration. If the
requested family is unavailable, record the blocker rather than silently substitute.

## Usage and token budget

Codex's five-hour usage is shared across the account, not just this chat.
Use the desktop usage tool when available; otherwise read the actual usage UI.
Check at session start, before dispatch/review/publication, and at task boundaries;
do not poll continuously. Compute remaining reset time from its Unix timestamp
in UTC; show user-facing times in Asia/Calcutta. Missing telemetry is unknown,
not zero. If reserve eligibility cannot be established, checkpoint and obtain
actual telemetry before starting more Codex work.

| Five-hour usage | Time until reset | Action |
|---|---|---|
| Below 90% used | any | Work within the remaining allowance. |
| At least 90% used | more than 40 minutes | Stop Codex feature work and reviews; preserve the remaining allowance for other users. |
| At least 90% used | 40 minutes or less | May use remaining allowance for bounded work; do not assume a reset happened. |
| Exhausted or otherwise rate-limited | any | Save available state and wait, or let the other available agent prepare isolated work. |

At the reserve boundary save a brief local checkpoint and status message, then
stop; do not spend the reserve on a long review or handoff. Prepare durable
handoffs before reaching the boundary. Schedule a wake-up only when the human
requests it; do not keep an idle tool loop running. Antigravity has no 90% reserve:
when its allowance is exhausted, Codex may do authorized work if eligible, or
wait. Agent availability never waives independent review before publication.
Do not consume reset credits, buy credits or change account settings implicitly.

Use compact briefs and reports with paths and changed-contract summaries. Reuse
the worker conversation, batch independent reads, and load relevant skill detail
only when needed. Do not reread whole transcripts or rerun a passing unchanged
suite. Token savings must not remove tests, isolation checks, security gates,
conflict inspection, review, or any requirement the human requested.

## Finish every iteration

Follow [[collaboration/safe-publishing]] and SKILL.md C2. Commit code and context
together on the feature branch after every completed iteration; push only when
review and checks pass. A blocked iteration is checkpointed locally and named
as blocked, never described as published. Update only Harshit's STATE entries.
Store the goal, contract, files, checks, decisions, next step, blockers and review
reference in a short committed iteration note. PR descriptions hold approval
verdicts and exact reviewed commit IDs; STATE links the branch/PR. Every durable
note is reachable from [[00 Index]]. Chat messages may repeat this information
but never replace it. Current setup: [[collaboration/iterations/001-collaboration-bootstrap]].
