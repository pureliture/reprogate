# AI Ops Vision

## Tagline

> **"ai-ops는 개발 방법론을 LLM에게 이식해, LLM이 당신처럼 일하게 만든다"**
>
> ai-ops transplants your development methodology into LLMs, making them work like you do.

## Purpose

AI Ops exists to make AI-assisted engineering work reproducible, reviewable, and portable across tools.

Its long-term vision is not to become a single-vendor assistant feature. It is to become a stable operating layer that teams can keep even while models, IDEs, shells, and agent runtimes keep changing.

## Core Thesis

AI coding has three structural failure modes:

1. context loss
2. skipped supporting work
3. weak traceability

AI Ops addresses those failures by transplanting development methodology into LLMs:

- **Process definition**: Define how your team works once
- **Automatic records**: ai-ops generates WP, ADR, and change logs automatically
- **Enforcement**: Gates ensure the process is followed

The key insight: CI/CD manages output quality at the team/system level. AI Ops manages process quality at the individual developer level — the methodology each developer follows (TDD, documentation, design review) is now transplanted into LLMs.

```
┌─────────────────────────────────────────────────────────────┐
│  Team/System Level: CI/CD, code review, linters             │
│  → "Does the output meet standards?"                        │
├─────────────────────────────────────────────────────────────┤
│  Individual Developer Level: TDD, docs, design reviews      │
│  → "How does each developer work?"                          │
├─────────────────────────────────────────────────────────────┤
│  ai-ops: Transplants this methodology into LLMs             │
└─────────────────────────────────────────────────────────────┘
```

## What Success Looks Like

A team using AI Ops should be able to:

- restart work after context loss without losing intent
- keep work packets, decisions, and verification traces aligned with implementation
- move between toolchains without rewriting its operating model from scratch
- adopt stricter or lighter workflows without abandoning the same core framework

## Long-Term Direction

The long-term direction is a portable framework with:

- framework-owned operating docs and enforcement rules
- repository-local adapters generated from configuration
- a shared control-board and decision record model
- optional integrations with other systems once the core operating surface is stable

## Design Commitments

- process-first, not prompt-first
- framework and adapter separation
- tool independence over vendor lock-in
- explicit records over hidden chat-only state
- verification before completion claims
