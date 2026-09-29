# CCP v2 — R0–R15 REQUIREMENT / TEST TRACEABILITY MATRIX
Status: RECOVERY A CONTROL ARTIFACT

|Gate|Requirement|Executable proof required|Authority evidence|Current state|Blocker|
|---|---|---|---|---|---|
|R0|single classified authority map; no ambiguous runtime authority|authority inventory + bypass scan|R0_AUTHORITY_MAP|BUILT|legacy readers not fully migrated|
|R1|typed/versioned records reject malformed state|validator/unit tests|models.py, schema, validate.py|BUILT|CI receipt|
|R2|12 owners migrate without silent invention|12-record validation + field diff|records.py + legacy canon|BUILT|field-by-field reconciliation|
|R3|indexes derive from records; collisions fail|resolver/collision tests|registry.py|BUILT|CI receipt|
|R4|12 exact refs are durable and hash-verified|12 SHA checks + fresh resolver + corruption/missing attacks|Commissioner reference register|HOLD|BUG-R4-001|
|R5|layer precedence prevents illegal mutation|negative + positive composition tests|models.py/compose.py|BUILT|CI receipt|
|R6|POV claims evidence-bound; weekly state transient|POV schema/provenance + mutation tests|POV register/memo evidence|BUILT|12 detailed evidence profiles|
|R7|contract deterministic; asset proof controls readiness|determinism + missing-asset tests|compiler.py|BUILT|R4 + CI|
|R8|QA named/executable/fail-closed|policy unit tests + image evaluators|qa.py|BUILT_PARTIAL|image-level evaluators|
|R9|only PASS can create immutable receipt|receipt unit + roundtrip|receipts.py|BUILT|CI + output roundtrip|
|R10|automated regression suite executes|observed CI/local reproducible receipt|workflow + tests|HOLD|no observed workflow receipt|
|R11|all consumers use public v2 interface|adapter contract tests + bypass scan|consumer contract|PREAPPROVED|actual adapters|
|R12|v1/v2 expected behavior reconciled|executed shadow run|shadow_run.py|PREAPPROVED|execution receipt|
|R13|Austin/Pitts candidate production through v2|READY_FOR_ART contracts + board QA + Jake promotion|R13 gate|BLOCKED|R4,R8,R10,R11,R12 prerequisites|
|R14|12-character image/POV acceptance|individual/pair/6/12 receipts|acceptance spec|BLOCKED|R13 + R4|
|R15|fresh-context release certification|E2E + zero P0/P1 + receipt roundtrip|all prior evidence|BLOCKED|R4,R10,R11,R12,R13,R14|

Rule: PASS requires the proof column to exist and be observed, not merely planned.
