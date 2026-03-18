package reprogate.rules

import rego.v1

# scope-defined: RFC 타입 기록에 Design/Proposal과 Summary 섹션이 존재하는지 검사

deny contains msg if {
    some record in input.records
    record.frontmatter.type == "rfc"
    not record.sections.Summary
    msg := sprintf("RFC '%s'에 Summary 섹션이 누락되었습니다.", [record.path])
}

deny contains msg if {
    some record in input.records
    record.frontmatter.type == "rfc"
    not record.sections.Design
    not record.sections["Design / Proposal"]
    msg := sprintf("RFC '%s'에 Design / Proposal 섹션이 누락되었습니다.", [record.path])
}
