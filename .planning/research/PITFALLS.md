# Project Research — Pitfalls

## Summary
Building AI-collaborative engineering frameworks like ReproGate requires navigating the tension between automated enforcement and developer velocity. While gating systems ensure reproducibility, they often introduce "slop" if not carefully calibrated. Key areas of failure include brittle orchestrator logic, policy-as-code complexity at scale, and the degradation of documentation quality when enforced by "context-blind" agents.

## Key Pitfalls

### 1. "Vibe Coding" and the Silent Failure Loop
*Mistakes in AI orchestrator integration (Claude, Gemini, etc.)*
- **Warning Signs**: Agents getting stuck in repetitive "fix-test-fail" loops; costs spiking without corresponding progress; successful "thoughts" but failing implementations.
- **Prevention Strategy**: Implement **Deterministic Validation Gates**. Never trust an agent's self-assessment. Use actual compilers, linters, and test suites as circuit breakers. Implement model routing to use cheaper models for boilerplate and frontier models for complex reasoning.
- **Relevant Phase**: Implementation / Execution

### 2. The "Mega-Policy" Trap and Undefined Behavior
*Issues with scaling repository-wide "Skills" and OPA/Rego gates to multiple teams*
- **Warning Signs**: Large, monolithic `.rego` files that are difficult to debug; "allow-by-default" scenarios occurring when data is missing; merge conflicts in central policy files.
- **Prevention Strategy**: **Decouple Policy from Data.** Use a hierarchical namespace strategy (e.g., `package skills.team_a`) and enforce `default allow = false`. Treat policies as first-class code with their own unit tests (`opa test`) and versioned bundles.
- **Relevant Phase**: Scale / Integration

### 3. "Governance by Policing" & Rationale Hallucination
*Pitfalls in enforcing mandatory documentation (ADRs/RFCs) via agents*
- **Warning Signs**: Developers adding `// arch-ignore` or filler text to bypass bots; AI-generated ADRs that follow the template but contain hallucinated or non-sensical rationale just to "pass the gate."
- **Prevention Strategy**: Shift from policing to **Guidance-based Gating**. Use agents to *draft* the ADR based on code intent, but require human sign-off on the rationale. Implement "baseline" features to ignore legacy violations and focus only on new architectural "one-way door" decisions.
- **Relevant Phase**: Documentation / Gatekeeping

### 4. Context Drift & The Stale Knowledge Gap
*The gap between durable Skills and the evolving codebase*
- **Warning Signs**: AI agents suggesting patterns that were recently deprecated in an ADR; documentation-first architecture becoming "shelfware" that doesn't reflect the actual code.
- **Prevention Strategy**: Establish a **Runtime Feedback Loop**. Ensure that "Skills" are not just static Markdown files but are active inputs to the agent's system prompt. Automate the synchronization between ADR status and the agent's available toolset/constraints.
- **Relevant Phase**: Strategy / Evolution

## Conclusion
The ultimate pitfall in AI-collaborative systems is treating the AI as an autonomous engineer rather than a high-powered compiler of intent. ReproGate's success depends on keeping "human-in-the-loop" at the rationale layer while delegating "grunt-work enforcement" to deterministic gates. Avoiding these pitfalls ensures the framework remains a productivity multiplier rather than a bureaucratic bottleneck.
