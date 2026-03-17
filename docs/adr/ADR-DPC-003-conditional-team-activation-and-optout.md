# ADR-DPC-003: 조건부 Team 활성화 및 프로세스 미적용(NONE) 분기 허용

## Status

**Accepted** (2026-03-08)

## Context

`/ai-ops` 실행 시 사용자 프로세스 선택 전에 Team mode가 자동 활성화되어,
Stop hook의 "Continue working" 루프와 결합된 대기 반복 문제가 발생했다.

실행 로그에서 아래가 확인되었다.
- `keyword_detected: team`
- `mode_change: none -> team`
- `skill_invoked: oh-my-claudecode:team`

또한 기존 정책은 "AI Ops 작업은 반드시 Team 구성"을 전제했기 때문에,
사용자가 프로세스 적용을 원하지 않는 경우(`NONE`)를 처리할 운영 규칙이 부재했다.

## Decision

### 1. `/ai-ops` 실행 모델을 3단계로 고정

1. 프로세스 추천
   - `P0~P4`, `S1~S4` 중 권장 1개 + 대안 제시
2. 사용자 선택 분기
   - 선택: 해당 프로세스로 착수
   - `NONE`: 일반 작업(single-agent)으로 수행
3. Team 조건부 활성화
   - 사용자 프로세스 선택 완료 + 다중 역할 검증 필요 시에만 활성화

### 2. Team 필수 규칙을 조건부 규칙으로 변경

- 기존: "AI Ops 작업은 반드시 Team 구성"
- 변경: "프로세스 선택 후 필요 조건을 만족할 때만 Team 활성화"

필요 조건 예시:
- 다중 파일 또는 고위험 변경
- 리뷰 강도 요구
- 사용자 명시 요청

Team 사용 가능 프로세스 기본값:
- `P3`, `P4`, `S3` (필요 시 `S1`)

Team 미사용 프로세스:
- `G0`, `P0`, `P1`, `P2`, `S2`, `S4`, `NONE`

### 3. 오탐 안전장치 추가

- `/ai-ops` 호출 직후 Team mode 오탐이 감지되면:

```bash
/oh-my-claudecode:cancel --force
```

로 `none` 상태 복귀 후 프로세스 선택 질의를 재개한다.

### 4. 운영 문서 참조 경로 고정

도구 명령/규칙 문서는 `ai-collaboration-guide.md` 직접 참조 대신
아래 분해 문서를 참조한다.

- `docs/process-catalog/process-selection-guide.md`
- `docs/process-catalog/P0-P4-core-processes.md`
- `docs/process-catalog/S1-S4-support-processes.md`

### 5. 프로세스 컨텍스트 기록 및 훅 연동

선택된 프로세스는 컨텍스트 파일로 기록하고 훅에서 참조한다.

```bash
python3 scripts/set_process_context.py --process <P0~P4|S1~S4|G0|NONE> --wp <WP-ID>
```

Claude PreToolUse 가드는 다음 원칙으로 차단/허용한다.
- `G0/P0/P1/P2/S1/S2/S4`: 읽기/문서 중심 작업만 허용
- `P3/P4/S3/NONE`: 구현 작업 허용

### 6. 최소 논리 역할 프로파일 도입

프로세스 보장을 위해 도구/팀원 이름과 무관한 최소 논리 역할 세트를 도입한다.

- 기준 문서: `docs/process-catalog/minimum-logical-role-set.md`
- Team 가능 프로세스(`P3`, `P4`, `S3`, 필요 시 `S1`)는 `team_mode=auto` 상태에서 구현 변경 금지
- Team 경로(`team_mode=team`)에서는 최소 역할 프로파일 미충족 시 PreToolUse에서 차단

최소 프로파일 예시:
- `DELIVERY_MIN3`: `executor`, `verifier`, `recorder`
- `ANALYSIS_MIN2`: `analyst`, `verifier`

### 7. 팀원별 실제 역할 매핑 강제

Team 경로(`team_mode=team`)에서는 논리 역할 집합뿐 아니라
각 팀원에 대한 실제 역할 매핑(`member:role`)을 반드시 기록한다.

- OMC 사용 시: OMC 에이전트 이름 기준으로 매핑
- OMC 미사용 시: Claude native 팀원 식별자 기준으로 동일 매핑

PreToolUse 가드는 `--members`가 없거나 필수 역할이 누락된 경우 구현 변경을 차단한다.

## Consequences

### 긍정적

- 사용자 선택 전에 Team이 켜지는 오작동을 방지할 수 있다.
- 프로세스 미적용(`NONE`) 요구를 정책 위반 없이 처리할 수 있다.
- 프로세스 기반 협업과 일반 작업 경로를 명시적으로 분리할 수 있다.
- 프로세스별 필수 역할이 고정되어 팀원 변동 시에도 최소 품질선을 유지할 수 있다.
- OMC 사용 유무와 무관하게 동일한 역할 책임 구조를 유지할 수 있다.

### 부정적

- Team 강제 정책 대비 일관성 관리 포인트가 증가한다.
- `NONE` 경로가 남용되면 프로세스 적용률이 낮아질 수 있다.

### 완화 조치

- `NONE` 선택 시 사유와 리스크를 기록한다.
- 종료 전 `S1/S2/S4` 연결 필요 여부를 재제안한다.
- WP/CHANGELOG에 적용 이력을 남긴다.

## Related

- [WP-DPC-2026-03-005](../archive/ai-ops/work-packets/WP-DPC-2026-03-005-process-based-collaboration.md)
- [ops-bootstrap-master-plan.md](../governance/ops-bootstrap-master-plan.md)
- [ADR-DPC-002](./ADR-DPC-002-goal-alignment-process.md)
- [ai-ops command](../commands/ai-ops.md)
