---
title: "Collaboration skills — install and load"
tags:
  - kind/doc
  - area/process
  - status/current
---

# Collaboration skills — install and load

All agents follow `SKILL.md` A/B. This note records the verified installation
for [[collaboration/codex-antigravity]]; it does not extend the third-party allowlist.

| Skill | Source repository | Path | Required use |
|---|---|---|---|
| karpathy-guidelines | forrestchang/andrej-karpathy-skills | skills/karpathy-guidelines | every task |
| ponytail | DietrichGebert/ponytail | skills/ponytail | every task |
| ponytail-review | DietrichGebert/ponytail | skills/ponytail-review | review |
| requesting-code-review | obra/superpowers | skills/requesting-code-review | independent review |
| using-git-worktrees | obra/superpowers | skills/using-git-worktrees | isolated work |

Installed on this PC on 2026-10-09 in `C:/Users/harsh/.codex/skills/<skill>/`.
Both agents explicitly read the installed `SKILL.md` files before applying them;
a directory existing is not proof that a harness loaded its instructions.
Codex can discover user skills on a subsequent turn. Antigravity can use the same
files through explicit reads, as SKILL.md A's "Any other agent" row permits.
Other developers install the same sources in their harness's supported location.

Pinned upstream revisions used for this installation:
- karpathy: `2c606141936f1eeef17fa3043a72095b4765b9c2`
- ponytail and ponytail-review: `9cc65d03aa2da1db7121b912d03596409ee340b8`
- superpowers review/worktrees: `8ca22dba9a94f28898bbce59f2537ff4d87c747d`

Use Codex's bundled `skill-installer/scripts/install-skill-from-github.py` with
`--repo`, `--ref` and `--path` from the table. It installs the skill directory,
including its references. Use an available Python interpreter; no project
application dependencies are required. Do not overwrite an existing installation
without reading its provenance and checking local modifications.

Before loading a new or updated skill, read its instructions and referenced
executables; scan for downloads, eval, credential access, deletion and secret
handling as SKILL.md A requires. The scan is a prompt to inspect, not proof of
malice. The installed skills here contained only review/context and security
checklist matches, with no suspicious executable action required. Upgrade only
from the allowlist, inspect changes and record the new revision. Install other
registry skills when the task requires them, not the whole catalog by default.

The project-owned compact skill is `.agents/skills/wms-collaboration/SKILL.md`.
It routes to these committed procedures instead of duplicating them. Codex scans
repo `.agents/skills`; other harnesses explicitly read the same file if their
native discovery differs. Source: https://learn.chatgpt.com/docs/build-skills.
Read it when coordinating this PC, recovering context, reviewing an iteration
or publishing. Keep runtime inbox/outbox files ignored; keep this skill tracked.

Related: [[STATE]] · [[00 Index]].
