# Codebase Concerns

**Analysis Date:** 2026-03-24

## Tech Debt

**Bootstrap config schema split:**
- Issue: `scripts/init.py` renders a flat config from `templates/reprogate.yaml.j2` (`project_name`, `skills_dir`, `records_dir`), while `scripts/generate.py` expects a nested schema with `project.name`, `workspaces.primary.*`, `tools.*`, and `records.*`.
- Files: `scripts/init.py`, `templates/reprogate.yaml.j2`, `scripts/generate.py`, `reprogate.yaml`, `scripts/tests/test_bootstrap_smoke.py`
- Impact: the advertised bootstrap flow is internally inconsistent; `uv run python3 scripts/generate.py --config reprogate.yaml --output-root . --force` crashes with `KeyError: 'name'` against the repository's own `reprogate.yaml`.
- Fix approach: define one canonical config schema, update both `init.py` and `generate.py` to use it, regenerate `reprogate.yaml`, and rewrite the smoke tests to assert the same structure end to end.

**Removed compliance layer is still wired into the product surface:**
- Issue: multiple entrypoints still depend on `scripts/check_compliance.py` and `scripts/set_process_context.py`, but neither file exists in the working tree.
- Files: `scripts/cli.py`, `scripts/hooks/claude_pretooluse_guard.py`, `scripts/install_git_hooks.sh`, `templates/claude/commands/dpc.md.j2`, `scripts/tests/test_bootstrap_smoke.py`, `scripts/tests/test_yaml_parsing.py`
- Impact: `scripts/cli.py check` is dead, the Claude pre-tool hook points at a missing checker, the hook installer fails during `chmod`, and the test suite hard-fails before the bootstrap path can be validated.
- Fix approach: either restore the missing scripts or replace every remaining reference with the current `scripts/gatekeeper.py` and a real process-context implementation.

**Identity transition is incomplete across runtime, docs, and tests:**
- Issue: ReproGate-facing files still expose legacy `dpc` and `ai-ops` names, paths, and examples.
- Files: `scripts/cli.py`, `scripts/search_docs.py`, `README.md`, `docs/README.md`, `templates/claude/commands/dpc.md.j2`, `templates/claude/settings.json.j2`, `scripts/tests/test_bootstrap_smoke.py`
- Impact: contributors are directed toward obsolete names such as `ai-ops.config.yaml`, `.ai-ops/README.md`, and `dpc` commands, which makes onboarding, debugging, and generated output reviews harder.
- Fix approach: sweep the user-facing command surface, templates, tests, and docs in one change so the repository presents one product identity.

**Policy-engine claims are ahead of implementation:**
- Issue: the repository ships `rules.rego` files and documents OPA/Rego enforcement, but `scripts/gatekeeper.py` never invokes OPA and only performs hard-coded Python checks.
- Files: `scripts/gatekeeper.py`, `skills/record-required/rules.rego`, `skills/decision-documented/rules.rego`, `skills/scope-defined/rules.rego`, `skills/verification-present/rules.rego`, `records/adr/ADR-002-rules-engine-selection.md`, `templates/reprogate.yaml.j2`
- Impact: the product advertises Rego-based gating, but current enforcement ignores the rules files entirely; rule edits do not change runtime behavior and `gatekeeper.strict_mode` in `reprogate.yaml` creates false confidence.
- Fix approach: implement OPA-backed evaluation in `scripts/gatekeeper.py`, or explicitly relabel the current gate as a Stage-1 Python fallback and stop exposing unused policy settings until they work.

## Known Bugs

**`generate.py` crashes against the repository's current config:**
- Symptoms: `uv run python3 scripts/generate.py --config reprogate.yaml --output-root . --force` raises `KeyError: 'name'`.
- Files: `scripts/generate.py`, `reprogate.yaml`, `templates/reprogate.yaml.j2`
- Trigger: run the generator against a config produced by `scripts/init.py` or the checked-in `reprogate.yaml`.
- Workaround: no reliable in-repo workaround; the script only runs if a manually rewritten nested config is supplied.

**Git hook installation fails on a clean checkout:**
- Symptoms: `bash scripts/install_git_hooks.sh` aborts on missing files during `chmod`, specifically `scripts/check_compliance.py` and `scripts/set_process_context.py`.
- Files: `scripts/install_git_hooks.sh`, `scripts/hooks/claude_pretooluse_guard.py`
- Trigger: execute `scripts/install_git_hooks.sh` in the current working tree.
- Workaround: install hooks manually and point them at existing scripts such as `scripts/gatekeeper.py`.

## Security Considerations

**Branch-mutating workflow runs with write permissions on PR activity:**
- Risk: `.github/workflows/update-progress-report.yml` grants `contents: write` and pushes commits back to `${{ github.event.pull_request.head.ref }}` during `pull_request` events.
- Files: `.github/workflows/update-progress-report.yml`, `meta/progress/build_progress_report.py`
- Current mitigation: the workflow only stages `meta/progress/progress.md` and `meta/progress/progress.json`.
- Recommendations: restrict auto-commit behavior to `push`/`workflow_dispatch`, or move report generation to a non-PR workflow so workflow bugs cannot mutate contributor branches during review.

**Documented policy enforcement can be bypassed by implementation gaps:**
- Risk: the repo claims OPA/Rego-backed enforcement in `README.md`, `docs/spec/product-surface-spec.md`, and `records/adr/ADR-002-rules-engine-selection.md`, but the live gate in `scripts/gatekeeper.py` does not execute `rules.rego`.
- Files: `README.md`, `docs/spec/product-surface-spec.md`, `records/adr/ADR-002-rules-engine-selection.md`, `scripts/gatekeeper.py`
- Current mitigation: `scripts/gatekeeper.py` still checks frontmatter and required section names in `records/`.
- Recommendations: treat current gating as best-effort only, add CI that proves `rules.rego` changes affect runtime behavior, and remove the "OPA required" claim from `README.md` until OPA is actually executed.

## Performance Bottlenecks

**Progress report generation scales linearly with external API calls:**
- Problem: `meta/progress/build_progress_report.py` fetches each issue/PR state individually while iterating every item in `meta/progress/progress-map.yaml`.
- Files: `meta/progress/build_progress_report.py`, `meta/progress/progress-map.yaml`, `.github/workflows/update-progress-report.yml`
- Cause: each `kind: issue` and `kind: pr` entry triggers its own GitHub API or `gh` CLI call.
- Improvement path: batch state reads through GraphQL, cache responses per run, and avoid running the workflow on every issue/PR edit when only progress metadata changes.

## Fragile Areas

**Core docs point to directories and records that do not exist:**
- Files: `docs/README.md`, `docs/governance/operating-model.md`, `docs/governance/ops-bootstrap-master-plan.md`
- Why fragile: the docs reference missing paths such as `docs/guide/`, `docs/process-catalog/`, `docs/work-packets/`, and `docs/adr/`, so "read this first" guidance sends contributors to dead ends.
- Safe modification: add a markdown link check in CI before moving doc trees, and update all top-level read-order docs as part of any documentation reorganization.
- Test coverage: no automated doc-link validation exists in `scripts/tests/` or `.github/workflows/`.

**Adapter and workflow content is duplicated four ways:**
- Files: `.claude/get-shit-done/**`, `.codex/get-shit-done/**`, `.gemini/get-shit-done/**`, `.github/get-shit-done/**`, `.claude/agents/**`, `.codex/agents/**`, `.gemini/agents/**`, `.github/agents/**`
- Why fragile: each `get-shit-done` tree currently contains 133 files, and the agent surfaces are duplicated per tool vendor, so every fix requires multi-surface sync and stale references can survive in only one copy.
- Safe modification: treat one tree as canonical, generate the other adapter surfaces from it, and verify byte-for-byte sync in CI.
- Test coverage: no generator or integrity test currently proves these duplicated surfaces stay aligned.

## Scaling Limits

**Manual duplication becomes a maintenance multiplier as tool surfaces grow:**
- Current capacity: four copies of the `get-shit-done` payload (`.claude/`, `.codex/`, `.gemini/`, `.github/`), each with 133 files, plus duplicated agent catalogs.
- Limit: every doc, workflow, or prompt change multiplies into four review surfaces and makes partial migrations likely.
- Scaling path: store one canonical source tree under `templates/` or a dedicated generator input, then regenerate vendor-specific outputs instead of editing copies by hand.

**Progress tracking is tied to fixed issue numbers and placeholder scores:**
- Current capacity: `meta/progress/progress-map.yaml` mixes live GitHub issue/PR numbers with `manual_placeholder` entries.
- Limit: roadmap accuracy depends on keeping hard-coded numbers valid; missing GitHub objects resolve to `0.0`, and placeholder scores can drift away from real delivery state.
- Scaling path: move to label-based or query-based aggregation, or record explicit stage evidence in versioned project artifacts instead of manual placeholders.

## Dependencies at Risk

**PyYAML is required at runtime, but execution guidance is inconsistent:**
- Risk: `scripts/generate.py` imports `yaml`, while `README.md`, `scripts/install_git_hooks.sh`, and other entrypoints still instruct users to run plain `python3` instead of the `uv run` standard adopted in `records/adr/ADR-007-uv-toolchain-adoption.md`.
- Impact: fresh environments hit `ModuleNotFoundError: No module named 'yaml'`, and contributors can misdiagnose the failure as a code bug instead of an execution-mode mismatch.
- Migration plan: standardize every Python invocation on `uv run python3 ...`, including docs, hooks, tests, and generated templates, or remove the PyYAML dependency from the bootstrap path.

## Missing Critical Features

**No working `check` implementation in the current tree:**
- Problem: the advertised compliance entrypoint no longer exists, but the repo still routes commands and hooks through it.
- Blocks: `scripts/cli.py check`, `scripts/install_git_hooks.sh`, `scripts/tests/test_bootstrap_smoke.py`, `scripts/tests/test_yaml_parsing.py`, and the Claude hook path in `scripts/hooks/claude_pretooluse_guard.py`.

**No automated documentation integrity check:**
- Problem: broken read-order links and missing directories can persist without any gate.
- Blocks: trustworthy onboarding from `README.md`, `docs/README.md`, and `docs/governance/operating-model.md`.

## Test Coverage Gaps

**`scripts/gatekeeper.py` and hook installation paths are effectively untested:**
- What's not tested: the current gate implementation in `scripts/gatekeeper.py`, the shell installer in `scripts/install_git_hooks.sh`, and the repo hook in `scripts/hooks/git_pre_commit.sh`.
- Files: `scripts/gatekeeper.py`, `scripts/install_git_hooks.sh`, `scripts/hooks/git_pre_commit.sh`
- Risk: the only live enforcement path can drift independently from the stale bootstrap tests and fail in real repositories without warning.
- Priority: High

**Current bootstrap tests no longer represent the shipped product surface:**
- What's not tested: a passing end-to-end flow for the real `reprogate.yaml`, `scripts/init.py`, `scripts/generate.py`, and hook/check commands.
- Files: `scripts/tests/test_bootstrap_smoke.py`, `scripts/tests/test_yaml_parsing.py`, `scripts/init.py`, `scripts/generate.py`
- Risk: regressions in the initialization path are already shipping; the current test suite fails under `uv run python3 -m unittest discover -s scripts/tests -v`.
- Priority: High

**Validation and reporting scripts have no focused tests:**
- What's not tested: PR body validation rules and progress scoring behavior.
- Files: `scripts/validate_product_definition.py`, `meta/progress/build_progress_report.py`, `meta/progress/progress-map.yaml`
- Risk: CI-only logic can reject valid PRs, miss invalid ones, or emit misleading progress reports without local feedback.
- Priority: Medium

---

*Concerns audit: 2026-03-24*
