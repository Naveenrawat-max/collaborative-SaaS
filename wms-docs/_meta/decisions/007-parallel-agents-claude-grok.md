---
title: "ADR-007 — Parallel agents: Claude Code and Grok Build on one machine"
tags:
  - kind/decision
  - area/process
  - status/proposed
---

# ADR-007 — Parallel agents: Claude Code and Grok Build on one machine

- **Date:** 2026-10-09
- **Status:** proposed. Becomes accepted after the pilot in "Verify in the pilot" below.
- **Deciders:** Naveen, Harshit, Joseph

## Context

A developer wants two coding agents, Claude Code and Grok Build, building different
features of the same platform **at the same time**. Each agent cross-reviews the
other's work, so the result is ready faster than one agent working alone. Both
agents also spawn their own sub-agents.

Constraints:
- AGENTS.md rules still apply: contract-first, tenant isolation, small commits, no
  AI attribution, code and context in the same PR. Run procedure **C6** in
  `SKILL.md` for every parallel run.
- Grok runs as one long, interactive session in its own PowerShell tab. It never
  exits between tasks and is never resumed, because re-reading the whole chat on
  every resume costs tokens.
- Grok runs with `--sandbox`.
- The developer tells the team beforehand which features they are working on.
  DevOps merges everything into `main`, so nothing gets overwritten there.
- Agents must not block each other. A feature that depends on another feature's
  unfinished API is not a parallel task.

Facts checked on this machine (Grok Build `1.0.44`, `grok --help`):
- `--worktree [<name>]` starts a session in a new git worktree.
- `--sandbox <profile>`, `--permission-mode`, `--rules` (extra rules added to the
  system prompt), and `grok plugin install <git url | path>`.
- `grok inspect` shows which instruction files and skills Grok loads. On this repo
  it reported **"Project trusted: no"**, and only the global instruction files were
  loaded. Grok must trust the project before it reads this repo's `AGENTS.md`.

## Options considered

1. **One agent at a time** (status quo).
   - Pro: no coordination needed.
   - Con: slowest, and only one model ever looks at the code.
2. **Split by platform**: Claude on `backend/`, Grok on `android/`, at the same time.
   - Pro: the agents almost never touch the same files.
   - Con: one platform can't be finished before the next one starts. Phone and
     web screens are always waiting on a backend contract.
3. **Split by feature within one platform**: both agents on the same platform,
   on unrelated features, for example web sign-in vs tag registration screens.
   Each feature gets its own worktree and branch, and the two agents cross-review
   each other.
   - Pro: one platform at a time, as the developer prefers. Two models review
     every change.
   - Con: the features must have **separate file sets**. Shared files need a
     single owner (the lead).

## Decision

**Option 3, with option 2 as the fallback.** If two features can't be given
separate file sets, split by platform instead.

The working model:

| Part | Rule |
|---|---|
| **Roles** | Claude Code is the **lead**: it splits the work, writes the task briefs, owns the shared files and opens the PRs. Grok Build is the **worker**: it builds its features and reviews Claude's. Either agent may spawn sub-agents; every sub-agent gets its own worktree. |
| **One feature = one branch = one worktree = one PR** | Branch `feat/<module>-<thing>` (AGENTS.md §6.1). Worktrees live under `../wms-wt/<branch-name>/`. An agent never edits the main checkout while another agent is working. |
| **Mailbox** | Agents talk through files in `.agents/` at the main checkout's root. The folder is gitignored, because it holds runtime messages, not context. Task briefs, reports and reviews follow the templates in `SKILL.md` C6. |
| **File ownership** | Every task brief lists the paths that task may change. Only the lead edits the shared files: `wms-docs/STATE.md`, `VERSION`, `backend/config/*`, `backend/pyproject.toml`, `backend/uv.lock`, `web/package.json` and its lockfile, the Android Gradle files, and migrations of any app that two tasks touch. A worker that needs one of them changed asks for it in its report. |
| **Cross-review** | No branch is pushed until **the other agent** has reviewed it. Grok's work is reviewed by a Claude review sub-agent, and Claude's work by Grok. A reviewer reads the diff against `main`, runs the tests itself, checks the spec and AGENTS.md invariants, and checks both mandatory skills (below). Two rounds of fixes at most, then the human decides. |
| **Merging** | The lead pushes the reviewed branch and opens the PR (C5). DevOps merges it into `main`. Agents never merge into `main`. |
| **Mandatory skills** | Every agent loads and actively applies **karpathy-guidelines** (`forrestchang/andrej-karpathy-skills`) and **ponytail** (`DietrichGebert/ponytail`). If either is missing, the agent installs it first (SKILL.md A3). Each task brief also names any other skills to use. |
| **Version** | Feature PRs in a parallel run don't bump `VERSION`; DevOps bumps it when merging. This avoids a guaranteed conflict on one line. It overrides AGENTS.md §6.9 for parallel runs only. |
| **Concurrency** | At most **2 features per agent** at a time (4 in total) until the pilot shows how fast reviews keep up. Raise the limit in this ADR when it does. |

## Verify in the pilot

These are not proven yet. The first parallel run (one small feature per agent) must
answer each one and record the answer here, before this ADR is accepted:

1. **How Grok picks up a task without exiting.** It needs a trigger that doesn't
   restart the session. Try these in order and keep the first that works:
   1. Grok's standing brief tells it to check `.agents/inbox/grok/` after every
      task and wait for the next one.
   2. The human types `next` into Grok's tab when Claude reports that a brief is ready.
   3. A small bridge process that feeds the inbox to `grok agent stdio`. That is
      code, so it would need its own spec.
2. **Grok's `--worktree` and branch names:** does the branch it creates follow
   `feat/<module>-<thing>`?
3. **Sandbox profile name** for `--sandbox`. Record the exact profile, and confirm
   it still allows `git`, `uv`, `npm` and Gradle inside `../wms-wt/`.
4. **Project trust:** after trusting the repo, does `grok inspect` list this
   repo's `AGENTS.md`?
5. **Review throughput:** time per review compared with time per feature. If
   reviews take longer than builds, lower the concurrency limit.

## Consequences

- **Easier:**
  - Two features of one platform progress at once.
  - Every change gets a second model's review before a teammate sees it.
- **Harder:**
  - Splitting the work takes planning up front: each task needs a file list and
    a published contract.
  - Shared files go through the lead.
  - A worker that needs a shared file waits for the lead.
- **Constrains:** `SKILL.md` C6 (the procedure), AGENTS.md §3, §6 and §7, `.gitignore`
  (the `.agents/` mailbox), and every plan in `wms-docs/plans/` (each task lists the
  files it touches).
- **Out of scope:** agents on different machines (one per developer stays the
  normal team flow) and any automatic merge into `main`.

Related: [[STATE]] · [[_meta/decisions/001-stack-django-react]] · [[00 Index]]
