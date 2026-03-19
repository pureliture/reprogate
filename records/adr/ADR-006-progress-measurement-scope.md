---
record_id: "ADR-006"
title: "Progress Measurement Scope — Full Roadmap Coverage"
type: "adr"
status: "Accepted"
created_at: "2026-03-19"
extends: "ADR-005"
tags: ["progress", "roadmap", "measurement"]
---

# ADR-006: Progress Measurement Scope — Full Roadmap Coverage

## Status
Accepted

## Context
ADR-005에서 progress reporting 시스템을 `meta/progress/`에 격리하기로 결정했다. 그러나 ADR-005는 **"어디에 둘 것인가"** 만 다루었고, **"무엇을 측정할 것인가"** 는 명시하지 않았다.

PR #12에서 초기 구현된 `progress-map.yaml`은 4개 stage만 포함했다:
- Foundation
- Canonical definition & Product boundary
- Record-backed core
- ReproGate identity transition

그러나 `docs/strategy/roadmap.md`에는 8개 stage가 정의되어 있다:
- Foundation
- Near-Term 1: Canonical definition & Product boundary
- Near-Term 2: Record-backed core implementation
- Near-Term 3: ReproGate identity transition
- Mid-Term: Multi-entry & Late binding
- Mid-Term: Stronger adapter surfaces
- Long-Term: Team operating standard
- Long-Term: Optional integrations

결과적으로 전체 진척도가 79%로 과대 계산되었으나, 실제 roadmap 기준으로는 약 42%다.

## Decision
`progress-map.yaml`은 `docs/strategy/roadmap.md`에 정의된 **전체 stage를 반영**해야 한다.

구체적으로:
1. roadmap.md의 모든 stage(8개)를 progress-map.yaml에 포함한다
2. 각 stage의 weight는 roadmap에서의 실제 비중을 반영한다
3. 중기/장기 stage는 아직 issue/PR이 없더라도 `manual_placeholder`로 포함하여 전체 분모에 반영한다
4. 전체 진척도(overall)는 roadmap 전체 weight 합계를 분모로 계산한다

## Consequences
- 긍정: 전체 진척도가 실제 roadmap 대비 정확하게 표시됨
- 긍정: 중기/장기 목표가 시각화에 포함되어 전체 방향성이 보임
- 중립: 아직 시작하지 않은 stage는 0%로 표시되어 전체 수치가 낮아 보일 수 있음
- 중립: roadmap.md 변경 시 progress-map.yaml도 함께 갱신 필요

## Verification
- [ ] progress-map.yaml이 8개 stage를 모두 포함
- [ ] 전체 진척도가 roadmap 전체 기준으로 계산됨 (예상: ~42%)
- [ ] 중기/장기 stage가 시각화에 표시됨
- [ ] README.md에 progress 링크 추가
