package reprogate.rules

import rego.v1

# decision-documented: records/adr/ 에 유효한 ADR이 존재하는지 검사

warn contains msg if {
    adr_records := [r | some r in input.records; r.frontmatter.type == "adr"]
    count(adr_records) == 0
    msg := "의사결정 기록(ADR)이 없습니다. 중요한 기술적 결정이 있다면 records/adr/에 ADR을 작성해 주세요."
}

deny contains msg if {
    some record in input.records
    record.frontmatter.type == "adr"
    not record.sections.Context
    msg := sprintf("ADR '%s'에 Context 섹션이 누락되었습니다.", [record.path])
}

deny contains msg if {
    some record in input.records
    record.frontmatter.type == "adr"
    not record.sections.Decision
    msg := sprintf("ADR '%s'에 Decision 섹션이 누락되었습니다.", [record.path])
}

deny contains msg if {
    some record in input.records
    record.frontmatter.type == "adr"
    not record.sections.Consequences
    msg := sprintf("ADR '%s'에 Consequences 섹션이 누락되었습니다.", [record.path])
}
