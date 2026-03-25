# GSD Framework Comparison for ReproGate

**Project:** ReproGate  
**Compared artifact:** vendored GSD framework in `.github/get-shit-done/`  
**Prepared:** 2026-03-24  
**Status:** Research complete, ready to inform Phase 1 discussion and Phase 3 design

## Executive Summary

ReproGate has **not yet completed a canonical comparison/reference pass** against the vendored GSD framework.
Today, direct GSD references are visible only in planning artifacts such as `.planning/PROJECT.md`,
`.planning/ROADMAP.md`, and `.planning/REQUIREMENTS.md`; the repository's canonical `docs/` and `records/`
surfaces do not currently define ReproGate's relationship to GSD.

The comparison shows that **GSD and ReproGate are complementary, not interchangeable**.
GSD is primarily a **workflow orchestrator**: it structures work into project setup, discussion, research,
planning, execution, verification, completion, milestone management, and handoff. ReproGate is primarily an
**artifact-driven compiler/gatekeeper**: it requires durable records, accumulates reusable Skills, and enforces
rules against inspectable evidence.

Recommended posture:

- **Use GSD as an execution shell and operator experience layer**
- **Keep ReproGate as the governance and evidence engine**
- **Do not let GSD's mutable planning state replace ReproGate's record-backed truth model**
- **Document the relationship explicitly before deeper integration work**

## Current Status in This Repository

### What already exists

- Vendored GSD workflow/runtime assets under `.github/get-shit-done/`
- GSD-oriented planning artifacts already initialized in `.planning/`
- Roadmap intent to automate harness-neutral workflow automation in **Phase 3**

### What is missing

- No canonical strategy or ADR that says whether GSD is:
  - a reference architecture,
  - a compatibility target,
  - an embedded workflow engine,
  - or a temporary bootstrap mechanism
- No explicit mapping between GSD artifacts and ReproGate evidence/gate semantics
- No durable document that explains which GSD patterns should be adopted, modified, or rejected

## GSD Framework Overview

### Structure

The vendored GSD payload is a self-contained workflow framework centered on:

- `bin/gsd-tools.cjs` — operational CLI for state, roadmap, templates, commits, phase init, verification, config, and todo flows
- `bin/lib/*.cjs` — parsing, initialization, state progression, template fill, roadmap analysis, config, verification, workstream, and git helpers
- `workflows/*.md` — command-level orchestration logic such as `new-project`, `discuss-phase`, `plan-phase`, `execute-phase`, `verify-work`, `complete-milestone`, `next`
- `templates/*.md` — canonical artifact shapes for `PROJECT.md`, `REQUIREMENTS.md`, `ROADMAP.md`, `STATE.md`, context, research, summary, verification, discussion log, UAT, and milestone docs
- `references/*.md` — operational guidance for config, git integration, checkpoints, questioning, TDD, and verification patterns

This means GSD is not just "a few prompts." It is a **documented workflow engine plus a supporting CLI runtime**.

### Core concepts

GSD organizes delivery around a predictable chain:

1. Initialize project
2. Gather phase context
3. Research phase
4. Generate executable plans
5. Execute plans
6. Verify outcomes
7. Complete phase / milestone

Its core durable artifacts are:

- `.planning/PROJECT.md`
- `.planning/REQUIREMENTS.md`
- `.planning/ROADMAP.md`
- `.planning/STATE.md`
- per-phase directories with `CONTEXT.md`, `RESEARCH.md`, `PLAN.md`, `SUMMARY.md`, `VERIFICATION.md`, `UAT.md`, `DISCUSSION-LOG.md`
- `.planning/config.json`
- `.planning/todos/`

### Workflow engine

GSD workflows are declarative in Markdown but operationally backed by `gsd-tools.cjs`.
The workflow docs describe what to read, what to ask, what artifacts to write, what agent types to use,
and when to commit/update state. The Node CLI provides the repeatable primitives that keep those workflows
from devolving into fragile inline shell scripts.

Important characteristics:

- explicit phase initialization (`init phase-op`, `init plan-phase`, `init execute-phase`)
- explicit state progression (`state begin-phase`, `state record-session`, `state advance-plan`)
- explicit roadmap introspection (`roadmap get-phase`, `roadmap analyze`)
- explicit artifact scaffolding and template fill
- explicit git handling for planning artifacts via `commit_docs` and branch strategies

### Agent model

GSD assumes a multi-agent workflow model:

- specialized agents for research, planning, execution, verification, UI review, debugging, assumptions, and integration
- orchestrator workflows that decide when to spawn or inline those agents
- runtime-specific fallbacks when a host cannot reliably coordinate subagents

Notably, `execute-phase.md` contains a **Copilot-specific fallback** to sequential inline execution because
subagent completion signals are not always reliable. This is a practical sign that GSD is designed as a
real multi-runtime orchestration system, not just a single-tool prompt pack.

### Git and history model

GSD treats planning artifacts as optionally versioned operational state:

- if `commit_docs: true`, `.planning/` artifacts are committed
- if `commit_docs: false`, GSD still uses them, but keeps them local/private
- branch strategies can be `none`, `phase`, or `milestone`

This is stronger than "session memory" but weaker than a fully governed record model. It preserves execution
history well, but it does not by itself define whether a planning document is authoritative evidence.

## ReproGate Overview (Current State)

ReproGate's current core is concentrated in:

- `docs/strategy/final-definition.md`
- `docs/governance/constitution.md`
- `docs/governance/operating-model.md`
- `scripts/init.py`
- `scripts/generate.py`
- `scripts/cli.py`
- `scripts/gatekeeper.py`
- `skills/*/guidelines.md`
- `skills/*/rules.rego`
- `templates/`
- `records/`

The current implementation emphasizes:

- **record-backed intent**
- **Skills as reusable work patterns**
- **Rego-based rule enforcement**
- **framework vs adapter boundary**
- **artifact-first, fail-closed governance**

The key distinction from GSD is that ReproGate's identity is not "move work through a state machine."
Its identity is "require evidence, then enforce rules against that evidence."

## Comparison Table

| Dimension | GSD | ReproGate | Implication |
|---|---|---|---|
| Primary identity | Workflow orchestrator for discuss → plan → execute → verify → complete | Artifact-driven compiler/gatekeeper for records, Skills, and rules | ReproGate should not collapse into a workflow-only product |
| Main durable unit | Planning/state artifacts in `.planning/` | Records, Skills, rules, and governance docs | GSD artifacts can be inputs/evidence, but should not replace ReproGate records |
| State model | Explicit `STATE.md`, `ROADMAP.md`, phase status, config flags, workstreams, waiting signals | Explicitly skeptical of heavy state tracking; prefers inspectable artifacts and gates | Use GSD state as operational context, not as final truth |
| Enforcement | Procedural workflow discipline plus verification steps | Fail-closed gates inspecting artifacts and rules | ReproGate remains stronger on auditable compliance |
| Agent model | Native multi-agent orchestration with named specialist roles and runtime fallbacks | No first-class orchestrator yet; current repo is governance-heavy | GSD is a strong reference for orchestration ergonomics |
| Template system | Large library of planning/execution templates plus template-fill helpers | Simpler repo/bootstrap generation from `reprogate.yaml` and copied framework files | ReproGate can borrow richer execution artifact templates |
| Git model | Planning docs optionally committed; phase/milestone branch support | Strong PR/body/doc alignment requirements and durable records | GSD is stronger on workflow-local git ergonomics; ReproGate is stronger on governance traceability |
| Scope discipline | Enforced by phase boundaries and workflow rules | Enforced by explicit records, strategy docs, and gates | The two approaches fit together well |
| Portability boundary | Practical but currently duplicated across `.github/`, `.claude/`, `.codex/`, `.gemini/` vendored trees | Explicitly separates framework assets from adapter-owned assets | ReproGate has the clearer long-term architecture here |
| Audit trail | Rich execution logs: context, discussion logs, summaries, verification, milestone history | Rich governance trail: ADRs, RFCs, Skills, PR validation, operating model | Best result is a layered model: GSD for execution trace, ReproGate for governance proof |

## Where GSD Is Stronger

### 1. End-to-end delivery ergonomics

GSD already has the connective tissue ReproGate does not yet have:

- `/gsd-next` style state-based routing
- lightweight discussion capture
- research and plan loops
- execution/verification orchestration
- todo folding and deferred-idea handling
- milestone completion flows

This is valuable because ReproGate currently explains **what must be true** better than it explains
**how a contributor moves through work day to day**.

### 2. Execution artifact richness

GSD's artifact set is much more complete for active implementation work:

- context capture
- discussion log
- phase research
- structured plans
- summaries
- verification reports
- UAT tracking
- session continuity

ReproGate currently has stronger governance documents, but a weaker standard operating surface for
in-flight implementation work.

### 3. Runtime-aware multi-agent design

GSD already encodes practical lessons about:

- unreliable subagent completion
- worktree/workstream variants
- conditional auto-advance
- checkpoint types
- planning privacy vs committed docs

That makes GSD a strong reference point for ReproGate Phase 3.

## Where ReproGate Is Stronger

### 1. Product clarity

ReproGate has a clearer statement of what it is:

- not a heavy state tracker
- not a prompt library
- not a vendor wrapper
- yes to records, Skills, rules, and gates

This clarity is captured in `docs/strategy/final-definition.md`, `docs/governance/constitution.md`,
and `docs/governance/operating-model.md`.

### 2. Governance rigor

ReproGate is stronger on:

- non-negotiable goals
- fail-closed rules
- documented framework/adapter boundaries
- PR-body validation
- mandatory doc coupling for implementation-surface changes

GSD preserves execution history well, but ReproGate is better positioned to prove compliance.

### 3. Framework/adaptor separation

ReproGate explicitly distinguishes portable framework assets from project-owned adapters.
This is a major architectural advantage.

By contrast, the current repository already shows a fragility point around GSD: the vendored
payload is duplicated across `.github/`, `.claude/`, `.codex/`, and `.gemini/`.
That duplication is already flagged in `.planning/codebase/CONCERNS.md` as a maintenance risk.

## Key Integration Insight

The cleanest model is:

> **GSD orchestrates work. ReproGate governs and verifies work.**

More concretely:

- GSD can decide **what happens next**
- GSD can capture **phase-local context and execution traces**
- ReproGate should decide **what evidence is mandatory**
- ReproGate should enforce **what must be true before work is considered valid**

This prevents a design trap where ReproGate slowly becomes "a clone of GSD with more rules."
That would weaken its identity.

## Harness-Agnostic Layered-Harness Feasibility

### Short verdict

**Yes — this is realistic, and strategically stronger than hard-binding ReproGate to GSD.**

But it is realistic only if ReproGate is designed as:

- a **harness-agnostic artifact contract**,
- a **policy/gate layer**,
- and a **thin adapter surface** over whichever workflow system is currently in use.

It becomes much harder if ReproGate tries to be:

- a universal orchestrator,
- a perfect semantic superset of every harness,
- or a round-trip translator that makes GSD, Kiro-style SDD, and freeform chat all behave identically.

### Feasibility assessment by dimension

| Dimension | Feasibility | Why |
|---|---|---|
| Enterprise-grade artifact guarantees across tools | High | The guarantee can live in canonical records and gates rather than in any one harness |
| Supporting multiple entry modes | Medium-High | "Forced workflow" and "derive workflow from conversation" can coexist if both normalize into the same evidence contract |
| Deriving workflow from general conversation | Medium | Feasible with extraction + confirmation checkpoints, risky if made fully automatic |
| Supporting multiple harnesses over time | Medium-High | Practical if adapters map into one canonical model; expensive if each harness gets bespoke logic everywhere |
| Long-term maintainability | Medium | Good with one canonical schema and generated adapters; bad if vendor/harness duplication spreads |
| Full cross-harness behavioral equivalence | Low | Different harnesses have different native abstractions, so exact parity is the wrong goal |

### What makes it feasible

#### 1. Make the artifact contract canonical

The stable center should not be:

- GSD `STATE.md`
- Kiro-style SDD stages
- chat transcripts
- any tool-specific workflow object

The stable center should be ReproGate-owned artifacts such as:

- intent/scope record
- decision record
- design/spec reference
- execution evidence
- verification evidence
- Skill/rule bindings
- traceability index

Then every harness becomes just another way of producing or enriching those artifacts.

#### 2. Treat harnesses as ingress adapters

A practical model is:

- **GSD adapter** — reads phase/context/plan/summary style artifacts
- **SDD adapter** — reads spec/design/task style artifacts
- **Conversation adapter** — extracts candidate intent/scope/decision artifacts from ordinary chat

All three should normalize into ReproGate's canonical evidence model before gates decide anything important.

#### 3. Separate "workflow help" from "governance truth"

This is the most important architectural rule.

Harnesses help users move.
ReproGate decides whether the move is acceptable.

That means:

- harness state may guide UX
- harness artifacts may provide useful evidence
- but final gate logic should read **canonical ReproGate evidence contracts**

This is what preserves tool independence.

#### 4. Use convergence, not uniformity

The goal should not be:

> "Make every harness look identical."

The goal should be:

> "Allow different harnesses to start differently, but force them to converge on the same required evidence before implementation, merge, or release."

That is much more realistic.

### Where it gets hard

#### 1. Freeform conversation extraction is lossy

If a user starts in ordinary chat, the system can usually infer:

- goal,
- rough scope,
- some decisions,
- maybe next steps

But it cannot safely infer all enterprise-grade evidence without confirmation.

So a realistic design is:

- extract draft artifacts,
- show them back,
- require confirmation before they become gateable evidence.

#### 2. Different harnesses slice work differently

Examples:

- GSD thinks in project → phase → plan → summary → verification
- SDD-style systems think in problem → spec → design → tasks → validation
- ad-hoc chat often thinks in issue → discussion → patch → test

If ReproGate tries to preserve every native abstraction exactly, complexity spikes fast.

The safer path is to map only what matters for governance:

- intent
- scope
- decisions
- implementation evidence
- verification evidence

#### 3. Adapter explosion is a real risk

The current repository already shows the pain of duplicated vendor payloads.

A harness-agnostic design only stays sane if:

- one canonical schema exists,
- adapter behavior is generated or centralized,
- and harness-specific logic stays thin.

Otherwise "tool-agnostic" turns into "many copies of almost-the-same system."

### Recommended architecture for this direction

#### Layer 1 — Canonical ReproGate Core

Owns:

- artifact schemas
- Skill/rule model
- gate evaluation
- traceability requirements
- CI / hook / PR enforcement

This is the non-negotiable center.

#### Layer 2 — Harness Adapters

Per-harness translators that can:

- detect existing harness artifacts
- scaffold missing ReproGate records
- translate harness-local outputs into canonical evidence
- surface missing evidence back to the user

Examples:

- `adapter-gsd`
- `adapter-sdd`
- `adapter-chat`

#### Layer 3 — Optional Orchestration Surfaces

These can remain tool-specific:

- GSD command surface
- MCP tool/resource surface
- IDE assistant flows
- future enterprise workflow surfaces

These layers are replaceable.
Layer 1 should not be.

### Enterprise viability

This direction is especially viable for enterprise use because enterprises usually care more about:

- evidence,
- auditability,
- policy consistency,
- reviewability,
- and explainable compliance

than about which harness initiated the work.

That means a decorator/layered-harness strategy is actually a better enterprise story than a GSD-bound product,
provided ReproGate clearly defines:

- what evidence is required,
- who/what may generate it,
- what must be human-confirmed,
- and what gates inspect before promotion.

### Practical recommendation

The best product bet is:

> **ReproGate as a harness-agnostic governance layer with optional harness adapters.**

Concretely:

- allow GSD today,
- allow other harnesses later,
- allow freeform conversation as an ingress path,
- but require all paths to converge on ReproGate evidence contracts before gated transitions.

### What not to promise

Do **not** promise:

- perfect automatic workflow derivation from arbitrary chat,
- full semantic parity across all harnesses,
- or zero-cost support for every tool ecosystem.

Instead promise:

- consistent evidence requirements,
- harness-independent gates,
- and adapter-based interoperability.

## Recommended Reference Posture by Phase

### Phase 1 — Foundation & Governance

Recommended reference posture: **selective borrowing, no wholesale adoption**

Adopt from GSD:

- command ergonomics and lifecycle naming
- richer artifact templates for implementation work
- helper-CLI pattern for reading/updating planning artifacts

Do not adopt as-is:

- GSD `STATE.md` as the authoritative truth model
- GSD workflow files as a substitute for ReproGate records or ADRs
- manual multi-surface vendoring as the long-term architecture

Phase 1 deliverable recommendation:

- create a durable decision record clarifying ReproGate's relationship to GSD
- define which GSD artifacts count as acceptable ReproGate evidence
- define which evidence still requires ADR/RFC or Skill/rule backing

### Phase 2 — MCP Integration

Recommended reference posture: **bridge, do not blend**

Expose through MCP:

- ReproGate canonical docs and records as the governance namespace
- optionally, GSD planning artifacts as an execution namespace when present

Important rule:

- clients should be able to distinguish **canonical governance evidence** from **workflow-local execution artifacts**

### Phase 3 — Harness-Agnostic Workflow Automation

Recommended reference posture: **adapter architecture**

This is the phase where GSD should be explicitly referenced as a design input.

Recommended shape:

- treat GSD as the orchestration shell
- insert ReproGate gates before/after major transitions
- map GSD artifacts to ReproGate checks

Example mapping:

- `CONTEXT.md` → acceptable design-intent evidence for planning
- `PLAN.md` → acceptable execution-intent evidence
- `SUMMARY.md` / `VERIFICATION.md` → acceptable completion evidence
- `STATE.md` → operational resume context only
- ADR/RFC + Skills/rules → governance authority

### Phase 4 — HUD

Recommended reference posture: **dual-surface visibility**

The HUD should show both:

- **GSD execution state**: current phase, plan progress, blockers, next step
- **ReproGate governance state**: required records present, gate status, verification status, missing evidence

That pairing turns GSD's operational visibility into something governance-safe.

## Anti-Patterns to Avoid

### 1. Treating GSD state as product truth

`STATE.md` is useful, but it is mutable operational context.
ReproGate should not make mutable state files the sole basis for compliance decisions.

### 2. Replacing ADR/RFC discipline with phase-local notes

`CONTEXT.md`, `DISCUSSION-LOG.md`, and `SUMMARY.md` are useful execution artifacts.
They do not replace long-lived decision records.

### 3. Copying GSD's vendored-tree duplication model

This repo already carries the cost of four mirrored GSD payloads.
Future integration should move toward one canonical source and generated adapter outputs.

### 4. Allowing orchestration success to imply governance success

GSD can complete a workflow and still leave governance gaps.
ReproGate must keep deterministic gate checks independent from orchestration status.

### 5. Blurring "workflow aid" and "evidence contract"

Some GSD artifacts are helpful for humans but should not automatically count as required evidence unless
ReproGate explicitly adopts them as inspectable contract surfaces.

## Concrete Recommendations

### Immediate

1. Record that the comparison is now complete in planning artifacts.
2. Use this document as a canonical reference during Phase 1 discussion.
3. Add a future ADR or design doc that answers:
   - Is GSD an embedded dependency, a reference model, or both?
   - Which GSD artifacts become first-class ReproGate evidence?
   - Which remain optional execution helpers?

### Near-term

1. Design a translation layer from GSD artifacts to ReproGate gates.
2. Define a small compatibility surface instead of importing all of GSD's state model.
3. Normalize vendored GSD content so one source tree is canonical and the other adapter copies are generated.

### Long-term

1. Let ReproGate govern any orchestrator, not only GSD.
2. Keep the product identity centered on records/Skills/rules.
3. Treat GSD as the first major orchestration backend that ReproGate can supervise.

## Recommended Canonical References for Follow-on Work

### ReproGate core identity

- `docs/strategy/final-definition.md` — defines ReproGate as an artifact-driven compiler/gatekeeper, not a heavy state orchestrator
- `docs/governance/constitution.md` — defines non-negotiable traceability and fail-closed enforcement principles
- `docs/governance/operating-model.md` — defines record-backed engineering as the operating norm

### Current ReproGate implementation

- `scripts/cli.py` — current CLI surface
- `scripts/init.py` — initial config bootstrap
- `scripts/generate.py` — framework copy/render workflow
- `scripts/gatekeeper.py` — current enforcement implementation
- `skills/record-required/guidelines.md` and `skills/record-required/rules.rego` — representative Skill + rule pairing

### GSD runtime and workflow model

- `.github/get-shit-done/bin/gsd-tools.cjs` — operational CLI surface
- `.github/get-shit-done/bin/lib/init.cjs` — workflow initialization payloads
- `.github/get-shit-done/bin/lib/state.cjs` — state progression logic
- `.github/get-shit-done/bin/lib/roadmap.cjs` — roadmap parsing and disk-state analysis
- `.github/get-shit-done/bin/lib/template.cjs` — template fill operations
- `.github/get-shit-done/bin/lib/config.cjs` — planning/workflow config model
- `.github/get-shit-done/workflows/new-project.md` — project bootstrap orchestration
- `.github/get-shit-done/workflows/discuss-phase.md` — context capture orchestration
- `.github/get-shit-done/workflows/plan-phase.md` — research/plan/check orchestration
- `.github/get-shit-done/workflows/execute-phase.md` — phase execution orchestration
- `.github/get-shit-done/templates/project.md` — project context artifact
- `.github/get-shit-done/templates/requirements.md` — requirements artifact
- `.github/get-shit-done/templates/roadmap.md` — roadmap artifact
- `.github/get-shit-done/templates/state.md` — operational state artifact
- `.github/get-shit-done/templates/discussion-log.md` — audit-only execution artifact
- `.github/get-shit-done/references/planning-config.md` — planning/git config and branching model
- `.github/get-shit-done/references/checkpoints.md` — human verification and decision checkpoint model
- `.github/get-shit-done/references/git-planning-commit.md` — planning-doc git history conventions

---

*Comparison completed: 2026-03-24*  
*Suggested use: Phase 1 context + Phase 3 architecture input*
