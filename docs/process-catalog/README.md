# AI Ops Process Catalog

> Status: Active
> Version: `1.0.0`

## Overview

This directory defines the standard AI Ops processes.
Execution should begin by choosing the right process and then following its inputs, steps, deliverables, exit criteria, and next-process guidance.

## Document Structure

| Document | Purpose |
|---|---|
| [session-start-protocol.md](./session-start-protocol.md) | Required startup routine for a new AI session |
| [process-selection-guide.md](./process-selection-guide.md) | How to choose the right process |
| [G0-goal-alignment.md](./G0-goal-alignment.md) | Goal-alignment checkpoint before work starts |
| [P0-P4-core-processes.md](./P0-P4-core-processes.md) | Core delivery processes |
| [S1-S4-support-processes.md](./S1-S4-support-processes.md) | Review, documentation, refactoring, and recording processes |
| [minimum-logical-role-set.md](./minimum-logical-role-set.md) | Minimum logical-role profiles for delivery safety |

## Process Summary

| ID | Name | Purpose | Typical Next |
|---|---|---|---|
| `G0` | Goal alignment | Confirm that the work matches higher-level goals | `P0`-`P4`, `S1`-`S4` |
| `P0` | Existing-state analysis | Understand structure, behavior, and impact area | `P1`, `P2`, `P3`, `P4`, `S3` |
| `P1` | Requirement refinement | Turn vague requests into implementable scope | `P3`, `P4` |
| `P2` | Troubleshooting strategy | Define root-cause hypotheses and resolution paths | `P4` |
| `P3` | Feature delivery | Implement new functionality or structural change | `S1`, `S2`, `S3`, `S4` |
| `P4` | Bug-fix delivery | Correct defects and prevent regression | `S1`, `S2`, `S4` |
| `S1` | Work review | Validate completeness and detect gaps | `S2`, `S3`, `S4`, `P3`, `P4` |
| `S2` | Documentation refresh | Update affected documentation | `S4` |
| `S3` | Refactoring | Improve structure while preserving intent | `S1`, `S2`, `S4` |
| `S4` | Change recording | Preserve what changed and why | end or follow-up work |

## Shared Operating Rules

1. Start with process selection instead of immediate execution.
2. Prefer file-backed artifacts over chat-only memory.
3. Treat verification and recording as part of delivery.
4. Check documentation impact for major changes.
5. Connect each process to an explicit next step when possible.
6. Keep the catalog tool-agnostic.

## Typical Process Chains

- `G0 -> P0 -> P1 -> P3 -> S1 -> S2 -> S4`
- `G0 -> P0 -> P2 -> P4 -> S1 -> S2 -> S4`
- `G0 -> P1 -> P3 -> S1 -> S3 -> S2 -> S4`
- `G0 -> P0 -> S3 -> S1 -> S2 -> S4`

## Related Documents

- [Constitution](../constitution.md)
- [Operating Model](../operating-model.md)
