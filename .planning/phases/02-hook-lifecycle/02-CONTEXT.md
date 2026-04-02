# Phase 2: Hook Lifecycle - Context

**Gathered:** 2026-04-02
**Status:** Ready for planning
**Mode:** Auto-generated (discuss skipped via workflow.skip_discuss)

<domain>
## Phase Boundary

Harness automatically captures session state, governance events, and gate failures through the ECC hook lifecycle. Phase delivers: REPROGATE_HOOK_PROFILE gating (minimal/standard/strict), SessionStart hook (current-session.json init), Stop hook (session summary + observation YAML draft), PreCompact hook (pre-compact-state.json), PreToolUse governance capture (advisory + hard gate at git commit), PostToolUseFailure gate failure logger to records/gate-failures/.

</domain>

<decisions>
## Implementation Decisions

### Claude's Discretion
All implementation choices are at Claude's discretion — discuss phase was skipped per user setting. Use ROADMAP phase goal, success criteria, and codebase conventions to guide decisions.

Key constraints from requirements:
- All hooks must check `REPROGATE_HOOK_PROFILE` (minimal/standard/strict) and gate behavior on profile
- Phase 1 stub scripts (session_start.py, session_stop.py, pretooluse_guard.py, failure_logger.py) must be fully implemented
- Session data stored in `.claude/session-data/` (project-local, gitignored)
- Hook base module `scripts/hooks/reprogate_hook_base.py` already exists with `check_disabled()`
- PreToolUse: advisory during CC execution, hard gate only at `git commit` via pre-commit hook
- Gate failures logged to `records/gate-failures/` (auto-created if missing)

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `scripts/hooks/reprogate_hook_base.py` — `check_disabled()` for REPROGATE_DISABLED env var
- `scripts/hooks/session_start.py` — Phase 1 stub (exit 0), needs full implementation
- `scripts/hooks/session_stop.py` — Phase 1 stub (exit 0), needs full implementation
- `scripts/hooks/pretooluse_guard.py` — Phase 1 stub (exit 0), needs full implementation
- `scripts/hooks/failure_logger.py` — Phase 1 stub (exit 0), needs full implementation
- `.claude/settings.json` — hooks already wired (SessionStart, Stop, PreToolUse/Bash, PostToolUseFailure)
- `scripts/hooks/__init__.py` — package init exists

### Established Patterns
- Hook scripts use `check_disabled()` early exit from reprogate_hook_base
- Scripts use `sys.path.insert(0, ...)` for local imports
- TDD pattern: test file first (RED), then implementation (GREEN)
- All scripts use `uv run python3 -m pytest` for testing
- JSON for structured data (session-data files)
- YAML frontmatter for observation drafts

### Integration Points
- `scripts/hooks/` directory is the hook implementation home
- `.claude/session-data/` is the session state directory (Phase 1 created + gitignored)
- `records/gate-failures/` is the failure log directory (needs creation)
- `scripts/gatekeeper.py` already implements gate evaluation

</code_context>

<specifics>
## Specific Ideas

No specific requirements — discuss phase skipped. Refer to ROADMAP phase description and success criteria.

</specifics>

<deferred>
## Deferred Ideas

None — discuss phase skipped.

</deferred>
