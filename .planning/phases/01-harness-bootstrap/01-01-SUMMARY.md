---
phase: 01-harness-bootstrap
plan: 01
subsystem: infra
tags: [yaml-schema, gatekeeper, generate, templates, tdd]

# Dependency graph
requires: []
provides:
  - Canonical unified reprogate.yaml schema (INIT-05) — both gatekeeper.py and generate.py consumers aligned
  - record_triggers field in generate.py and gatekeeper.py load_config() defaults
  - templates/reprogate.yaml.j2 containing all canonical sections including record_triggers
  - Updated harness identity text in AGENTS.md.j2 and CLAUDE.md.j2 (INIT-06)
  - 8 TDD tests for INIT-05 schema alignment and INIT-06 template identity
affects:
  - 01-02 (INIT-04 record_triggers gatekeeper enforcement — depends on record_triggers in schema)
  - 01-03 (any plan consuming generate.py or gatekeeper.py load_config())
  - templates-based generation (reprogate.yaml.j2 now canonical)

# Tech tracking
tech-stack:
  added: [pytest (dev dependency)]
  patterns:
    - "Unified schema defaults: generate.py load_config() extends defaults to include all gatekeeper fields"
    - "Optional path param: gatekeeper.py load_config(path=None) accepts explicit path for testability"
    - "TDD for config alignment: test canonical fields in both consumers via tmp_path fixture"

key-files:
  created:
    - scripts/tests/test_schema_alignment.py
    - scripts/tests/test_template_identity.py
  modified:
    - templates/reprogate.yaml.j2
    - reprogate.yaml
    - scripts/generate.py
    - scripts/gatekeeper.py
    - templates/AGENTS.md.j2
    - templates/claude/CLAUDE.md.j2

key-decisions:
  - "Unified canonical defaults in generate.py rather than separate schema files — simpler, single source of truth"
  - "gatekeeper.py load_config() now accepts optional path parameter for testability without breaking module-level _config = load_config() usage"
  - "reprogate.yaml.j2 now contains all canonical sections with static defaults; init.py still uses {{ project_name }} placeholder but hardcodes process/record paths"

patterns-established:
  - "TDD for schema alignment: write tests asserting canonical key presence, then extend defaults dicts"
  - "Gatekeeper function accepts optional path: load_config(config_path=None) pattern for test isolation"

requirements-completed: [INIT-05, INIT-06]

# Metrics
duration: 4min
completed: 2026-04-02
---

# Phase 01 Plan 01: Fix Two-Schema Problem and Harness Identity Summary

**Canonical reprogate.yaml schema unified across generate.py and gatekeeper.py load_config() defaults, with record_triggers field added and compiler/gatekeeper identity replaced with delivery harness in all templates**

## Performance

- **Duration:** 4 min
- **Started:** 2026-04-02T05:11:28Z
- **Completed:** 2026-04-02T05:15:47Z
- **Tasks:** 2 (TDD RED + GREEN)
- **Files modified:** 6 + 2 test files created

## Accomplishments
- INIT-05: generate.py load_config() now returns all 12 canonical schema fields including records_dir, record_types, skills_dir, active_skills, gatekeeper, reprogate_version, record_triggers
- INIT-05: gatekeeper.py load_config() now accepts optional path parameter and includes record_triggers in defaults
- INIT-05: templates/reprogate.yaml.j2 now contains full canonical schema with project, workspaces, tools, records, record_triggers sections
- INIT-05: reprogate.yaml live file updated with all canonical sections including project identity, workspace config, and record_triggers
- INIT-06: "compiler/gatekeeper" identity text replaced with "delivery harness" in AGENTS.md.j2 and CLAUDE.md.j2
- 8 TDD tests written and verified passing (4 schema alignment + 4 template identity)

## Task Commits

Each task was committed atomically:

1. **Task 1: Write failing tests for INIT-05 and INIT-06** - `4d2d077` (test)
2. **Task 2: Implement canonical schema (INIT-05) and harness identity (INIT-06)** - `fd0f751` (feat)

_Note: TDD tasks: test commit (RED) then feat commit (GREEN)_

## Files Created/Modified
- `scripts/tests/test_schema_alignment.py` - 4 TDD tests for INIT-05 canonical schema fields
- `scripts/tests/test_template_identity.py` - 4 TDD tests for INIT-06 delivery harness identity
- `templates/reprogate.yaml.j2` - Canonical unified schema template with all sections
- `reprogate.yaml` - Live config updated with project identity, workspace config, record_types, record_triggers
- `scripts/generate.py` - load_config() defaults extended with records_dir, record_types, skills_dir, active_skills, gatekeeper, reprogate_version, record_triggers
- `scripts/gatekeeper.py` - load_config() accepts optional path param; record_triggers added to defaults dict
- `templates/AGENTS.md.j2` - "compiler/gatekeeper" replaced with "delivery harness"
- `templates/claude/CLAUDE.md.j2` - "compiler/gatekeeper" replaced with "delivery harness"

## Decisions Made
- Unified canonical defaults in generate.py by extending default_data dict — simpler than maintaining separate schema files
- gatekeeper.py load_config() made testable via optional path parameter; module-level _config = load_config() still works with no args
- reprogate.yaml.j2 hardcodes static defaults (no {{ enabled_process_lines }} placeholder); init.py rendering of those sections was pre-existing broken behavior

## Deviations from Plan

None - plan executed exactly as written. The test for gatekeeper.load_config(path) required adding an optional path parameter to gatekeeper.py, which was the correct interpretation of the plan's intent (making load_config testable).

## Issues Encountered

Pre-existing test failures discovered (not caused by this plan — verified by stashing changes):
- `test_yaml_parsing.py` imports `check_compliance` module which doesn't exist
- `test_bootstrap_smoke.py::TestBootstrapSmokeTest` requires `check_compliance.py`
- `test_bootstrap_smoke.py::TestBootstrapEdgeCases::test_init_with_custom_processes` — `init.py` template doesn't use `{{ enabled_process_lines }}` placeholder in processes section
- `test_bootstrap_smoke.py::TestBootstrapEdgeCases::test_generate_with_disabled_claude_skips_claude_files` — pre-existing logic issue

All deferred to `deferred-items.md` in this phase directory. Not caused by plan 01-01 changes.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- record_triggers field is now in both generate.py and gatekeeper.py defaults — INIT-04 (plan 01-02) can implement trigger enforcement
- Template identity aligned with ADR-009 harness pivot — all downstream consumers will see "delivery harness" identity
- Canonical schema allows gatekeeper.py and generate.py consumers to work from same reprogate.yaml without silent fallbacks

---
*Phase: 01-harness-bootstrap*
*Completed: 2026-04-02*
