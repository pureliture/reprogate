# ReproGate Roadmap

## Current Stage

ReproGate has pivoted from a methodology compiler/gatekeeper to a **Claude Code-centered, artifact-driven delivery harness** ([ADR-009](../../records/adr/ADR-009-reprogate-harness-pivot.md)).

The foundation layer is complete:

- CLI (`cli.py`), record management, gatekeeper, and skills infrastructure are working
- Pre-commit gate enforcement is active
- Strategy documents are being aligned to the new harness identity

The next cycle builds the harness runtime on top of this foundation.

## v1.0 Priorities

The v1.0 milestone delivers a single-developer delivery harness integrating ECC-style operating primitives with GSD-style phase workflow. Six phases, executed in order (see `.planning/ROADMAP.md` for implementation detail):

### 1. Harness Bootstrap

`reprogate init/disable` commands and settings injection. A developer can install, configure, and deactivate the harness with a single command.

### 2. Hook Lifecycle

ECC-style session, compact, tool-use, and failure hooks. The harness automatically captures state, governance events, and gate failures through the hook lifecycle.

### 3. Skill Evolution

Structured observation → instinct → prose skill pipeline. Session observations are progressively refined into reusable, enforceable skills.

### 4. Specialist Agents

Executor, verifier, and planner agents running as Claude Code sub-processes with clear input/output contracts.

### 5. Phase Workflow

`discuss → plan → execute → verify` slash commands with phase artifact packets. The full development cycle is driven through `/rg:*` commands.

### 6. Artifact Lifecycle

Phase summary generation for sharing and harness health checks for operational awareness.

## Mid-Term Direction (v2)

Once the v1.0 harness is stable, expansion focuses on automation, visibility, and integration:

- **Skill evolution automation** — automated prose-to-rego conversion (`evolve-to-rego`)
- **Terminal HUD** — real-time gate status and phase progress visibility
- **MCP server** — expose records and skills as resources to external AI agents
- **Deep search integration** — `reprogate search` backed by structured document indexing
- **Team-scale skill sharing** — remote policy synchronization across repositories

These are deferred to v2 to keep v1.0 focused on the core harness loop.

## Longer-Term Direction

### Team operating standard

ReproGate should become usable as a shared team operating standard:

- reusable work records with predictable gate points
- explicit skill extension and sharing rules
- stable semantics across repositories and teams

### Multi-runtime potential

The harness architecture should remain open to:

- MCP-based integration with non-Claude runtimes
- multi-agent orchestration beyond the current CC sub-process model
- enterprise audit and compliance surface extensions

These are architectural options, not committed work.

## Non-Roadmap Warning

ReproGate should not expand by chasing features outside the harness delivery loop. The roadmap stays anchored to:

- hook-driven state capture and governance
- structured skill evolution from session observations
- artifact-backed phase workflow with specialist agents
- inspectable gates at every stage
