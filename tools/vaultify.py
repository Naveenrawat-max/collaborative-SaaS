#!/usr/bin/env python3
"""
vaultify - turn any project folder into a live Obsidian vault with a real dependency graph.

    vaultify init  [PATH]      create .obsidian/ config + scaffold notes
    vaultify sync  [PATH]      scan code, (re)write linked companion notes + code map
    vaultify open  [PATH]      register the vault and open it in Obsidian
    vaultify all   [PATH]      init + sync + open
    vaultify watch [PATH]      re-sync whenever a file changes
    vaultify agents [PATH]     append/refresh the vault rules in your AGENT.md

Stdlib only. Works on macOS, Linux and Windows.
"""

from __future__ import annotations

import argparse
import ast
import json
import os
import re
import secrets
import shutil
import subprocess
import sys
import time
import urllib.parse
from pathlib import Path

AUTO_START = "<!-- vaultify:auto:start -->"
AUTO_END = "<!-- vaultify:auto:end -->"
AGENTS_START = "<!-- vaultify:agents:start -->"
AGENTS_END = "<!-- vaultify:agents:end -->"

AGENT_FILES = ["AGENT.md", "AGENTS.md", "CLAUDE.md", ".cursorrules",
               ".github/copilot-instructions.md"]

AGENTS_SECTION = """\
## Knowledge-vault conventions (project-scoped)

Subordinate to the global operating rules. Where these conflict with anything in the
global file, the global file wins.

**Ownership.** The `docs` domain owns this folder's notes and link graph. No other
domain writes notes. If a task changes a contract, it touches `docs` and is therefore
multi-domain — classify it that way.

**Mechanical sync is a build step, not a domain action.** Regenerating `_code/` from
import statements is deterministic and derived, like a lockfile or generated types. It
runs from a harness hook or a background `vaultify watch`, never as an agent decision,
so it crosses no lane. Only *prose* in notes is `docs` work.

**Bootstrapping.** `vaultify init .` writes `.obsidian/` (wikilinks, arrows in graph
view, tag colour groups), `00 Index.md` and `_meta/Conventions.md`.

**Notes**

- Frontmatter on line 1 or Obsidian silently ignores it. Always `title` and `tags`.
- No orphans. Every note links to an existing note with `[[wikilinks]]` and is
  reachable from `00 Index.md`.
- Link inline in prose (`the refresh path lives in [[_code/src/auth-py]]`), not as a
  "Related" dump at the bottom.
- One idea per note. Two `#` headings that could stand alone means split and link.
- Tag namespaces drive the preset graph colours: `kind/` (doc, code, map, decision),
  `area/`, `status/`, `role/`.
- Practical means actionable: real paths, real commands, real values. Every note
  answers one of — how do I run this, what breaks if I change it, why is it this way.

**Wiring into the global protocol**

- The `docs` pass consumes the **Contract** and **Do NOT change** lines from each
  role's HANDOFF block. Those become the note bodies; nothing gets re-derived by hand.
- Contract changes get an ADR at `_meta/decisions/NNN-slug.md`, wikilinked from the
  code notes it constrains.
- Issues found but out of scope go in `NOTES.md` per the global no-scope-creep rule —
  do not open a note and start fixing.
- `docs` runs after the testing and security gates pass, so notes describe what
  shipped rather than what was planned.

**Code notes**

- `vaultify sync .` parses real imports and writes one companion note per source file
  into `_code/`, wikilinked to its dependencies.
- Never hand-edit inside the `vaultify:auto` markers — the next sync overwrites them.
  Write below `<!-- vaultify:auto:end -->`; that region is preserved permanently. Put
  "why this file exists" and any gotchas there.
- Every source file gets a module docstring or header comment. Sync lifts the first
  line into the companion note; no docstring means a blank note.
- After sync, check `_code/00 Code map.md` for isolated files. An unexpected one is
  dead code or a missing wire-up — that is a finding for the HANDOFF **Open risks**
  line, not something to silently fix.
- Hand off with `vaultify open . --restart`.
"""

SKIP_DIRS = {
    ".git", ".hg", ".svn", ".obsidian", ".idea", ".vscode", "node_modules",
    "__pycache__", ".mypy_cache", ".pytest_cache", ".ruff_cache", ".tox",
    "venv", ".venv", "env", "dist", "build", "target", "out", ".next",
    ".nuxt", ".svelte-kit", "coverage", "vendor", ".terraform", ".gradle",
    "Pods", ".cargo", "site-packages", ".cache",
}

LANGS = {
    ".py": "python", ".pyi": "python",
    ".ts": "typescript", ".tsx": "typescript",
    ".js": "javascript", ".jsx": "javascript", ".mjs": "javascript", ".cjs": "javascript",
    ".rs": "rust", ".go": "go",
    ".c": "c", ".h": "c", ".cc": "cpp", ".cpp": "cpp", ".hpp": "cpp", ".hh": "cpp",
    ".rb": "ruby", ".java": "java", ".kt": "kotlin", ".swift": "swift",
    ".php": "php", ".cs": "csharp", ".sh": "shell", ".bash": "shell",
    ".sql": "sql", ".vue": "vue", ".svelte": "svelte",
}

JS_EXTS = [".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".vue", ".svelte"]

# ---------------------------------------------------------------- config files

APP_JSON = {
    "attachmentFolderPath": "_attachments",
    "alwaysUpdateLinks": True,
    "newLinkFormat": "absolute",
    "useMarkdownLinks": False,
    "showUnsupportedFiles": True,
    "showInlineTitle": True,
    "readableLineLength": False,
    "strictLineBreaks": False,
    "userIgnoreFilters": [
        ".git/", "node_modules/", "__pycache__/", ".venv/", "venv/",
        "dist/", "build/", "target/", ".next/", "coverage/",
    ],
}

CORE_PLUGINS = {
    "file-explorer": True, "global-search": True, "switcher": True,
    "graph": True, "backlink": True, "outgoing-link": True,
    "tag-pane": True, "properties": True, "page-preview": True,
    "outline": True, "word-count": True, "bookmarks": True,
    "canvas": True, "templates": True, "file-recovery": True,
}


def _rgb(hex_str: str) -> int:
    return int(hex_str.lstrip("#"), 16)


GRAPH_JSON = {
    "collapse-filter": False,
    "search": "",
    "showTags": True,
    "showAttachments": False,
    "hideUnresolved": True,
    "showOrphans": True,
    "collapse-color-groups": False,
    "colorGroups": [
        {"query": "tag:#kind/doc", "color": {"a": 1, "rgb": _rgb("#7f9cf5")}},
        {"query": "tag:#kind/code", "color": {"a": 1, "rgb": _rgb("#48bb78")}},
        {"query": "tag:#role/entrypoint", "color": {"a": 1, "rgb": _rgb("#ed8936")}},
        {"query": "tag:#role/hub", "color": {"a": 1, "rgb": _rgb("#f56565")}},
        {"query": "tag:#kind/map", "color": {"a": 1, "rgb": _rgb("#d69e2e")}},
    ],
    "collapse-display": False,
    "showArrow": True,
    "textFadeMultiplier": -0.6,
    "nodeSizeMultiplier": 1.3,
    "lineSizeMultiplier": 1,
    "collapse-forces": False,
    "centerStrength": 0.4,
    "repelStrength": 12,
    "linkStrength": 0.6,
    "linkDistance": 220,
    "scale": 1,
}

# ---------------------------------------------------------------- small helpers


def write_json(path: Path, data: dict, merge: bool = True) -> None:
    existing = {}
    if merge and path.exists():
        try:
            existing = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            existing = {}
    existing.update(data)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(existing, indent=2) + "\n", encoding="utf-8")


def write_managed(path: Path, frontmatter: str, body: str) -> None:
    """Frontmatter stays on line 1 (Obsidian requires it there); the auto block holds
    generated body; anything the human or agent writes after AUTO_END is preserved."""
    block = f"{AUTO_START}\n{body.strip()}\n{AUTO_END}\n"
    tail = ""
    if path.exists():
        old = path.read_text(encoding="utf-8")
        if AUTO_END in old:
            tail = old.split(AUTO_END, 1)[1]
        elif AUTO_START not in old:
            tail = "\n" + old.strip() + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(frontmatter.strip() + "\n\n" + block + tail.lstrip("\n"),
                    encoding="utf-8")


def note_name(rel: Path) -> str:
    """src/main.py -> src/main-py   (avoids Obsidian treating .py as the extension)"""
    parent = rel.parent.as_posix()
    stem = rel.name.replace(".", "-")
    return f"{parent}/{stem}" if parent != "." else stem


def iter_files(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        for fn in filenames:
            p = Path(dirpath) / fn
            if p.suffix.lower() in LANGS:
                yield p.relative_to(root)


def read(root: Path, rel: Path) -> str:
    try:
        return (root / rel).read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


# ---------------------------------------------------------------- import parsers


def py_module_index(files: list[Path]) -> dict[str, Path]:
    idx: dict[str, Path] = {}
    for rel in files:
        if rel.suffix not in (".py", ".pyi"):
            continue
        parts = list(rel.with_suffix("").parts)
        if parts[-1] == "__init__":
            parts = parts[:-1]
        if not parts:
            continue
        # register under the full path and under each trimmed prefix (src/ layouts)
        for start in range(len(parts)):
            idx.setdefault(".".join(parts[start:]), rel)
    return idx


def py_deps(root: Path, rel: Path, idx: dict[str, Path]) -> set[Path]:
    out: set[Path] = set()
    try:
        tree = ast.parse(read(root, rel))
    except Exception:
        return out
    pkg = list(rel.parent.parts)
    for node in ast.walk(tree):
        names: list[str] = []
        if isinstance(node, ast.Import):
            names = [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom):
            base = node.module or ""
            if node.level:
                up = pkg[: len(pkg) - (node.level - 1)] if node.level > 1 else pkg
                names = [".".join([*up, base]) if base else ".".join(up)]
            else:
                names = [base]
            names += [f"{names[0]}.{a.name}" for a in node.names if names and names[0]]
        for n in names:
            while n:
                if n in idx and idx[n] != rel:
                    tgt = idx[n]
                    # an empty __init__.py is packaging noise, not a real dependency
                    if not (tgt.name == "__init__.py"
                            and len([l for l in read(root, tgt).splitlines() if l.strip()]) < 2):
                        out.add(tgt)
                    break
                n = n.rpartition(".")[0]
    return out


JS_IMPORT = re.compile(
    r"""(?:\bfrom\s*|\brequire\s*\(\s*|\bimport\s*\(\s*|\bimport\s+)['"]([^'"]+)['"]""")


def js_deps(root: Path, rel: Path, known: set[Path]) -> set[Path]:
    out: set[Path] = set()
    for spec in JS_IMPORT.findall(read(root, rel)):
        if not spec.startswith("."):
            continue
        base = (rel.parent / spec)
        for cand in [base, *(base.with_name(base.name + e) for e in JS_EXTS),
                     *(base / f"index{e}" for e in JS_EXTS)]:
            try:
                c = Path(os.path.normpath(cand))
            except Exception:
                continue
            if c in known and c != rel:
                out.add(c)
                break
    return out


RS_MOD = re.compile(r"^\s*(?:pub\s+)?mod\s+([A-Za-z_][A-Za-z0-9_]*)\s*;", re.M)


def rs_deps(root: Path, rel: Path, known: set[Path]) -> set[Path]:
    out = set()
    for name in RS_MOD.findall(read(root, rel)):
        stem = rel.parent if rel.stem in ("mod", "lib", "main") else rel.parent / rel.stem
        for cand in (stem / f"{name}.rs", stem / name / "mod.rs"):
            c = Path(os.path.normpath(cand))
            if c in known and c != rel:
                out.add(c)
    return out


C_INCLUDE = re.compile(r'^\s*#\s*include\s*"([^"]+)"', re.M)


def c_deps(root: Path, rel: Path, known: set[Path]) -> set[Path]:
    out = set()
    for spec in C_INCLUDE.findall(read(root, rel)):
        for base in (rel.parent / spec, Path(spec)):
            c = Path(os.path.normpath(base))
            if c in known and c != rel:
                out.add(c)
    return out


GO_IMPORT = re.compile(r'^\s*(?:import\s+)?(?:[\w.]+\s+)?"([^"]+)"', re.M)


def go_deps(root: Path, rel: Path, known: set[Path], module: str | None) -> set[Path]:
    if not module:
        return set()
    out = set()
    for spec in GO_IMPORT.findall(read(root, rel)):
        if not spec.startswith(module):
            continue
        d = Path(spec[len(module):].lstrip("/"))
        for k in known:
            if k.suffix == ".go" and k.parent == d and k != rel:
                out.add(k)
    return out


def build_graph(root: Path, files: list[Path]) -> dict[Path, set[Path]]:
    known = set(files)
    pidx = py_module_index(files)
    module = None
    gomod = root / "go.mod"
    if gomod.exists():
        m = re.search(r"^module\s+(\S+)", gomod.read_text(errors="replace"), re.M)
        module = m.group(1) if m else None

    graph: dict[Path, set[Path]] = {}
    for rel in files:
        lang = LANGS.get(rel.suffix.lower(), "")
        if lang == "python":
            deps = py_deps(root, rel, pidx)
        elif lang in ("typescript", "javascript", "vue", "svelte"):
            deps = js_deps(root, rel, known)
        elif lang == "rust":
            deps = rs_deps(root, rel, known)
        elif lang in ("c", "cpp"):
            deps = c_deps(root, rel, known)
        elif lang == "go":
            deps = go_deps(root, rel, known, module)
        else:
            deps = set()
        graph[rel] = deps
    return graph


# ---------------------------------------------------------------- note writing


def first_docstring(root: Path, rel: Path) -> str:
    text = read(root, rel)
    if rel.suffix in (".py", ".pyi"):
        try:
            doc = ast.get_docstring(ast.parse(text))
            if doc:
                return doc.strip().split("\n")[0][:200]
        except Exception:
            pass
    for line in text.splitlines()[:8]:
        s = line.strip()
        if s.startswith(("///", "//!", "/**", "* ", "//", "#")) and len(s) > 4:
            return s.lstrip("/*#! ").strip()[:200]
    return ""


def public_symbols(root: Path, rel: Path) -> list[str]:
    text = read(root, rel)
    if rel.suffix in (".py", ".pyi"):
        try:
            tree = ast.parse(text)
        except Exception:
            return []
        return [n.name for n in tree.body
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
                and not n.name.startswith("_")][:25]
    pats = [r"export\s+(?:default\s+)?(?:async\s+)?(?:function|class|const|let|type|interface|enum)\s+(\w+)",
            r"pub\s+(?:async\s+)?(?:fn|struct|enum|trait|mod)\s+(\w+)",
            r"^func\s+(?:\([^)]*\)\s*)?([A-Z]\w*)"]
    found: list[str] = []
    for p in pats:
        found += re.findall(p, text, re.M)
    seen, res = set(), []
    for f in found:
        if f not in seen:
            seen.add(f)
            res.append(f)
    return res[:25]


def sync(root: Path, notes_dir: str = "_code", quiet: bool = False,
         bidirectional: bool = False) -> dict:
    files = sorted(iter_files(root))
    if not files:
        if not quiet:
            print("no source files found - nothing to map")
        return {"files": 0}

    graph = build_graph(root, files)
    dependents: dict[Path, set[Path]] = {f: set() for f in files}
    for src, deps in graph.items():
        for d in deps:
            dependents[d].add(src)

    ndir = root / notes_dir
    names: dict[Path, str] = {}
    used: set[str] = set()
    for rel in files:
        n = note_name(rel)
        while n in used:
            n += "-1"
        used.add(n)
        names[rel] = n

    for rel in files:
        lang = LANGS.get(rel.suffix.lower(), "text")
        deps = sorted(graph[rel])
        rdeps = sorted(dependents[rel])
        loc = len(read(root, rel).splitlines())
        role = []
        if not rdeps and deps:
            role.append("role/entrypoint")
        if len(rdeps) >= 4:
            role.append("role/hub")
        if not deps and not rdeps:
            role.append("role/isolated")
        tags = ["kind/code", f"lang/{lang}", *role]
        if rel.parent != Path("."):
            tags.append("area/" + rel.parent.as_posix().replace("/", "-"))

        fm = "\n".join([
            "---",
            f'title: "{rel.as_posix()}"',
            f'source: "{rel.as_posix()}"',
            f"language: {lang}",
            f"lines: {loc}",
            f"imports: {len(deps)}",
            f"imported_by: {len(rdeps)}",
            "tags:",
            *[f"  - {t}" for t in tags],
            "---",
        ])

        lines = [f"# `{rel.as_posix()}`", ""]
        summary = first_docstring(root, rel)
        if summary:
            lines += [f"> {summary}", ""]
        lines += ["## Imports", ""]
        lines += ([f"- [[{notes_dir}/{names[d]}|{d.as_posix()}]]" for d in deps]
                  or ["_no internal imports_"])
        lines += ["", "## Imported by", ""]
        if not rdeps:
            lines += ["_nothing in this project imports it_"]
        elif bidirectional:
            lines += [f"- [[{notes_dir}/{names[d]}|{d.as_posix()}]]" for d in rdeps]
        else:
            # plain text keeps graph edges one-directional so arrows stay meaningful;
            # the Backlinks pane renders these live and clickable anyway
            lines += [f"- `{d.as_posix()}`" for d in rdeps]
            lines += ["", "_(clickable in the Backlinks pane)_"]
        syms = public_symbols(root, rel)
        if syms:
            lines += ["", "## Public surface", "", ", ".join(f"`{s}`" for s in syms)]
        lines += ["", "## Notes", "", f"Part of [[{notes_dir}/00 Code map]].", ""]
        write_managed(ndir / f"{names[rel]}.md", fm, "\n".join(lines))

    # ---- code map
    by_dir: dict[str, list[Path]] = {}
    for rel in files:
        by_dir.setdefault(rel.parent.as_posix(), []).append(rel)
    entry = [f for f in files if not dependents[f] and graph[f]]
    hubs = sorted(files, key=lambda f: -len(dependents[f]))[:10]
    hubs = [h for h in hubs if dependents[h]]
    iso = [f for f in files if not graph[f] and not dependents[f]]
    edges = sum(len(v) for v in graph.values())

    map_fm = "\n".join(["---", 'title: "Code map"', "tags:", "  - kind/map", "---"])
    m = ["# Code map", "",
         f"{len(files)} source files, {edges} internal dependency edges, "
         f"{len(by_dir)} directories.", "",
         "| | |", "|---|---|",
         f"| Entry points | {len(entry)} |",
         f"| Isolated files | {len(iso)} |",
         f"| Most depended-on | {hubs[0].as_posix() if hubs else '-'} |", ""]

    if entry:
        m += ["## Entry points", "",
              *[f"- [[{notes_dir}/{names[f]}|{f.as_posix()}]]" for f in entry[:20]], ""]
    if hubs:
        m += ["## Hubs (most imported)", "",
              *[f"- [[{notes_dir}/{names[f]}|{f.as_posix()}]] "
                f"— {len(dependents[f])} dependents" for f in hubs], ""]
    if iso:
        m += ["## Isolated (no internal links — review these)", "",
              *[f"- [[{notes_dir}/{names[f]}|{f.as_posix()}]]" for f in iso[:30]], ""]

    m += ["## By directory", ""]
    for d in sorted(by_dir):
        m += [f"### `{d}`", "",
              *[f"- [[{notes_dir}/{names[f]}|{f.name}]]" for f in sorted(by_dir[d])], ""]

    if len(files) <= 45 and edges:
        m += ["## Dependency diagram", "", "```mermaid", "graph LR"]
        ids = {f: f"n{i}" for i, f in enumerate(files)}
        for f in files:
            if graph[f] or dependents[f]:
                m.append(f'  {ids[f]}["{f.as_posix()}"]')
        for f, deps in graph.items():
            for d in deps:
                m.append(f"  {ids[f]} --> {ids[d]}")
        m += ["```", ""]

    write_managed(ndir / "00 Code map.md", map_fm, "\n".join(m))
    if not quiet:
        print(f"synced {len(files)} files / {edges} edges -> {notes_dir}/")
    return {"files": len(files), "edges": edges}


# ---------------------------------------------------------------- init


def init(root: Path, name: str | None = None, notes_dir: str = "_code") -> None:
    root.mkdir(parents=True, exist_ok=True)
    cfg = root / ".obsidian"
    write_json(cfg / "app.json", APP_JSON)
    write_json(cfg / "core-plugins.json", CORE_PLUGINS)
    write_json(cfg / "graph.json", GRAPH_JSON)
    write_json(cfg / "appearance.json", {"accentColor": "", "theme": "obsidian"})
    (root / "_attachments").mkdir(exist_ok=True)

    vault = name or root.name
    index = root / "00 Index.md"
    if not index.exists():
        index.write_text(
            f"---\ntitle: \"{vault}\"\ntags:\n  - kind/map\n---\n\n"
            f"# {vault}\n\n"
            "Vault root. Everything reachable from here.\n\n"
            "## Maps\n\n"
            f"- [[{notes_dir}/00 Code map]] — every source file, what it imports, "
            "what imports it\n"
            "- [[_meta/Conventions]] — how notes in this vault are written\n\n"
            "## Decisions\n\n_ADRs go in `_meta/decisions/`._\n\n"
            "## Open threads\n\n- \n",
            encoding="utf-8")

    conv = root / "_meta" / "Conventions.md"
    if not conv.exists():
        conv.parent.mkdir(parents=True, exist_ok=True)
        conv.write_text(
            "---\ntitle: \"Conventions\"\ntags:\n  - kind/doc\n---\n\n"
            "# Conventions\n\n"
            "- Every note has YAML frontmatter with `title` and `tags`.\n"
            "- Every note links to at least one other note. No orphans.\n"
            "- Tag namespaces: `kind/`, `lang/`, `area/`, `role/`, `status/`.\n"
            "- Auto-generated regions sit between `vaultify:auto` markers. "
            "Anything outside them is preserved across syncs — put your own "
            "prose there.\n"
            f"- Code companion notes live in `{notes_dir}/` and mirror the source tree.\n",
            encoding="utf-8")
    print(f"initialised vault: {root}")


def install_agents(root: Path, target: str | None = None) -> None:
    """Append (or refresh) the Obsidian section in an existing agent instruction file."""
    path = None
    if target:
        path = root / target
    else:
        for cand in AGENT_FILES:
            if (root / cand).exists():
                path = root / cand
                break
    if path is None:
        path = root / "AGENTS.md"

    block = f"{AGENTS_START}\n{AGENTS_SECTION.strip()}\n{AGENTS_END}\n"
    if path.exists():
        old = path.read_text(encoding="utf-8")
        shutil.copy2(path, path.with_suffix(path.suffix + ".vaultify-bak"))
        if AGENTS_START in old and AGENTS_END in old:
            head, rest = old.split(AGENTS_START, 1)
            _, tail = rest.split(AGENTS_END, 1)
            path.write_text(head + block + tail.lstrip("\n"), encoding="utf-8")
            print(f"refreshed existing Obsidian section in {path.name} "
                  f"(backup: {path.name}.vaultify-bak)")
            return
        path.write_text(old.rstrip() + "\n\n" + block, encoding="utf-8")
        print(f"appended Obsidian section to {path.name} "
              f"({len(old.splitlines())} existing lines untouched, "
              f"backup: {path.name}.vaultify-bak)")
        return
    path.write_text(block, encoding="utf-8")
    print(f"created {path.name}")


# ---------------------------------------------------------------- open / register


def obsidian_config_dir() -> Path | None:
    home = Path.home()
    cands = []
    if sys.platform == "darwin":
        cands.append(home / "Library/Application Support/obsidian")
    elif os.name == "nt":
        appdata = os.environ.get("APPDATA")
        if appdata:
            cands.append(Path(appdata) / "obsidian")
    else:
        xdg = os.environ.get("XDG_CONFIG_HOME")
        cands.append(Path(xdg) / "obsidian" if xdg else home / ".config/obsidian")
        cands.append(home / ".var/app/md.obsidian.Obsidian/config/obsidian")
        cands.append(home / "snap/obsidian/current/.config/obsidian")
    for c in cands:
        if c.exists():
            return c
    return cands[0] if cands else None


def obsidian_running() -> bool:
    try:
        if os.name == "nt":
            out = subprocess.run(["tasklist"], capture_output=True, text=True, timeout=10)
            return "obsidian" in out.stdout.lower()
        return subprocess.run(["pgrep", "-fi", "obsidian"],
                              capture_output=True, timeout=10).returncode == 0
    except Exception:
        return False


def register(root: Path, name: str | None = None) -> tuple[bool, str]:
    """Add the vault to obsidian.json. Returns (was_new, vault_name)."""
    cfgdir = obsidian_config_dir()
    vault = name or root.name
    if cfgdir is None:
        return False, vault
    cfgdir.mkdir(parents=True, exist_ok=True)
    f = cfgdir / "obsidian.json"
    data = {}
    if f.exists():
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            data = {}
        shutil.copy2(f, f.with_suffix(".json.vaultify-bak"))
    vaults = data.setdefault("vaults", {})
    target = str(root.resolve())
    for vid, v in vaults.items():
        if str(Path(v.get("path", "")).resolve()) == target:
            v["ts"] = int(time.time() * 1000)
            f.write_text(json.dumps(data, indent=2), encoding="utf-8")
            return False, Path(target).name
    vaults[secrets.token_hex(8)] = {
        "path": target, "ts": int(time.time() * 1000), "open": False}
    f.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return True, vault


def launch_uri(uri: str) -> None:
    try:
        if sys.platform == "darwin":
            subprocess.run(["open", uri], check=False)
        elif os.name == "nt":
            os.startfile(uri)  # type: ignore[attr-defined]
        else:
            subprocess.run(["xdg-open", uri], check=False)
    except Exception as e:
        print(f"could not launch Obsidian automatically ({e}). Open this URI manually:\n  {uri}")


def kill_obsidian() -> None:
    try:
        if os.name == "nt":
            subprocess.run(["taskkill", "/IM", "Obsidian.exe", "/F"],
                           capture_output=True, check=False)
        else:
            subprocess.run(["pkill", "-fi", "obsidian"], capture_output=True, check=False)
        time.sleep(2)
    except Exception:
        pass


def open_vault(root: Path, name: str | None = None,
               file: str | None = None, restart: bool = False) -> None:
    was_new, vault = register(root, name)
    if was_new and obsidian_running():
        if restart:
            print("new vault registered - restarting Obsidian to reload its config")
            kill_obsidian()
        else:
            print("NOTE: Obsidian was already running. It caches its vault list, so a "
                  "brand-new vault may report 'vault not registered'. Re-run with "
                  "--restart, or quit and reopen Obsidian once.")
    q = {"vault": vault}
    if file:
        q["file"] = file
    launch_uri("obsidian://open?" + urllib.parse.urlencode(q))
    print(f"opening vault '{vault}'")


# ---------------------------------------------------------------- watch


def watch(root: Path, notes_dir: str, interval: float = 2.0) -> None:
    print(f"watching {root} (ctrl-c to stop)")
    last: dict[Path, float] = {}
    while True:
        cur = {}
        for rel in iter_files(root):
            try:
                cur[rel] = (root / rel).stat().st_mtime
            except OSError:
                pass
        if cur != last:
            if last:
                sync(root, notes_dir)
            last = cur
        time.sleep(interval)


# ---------------------------------------------------------------- cli


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="vaultify", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("command",
                   choices=["init", "sync", "open", "all", "watch", "agents"])
    p.add_argument("path", nargs="?", default=".")
    p.add_argument("--name", help="vault name (default: folder name)")
    p.add_argument("--notes-dir", default="_code", help="where code notes go")
    p.add_argument("--file",
                   help="note to focus when opening; or target file for `agents`")
    p.add_argument("--restart", action="store_true",
                   help="restart Obsidian if a new vault was registered")
    p.add_argument("--bidirectional", action="store_true",
                   help="link dependents too (loses clean arrow direction)")
    p.add_argument("--quiet", action="store_true")
    a = p.parse_args(argv)
    root = Path(a.path).expanduser().resolve()

    if a.command in ("init", "all"):
        init(root, a.name, a.notes_dir)
    if a.command in ("sync", "all"):
        sync(root, a.notes_dir, a.quiet, a.bidirectional)
    if a.command in ("open", "all"):
        open_vault(root, a.name, a.file, a.restart)
    if a.command == "agents":
        install_agents(root, a.file)
    if a.command == "watch":
        try:
            watch(root, a.notes_dir)
        except KeyboardInterrupt:
            print("\nstopped")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
