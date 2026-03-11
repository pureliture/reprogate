# Core Processes (`P0`-`P4`)

> Status: Active

---

## P0. Existing-State Analysis

### Purpose
Understand the current structure, behavior, dependencies, tests, and risks before design or implementation.

### Start Conditions
- The target area already exists.
- Accurate understanding is required before change.

### Inputs
- target feature or module,
- background or issue context,
- related code, configuration, documents, and tests,
- known questions or suspected risks.

### Steps
1. Define the analysis scope.
2. Identify relevant code, config, docs, and tests.
3. Trace the entry points and main flow.
4. Summarize dependencies and boundaries.
5. Separate external contracts from internal behavior.
6. Identify test coverage and validation gaps.
7. Compare documentation with implementation.
8. Record risks and open questions.
9. Recommend the next process.

### Required Deliverables
- scope summary
- current behavior summary
- component and dependency map
- test and document status
- risk list
- open questions
- recommended next process

### Exit Criteria
- the current behavior can be explained,
- key artifacts are identified,
- and the next process is clear.

### Typical Next Processes
- `P1`
- `P2`
- `P3`
- `P4`
- `S3`

---

## P1. Requirement Refinement

### Purpose
Turn a vague request, idea, or expectation into implementable requirements.

### Start Conditions
- The problem or goal is known.
- The implementation scope is still fuzzy.

### Inputs
- request or idea,
- background and goals,
- analysis results when available,
- constraints,
- desired outcome,
- priorities and risks.

### Steps
1. Capture background and intent.
2. Define the problem clearly.
3. Break requirements into implementable units.
4. Separate in-scope from out-of-scope.
5. Record constraints and risks.
6. Compare possible approaches.
7. Define done criteria.
8. Record unresolved questions.
9. Prepare the next-process input.

### Required Deliverables
- refined requirements
- scope / non-scope
- constraints
- done criteria
- decision basis
- unresolved questions
- recommended next process

### Exit Criteria
- implementation scope is clear,
- completion can be judged,
- and downstream execution has enough input.

### Typical Next Processes
- `P3`
- `P4`
- `P0` (additional analysis)

---

## P2. Troubleshooting Strategy

### Purpose
Define root-cause hypotheses and a resolution strategy before changing code.

### Start Conditions
- A symptom or defect is known.
- The cause or fix path is still uncertain.

### Inputs
- symptom,
- reproduction details,
- logs or observations,
- related code, docs, and tests,
- prior analysis when available.

### Steps
1. Define the symptom precisely.
2. Record reproduction and non-reproduction conditions.
3. Estimate impact scope.
4. List plausible hypotheses.
5. Define how each hypothesis will be checked.
6. Compare candidate fixes.
7. Choose the preferred strategy.
8. Define any extra logging or tests needed before fixing.
9. Prepare the handoff to `P4`.

### Required Deliverables
- problem definition
- symptom and reproduction record
- impact estimate
- hypothesis list
- validation plan
- candidate fixes
- chosen strategy
- handoff input for `P4`

### Exit Criteria
- the preferred validation path is clear,
- and there is enough direction to start `P4`.

### Typical Next Processes
- `P4`
- `P0`
- test expansion
- observability work

---

## P3. Feature Delivery

### Purpose
Implement new functionality or structural change safely from refined requirements.

### Start Conditions
- Requirements or design input is ready.
- Scope and done criteria are defined.

### Inputs
- requirement refinement results,
- prior analysis if needed,
- constraints,
- test status,
- document status,
- done criteria.

### Steps
1. Review the execution plan and implementation order.
2. Reconfirm impact scope.
3. Implement the required changes.
4. Add or update tests.
5. Add code comments or explanations where needed.
6. Identify documentation impact.
7. Perform focused refactoring when helpful.
8. Review the implementation.
9. Record the change summary and key decisions.
10. Hand off to review and documentation processes.

### Required Deliverables
- implementation result
- test result or test delta
- change-scope summary
- document-impact list
- refactoring note when relevant
- change record
- decision record

### Exit Criteria
- implementation is complete,
- basic verification ran,
- document impact is identified,
- and the work is ready for review.

### Typical Next Processes
- `S1`
- `S2`
- `S3`
- `S4`

---

## P4. Bug-Fix Delivery

### Purpose
Correct a known problem, reduce recurrence risk, and verify the resolution.

### Start Conditions
- The issue is identified.
- A cause analysis or resolution strategy exists.

### Inputs
- troubleshooting results,
- prior analysis if needed,
- problem definition,
- reproduction conditions,
- impact scope,
- chosen fix direction.

### Steps
1. Check that the fix direction matches the problem definition.
2. Record the expected before/after behavior.
3. Implement the fix.
4. Add or update regression tests.
5. Recheck impact scope.
6. Review the fix result.
7. Classify documentation impact.
8. Record the change summary and decisions.
9. Hand off to review and documentation processes.

### Required Deliverables
- fix summary
- before/after validation criteria
- regression-test delta
- impact review result
- change record
- decision record

### Exit Criteria
- the defect is fixed,
- the resolution can be validated,
- and regression protection exists.

### Typical Next Processes
- `S1`
- `S2`
- `S4`
