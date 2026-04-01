# Roadmap

## Phases

- [ ] **Phase 1: Foundation & Governance** - Establish core repository initialization and policy enforcement.
- [ ] **Phase 2: Claude Code Workflow Integration** - Automate the end-to-end workflow lifecycle through durable artifacts and Claude Code adapter commands.
- [ ] **Phase 3: Visibility & Monitoring (HUD)** - Provide real-time status and progress tracking via a terminal dashboard.

## Phase Details

### Phase 1: Foundation & Governance
**Goal**: Establish the core framework for repository initialization, record creation, and policy enforcement.
**Depends on**: Nothing
**Requirements**: CORE-01, CORE-02, CORE-03, CORE-04, CORE-05
**Success Criteria**:
  1. User can initialize a new repository with ReproGate using `scripts/init.py`.
  2. User can generate work records (ADRs/RFCs) via the CLI.
  3. The gatekeeper blocks commits/operations if required records are missing or invalid according to Skill rules.
  4. All core tools are accessible through a single `reprogate` CLI entry point.
**Plans:** 0/3 plans executed

Plans:
- [x] 01-01-PLAN.md — Canonical config schema, record creation with sequential IDs, CLI rebranding and console-script entry point
- [x] 01-02-PLAN.md — OPA-wrapper gatekeeper with structural fallback (per ADR-002), PyYAML config, fail-closed enforcement
- [ ] 01-03-PLAN.md — Bootstrap test fixes and end-to-end integration tests for full init->create->check pipeline

### Phase 2: Claude Code Workflow Integration
**Goal**: Automate the research→strategy→execution lifecycle using durable artifacts and Claude Code as the primary harness. Establish the artifact contract that future harnesses can adopt without changing core semantics.
**Depends on**: Phase 1
**Requirements**: AUTO-01, AUTO-02
**Success Criteria**:
  1. User can trigger a workflow cycle via Claude Code commands that progresses from research to plan execution, leaving inspectable artifacts at each stage.
  2. The system generates and tracks progress via durable `ROADMAP.md` and `STATE.md` artifacts; any session can resume from these artifacts.
  3. Automated workflow tasks are subject to the same gatekeeper checks as manual ones.
  4. Claude Code adapter commands are generated via `scripts/generate.py` and live under `.claude/commands/`, keeping core logic harness-independent.
**Plans:** 3 plans

Plans:
- [ ] 02-01-PLAN.md — Wave 0 test scaffolds: failing stubs for workflow.py and generate extension (AUTO-01, AUTO-02)
- [ ] 02-02-PLAN.md — scripts/workflow.py lifecycle coordinator and three Claude Code command templates (AUTO-01, AUTO-02)
- [ ] 02-03-PLAN.md — cli.py and generate.py extension wiring, run generator to produce .claude/commands/ artifacts (AUTO-01, AUTO-02)

### Phase 3: Visibility & Monitoring (HUD)
**Goal**: Provide real-time visibility into gate status and project progress via a terminal dashboard.
**Depends on**: Phase 2
**Requirements**: UI-01
**Success Criteria**:
  1. User can view a real-time, terminal-based dashboard showing the status of all gates (pass/fail).
  2. The HUD displays project progress based on the current `STATE.md` and `ROADMAP.md`.
**Plans**: TBD
**UI hint**: yes

## Progress Table

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Foundation & Governance | 0/3 | Planned    |  |
| 2. Claude Code Workflow Integration | 0/3 | Planned | - |
| 3. Visibility & Monitoring (HUD) | 0/1 | Not started | - |
