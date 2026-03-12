# Staged Migration Deletion Readiness Checklist

> Archived review record.
> Archived at: 2026-03-11 P3 legacy namespace sunset round
> Next live decision point: WP-010 `S1`

## Purpose

Use this checklist before deciding whether the source repository can safely remove the legacy
`docs/ai-ops/` directory structure.

## 1. Entry / Read Path Cutover

- [x] Active adapters read root-bridge paths instead of legacy paths
- [x] Root canonical docs exist for required first-read documents
- [x] Root-owned command implementations exist for required execution commands
- [x] No active adapter still depends on legacy record-path guidance except intentionally retained bridge/archive docs

## 2. Canonical Storage Decision

- [x] AI Ops work packets have a final canonical location decision (`docs/work-packets/`)
- [x] AI Ops ADRs have a final canonical location decision (`docs/adr/`)
- [x] changelog canonical location is explicitly fixed (`docs/CHANGELOG.md`)
- [x] script canonical location is explicitly fixed (`scripts/*`)
- [x] non-record AI Ops SoT is promoted to root `docs/*`

## 3. Compatibility Layer Rules

- [x] Every remaining bridge/wrapper has an owner and removal condition
- [x] The repository documents which bridge files are temporary
- [x] The repository documents which legacy files remain authoritative vs non-authoritative

## 4. Historical Material Treatment

- [x] Historical WP/ADR/archive documents have a retention policy
- [x] Old path references in historical material are accepted as frozen history or redirected
- [x] Removal of legacy canonical paths will not erase required historical context
- [x] Closed historical WPs have a dedicated archive path (`docs/archive/ai-ops/work-packets/*`)

## 5. Tooling / Hooks

- [x] `scripts/set_process_context.py` works as the root-owned implementation
- [x] `scripts/check_compliance.py` works as the root-owned implementation
- [x] `scripts/launch_ai_ops_session.py --dry-run` works as the root-owned implementation
- [x] git hook / OMC policy sync path strategy is aligned to the root stable command path

## 6. Final Go / No-Go Rule

Legacy `docs/ai-ops/` deletion can be considered only when:

1. entry/read paths are already cut over,
2. canonical record/script storage decisions are fixed,
3. compatibility layer removal conditions are documented,
4. historical materials have an explicit treatment plan,
5. a final S1 review marks deletion readiness as pass.

For this WP, “legacy removal” now means all of the following:

6. frozen discussion material is either archived or intentionally deleted by policy,
7. migration-review docs are no longer live blockers under `docs/ai-ops/portability/`,
8. the five redirect-only shim scripts under `scripts/ai-ops/*` are removed,
9. any surviving tool-specific asset is relocated to a root-owned non-legacy path,
10. live/operator-facing surfaces no longer require `docs/ai-ops/*` or `scripts/ai-ops/*`.

## 7. Next S1 Review Must Verify

- [ ] `docs/ai-ops/CONTINUE-DISCUSSION-PROMPT.md` is deleted
- [ ] `docs/ai-ops/future-direction-discussion-2026-03-09.md` is archived under `docs/archive/ai-ops/discussions/`
- [ ] migration-review docs moved to `docs/archive/ai-ops/migration-review/` or are explicitly justified as temporary if S1 is still No-Go
- [ ] `scripts/ai-ops/check_ai_ops_compliance.py`, `set_process_context.py`, `launch_ai_ops_session.py`, `install_git_hooks.sh`, `sync_omc_policy.sh` are removed
- [ ] `scripts/ai-ops/claude_pretooluse_guard.py` is relocated to a root-owned path and install/sync still works
- [ ] live docs/adapters/scripts show zero operational dependence on legacy paths
- [ ] historical references remain preserved only in frozen WP/CHANGELOG/archive materials
- [ ] final deletion-readiness verdict is explicitly recorded as PASS or NO-GO with rationale

## Current Verdict

**S1 re-review complete: Approve(root canonical direction) / No-Go(immediate full legacy deletion) (2026-03-11)**

Reason:
- root non-record AI Ops SoT is now canonical under `docs/*`,
- the five stable commands now own their implementation under `scripts/*`,
- closed historical WPs moved to `docs/archive/ai-ops/work-packets/*`,
- targeted live-path consistency issues were corrected and re-reviewed,
- but `docs/ai-ops/*` still intentionally retains bridge/review/discussion surfaces and `scripts/ai-ops/claude_pretooluse_guard.py` remains a supporting-asset exception, so immediate physical deletion still needs one more P1 policy round.
