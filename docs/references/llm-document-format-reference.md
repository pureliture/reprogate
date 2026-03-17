# LLM 친화적 문서 포맷 레퍼런스

> dpc guidelines.md 포맷 설계의 근거 문서

---

## 1. 공식 출처

| 도구 | 문서 | 출처 |
|------|------|------|
| Claude Code | CLAUDE.md | [Anthropic 공식](https://code.claude.com/docs/en/memory) |
| Codex CLI | AGENTS.md | [OpenAI 공식](https://developers.openai.com/codex/guides/agents-md/) |
| 웹 표준 | llms.txt | [llmstxt.org](https://llmstxt.org/) (Linux Foundation) |

---

## 2. CLAUDE.md 공식 가이드라인

> 출처: [Anthropic 공식 문서](https://code.claude.com/docs/en/memory)

### 2.1 공식 권장사항

| 항목 | 권장 | 공식 인용 |
|------|------|----------|
| **Size** | < 200줄 | "target under 200 lines per CLAUDE.md file. Longer files consume more context and reduce adherence." |
| **Structure** | 헤딩 + 불릿 | "use markdown headers and bullets to group related instructions" |
| **Specificity** | 구체적으로 | "write instructions that are concrete enough to verify" |
| **Consistency** | 충돌 제거 | "if two rules contradict each other, Claude may pick one arbitrarily" |

### 2.2 구체적 지시 예시 (공식)

| Good | Bad |
|------|-----|
| "Use 2-space indentation" | "Format code properly" |
| "Run `npm test` before committing" | "Test your changes" |
| "API handlers live in `src/api/handlers/`" | "Keep files organized" |

---

## 3. AGENTS.md 공식 가이드라인

> 출처: [OpenAI Codex Docs](https://developers.openai.com/codex/guides/agents-md/)

### 3.1 핵심 특징

- **포맷**: 순수 마크다운 (특별한 형식 없음)
- **크기**: 기본 32KB 제한 (`project_doc_max_bytes`로 조정 가능)
- **계층**: 하위 디렉토리가 상위 덮어씀

### 3.2 발견 순서

```
1. ~/.codex/AGENTS.override.md → AGENTS.md (전역)
2. repo root → cwd (프로젝트, 디렉토리별)
```

---

## 4. llms.txt 표준

> 출처: [llmstxt.org](https://llmstxt.org/) (Linux Foundation 산하)

### 4.1 핵심 원칙

> "현재 언어 모델이 가장 널리, 쉽게 이해하는 포맷은 마크다운이다"

### 4.2 권장 구조

```markdown
# Project Name

> 한 줄 요약

상세 설명...

## Section Name
- [Link Title](url): 설명

## Optional
- [Secondary Info](url): 컨텍스트 작을 때 생략 가능
```

---

## 5. dpc guidelines.md 포맷 도출

### 5.1 공식 문서에서 채택한 원칙

| 원칙 | 출처 | 적용 |
|------|------|------|
| < 200줄 | Anthropic | ✓ |
| 헤딩 + 불릿 구조 | Anthropic | ✓ |
| 구체적 지시 | Anthropic | ✓ |
| 충돌 제거 | Anthropic | ✓ |
| 순수 마크다운 | OpenAI | ✓ |
| 계층적 오버라이드 | OpenAI | preset extends |
| 제목→요약→상세 순서 | llms.txt | ✓ |

### 5.2 권장 포맷

```markdown
# {Preset Name} Guidelines

> 한 줄 요약

## Philosophy
- 핵심 원칙 (구체적으로)

## Workflow
1. 단계 1
2. 단계 2

## Conventions
### 카테고리
- 규칙 (검증 가능하게)

## Examples
### Good
```code
예시
```

### Bad
```code
예시
```
```

### 5.3 검증 체크리스트

- [ ] 200줄 미만인가?
- [ ] 모든 섹션에 헤딩이 있는가?
- [ ] 불릿/번호 리스트로 구성되었는가?
- [ ] 지시가 구체적이고 검증 가능한가?
- [ ] 규칙 간 충돌이 없는가?

---

## 6. 참고 자료

- [Anthropic - How Claude remembers your project](https://code.claude.com/docs/en/memory)
- [OpenAI - Custom instructions with AGENTS.md](https://developers.openai.com/codex/guides/agents-md/)
- [llms.txt Standard](https://llmstxt.org/)
