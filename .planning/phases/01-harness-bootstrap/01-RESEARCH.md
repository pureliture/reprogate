# Phase 01: Harness Bootstrap - Research

**Researched:** 2026-04-02
**Domain:** Python CLI tooling, Claude Code settings.json schema, JSON file manipulation, path-pattern gating, template identity
**Confidence:** HIGH (based on direct codebase inspection and ADR reading)

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
All implementation choices are at Claude's discretion — pure infrastructure phase. Use ROADMAP success criteria (INIT-01 through INIT-06) and existing codebase conventions to guide all decisions.

Key constraints from requirements:
- `reprogate init` must modify `.claude/settings.json` (hooks injection)
- `reprogate disable` must remove hook config from `.claude/settings.json`
- `REPROGATE_DISABLED=1` env var disables hook layer (no file changes needed)
- `record_triggers` in `reprogate.yaml` gates record requirements
- Schema alignment between `init.py` output and `generate.py` expectations

### Claude's Discretion
All implementation choices.

### Deferred Ideas (OUT OF SCOPE)
None — discuss phase skipped.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| INIT-01 | `reprogate init` injects hook config into `.claude/settings.json` and creates `.claude/session-data/` directory | JSON read/merge/write pattern; session-data directory creation; hook schema documented below |
| INIT-02 | `REPROGATE_DISABLED=1` env var disables hook layer without uninstalling | Hook scripts must check `os.environ.get("REPROGATE_DISABLED")` and exit 0 early; settings.json is unchanged |
| INIT-03 | `reprogate disable` removes hook config from `.claude/settings.json` | Inverse of INIT-01: read JSON, remove ReproGate keys, write back |
| INIT-04 | `reprogate.yaml` `record_triggers` path patterns gate record requirements | ADR-014 defines schema; `gatekeeper.py` needs pattern-matching against git diff file list |
| INIT-05 | Fix `generate.py` schema misalignment with `init.py` output schema | Schema gap documented in detail below — two incompatible schemas exist |
| INIT-06 | Update `AGENTS.md.j2` and `CLAUDE.md.j2` templates with harness identity | Old text: "compiler/gatekeeper" — replace with "delivery harness" identity |
</phase_requirements>

---

## Summary

Phase 01 implements the harness installation surface for ReproGate. It consists of six tightly scoped sub-tasks: (1) `reprogate init` hook injection, (2) `REPROGATE_DISABLED` env var support, (3) `reprogate disable` hook removal, (4) `record_triggers` path-pattern gating in `gatekeeper.py`, (5) schema alignment between `init.py` and `generate.py`, and (6) template identity text updates.

The core technical challenge is INIT-05: there are currently **two incompatible YAML schemas** in the codebase. `init.py` generates `reprogate.yaml` with gatekeeper fields (`project_name`, `reprogate_version`, `records_dir`, `record_types`, `skills_dir`, `gatekeeper`), while `generate.py`'s `load_config()` expects project/workspace/tools fields (`project.name`, `workspaces.primary.name`, `tools.claude`, `records.wp_path`). The live `reprogate.yaml` in the repo uses the gatekeeper schema — so `generate.py` silently falls back to defaults for everything it reads. This must be resolved by defining a unified canonical schema and updating both scripts.

The INIT-01/INIT-03 work requires careful JSON manipulation of `.claude/settings.json` — the file already exists with GSD hooks that must be preserved. ReproGate's hook entries must be injected under a distinct key (or as a clearly marked group) so disable can remove only ReproGate entries.

**Primary recommendation:** Implement in dependency order — INIT-05 (schema fix) first, then INIT-01/INIT-03 (hook injection/removal), then INIT-04 (record triggers), then INIT-02 (env var in future hook scripts), then INIT-06 (template text). INIT-02 is effectively a design contract for Phase 2 hook scripts rather than standalone code.

---

## Project Constraints (from CLAUDE.md)

- Language: Python 3.10+, Shell (Bash), Markdown
- Runtime: Python 3.10+, `uv` toolchain (`uv run python3 <script>`)
- Testing: `pytest` via `uv run python3 -m pytest scripts/tests/`
- Code style: PEP 8, snake_case functions/files, PascalCase classes, 4-space indent
- Error handling: `try/except` for specific errors, `sys.exit(main())`, stderr for errors
- No mutation: always create new objects/dicts rather than mutating in-place
- Functions: focused (<50 lines), type-hinted, explicit return types
- Files: cohesive (<800 lines), organized by feature
- Entry point: `scripts/cli.py` routes all subcommands via `run_script()`
- No direct repo edits outside GSD workflow unless user explicitly asks

---

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python stdlib `json` | 3.10+ | Read/write `.claude/settings.json` | No extra deps; JSON is simple dict manipulation |
| Python stdlib `pathlib` | 3.10+ | Path resolution throughout scripts | Already used in all scripts |
| Python stdlib `os` | 3.10+ | `os.environ.get("REPROGATE_DISABLED")` for env var check | Stdlib; no overhead |
| Python stdlib `fnmatch` | 3.10+ | Path-pattern matching for `record_triggers` | Handles `**` glob patterns with `pathlib.PurePosixPath.match()` |
| `PyYAML` | >=6.0 | Read/write `reprogate.yaml` | Already a project dependency |
| `argparse` | stdlib | Add `disable` subcommand to CLI | Already used in `cli.py` |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| Python stdlib `subprocess` | 3.10+ | `git diff --name-only HEAD` for changed files | Only in gatekeeper record_triggers evaluation |
| Python stdlib `shutil` | 3.10+ | Directory creation | Only for `.claude/session-data/` init |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| `fnmatch` / `pathlib.match()` | `glob` module | `pathlib.PurePosixPath.match()` handles `**` natively in Python 3.12+; for 3.10 use `fnmatch.fnmatch` with `**/` expansion |
| `json` stdlib | `pydantic` | No pydantic dep in project; stdlib is sufficient for flat settings.json manipulation |

**Installation:** No new dependencies required. All needed modules are Python stdlib or already in `pyproject.toml`.

---

## Architecture Patterns

### Recommended Project Structure

New files this phase creates or modifies:
```
scripts/
├── cli.py                   # Add "disable" to choices list + route
├── init.py                  # Extend: add hook injection + session-data creation
├── generate.py              # Fix: align load_config() to canonical schema
└── tests/
    └── test_init_hooks.py   # New: tests for INIT-01, INIT-03, INIT-05
templates/
├── AGENTS.md.j2             # Update: harness identity text
└── claude/
    └── CLAUDE.md.j2         # Update: harness identity text
reprogate.yaml               # Add: record_triggers section (INIT-04)
.gitignore                   # Add: .claude/session-data/
```

### Pattern 1: JSON Merge-Write for settings.json (INIT-01)

**What:** Read existing `.claude/settings.json` → merge ReproGate hook entries → write back atomically. Never clobber non-ReproGate entries.

**When to use:** `reprogate init` (inject) and `reprogate disable` (remove).

**Key insight:** The existing `settings.json` already has GSD hooks for SessionStart, PostToolUse, PreToolUse, and statusLine. ReproGate must add entries under a clearly namespaced key so that `disable` can surgically remove only ReproGate entries.

**Approach:** Store ReproGate hooks inside the existing `hooks` dict under the standard hook event keys (e.g., `hooks.PreToolUse`, `hooks.Stop`). To enable surgical removal, each ReproGate hook entry must carry an identifying marker — either a `_reprogate: true` field or a comment. Since JSON does not support comments, use a sentinel field: `"_reprogate": true` on each hook entry object.

**The settings.json `hooks` schema (verified from live file):**
```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "optional-matcher",
        "hooks": [
          {
            "type": "command",
            "command": "...",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

Each event key maps to a list of hook group objects. Each hook group has an optional `matcher` and a `hooks` array of command objects. ReproGate must append to (or create) these lists, not replace them.

**Example: inject pattern**
```python
# Source: direct settings.json schema inspection
import json
import pathlib

def inject_reprogate_hooks(settings_path: pathlib.Path, hooks_to_add: dict) -> None:
    data = json.loads(settings_path.read_text(encoding="utf-8")) if settings_path.exists() else {}
    if "hooks" not in data:
        data["hooks"] = {}
    for event, groups in hooks_to_add.items():
        if event not in data["hooks"]:
            data["hooks"][event] = []
        # Only add if not already present (idempotent)
        existing_commands = {
            h["command"]
            for g in data["hooks"][event]
            for h in g.get("hooks", [])
        }
        for group in groups:
            for hook in group.get("hooks", []):
                if hook["command"] not in existing_commands:
                    data["hooks"][event].append(group)
                    break
    settings_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
```

**Example: remove pattern (INIT-03)**
```python
def remove_reprogate_hooks(settings_path: pathlib.Path) -> None:
    if not settings_path.exists():
        return
    data = json.loads(settings_path.read_text(encoding="utf-8"))
    hooks = data.get("hooks", {})
    for event in list(hooks.keys()):
        hooks[event] = [
            g for g in hooks[event]
            if not any(h.get("_reprogate") for h in g.get("hooks", []))
        ]
        if not hooks[event]:
            del hooks[event]
    settings_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
```

### Pattern 2: REPROGATE_DISABLED env var (INIT-02)

**What:** Hook scripts check `REPROGATE_DISABLED` at the top and exit 0 (no-op) if set to `1`.

**When to use:** This is a **design contract** for Phase 2 hook scripts, not standalone code for Phase 1. However, Phase 1 must document the convention so Phase 2 implements it consistently.

**Convention (all ReproGate hook scripts must follow this):**
```python
import os
import sys

def main() -> int:
    if os.environ.get("REPROGATE_DISABLED") == "1":
        sys.exit(0)
    # ... actual hook logic

if __name__ == "__main__":
    sys.exit(main())
```

For Phase 1, the deliverable is: this convention is documented AND the `reprogate init` command injects a hook entry that wraps the env var check. No standalone hook script exists in Phase 1 — that's Phase 2's job.

**Verification approach for INIT-02 in Phase 1:** Write a test that verifies the injected hook command string includes the env var check pattern (or that a wrapper script skeleton is created that does the check).

### Pattern 3: record_triggers Path Matching (INIT-04)

**What:** `gatekeeper.py` reads `record_triggers` from `reprogate.yaml`, gets the list of files changed in the current commit via `git diff`, and only enforces the record-required policy if at least one changed file matches a trigger pattern.

**Schema (from ADR-014):**
```yaml
record_triggers:
  - pattern: "scripts/**"
    record_type: "adr"
    reason: "Core script changes require decision record"
  - pattern: "skills/**"
    record_type: "adr"
    reason: "Skill policy changes require decision record"
```

**Pattern matching:** Use `pathlib.PurePosixPath(filepath).match(pattern)` for Python 3.12+. For Python 3.10/3.11, `pathlib.PurePosixPath.match()` does NOT support `**` — use `fnmatch.fnmatch(filepath, pattern)` instead, which handles `*` within a directory segment but not `**` cross-directory. The safe cross-version approach is:

```python
import fnmatch

def matches_trigger(filepath: str, pattern: str) -> bool:
    # Normalize to forward slashes
    normalized = filepath.replace("\\", "/")
    # fnmatch handles * within segments; for **, split and check prefix
    if "**" in pattern:
        prefix = pattern.split("**")[0].rstrip("/")
        return normalized.startswith(prefix + "/") or normalized == prefix
    return fnmatch.fnmatch(normalized, pattern)
```

**Getting changed files from git:**
```python
import subprocess

def get_changed_files() -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        capture_output=True, text=True, check=False
    )
    if result.returncode != 0:
        return []
    return [f.strip() for f in result.stdout.splitlines() if f.strip()]
```

Note: use `--cached` (staged files) not `HEAD` when running as a pre-commit hook.

### Pattern 4: Schema Alignment (INIT-05) — Critical Fix

**What:** The most structurally important task. Two incompatible schemas exist. This must be resolved.

**Current state (verified by codebase inspection):**

The live `reprogate.yaml` uses the **gatekeeper schema**:
```yaml
project_name: "ReproGate"
reprogate_version: "1.0.0"
records_dir: "records"
record_types: {adr: {...}, rfc: {...}}
skills_dir: "skills"
gatekeeper: {engine: "opa", strict_mode: true, fail_closed: true}
```

`generate.py`'s `load_config()` expects the **generator schema**:
```yaml
project:
  name: "..."
  description: "..."
workspaces:
  primary:
    name: "..."
    branch: "..."
    runtime: "..."
processes:
  enabled: [...]
tools:
  claude:
    enabled: true
    hook_enforcement: true
  codex:
    enabled: true
records:
  wp_path: "..."
  adr_path: "..."
  changelog_path: "..."
```

`gatekeeper.py`'s `load_config()` uses a third partial schema: `records_dir`, `skills_dir`, `active_skills`, `gatekeeper`.

**Resolution approach (canonical merged schema):**

Define one `reprogate.yaml` schema that satisfies all three consumers. The canonical schema must include:
- Fields for `gatekeeper.py`: `records_dir`, `skills_dir`, `active_skills`, `gatekeeper`
- Fields for `generate.py`: `project.name`, `workspaces.primary`, `tools`, `records`
- New Phase 1 fields: `record_triggers`
- Retain: `reprogate_version`

The `generate.py` `context_from_config()` function accesses `config["records"]["wp_path"]`, `config["records"]["adr_path"]`, `config["records"]["changelog_path"]` — these keys conflict with `gatekeeper.py`'s flat `records_dir`. The resolution is: the canonical schema uses **nested `records` for generate.py paths** AND flat `records_dir`/`skills_dir` for gatekeeper.py (both can coexist since they use different key names).

**`init.py` template** (`templates/reprogate.yaml.j2`) must be updated to emit the canonical schema with all required sections populated.

**`generate.py` `load_config()` defaults** must be updated to include the canonical defaults for all sections including `record_triggers: []`.

**`gatekeeper.py` `load_config()`** needs `record_triggers` added to its defaults dict.

### Anti-Patterns to Avoid

- **Clobbering settings.json**: Never overwrite the entire file. Always read-merge-write. The file has GSD hooks that must survive `reprogate init`.
- **Blocking hook invocation at settings.json level**: The `REPROGATE_DISABLED` env var must be checked inside hook scripts, not by removing entries from settings.json. Removing entries is `reprogate disable`'s job.
- **Using `pathlib.match()` with `**` on Python 3.10/3.11**: Returns incorrect results. Use `fnmatch.fnmatch` with a custom `**` handler.
- **Running gatekeeper on HEAD diff instead of staged diff**: Pre-commit hooks evaluate staged changes (`--cached`), not the working tree diff.
- **Making `reprogate init` fail if `reprogate.yaml` doesn't exist**: Per ADR-015, `reprogate.yaml` presence is the "context declared" precondition. `init` should print a clear error if the file is absent.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| JSON file read-merge-write | Custom serializer | `json.loads` + dict merge + `json.dumps(indent=2)` | Stdlib; settings.json is small flat JSON |
| Path pattern matching | Custom glob engine | `fnmatch.fnmatch` (cross-version safe) | stdlib; handles all cases in ADR-014 patterns |
| YAML loading | Custom YAML parser | `yaml.safe_load` (PyYAML, already in deps) | Already a dependency; handles all edge cases |
| Git staged file list | Custom git parsing | `subprocess.run(["git", "diff", "--cached", "--name-only"])` | 3-line subprocess call; no custom parsing needed |

**Key insight:** Every operation in this phase is a simple file read/modify/write or subprocess call. No new libraries are needed. The complexity is in the schema design and idempotency, not the tooling.

---

## Common Pitfalls

### Pitfall 1: settings.json Idempotency
**What goes wrong:** Running `reprogate init` twice injects duplicate hook entries.
**Why it happens:** Naive append-to-list without checking for existing entries.
**How to avoid:** Before appending a hook group, check if a hook with the same `command` value already exists in the event's group list. If found, skip. Use set of command strings as existence check.
**Warning signs:** Running `reprogate init; reprogate init` and seeing the hooks array double in length.

### Pitfall 2: schema misalignment causing silent generate.py failures
**What goes wrong:** `generate.py` runs without error but produces template output with empty/default values because `reprogate.yaml` doesn't have the fields it reads.
**Why it happens:** `load_config()` in `generate.py` merges with defaults silently — no KeyError, just wrong output.
**How to avoid:** After fixing INIT-05, add a validation step in `generate.py` that warns if required fields are missing (not just defaulted).
**Warning signs:** Generated `AGENTS.md` or `CLAUDE.md` shows placeholder text like "Fill in the primary runtime" even after config is set.

### Pitfall 3: record_triggers with `**` on Python 3.10
**What goes wrong:** `pathlib.PurePosixPath("scripts/foo.py").match("scripts/**")` returns `False` on Python 3.10/3.11 because `**` in `match()` was fixed only in Python 3.12.
**Why it happens:** Python 3.10/3.11 `pathlib.match()` treats `**` as a literal path segment, not a wildcard.
**How to avoid:** Use `fnmatch.fnmatch` with a simple `**` expansion: if pattern ends with `/**`, check if filepath starts with the prefix. The codebase requires Python 3.10+, so must handle this.
**Warning signs:** Tests on Python 3.12 pass but CI (3.10) fails for path-pattern matching.

### Pitfall 4: reprogate disable removes too much
**What goes wrong:** `reprogate disable` removes GSD hooks that were not installed by ReproGate.
**Why it happens:** Using a broad removal strategy (e.g., removing entire events) instead of targeting only ReproGate-owned entries.
**How to avoid:** Tag all ReproGate-injected hook entries with `"_reprogate": true`. Removal only removes entries bearing this tag. GSD hooks lack this tag and are left untouched.
**Warning signs:** After `reprogate disable`, the GSD statusLine or gsd-check-update hook disappears.

### Pitfall 5: `init.py` schema template not updated
**What goes wrong:** `init.py` generates a `reprogate.yaml` with the old gatekeeper-only schema after INIT-05 is meant to fix this.
**Why it happens:** `init.py` renders `templates/reprogate.yaml.j2` — if the template file is not updated, the schema stays broken.
**How to avoid:** INIT-05 must update BOTH `templates/reprogate.yaml.j2` (the template `init.py` uses) AND `generate.py`'s `load_config()` defaults. Both must agree.

### Pitfall 6: .gitignore not updated for session-data
**What goes wrong:** `.claude/session-data/*.json` files get committed to the repo accidentally.
**Why it happens:** The directory is created by `reprogate init` but the `.gitignore` is not updated.
**How to avoid:** `reprogate init` must also check/add `.claude/session-data/` to `.gitignore` (or the task list must include this separately). Per ADR-011, session runtime data must not be committed.

---

## Code Examples

Verified patterns from direct codebase inspection:

### CLI subcommand routing (existing pattern in cli.py)
```python
# Source: scripts/cli.py (existing pattern — follow this exactly)
def main(argv: List[str] | None = None) -> int:
    args = parse_args(argv)
    extra = list(args.extra)
    if extra and extra[0] == "--":
        extra = extra[1:]
    if args.command == "disable":
        return run_script("disable.py", extra)
    # ... existing routes
```

When adding `disable` subcommand:
1. Add `"disable"` to the `choices` list in `parse_args()`
2. Add routing in `main()` pointing to a new `scripts/disable.py`
3. Keep `init.py` for init logic; consider refactoring hook injection into `init.py` vs a separate module

### init.py extension pattern (existing pattern)
```python
# Source: scripts/init.py (existing pattern)
def main(argv: List[str] | None = None) -> int:
    args = parse_args(argv)
    output_path = pathlib.Path(args.output)
    # ... existing logic for reprogate.yaml creation

    # New: inject hooks into .claude/settings.json
    settings_path = ROOT / ".claude" / "settings.json"
    inject_reprogate_hooks(settings_path, REPROGATE_HOOKS)

    # New: create .claude/session-data/ directory
    session_data_dir = ROOT / ".claude" / "session-data"
    session_data_dir.mkdir(parents=True, exist_ok=True)
    print(f"Created {session_data_dir.relative_to(ROOT)}")
    return 0
```

### gatekeeper.py record_triggers integration
```python
# New function to add to gatekeeper.py
def is_record_required(config: Dict[str, Any]) -> bool:
    """Check if current commit touches any record-trigger paths."""
    triggers = config.get("record_triggers", [])
    if not triggers:
        return False  # No triggers defined = no record required

    changed = get_changed_files()  # git diff --cached --name-only
    for filepath in changed:
        for trigger in triggers:
            if matches_trigger(filepath, trigger["pattern"]):
                return True
    return False
```

---

## Runtime State Inventory

This is a new feature phase, not a rename/refactor. No runtime state inventory required.

The only existing runtime state relevant to this phase:
- `.claude/settings.json` — already exists with GSD hooks; `reprogate init` must preserve them
- `.gitignore` — does not yet have `.claude/session-data/` entry; must be added
- `reprogate.yaml` — exists with gatekeeper-schema only; INIT-05 updates the template but the live file needs migration or `init --force`

---

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Python 3.10+ | All scripts | ✓ | 3.13.3 (CPython) | — |
| PyYAML | `generate.py`, `gatekeeper.py` | ✓ | >=6.0 (in pyproject.toml) | — |
| uv | Test runner | ✓ | present | `python3 -m pytest` directly |
| pytest | Test suite | ✓ | >=9.0.2 (in dev deps) | — |
| git | `get_changed_files()` in gatekeeper | ✓ | git repo confirmed | Return [] if not available |
| `.claude/session-data/` | INIT-01 | ✗ | does not exist | Created by `reprogate init` |
| `.gitignore` session-data entry | ADR-011 | ✗ | missing | Must be added |

**Missing dependencies with no fallback:**
- None that block execution.

**Missing dependencies with fallback:**
- `.claude/session-data/` — created by this phase's implementation.
- `.gitignore` session-data entry — added by this phase's implementation.

Note: PyPI access was unavailable during research (SSL certificate error). However, all dependencies are already specified in `pyproject.toml` and present in the existing project — no new packages are needed.

---

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest >=9.0.2 |
| Config file | none (discovered via `scripts/tests/` directory) |
| Quick run command | `uv run python3 -m pytest scripts/tests/ -x -q` |
| Full suite command | `uv run python3 -m pytest scripts/tests/` |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| INIT-01 | `reprogate init` injects hook config into `.claude/settings.json` | unit | `uv run python3 -m pytest scripts/tests/test_init_hooks.py::test_init_injects_hooks -x` | ❌ Wave 0 |
| INIT-01 | `reprogate init` creates `.claude/session-data/` directory | unit | `uv run python3 -m pytest scripts/tests/test_init_hooks.py::test_init_creates_session_data -x` | ❌ Wave 0 |
| INIT-01 | `reprogate init` is idempotent (double-run safe) | unit | `uv run python3 -m pytest scripts/tests/test_init_hooks.py::test_init_idempotent -x` | ❌ Wave 0 |
| INIT-02 | `REPROGATE_DISABLED=1` makes hooks no-op | unit | `uv run python3 -m pytest scripts/tests/test_init_hooks.py::test_disabled_env_var -x` | ❌ Wave 0 |
| INIT-03 | `reprogate disable` removes hook config | unit | `uv run python3 -m pytest scripts/tests/test_init_hooks.py::test_disable_removes_reprogate_hooks -x` | ❌ Wave 0 |
| INIT-03 | `reprogate disable` preserves non-ReproGate hooks | unit | `uv run python3 -m pytest scripts/tests/test_init_hooks.py::test_disable_preserves_gsd_hooks -x` | ❌ Wave 0 |
| INIT-04 | `record_triggers` pattern matches trigger required paths | unit | `uv run python3 -m pytest scripts/tests/test_record_triggers.py::test_trigger_pattern_match -x` | ❌ Wave 0 |
| INIT-04 | `record_triggers` does not trigger for exempt paths | unit | `uv run python3 -m pytest scripts/tests/test_record_triggers.py::test_no_trigger_exempt_paths -x` | ❌ Wave 0 |
| INIT-05 | `generate.py` schema includes all canonical fields | unit | `uv run python3 -m pytest scripts/tests/test_schema_alignment.py::test_canonical_schema -x` | ❌ Wave 0 |
| INIT-05 | `init.py` template produces canonical schema fields | unit | `uv run python3 -m pytest scripts/tests/test_schema_alignment.py::test_init_template_fields -x` | ❌ Wave 0 |
| INIT-06 | `AGENTS.md.j2` does not contain "compiler/gatekeeper" | unit | `uv run python3 -m pytest scripts/tests/test_template_identity.py::test_agents_md_identity -x` | ❌ Wave 0 |
| INIT-06 | `CLAUDE.md.j2` does not contain "compiler/gatekeeper" | unit | `uv run python3 -m pytest scripts/tests/test_template_identity.py::test_claude_md_identity -x` | ❌ Wave 0 |

### Sampling Rate
- **Per task commit:** `uv run python3 -m pytest scripts/tests/ -x -q`
- **Per wave merge:** `uv run python3 -m pytest scripts/tests/`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `scripts/tests/test_init_hooks.py` — covers INIT-01, INIT-02, INIT-03
- [ ] `scripts/tests/test_record_triggers.py` — covers INIT-04
- [ ] `scripts/tests/test_schema_alignment.py` — covers INIT-05
- [ ] `scripts/tests/test_template_identity.py` — covers INIT-06

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| `compiler/gatekeeper` identity in templates | `delivery harness` identity | ADR-009 (2026-04-02) | Templates must be updated (INIT-06) |
| Implicit hook activation (ECC global settings) | Explicit `reprogate init` + repo-local settings.json | ADR-013 (2026-04-02) | Developer must run `reprogate init` after clone |
| Flat gatekeeper-only `reprogate.yaml` schema | Canonical unified schema | INIT-05 (this phase) | All scripts read from one schema |
| No path-based record requirement scoping | `record_triggers` in `reprogate.yaml` | ADR-014 (2026-04-02) | Gatekeeper now scopes enforcement to specific paths |

---

## Open Questions

1. **`REPROGATE_DISABLED` in Phase 1 scope**
   - What we know: INIT-02 is listed as Phase 1 requirement; hook scripts don't exist yet (Phase 2)
   - What's unclear: What exactly does Phase 1 deliver for INIT-02? A test that checks the env var convention? A wrapper script skeleton?
   - Recommendation: Deliver the env var check as a convention documented in `reprogate init`'s output — specifically, `reprogate init` should create a `scripts/hooks/reprogate_hook_base.py` helper that every Phase 2 hook will import. The helper's `check_disabled()` function provides the standard early-exit. This makes INIT-02 testable in Phase 1 without needing full hook scripts.

2. **Canonical `reprogate.yaml` migration for the live file**
   - What we know: The live `reprogate.yaml` uses gatekeeper schema; INIT-05 updates the template
   - What's unclear: Should `reprogate init` (with `--force`) migrate the live `reprogate.yaml`? Or is the live file left as-is until the developer runs `reprogate generate`?
   - Recommendation: `reprogate init` should update the live `reprogate.yaml` with the canonical schema if it exists but is missing sections — a non-destructive merge. If it doesn't exist, create from template. Use `--force` to overwrite entirely.

3. **`record_triggers` default injection timing**
   - What we know: ADR-015 says `reprogate init` injects `record_triggers` defaults into `reprogate.yaml`
   - What's unclear: Should `record_triggers` defaults be in the template (`reprogate.yaml.j2`) or injected dynamically by `init.py`?
   - Recommendation: Put defaults in `reprogate.yaml.j2` template so they're always present in freshly initialized repos. `init.py` can still inject them if the key is missing from an existing file.

---

## Sources

### Primary (HIGH confidence)
- Direct codebase inspection: `scripts/cli.py`, `scripts/init.py`, `scripts/generate.py`, `scripts/gatekeeper.py`
- Direct codebase inspection: `.claude/settings.json` (live hook configuration)
- Direct codebase inspection: `reprogate.yaml` (live config schema)
- ADR-011 (2026-04-02): Session state path decision
- ADR-013 (2026-04-02): Hook delivery mechanism
- ADR-014 (2026-04-02): Record trigger scope
- ADR-015 (2026-04-02): Harness activation model
- `.planning/research/HARNESS-ARCHITECTURE.md` (2026-04-02)
- `pyproject.toml`: confirmed Python 3.10+ requirement, pytest dep, no new deps needed

### Secondary (MEDIUM confidence)
- Python 3.10 `pathlib.match()` `**` limitation: documented in Python changelog (fixed in 3.12); verified via training knowledge that 3.10 `fnmatch`-based approach is needed

### Tertiary (LOW confidence)
- None

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — all stdlib + existing deps; no new packages
- Architecture: HIGH — based on direct codebase reading and ADR decisions
- Pitfalls: HIGH — identified from actual schema mismatches in live code
- Schema alignment (INIT-05): HIGH — verified by reading both `init.py` template and `generate.py` `load_config()` defaults

**Research date:** 2026-04-02
**Valid until:** 2026-05-02 (stable codebase, no fast-moving external deps)
