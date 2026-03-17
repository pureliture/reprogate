# ReproGate

> **AI 협업을 대화 기반 감각 작업에서 재현 가능한 엔지니어링 체계로**

Methodology compiler and gatekeeper for record-backed AI engineering.

## Purpose

ReproGate turns AI work from memory-dependent coding into reproducible engineering by making work records mandatory, accumulating durable Skills from those records, and enforcing them through gates.

The repository still contains legacy `dpc` names in scripts, IDs, and configuration while the product identity transitions to ReproGate.

## Included in This Repository

- Canonical product definition and strategy docs
- Record-backed gating and enforcement surfaces
- Tool-hook enforcement and compliance checks
- Config-driven project initialization and template generation
- Portable templates for Claude, Codex, workspace metadata, and work-record scaffolds
- Bootstrap copy of framework docs/scripts/config/templates into a target repository during `generate`

## Requirements

- Python 3.10+
- Git

Verified in this workspace with Python `3.13.3`.

## Quick Start

Create a starter config:

```bash
python3 scripts/cli.py init --project-name sample-app --force
```

Generate adapter files from the config:

```bash
python3 scripts/cli.py generate --force
```

That command now copies the framework payload needed by the adapters into the target repository:

- `docs/`
- `scripts/`
- `config/`
- `templates/`
- `dpc.config.yaml`
- generated adapter files such as `AGENTS.md`, `WORKSPACE-PROFILE.md`, `.codex/README.md`, `.claude/*`, and project record scaffolds

Run the compliance checker:

```bash
python3 scripts/cli.py check --mode none
```

Record process context:

```bash
python3 scripts/set_process_context.py --process P3 --wp WP-DEMO --team-mode single
```

Optional helpers:

```bash
./scripts/install_git_hooks.sh
./scripts/sync_omc_policy.sh
python3 scripts/launch_dpc_session.py --launcher omx -- --model gpt-5
```

For a fuller walkthrough, see [docs/installation.md](./docs/installation.md).

For the canonical product definition and direction, see:

- [docs/strategy/final-definition.md](./docs/strategy/final-definition.md)
- [docs/strategy/vision.md](./docs/strategy/vision.md)
- [docs/strategy/roadmap.md](./docs/strategy/roadmap.md)
- [docs/guide/why-dpc.md](./docs/guide/why-dpc.md)

## Core Ideas

- **Work records are mandatory**: intent, scope, decisions, and verification must survive beyond chat context.
- **Skills accumulate from records**: repeated patterns become durable text assets instead of disappearing into prior sessions.
- **Rules enforce the pattern**: records and artifacts give gates something concrete to inspect.
- **Artifact-driven workflow beats fragile state tracking**: the presence or absence of required outputs drives the next step.
- **Personal patterns can scale to team standards**: the same Skills and gates can be shared across a repository.

## Repository Layout

```text
reprogate/
├── docs/
├── scripts/
├── config/
└── templates/
```

## License

MIT
