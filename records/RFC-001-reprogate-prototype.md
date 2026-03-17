---
record_id: "RFC-001"
title: "ReproGate 프로토타입 구축"
type: "rfc"
status: "Accepted"
created_at: "2026-03-18"
tags: ["prototype", "stage-0", "bootstrap"]
---

# RFC-001: ReproGate 프로토타입 구축

## Status
Accepted

## Summary
ReproGate 프레임워크의 최소 동작 루프(기록 → 검사 → 차단)를 이 저장소 자체에 적용하여, Self-Hosting 방식으로 프로토타입을 구축한다.

## Motivation
ReproGate의 핵심 주장은 "기록 기반 작업만이 강제 가능하다"이다. 이를 증명하는 가장 강력한 방법은 ReproGate 자신이 이 규칙을 따르며 만들어지는 것이다.

## Design / Proposal

### Stage 0 구성요소
1. `reprogate.yaml` — 이 저장소의 실제 config
2. `records/` — RFC, ADR 작업 기록 저장
3. `skills/record-required/` — 첫 번째 Skill (기록 필수 강제)
4. `gatekeeper.py` — 기본 파일 존재 검사 (OPA 없이)

### Record Template
- 의사결정 기록: ADR (Michael Nygard 원본)
- 작업 계획 기록: RFC (Rust RFC / Oxide RFD 변형 + Verification 확장)

### 문서 구조
- 모든 문서에 YAML Frontmatter 필수화 (notesmd-cli 호환)
- Frontmatter만으로 gate 평가 가능하도록 설계

## Alternatives Considered
- 외부 프로젝트에 먼저 적용 후 프레임워크 구축 → Self-Hosting의 설계 피드백 루프를 잃음
- 전체 기능을 완성한 후 적용 → 점진적 개선 불가, 완벽주의 함정

## Unresolved Questions
- OPA/Rego 엔진 연동 시점 (Stage 1에서 진행)
- npm 패키지 배포 구조 확정 (Stage 2에서 진행)

## Verification
- [x] `reprogate.yaml`이 저장소 루트에 생성됨
- [x] 이 RFC 자체가 첫 번째 Work Record로 존재함
- [ ] `gatekeeper.py`가 records 존재 여부를 실제로 검사하고 pass/fail 반환
- [ ] `skills/record-required/`에 첫 번째 Skill이 존재
