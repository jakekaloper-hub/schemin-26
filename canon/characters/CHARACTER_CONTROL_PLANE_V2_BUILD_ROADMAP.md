# CHARACTER CONTROL PLANE v2 — SENIOR BUILD ROADMAP
Rule: Existing T05–T14 artifacts remain evidence/prototypes. v2 converts them into executable infrastructure.

R0 Freeze/map: classify every character-authority file and consumer AUTHORITATIVE / GENERATED_VIEW / HISTORICAL / CONSUMER / DEPRECATED.
R1 Typed domain model: CharacterRecord, Identity, VisualDNA, Invariant, NegativeLock, ObjectCompanion, Environment, AssetReference, CharacterVersion, Alias, POVProfile, ContinuityState, WeeklyStoryState, SceneState, QAResult, PublicationReceipt. Strict schema_version.
R2 Canon migration: one canonical record per Character ID; preserve UNKNOWN; generate human views.
R3 Registry/index compiler: owner/team/alias/retired-alias indexes; fail duplicate aliases, missing IDs, supersession cycles, invalid versions.
R4 Asset resolver: logical IDs → durable locations; SHA-256, availability, provenance, approval; explicit MISSING_REFERENCE. This is G1's durable solution.
R5 Layer composer: deterministic precedence and field mutation policy; reject anatomy edits from weekly/scene layers.
R6 POV/story subsystem: 12 evidence-bound POV profiles; weekly memo writes WeeklyStoryState only; POV claims carry ESTABLISHED/SUPPORTED/PROPOSED + provenance.
R7 Render compiler v2: immutable resolved snapshot with exact asset hashes and field provenance; content-hash contract.
R8 QA engine v2: executable severity/evidence/decision trace; fail closed; ensemble contamination.
R9 Publication receipts: contract hash, IDs/versions, asset hashes, QA version/results, output hash, override events.
R10 CI suite: schema/migration/alias/supersession/12-owner parity/assets/Wilson/Pitts/Jake/contamination/POV boundary/determinism/consumer contracts.
R11 Consumer adapters: Memo, Chronicles, Novel, Live Looks, Xcode/app consume public API/compiled artifacts.
R12 Shadow run: old vs v2 Week 2/3 scenarios; reconcile differences.
R13 Austin/Pitts production: use v2 compiled contracts; approved winners become new version/assets; legacy demotes without deletion.
R14 12-character visual/POV acceptance: individual/pair/6/12 tests.
R15 Release: fresh-context asset resolution, CI green, shadow-run reconciled, adapters verified, receipt round-trip; then and only then ACTIVE.

Every R gate: BUILD → executable TEST → AUDIT → FIX → RETEST → independent sign-off → migration note → ledger update. Markdown reports are evidence, never substitutes for executable tests.
