---
phase: 1
reviewers: [gemini, codex]
reviewed_at: 2026-03-25T09:10:00+09:00
plans_reviewed: [01-01-PLAN.md, 01-02-PLAN.md, 01-03-PLAN.md]
---

# Cross-AI Plan Review — Phase 1

## Gemini Review

### 1. Summary
The proposed plans provide a logical and sequential path toward establishing ReproGate's core governance framework. Plan 01 correctly prioritizes the user experience and record-taking capability, while Plan 03 ensures long-term stability through integration testing and configuration schema expansion. However, **Plan 02 contains a significant architectural risk** regarding the "Python-native Rego evaluator," which threatens the project's promise of standardized policy-as-code enforcement.

### 2. Strengths
- **Traceability-First Design:** The sequential ID format (`ADR-YYYYMMDD-NNN`) in Plan 01 is excellent for AI-driven development, providing immutable temporal context for every decision.
- **Fail-Closed Security:** Plan 02 explicitly addresses User Decision **D-08** by refactoring the gatekeeper to fail closed, ensuring no unverified work bypasses the governance layer.
- **Unified Entry Point:** The rebranding and routing in Plan 01 fulfill **D-09**, consolidating the toolset into a single, harness-neutral CLI.
- **Validation Loop:** Plan 03's focus on integration tests (`test_integration.py`) is critical for a tool that markets "reproducibility" as its core value.

### 3. Concerns
- **HIGH: The "Rego-lite" Trap (Plan 02, Task 1):** Implementing a "Python-native" evaluator for a subset of Rego is highly risky. Rego is a complex logic language; a partial parser creates a "leaky abstraction" where users might write valid Rego that silently fails or behaves inconsistently. Breaks the "Policy-as-Code" promise and creates significant technical debt.
- **MEDIUM: Template Decoupling (Plan 01, Task 1):** The plan mentions scaffolding "sections" but doesn't explicitly state it will use the existing `.j2` templates in `templates/records/`. Hardcoding record structures in Python scripts makes the system less extensible.
- **LOW: Sequential ID Collision (Plan 01, Task 1):** The plan doesn't specify how it handles concurrent record creation in a team environment.
- **LOW: Dependency on `uv` (General):** The plans don't mention ensuring `uv` environment isolation during init or gatekeeper execution.

### 4. Suggestions
- **Adopt Official OPA Tooling:** In Plan 02, replace the custom evaluator with a call to the `opa` binary or a verified library. If a lightweight Python-native check is required, avoid calling it "Rego" to prevent user confusion.
- **Centralize Template Logic:** Ensure `create_record.py` uses a Jinja2 environment to render the templates in `templates/records/`.
- **Atomic Sequential Check:** Implement a robust "next ID" finder that scans the records directory.
- **CLI Argument Passthrough:** Ensure `scripts/cli.py` correctly passes sub-command flags to underlying scripts.

### 5. Risk Assessment
**Level: MEDIUM** — The path to a functional CLI and record system is clear and well-ordered. However, the risk of building a custom, incomplete Rego evaluator is the primary concern.

---

## Codex Review

### Cross-cutting findings

Two repository facts materially change the review:
- The current CLI is broken because `check` still routes to a nonexistent `check_compliance.py`.
- The repo already has an accepted ADR (ADR-002) choosing OPA/Rego as the rules engine, explicitly to avoid writing a custom parser/interpreter in Python.

### Plan 01: CLI Entry Point & Record Creation

**Summary:** Directionally right and fixes a real blocker fast, but underspecifies the actual record contract and likely does not fully satisfy CORE-05.

**Strengths:**
- Fixes an immediate repo defect: broken `check` routing.
- Targets a real phase goal by adding record creation to the unified CLI surface.
- TDD-first posture is appropriate.
- Narrow enough to be deliverable in one wave.

**Concerns:**
- `HIGH`: The plan may not achieve CORE-05. Updating `scripts/cli.py` alone does not create an installed `reprogate` entry point; there is no console-script registration in pyproject.toml.
- `HIGH`: Proposed IDs like `ADR-YYYYMMDD-NNN` conflict with current repository conventions (`ADR-003`, `RFC-003`). That is a migration/design decision, not a harmless implementation detail.
- `MEDIUM`: No mention of slug sanitization, collision behavior, or honoring configurable record paths.
- `LOW`: "Fix branding from dpc to ReproGate" is useful but easy to let cosmetic work grow wider than needed.

**Suggestions:**
- Define the canonical record ID/file naming scheme before implementation.
- Make `create` respect config-driven record directories.
- Add packaging work for a real `reprogate` command, or narrow CORE-05 wording.

**Risk Assessment:** `MEDIUM`

### Plan 02: Skill Evaluator & Gatekeeper Refactor

**Summary:** This is the weakest plan as written. Building a Python-native mini-Rego evaluator directly conflicts with the repository's accepted architecture (ADR-002) and creates a long-term correctness trap.

**Strengths:**
- Correctly identifies that current YAML parsing is too hand-rolled.
- Moves toward cleaner separation between record collection and rule evaluation.
- Aligns with D-08 in spirit by emphasizing fail-closed behavior.

**Concerns:**
- `HIGH`: A Python-native evaluator contradicts ADR-002 that explicitly chose OPA/Rego to avoid implementing a parser/interpreter in-house.
- `HIGH`: Supporting only "5 specific patterns" creates silent policy drift. Future valid Rego rules could become unsupported.
- `HIGH`: The repo already stores real Rego policies. Reinterpreting them in Python introduces dual semantics.
- `MEDIUM`: No test strategy for policy evaluation equivalence, malformed `.rego`, or OPA invocation errors.

**Suggestions:**
- Replace `skill_evaluator.py` with an OPA wrapper that builds input, evaluates via `opa eval`, and fails closed on missing binary/invalid policy.
- If OPA integration is deferred, record a new ADR first; otherwise this plan is governance-noncompliant.

**Risk Assessment:** `HIGH`

### Plan 03: Config Schema & Integration Tests

**Summary:** Contains necessary work, but sequenced too late and misses the deeper config mismatch between `init.py`, `generate.py`, and the template.

**Strengths:**
- Adds end-to-end testing.
- Correctly targets the broken smoke test dependency.
- Recognizes that `init.py` and the config template need coordinated updates.

**Concerns:**
- `HIGH`: Config contract is already inconsistent: `init.py` renders a flat template while `generate.py` expects nested sections.
- `HIGH`: `active_skills`, `record_types`, and `fail_closed` don't define coexistence with current config fields.
- `MEDIUM`: Integration test scope is too narrow.
- `MEDIUM`: Current tests still use legacy `ai-ops` naming.

**Suggestions:**
- Move config-schema reconciliation earlier.
- Define one canonical `reprogate.yaml` structure consumed by both `init.py` and `generate.py`.
- Expand integration coverage to include fail-closed behavior, config portability, and active-skill selection.

**Risk Assessment:** `MEDIUM-HIGH`

### Overall Recommendation
Prioritize: 1) Lock canonical config schema, 2) Implement CLI + record creation aligned to existing standards, 3) Integrate with OPA/Rego directly, 4) Add end-to-end tests. The main blocker is Plan 02 as written.

---

## Consensus Summary

### Agreed Strengths
- TDD-first approach and fail-closed security posture are well-designed (both reviewers)
- CLI branding fix and unified entry point are valuable and correctly scoped (both reviewers)
- Integration testing in Plan 03 is critical for reproducibility promise (both reviewers)

### Agreed Concerns
1. **[HIGH] Python-native Rego evaluator is architecturally risky** — Both reviewers flag Plan 02's custom evaluator as the top concern. Gemini calls it the "Rego-lite Trap"; Codex notes it contradicts ADR-002 which explicitly chose OPA to avoid in-house interpreters. Both recommend using OPA binary or recording a new ADR if deferring.
2. **[HIGH] CORE-05 may not be satisfied** — Codex flags that `scripts/cli.py` alone doesn't create an installed `reprogate` entry point (no console-script in pyproject.toml). Gemini notes CLI argument passthrough needs attention.
3. **[MEDIUM-HIGH] Config schema inconsistency** — Codex identifies that `init.py` and `generate.py` already disagree on config structure. Gemini notes template decoupling concern. Both suggest locking the canonical config schema earlier.
4. **[MEDIUM] Record ID naming conflict** — Codex flags that `ADR-YYYYMMDD-NNN` conflicts with existing `ADR-003` convention. Gemini's sequential ID collision concern is related.

### Divergent Views
- **OPA vs Python-native:** Gemini suggests OPA binary OR verified library as alternatives; Codex is firmer that OPA wrapper is the only acceptable path given ADR-002.
- **Plan ordering:** Codex argues config schema should move earlier (before Plan 01); Gemini accepts the current wave ordering.
- **Scope of Plan 01:** Codex raises CORE-05 packaging concern as HIGH; Gemini doesn't flag this specifically.
