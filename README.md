# ReproGate

> **AI 협업을 대화 기반 감각 작업에서 재현 가능한 엔지니어링 체계로**

Methodology compiler and gatekeeper for record-backed AI engineering.

## Purpose

ReproGate turns AI work from memory-dependent coding into reproducible engineering by making work records mandatory, accumulating durable Skills from those records, and enforcing them through gates (OPA/Rego).

Rather than being a heavy state-tracking orchestrator, it is an **artifact-driven compiler/gatekeeper**. It is designed as an **installable software framework** that can be ported directly into target projects.

## Included in This Repository

- Canonical product definition and strategy docs (`docs/strategy/`, `docs/design/`)
- Record-backed gating and enforcement tools (`scripts/gatekeeper.py`)
- Config-driven project initialization and template generation (`scripts/init.py`, `scripts/generate.py`)
- Gate mechanics driven by OPA/Rego policies

## Requirements

- Python 3.10+
- Git
- OPA (Open Policy Agent) (Required for Rego evaluation)

Verified in this workspace with Python `3.13.3`.

## Quick Start

Create a starter config in your target project:

```bash
python3 scripts/init.py --project-name sample-app --force
```

Generate adapter files and port the ReproGate framework into the repository:

```bash
python3 scripts/generate.py --force
```

This command copies the framework payload needed by the adapters into the target repository:

- `docs/`
- `scripts/`
- `config/`
- `templates/`
- `dpc.config.yaml`
- generated adapter files such as `AGENTS.md`, `WORKSPACE-PROFILE.md`

Validate the records against defined Skills/Gates:

```bash
python3 scripts/gatekeeper.py
```

For the canonical product definition and direction, see:

- [docs/strategy/final-definition.md](./docs/strategy/final-definition.md)
- [docs/strategy/vision.md](./docs/strategy/vision.md)
- [docs/strategy/roadmap.md](./docs/strategy/roadmap.md)
- [docs/design/architecture.md](./docs/design/architecture.md)

## Core Ideas

- **Work records are mandatory**: intent, scope, decisions, and verification must survive beyond chat context.
- **Skills accumulate from records**: repeated patterns become durable text assets (`guidelines.md`, `rules.rego`) instead of disappearing into prior sessions.
- **Rules enforce the pattern**: records and artifacts give gates something concrete to inspect.
- **Artifact-driven workflow beats fragile state tracking**: the presence or absence of required outputs drives the next step.
- **Personal patterns can scale to team standards**: the same Skills and gates can be shared across a repository via ported configurations.

## Repository Layout

```text
reprogate/
├── docs/       # Strategy, Design, and Governance docs
├── scripts/    # Framework bootstrap (init, generate) and Gatekeeper engine
├── config/     # Configuration schemas
└── templates/  # Templates for generation
```

## License

MIT

## Progress

[View Progress Report](./meta/progress/progress.md)
