# Process Selection Guide

> Status: Active
> Purpose: choose the right process before starting work

## Purpose

Select the most appropriate process before execution begins.
Do not skip process selection unless the operating mode explicitly allows a no-process path.

## Selection Matrix

| Situation | Recommended Process | Why |
|---|---|---|
| Need to understand existing behavior first | `P0` | analysis before change |
| Request is vague or underspecified | `P1` | clarify scope and done criteria |
| A problem exists but root cause is unclear | `P2` | define hypotheses and checks |
| Implementation scope is ready | `P3` | deliver new functionality |
| Bug-fix direction is ready | `P4` | correct defects and verify |
| Output needs validation | `S1` | review for gaps and side effects |
| Documentation must be updated | `S2` | refresh affected docs |
| Structure needs cleanup | `S3` | refactor safely |
| Decisions and history must be preserved | `S4` | record the change |
| Process flow is intentionally skipped | `NONE` | general single-agent path |

## Selection Rules

1. Start with `G0`.
2. Favor `P0` when existing code or behavior must be understood.
3. Favor `P1` when scope or expectations are ambiguous.
4. Favor `P2` when debugging without a stable theory would be risky.
5. Connect implementation work to `S1`, `S2`, and `S4` when appropriate.
6. Consider `S3` after large or messy changes.

## User-Facing Selection Prompt

```text
Recommended process: <ID> (<brief reason>)
Alternatives: <ID>, <ID>

Choose the process to apply.
- G0/P0/P1/P2/P3/P4/S1/S2/S3/S4
- NONE
```

## Process Contract

Every selected process should define:

- inputs,
- execution steps,
- required deliverables,
- exit criteria,
- and likely next processes.

## Role Profile Check

When the process is chosen, confirm its minimum logical-role profile.
See [minimum-logical-role-set.md](./minimum-logical-role-set.md).
