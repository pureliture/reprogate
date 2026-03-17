# AI Ops Roadmap

## Current Stage

AI Ops is now at the point where:

- the framework surface exists as an independent repository
- the repository can bootstrap a self-contained target project
- the external repository can serve as the canonical workspace for future framework work

## Near-Term Priorities

### 1. Public-facing strategy layer

Add the missing strategy documents that explain:

- why AI Ops exists
- who it is for
- what it will and will not try to become

Planned outputs:

- `docs/vision.md`
- `docs/roadmap.md`
- `docs/why-ai-ops.md`

### 2. Canonical external control-board maturity

Harden the external repository as the only live control-board for framework work.

Focus areas:

- keep work packets and ADRs current in the external repo
- keep adapter and workspace surfaces aligned with the control-board
- reduce remaining dependence on source-of-origin archive context

### 3. Public release readiness

Before broad publication:

- confirm branch strategy
- keep bootstrap smoke tests green
- document maintainer expectations
- decide how much archive material remains public-facing versus maintainer-only

## Mid-Term Direction

### AI Ops Lite

Define a lighter entry path for teams or individuals that do not want the full framework surface on day one.

Expected characteristics:

- fewer processes
- fewer required artifacts
- smaller adapter footprint
- lower adoption friction

### Stronger adapter surfaces

Improve first-class support for:

- Codex and OMX
- Claude and OMC
- future toolchains through the same framework boundary model

## Longer-Term Direction

### Team operating standard

AI Ops should become usable as a shared team operating standard rather than only a solo workflow.

This requires:

- reusable records
- predictable review points
- explicit extension rules
- stable framework semantics across repositories

### Optional integrations

Once the framework core is stable, AI Ops may grow optional integrations with:

- external knowledge systems
- pipelines
- approval systems
- shared reporting or audit layers

Those are downstream integrations, not the current center of gravity.

## Non-Roadmap Warning

AI Ops should not expand by chasing every tool feature. The roadmap should stay anchored to the framework's core promise:

- preserve intent
- structure work
- enforce completion discipline
