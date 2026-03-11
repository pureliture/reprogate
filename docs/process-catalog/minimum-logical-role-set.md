# Minimum Logical Role Set

> Status: Active
> Version: `1.0.0`

## Purpose

Process selection alone is not enough when verification and recording responsibilities can be skipped.
This document defines the minimum logical-role profiles that should remain stable across tools and team layouts.

## Role Separation Rules

1. Roles are defined by responsibility, not by tool capability.
2. Team execution should satisfy the minimum profile for the selected process.
3. Team execution should map each member to an explicit logical role.
4. For team-capable processes, implementation work should not start while team mode is still undecided.
5. Single fallback still retains the responsibilities of the required logical roles.

## Logical Roles

| Role | Core Responsibility | Risk If Missing |
|---|---|---|
| `analyst` | gather analysis, requirements, or root-cause findings | implementation without understanding |
| `executor` | perform implementation, fixes, or refactoring | execution gap |
| `verifier` | validate outputs, done criteria, and regression risk | verification gap |
| `recorder` | update packets, indexes, changelogs, or decision logs | traceability loss |
| `reviewer` | detect defects, risks, and maintainability issues | quality erosion |

## Minimum Profiles

| Profile ID | Required Roles | Use |
|---|---|---|
| `ANALYSIS_MIN2` | `analyst`, `verifier` | analysis, refinement, troubleshooting |
| `DELIVERY_MIN3` | `executor`, `verifier`, `recorder` | implementation plus verification and recording |
| `REVIEW_MIN2` | `reviewer`, `verifier` | review-heavy work |
| `DOC_MIN2` | `recorder`, `verifier` | documentation or record maintenance |
| `SINGLE_MIN1` | `executor` | general single-agent path |

## Process Mapping

| Process | Default Profile | Team-Capable |
|---|---|---|
| `G0` | `ANALYSIS_MIN2` | no |
| `P0` | `ANALYSIS_MIN2` | no |
| `P1` | `ANALYSIS_MIN2` | no |
| `P2` | `ANALYSIS_MIN2` | no |
| `P3` | `DELIVERY_MIN3` | yes |
| `P4` | `DELIVERY_MIN3` | yes |
| `S1` | `REVIEW_MIN2` | conditional |
| `S2` | `DOC_MIN2` | no |
| `S3` | `DELIVERY_MIN3` | yes |
| `S4` | `DOC_MIN2` | no |
| `NONE` | `SINGLE_MIN1` | no |

## Example Tool Mapping

Tool names vary, but the responsibilities should remain equivalent.

| Logical Role | Example Agent Types |
|---|---|
| `analyst` | explore, analyst, debugger |
| `executor` | executor, build-fixer |
| `verifier` | verifier, quality reviewer, code reviewer |
| `recorder` | writer |
| `reviewer` | code reviewer, security reviewer, quality reviewer |

## Example Context Commands

### Record process context

```bash
python3 scripts/set_process_context.py --process <PROCESS> --wp <WP-ID> --team-mode <auto|single|team>
```

### Team path

```bash
python3 scripts/set_process_context.py --process P3 --wp <WP-ID> --team-mode team --profile DELIVERY_MIN3 --roles executor,verifier,recorder --members member-a:executor,member-b:verifier,member-c:recorder
```

### Single fallback for a team-capable process

```bash
python3 scripts/set_process_context.py --process P3 --wp <WP-ID> --team-mode single
```

In single fallback, one worker still performs `executor -> verifier -> recorder` responsibilities sequentially.
