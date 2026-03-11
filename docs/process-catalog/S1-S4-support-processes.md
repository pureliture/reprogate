# Support Processes (`S1`-`S4`)

> Status: Active

---

## S1. Work Review

### Purpose
Check whether the result matches the intent, scope, and done criteria, and detect omissions, over-implementation, or side effects.

### Start Conditions
- implementation-oriented work such as `P3` or `P4` is complete,
- and reviewable artifacts exist.

### Inputs
- background,
- requirements or problem definition,
- implementation result,
- test result,
- change scope,
- done criteria.

### Steps
1. Reconfirm the original intent and done criteria.
2. Review the actual result.
3. Detect missing pieces.
4. Check for scope creep or over-implementation.
5. Check for test, document, or refactoring gaps.
6. Choose the next action when follow-up is needed.

### Required Deliverables
- review result
- gap or follow-up list
- approve / rework decision
- recommended next process

### Exit Criteria
- an approval or rework judgment exists,
- and the next action is clear.

### Typical Next Processes
- `S2`
- `S3`
- `S4`
- `P3`
- `P4`

---

## S2. Documentation Refresh

### Purpose
Identify and update affected documents to reduce outdated, duplicated, or conflicting information.

### Start Conditions
- code, configuration, structure, or operating behavior changed,
- and documentation impact is expected.

### Inputs
- change summary,
- candidate documents,
- current document structure,
- audience and sharing needs.

### Steps
1. Identify affected documents.
2. Prioritize mandatory updates.
3. Resolve duplicate or conflicting descriptions.
4. Update tables, diagrams, and explanations as needed.
5. Check reader-specific needs.
6. Record the documentation change history.

### Required Deliverables
- updated-document list
- applied changes
- deferred-document list
- documentation history note

### Exit Criteria
- all mandatory documentation updates are complete,
- and deferred work is identified.

### Typical Next Processes
- `S4`
- follow-up packet creation

---

## S3. Refactoring

### Purpose
Improve structure and maintainability after change accumulation while preserving intended behavior.

### Start Conditions
- complexity has risen,
- cleanup is justified,
- or large work left the structure harder to maintain.

### Inputs
- structural pain points,
- recent change history,
- desired design principles,
- impact scope.

### Steps
1. Identify the structural problem.
2. Define the refactoring goal.
3. Break work into safe units.
4. Check the available safety net.
5. Apply the structural improvement.
6. Validate functional equivalence or intended improvement.
7. Check documentation and recording impact.

### Required Deliverables
- refactoring goal
- structure-change summary
- safety-net review result
- follow-up documentation or record targets

### Exit Criteria
- the structural improvement is complete,
- expected behavior is preserved,
- and the result is ready for review.

### Typical Next Processes
- `S1`
- `S2`
- `S4`

---

## S4. Change / Decision Recording

### Purpose
Preserve not only what changed, but also why it changed, so the work remains reusable across sessions, tools, reviews, and retrospectives.

### Start Conditions
- a meaningful change or decision occurred.

### Inputs
- background,
- actual change result,
- review outcome,
- document updates,
- selected approach,
- rejected alternatives and reasoning.

### Steps
1. Record background and intent.
2. Summarize the actual change.
3. Record the selected approach and why it was chosen.
4. Record rejected alternatives when relevant.
5. Record remaining risks and TODOs.
6. Link the result to related tasks, documents, or commits.

### Required Deliverables
- change history
- decision record
- related links
- remaining TODOs or risks

### Exit Criteria
- the result and reasoning are traceable.

### Typical Next Processes
- completion
- new follow-up packet
- downstream handoff
