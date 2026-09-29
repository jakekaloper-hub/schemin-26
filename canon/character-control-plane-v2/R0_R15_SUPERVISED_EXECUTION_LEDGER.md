# R0–R12 SUPERVISED EXECUTION LEDGER

Workflow enforced per gate: BUILD → AUDIT → TEST DESIGN/EXECUTION PATH → BUG ID → BUGFIX → RETEST PATH → PREAPPROVAL → POLISH → APPROVAL/HOLD.

|Gate|Build|Audit / Bug ID|Fix|Test / Retest|Preapproval|Decision|
|---|---|---|---|---|---|---|
|R0|Authority map|BUG-R0-001 duplicate runtime truth classified|legacy runtime dictionaries marked deprecated candidates; no deletion|authority classes review|Librarian|PASS|
|R1|typed dataclasses + JSON Schema|BUG-R1-001 schema alone did not validate runtime objects|added runtime validator|record/asset validation tests|Architect|PASS pending CI receipt|
|R2|12 typed records + POV + asset records|BUG-R2-001 unknown/low-quality assets could be mistaken render-ready|all current assets PENDING_INGESTION|12-record parity + asset fail-closed tests|Character Director|PASS semantic migration|
|R3|compiled owner/team/alias/retired indexes|BUG-R3-001 hard-coded v1 resolver drift|v2 index derives from records; collision build-fail|alias + collision tests|Architect/League Historian|PASS pending CI receipt|
|R4|AssetReference + resolver|BUG-R4-001 no durable bytes|architecture fixed; physical ingestion still external prerequisite|missing asset fail-closed|Librarian/Visual|HOLD portability; system behavior PASS|
|R5|layer composer|BUG-R5-001 initial composer made weekly/scene layers unusable; override provenance optional|namespaced story/scene overlays; identity mutation blocked; override provenance required|identity-mutation, scene, weekly, override tests added|Continuity/Architect|PASS pending CI receipt|
|R6|typed POV claims in records|BUG-R6-001 POV could harden unsupported psychology|evidence class + provenance; Pitts vigilance PROPOSED|POV/identity separation exercised by composer policy|Narrative Director|PASS semantic|
|R7|immutable contract compiler/hash|BUG-R7-001 renderer could infer readiness|render_ready derives from AssetReference PASS only|missing-asset contract test|Visual Systems|PASS semantics / HOLD rendering|
|R8|QA policy core|BUG-R8-001 reports previously substituted for executable checks|QACheck + deterministic decision|fatal/missing-reference tests|Umpire|PASS pending CI receipt|
|R9|publication receipt|BUG-R9-001 no immutable acceptance receipt|receipt requires QA PASS and contract hash|non-PASS rejection test|Umpire|PASS pending CI receipt|
|R10|unittest suite + GitHub Actions workflow|BUG-R10-001 no executable CI existed|compileall + unittest workflow added|CI status queried; no status returned yet|Red Team|HOLD until CI receipt visible|
|R11|consumer adapter contract|BUG-R11-001 consumers could read arbitrary canon prose|public-interface-only contract|consumer contract audit|OS Directors|PREAPPROVED; code adapters still migration work|
|R12|shadow_run.py Week2/3 alias/identity expectations|BUG-R12-001 old/new differences lacked deterministic harness|15 canonical/historical query cases encoded|shadow runner created|Continuity/League Historian|PREAPPROVED pending executable run|

## Supervision finding
R0–R12 infrastructure has materially advanced, but senior-grade discipline forbids converting “test file exists” into “test passed.” GitHub connector exposed no completed CI status for the workflow commit. R10/R12 therefore remain evidence HOLDs until an executable receipt is observed.

## R13–R15
R13 preproduction contracts exist; artwork intentionally deferred to the next art session by Commissioner direction.
R14 cannot execute image-level acceptance before R13 candidates and portable references.
R15 cannot release before R10/R12 CI receipts, R4 portability, R13 Jake approvals and R14 PASS.

CLOSER: do not declare ACTIVE.
