# CCP v2 — NORMALIZED RECOVERY LEDGER
Allowed states: NOT_STARTED / BUILT / TESTED / PREAPPROVED / PASS / HOLD / BLOCKED.

|Gate|State|Reason|
|---|---|---|
|R0|HOLD|authority map built; legacy runtime readers still exist|
|R1|BUILT|typed model/validation built; executable receipt pending|
|R2|BUILT|12 records exist; field-level reconciliation pending|
|R3|BUILT|registry compiler exists; executable receipt pending|
|R4|HOLD|exact durable asset ingestion not proven|
|R5|BUILT|composer + regression tests exist; receipt pending|
|R6|BUILT|POV model exists; 12 evidence profiles incomplete|
|R7|BUILT|compiler exists; R4 prevents render-ready proof|
|R8|BUILT|core QA exists; image policy/evaluator incomplete|
|R9|BUILT|receipt core exists; executable roundtrip pending|
|R10|HOLD|workflow/test definitions exist; observed execution absent|
|R11|PREAPPROVED|contract exists; concrete adapters/bypass proof absent|
|R12|PREAPPROVED|shadow harness exists; execution receipt absent|
|R13|BLOCKED|art deferred and prerequisites open|
|R14|BLOCKED|requires R13/R4|
|R15|BLOCKED|release prerequisites open|

This ledger supersedes earlier mixed labels such as “PASS pending CI.” There is no conditional PASS.
