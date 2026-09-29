# BULLPEN BOARD MEETING — CCP v2 RECOVERY / CORRECTIVE ACTION PLAN
Date: 2026-09-29
Status: APPROVED BOARD PLAN / EXECUTION SEQUENCING RESET

## Premise
The R0–R15 attempt produced useful infrastructure but exposed governance debt: some gates were described as PASS/preapproved before executable evidence existed; R4 portability remains open; R11 is a contract rather than concrete adapters; R12 has a harness without execution receipt; R8 is only a QA core; R13–R15 are legitimately blocked. These are maturity findings, not reasons to bypass gates.

## Domain roundtable
ARCHITECT — v2 direction is correct, but runtime authority is not fully consolidated. Action: one public runtime API, no copied character truth in consumers, deterministic compilation.
LIBRARIAN — R4 is the primary infrastructure blocker. Action: exact 12 binaries, byte-hash verification, durable locations, media/provenance/approval metadata; never fabricate paths.
CHARACTER DIRECTOR — all 12 records need field-level reconciliation against active authority. Action: 12-owner migration diff and explicit discrepancy classification.
NARRATIVE DIRECTOR — POV architecture is strong but provenance is uneven. Action: 12 claim-level evidence-bound POV profiles; WeeklyStoryState remains transient.
VISUAL DIRECTOR — render certification cannot occur while assets are PENDING_INGESTION; image QA is absent. Action: close R4, then candidate contracts + visual QA before generation.
MEMO/CHRONICLES/NOVEL DIRECTORS — R11 describes routing but does not prove adapters. Action: concrete adapters + contract tests.
RED TEAM — attack surfaces: duplicate truth, bypasses, alias ambiguity, stale text, asset substitution, contamination, unproven CI, override misuse. Action: executable negative tests.
UMPIRE — ledger mixes semantic PASS, implementation PASS and evidence HOLD. Action: states become NOT_STARTED / BUILT / TESTED / PREAPPROVED / PASS / HOLD / BLOCKED. PASS requires observed receipt where tests are required.
CLOSER — stop broad simultaneous progression. Close foundations before art promotion or R14/R15.

## Corrective sequence
A GOVERNANCE RESET — normalize ledger; requirement-to-test traceability; authority/consumer dependency graph.
B RUNTIME FOUNDATION — package/import audit; execute validators/tests; BUG IDs/fixes; obtain CI or reproducible equivalent receipt; execute shadow run.
C SOURCE-OF-TRUTH MIGRATION — 12 field-level legacy-to-v2 diffs; reconcile; generated human views; deprecate legacy runtime readers.
D ASSET PORTABILITY — exact 12 binaries; hash verify; durable locations; fresh-context resolver; wrong/hash/missing attacks.
E POV/WEEKLY STORY — 12 persistent POV profiles; claim provenance; Week2/3 overlays; prove weekly state cannot mutate identity/POV.
F CONSUMER ADAPTERS — Memo, Chronicles, Novel, Live Looks/Xcode/app adapters + bypass tests.
G VISUAL QA READINESS — named evaluator policies; single/pair/6/12 contamination; receipt round-trip; Austin/Pitts preflight.
H ART SESSION — Austin/Pitts candidates only after G; full domain review; Jake alone promotes PRIMARY_HIGH.
I R14 — 12 individual + pair + six + twelve-character image tests including POV/world continuity.
J R15 — fresh-context E2E; receipts; zero P0/P1; adapters/assets/R14 verified; Umpire concurrence before ACTIVE.

## Mandatory loop
PLAN → BUILD → INDEPENDENT AUDIT → EXECUTABLE TEST → BUG_ID → BUGFIX → REGRESSION RETEST → DOMAIN PREAPPROVAL → POLISH → FINAL RETEST → UMPIRE APPROVAL/HOLD → LEDGER UPDATE.

No downstream gate may use planned, file-exists, test-written or preapproved as proof a dependency passed.

## Resolution
Priority is converting existing architecture into reproducible, tested, provenance-backed operations. Artwork is useful only if the pipeline can prove which character/version/reference/POV/scene/QA contract produced it.
