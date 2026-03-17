# ReproGate Vision

## Summary

> **작업 기록을 기반으로 AI 협업을 재현 가능한 엔지니어링 체계로 바꾸는 방법론 컴파일러이자 Gatekeeper**

## Tagline

> **AI 협업을 대화 기반 감각 작업에서 재현 가능한 엔지니어링 체계로**

## Purpose

ReproGate exists to make AI-assisted work reproducible, explainable, and enforceable through work records.

Its long-term vision is not to become a chat-memory product or a heavy state orchestrator. It is to become the stable layer that teams keep while models, IDEs, shells, and runtimes keep changing.

## Core Thesis

AI coding has three structural failure modes:

1. context loss
2. decisions that are hard to explain later
3. skipped supporting work because nothing concrete proves they happened

ReproGate addresses those failures by moving AI work onto record-backed artifacts:

- **Work records**: intent, scope, decisions, and verification are preserved as inspectable artifacts
- **Skill accumulation**: repeated good patterns become durable Skills instead of vanishing into prior chats
- **Gate enforcement**: rules inspect records and outputs, then block work that violates the expected pattern

The key insight: memory-based AI coding cannot be enforced, but record-based AI engineering can. Gates need evidence. Work records provide that evidence.

```
┌─────────────────────────────────────────────────────────────┐
│  Chat / Memory-Only AI Coding                                │
│  → fragile, hard to explain, easy to skip supporting work    │
├─────────────────────────────────────────────────────────────┤
│  Work Records + Skills + Gates                               │
│  → intent is recorded, patterns accumulate, gates can enforce│
├─────────────────────────────────────────────────────────────┤
│  ReproGate                                                   │
│  → reproducible AI engineering                               │
└─────────────────────────────────────────────────────────────┘
```

## What Success Looks Like

A team using ReproGate should be able to:

- restart work after context loss without losing intent
- inspect why a design changed course or where a workflow drift began
- convert repeated lessons into durable Skills and enforcement rules
- move between toolchains without rebuilding the same operating discipline from scratch
- share a stronger team standard without relying on everyone to remember it manually

## Long-Term Direction

The long-term direction is a portable framework with:

- framework-owned definitions for work records, Skills, and gates
- repository-local adapters generated from configuration
- team-shareable standards built from accumulated patterns
- optional integrations only after the core record-and-gate surface is stable

## Design Commitments

- record-first, not memory-first
- artifact-driven enforcement over hidden state tracking
- framework and adapter separation
- tool independence over vendor lock-in
- verification before completion claims
