# ReproGate Roadmap

## Current Stage

ReproGate is now at the point where:

- the framework surface exists as an independent repository
- the repository can bootstrap a self-contained target project
- the canonical definition exists in `docs/strategy/final-definition.md`
- the remaining work is to align the rest of the living docs and implementation surface to that definition

## Near-Term Priorities

### 1. Canonical definition injection

Inject the final definition into the living documentation surface so the product reads consistently everywhere.

Focus areas:

- README and strategy docs
- governance and master-plan docs
- design and implementation planning docs
- historical alignment notes where needed

### 2. Record-backed core implementation

Harden the core around the final ReproGate thesis:

Focus areas:

- work records as mandatory artifacts
- Skill accumulation as a first-class product concept
- Rego-based gate enforcement
- artifact-driven workflow instead of heavy state tracking

### 3. ReproGate identity transition

Complete the outward transition from legacy `dpc` wording to ReproGate while preserving historical IDs where needed.

Focus areas:

- product-facing naming updates
- clear explanation of legacy `dpc` identifiers in code and records
- docs and package surface consistency

## Mid-Term Direction

### Lightweight adoption path

Define a lighter path for teams or individuals that want record-backed enforcement without the full surrounding framework surface on day one.

Expected characteristics:

- fewer default records
- fewer default Skills
- smaller adapter footprint
- lower adoption friction

### Stronger adapter surfaces

Improve first-class support for:

- Codex and OMX
- Claude and OMC
- future toolchains through the same record-and-gate boundary model

## Longer-Term Direction

### Team operating standard

ReproGate should become usable as a shared team operating standard rather than only a solo workflow.

This requires:

- reusable work records
- predictable gate points
- explicit Skill extension rules
- stable semantics across repositories

### Optional integrations

Once the framework core is stable, ReproGate may grow optional integrations with:

- external knowledge systems
- pipelines
- approval systems
- shared reporting or audit layers

Those are downstream integrations, not the current center of gravity.

## Non-Roadmap Warning

ReproGate should not expand by chasing every tool feature. The roadmap should stay anchored to the product's core promise:

- make work records mandatory
- turn repeated patterns into durable Skills
- enforce those patterns through inspectable gates
