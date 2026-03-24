# Requirements

## v1 Requirements

### CORE: Repository Governance
- [ ] **CORE-01**: Support mandatory work record creation (ADRs, RFCs) via CLI.
- [ ] **CORE-02**: Enforce work record presence and structure via `scripts/gatekeeper.py`.
- [ ] **CORE-03**: Validate work records against "Skills" (OPA/Rego policies) in `skills/`.
- [ ] **CORE-04**: Support repository initialization and framework porting via `scripts/init.py` and `scripts/generate.py`.
- [ ] **CORE-05**: Provide a unified CLI entry point via `scripts/cli.py`.

### INTEG: AI Orchestrator Integration
- [ ] **INTEG-01**: Implement a Model Context Protocol (MCP) server to expose ReproGate records and skills to AI agents (Claude, Gemini).
- [ ] **INTEG-02**: Support "Skill" discovery and documentation-first architecture visibility for AI orchestrators.

### AUTO: GSD Workflow Automation
- [ ] **AUTO-01**: Automate the basic "Research -> Strategy -> Execution" (GSD) lifecycle within the framework.
- [ ] **AUTO-02**: Support plan generation and execution tracking through durable artifacts.

### UI: Progress & Visibility
- [ ] **UI-01**: Provide a terminal-based HUD (Heads-Up Display) for real-time gate status and progress tracking using Textual.

## v2 Requirements (Deferred)
- [ ] **SCALE-01**: Support for remote policy synchronization via OCI registries.
- [ ] **SCALE-02**: Team-wide "Skill" sharing and hierarchical policy management.
- [ ] **INTEG-03**: Support for additional AI orchestrator protocols beyond MCP.

## Out of Scope
- [ ] **STATE-01**: Centralized server-side state tracking (prioritize local, Git-resident state).
- [ ] **EXEC-01**: Arbitrary code execution outside of defined framework scripts.

## Traceability

| REQ-ID | Phase | Status |
|--------|-------|--------|
| CORE-01 | | Pending |
| CORE-02 | | Pending |
| CORE-03 | | Pending |
| CORE-04 | | Pending |
| CORE-05 | | Pending |
| INTEG-01 | | Pending |
| INTEG-02 | | Pending |
| AUTO-01 | | Pending |
| AUTO-02 | | Pending |
| UI-01 | | Pending |
