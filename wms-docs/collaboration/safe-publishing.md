---
title: "Safe publishing — preserve both developers' work"
tags:
  - kind/doc
  - area/process
  - status/current
---

# Safe publishing — preserve both developers' work

Applies to every developer and agent. Profile: [[collaboration/codex-antigravity]].
Rules: `AGENTS.md` §6 and `SKILL.md` C2/C7. Status: [[STATE]].

## Before integrating

Work in the assigned feature worktree. Record the original base and local HEAD.
Inspect `git status --short`, staged and unstaged diffs; never commit another
person's files. Stage named task paths. Checkpoint your own changes before merging.
If unrelated dirty files prevent integration, stop and preserve them; never use
reset --hard, clean, blanket stash, or ours/theirs to make them disappear.

```powershell
git fetch origin --prune
$base = git merge-base HEAD origin/main
git diff --name-status "$base..HEAD"
git diff --name-status "$base..origin/main"
git log --oneline "$base..origin/main"
# If this feature branch already exists remotely, also compare its remote HEAD.
git ls-remote --heads origin '<feature-branch>'
```

Read both actual diffs, especially overlapping paths and changed APIs, migrations,
permissions and dependency files. Nonoverlapping filenames do not prove that
features are compatible. Integrate newer `origin/main` with `git merge origin/main`.
If a teammate also advanced this feature branch, fetch and inspect that branch,
then merge its commits without rewriting published history. Never push to main,
force-push, delete another branch, or merge a PR as part of this procedure.

## Resolve conflicts by intent

Inspect the common base and both versions (`git show :1:path`, `:2:path`, `:3:path`
for an unmerged path). Keep the behavior added by the teammate and the behavior
required by this task. Do not pick an entire side mechanically. If the intended
combined behavior cannot be established from contracts, record the precise
conflict and ask the human/module owner; do not guess or overwrite it.

STATE log entries are append-only: retain both developers' entries and their
ownership lines. Preserve completed work and blockers from both sides. Resolve
VERSION according to the serial/parallel rule below. Use the project's package
manager to regenerate a conflicted lockfile once its manifest is resolved.
Never regenerate or renumber a teammate's shipped migration blindly.

Record remote base, teammate commits, affected paths, resolution rationale and
checks in this iteration's committed note. If there was no concurrent change,
record that fact with the fetched base. Chat alone is insufficient evidence.

## Validate, review, push

Run checks for this task and every behavior affected by integration. Required
cross-tenant, server-role and RFID checks remain mandatory for new endpoints.
For docs-only changes validate links/frontmatter, skills and `git diff --check`;
do not claim nonexistent application tests passed. In paired sessions, the other agent reviews the
final candidate and independently runs relevant checks. Unpaired sessions follow
the ordinary project gates and teammate PR approval. Record its verdict,
candidate SHA and limitations in the PR; mailbox evidence alone is not durable.

Immediately before push fetch again. If main or the remote feature branch moved
in a way not yet integrated, repeat comparison, integration, checks and review.
Then use an ordinary push of the reviewed feature branch. A non-fast-forward
rejection means fetch and compare again, never force. If the remote keeps moving,
checkpoint and report the pending integration instead of spinning indefinitely.
A main update racing after the final fetch is handled again before PR merge;
never claim this procedure can eliminate all remote races.

Push each completed, reviewed iteration and create or update its PR. Include
what changed, checks, reviewer/candidate, integration outcome and remaining risks.
AGENTS.md §6.1 still requires at least one teammate approval; DevOps merges.

## Version ownership

Serial documentation/bootstrap changes bump VERSION once per completed iteration
(patch), with manifests matched if they exist. Parallel feature branches leave
VERSION unchanged; DevOps bumps it at merge, per ADR-007. Mark this exception
explicitly in the PR checklist. Never silently overwrite a teammate's version bump.
