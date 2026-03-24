# Project Research Summary

**Project:** ReproGate
**Domain:** AI-Collaborative Repository Governance & Automation
**Researched:** 2026-03-24
**Confidence:** HIGH

## Executive Summary

ReproGate is a reproducible AI engineering framework designed to move repository governance from "vibe checks" to formal, policy-driven verification. It addresses the growing challenge of "AI slop" and inconsistent engineering standards in AI-collaborative environments by enforcing mandatory work records (ADRs/RFCs) and validating them against machine-readable "Skills" using Open Policy Agent (OPA). Experts build these systems by decoupling policy from execution and using durable, stateful agent orchestration.

The recommended approach centers on an "Artifact-driven" philosophy where all state is stored in Git-resident Markdown files. Technical implementation relies on LangGraph for resilient multi-agent workflows, Pydantic AI for structured data integrity, and the Model Context Protocol (MCP) to provide a standardized interface for external AI tools. This architecture ensures that governance is not a "black box" but a transparent, version-controlled part of the codebase.

Key risks include agentic "silent failure loops" where AI models hallucinate success, and the potential for "governance by policing" to degrade documentation quality. These are mitigated by shifting from reactive policing to proactive guidance-based gating, implementing deterministic circuit breakers (compilers/linters), and ensuring a tight feedback loop between human rationale and automated enforcement.

## Key Findings

### Recommended Stack

The stack is optimized for local-first reproducibility, high-rigor engineering, and seamless integration with modern AI orchestrators like Claude and Gemini.

**Core technologies:**
- **LangGraph (v1.0.0):** Durable Agent Orchestration — Handles stateful, human-in-the-loop cycles needed for complex gate enforcement.
- **OPA (Open Policy Agent):** Policy Engine — Industry standard for Policy-as-Code (Rego); allows "Skills" to be versioned and shared.
- **Pydantic AI (v1.0.1):** Production AI Framework — Enforces strict schemas on AI outputs, ensuring artifacts match required templates.
- **MCP Python SDK:** Model Context Protocol — Exposes ReproGate records and skills as resources to external AI models.

### Expected Features

The framework prioritizes engineering rigor and reproducibility over simple automation.

**Must have (table stakes):**
- **Tool Calling / MCP:** Standardized interaction with Git and the CLI.
- **Human-in-the-Loop (HITL):** Manual approval for critical architectural or state changes.
- **Structured Outputs:** Pydantic-validated JSON for all AI-generated artifacts.

**Should have (competitive):**
- **Mandatory Record Enforcement:** Blocking implementations that lack a corresponding ADR/RFC.
- **OPA/Rego Skill Gates:** Formal verification of engineering standards.
- **Artifact-Driven State:** Git-resident state for total reproducibility.

**Defer (v2+):**
- **Remote Policy Sync:** Centralized management for large distributed teams.
- **Self-Healing Evals:** Automated "judge" agents for filtering low-quality work.

### Architecture Approach

ReproGate uses a three-layer architecture (Context, Agentic, Governance) connected via the Model Context Protocol. It treats "Skills" and "Records" as first-class citizens, stored in dedicated directories for maximum portability and AI legibility.

**Major components:**
1. **MCP Server:** The "USB-C" interface exposing tools and resources to AI orchestrators.
2. **Gatekeeper (Python/OPA):** Core logic for enforcing mandatory records and running Rego policy checks.
3. **Agentic Orchestrator (LangGraph):** Manages the "ReproGate Loop" (Planner → Auditor → Executor).

### Critical Pitfalls

1. **"Vibe Coding" Silent Failures** — Avoid by using deterministic validation gates (compilers/tests) as circuit breakers.
2. **The "Mega-Policy" Trap** — Avoid by decoupling policy from data and using hierarchical namespaces in Rego.
3. **Rationale Hallucination** — Avoid by using agents to *draft* documentation while requiring human sign-off on the "why".

## Implications for Roadmap

### Phase 1: Foundation & Skill Gates
**Rationale:** Establishing the "Golden Principles" (Skills) and enforcement logic (Gatekeeper) is the prerequisite for all automation.
**Delivers:** Core CLI, OPA integration, and mandatory ADR/RFC enforcement logic.
**Addresses:** Mandatory Record Enforcement, Skill-based Gates.
**Avoids:** "Governance by Policing" (by setting up the guidance framework early).

### Phase 2: Agentic Integration (MCP)
**Rationale:** Once gates exist, we need to expose them to AI models via a standard interface.
**Delivers:** ReproGate MCP Server with Tool and Resource exposure.
**Uses:** MCP Python SDK, Pydantic AI.
**Implements:** Resource-Augmented Generation (RAG) pattern.

### Phase 3: Orchestration & Automation
**Rationale:** Automating the full GSD loop requires the foundations from Phases 1 & 2 to be stable.
**Delivers:** LangGraph-based workflows for Planner/Auditor/Executor agents.
**Addresses:** Multi-Agent Orchestration, Stateful Context Management.
**Avoids:** Silent Failure Loops (via integrated Auditor agent checks).

### Phase 4: UI & Scaling
**Rationale:** Real-time visibility and team-wide scaling are optimizations for the mature framework.
**Delivers:** Textual-based CLI Dashboard and Remote Policy Sync capabilities.

### Phase Ordering Rationale

- **Dependency-Driven:** Policy enforcement (Phase 1) must exist before we can automate the agents that are subject to those policies (Phase 3).
- **Integration-First:** Building the MCP server (Phase 2) ensures that the framework is immediately useful in modern IDEs before the full custom orchestrator is finished.
- **Risk Mitigation:** High-complexity features like "Self-Healing Evals" are deferred to later phases or v2 to focus on core stability.

### Research Flags

Phases likely needing deeper research during planning:
- **Phase 3 (Orchestration):** Complex state transitions in LangGraph require careful design of the "GSD" state schema.
- **Phase 4 (Scaling):** Remote Policy Sync via OCI bundles needs verification against internal registry security policies.

Phases with standard patterns (skip research-phase):
- **Phase 1 (Foundation):** OPA/Rego patterns and ADR/RFC templates are well-established.
- **Phase 2 (MCP):** MCP SDK provides clear, well-documented patterns for tool/resource exposure.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | Based on 2025 industry standards (LangGraph, MCP, OPA). |
| Features | HIGH | Aligned with ISO/IEC 42001 and NIST AI RMF requirements. |
| Architecture | HIGH | Standard 3-layer agentic pattern with MCP integration. |
| Pitfalls | HIGH | Derived from common agentic development failures (2024-2025). |

**Overall confidence:** HIGH

### Gaps to Address

- **Self-Healing Evals:** The threshold for "low-quality" rationale is subjective; needs validation during Phase 3.
- **SSE-based MCP:** Transitioning from `stdio` to `SSE` for team environments needs testing for latency/reconnection.

## Sources

### Primary (HIGH confidence)
- `mcp__context7__resolve-library-id` — Verified LangGraph, Pydantic AI, and OPA status.
- [https://openpolicyagent.org/docs/v1.12.x/oci-bundles/](https://openpolicyagent.org/docs/v1.12.x/oci-bundles/) — OCI bundle verification.
- [https://modelcontextprotocol.io/](https://modelcontextprotocol.io/) — MCP SDK version and protocol alignment.

### Secondary (MEDIUM confidence)
- [ISO/IEC 42001](https://www.iso.org/standard/81230.html) — AI Management System standards.
- [NIST AI RMF 1.0](https://www.nist.gov/itl/ai-risk-management-framework) — Risk management guidance.

---
*Research completed: 2026-03-24*
*Ready for roadmap: yes*
