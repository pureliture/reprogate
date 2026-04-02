# Phase 1: Harness Bootstrap - Context

**Gathered:** 2026-04-02
**Status:** Ready for planning
**Mode:** Auto-generated (infrastructure phase — discuss skipped)

<domain>
## Phase Boundary

Phase 1 delivers the harness installation and activation surface: `reprogate init` injects hook configuration into `.claude/settings.json` and initializes `.claude/session-data/`; `reprogate disable` cleanly removes hook config; `REPROGATE_DISABLED=1` env var disables hook layer without uninstalling; `record_triggers` path patterns correctly gate record requirements; and template files (`AGENTS.md.j2`, `CLAUDE.md.j2`) are updated to reflect harness identity with `generate.py` schema aligned to `init.py` output.

</domain>

<decisions>
## Implementation Decisions

### Claude's Discretion
All implementation choices are at Claude's discretion — pure infrastructure phase. Use ROADMAP success criteria (INIT-01 through INIT-06) and existing codebase conventions to guide all decisions.

Key constraints from requirements:
- `reprogate init` must modify `.claude/settings.json` (hooks injection)
- `reprogate disable` must remove hook config from `.claude/settings.json`
- `REPROGATE_DISABLED=1` env var disables hook layer (no file changes needed)
- `record_triggers` in `reprogate.yaml` gates record requirements
- Schema alignment between `init.py` output and `generate.py` expectations

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `scripts/cli.py` — unified entry point; add `init` (hook injection), `disable` subcommands
- `scripts/init.py` — currently generates `reprogate.yaml`; needs extension for hook injection
- `scripts/generate.py` — template rendering with PyYAML; schema needs alignment with `init.py`
- `templates/AGENTS.md.j2`, `templates/CLAUDE.md.j2` — need harness identity text updates

### Established Patterns
- CLI uses `argparse` with subcommands routed via `run_script()`
- Config loading via PyYAML with defaults merging (`load_config()` in `generate.py`)
- Template rendering via simple string replacement (not Jinja2)
- `.claude/settings.json` is the ECC hook configuration file

### Integration Points
- `scripts/cli.py` routes subcommands — add `init` (hook injection) and `disable` commands
- `.claude/settings.json` is where hooks are configured (ECC standard)
- `reprogate.yaml` holds `record_triggers` for path-based gating
- `.claude/session-data/` is the session state directory to initialize

</code_context>

<specifics>
## Specific Ideas

No specific requirements — infrastructure phase. Follow INIT-01 through INIT-06 requirements exactly as specified in REQUIREMENTS.md.

</specifics>

<deferred>
## Deferred Ideas

None — discuss phase skipped.

</deferred>
