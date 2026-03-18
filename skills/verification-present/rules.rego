package reprogate.rules

import rego.v1

# verification-present: 모든 기록에 Verification 섹션이 존재하는지 검사

deny contains msg if {
    some record in input.records
    not record.sections.Verification
    msg := sprintf("기록 '%s'에 Verification 섹션이 누락되었습니다.", [record.path])
}
