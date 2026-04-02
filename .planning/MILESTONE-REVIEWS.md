---
milestone: v1.0
reviewers: [gemini, codex]
skipped: [claude (auth 403)]
reviewed_at: 2026-04-03
artifacts_reviewed:
  - .planning/PROJECT.md
  - .planning/REQUIREMENTS.md
  - .planning/ROADMAP.md
  - .planning/research/SUMMARY.md
---

# Cross-AI Milestone Review — v1.0 ReproGate Delivery Harness

## Gemini Review

I have reviewed the four milestone artifacts for **ReproGate v1.0** following the ADR-009 product pivot. My analysis focuses on the transition from a "compiler/gatekeeper" model to the "ECC+GSD delivery harness" and identifies several critical misalignments between the legacy research and the new strategic direction.

### 1. Executive Summary
The ReproGate v1.0 plan successfully reorients the project toward a lean, artifact-driven harness optimized for 1인 개발자(solo developers) using Claude Code. By combining ECC-style hooks with GSD-style phase workflows, the plan creates a clear path for reproducible AI engineering. However, the technical stack has drifted significantly from the original research (LangGraph/MCP-centric) toward a more direct CLI/Hook-based architecture, leaving a "research debt" regarding the performance and reliability of shell-level orchestration.

### 2. Cross-Artifact Consistency
*   **Phase Numbering Clash:** `REQUIREMENTS.md` refers to the existing foundation as "Phase 1," while `ROADMAP.md` defines "Phase 1" as the upcoming "Harness Bootstrap" work. This will cause confusion during status reporting and `/gsd-next` execution.
*   **Orchestrator Identity:** `PROJECT.md` and `ROADMAP.md` consistently name Claude Code as the primary orchestrator, but `REQUIREMENTS.md` (AGENT-01~03) describes agents as "CC sub-processes." There is a slight ambiguity whether these are standalone CLIs called by CC or integrated MCP tools.
*   **State Management:** `PHASE-05` mentions `STATE.md` for auto-routing, but `STATE.md` is not explicitly defined in the `INIT` or `PHASE` requirement blocks as a managed artifact (only its *use* is mentioned).
*   **Terminology Drift:** The term "Skill Evolution" (ECC) and "Phase Workflow" (GSD) are well-integrated, but the "Layer 3: ReproGate Unique" section in `PROJECT.md` mentions "operate/maintain" surfaces that aren't fully fleshed out in the specific requirements beyond a single health check.

### 3. Requirements Gaps
*   **[HIGH] Hook Performance/Timeout:** No requirement defines the latency budget for `PreToolUse` hooks. If OPA evaluation or state capture takes >500ms, it will degrade the Claude Code user experience.
*   **[MEDIUM] Hook Recovery/Fail-safe:** If `reprogate` hooks fail (e.g., Python error, binary missing), does the harness block all development or fail-open? `INIT-02` (Manual disable) is present, but automated "Safe Mode" is missing.
*   **[MEDIUM] Artifact Cleanup/Pruning:** `PHASE-06` defines the packet structure, but there is no requirement for archiving or pruning old `.planning/phases/` data, which could lead to context bloat in long-lived projects.
*   **[LOW] Environment Parity:** The requirements don't specify if `reprogate` should behave differently in CI vs. Local, though `HOOK-01` (Profiles) partially addresses this.

### 4. Roadmap Feasibility
*   **Logic:** The ordering (Bootstrap -> Hooks -> Skills -> Agents -> Workflow) is highly logical. Implementing the "observation" engine (Hooks) before the "evolution" engine (Skills) is correct.
*   **Phase 4 vs 5:** Placing Specialist Agents (Phase 4) before Workflow (Phase 5) is the correct dependency choice, as the workflow commands are essentially wrappers/orchestrators for these agents.
*   **Sizing:** Phase 2 (Hooks) and Phase 5 (Workflow) are significantly "heavier" than Phase 4. Phase 4 might be better merged into Phase 5 or treated as a "Utilities" phase.

### 5. Research Staleness
The research summary is currently **40% stale** due to the pivot away from a heavy Python-framework stack.

| Finding | Status | Note |
|:---|:---|:---|
| **LangGraph (v1.0.0)** | **STALE** | Pivot favors CC-as-orchestrator + shell sub-agents. LangGraph is likely too heavy for this "lean harness" model. |
| **Pydantic AI** | **STALE** | While sub-agents might use it internally, it's no longer the "Core Stack" for the harness itself. |
| **OPA / Rego** | **CURRENT** | Remains the foundational technology for Skill gating (FOUND-03, SKILL-EVO-04). |
| **MCP (Model Context Protocol)** | **MISSING** | `PROJECT.md` ignores MCP in favor of "slash commands." If CC is the orchestrator, MCP is the idiomatic way to expose ReproGate tools. |
| **Artifact-Driven State** | **CURRENT** | Perfectly aligned with the new GSD/ECC hybrid (Markdown/YAML in Git). |

### 6. Top 3 Risks
1.  **[Orchestrator Lock-in]** High dependency on Claude Code's specific hook/slash-command implementation. 
    *   *Mitigation:* Ensure `reprogate` CLI remains fully functional as a standalone tool (standard input/output) so it can be adapted to other orchestrators (e.g., Gemini CLI, Goose).
2.  **[The "Prose-to-Rego" Chasm]** v1 relies on manual conversion of prose skills to OPA/Rego. This is a friction point that may lead to users ignoring the "Skill Evolution" feature.
    *   *Mitigation:* Provide a library of "Standard Rego Patterns" in Phase 1 to make manual authoring easier.
3.  **[Hook Latency/Blocking]** Mandatory hooks on every tool use can feel like "policing" rather than "harnessing."
    *   *Mitigation:* Implement `HOOK-01` profiles strictly, ensuring "minimal" profile has zero network/heavy-file I/O.

### 7. Overall Assessment
**Confidence Level: HIGH**

The transition to a "Delivery Harness" identity is a brilliant strategic move that matches how AI agents are actually used in 2026. The plan is technically grounded in the successful `FOUND-01~05` work and avoids the "over-engineering trap" of building a custom LangGraph orchestrator. Once the phase numbering is reconciled and the research summary is updated to reflect the "Lean CLI" approach over the "Heavy Python Framework" approach, this is a solid foundation for v1.0.

---

## Codex Review

1. **Executive Summary**
The three planning artifacts in PROJECT.md, REQUIREMENTS.md, and ROADMAP.md are mostly internally aligned around the new ECC+GSD harness story. The main problem is not internal coherence, but authority: the repo's canonical product definition in `final-definition.md` still defines ReproGate as a compiler/gatekeeper, and ADR-009 explicitly says the old strategy baseline must be rewritten before normal planning resumes. The requirements are structured and mostly testable, but they miss several integration-contract requirements that are critical for implementation. The research summary is useful for governance and OPA-related foundations, but much of its stack and architecture advice is now stale after the pivot.

2. **Cross-Artifact Consistency**
- `PROJECT.md`, `REQUIREMENTS.md`, and `ROADMAP.md` tell a broadly consistent v1 story: solo-developer, Claude Code-centered, ECC hooks + GSD workflow + thin lifecycle layer.
- The biggest inconsistency is external to the set: `final-definition.md` still describes ReproGate as an artifact-driven compiler/gatekeeper, while ADR-009 says that framing is superseded.
- `PROJECT.md` cites `.github/notes/2026-04-02-reprogate-harness-ecc-gsd.md`, but that file is not present at the referenced path. That weakens traceability for the pivot context.
- `PROJECT.md` uses validated IDs `CORE-01~03`, while `REQUIREMENTS.md` and `ROADMAP.md` use `FOUND-01~05`. That is a real traceability mismatch.
- `PROJECT.md` says activation enforces both command and hook layers, but the requirements mostly specify hook installation and phase commands, not the enforcement contract for the command layer itself.
- Terminology is slightly unstable: `PROJECT.md` says "enterprise delivery harness," while the rest of the milestone artifacts are explicitly scoped to a solo developer MVP.
- `research/SUMMARY.md` does not align with the current direction. It assumes MCP/LangGraph/Pydantic-centered orchestration and a governance-framework identity, not the current Claude Code harness model.

3. **Requirements Gaps**
- `HIGH`: No requirement explicitly updates or supersedes the authoritative strategy baseline. ADR-009 says strategy docs must be rewritten before a new planning cycle is authoritative, but the milestone requirements do not include that prerequisite.
- `HIGH`: No explicit requirement defines how `/rg:*` commands are installed or exposed in Claude Code. The roadmap assumes slash commands exist, but there is no requirement for `.claude/commands/` generation, registration, or compatibility.
- `HIGH`: No explicit requirement defines the command-layer enforcement model. `PROJECT.md` says both layers are enforced, but there is no requirement for what happens when a user edits outside phase flow, bypasses `/rg:*`, or resumes mid-phase.
- `MEDIUM`: `reprogate.yaml` is central to activation and `record_triggers`, but there is no requirement for schema validation, defaults migration, error handling, or versioning of that config.
- `MEDIUM`: Specialist-agent I/O contracts are underspecified. The requirements say "spawn gsd-planner/executor/verifier," but not the invocation contract, expected inputs, failure modes, or how outputs are normalized into phase packets.
- `MEDIUM`: `FOUND-01~05` is sufficient as governance substrate, but not sufficient by itself to de-risk the harness runtime. It gives you CLI, records, OPA, and pre-commit; it does not yet validate Claude Code hooks, slash commands, or sub-agent orchestration.
- `MEDIUM`: Some requirements are still vague at verification level. Examples: "correctly determine when a record is required," "readable summary/share document," and the `learn-eval` verdict categories without acceptance criteria.
- `LOW`: There is no explicit requirement for idempotency of `reprogate init` / `reprogate disable`, even though that will matter in daily use.

4. **Roadmap Concerns**
- `HIGH`: The roadmap is not fully implementation-safe while the canonical product definition remains outdated. That is a governance and traceability blocker more than an engineering blocker, but it matters in this repo.
- `MEDIUM`: Phase ordering is mostly logical for `INIT -> HOOK -> SKILL-EVO -> LIFECYCLE`, but `AGENT -> PHASE` is debatable. The workflow contract should usually define the agent contract, not the other way around.
- `MEDIUM`: A better split would be to establish the phase packet structure and `/rg:discuss-phase` / `/rg:next` workflow shell first, then plug planner/executor/verifier behind it. Otherwise Phase 4 risks building abstract agents before the integration surface is stable.
- `MEDIUM`: Phase 2 and Phase 5 are the largest phases. Hook lifecycle includes multiple Claude Code hooks plus profile behavior plus gate-failure persistence; Phase workflow includes command UX, packet structure, routing, and agent integration.
- `LOW`: Phase 3 may be too small on paper relative to actual ambiguity. Skill evolution touches observation format, clustering, evaluation criteria, storage locations, and the manual handoff to `.rego`.
- `LOW`: Success criteria are mostly directionally good, but some still need more observable outputs or test matrices to be strong completion gates.

5. **Research Staleness**

| Finding | Status |
|---|---|
| OPA/Rego as policy engine and skill-gate substrate | CURRENT |
| Record-backed, artifact-driven execution as core philosophy | CURRENT |
| Silent-failure risk and deterministic verification gates | CURRENT |
| "Mega-policy" trap warning and hierarchical policy design | CURRENT |
| LangGraph as recommended orchestration backbone | STALE |
| Pydantic AI as required structured-output backbone | STALE |
| MCP server as near-term Phase 2 necessity | STALE |
| Three-layer architecture centered on Context/Agentic/Governance via MCP | STALE |
| "All state stored in Git-resident Markdown files" | STALE |
| Team/remote-policy-sync/scaling emphasis as near-term roadmap driver | STALE |
| Claude Code hook semantics and `.claude/settings.json` delivery constraints | MISSING |
| Claude Code slash-command installation and `/rg:*` command surface | MISSING |
| CC-centered sub-agent spawn model and failure-handling contract | MISSING |
| Phase packet schema and `must_haves` contract as the primary integration boundary | MISSING |
| Solo-dev activation UX, disable/idempotency, and recovery behavior | MISSING |

6. **Top 3 Risks**
1. Strategic authority split between pivoted planning artifacts and the still-old canonical strategy docs.  
Mitigation: update `final-definition.md` and linked strategy docs first, then explicitly mark the new planning set as authoritative.

2. Claude Code integration assumptions are the biggest implementation unknown.  
Mitigation: create a small interface spec first for `.claude/settings.json`, slash-command installation, hook lifecycle semantics, and subprocess invocation before broad feature work.

3. v1 scope is wide for one milestone: hooks, skill evolution, three agents, full workflow, and lifecycle surfaces.  
Mitigation: narrow the MVP around activation + hook lifecycle + minimal phase packet workflow, and treat advanced skill evolution and richer agent behavior as optional unless the basic harness loop is already proven.

7. **Overall Assessment**
`MEDIUM`

The milestone artifacts are good enough to show a coherent intended product, but not yet strong enough to be treated as a fully reliable implementation foundation. Internally, the planning set is mostly disciplined: the scope is bounded, requirements are organized, and the roadmap follows a reasonable dependency chain. The confidence drops because the authoritative repo definition still conflicts with the new milestone story, the pivot traceability is partially broken, and the hardest engineering surfaces introduced by the pivot, especially Claude Code hooks, slash commands, and subprocess contracts, are still assumed more than specified.

---

## Consensus Summary

### Agreed Strengths
- PROJECT.md, REQUIREMENTS.md, ROADMAP.md tell a **coherent and consistent** harness pivot story
- Phase ordering (INIT → HOOK → SKILL-EVO → AGENT → PHASE → LIFECYCLE) follows logical dependencies
- Requirements are well-structured with clear traceability (27 active REQ-IDs mapped to 6 phases)
- OPA/Rego foundation and artifact-driven philosophy remain valid and well-preserved
- Scope is bounded — explicitly solo-dev, explicitly defers team features to v2

### Agreed Concerns (Priority Order)

| # | Concern | Severity | Gemini | Codex |
|---|---------|----------|--------|-------|
| 1 | **Research SUMMARY.md is ~40-50% stale** — LangGraph, MCP, Pydantic AI references no longer apply | HIGH | ✓ | ✓ |
| 2 | **Claude Code integration specifics unspecified** — hook semantics, slash command installation, sub-agent contracts | HIGH | ✓ (latency) | ✓ (missing research) |
| 3 | **Strategy docs still reference old identity** — `final-definition.md` says compiler/gatekeeper | HIGH | — | ✓ |
| 4 | **Foundation ID mismatch** — PROJECT.md uses CORE-01~03, REQUIREMENTS.md uses FOUND-01~05 | MEDIUM | ✓ | ✓ |
| 5 | **Hook fail-safe/recovery missing** — no requirement for what happens when hooks crash | MEDIUM | ✓ | ✓ |
| 6 | **Agent I/O contracts underspecified** — invocation, failure modes, output normalization | MEDIUM | — | ✓ |
| 7 | **Phase 2 and Phase 5 are disproportionately large** — may need splitting | LOW | ✓ | ✓ |

### Divergent Views

| Topic | Gemini | Codex |
|-------|--------|-------|
| **Overall Confidence** | HIGH | MEDIUM |
| **Phase 4 vs 5 ordering** | Phase 4 before 5 is correct (agents are building blocks) | Workflow shell should come first, then plug agents |
| **MCP relevance** | Missing from plan — should reconsider | Stale — pivot moved away from MCP |
| **Scope risk** | Manageable — lean harness avoids over-engineering | Wide for one milestone — consider narrowing MVP |
| **Phase 4 sizing** | Could merge into Phase 5 | Acceptable as separate phase |

### Actionable Items (Pre-Planning)

1. **Update strategy docs** — `final-definition.md`, `vision.md`, `roadmap.md`, `product-boundary.md` to reflect harness identity (traceability blocker)
2. **Reconcile foundation IDs** — Align CORE-01~03 (PROJECT.md) with FOUND-01~05 (REQUIREMENTS.md)
3. **Add CC integration research** — Hook semantics, slash command installation, sub-agent spawn model (new research needed)
4. **Update research/SUMMARY.md** — Mark stale sections, add missing sections for CC-specific concerns
5. **Add hook fail-safe requirement** — Fail-open vs fail-closed policy decision needed
6. **Decide Phase 4/5 ordering** — Architecture decision: agents-first or workflow-first?
