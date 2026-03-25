---
phase: 01-foundation-governance
plan: 01
subsystem: cli
tags: [yaml, argparse, pytest, record-creation, config-schema]

requires:
  - phase: none
    provides: "initial codebase with scripts/init.py, cli.py, reprogate.yaml"
provides:
  - "Canonical reprogate.yaml schema with record_types, active_skills, gatekeeper config"
  - "scripts/create_record.py for ADR/RFC creation with sequential IDs"
  - "Rebranded ReproGate CLI with create, check/gate commands"
  - "Console-script entry point in pyproject.toml"
affects: [01-02-PLAN, 01-03-PLAN]

tech-stack:
  added: [pytest]
  patterns: [sequential-record-ids, yaml-config-driven-record-types, subprocess-cli-dispatch]

key-files:
  created:
    - scripts/create_record.py
    - scripts/__init__.py
    - scripts/tests/test_record_creation.py
    - scripts/tests/test_cli.py
  modified:
    - reprogate.yaml
    - templates/reprogate.yaml.j2
    - scripts/init.py
    - scripts/cli.py
    - pyproject.toml
    - uv.lock

key-decisions:
  - "Canonical config uses flat structure with record_types and active_skills, not nested generate.py structure"
  - "generate.py left untouched -- separate reconciliation concern"
  - "Added gate as alias for check command per D-09 ReproGate-native vocabulary"
  - "Two ADR-008 files exist on disk; next_id correctly scans and would produce ADR-009"

patterns-established:
  - "Record type config in reprogate.yaml drives create_record.py behavior"
  - "Sequential zero-padded 3-digit IDs (ADR-NNN) for all record types"
  - "CLI uses subprocess dispatch pattern for all subcommands"

requirements-completed: [CORE-01, CORE-04, CORE-05]

duration: 3min
completed: 2026-03-25
---

# Phase 01 Plan 01: Config Schema, Record Creation, and CLI Summary

**Canonical reprogate.yaml with record_types/active_skills, create_record.py with sequential ADR-NNN IDs, ReproGate-branded CLI with console-script entry point**

## Performance

- **Duration:** 3 min
- **Started:** 2026-03-25T00:40:08Z
- **Completed:** 2026-03-25T00:43:15Z
- **Tasks:** 2
- **Files modified:** 9

## Accomplishments
- Locked canonical config schema with record_types, active_skills, and fail_closed gatekeeper config
- Built create_record.py with sequential ID generation matching existing ADR-NNN/RFC-NNN convention
- Rebranded CLI from "dpc" to "ReproGate", fixed broken check routing, added create and gate commands
- Registered reprogate console-script entry point in pyproject.toml
- 21 tests passing (12 record creation + 4 slug/id + 6 CLI)

## Task Commits

Each task was committed atomically:

1. **Task 1: Lock canonical config schema and update init.py** - `be6e4a1` (feat)
2. **Task 2 RED: Failing tests for record creation and CLI** - `1aeb94b` (test)
3. **Task 2 GREEN: Record creation, CLI rebranding, console-script** - `bb596b1` (feat)

## Files Created/Modified
- `reprogate.yaml` - Canonical expanded schema with record_types, active_skills, gatekeeper
- `templates/reprogate.yaml.j2` - Template matching canonical schema with project_name placeholder
- `scripts/init.py` - Simplified to only project_name arg, removed DEFAULT_PROCESSES
- `scripts/create_record.py` - Record scaffolding with sequential IDs, config-driven sections
- `scripts/cli.py` - ReproGate branding, create command, gate alias, gatekeeper.py routing
- `scripts/__init__.py` - Empty package init for console-script importability
- `pyproject.toml` - Console-script entry point and pytest dev dependency
- `scripts/tests/test_record_creation.py` - 15 tests for slugify, next_id, create_record
- `scripts/tests/test_cli.py` - 6 tests for branding, routing, commands

## Decisions Made
- Canonical config uses flat structure with record_types and active_skills -- does not adopt generate.py's nested structure. generate.py reconciliation deferred to separate work.
- Added "gate" as alias for "check" per D-09 ReproGate-native vocabulary.
- Two ADR-008 files already exist on disk (duplicate IDs from prior work); next_id correctly handles this by scanning max.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] pytest not installed in venv**
- **Found during:** Task 2 (TDD RED)
- **Issue:** uv venv did not have pytest; `uv add --dev pytest` needed before tests could run
- **Fix:** Ran `uv add --dev pytest` which updated pyproject.toml and uv.lock
- **Files modified:** pyproject.toml, uv.lock
- **Verification:** pytest runs successfully
- **Committed in:** 1aeb94b (Task 2 RED commit)

---

**Total deviations:** 1 auto-fixed (1 blocking)
**Impact on plan:** Trivial -- pytest installation was implicit in the plan but needed explicit execution.

## Issues Encountered
None

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Canonical config schema locked -- Plan 02 (gatekeeper) can read record_types and active_skills
- create_record.py ready for end-to-end integration testing in Plan 03
- CLI routing complete -- Plan 02 can add gatekeeper logic without CLI changes

---
*Phase: 01-foundation-governance*
*Completed: 2026-03-25*

## Self-Check: PASSED

All 10 files verified present. All 3 commits verified in git log.
