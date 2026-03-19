# ReproGate Adapter Rules for dev-ps-cast

Use the ReproGate framework as the source of truth for all AI-assisted work in this repository.

## Required References

Read these files before starting substantial work:

1. `WORKSPACE-PROFILE.md`
2. `docs/governance/constitution.md`
3. `docs/governance/operating-model.md`
4. `docs/strategy/final-definition.md`

## Operating Rules

ReproGate is an **artifact-driven compiler/gatekeeper**, not a state-tracking orchestrator. Your execution must be record-backed.

1. **Record-First Work**: Before implementing code changes, ensure there is a clear work record (e.g., plan, intent, scope).
2. **Explainable Decisions**: Document any significant technical decisions, alternative approaches discarded, and the reasoning behind them.
3. **Verification over Completion**: Implementation alone is not completion. Always include explicit verification steps and document the results.
4. **Skills and Gates**: Rely on explicitly recorded rules (`rules.rego`) and guidelines (`guidelines.md`) when they exist in the repository to guide your workflow.

## Expected Behavior

- Do not rely solely on conversational memory; if it matters, it should exist as an inspectable artifact.
- Follow the workflow dictated by the presence or absence of required outputs (Artifact-Driven Workflow). If a required artifact (like a design doc) is missing, create or request it before proceeding.

## Python Execution Standard

This repository uses `uv` as the Python execution standard.

### Required

- Use `uv run python3 <script>` for all Python execution
- Declare persistent dependencies in `pyproject.toml` and lock them in `uv.lock`

### Forbidden

- `python3 -m venv` - Do not create virtual environments manually
- `source venv/bin/activate` - Do not activate virtual environments
- `pip install` / `pip3 install` - Do not use pip directly
- `uv run --with ...` in committed code - Use `pyproject.toml` for persistent dependencies

### Examples

```bash
# Run a script
uv run python3 scripts/validate_product_definition.py --help

# One-liner
uv run python3 -c "print('hello')"

# Install dependencies (CI or first-time setup)
uv sync --frozen
```
