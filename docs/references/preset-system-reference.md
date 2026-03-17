# 프리셋 시스템 레퍼런스

> dpc 프리셋 시스템 설계의 근거 문서

---

## 1. 공식 레퍼런스

| 항목 | 레퍼런스 | 출처 |
|------|----------|------|
| 메타데이터 스키마 | npm package.json | [npm 공식](https://docs.npmjs.com/cli/v11/configuring-npm/package-json/) |
| 배포/상속 방식 | ESLint shareable config | [ESLint 공식](https://eslint.org/docs/latest/extend/shareable-configs) |
| extends 패턴 | Renovate presets | [Renovate 공식](https://docs.renovatebot.com/config-presets/) |
| 프리셋 구조 | Babel presets | [Babel 공식](https://babeljs.io/docs/presets) |

---

## 2. 메타데이터 스키마: npm package.json

> 출처: [npm 공식 문서](https://docs.npmjs.com/cli/v11/configuring-npm/package-json/)

### 2.1 필수 필드

| 필드 | 규칙 | 공식 인용 |
|------|------|----------|
| **name** | 소문자, URL-safe | "must be lowercase, no spaces, hyphens/underscores allowed" |
| **version** | semver 형식 | "must be in the form x.x.x and follow semantic versioning" |

> "The name and version together form an identifier that is assumed to be completely unique."

### 2.2 선택 필드

| 필드 | 용도 |
|------|------|
| description | 패키지 설명 (검색에 사용) |
| keywords | 태그 배열 (검색에 사용) |
| author | 작성자 정보 |
| main | 진입점 파일 |

### 2.3 dpc preset.yaml 적용

| npm | dpc | 채택 이유 |
|-----|-----|----------|
| name | name | 프리셋 식별자 |
| version | version | 버전 관리 |
| description | description | 프리셋 설명 |
| keywords | tags | 검색/분류 |
| - | extends | Renovate에서 채택 |

---

## 3. extends 패턴: Renovate

> 출처: [Renovate 공식 문서](https://docs.renovatebot.com/config-presets/)

### 3.1 extends 동작

```json
{
  "extends": ["config:recommended", "schedule:nonOfficeHours"]
}
```

> "Presets referenced with extends are resolved first and take lower precedence over regular config."

### 3.2 우선순위

> "If there is a logical conflict between presets, then the last preset in the extends array wins."

### 3.3 기본 파일

> "If you omit a file name, Renovate will look for a default.json file."

### 3.4 dpc 적용

| Renovate | dpc | 채택 이유 |
|----------|-----|----------|
| extends 배열 | extends 단일값 | 단순화 (1개만 상속) |
| default.json | preset.yaml | 진입점 명시 |
| 마지막 우선 | 하위 우선 | 동일 패턴 |

---

## 4. ESLint Shareable Config

> 출처: [ESLint 공식 문서](https://eslint.org/docs/latest/extend/shareable-configs)

### 1.1 ESLint 구조

| 항목 | ESLint | 출처 |
|------|--------|------|
| 배포 방식 | npm 패키지 | [Share Configurations](https://eslint.org/docs/latest/extend/shareable-configs) |
| 네이밍 | `eslint-config-*`, `@scope/eslint-config` | 동일 |
| 진입점 | `index.js` (설정 객체 export) | 동일 |
| 상속 | `extends: [config]` | 동일 |
| 오버라이드 | import 후 rules 추가 | 동일 |
| 다중 설정 | 패키지 내 여러 파일 export | 동일 |

### 1.2 ESLint 패키지 구조

```
eslint-config-myconfig/
├── package.json
├── index.js              # 기본 설정 export
└── strict.js             # 추가 설정 (선택)
```

```javascript
// index.js
export default [
  {
    rules: { semi: [2, "always"] }
  }
];
```

```json
// package.json
{
  "name": "eslint-config-myconfig",
  "main": "index.js",
  "peerDependencies": { "eslint": ">= 9" },
  "keywords": ["eslint", "eslintconfig"]
}
```

### 1.3 ESLint 사용 방식

```javascript
// eslint.config.js
import myconfig from "eslint-config-myconfig";

export default [
  ...myconfig,
  {
    rules: { "no-unused-vars": "warn" }  // 오버라이드
  }
];
```

---

## 2. dpc 프리셋 vs ESLint

### 2.1 채택한 패턴

| 패턴 | ESLint | dpc | 채택 이유 |
|------|--------|-----|----------|
| npm 배포 | ✓ | ✓ | 표준 패키지 생태계 활용 |
| 네이밍 규칙 | `eslint-config-*` | `dpc-preset-*` | 일관된 발견성 |
| extends 상속 | ✓ | ✓ | 프리셋 계층화 |
| 오버라이드 | rules 추가 | override 필드 | 설정 수정 용이성 |
| 로컬 설정 | 프로젝트 내 config | `.dpc/presets/` | 프로젝트별 커스텀 |

### 2.2 차별화된 설계

| 항목 | ESLint | dpc | 이유 |
|------|--------|-----|------|
| **설정 형식** | JavaScript 객체 | YAML + Markdown | LLM 친화적 (자연어) |
| **규칙 분리** | 단일 rules 객체 | guidelines + rules | 의도(soft) vs 보장(hard) 분리 |
| **로딩 위치** | node_modules만 | builtin → global → local → npm | 유연한 오버라이드 |
| **메타데이터** | package.json | preset.yaml | 프리셋 전용 메타 |

### 2.3 핵심 차별점: 하이브리드 구조

ESLint는 **규칙(rules)만** 정의한다:
```javascript
{ rules: { "semi": "error" } }
```

dpc는 **의도(guidelines) + 보장(rules)**을 분리한다:
```yaml
# guidelines.md - LLM이 이해하는 자연어
"세미콜론을 항상 사용하세요. 일관성이 중요합니다."

# rules.yaml - Gate가 강제하는 규칙
- id: "require-semi"
  trigger: "write"
  require: "semicolon at end of statement"
```

**이유**: LLM은 자연어를 더 잘 이해하지만, 100% 준수를 보장하지 않는다.
따라서 guidelines로 **의도를 전달**하고, rules로 **준수를 강제**한다.

---

## 3. 로딩 우선순위 근거

### 3.1 ESLint 방식

ESLint는 `node_modules`에서만 로드한다:
```
node_modules/eslint-config-* → 로드
```

프로젝트 로컬 설정은 `eslint.config.js`에 직접 작성한다.

### 3.2 dpc 방식

dpc는 다중 위치에서 로드한다:
```
1. builtin (dpc 패키지 내장)
2. global (~/.dpc/presets/)
3. local (.dpc/presets/)
4. npm (node_modules/)
```

**채택 이유**:

| 위치 | 용도 | ESLint 대응 |
|------|------|-------------|
| builtin | 공식 프리셋 (tdd, minimal) | eslint:recommended |
| global | 사용자 개인 표준 | 없음 (dpc 고유) |
| local | 프로젝트 커스텀 | eslint.config.js 직접 작성 |
| npm | 조직/커뮤니티 공유 | eslint-config-* |

**global 추가 이유**:
- 개인 개발자가 모든 프로젝트에 일관된 방법론 적용
- npm 배포 없이 개인 표준 유지
- ESLint에는 없는 dpc 고유 기능

---

## 4. 오버라이드 우선순위 근거

### 4.1 ESLint 방식

```javascript
// 나중에 정의된 것이 우선
export default [
  ...recommendedConfig,  // 기본
  ...strictConfig,       // 오버라이드
  { rules: { ... } }     // 최종 오버라이드
];
```

배열 순서로 우선순위 결정.

### 4.2 dpc 방식

```yaml
preset: "tdd"
override:
  guidelines: "..."
  rules: [...]
methodology:
  guidelines: "..."
  rules: [...]
```

명시적 레벨로 우선순위 결정:
```
methodology > override > preset > default
```

**채택 이유**:
- 배열 순서보다 **의도가 명확**
- `override`는 프리셋 수정, `methodology`는 완전 대체
- 실수로 순서 바꿔서 설정 깨지는 문제 방지

---

## 5. 결론

### 5.1 ESLint에서 채택

- npm 패키지 배포
- 네이밍 규칙 (`dpc-preset-*`)
- extends 상속 구조
- 오버라이드 지원

### 5.2 dpc 고유 설계

- **하이브리드**: guidelines(의도) + rules(보장)
- **다중 로딩 위치**: global 레벨 추가
- **선언적 설정**: JS 대신 YAML/Markdown
- **명시적 우선순위**: methodology > override > preset

### 5.3 설계 원칙

> "ESLint의 검증된 패턴을 따르되, LLM 협업에 최적화된 구조로 확장한다"

---

## 6. 참고 자료

- [ESLint Share Configurations](https://eslint.org/docs/latest/extend/shareable-configs)
- [ESLint Configuration Files](https://eslint.org/docs/latest/use/configure/configuration-files)
- [ESLint Stylistic Config Presets](https://eslint.style/guide/config-presets)
