# Installation and Bootstrap

## Requirements

- Python 3.10+
- Git
- notesmd-cli (optional, for document search)

Verified in this repository with Python `3.13.3`.


## 1. Create a Config File

Generate a starter `dpc.config.yaml`:

```bash
python3 scripts/cli.py init --project-name sample-app --force
```

Optional example with an explicit output path:

```bash
python3 scripts/cli.py init --output /tmp/sample-dpc/dpc.config.yaml --project-name sample-app --force
```

## 2. Generate Adapter Files

Generate adapter assets into the current repository:

```bash
python3 scripts/cli.py generate --force
```

Generate into another target directory:

```bash
python3 scripts/cli.py generate --config /tmp/sample-dpc/dpc.config.yaml --output-root /tmp/sample-dpc/output --force
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
python3 scripts/launch_dpc_session.py --launcher omx -- --model gpt-5
```

## Generated Files

Current generator bootstraps a reusable local copy of the framework into the target repository:

- `dpc.config.yaml`
- `docs/`
- `scripts/`
- `config/`
- `templates/`
- `AGENTS.md`
- `WORKSPACE-PROFILE.md`
- `.codex/README.md` when Codex support is enabled in the config
- `.claude/CLAUDE.md` when Claude support is enabled in the config
- `.claude/commands/dpc.md`, `.claude/settings.json`, and `.claude/hooks/pretooluse-dpc-guard.py` when Claude support is enabled
- project record scaffolds at the configured `wp_path`, `adr_path`, and `changelog_path`

## Document Search

### Option A: Built-in (no dependencies)

```bash
python3 scripts/cli.py search "constitution"           # fuzzy file search
python3 scripts/cli.py search-content "process"        # content search
python3 scripts/cli.py search-content "WP-DPC" --format json
python3 scripts/cli.py print "constitution"            # view document
```

### Option B: notesmd-cli (recommended for power users)

Install:
```bash
brew tap yakitrak/yakitrak && brew install notesmd-cli
```

Register vault (one-time setup):
```bash
mkdir -p ~/Library/Application\ Support/obsidian
cat > ~/Library/Application\ Support/obsidian/obsidian.json << EOF
{
  "vaults": {
    "dpc-docs": {
      "path": "$(pwd)/docs"
    }
  }
}
EOF
notesmd-cli set-default "docs"
```

Usage:
```bash
notesmd-cli search                              # interactive fuzzy search
notesmd-cli search-content "process"            # content search
notesmd-cli search-content "WP-DPC" --format json --no-interactive
notesmd-cli print "constitution"
```

## Notes

- The generated repository is self-contained enough to run the copied process docs and scripts without opening the source framework checkout.
- Runtime process context is stored under `.dpc/` and should remain local-only.
