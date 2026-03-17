# ReproGate Docs

This directory contains the living documents for ReproGate.

The canonical product definition is:

1. `docs/strategy/final-definition.md`

## Read Order for a Fresh Session

1. `docs/strategy/final-definition.md`
2. `docs/strategy/vision.md`
3. `docs/strategy/roadmap.md`
4. `docs/guide/why-dpc.md`
5. `docs/governance/operating-model.md`

## Included Sections

- `process-catalog/` — process definitions and selection guidance
- `tool-hooks/` — tool-specific enforcement guidance
- `commands/` — named entrypoint and command references
- `portability/` — boundaries between framework, adapters, and local runtime
- `omc-config/` — optional OMC policy templates
- `strategy/` — canonical definition, vision, and roadmap
- `guide/` — positioning and adoption guidance

## Portability Notes

- These docs describe a record-backed methodology compiler and gatekeeper, not a chat-memory utility.
- ReproGate focuses on work records, Skill accumulation, and gate enforcement; runtime state alone is not treated as sufficient evidence.
- These docs are framework-owned and reusable across repositories.
- Generated project adapters may point at project-specific work packet and ADR locations through `dpc.config.yaml`.
- Hidden runtime directories such as `.claude/`, `.codex/`, `.omc/`, and `.omx/` remain local-only unless a generated adapter file explicitly belongs there.
