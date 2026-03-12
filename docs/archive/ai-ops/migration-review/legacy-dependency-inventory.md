# Legacy Dependency Inventory for Staged Migration

> Archived review record.
> Archived at: 2026-03-11 P3 legacy namespace sunset round
> Use with: `docs/work-packets/WP-AIOPS-2026-03-010-framework-extraction.md`

## Purpose

This document records what still remains under the legacy `docs/ai-ops/*` and `scripts/ai-ops/*`
namespace after the 2026-03-11 root non-record SoT promotion / implementation-layer collapse round.

It answers two questions:

1. what is now canonical at the root namespace?
2. what legacy artifacts still remain, and why?

## 0. P1 Final Policy Snapshot (2026-03-11)

The legacy namespaces are now treated as **temporary transition surfaces only**.

- target end-state:
  - no live AI Ops operational surface under `docs/ai-ops/*`
  - no live operator-facing or hook-source implementation under `scripts/ai-ops/*`
- allowed final survivors:
  - archived history under `docs/archive/ai-ops/*`
  - none under `scripts/ai-ops/*`

This means the next P3 is expected to remove or relocate the remaining legacy surfaces rather than
extend them.

## 1. Canonical State After P3 Follow-up

### 1.1 Live AI Ops records

The live AI Ops control-board now uses the root namespace:

- `docs/work-packets/index.md`
- `docs/work-packets/WP-AIOPS-2026-03-001-ai-ops-bootstrap.md`
- `docs/work-packets/WP-AIOPS-2026-03-008-codex-omx-alignment.md`
- `docs/work-packets/WP-AIOPS-2026-03-010-framework-extraction.md`
- `docs/adr/ADR-AIOPS-001..005`
- `docs/CHANGELOG.md`

Status: **canonical live path fixed**

### 1.2 Stable operator-facing commands

The stable command surface is now the root script namespace:

- `scripts/set_process_context.py`
- `scripts/check_compliance.py`
- `scripts/launch_ai_ops_session.py`
- `scripts/install_git_hooks.sh`
- `scripts/sync_omc_policy.sh`

Status: **canonical stable command path fixed**

### 1.3 Root non-record AI Ops SoT

The broader non-record AI Ops SoT is now promoted into the root namespace:

- `docs/constitution.md`
- `docs/ops-bootstrap-master-plan.md`
- `docs/operating-model.md`
- `docs/work-packet-spec.md`
- `docs/goal-alignment-checklist.md`
- `docs/commands/*`
- `docs/process-catalog/*`
- `docs/tool-hooks/*`
- `docs/portability/ai-tool-artifact-boundary.md`
- `docs/omc-config/*`
- `docs/workspace-profiles/*`

Status: **root canonical non-record SoT fixed**

## 2. Remaining Legacy Dependencies

### 2.1 Legacy bridge docs / records

The following legacy files remain on purpose, but are no longer canonical:

- `docs/ai-ops/CHANGELOG.md`
- `docs/ai-ops/work-packets/index.md`
- `docs/ai-ops/work-packets/WP-AIOPS-2026-03-001-ai-ops-bootstrap.md`
- `docs/ai-ops/work-packets/WP-AIOPS-2026-03-008-codex-omx-alignment.md`
- `docs/ai-ops/work-packets/WP-AIOPS-2026-03-010-framework-extraction.md`
- `docs/ai-ops/adr/ADR-AIOPS-001..005`
- promoted legacy doc stubs under:
  - `docs/ai-ops/constitution.md`
  - `docs/ai-ops/ops-bootstrap-master-plan.md`
  - `docs/ai-ops/commands/*`
  - `docs/ai-ops/process-catalog/*`
  - `docs/ai-ops/tool-hooks/*`
  - `docs/ai-ops/omc-config/*`
  - `docs/ai-ops/workspace-profiles/*`
  - `docs/ai-ops/operating-model.md`
  - `docs/ai-ops/work-packet-spec.md`
  - `docs/ai-ops/goal-alignment-checklist.md`

Role:
- compatibility pointer
- legacy entry-path redirect
- historical namespace preservation during migration review

Owner: `WP-AIOPS-2026-03-010 / next S1`

Removal condition:
- S1 confirms the root canonical paths are self-consistent, and
- deletion-readiness review explicitly approves removal or archive relocation.

### 2.2 Historical retained archive material

The historical archive is now split as follows:

- canonical historical WP archive:
  - `docs/archive/ai-ops/work-packets/WP-AIOPS-2026-03-002..007,009`
- canonical archived design source:
  - `docs/archive/ai-ops/ai-collaboration-guide.md`
- retained legacy stub redirects:
  - legacy `docs/ai-ops/work-packets/WP-AIOPS-2026-03-002..007,009`
- retained in-place discussion artifacts pending next P3:
  - `docs/ai-ops/CONTINUE-DISCUSSION-PROMPT.md`
  - `docs/ai-ops/future-direction-discussion-2026-03-09.md`

Role:
- historical traceability
- frozen references to earlier path contracts

Policy:
- do not bulk-rewrite old path strings inside these materials
- preserve them as frozen history unless a redirect note is needed at an entry path
- final disposition fixed in this P1:
  - `future-direction-discussion-2026-03-09.md` → move to `docs/archive/ai-ops/discussions/`
  - `CONTINUE-DISCUSSION-PROMPT.md` → delete in next P3 after the discussion record is archived

### 2.3 Legacy compatibility shims under `scripts/ai-ops/*`

The five stable root commands now own the implementation. The remaining legacy files are only thin shims:

- `scripts/ai-ops/check_ai_ops_compliance.py`
- `scripts/ai-ops/set_process_context.py`
- `scripts/ai-ops/launch_ai_ops_session.py`
- `scripts/ai-ops/install_git_hooks.sh`
- `scripts/ai-ops/sync_omc_policy.sh`

Status: **compatibility shim layer**

Interpretation:
- stable command contract is root `scripts/*`
- stable command implementation is also root `scripts/*`
- legacy `scripts/ai-ops/*` for the five operator-facing commands are now redirect-only compatibility shims

Owner: `WP-AIOPS-2026-03-010 / next S1`

Removal condition:
- no remaining active/local-only adapter requires direct legacy invocation
- live docs/examples stop recommending direct legacy invocation
- next P3 relocates any remaining non-shim tool asset out of `scripts/ai-ops/*`
- S1 approves final removal

### 2.4 Tool-specific supporting asset relocation policy

`scripts/ai-ops/claude_pretooluse_guard.py` remains a versioned supporting asset **for now**.

Reason:
- it is copied into `.claude/hooks/` by install/sync flows
- it is not part of the root stable operator-facing command list

Final policy:
- keep the file versioned, but **do not keep it under the legacy namespace long-term**
- move it in next P3 to a root-owned tool path such as `scripts/hooks/claude_pretooluse_guard.py`
- update `scripts/install_git_hooks.sh`, docs, and sync references to the new root path
- remove the legacy copy in the same P3 once the new root path is verified

This file is therefore a temporary relocation candidate, not a permanent exception to the root
stable-command policy.

### 2.5 `claude_prompthouse_qa.py` note

No `scripts/ai-ops/claude_prompthouse_qa.py` file exists in the current repository snapshot or git
history reviewed on 2026-03-11.

Policy:
- do not create or restore such a file under `scripts/ai-ops/*`
- if a Claude-specific QA helper is needed later:
  - operational hook/support asset → root-owned `scripts/hooks/*`
  - experimental/manual helper → non-legacy utility namespace or separate repo
- therefore this item is **not a current deletion blocker**

## 3. Authoritative vs Non-Authoritative Summary

### Authoritative now

- root live records in `docs/work-packets/`, `docs/adr/`, `docs/CHANGELOG.md`
- root non-record AI Ops SoT in `docs/*`
- root stable commands in `scripts/*`
- archive copies in `docs/archive/ai-ops/*` for closed historical WP/design material

### Non-authoritative now

- legacy bridge records in `docs/ai-ops/work-packets/*`, `docs/ai-ops/adr/*`, `docs/ai-ops/CHANGELOG.md`
- legacy promoted-doc stubs in `docs/ai-ops/*`
- legacy shim scripts in `scripts/ai-ops/*` for the five stable commands

## 4. Remaining Deletion Blockers

The repository is still not automatically deletion-ready because:

1. `docs/ai-ops/*` still intentionally retains bridge stubs, migration-review docs, and frozen discussion exceptions
2. `scripts/ai-ops/*` still exist as compatibility shims/supporting assets, even though implementation ownership moved to `scripts/*`
3. hidden/local adapter surfaces (`.claude/*`, `.omc/*`, project skill metadata) were not rewritten in this round and must be reviewed separately from root canonical policy

## 5. P1 Final Disposition Matrix

| Artifact class | Current role | Final action | Target path / outcome |
|---|---|---|---|
| `docs/ai-ops/CONTINUE-DISCUSSION-PROMPT.md` | session helper prompt | **delete** | none |
| `docs/ai-ops/future-direction-discussion-2026-03-09.md` | frozen discussion record | **archive move** | `docs/archive/ai-ops/discussions/` |
| `docs/ai-ops/portability/legacy-dependency-inventory.md` | migration-review input | **archive move after next S1 pass** | `docs/archive/ai-ops/migration-review/` |
| `docs/ai-ops/portability/staged-migration-deletion-readiness-checklist.md` | migration-review gate | **archive move after next S1 pass** | `docs/archive/ai-ops/migration-review/` |
| legacy bridge docs under `docs/ai-ops/*` | redirect / compatibility entry path | **remove in next P3** | none |
| five legacy shims under `scripts/ai-ops/*` | redirect-only compatibility executables | **remove in next P3** | none |
| `scripts/ai-ops/claude_pretooluse_guard.py` | versioned hook source | **move in next P3** | root-owned `scripts/hooks/*` |
| `scripts/ai-ops/claude_prompthouse_qa.py` (if ever introduced) | not present | **disallow under legacy namespace** | root-owned or experimental non-legacy path only |

## 6. Next P3 Planned Removal Scope

The next implementation round should physically execute the following:

1. archive the frozen discussion record to `docs/archive/ai-ops/discussions/`
2. delete `docs/ai-ops/CONTINUE-DISCUSSION-PROMPT.md`
3. relocate `scripts/ai-ops/claude_pretooluse_guard.py` to a root-owned path and rewire install/docs
4. delete the five redirect-only legacy shim scripts
5. remove remaining `docs/ai-ops/*` bridge/stub files once zero live entry-path dependence is rechecked
6. move migration-review docs to `docs/archive/ai-ops/migration-review/` after the deletion-readiness verdict is finalized in S1

## 7. Remaining S1 Review Questions

1. After the next P3, do any live adapters/docs/scripts still materially depend on `docs/ai-ops/*` or `scripts/ai-ops/*`?
2. Was the hook-source relocation completed without breaking `.claude/hooks/pretooluse-ai-ops-guard.py` sync?
3. Are the archived discussion/migration-review materials sufficient to preserve historical traceability?
4. Can the repository now pass a zero-live-legacy-surface review?
