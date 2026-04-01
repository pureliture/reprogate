# Phase 2: Claude Code Workflow Integration - Research

**Researched:** 2026-04-01
**Domain:** Python CLI extension, Claude Code custom commands, artifact-driven workflow coordination
**Confidence:** HIGH

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01:** Claude Code is the sole target harness for this phase. Adapter commands live under `.claude/commands/` and are generated via `scripts/generate.py` to keep the generation surface consistent with Phase 1 patterns.
- **D-02:** Core workflow logic (lifecycle coordination, artifact reads/writes, status derivation) lives in `scripts/` — not inside `.claude/`. This is what makes future harness adoption possible without rewriting the core.
- **D-03:** ECC's per-harness directory pattern (`.claude/`, `.codex/`, `.cursor/`) is the reference model. Phase 2 builds `.claude/` adapter commands; later phases add `.codex/` etc. as thin adapters over the same core.
- **D-04:** Entry points: `reprogate workflow start` (CLI) and `.claude/commands/workflow-*.md` (Claude Code). Both converge on the same artifact contract: `STATE.md`, `ROADMAP.md`, and per-phase `CONTEXT.md` / `PLAN.md` / `SUMMARY.md` / `VERIFICATION.md`.
- **D-05:** The minimum automated chain is research → strategy → execution tracking, with each stage leaving an inspectable artifact so any subsequent session or adapter can resume.
- **D-06:** Status is derivable from on-disk artifacts alone. Helper state files accelerate routing but are never the sole authority.
- **D-07:** Status views emphasize missing evidence and next candidate actions derived from repo artifacts — not opaque step counters.
- **D-08:** Automation ends at preparing, routing, and verifying governed work. ReproGate does not become a direct execution engine or heavy stateful orchestrator.
- **D-09:** Claude Code command UX (command names, display text, progress hints) is adapter-side concern. Core artifact schema remains harness-neutral so future adapters can reuse it.
- **D-10:** Phase 3 HUD reads from artifacts (gate status, record compliance, skill results) — not from Claude Code session state.

### Claude's Discretion
- Exact command names and file naming details for workflow helper artifacts, as long as they remain durable and reconstructible from repo state.
- Whether status derivation uses directory scans, frontmatter indexes, or lightweight manifests.
- Amount of Claude Code command UX polish, as long as the shared artifact contract stays stable.

### Deferred Ideas (OUT OF SCOPE)
- Harness-agnostic extension layer (Codex, Cursor, Gemini adapters) — planted as a seed, surfaces when a second harness is added.
- External storage synchronization policy — later RFC-driven design work.
- HUD visualization — Phase 3 scope.
- Deep multi-agent runtime orchestration — beyond this milestone.
</user_constraints>

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| AUTO-01 | Automate the basic research -> strategy -> execution lifecycle within the framework using Claude Code as the primary harness. | scripts/workflow.py design, Claude Code command format, artifact contract definition |
| AUTO-02 | Support plan generation and execution tracking through durable artifacts and Claude Code adapter commands. | generate.py extension pattern, `.claude/commands/workflow-*.md` generation, STATE.md/ROADMAP.md artifact schema |
</phase_requirements>

---

## Summary

Phase 2 extends ReproGate's existing Python CLI and generator to automate the research → strategy → execution lifecycle. The implementation has three parts: (1) a new `scripts/workflow.py` module that coordinates artifact creation and status derivation; (2) extensions to `scripts/cli.py` adding a `workflow` subcommand; and (3) extensions to `scripts/generate.py` that render `.claude/commands/workflow-*.md` template files during the standard generate step.

The Claude Code command format is already established in this repository: a Markdown file with a YAML frontmatter block (`---name, description, argument-hint, allowed-tools---`) followed by objective, context, and process sections. The existing `.claude/commands/gsd/execute-phase.md` demonstrates the exact pattern. New `workflow-*.md` commands delegate to `scripts/workflow.py` via `Bash` tool calls, keeping all logic in `scripts/`.

Artifact authority is clear: `.planning/STATE.md` and `.planning/ROADMAP.md` are the durable operational context; per-phase directories (`.planning/phases/XX-name/`) hold `CONTEXT.md`, `PLAN.md`, `SUMMARY.md`, `VERIFICATION.md`. Status derivation scans these files for presence and YAML frontmatter fields — no additional state files are needed.

**Primary recommendation:** Implement `scripts/workflow.py` as the artifact coordinator, extend `cli.py` with `workflow` subcommand routing, add `templates/claude/commands/workflow-*.md.j2` templates, and extend `generate.py` to render them. This follows the Phase 1 pattern exactly.

---

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python stdlib: `pathlib`, `argparse`, `re`, `json` | 3.10+ (built-in) | Artifact scanning, CLI dispatch, frontmatter parsing | Already used throughout `scripts/`; no new dependency |
| PyYAML | >=6.0 (pinned in pyproject.toml) | YAML frontmatter parsing in artifacts | Already a dependency; `generate.py` and `gatekeeper.py` use it |
| pytest | >=9.0.2 (dev dependency) | Test framework for `scripts/tests/` | Already in use; all Phase 1 tests use it |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| `subprocess` | stdlib | CLI integration tests that invoke `workflow.py` via `scripts/cli.py` | Integration tests only (per existing `test_integration.py` pattern) |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| PyYAML for frontmatter | `python-frontmatter` library | `python-frontmatter` is cleaner but adds a dependency; existing code uses manual regex + PyYAML which is sufficient for the simple schema used here |
| Directory scan for status | SQLite index | SQLite would be faster at scale but adds complexity and state; on-disk scan matches D-06's "artifacts as sole authority" principle |

**Version verification (confirmed 2026-04-01):**
- PyYAML pinned at `>=6.0` in `pyproject.toml` — current published 6.0.2.
- pytest pinned at `>=9.0.2` — current published 8.x. Note: constraint reads `>=9.0.2` in `pyproject.toml` but latest stable is 8.3.x. This is an existing project state; no change needed for Phase 2.
- Python: `>=3.10` confirmed in `pyproject.toml`.

**Installation:** No new packages needed. All dependencies are already in `pyproject.toml`.

---

## Architecture Patterns

### Recommended Project Structure Additions
```
scripts/
├── workflow.py              # New: lifecycle coordinator (research/strategy/execution artifacts)
├── tests/
│   └── test_workflow.py     # New: unit + integration tests for workflow.py

templates/
└── claude/
    └── commands/
        ├── workflow-start.md.j2     # New: rendered to .claude/commands/workflow-start.md
        ├── workflow-status.md.j2    # New: rendered to .claude/commands/workflow-status.md
        └── workflow-gate.md.j2      # New: rendered to .claude/commands/workflow-gate.md

.claude/
└── commands/
    ├── workflow-start.md    # Generated output
    ├── workflow-status.md   # Generated output
    └── workflow-gate.md     # Generated output
```

### Pattern 1: scripts/workflow.py Lifecycle Coordinator

**What:** A Python module that reads `.planning/` artifacts, determines current workflow position, scaffolds missing artifacts, and returns structured status. The module exposes sub-commands consumed by `cli.py`.

**When to use:** Any time the CLI needs to read or write workflow lifecycle state.

**Design:**
```python
#!/usr/bin/env python3
"""ReproGate workflow lifecycle coordinator."""
import argparse
import pathlib
import sys
from typing import Any, Dict, List

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
PLANNING_DIR = ROOT / ".planning"

def derive_status(planning_dir: pathlib.Path) -> Dict[str, Any]:
    """Scan on-disk artifacts to derive workflow status.

    Returns dict with: current_phase, completed_phases, missing_artifacts,
    next_actions. Never relies on a live session or non-artifact state.
    """
    ...

def scaffold_phase_artifacts(phase_dir: pathlib.Path, phase_name: str) -> List[pathlib.Path]:
    """Create missing artifact stubs (CONTEXT.md, PLAN.md placeholders).

    Returns list of paths created. Idempotent: skips existing files.
    """
    ...

def parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="ReproGate workflow coordinator.")
    sub = parser.add_subparsers(dest="subcommand", required=True)
    sub.add_parser("start", help="Scaffold artifacts for current phase and emit status.")
    sub.add_parser("status", help="Print missing evidence and next candidate actions.")
    sub.add_parser("gate", help="Run gatekeeper against current phase artifacts and exit 0/1.")
    return parser.parse_args(argv)

def main(argv: List[str] | None = None) -> int:
    args = parse_args(argv)
    if args.subcommand == "start":
        return cmd_start()
    if args.subcommand == "status":
        return cmd_status()
    if args.subcommand == "gate":
        return cmd_gate()
    return 1
```

**Key principle:** Every public function takes explicit paths rather than module-level constants, enabling `monkeypatch`-based test isolation (per existing Phase 1 pattern in `test_gatekeeper.py`).

### Pattern 2: Claude Code Command Format

**What:** A Markdown file in `.claude/commands/` (or a subdirectory thereof) with YAML frontmatter and structured sections. Claude Code parses the frontmatter to register the command; the body is the system prompt.

**Confirmed format** (observed in `.claude/commands/gsd/execute-phase.md`):
```markdown
---
name: reprogate:workflow-start
description: Scaffold workflow artifacts and start the research->strategy->execution chain
argument-hint: "[phase-number]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---
<objective>
[purpose statement]
</objective>

<context>
Phase: $ARGUMENTS
</context>

<process>
[step-by-step instructions that delegate to scripts/workflow.py]
</process>
```

**Key insight:** The command body is a Claude system prompt, not a shell script. All executable logic belongs in `scripts/workflow.py`. The command instructs Claude to call `Bash` with `uv run python3 scripts/workflow.py <subcommand>`.

**Slash command invocation:** In Claude Code, the user types `/reprogate:workflow-start` or `/workflow-start` (depending on registered name). The `$ARGUMENTS` token receives anything typed after the command name.

### Pattern 3: generate.py Extension for Claude Commands

**What:** Add new `(output_path, template_path)` tuples to the `rendered_outputs` list inside `render_outputs()` in `generate.py`.

**Established pattern** (from existing `generate.py` lines 194-209):
```python
if bool(config["tools"].get("claude", {}).get("enabled", True)):
    rendered_outputs.extend([
        (output_root / ".claude" / "CLAUDE.md", TEMPLATES_DIR / "claude" / "CLAUDE.md.j2"),
        (output_root / ".claude" / "commands" / "dpc.md", TEMPLATES_DIR / "claude" / "commands" / "dpc.md.j2"),
        # Phase 2 additions:
        (output_root / ".claude" / "commands" / "workflow-start.md", TEMPLATES_DIR / "claude" / "commands" / "workflow-start.md.j2"),
        (output_root / ".claude" / "commands" / "workflow-status.md", TEMPLATES_DIR / "claude" / "commands" / "workflow-status.md.j2"),
        (output_root / ".claude" / "commands" / "workflow-gate.md", TEMPLATES_DIR / "claude" / "commands" / "workflow-gate.md.j2"),
    ])
```

Templates use `{{ variable }}` simple string replacement (not Jinja2 — confirmed in `generate.py` `render_template()` which does literal `{{ key }}` substitution). Context variables available are those returned by `context_from_config()`.

### Pattern 4: cli.py Extension for workflow Subcommand

**What:** Add `workflow` to the `choices` list in `parse_args()` and add a routing branch in `main()`.

**Established pattern** (from `cli.py`):
```python
# In parse_args():
"command",
choices=["init", "generate", "check", "gate", "create", "search", "search-content", "print", "workflow"],

# In main():
if args.command == "workflow":
    return run_script("workflow.py", extra)
```

The `workflow` command forwards all remaining args (`extra`) to `workflow.py`, which handles its own `start | status | gate` sub-dispatch.

### Pattern 5: Artifact Contract Schema

**What:** The on-disk layout that both the CLI and Claude Code commands read/write. Defines what "status derivable from artifacts alone" means in practice.

**Artifact locations and authority:**

| Artifact | Location | Authority | Inspected Fields |
|----------|----------|-----------|-----------------|
| ROADMAP.md | `.planning/ROADMAP.md` | Phase list and success criteria | Phase names, `Plans:` section |
| STATE.md | `.planning/STATE.md` | Current position (operational context only, per D-06) | YAML frontmatter: `milestone`, `status`, progress block |
| Phase CONTEXT.md | `.planning/phases/XX-name/XX-CONTEXT.md` | Design decisions locked for this phase | Presence = phase discussed |
| Phase PLAN.md | `.planning/phases/XX-name/XX-NN-PLAN.md` | Execution intent | Presence = plan exists |
| Phase SUMMARY.md | `.planning/phases/XX-name/XX-NN-SUMMARY.md` | Completion evidence | Presence = plan executed |
| Phase VERIFICATION.md | `.planning/phases/XX-name/XX-VERIFICATION.md` | Gate evidence | Presence = phase verified |

**Status derivation algorithm** (per D-06, D-07):
1. Scan `.planning/phases/` for phase directories matching pattern `NN-*`.
2. For each phase, check which of the four artifact types exist.
3. Report missing artifacts as "missing evidence" — not as a step counter.
4. The "next candidate action" is the first phase with a gap in the required artifact chain.

### Anti-Patterns to Avoid
- **Storing workflow state outside `.planning/`:** All lifecycle state must be readable from committed Markdown files, not from hidden files, sockets, or in-process caches (D-06).
- **Workflow logic inside `.claude/commands/`:** Claude command files must delegate to `scripts/workflow.py`. Logic in command files can't be tested or reused by other harnesses (D-02).
- **Using gatekeeper for workflow routing:** `gatekeeper.py` is the terminal gate, not a navigation oracle. `workflow.py` handles routing; `gatekeeper.py` handles enforcement.
- **Making `workflow status` print a progress bar:** Output must show missing evidence and next actions, not opaque "Step 2 of 5" counters (D-07).
- **Calling `reprogate check` from inside `workflow start`:** The workflow coordinator prepares artifacts; the gatekeeper is a separate terminal check invoked explicitly (D-08).

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| YAML frontmatter parsing | Custom regex parser | PyYAML (already in use) | `gatekeeper.py` already has a robust regex+PyYAML approach for this exact schema |
| Template variable substitution | Jinja2 or string.Template | Existing `render_template()` in `generate.py` | Already in use and sufficient for `{{ variable }}` simple replacement |
| Test isolation for PATH-dependent scripts | subprocess with env override | `monkeypatch` on module constants | Established in Phase 1 `test_gatekeeper.py`; avoids subprocess spawn overhead |
| Recursive directory scanning | `os.walk` | `pathlib.Path.rglob("*.md")` | Consistent with existing `gatekeeper.py` and `generate.py` patterns |
| CLI argument parsing | Manual `sys.argv` slicing | `argparse` | Already used in every `scripts/*.py` file |

**Key insight:** The implementation should contain almost no net-new patterns. Every primitive needed for Phase 2 is already demonstrated in the codebase.

---

## Common Pitfalls

### Pitfall 1: Placing Logic in Command Templates Instead of workflow.py
**What goes wrong:** Claude command files grow into prompt-heavy scripts. They can't be unit-tested and block future harness adoption.
**Why it happens:** It feels faster to write instructions directly in the command file.
**How to avoid:** Command files contain only: objective, context reference, and a single `Bash` call to `uv run python3 scripts/workflow.py <subcommand>`. All logic lives in the Python module.
**Warning signs:** A command file exceeds 40 lines of `<process>` content or contains conditional logic.

### Pitfall 2: generate.py `--force` Required for Workflow Commands After First Run
**What goes wrong:** On re-running `reprogate generate`, the workflow command files already exist and generate.py exits with `FileExistsError` without `--force`.
**Why it happens:** `write_file()` in `generate.py` raises `FileExistsError` if the output path exists and `force=False` (line 132-133).
**How to avoid:** Document this in command UX. Tests that verify regeneration must pass `--force`. Consider whether idempotent generation (only update if template changes) is worth the complexity — for Phase 2, using `--force` is simpler.
**Warning signs:** CI fails with "Refusing to overwrite without --force" after adding workflow templates.

### Pitfall 3: STATUS.md or Helper State File Becoming the Sole Truth
**What goes wrong:** `workflow status` caches results to a `STATUS.json` helper file, and future code reads only that file instead of scanning artifacts.
**Why it happens:** Caching feels like an optimization.
**How to avoid:** Any helper state file must be derived from artifact scans, not authoritative itself (D-06). If a helper file is used, it must have a staleness check or be regenerated on every read. Simpler: just don't cache.
**Warning signs:** Code that reads `STATUS.json` without first verifying the file was just generated from a fresh scan.

### Pitfall 4: cli.py choices List Drift
**What goes wrong:** Adding `workflow` to `cli.py` but forgetting to update the `choices=` list in `parse_args()` causes `argparse` to reject the command with a cryptic error.
**Why it happens:** The `choices=` list and the `if args.command ==` branches are separate code locations.
**How to avoid:** Add both in the same commit. The test `test_all_commands_accepted` in `test_cli.py` catches this if it is updated to include `"workflow"`.
**Warning signs:** `reprogate workflow` returns "argument command: invalid choice: 'workflow'".

### Pitfall 5: Template Rendering With Unresolved Variables
**What goes wrong:** A `{{ variable }}` placeholder in a new `.j2` template is not present in `context_from_config()`, so the rendered output contains literal `{{ variable }}` text instead of a value.
**Why it happens:** Adding a new template variable without extending `context_from_config()`.
**How to avoid:** Keep workflow command templates free of project-specific variables where possible. If a template variable is needed (e.g., `{{ project_name }}`), verify it exists in the dict returned by `context_from_config()` before shipping. The existing set includes: `project_name`, `today`, `wp_path`, `adr_path`, `changelog_path`, etc.
**Warning signs:** A rendered `.claude/commands/workflow-*.md` file contains `{{ ` in its body.

---

## Code Examples

Verified patterns from the existing codebase:

### Existing Command File Format (.claude/commands/gsd/execute-phase.md)
```markdown
---
name: gsd:execute-phase
description: Execute all plans in a phase with wave-based parallelization
argument-hint: "<phase-number> [--wave N] [--gaps-only] [--interactive]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - Task
  - TodoWrite
  - AskUserQuestion
---
<objective>
[purpose]
</objective>

<execution_context>
@/path/to/workflow.md
</execution_context>

<context>
Phase: $ARGUMENTS
...
</context>

<process>
Execute the workflow from @path end-to-end.
</process>
```
Source: `.claude/commands/gsd/execute-phase.md` (confirmed in repo).

### Existing generate.py Template Registration Pattern
```python
# In render_outputs(), within the claude-enabled block:
rendered_outputs.extend([
    (output_root / ".claude" / "commands" / "dpc.md",
     TEMPLATES_DIR / "claude" / "commands" / "dpc.md.j2"),
])
```
Source: `scripts/generate.py` lines 198-199 (confirmed).

### Existing cli.py Routing Pattern
```python
# parse_args(): choices=["init", "generate", "check", ...]
# main():
if args.command == "init":
    return run_script("init.py", extra)
```
Source: `scripts/cli.py` lines 26-53 (confirmed).

### Existing Frontmatter-Based Status Derivation (gatekeeper.py)
```python
def parse_frontmatter(path: pathlib.Path) -> Dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return {}
    # ... parse key: value lines
    return frontmatter
```
Source: `scripts/gatekeeper.py` lines 69-89 (confirmed). This pattern can be imported or copied into `workflow.py`.

### Existing Test Isolation Pattern (test_gatekeeper.py)
```python
def test_valid_records_pass(monkeypatch, tmp_path):
    monkeypatch.setattr(gatekeeper, "RECORDS_DIR", records_dir)
    monkeypatch.setattr(gatekeeper, "SKILLS_DIR", skills_dir)
    exit_code, messages = gatekeeper.evaluate_gate(config=config)
    assert exit_code == 0
```
Source: `scripts/tests/test_gatekeeper.py` (confirmed pattern). Use the same approach for `workflow.py` tests.

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| `dpc` CLI naming | `reprogate` CLI (via `pyproject.toml` console-script) | Phase 1 | Command templates must reference `reprogate workflow`, not `dpc workflow` |
| Jinja2-style templates (referenced in docs) | Simple `{{ key }}` string replacement in `render_template()` | Phase 1 implementation | No Jinja2 dependency; keep templates simple |
| `tools.claude.enabled` key in config | Same key, but loaded with defaults fallback | Phase 1 | `config["tools"]["claude"]` is always present due to `load_config()` defaults |

**Deprecated/outdated in this context:**
- References to `dpc` CLI surface in older docs: these are legacy naming; `reprogate` is canonical.
- GSD's `gsd-tools.cjs` pattern: powerful reference but not used directly in ReproGate core. ReproGate uses Python scripts.

---

## Open Questions

1. **Should workflow-start also trigger `reprogate check` automatically, or only on demand?**
   - What we know: D-08 says automation ends at "preparing, routing, and verifying governed work" — the gate is a check, not an automatic block mid-workflow-start.
   - What's unclear: Whether `workflow start` should call gatekeeper as a pre-condition check (to surface blockers early) or leave that to `workflow gate` explicitly.
   - Recommendation: Keep them separate. `workflow start` scaffolds artifacts; `workflow gate` runs the gatekeeper. This respects D-08 and makes the two operations independently testable.

2. **Should phase artifact directories be created by `workflow start` or be pre-existing?**
   - What we know: Phase 1 evidence shows `.planning/phases/` directories are manually created as part of the planning workflow.
   - What's unclear: Whether `workflow start` should create the directory structure if absent.
   - Recommendation: `workflow start` creates the phase directory and stubs missing artifact files (with minimal frontmatter placeholders), but never overwrites existing content. This makes the command safe to call multiple times.

3. **Exact set of workflow command files needed for AUTO-01 and AUTO-02?**
   - What we know: The minimum chain is research → strategy → execution tracking (D-05).
   - Recommendation: Three commands cover this: `workflow-start` (scaffolds artifacts, emits status), `workflow-status` (reads artifacts, reports missing evidence), `workflow-gate` (delegates to gatekeeper). A fourth `workflow-next` can be discretionary (routes to the next required action). Keep to three for the minimum viable delivery.

---

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Python 3.10+ | All scripts | ✓ | Darwin 24.6.0 (via uv) | — |
| uv | Dependency management, test runner | ✓ | Present (uv.lock confirmed) | `pip install -e .` |
| pytest | Test suite | ✓ | >=9.0.2 (dev dep) | — |
| PyYAML | Frontmatter parsing | ✓ | >=6.0 (pinned) | — |

**Missing dependencies with no fallback:** None.

**Missing dependencies with fallback:** None.

---

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest >=9.0.2 |
| Config file | None — pytest auto-discovers `scripts/tests/` |
| Quick run command | `uv run python3 -m pytest scripts/tests/test_workflow.py -x -q` |
| Full suite command | `uv run python3 -m pytest scripts/tests/ -q` |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| AUTO-01 | `workflow start` scaffolds research/strategy/execution artifacts | unit | `uv run python3 -m pytest scripts/tests/test_workflow.py::test_start_scaffolds_artifacts -x` | ❌ Wave 0 |
| AUTO-01 | `workflow status` reports missing evidence from artifact scan | unit | `uv run python3 -m pytest scripts/tests/test_workflow.py::test_status_reports_missing -x` | ❌ Wave 0 |
| AUTO-01 | Full chain: `reprogate workflow start` → artifacts present → `reprogate workflow gate` exits 0 | integration | `uv run python3 -m pytest scripts/tests/test_workflow.py::test_full_workflow_chain -x` | ❌ Wave 0 |
| AUTO-02 | `reprogate generate` produces `.claude/commands/workflow-*.md` files | unit | `uv run python3 -m pytest scripts/tests/test_generate_workflow.py::test_generate_produces_workflow_commands -x` | ❌ Wave 0 |
| AUTO-02 | Generated commands reference `scripts/workflow.py` not inline logic | unit | `uv run python3 -m pytest scripts/tests/test_generate_workflow.py::test_commands_delegate_to_workflow_py -x` | ❌ Wave 0 |
| AUTO-02 | `reprogate workflow` is accepted by CLI argument parser | unit | `uv run python3 -m pytest scripts/tests/test_cli.py::test_workflow_command_accepted -x` | ❌ Wave 0 (extend existing) |

### Sampling Rate
- **Per task commit:** `uv run python3 -m pytest scripts/tests/test_workflow.py -x -q`
- **Per wave merge:** `uv run python3 -m pytest scripts/tests/ -q`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `scripts/tests/test_workflow.py` — covers AUTO-01 unit and integration tests
- [ ] `scripts/tests/test_generate_workflow.py` — covers AUTO-02 generate extension tests
- [ ] Update `scripts/tests/test_cli.py` — add `"workflow"` to existing `test_all_commands_accepted`
- [ ] `templates/claude/commands/workflow-start.md.j2` — template stub
- [ ] `templates/claude/commands/workflow-status.md.j2` — template stub
- [ ] `templates/claude/commands/workflow-gate.md.j2` — template stub

---

## Project Constraints (from CLAUDE.md)

All CLAUDE.md directives apply to this phase. Extracted actionable rules:

| Directive | Impact on Phase 2 |
|-----------|-------------------|
| Python 3.10+ with `uv` toolchain | All scripts use `uv run python3`; no bare `python3` in commands |
| `snake_case.py` for script files | New file: `scripts/workflow.py` |
| `snake_case` for functions, `UPPER_CASE` for module constants | `ROOT`, `PLANNING_DIR` as module constants |
| Type hints with `|` union syntax (3.10+) | All function signatures use `List[str] | None` pattern |
| `sys.exit(main())` entry point | `workflow.py` must follow this pattern |
| `print()` for stdout, `sys.stderr` for errors | No logging library |
| `try/except` for specific errors with `sys.exit(1)` | Error handling in `cmd_*` functions |
| 4-space indentation, PEP 8 | Enforced by convention |
| Shebang `#!/usr/bin/env python3` on all scripts | Required on `workflow.py` |
| GSD Workflow Enforcement: start work via GSD command | Phase execution goes through `/gsd:execute-phase` |
| Core workflow logic in `scripts/`, not `.claude/` | D-02 compliance — the planner MUST enforce this |
| Adapter commands generated via `scripts/generate.py` | D-01 compliance — no hand-edited command files |

---

## Sources

### Primary (HIGH confidence)
- `scripts/cli.py` — actual CLI structure; routing and choices pattern confirmed
- `scripts/generate.py` — actual template rendering pipeline; extension pattern confirmed
- `scripts/gatekeeper.py` — frontmatter parsing pattern; test isolation approach confirmed
- `.claude/commands/gsd/execute-phase.md` — confirmed Claude Code command format in this repo
- `templates/claude/commands/dpc.md.j2` — confirmed existing template structure
- `pyproject.toml` — confirmed dependencies and console-script entry point
- `scripts/tests/test_integration.py` — confirmed subprocess integration test pattern
- `.planning/phases/02-claude-code-workflow-integration/02-CONTEXT.md` — locked decisions confirmed

### Secondary (MEDIUM confidence)
- `docs/portability/ai-tool-artifact-boundary.md` — Framework/adapter/runtime boundary rules
- `docs/design/architecture.md` — Four-layer model (Records, Skills, Gates, Adapters)
- `.planning/research/GSD-COMPARISON.md` — ECC per-harness pattern analysis

### Tertiary (LOW confidence — for reference only)
- ECC GitHub repo (`https://github.com/affaan-m/everything-claude-code`) — WebFetch unavailable; knowledge based on GSD-COMPARISON.md analysis in this repo, which confirms the per-harness directory pattern (`.claude/`, `.codex/`, `.cursor/`)

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — confirmed from existing `pyproject.toml` and running `pytest --collect-only`
- Architecture patterns: HIGH — all patterns derived from existing code in `scripts/`
- Pitfalls: HIGH — derived from known `generate.py` behavior (`FileExistsError`) and Phase 1 architectural decisions
- Test map: HIGH — framework confirmed running; test files identified as gaps to create

**Research date:** 2026-04-01
**Valid until:** 2026-05-01 (stable domain — Python stdlib, PyYAML, pytest)
