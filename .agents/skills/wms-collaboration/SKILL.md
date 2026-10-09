---
name: wms-collaboration
description: Coordinate Codex and Antigravity on Harshit's WMS workstation, recover shared context, enforce cross-review and usage reserves, and publish iterations while preserving concurrent teammate changes.
---

# WMS collaboration

Apply the repository's `AGENTS.md` and root `SKILL.md` first. Resolve paths below
from the repository root of the assigned worktree, not the current shell directory.

- Start/recover/dispatch: read `wms-docs/STATE.md`, then
  `wms-docs/collaboration/codex-antigravity.md` and the current iteration/spec.
- Skills: read `wms-docs/collaboration/skills.md`; load karpathy-guidelines and
  ponytail for every task, plus the review or task skills actually needed.
- Review/publish: read `wms-docs/collaboration/safe-publishing.md`. Integrate
  teammates' work, validate, get the other agent's approval for the final
  candidate, fetch again, and push the feature branch only.

Codex leads; Antigravity works and reviews. Use the saved exact worker conversation
and a verified Gemini Flash High model. Keep one bounded worker task active.
Work in isolated `../wms-wt/` feature/review worktrees; only the lead edits shared
files. Preserve permissions and sandboxing. Save durable decisions, contracts,
checks and next steps in committed notes; runtime IDs/mailboxes stay ignored.

Check Codex usage before dispatch/review/push: >=90% of the five-hour allowance
used with >40 minutes to reset means checkpoint and stop Codex work. At <=40
minutes remaining, bounded use is allowed. Unknown telemetry cannot establish
eligibility. An absent reviewer never authorizes self-approval or an unreviewed push.

Honor the existing serial/parallel VERSION rule and teammate approval before
DevOps merge. Read only the relevant detail; keep briefs and reports compact.
