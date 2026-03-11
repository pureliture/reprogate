# AI Ops Policy for OMC

## Source of Truth

- Framework docs live under `docs/`
- Framework scripts live under `scripts/`
- Project-specific record paths come from `ai-ops.config.yaml`

## Mandatory First Reads

1. `WORKSPACE-PROFILE.md`
2. `AGENTS.md`
3. `docs/constitution.md`
4. `docs/process-catalog/README.md`

## Execution Rules

1. Start with `G0` alignment.
2. Recommend one process and one or two alternatives.
3. Wait for explicit user selection.
4. Record the chosen process with `python3 scripts/set_process_context.py ...`.
5. Resolve `team` vs `single` before implementation for team-capable processes.
6. Run `python3 scripts/check_compliance.py --mode working_tree` before process-end reporting.
