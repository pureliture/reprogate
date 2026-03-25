# Phase 1: Foundation & Governance - Context

**Gathered:** 2026-03-24
**Status:** Ready for planning

<domain>
## Phase Boundary

Establish the core framework for repository initialization, record creation, and policy enforcement.
This phase defines ReproGate's governance core and the evidence model it will enforce. It does **not**
turn ReproGate into a GSD-specific orchestrator; workflow automation and harness adapters belong in later phases.

</domain>

<decisions>
## Implementation Decisions

### Relation to external harnesses
- **D-01:** Treat GSD as a reference input, not as the product architecture or authority model for ReproGate.
- **D-02:** Position ReproGate as a harness-agnostic governance layer; GSD, SDD/Kiro-style workflows, and freeform chat are ingress paths, not the core identity.
- **D-03:** Future workflow automation should be described generically rather than as GSD-bound product scope.

### Evidence authority
- **D-04:** GSD-style artifacts such as `CONTEXT.md`, `PLAN.md`, `SUMMARY.md`, and `STATE.md` are helper artifacts, not authoritative proof on their own.
- **D-05:** Official gate authority remains in ReproGate-owned records, Skills, rules, and explicit verification evidence.

### Workflow ingress and gate convergence
- **D-06:** ReproGate must support both explicit workflow entry and workflow extraction from general conversation.
- **D-07:** Regardless of ingress, all paths must converge on the same evidence contract before implementation, merge, or release.
- **D-08:** The gatekeeper should fail closed on missing required evidence rather than treating workflow completion itself as success.

### CLI and adapter surface
- **D-09:** The core CLI should remain ReproGate-native and harness-neutral.
- **D-10:** Workflow-specific command experiences should live in adapters or outer harness layers instead of redefining the core product around one harness's vocabulary.

### the agent's Discretion
- Exact naming and packaging of future harness adapters
- Canonical schema names for intent, scope, execution, and verification records
- Whether adapter translations are one-way or partially round-trippable, as long as governance truth remains ReproGate-owned

</decisions>

<specifics>
## Specific Ideas

- Use ReproGate as an enterprise-grade decorating / layered harness rather than a single orchestrator.
- Support GSD today without preventing future harnesses or Kiro-style SDD flows later.
- Allow both forced workflow and ordinary conversation ingress, but require convergence before gated transitions.

</specifics>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### ReproGate core identity and governance
- `docs/strategy/final-definition.md` — Defines ReproGate as an artifact-driven compiler/gatekeeper rather than a heavy state orchestrator
- `docs/governance/constitution.md` — Defines fail-closed enforcement, traceability-first rules, and framework/adapter separation
- `docs/governance/operating-model.md` — Defines record-backed engineering as the operating model

### Current project scope
- `.planning/PROJECT.md` — Current project framing and active requirements
- `.planning/REQUIREMENTS.md` — Phase 1 requirement mapping (`CORE-01` to `CORE-05`)
- `.planning/ROADMAP.md` — Phase boundary, success criteria, and downstream milestone structure
- `.planning/research/GSD-COMPARISON.md` — Comparison and feasibility guidance for GSD reference use and harness-agnostic layering

### Existing implementation surfaces
- `scripts/cli.py` — Current CLI entry surface
- `scripts/init.py` — Existing repository bootstrap flow
- `scripts/generate.py` — Existing framework copy/render flow
- `scripts/gatekeeper.py` — Existing enforcement entrypoint to evolve in this phase
- `skills/record-required/guidelines.md` — Representative current Skill contract
- `skills/record-required/rules.rego` — Representative current rule surface

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `scripts/cli.py` — Existing command router that can grow a harness-neutral ReproGate surface
- `scripts/init.py` — Existing config bootstrap entrypoint
- `scripts/generate.py` — Existing portable framework generation pipeline
- `scripts/gatekeeper.py` — Existing Python gate evaluator to strengthen and connect with Skill/rule enforcement
- `skills/*/guidelines.md` + `skills/*/rules.rego` — Existing Skill + rule pairing model
- `templates/` — Existing scaffold root for portable generated assets

### Established Patterns
- Canonical governance belongs under `docs/` and `records/`, not in tool-specific runtime state
- Framework assets and adapter-owned assets should stay physically separated
- Python CLI + Markdown artifacts + YAML/TOML/JSON config is the current implementation style

### Integration Points
- Future harness adapters should translate into ReproGate records, Skills, and gates rather than replace them
- Workflow automation must write artifacts the gatekeeper can inspect deterministically
- Core CLI additions should connect through `scripts/cli.py` and reuse existing init/generate/gatekeeper flows where possible

</code_context>

<deferred>
## Deferred Ideas

- Full adapter design for non-GSD harnesses belongs to later phases
- Exact Kiro/SDD adapter semantics belong outside Phase 1

</deferred>

---

*Phase: 01-foundation-governance*
*Context gathered: 2026-03-24*
