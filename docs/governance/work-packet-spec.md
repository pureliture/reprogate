# Work Packet Specification

Work packets are one kind of durable work record for ReproGate work.
They are planning and execution artifacts, distinct from transient runtime state.

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

If the repository uses program goals, also include:

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

## Role in the ReproGate Model

A work packet does not replace every form of record.
It specifically captures delivery intent, scope, status, and execution planning so that later Skills, gates, decisions, and verification can be explained against a durable artifact.

Use work packets when the work needs:

- explicit scope control
- traceable status and next steps
- linkage to decisions and changelog entries
- a durable record that outlives session memory

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

- Framework packets: `WP-DPC-YYYY-MM-NNN-short-title.md`
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
