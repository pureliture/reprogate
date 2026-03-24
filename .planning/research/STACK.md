# Stack Research: AI-Collaborative Repository Governance & Automation

**Domain:** ReproGate / Reproducible AI Engineering Framework
**Researched:** 2026-03-24
**Confidence:** HIGH

## Recommended Stack

### Core Technologies

| Technology | Version | Purpose | Why Recommended |
|------------|---------|---------|-----------------|
| **LangGraph** | `v1.0.0` | Durable Agent Orchestration | 2025 standard for multi-agent "GSD" workflows. Handles stateful, human-in-the-loop cycles needed for gate enforcement. |
| **OPA (Open Policy Agent)** | `v1.12.1` | Policy Engine (Rego v1.0) | Industry standard for Policy-as-Code. OCI bundle support allows scaling "Skills" across teams via registries. |
| **Pydantic AI** | `v1.0.1` | Production AI Framework | Enforces strict schemas (ADRs, RFCs) on AI outputs. Ensures the "Artifact-driven" philosophy is code-validated. |

### Supporting Libraries

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| **MCP Python SDK** | `v1.25.0` | Model Context Protocol | For building the `reprogate-mcp` server to expose records/skills to Claude/Gemini. |
| **Textual** | `v6.5.0` | Terminal UI (HUD) | For the real-time CLI dashboard tracking gate status and automation progress. |
| **Cosign (Sigstore)** | `v2.4.x` | Artifact Signing | When distributing OPA "Skills" via OCI to ensure provenance and security in shared repos. |

### Development Tools

| Tool | Purpose | Notes |
|------|---------|-------|
| **uv** | Python Manager | Lightning-fast dependency management and tool isolation (already standard in ReproGate). |
| **opa CLI** | Policy Testing | Use `opa test` for TDD on `skills/` policies (Rego v1.0). |

## Installation

```bash
# Core AI & Automation
uv add langgraph@^1.0.0 pydantic-ai@^1.0.1

# Integration & UI
uv add mcp-sdk@^1.25.0 textual@^6.5.0

# Dev dependencies
uv add --dev pytest-mock "opa-python-sdk>=1.12"
```

## Alternatives Considered

| Recommended | Alternative | When to Use Alternative |
|-------------|-------------|-------------------------|
| **LangGraph** | **Temporal** | If workflow state needs to survive server restarts across months (ReproGate focuses on local-first). |
| **Pydantic AI** | **Instructor** | If using older models or specific legacy Pydantic (v1) constraints. |
| **Textual** | **Next.js / Dashboard** | If a web-based team HUD is required (ReproGate prioritizes "local-first, artifact-driven" CLI). |

## What NOT to Use

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| **LangChain (Full)** | High abstraction "magic" makes debugging complex engineering gates difficult. | **LangGraph** (explicit state/control) |
| **Postgres/Redis** | Violates "Artifact-driven" goal by adding heavy external infrastructure. | **Git / Local JSON / OCI** |
| **Custom HTTP APIs** | Fragile interop between AI models and repository state. | **Model Context Protocol (MCP)** |

## Stack Patterns by Variant

**If Team-based Scaling:**
- Use **OCI Registries (GHCR)** for OPA bundles.
- Because it treats "Skills" as versioned, signed, and reproducible artifacts.

**If Agentic GSD Automation:**
- Use **LangGraph** with **Pydantic AI** tools.
- Because it allows the AI to perform "Research" and "Generation" while respecting "Gates".

## Version Compatibility

| Package A | Compatible With | Notes |
|-----------|-----------------|-------|
| `langgraph@1.0.0` | `pydantic-ai@1.0.1` | LangGraph v1 stabilized the AI framework ecosystem. |
| `opa@1.12.1` | `Rego v1.0` | Requires `rego_version: 1` in bundle manifests. |
| `mcp-sdk@1.25.0` | `MCP Protocol 2025-11-25` | Latest interop spec for Claude/Gemini desktops. |

## Sources

- `mcp__context7__resolve-library-id` — Verified LangGraph, Pydantic AI, and OPA status for 2025.
- [https://openpolicyagent.org/docs/v1.12.x/oci-bundles/](https://openpolicyagent.org/docs/v1.12.x/oci-bundles/) — OCI bundle verification.
- [https://modelcontextprotocol.io/](https://modelcontextprotocol.io/) — MCP SDK version and protocol alignment.
- Community Consensus 2025 — Confidence: HIGH for "Policy-as-Code" + "MCP" trend.

---
*Stack research for: Reproducible AI Engineering Framework (ReproGate)*
*Researched: 2026-03-24*
