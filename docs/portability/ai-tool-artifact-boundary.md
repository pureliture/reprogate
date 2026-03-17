# AI Tool Artifact Boundary

ReproGate separates reusable framework assets from project adapters and local runtime data.

## Artifact Classes

| Class | Purpose | Typical Location | Commit? |
| --- | --- | --- | --- |
| Framework | Reusable templates, schemas, framework docs | `docs/`, `scripts/`, `skills/`, `templates/` | Yes |
| Project Adapter | Project-specific entrypoints and record scaffolds | `AGENTS.md`, `.codex/`, `.claude/`, `dpc.config.yaml` | Yes |
| Local Runtime | Session state and local-only tool outputs | `.omc/`, `.omx/`, `.claude/settings.local.json` | No |

## Hard Rules

1. Do not treat hidden runtime state as the source of truth.
2. Do not push project-specific values back into the shared framework repository.
3. Keep generated adapters traceable to `dpc.config.yaml`.
4. If a generated file points to a framework doc or script, bootstrap that file into the target repository as part of generation.

## Porting Rule of Thumb

If a target repository should be able to run ReproGate without reading the source framework checkout, the generated output must include:

- the adapter files,
- the framework docs they reference,
- the scripts and hooks they invoke,
- and the record scaffolds implied by the configured paths.
