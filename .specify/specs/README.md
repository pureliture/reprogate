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

1. Create `<feature-slug>/spec.md` when starting a feature
2. Add `plan.md` after spec approval
3. Add `tasks.md` for execution tracking
4. After completion, record durable decisions in `records/adr/` if needed
5. Post-merge retention or archival policy is determined by repository workflow rules in later phases

## Notes

- These are **working documents**, not canonical specifications
- Product definitions belong in `docs/spec/` or `docs/design/`
- Architectural decisions belong in `records/adr/`
