---
title: "ADR-008 — Codex lead and Antigravity worker"
tags:
  - kind/decision
  - area/process
  - status/proposed
---

# ADR-008 — Codex lead and Antigravity worker

- **Date:** 2026-10-09
- **Status:** workstation profile authorized by Harshit; shared-rule changes proposed for teammate approval in this PR.
- **Decider for this workstation:** Harshit

## Context

Harshit's PC uses Codex and Antigravity. The existing
[[_meta/decisions/007-parallel-agents-claude-grok]] describes Claude/Grok; other
machines must retain that choice. New chats need committed recovery context,
not private transcripts. Concurrent pushes must preserve teammates' features.

## Options considered

1. Replace Claude/Grok globally: imposes one developer's tools on the team.
2. Add a workstation profile using the same lead/worker contracts: preserves
   team freedom while adding exact commands, review and usage rules.

## Decision

Option 2. Codex leads; Antigravity works and cross-reviews, using the persistent
worker conversation and verified `gemini-3.8-flash-high`. Newer available Gemini
Flash High versions may supersede it after verification and recording the change.
All machines use the common safe-publishing procedure; the Codex reserve is this
workstation's policy: at least 90% five-hour usage plus more than 40 minutes until
reset stops Codex work. At 40 minutes or less the remaining allowance may be used.

Details are maintained once in [[collaboration/codex-antigravity]],
[[collaboration/safe-publishing]] and [[collaboration/skills]].
The compact project skill routes to those notes. No daemon, polling loop,
permission bypass, auto-merge or full-transcript storage is introduced.

## Consequences

Every iteration has isolated ownership, independent review, a checked final
candidate, and committed decisions/status. Runtime conversation IDs and mailboxes
stay local. A reviewer outage prevents publication but permits isolated preparation.
Feature work and hardware remain unchanged. The existing serial/parallel VERSION
rules remain in force. Teammate approval is still required before DevOps merges.

## Verification

On 2026-10-09, `agy --help` verified conversation, print, JSON, model, add-dir and
sandbox flags; `agy models` listed Gemini 3.8 Flash High. The mandatory and review
skills were installed from pinned allowlisted sources. Runtime bootstrap/review
results and exact approved candidate belong in the PR for this iteration. The
OS rejected Antigravity sandbox execution on this PC; read-only plan-mode reviews
may use normal permissions with host per-command approval. Feature execution
requires working isolation or human-authorized alternative execution. Recovery:

[[collaboration/iterations/001-collaboration-bootstrap]]. End-to-end worker
implementation and ADR-007's larger concurrency remain future pilot checks.

Related: [[STATE]] · [[00 Index]].
