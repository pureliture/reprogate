# Session-Entry Enforcement Model

> Status: Active
> Version: `1.0.0`

## Purpose

Some toolchains do not provide a hard pre-execution hook for every tool call.
In that case, AI Ops relies on session-entry guidance, durable context, and final repository gates.

## Core Model

A session-entry enforcement path should combine these layers:

1. startup instructions that point to AI Ops source documents,
2. a process-first entry command or equivalent prompt routine,
3. adapter-owned context recording,
4. execution-path resolution for team-capable processes,
5. and final compliance checks at repository boundaries.

## Required Behavior

A conforming adapter should:

1. direct the tool to the framework source documents at session start,
2. require process choice before team execution starts,
3. resolve `team` or `single` for team-capable processes before implementation work,
4. preserve evidence when single fallback carries multiple logical roles,
5. and run a final compliance gate before commit or equivalent publication.

## Soft Guarantee Chain

When no per-tool hard hook exists, adapters should still make the workflow hard to bypass by chaining:

- startup rules,
- process-entry workflow,
- context recording,
- execution summaries,
- and final repository checks.

## Adapter Boundary

The framework does not require a specific launcher, IDE integration, or local rule-pack format.
Those details belong in adapter-owned docs.
