# Roadmap

## Phases

- [ ] **Phase 1: Foundation & Governance** - Establish core repository initialization and policy enforcement.
- [ ] **Phase 2: AI Orchestrator Integration (MCP)** - Expose ReproGate artifacts and tools to AI agents via MCP.
- [ ] **Phase 3: Harness-Agnostic Workflow Automation** - Automate the end-to-end workflow lifecycle through durable artifacts and adapter ingress.
- [ ] **Phase 4: Visibility & Monitoring (HUD)** - Provide real-time status and progress tracking via a terminal dashboard.

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
**Plans:** 3 plans

Plans:
- [ ] 01-01-PLAN.md — CLI entry point with reprogate branding and record creation command
- [ ] 01-02-PLAN.md — Python-native skill evaluator and gatekeeper refactoring
- [ ] 01-03-PLAN.md — Config schema expansion, init.py update, and integration tests

### Phase 2: AI Orchestrator Integration (MCP)
**Goal**: Expose ReproGate's governance artifacts and tools to external AI agents via MCP.
**Depends on**: Phase 1
**Requirements**: INTEG-01, INTEG-02
**Success Criteria**:
  1. An AI agent (e.g., Claude Desktop) can connect to the ReproGate MCP server.
  2. The AI agent can list and read available ADRs, RFCs, and Skills as MCP resources.
  3. The AI agent can trigger record creation and validation tools via MCP tool calls.
**Plans**: TBD

### Phase 3: Harness-Agnostic Workflow Automation
**Goal**: Automate the end-to-end research-strategy-execution lifecycle using durable artifacts and harness-neutral adapter ingress.
**Depends on**: Phase 2
**Requirements**: AUTO-01, AUTO-02
**Success Criteria**:
  1. User can trigger an automated workflow cycle that progresses from research to plan execution through supported adapters.
  2. The system automatically generates and tracks progress via durable `ROADMAP.md` and `STATE.md` artifacts.
  3. Automated tasks are subject to the same gatekeeper checks as manual ones.
**Plans**: TBD

### Phase 4: Visibility & Monitoring (HUD)
**Goal**: Provide real-time visibility into gate status and project progress via a terminal dashboard.
**Depends on**: Phase 3
**Requirements**: UI-01
**Success Criteria**:
  1. User can view a real-time, terminal-based dashboard showing the status of all gates (pass/fail).
  2. The HUD displays project progress based on the current `STATE.md` and `ROADMAP.md`.
**Plans**: TBD
**UI hint**: yes

## Progress Table

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Foundation & Governance | 0/3 | Planning complete | - |
| 2. AI Orchestrator Integration (MCP) | 0/1 | Not started | - |
| 3. Harness-Agnostic Workflow Automation | 0/1 | Not started | - |
| 4. Visibility & Monitoring (HUD) | 0/1 | Not started | - |
