# Roadmap: ReproGate Delivery Harness

## Overview

ReproGate v1.0은 ECC 코어(hook lifecycle, skill evolution)와 GSD 플로우(discuss→plan→execute→verify)를 통합한 1인 개발자용 artifact-driven delivery harness다. Phase 1 기술 기반(CLI, gatekeeper, records, skills)이 이미 작동 중이며, 이 위에 하네스 설치/활성화(INIT) → hook lifecycle(HOOK) → skill evolution(SKILL-EVO) → specialist agents(AGENT) → phase workflow(PHASE) → artifact lifecycle(LIFECYCLE) 순으로 구축한다.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [x] **Phase 1: Harness Bootstrap** - `reprogate init/disable` 명령과 설정 인프라로 하네스를 설치·활성화·비활성화할 수 있게 한다 (completed 2026-04-02)
- [ ] **Phase 2: Hook Lifecycle** - ECC 방식의 session/compact/tool-use/failure hook으로 자동 상태 캡처·거버넌스를 구현한다
- [ ] **Phase 3: Skill Evolution** - session observation에서 instinct → prose skill까지의 구조화된 진화 파이프라인을 구현한다
- [ ] **Phase 4: Specialist Agents** - executor, verifier, planner 3종 에이전트를 CC 서브프로세스로 스폰 가능하게 한다
- [ ] **Phase 5: Phase Workflow** - discuss→plan→execute→verify 슬래시 커맨드와 phase artifact packet 구조를 구현한다
- [ ] **Phase 6: Artifact Lifecycle** - 완료된 phase 요약·공유와 하네스 상태 점검 명령을 구현한다

## Phase Details

### Phase 1: Harness Bootstrap
**Goal**: Developer can install, activate, configure, and deactivate the ReproGate harness with a single command
**Depends on**: Nothing (builds on FOUND-01~05 foundation)
**Requirements**: INIT-01, INIT-02, INIT-03, INIT-04, INIT-05, INIT-06
**Success Criteria** (what must be TRUE):
  1. Running `reprogate init` creates hook configuration in `.claude/settings.json` and initializes `.claude/session-data/` directory
  2. Setting `REPROGATE_DISABLED=1` disables all hook-layer behavior without uninstalling
  3. Running `reprogate disable` cleanly removes hook configuration from `.claude/settings.json`
  4. `reprogate.yaml` `record_triggers` path patterns correctly determine when a record is required
  5. Template files (`AGENTS.md.j2`, `CLAUDE.md.j2`) reflect harness identity, and `generate.py` output schema aligns with `init.py`
**Plans**: 3 plans

Plans:
- [x] 01-01-PLAN.md — Canonical schema alignment (INIT-05) and harness identity text (INIT-06)
- [x] 01-02-PLAN.md — Hook injection (`reprogate init`), hook removal (`reprogate disable`), REPROGATE_DISABLED base (INIT-01, INIT-02, INIT-03)
- [x] 01-03-PLAN.md — record_triggers path-pattern gating in gatekeeper.py (INIT-04)

### Phase 2: Hook Lifecycle
**Goal**: Harness automatically captures session state, governance events, and gate failures through the ECC hook lifecycle
**Depends on**: Phase 1 (init injects hook configuration)
**Requirements**: HOOK-01, HOOK-02, HOOK-03, HOOK-04, HOOK-05, HOOK-06
**Success Criteria** (what must be TRUE):
  1. Hook behavior varies by `REPROGATE_HOOK_PROFILE` (minimal/standard/strict) — all hooks respect the active profile
  2. Starting a Claude Code session initializes `current-session.json` in `.claude/session-data/`
  3. Ending a session saves session summary and generates a session observation YAML draft in `.claude/session-data/`
  4. Pre-compact state is automatically preserved to `.claude/session-data/pre-compact-state.json`
  5. Tool-use governance is captured at standard+ profiles (advisory during execution, hard gate at `git commit`), and gate failures are logged to `records/gate-failures/`
**Plans**: TBD

Plans:
- [ ] 02-01: TBD
- [ ] 02-02: TBD

### Phase 3: Skill Evolution
**Goal**: Developer can evolve session observations into reusable prose skills through a structured observation→instinct→skill pipeline
**Depends on**: Phase 2 (Stop hook generates session observations)
**Requirements**: SKILL-EVO-01, SKILL-EVO-02, SKILL-EVO-03, SKILL-EVO-04
**Success Criteria** (what must be TRUE):
  1. Stop hook automatically generates instinct YAML drafts from session observations
  2. Running `/rg:learn-eval` evaluates instinct quality and returns a Save/Improve/Absorb/Drop verdict
  3. Running `/rg:evolve` clusters related instincts and generates a prose skill draft
  4. Developer can manually author `.rego` rules from prose skills (automated rego conversion is explicitly v2)
**Plans**: TBD

Plans:
- [ ] 03-01: TBD

### Phase 4: Specialist Agents
**Goal**: Three specialist agents (executor, verifier, planner) can run as independent CC sub-processes with clear input/output contracts
**Depends on**: Phase 1 (CLI infrastructure)
**Requirements**: AGENT-01, AGENT-02, AGENT-03
**Success Criteria** (what must be TRUE):
  1. `gsd-executor` accepts a plan file, executes tasks with atomic commits, and records deviations
  2. `gsd-verifier` performs goal-backward verification against `must_haves` and produces `VERIFICATION.md`
  3. `gsd-planner` decomposes work into tasks, derives `must_haves` (truths/artifacts/key_links), and produces `PLAN.md`
**Plans**: TBD

Plans:
- [ ] 04-01: TBD

### Phase 5: Phase Workflow
**Goal**: Developer can run the full discuss→plan→execute→verify cycle through `/rg:*` slash commands with all artifacts organized in phase packets
**Depends on**: Phase 4 (phase commands spawn specialist agents)
**Requirements**: PHASE-01, PHASE-02, PHASE-03, PHASE-04, PHASE-05, PHASE-06
**Success Criteria** (what must be TRUE):
  1. `/rg:discuss-phase N` runs an interactive discussion and produces `CONTEXT.md` in the phase directory
  2. `/rg:plan-phase N` spawns gsd-planner and produces `{N}-{M}-PLAN.md` with `must_haves` frontmatter
  3. `/rg:execute-phase N` spawns gsd-executor sequentially and produces `{N}-{M}-SUMMARY.md`
  4. `/rg:verify-phase N` spawns gsd-verifier and produces `VERIFICATION.md` checked against must_haves
  5. `/rg:next` auto-detects current state from STATE.md and routes to the correct next step; all artifacts live in `.planning/phases/{NN}-{slug}/`
**Plans**: TBD

Plans:
- [ ] 05-01: TBD
- [ ] 05-02: TBD

### Phase 6: Artifact Lifecycle
**Goal**: Developer can summarize completed work for sharing and monitor harness health at a glance
**Depends on**: Phase 5 (needs phase artifacts to summarize), Phase 2 (needs hooks to check)
**Requirements**: LIFECYCLE-01, LIFECYCLE-02
**Success Criteria** (what must be TRUE):
  1. `/rg:phase-summary` generates a readable summary/share document from completed phase artifacts
  2. `/rg:harness-check` reports hook activation status, skill policy validity, and lists unresolved gate failures
**Plans**: TBD

Plans:
- [ ] 06-01: TBD

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → 4 → 5 → 6

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Harness Bootstrap | 3/3 | Complete   | 2026-04-02 |
| 2. Hook Lifecycle | 0/2 | Not started | - |
| 3. Skill Evolution | 0/1 | Not started | - |
| 4. Specialist Agents | 0/1 | Not started | - |
| 5. Phase Workflow | 0/2 | Not started | - |
| 6. Artifact Lifecycle | 0/1 | Not started | - |
