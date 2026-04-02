## Context

Phase 02 (Hook Lifecycle)가 완료되어 `Stop` hook이 세션 종료 시 실행되는 기반이 갖춰졌다. 그러나 hook이 캡처한 세션 정보를 **structured instinct YAML**로 변환하고, 품질 검증 후 **prose skill**로 승격하는 파이프라인이 아직 없다.

현재 상태:
- `reprogate_hook_stop.py`가 존재하지만 observation 추출 로직이 없음
- `/learn-eval` 커맨드가 정의되지 않음
- `~/.claude/homunculus/instincts/` 디렉토리 구조가 미정

제약:
- ADR-012: v1은 prose instinct까지만 자동화. `.rego` 변환은 v2로 defer
- ADR-013: hook은 repo-local `.claude/settings.json`을 통해 전달
- instinct 및 evolved skill은 user-level 경로 (`~/.claude/homunculus/`)에 저장 — Git 외부

## Goals / Non-Goals

**Goals:**
- `Stop` hook에서 세션 observation YAML 자동 초안 생성
- `/learn-eval` 커맨드로 instinct 품질 평가 및 prose skill 저장
- instinct → prose skill 경로의 end-to-end 흐름 구현

**Non-Goals:**
- prose instinct → `.rego` 자동 변환 (v2 defer, ADR-012)
- instinct 클러스터링 (`/evolve` ECC 기능) — v2 범위
- 팀 단위 skill 공유 또는 원격 동기화 — v2 범위
- 기존 `.rego` 정책 수정 — 수동 유지

## Decisions

### Decision 1: Stop hook에서 LLM-assisted observation 생성

**선택**: Stop hook 실행 시 세션 대화 요약을 LLM에게 넘겨 instinct YAML 초안을 생성.

**대안 검토**:
- *규칙 기반 추출*: 패턴 매칭으로 관찰 추출 → 유연성 낮음, 새 패턴 커버 불가
- *사용자 수동 입력*: 세션 후 개발자가 직접 작성 → 파이프라인 자동화 목적에 반함

**근거**: LLM이 이미 세션 컨텍스트를 보유하므로 Stop hook 시점에 자연스럽게 요약 가능. instinct YAML은 초안이므로 품질 게이트(`/learn-eval`)에서 검증.

### Decision 2: instinct YAML 스키마

```yaml
# ~/.claude/homunculus/instincts/<session-id>.yaml
id: <uuid>
session_id: <claude-session-id>
captured_at: <ISO8601>
observations:
  - pattern: "<반복된 작업 패턴 설명>"
    frequency: <int>  # 세션 내 관찰 횟수
    trigger: "<어떤 상황에서 패턴이 발생했나>"
    suggested_skill_name: "<kebab-case>"
confidence: low | medium | high
raw_summary: "<세션 요약 원문>"
```

**근거**: 최소 필수 필드만 포함하여 LLM이 채우기 쉽고 `/learn-eval`이 평가하기 충분한 구조.

### Decision 3: `/learn-eval` — 대화형 품질 게이트

Stop hook은 instinct YAML 초안만 생성. 개발자가 세션 후 `/learn-eval`을 실행하면:
1. 미평가 instinct YAML 목록 표시
2. 개발자가 선택한 instinct를 LLM과 함께 리뷰
3. 통과 시 `~/.claude/homunculus/evolved/skills/<name>.md`로 prose skill 생성 및 저장

**대안**: Stop hook에서 즉시 prose skill까지 자동 생성 → 품질 게이트 없이 저품질 skill이 누적될 위험.

**근거**: 세션 직후 자동 승격은 노이즈가 많다. `/learn-eval`이라는 명시적 리뷰 스텝이 skill 품질을 보장한다.

## Risks / Trade-offs

- **[Risk] Stop hook LLM call latency** → 세션 종료 시 사용자 체감 지연. Mitigation: observation 생성을 비동기 또는 백그라운드 실행.
- **[Risk] 낮은 `/learn-eval` 사용률** → 개발자가 커맨드를 잊으면 instinct가 누적만 됨. Mitigation: Stop hook이 미평가 instinct 수를 알림 메시지로 표시.
- **[Risk] instinct YAML 품질 불균일** → LLM 생성 초안의 관찰 정확도가 세션 품질에 따라 달라짐. Mitigation: `confidence` 필드로 낮은 신뢰도 초안 필터링.
- **[Trade-off] User-level 저장** → Git 추적 불가. 의도적 결정: personal instinct는 레포 공개 범위 밖.

## Migration Plan

1. `reprogate_hook_stop.py`에 observation extraction 함수 추가
2. `.claude/commands/learn-eval.md` 슬래시 커맨드 생성
3. `~/.claude/homunculus/instincts/` 및 `~/.claude/homunculus/evolved/skills/` 디렉토리 초기화는 첫 실행 시 자동 생성
4. 기존 Stop hook 동작 (gate failure 로깅 등)은 변경 없음 — 신규 기능 추가만

롤백: `reprogate_hook_stop.py`에서 observation 블록 제거, `learn-eval.md` 삭제로 원복 가능.

## Open Questions

- ~~Stop hook에서 LLM call이 Claude Code API를 직접 호출할 수 있는가?~~ → **해소됨** ([ADR-016](../../../../records/adr/ADR-016-stop-hook-observation-mechanism.md)): Stop hook은 LLM 없이 template YAML만 생성. LLM 분석은 `/rg:learn-eval` 실행 시점에 수행.
- instinct YAML의 `session_id`는 Claude Code가 제공하는가, 아니면 임의 UUID를 생성해야 하는가? → `session_stop.py` 확인 결과 `current-session.json`에서 읽거나 timestamp 기반 fallback ID 사용 (기존 구현 재사용 가능).
