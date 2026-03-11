# ai-ops

Process-based AI collaboration framework for planning, implementation, verification, and traceability.

## Purpose

`ai-ops` separates reusable AI collaboration assets from project-specific adapters so the framework can be ported into other repositories without copying product history.

## Included in This Repository

- Process catalog for `G0`, `P0`-`P4`, `S1`-`S4`
- Tool-hook enforcement and compliance checks
- Config-driven project initialization and template generation
- Portable templates for Claude, Codex, workspace metadata, and project record scaffolds
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
- `ai-ops.config.yaml`
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
python3 scripts/launch_ai_ops_session.py --launcher omx -- --model gpt-5
```

For a fuller walkthrough, see [docs/installation.md](./docs/installation.md).

## Repository Layout

```text
ai-ops/
├── docs/
├── scripts/
├── config/
└── templates/
```

## License

MIT
