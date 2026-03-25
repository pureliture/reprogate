# Specs Directory Convention

This directory contains feature specifications organized by feature slug.

## Directory Structure

Each feature follows a directory-based convention:

```
.specify/specs/<feature-slug>/
├── spec.md     # Feature specification
├── plan.md     # Implementation plan
└── tasks.md    # Task breakdown
```

## File Roles

| File | Purpose |
|------|---------|
| `spec.md` | Feature requirements, scope, and acceptance criteria |
| `plan.md` | Implementation approach and design decisions |
| `tasks.md` | Granular task breakdown for execution |

## Naming Convention

- **Feature slug**: lowercase, hyphen-separated (e.g., `gate-engine`, `skill-registry`)
- **Files**: fixed names as shown above

## Lifecycle

> **Prerequisite:** The `record-required` gate requires an RFC or ADR under `records/` before meaningful implementation changes. Create the decision record first.

1. Create RFC/ADR in `records/` to satisfy gate requirements
2. Create `<feature-slug>/spec.md` when starting feature work
3. Add `plan.md` after spec approval
4. Add `tasks.md` for execution tracking
5. Post-merge retention or archival policy is determined by repository workflow rules in later phases

## Notes

- These are **working documents**, not canonical specifications
- Product definitions belong in `docs/spec/` or `docs/design/`
- Architectural decisions belong in `records/adr/`
