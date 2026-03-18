---
skill_id: "verification-present"
name: "검증 기록 필수"
version: "0.1.0"
tags: ["core", "stage-1"]
---

# 검증 기록 필수 (verification-present)

## Goal
모든 RFC와 ADR에 검증(Verification) 섹션이 포함되어 있어야 한다.

## Required Records
- `records/` 내 모든 `.md` 파일에 `## Verification` 섹션이 존재해야 한다.
- Verification 섹션에는 최소 1개의 체크리스트 항목(`- [ ]` 또는 `- [x]`)이 있어야 한다.

## Workflow Expectations
1. RFC를 작성할 때 Verification 섹션에 완료 조건을 명시한다.
2. 작업이 진행되면서 체크리스트를 갱신한다.
3. 모든 항목이 체크되면 작업 완료로 간주한다.

## Verification
- `gatekeeper.py`가 각 기록에 `## Verification` 헤더가 존재하는지 검사한다.
