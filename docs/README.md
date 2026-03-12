# AI Ops Framework Docs

This directory contains the portable framework documents that describe the AI Ops operating model.

## Read Order for a Fresh Session

1. `docs/constitution.md`
2. `docs/operating-model.md`
3. `docs/process-catalog/README.md`
4. `docs/goal-alignment-checklist.md`
5. `docs/work-packet-spec.md`

## Included Sections

- `process-catalog/` — process definitions and selection guidance
- `tool-hooks/` — tool-specific enforcement guidance
- `commands/` — named entrypoint and command references
- `portability/` — boundaries between framework, adapters, and local runtime
- `omc-config/` — optional OMC policy templates
- strategy docs — `vision.md`, `roadmap.md`, `why-ai-ops.md`

## Portability Notes

- These docs are framework-owned and reusable across repositories.
- Generated project adapters may point at project-specific work packet and ADR locations through `ai-ops.config.yaml`.
- Hidden runtime directories such as `.claude/`, `.codex/`, `.omc/`, and `.omx/` remain local-only unless a generated adapter file explicitly belongs there.
