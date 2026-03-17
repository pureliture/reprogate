---
skill_id: "record-required"
name: "작업 기록 필수"
version: "0.1.0"
tags: ["core", "stage-0"]
---

# 작업 기록 필수 (record-required)

## Goal
의미 있는 모든 변경 전에 Work Record(RFC 또는 ADR)를 작성한다.

## Required Records
- `records/` 디렉토리에 YAML Frontmatter가 포함된 `.md` 파일이 1개 이상 존재해야 한다.
- Frontmatter에는 `record_id`, `type`, `status` 필드가 반드시 포함되어야 한다.

## Workflow Expectations
1. 작업 시작 전에 RFC 또는 ADR을 작성한다.
2. 작업 중 의사결정이 발생하면 ADR로 기록한다.
3. 기록 없이 코드를 변경하면 Gate가 차단한다.

## Verification
- `gatekeeper.py`가 `records/` 내 `.md` 파일의 존재를 검사한다.
- Frontmatter의 `status` 필드가 `Draft` 이상이어야 통과한다.
