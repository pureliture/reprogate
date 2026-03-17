package reprogate.rules

import rego.v1

# record-required: records/ 디렉토리에 유효한 Work Record가 존재하는지 검사

deny contains msg if {
    count(input.records) == 0
    msg := "작업 기록이 필요합니다. records/ 디렉토리에 RFC 또는 ADR을 작성해 주세요."
}

deny contains msg if {
    some record in input.records
    not record.frontmatter.record_id
    msg := sprintf("기록 '%s'에 record_id가 누락되어 있습니다.", [record.path])
}

deny contains msg if {
    some record in input.records
    not record.frontmatter.status
    msg := sprintf("기록 '%s'에 status가 누락되어 있습니다.", [record.path])
}
