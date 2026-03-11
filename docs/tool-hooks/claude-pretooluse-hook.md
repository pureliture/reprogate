# Pre-Execution Hook Model

> Status: Active
> Version: `1.0.0`

## Purpose

Some AI tools support a hook immediately before a tool call or file mutation.
This document defines the portable AI Ops model for that kind of guard.

## When It Runs

A pre-execution hook runs before the tool performs a state-changing action such as:

- file creation,
- file edits,
- command execution,
- or multi-step mutation tools.

## What It Should Check

A conforming hook should validate:

1. whether a process has been selected,
2. whether the active process allows the requested action,
3. whether team-capable work has resolved `team` or `single`,
4. whether the required logical-role profile is satisfied,
5. and whether final compliance prerequisites are obviously missing.

## Expected Outcomes

| Result | Meaning |
|---|---|
| allow | the action matches the current process state |
| warn | the action is risky but not forbidden by the adapter |
| deny | the action violates process enforcement |

## Typical Deny Cases

- implementation work begins before process selection,
- implementation starts while a team-capable process is still undecided,
- required role separation is missing,
- or an adapter-defined protected boundary would be violated.

## Adapter Responsibilities

Adapter docs should define:

- the concrete hook registration method,
- the action classes that trigger the hook,
- the context file or store that the hook reads,
- and the denial message shape shown to users.
