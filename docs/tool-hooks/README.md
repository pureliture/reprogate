# Tool Hooks

> Status: Active
> Version: `1.0.0`

## Purpose

This directory defines portable enforcement points for AI Ops-aware tooling.
A tool hook exists to turn process rules into runtime behavior.

## Hook Categories

| Hook | Purpose |
|---|---|
| [process-enforcement-matrix.md](./process-enforcement-matrix.md) | Process-by-process enforcement model |
| [claude-pretooluse-hook.md](./claude-pretooluse-hook.md) | Pre-execution guard model for tools that support tool-call hooks |
| [codex-jetbrains-ai-assistant-rules.md](./codex-jetbrains-ai-assistant-rules.md) | Session-entry and instruction-based enforcement model |
| [omc-quality-gates-ultraqa.md](./omc-quality-gates-ultraqa.md) | Verification-loop and quality-gate enforcement model |

## Design Rules

1. Keep the framework hook model portable.
2. Put tool-specific installation steps in adapter-owned docs.
3. Keep hard gates and soft guarantees separate.
4. Treat hook updates as lifecycle work, not one-time setup.

## Shared Expectations

Every adapter should define:

- where process context is recorded,
- when enforcement happens,
- what gets blocked,
- what evidence proves compliance,
- and which final gate protects the repository boundary.
