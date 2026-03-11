# Installation and Bootstrap

## Requirements

- Python 3.10+
- Git

Verified in this repository with Python `3.13.3`.

## 1. Create a Config File

Generate a starter `ai-ops.config.yaml`:

```bash
python3 scripts/cli.py init --project-name sample-app --force
```

Optional example with an explicit output path:

```bash
python3 scripts/cli.py init --output /tmp/sample-ai-ops/ai-ops.config.yaml --project-name sample-app --force
```

## 2. Generate Adapter Files

Generate adapter assets into the current repository:

```bash
python3 scripts/cli.py generate --force
```

Generate into another target directory:

```bash
python3 scripts/cli.py generate --config /tmp/sample-ai-ops/ai-ops.config.yaml --output-root /tmp/sample-ai-ops/output --force
```

## 3. Validate the Framework

Run the compliance checker:

```bash
python3 scripts/cli.py check --mode none
```

## 4. Record Process Context

Record a selected process before implementation:

```bash
python3 scripts/set_process_context.py --process P3 --wp WP-DEMO --team-mode single
```

## 5. Optional Helper Scripts

Install local git hooks and a Claude hook wrapper:

```bash
./scripts/install_git_hooks.sh
```

Sync the optional OMC policy template into `.omc/`:

```bash
./scripts/sync_omc_policy.sh
```

Launch a new Codex or OMX session using the recorded process context:

```bash
python3 scripts/launch_ai_ops_session.py --launcher omx -- --model gpt-5
```

## Generated Files

Current generator bootstraps a reusable local copy of the framework into the target repository:

- `ai-ops.config.yaml`
- `docs/`
- `scripts/`
- `config/`
- `templates/`
- `AGENTS.md`
- `WORKSPACE-PROFILE.md`
- `.codex/README.md` when Codex support is enabled in the config
- `.claude/CLAUDE.md` when Claude support is enabled in the config
- `.claude/commands/ai-ops.md`, `.claude/settings.json`, and `.claude/hooks/pretooluse-ai-ops-guard.py` when Claude support is enabled
- project record scaffolds at the configured `wp_path`, `adr_path`, and `changelog_path`

## Notes

- The generated repository is self-contained enough to run the copied process docs and scripts without opening the source framework checkout.
- Runtime process context is stored under `.ai-ops/` and should remain local-only.
