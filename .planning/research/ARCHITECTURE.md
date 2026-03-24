# Architecture Research: Reproducible AI Engineering Frameworks

**Domain:** AI-First Repository Governance
**Researched:** 2026-03-24
**Confidence:** HIGH

## Standard Architecture

### System Overview

Modern AI-first repository governance systems (like ReproGate) are shifting from passive code storage to active, agent-driven ecosystems. The architecture is typically structured into three primary layers: the **Context Layer** (Knowledge/Policies), the **Agentic Workflow Layer** (Execution/Validation), and the **Governance Layer** (Enforcement/Auditing).

```
┌─────────────────────────────────────────────────────────────┐
│                 AI Orchestrator (Host/IDE)                  │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐        │
│  │ Planner │  │ Executor│  │ Auditor │  │Validator│        │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘        │
│       │            │            │            │              │
├───────┴────────────┴────────────┴────────────┴──────────────┤
│               Model Context Protocol (MCP)                  │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐    │
│  │                 ReproGate MCP Server                │    │
│  │ (Gatekeeper Tools, Knowledge Resources, Prompts)     │    │
│  └─────────────────────────────────────────────────────┘    │
├─────────────────────────────────────────────────────────────┤
│                  Core ReproGate Engine                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                   │
│  │ Skills   │  │ Records  │  │ Docs     │                   │
│  │ (Rego)   │  │ (ADRs)   │  │ (Spec)   │                   │
│  └──────────┘  └──────────┘  └──────────┘                   │
└─────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

| Component | Responsibility | Typical Implementation |
|-----------|----------------|------------------------|
| **AI Orchestrator** | Hosts AI models and manages the user conversation and session context. | Claude Desktop, Cursor, VS Code, JetBrains |
| **Specialized Agents** | Dedicated LLM personas (Planner, Executor, Auditor) with specific tool access and strict output rules. | System prompts + Tool calling (Function calling) |
| **MCP Server** | The "USB-C" interface that exposes ReproGate's local capabilities to external AI orchestrators. | Python/TS MCP SDK (JSON-RPC 2.0 over stdio/HTTP) |
| **Gatekeeper Tools** | Logic for enforcing mandatory work records (ADRs/RFCs) and running OPA/Rego policy checks. | `scripts/gatekeeper.py` (Python) |
| **Knowledge Resources** | Dynamic project context provided to AI agents (Architecture, Specs, Skills). | MCP Resource exposure of `docs/` and `skills/` |
| **Skills (Rego)** | The "Golden Principles" of the repository encoded as policy-as-code. | OPA (Open Policy Agent) / Rego files |
| **Records** | Durable artifacts that capture the "why" and "how" of engineering decisions. | ADRs, RFCs, Work Records (Markdown) |

## Recommended Project Structure

ReproGate's structure is designed for high portability (framework porting) and AI legibility.

```
reprogate/
├── .planning/           # Framework-level context and roadmap
│   ├── research/        # Domain research (Architecture, Pitfalls, etc.)
│   └── PROJECT.md       # Central project roadmap and requirements
├── skills/              # OPA/Rego policies (Golden Principles)
│   ├── naming/          # Naming convention skills
│   └── security/        # Security posture skills
├── docs/                # Multi-dimensional documentation
│   ├── strategy/        # High-level "Why"
│   ├── spec/            # Product "What"
│   └── design/          # Technical "How"
├── records/             # Durable work artifacts
│   ├── adr/             # Architecture Decision Records
│   └── rfc/             # Request for Comments / Plans
├── scripts/             # Framework tooling
│   ├── mcp/             # MCP Server implementation (INTEG-01)
│   │   ├── server.py    # Main MCP entry point
│   │   └── tools/       # Tool definitions (gatekeeper, generator)
│   ├── gatekeeper.py    # Core policy enforcement logic (GATE-01)
│   └── cli.py           # Unified CLI entry point (CLI-01)
└── templates/           # Jinja2-style adaptive templates (GEN-01)
```

### Structure Rationale

- **.planning/:** Separates project management context from the codebase, providing a "clean room" for AI agents to understand the roadmap without noise.
- **skills/:** Treats governance as a first-class citizen. Storing them in a dedicated folder allows for easy "Skill Porting" between projects.
- **records/:** Centralizes the "Paper Trail." Making this folder mandatory ensures reproducibility and auditability.
- **scripts/mcp/:** Isolates the integration layer. The MCP server acts as a translator, keeping the core `gatekeeper.py` logic pure and tool-agnostic.

## Architectural Patterns

### Pattern 1: Agent-in-the-Loop Gate

**What:** Integrating AI agents directly into the validation pipeline. Instead of just static analysis, an "Auditor Agent" uses the Gatekeeper tools to verify that a code change matches the *intent* described in its associated ADR/RFC.
**When to use:** In high-consequence repositories where human review is a bottleneck.
**Trade-offs:** Adds latency to the PR process, but significantly reduces "AI slop" and inconsistent code.

### Pattern 2: Resource-Augmented Generation (RAG) via MCP

**What:** Exposing the repository's `docs/` and `skills/` folders as MCP Resources. This allows the AI model to "pull" relevant context as needed rather than having to fit the entire repository into its prompt window.
**When to use:** When the codebase or documentation grows too large for a standard context window.
**Trade-offs:** Requires the model to be "agentic" (capable of deciding when to fetch resources).

### Pattern 3: Federated Skill Governance

**What:** A "Centralized-Federated" model where a core set of skills is maintained in a central repository (Skill Hub) and synced to local project repositories. Local teams can override or add domain-specific skills.
**When to use:** Scaling across multiple teams and hundreds of repositories (SCALE-01).
**Trade-offs:** Requires a synchronization mechanism (Git submodules, CLI sync, or a Policy API).

## Data Flow

### Request Flow (The "ReproGate Loop")

```
[User: "Build X"]
    ↓
[Planner Agent] ─── (Reads Docs/Skills via MCP) ───▶ [RFC Artifact]
    ↓                                                    ↓
[Auditor Agent] ◀─── (Validates RFC via Gatekeeper) ───┘
    │
    ▼ (Validated)
[Executor Agent] ─── (Applies Code + ADR) ──────────▶ [Draft Change]
    ↓                                                    ↓
[Auditor Agent] ◀─── (Full Verification via OPA) ─────┘
    │
    ▼ (Passed)
[Git Pull Request]
```

### Key Data Flows

1. **Policy Enforcement Flow:** `gatekeeper.py` reads a `record/`, looks up the corresponding `skill/` (Rego), and uses the OPA engine to return a PASS/FAIL result. This result is then wrapped by the MCP server and sent to the AI Host.
2. **Context Synchronization:** Changes to `skills/` in the "Skill Hub" are pulled by `scripts/cli.py sync`, updating the local `skills/` directory and immediately affecting the next AI agent interaction.

## Scaling Considerations

| Scale | Architecture Adjustments |
|-------|--------------------------|
| **Individual / Small Team** | Standard Git-resident skills and records. MCP server runs locally on the developer's machine via `stdio`. |
| **Mid-Size Org (10-100 devs)** | Introduce **Remote Policy Sync (SCALE-01)**. Centralize Skill management in a dedicated repo. Move MCP to an **SSE-based server** for team-wide sharing. |
| **Enterprise (100+ devs)** | **Federated Governance**. Sub-hubs for different domains (e.g., Frontend, Data Science). Automated **UI Dashboards (UI-01)** for compliance auditing. |

### Scaling Priorities

1. **First bottleneck (Context Drift):** As teams grow, local skills diverge. **Solution:** Remote Skill Hub with automated sync via CLI hooks.
2. **Second bottleneck (Agent Orchestration):** Manual agent handoffs become slow. **Solution:** Fully automated GSD pipeline (AUTO-01) where agents trigger each other based on gate status.

## Anti-Patterns

### Anti-Pattern 1: The "Invisible Rule"

**What people do:** Setting rules for AI in a system prompt or a `.cursorrules` file that isn't version-controlled or enforced.
**Why it's wrong:** Rules "drift" over time, are forgotten, and cannot be audited.
**Do this instead:** Encode every rule as an OPA/Rego skill in the `skills/` directory.

### Anti-Pattern 2: The "Chat-Only Decision"

**What people do:** Making architectural decisions in a chat thread and proceeding to code without creating an ADR.
**Why it's wrong:** Context is lost once the thread ends. The decision is not reproducible by other agents or future developers.
**Do this instead:** Make the Gatekeeper block any PR that doesn't have a corresponding record in `records/`.

## Integration Points

### External Services

| Service | Integration Pattern | Notes |
|---------|---------------------|-------|
| **AI Hosts (Claude/IDE)** | **MCP (Model Context Protocol)** | Standardizes how agents see ReproGate tools. Use `stdio` for local and `SSE` for remote. |
| **OPA (Open Policy Agent)** | **Python SDK / Binary** | Used by `gatekeeper.py` to evaluate Rego policies. |
| **Git / GitHub** | **Pre-commit Hooks / Actions** | Ensures that the Gatekeeper runs on every commit/push. |

### Internal Boundaries

| Boundary | Communication | Notes |
|----------|---------------|-------|
| **MCP Server ↔ Gatekeeper** | Direct Python calls | The MCP server is a lightweight wrapper around the CLI/Core logic. |
| **Planner ↔ Auditor Agents** | Shared Artifacts (RFC/ADR) | Agents communicate by reading and writing files in the `records/` directory. |

## Sources

- [Model Context Protocol (MCP) Official Docs](https://modelcontextprotocol.io)
- [Anthropic: Introducing MCP](https://www.anthropic.com/news/model-context-protocol)
- [Open Policy Agent (OPA) Documentation](https://www.openpolicyagent.org/docs/latest/)
- [Modern AI-first Governance Patterns (2025 Industry Survey)](https://medium.com/ai-governance-2025)
- [Federated Data/AI Governance - Databricks/Lifebit Case Studies](https://databricks.com/blog/federated-governance)

---
*Architecture research for: Reproducible AI Engineering Frameworks*
*Researched: 2026-03-24*
