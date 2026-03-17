# ReproGate Operating Model

> Status: Active
> Version: `1.0.0`

## 1. Purpose

This document records the repository-level operating model for teams that use ReproGate with AI tools.
It serves as the governance reference above process definitions, templates, and tool-specific adapters.

It does **not** replace the product definition in `docs/strategy/final-definition.md`; instead, it explains how this repository operates around that definition.

## 2. Background

AI-assisted development is fast, but informal chat-only execution creates repeatable problems:

- context resets between sessions,
- weak traceability for intent and decisions,
- decisions that are difficult to explain after the fact,
- inconsistent review and documentation follow-up,
- tool confusion about project boundaries,
- and drift between what changed and why it changed.

ReproGate addresses those problems by treating AI work as record-backed engineering rather than a one-shot prompt exchange.

## 3. North Star

> Run AI-assisted work through explicit work records, Skills, and gates,
> not through unstructured prompt history or opaque runtime state alone.

## 4. Core Principles

### 4.1 Treat AI as a workflow participant
AI tools should act like project collaborators that follow shared rules, read shared documents, and leave reusable outputs.

### 4.2 Record before relying on memory
If work must be explainable, reviewable, or enforceable later, the intent and reasoning need to exist as inspectable records.

### 4.3 Treat work records as operational assets
A durable project needs the reasoning behind changes, not just the diffs.
At minimum, preserve background, goals, chosen approach, rejected alternatives, completion criteria, and follow-up risks.

### 4.4 Enforce through artifacts, not hidden state
Gates should inspect concrete records and outputs whenever possible.
Runtime state may help resume work, but it is not sufficient as the primary evidence model.

### 4.5 Include review by default
Implementation alone is not completion.
Whenever practical, connect execution to verification, documentation, and decision recording.

## 5. Concept Model

### Work Record
An inspectable artifact that preserves intent, scope, decisions, progress, or verification.

### Skill
A reusable working pattern captured in text and later enforceable through rules and gates.

### Gate
A rule-enforcement surface that inspects artifacts and blocks work when required evidence is missing.

### Process
A repository-level execution aid used to structure delivery work and governance. Processes are part of the operating surface of this repository, not the sole definition of the product.

### Mode
The execution posture an AI tool currently uses, such as analysis, planning, implementation, review, or documentation.

## 6. Portability Boundary

Project-specific details such as runtime versions, branch strategy, workspace layout, legacy constraints, and deployment rules belong in adapter-owned assets.
The core ReproGate framework should stay portable across repositories and organizations.

## 7. Expected Transition

### From
- session-dependent prompting
- opaque runtime state
- missing rationale
- mixed framework and project concerns

### To
- record-backed execution
- explainable decisions
- explicit verification and gateable artifacts
- clean separation between framework and adapter assets

## Related Documents

- [Canonical Definition](../strategy/final-definition.md)
- [Vision](../strategy/vision.md)
- [Roadmap](../strategy/roadmap.md)
- [Constitution](./constitution.md)
- [Process Catalog](../process-catalog/README.md)
