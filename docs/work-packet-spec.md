# Work Packet Specification

Work packets are the durable delivery records for AI Ops work.

## Required Frontmatter Fields

Every work packet should include:

- `packet_id`
- `title`
- `status`
- `work_type`
- `priority`
- `target_environment`
- `start_process`
- `current_process`
- `next_process`
- `owner`
- `created_at`
- `last_updated`

If the repository uses AI Ops program goals, also include:

- `goal_ids`

## Recommended Sections

1. Background
2. Goal
3. Scope
4. Out of Scope
5. Done Criteria
6. Risks / Constraints
7. Related References
8. Process Plan
9. Execution Notes
10. Deliverables
11. Review Notes
12. Decisions
13. Follow-ups
14. Timeline

## Status Model

Recommended status values:

- `DRAFT`
- `READY`
- `IN_ANALYSIS`
- `IN_REFINEMENT`
- `IN_TROUBLESHOOTING`
- `IN_DEVELOPMENT`
- `IN_REFACTORING`
- `IN_REVIEW`
- `IN_DOCUMENTATION`
- `IN_RECORDING`
- `BLOCKED`
- `ON_HOLD`
- `DONE`
- `CANCELLED`

## Naming Guidance

- Framework packets: `WP-AIOPS-YYYY-MM-NNN-short-title.md`
- Project packets: `WP-YYYY-MM-NNN-short-title.md`

## Minimal Template

```markdown
---
packet_id: "[Packet ID]"
title: "[Title]"
status: "[Status]"
work_type: "[Work Type]"
priority: "[Priority]"
target_environment: "[environment]"
start_process: "[Process]"
current_process: "[Process]"
next_process: "[Process]"
owner: "[Owner]"
created_at: "[YYYY-MM-DD]"
last_updated: "[YYYY-MM-DD]"
---
# [Packet ID] [Title]

## 1. Background
## 2. Goal
## 3. Scope
## 4. Out of Scope
## 5. Done Criteria
## 6. Risks / Constraints
## 7. Related References
## 8. Process Plan
## 9. Execution Notes
## 10. Deliverables
## 11. Review Notes
## 12. Decisions
## 13. Follow-ups
## 14. Timeline
```
