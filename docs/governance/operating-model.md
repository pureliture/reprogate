# AI Ops Operating Model

> Status: Active
> Version: `1.0.0`

## 1. Purpose

This document records the operating model for teams that use AI tools through a process-based workflow.
It serves as the high-level reference above process definitions, templates, and tool-specific adapters.

## 2. Background

AI-assisted development is fast, but informal chat-only execution creates repeatable problems:

- context resets between sessions,
- weak traceability for intent and decisions,
- inconsistent review and documentation follow-up,
- tool confusion about project boundaries,
- and drift between what changed and why it changed.

AI Ops addresses those problems by treating AI work as a governed delivery workflow rather than a one-shot prompt exchange.

## 3. North Star

> Run AI-assisted work through explicit processes and file-backed artifacts,
> not through unstructured prompt history alone.

## 4. Core Principles

### 4.1 Treat AI as a workflow participant
AI tools should act like project collaborators that follow shared rules, read shared documents, and leave reusable outputs.

### 4.2 Manage work by process, not by prompt
Before execution, classify the work:

- what kind of task it is,
- which process fits,
- which prerequisites exist,
- which follow-up steps are required,
- and what proves completion.

### 4.3 Record intent as well as results
A durable project needs the reasoning behind changes, not just the diffs.
At minimum, preserve background, goals, chosen approach, rejected alternatives, completion criteria, and follow-up risks.

### 4.4 Treat documentation as an operational asset
Documentation is part of the delivery system.
It preserves context across sessions, tools, reviewers, and future maintainers.

### 4.5 Include review by default
Implementation alone is not completion.
Whenever practical, connect execution to verification, documentation, and decision recording.

## 5. Concept Model

### Process
A repeatable unit of work such as analysis, refinement, implementation, review, or recording.

### Mode
The execution posture an AI tool currently uses, such as analysis, planning, implementation, review, or documentation.

### Agent / Skill
A trigger or interface used to carry out a process quickly and consistently.

## 6. Portability Boundary

Project-specific details such as runtime versions, branch strategy, workspace layout, legacy constraints, and deployment rules belong in adapter-owned assets.
The core AI Ops framework should stay portable across repositories and organizations.

## 7. Expected Transition

### From
- session-dependent prompting
- scattered reasoning
- weak review discipline
- mixed framework and project concerns

### To
- process-first execution
- file-backed traceability
- explicit verification and recording
- clean separation between framework and adapter assets

## Related Documents

- [Constitution](./governance/constitution.md)
- [Process Catalog](./process-catalog/README.md)
