# ReproGate Entry Command Contract (`dpc` Legacy Alias)

> Status: Active
> Version: `1.0.0`

## Purpose

The ReproGate entry command (often exposed as `dpc` for backward compatibility) is the process-first entrypoint for framework-guided work.
Its job is to prevent immediate execution before the work is classified.

## Required Behavior

An adapter that exposes this entry command should enforce this sequence:

1. receive a task description,
2. recommend one process and one or two alternatives,
3. ask the user to choose a process or `NONE`,
4. wait for that choice before execution,
5. record the selected process in the adapter's context mechanism,
6. continue with the chosen process rules.

## Required User Choice

The command should present these selectable process IDs:

- `P0`, `P1`, `P2`, `P3`, `P4`
- `S1`, `S2`, `S3`, `S4`
- `NONE`

`NONE` means the user declines process enforcement for the current task.
In that case, the adapter may proceed with general work, but it should still note the opt-out and may suggest a follow-up process before the task closes.

## Team Activation Rule

The entry command must not start team execution before both conditions are true:

1. the user selected a process,
2. the selected process allows team execution.

By default, the framework treats these processes as team-capable:

- `P3`
- `P4`
- `S3`
- `S1` when the adapter explicitly supports it

All other processes default to single-path execution.

## Team-Capable Process Rule

For a team-capable process, the adapter should resolve execution mode before implementation starts:

- `team`
- `single`

If the adapter falls back to `single`, one worker still retains the required logical-role responsibilities in sequence.
See [Minimum Logical Role Set](../process-catalog/minimum-logical-role-set.md).

## Output Contract

A conforming ReproGate entry command should leave these outcomes:

1. a chosen process or `NONE`,
2. a stated execution path,
3. a durable context record in adapter-owned storage,
4. a clear next step.

## Portability Rules

Core command docs should stay tool-agnostic.
Keep these concerns out of this document:

- repository-specific paths,
- internal packet IDs,
- product changelog rules,
- branch naming policies,
- runtime-version exceptions,
- and vendor-specific command wrappers.

Those belong in adapter-owned docs.

## Related Documents

- [Process Catalog](../process-catalog/README.md)
- [Tool Hooks](../tool-hooks/README.md)
