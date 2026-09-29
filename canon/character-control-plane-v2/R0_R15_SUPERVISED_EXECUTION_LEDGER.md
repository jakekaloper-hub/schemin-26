# R0–R12 SUPERVISED EXECUTION LEDGER

Workflow enforced per gate: BUILD → AUDIT → TEST DESIGN/EXECUTION PATH → BUG ID → BUGFIX → RETEST PATH → PREAPPROVAL → POLISH → APPROVAL/HOLD.

|Gate|Build|Audit / Bug ID|Fix|Test / Retest|Preapproval|Decision|
|---|---|---|---|---|---|---|
|R0|Authority map|BUG-R0-001 duplicate runtime truth classified|legacy runtime dictionaries marked deprecated candidates; no deletion|authority classes review|Librarian|PASS|
|R1|typed dataclasses + JSON Schema|BUG-R1-001 schema alone did not validate runtime objects|added runtime validator|record/asset validation tests; observed in 17-test CI suite|Architect|PASS|
|R2|12 typed records + POV + asset records|BUG-R2-001 unknown/low-quality assets could be mistaken render-ready|all current assets PENDING_INGESTION|12-record parity + asset fail-closed tests|Character Director|PASS semantic migration|
|R3|compiled owner/team/alias/retired indexes|BUG-R3-001 hard-coded v1 resolver drift|v2 index derives from records; collision build-fail|alias + collision tests observed in CI|Architect/League Historian|PASS|
|R4|AssetReference + resolver|BUG-R4-001 no durable bytes|architecture fixed; physical ingestion still external prerequisite|missing asset fail-closed|Librarian/Visual|HOLD portability; system behavior PASS|
|R5|layer composer|BUG-R5-001 initial composer made weekly/scene layers unusable; override provenance optional|namespaced story/scene overlays; identity mutation blocked; override provenance required|identity-mutation, scene, weekly, override tests observed in CI|Continuity/Architect|PASS|
|R6|typed POV claims in records|BUG-R6-001 POV could harden unsupported psychology|evidence class + provenance; Pitts vigilance PROPOSED|POV/identity separation exercised by composer policy|Narrative Director|PASS semantic|
|R7|immutable contract compiler/hash|BUG-R7-001 renderer could infer readiness|render_ready derives from AssetReference PASS only|missing-asset contract test|Visual Systems|PASS semantics / HOLD rendering|
|R8|QA policy core|BUG-R8-001 reports previously substituted for executable checks|QACheck + deterministic decision|fatal/missing-reference tests observed in CI|Umpire|PASS core / image evaluators remain R14|
|R9|publication receipt|BUG-R9-001 no immutable acceptance receipt|receipt requires QA PASS and contract hash|non-PASS rejection test observed in CI|Umpire|PASS core|
|R10|unittest suite + GitHub Actions workflow|BUG-R10-001 no executable CI existed|compileall + unittest workflow added|GitHub Actions observed SUCCESS; 17/17 tests PASS|Red Team|PASS|
|R11|consumer adapter contract|BUG-R11-001 consumers could read arbitrary canon prose|public-interface-only contract|consumer contract audit|OS Directors|PREAPPROVED; code adapters still migration work|
|R12|shadow_run.py Week2/3 alias/identity expectations|BUG-R12-001 old/new differences lacked deterministic harness|15 canonical/historical query cases encoded; workflow executes harness|CI shadow contract 15/15 PASS|Continuity/League Historian|PASS|

## Supervision finding
Observed GitHub Actions evidence now exists. R10 and R12 evidence holds are closed. This does not authorize ACTIVE status because portability, consumer migration, visual modernization, image-level acceptance and final release gates remain open.

## R13–R15
R13 preproduction contracts exist; artwork intentionally deferred to the next art session by Commissioner direction.
R14 cannot execute image-level acceptance before R13 candidates and portable references.
R15 cannot release before R4 portability, R11 consumer migration, R13 Jake approvals and R14 PASS.

CLOSER: do not declare ACTIVE.
