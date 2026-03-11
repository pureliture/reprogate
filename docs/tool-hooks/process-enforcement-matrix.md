# Process Enforcement Matrix

> Status: Active
> Version: `1.0.0`

## Purpose

This matrix defines the minimum enforcement behavior that adapters should apply once a process has been selected.
It also preserves logical-role separation for team-capable work.

## Shared Rules

1. Process selection happens before execution.
2. The adapter records the selected process in durable context.
3. Team-capable processes resolve `team` or `single` before implementation starts.
4. Single fallback still keeps the required logical-role responsibilities.
5. Final repository-boundary checks remain separate from runtime guidance.

## Minimum Logical-Role Profiles

| Profile ID | Required Roles |
|---|---|
| `ANALYSIS_MIN2` | `analyst`, `verifier` |
| `DELIVERY_MIN3` | `executor`, `verifier`, `recorder` |
| `REVIEW_MIN2` | `reviewer`, `verifier` |
| `DOC_MIN2` | `recorder`, `verifier` |
| `SINGLE_MIN1` | `executor` |

Reference: [Minimum Logical Role Set](../process-catalog/minimum-logical-role-set.md)

## Process Matrix

| Process | Default Profile | Team-Capable | Minimum Enforcement |
|---|---|---|---|
| `G0` | `ANALYSIS_MIN2` | no | read and align only |
| `P0` | `ANALYSIS_MIN2` | no | analyze current state before changes |
| `P1` | `ANALYSIS_MIN2` | no | refine requirements before delivery |
| `P2` | `ANALYSIS_MIN2` | no | define troubleshooting path before fixes |
| `P3` | `DELIVERY_MIN3` | yes | resolve execution mode before implementation |
| `P4` | `DELIVERY_MIN3` | yes | resolve execution mode before bug-fix work |
| `S1` | `REVIEW_MIN2` | conditional | follow adapter review path |
| `S2` | `DOC_MIN2` | no | update documentation and verify it |
| `S3` | `DELIVERY_MIN3` | yes | resolve execution mode before refactoring |
| `S4` | `DOC_MIN2` | no | record change intent and outcome |
| `NONE` | `SINGLE_MIN1` | no | general work outside process enforcement |

## Enforcement Surfaces

| Surface | Responsibility |
|---|---|
| entry command | process recommendation and user choice |
| runtime hook | allow, warn, or deny based on active process |
| context store | preserve selected process and execution path |
| final gate | reject non-compliant repository changes |

## Portability Boundary

This matrix defines framework expectations only.
Adapters own concrete file paths, launch wrappers, hook registration steps, and repository-specific policies.
