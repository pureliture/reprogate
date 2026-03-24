# External Integrations

**Analysis Date:** 2026-03-24

## APIs & External Services

**Source control & repository hosting:**
- GitHub - Repository host and automation trigger source for `.github/workflows/product-definition-ci.yml` and `.github/workflows/update-progress-report.yml`.
  - SDK/Client: GitHub REST API via `requests` in `meta/progress/build_progress_report.py`; GitHub CLI fallback via `gh` in the same file.
  - Auth: `GITHUB_TOKEN` for API requests in `meta/progress/build_progress_report.py` and `.github/workflows/update-progress-report.yml`.

**Policy engine:**
- Open Policy Agent (OPA) - Selected rules engine in `reprogate.yaml` and documented as a required dependency in `README.md`.
  - SDK/Client: CLI-based integration path; rule assets live in `skills/record-required/rules.rego`, `skills/decision-documented/rules.rego`, `skills/scope-defined/rules.rego`, and `skills/verification-present/rules.rego`.
  - Auth: Not applicable.

**AI tool adapters:**
- Claude tooling - Local tool-hook integration configured in `.claude/settings.json` and templated in `templates/claude/settings.json.j2`.
  - SDK/Client: Shell command hooks that run `node` and Python wrapper scripts from `.claude/hooks/` and `scripts/hooks/claude_pretooluse_guard.py`.
  - Auth: Managed by the Claude host environment; no repository-managed credential file was detected.
- Gemini tooling - Local tool-hook integration configured in `.gemini/settings.json`.
  - SDK/Client: Shell command hooks invoking `node .gemini/hooks/*.js`.
  - Auth: Managed by the Gemini host environment; no repository-managed credential file was detected.
- Codex tooling - Local agent and hook integration configured in `.codex/config.toml`.
  - SDK/Client: `node /Users/pureliture/IdeaProjects/reprogate/.codex/get-shit-done/hooks/gsd-update-check.js` and TOML agent registrations in `.codex/config.toml`.
  - Auth: Managed by the Codex host environment; no repository-managed credential file was detected.
- GitHub Copilot custom instructions - Prompt-side integration in `.github/copilot-instructions.md`.
  - SDK/Client: Not applicable.
  - Auth: Managed by GitHub/Copilot outside this repository.

## Data Storage

**Databases:**
- Not detected.
  - Connection: Not applicable.
  - Client: Not applicable.

**File Storage:**
- Local filesystem only - Primary durable state lives in `docs/`, `records/`, `skills/`, `templates/`, `.planning/`, and `meta/progress/`.

**Caching:**
- None detected.

## Authentication & Identity

**Auth Provider:**
- GitHub token auth for automation - `meta/progress/build_progress_report.py` reads `GITHUB_TOKEN` to authorize REST calls; `.github/workflows/update-progress-report.yml` injects `${{ secrets.GITHUB_TOKEN }}`.
  - Implementation: Bearer-token HTTP headers in `meta/progress/build_progress_report.py`.
- GitHub CLI user auth fallback - `meta/progress/build_progress_report.py` falls back to `gh issue view` / `gh pr view` when `GITHUB_TOKEN` is missing.
  - Implementation: External `gh` login state on the executing machine.
- No application-level user authentication provider was detected for the repository itself.

## Monitoring & Observability

**Error Tracking:**
- None detected.

**Logs:**
- Script logs are plain stdout/stderr from Python and shell entry points such as `scripts/gatekeeper.py`, `scripts/validate_product_definition.py`, and `meta/progress/build_progress_report.py`.
- CI logs are emitted by GitHub Actions in `.github/workflows/product-definition-ci.yml` and `.github/workflows/update-progress-report.yml`.
- Generated status artifacts are written to `meta/progress/progress.md` and `meta/progress/progress.json`.

## CI/CD & Deployment

**Hosting:**
- GitHub repository hosting with no separate application hosting target detected.

**CI Pipeline:**
- GitHub Actions in `.github/workflows/product-definition-ci.yml` validates product-definition workflow changes on pull requests to `master` and `main`.
- GitHub Actions in `.github/workflows/update-progress-report.yml` rebuilds `meta/progress/progress.md` and `meta/progress/progress.json` on issue, pull request, push, schedule, and manual dispatch events.
- Local Git integration uses `.githooks/pre-commit`, `scripts/hooks/git_pre_commit.sh`, and `scripts/install_git_hooks.sh` to wire repository checks into Git hooks.

## Environment Configuration

**Required env vars:**
- `GITHUB_TOKEN` - Used by `meta/progress/build_progress_report.py` for GitHub REST API access.
- `DPC_CONTEXT_FILE` - Optional override read by `scripts/hooks/claude_pretooluse_guard.py` to locate process context JSON.
- `GITHUB_REPOSITORY` is exported in `.github/workflows/update-progress-report.yml`, although `meta/progress/build_progress_report.py` currently takes the repository slug from `meta/progress/progress-map.yaml`.

**Secrets location:**
- GitHub Actions secrets via `${{ secrets.GITHUB_TOKEN }}` in `.github/workflows/update-progress-report.yml`.
- Local developer environment variables for optional GitHub API access; no checked-in secret store was detected.

## Webhooks & Callbacks

**Incoming:**
- GitHub event callbacks drive `.github/workflows/update-progress-report.yml` on `issues`, `pull_request`, `push`, `workflow_dispatch`, and `schedule`.
- GitHub pull request events drive `.github/workflows/product-definition-ci.yml`.
- Local tool callback hooks are configured in `.claude/settings.json`, `.gemini/settings.json`, and `.codex/config.toml`.

**Outgoing:**
- HTTPS GET requests to `https://api.github.com/repos/{repo}/pulls/{number}` and `https://api.github.com/repos/{repo}/issues/{number}` from `meta/progress/build_progress_report.py`.
- `git push origin ...` from `.github/workflows/update-progress-report.yml` after regenerating progress artifacts.
- Local hook commands from `.claude/settings.json`, `.gemini/settings.json`, and `.codex/config.toml` invoke repository scripts and Node helpers.

---

*Integration audit: 2026-03-24*
