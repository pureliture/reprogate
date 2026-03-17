# Commands

> Status: Active
> Version: `1.0.0`

## Purpose

This directory defines portable command contracts for ReproGate entrypoints.
The documents here describe what an entry command must do, not how a specific tool implements it.

## Scope

Use this directory for:

- command intent,
- required decision flow,
- input and output contracts,
- adapter boundaries,
- and portability rules.

Do not place project-specific workspace rules, branch names, legacy runtime constraints, or delivery history here.
Those belong in adapter-owned assets.

## Documents

| Document | Purpose |
|---|---|
| [dpc.md](./dpc.md) | Portable process-first entrypoint contract (legacy command alias support) |
