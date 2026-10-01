# CHARACTER SOURCE-BYTE + NATIVE RENDER PROGRAM — PHASE 1–13 EXECUTION PLANS V1

**Date:** 2026-10-01  
**Status:** PLANNED / NOT YET EXECUTED  
**Upstream:** Phase 0 complete; lifecycle program merged at `8fe9f077`  
**Budget baseline:** ChatGPT Plus only / zero incremental spend  
**Program owner:** The Closer  
**Rule:** authoritative Director plans/executes; independent counterweight challenges; Umpire never accepts unsupported completion.

---

## Phase 1 — Exact Source-Byte Portability

### Mission
Make all 12 Commissioner-approved source images durably retrievable by Schemin itself, with exact byte identity and no dependency on chat history, Library UI state, or a paid provider store.

### Authority
- **Authoritative Director:** The Librarian — canon/provenance/history.
- **Execution support:** The Setup Man — transport/storage; The Warden — integrity/fail-closed; The Architect — storage boundary.
- **Counterweights:** Setup Man challenges archival-but-unusable storage; Architect challenges duplicate storage; Warden challenges unverifiable provenance.
- **Final acceptance:** The Umpire.

### Inputs
- `canon/characters/reference_sources_v1.json`
- `canon/characters/COMMISSIONER_REFERENCE_REGISTER_12_OF_12.md`
- `canon/characters/VISUAL_REFERENCE_AUTHORITY_V1.json`
- prior hash receipts under `canon/character-control-plane-v2/evidence/`
- owner-scoped `REFERENCE_MANIFEST.yaml`
- current Project/Library file handles where available.

### Deliverables
- 12 durable owner-scoped raw assets under canonical paths;
- fresh SHA-256 + size + media type receipt per source;
- Git blob/object identity where repository-backed;
- clean-context retrieval proof;
- corruption/mismatch fixtures;
- source-byte portability acceptance receipt.

### Execution steps
1. Enumerate 12 approved source records.
2. Attempt zero-spend raw-byte retrieval for each.
3. Materialize bytes into a controlled staging path.
4. Compute fresh hash/size/media type.
5. Compare against approved expectations.
6. Reject any mismatch; never “repair” by regenerating.
7. Store exact bytes at canonical owner-scoped paths.
8. Record durable object/Git blob identity.
9. Test fresh-context retrieval from repository/project storage.
10. Run wrong-file, truncated-file, and stale-file negatives.
11. File 12/12 matrix and Umpire acceptance.

### Director weakness check
Librarian may optimize for perfect archival provenance while overlooking runtime retrieval ergonomics. Setup Man must prove a clean runtime can actually fetch bytes; Architect must ensure no second canon store is created.

### Premortem
- file handle resolves but raw bytes unavailable;
- expected hash itself is stale;
- wrong owner file stored under correct path;
- Git LFS/large-file behavior breaks fresh retrieval;
- convenience derivative substituted for source;
- storage succeeds locally but not in clean context.

### Tests
Unit: hash/schema validation. Integration: store→retrieve→rehash. Negative: swapped owners, truncation, stale composite, generated preview. Clean-context: new checkout/retrieval. Rollback: delete candidate assets without changing source registry authority.

### Acceptance gate
**PASS only if 12/12 exact source bytes are durably retrievable in a fresh context and freshly hash-match approved expectations.**

### HOLD conditions
Any source byte missing, hash mismatch, provenance ambiguity, or storage path unavailable.

### Rollback
Remove staged/candidate assets and receipts; leave current canon/source registry unchanged.

### Downstream handoff
Phase 2 consumes durable path + exact hash contract; Phase 3 consumes actual retrievable bytes.

### Evidence receipt
`PHASE_1_SOURCE_BYTE_PORTABILITY_ACCEPTANCE.md` plus machine 12/12 matrix.

---

## Phase 2 — Provider-Neutral Render Adapter Baseline

### Mission
Define one Schemin render request/execution contract independent of any provider.

### Authority
- **Authoritative Director:** The Architect.
- **Support:** Setup Man, Pitching Coach, Groundskeeper, Bookkeeper for cost semantics.
- **Counterweights:** Groundskeeper challenges impractical abstraction; Closer challenges scope creep; Setup Man challenges non-runnable interfaces.
- **Final acceptance:** Umpire.

### Inputs
- Phase 1 source contract;
- current render-adapter research;
- zero-incremental-spend registry;
- active generation eligibility/runtime boundary;
- current provider capability registry.

### Deliverables
- versioned `RenderRequest` schema;
- adapter interface;
- No-Render adapter;
- Native-ChatGPT adapter interface;
- deterministic composition adapter contract;
- optional external adapter interface disabled by default;
- capability/cost/failure registry;
- execution receipt schema;
- adapter conformance tests.

### Execution steps
1. Inventory existing render request concepts.
2. Normalize only shared semantics.
3. Define provider-neutral request/receipt schemas.
4. Implement No-Render adapter first.
5. Define native ChatGPT interface without assuming undocumented capabilities.
6. Define deterministic composition path.
7. Define optional provider interface with cost metadata.
8. Add timeout/retry/cancel semantics.
9. Run conformance suite.
10. Reject any provider-specific authority field.

### Director weakness check
Architect may over-engineer. Groundskeeper must demand minimal operational interface; Closer rejects abstractions without a Phase 3 consumer.

### Premortem
duplicate control plane, leaky provider IDs, implicit paid dependency, impossible capability assumptions, retry loops, receipts that prove execution but not source identity.

### Tests
Schema/unit, adapter conformance, No-Render integration, cost-policy negative, unknown-provider fail-closed, receipt roundtrip, rollback compatibility.

### Acceptance gate
Same request can compile in No-Render mode and through the native adapter contract without changing canon semantics; no paid provider is required.

### HOLD conditions
Provider-specific canon fields, unfunded critical dependency, missing No-Render path, or ambiguous receipt semantics.

### Rollback
Retain current generation boundary and remove new adapter layer.

### Downstream handoff
Phase 3 consumes the native adapter contract.

### Evidence receipt
`PHASE_2_RENDER_ADAPTER_BASELINE_ACCEPTANCE.md`.

---

## Phase 3 — Native ChatGPT Reference-Mount Contract

### Mission
Prove ChatGPT-native execution can consume the exact approved source bytes and bind them to a specific subject/request without external paid credits.

### Authority
- **Authoritative Director:** The Setup Man.
- **Support:** Pitching Coach, Librarian, Warden, Architect.
- **Counterweights:** Librarian verifies source identity; Warden challenges subject-binding proof; Pitching Coach distinguishes actual capability from assumed capability.
- **Final acceptance:** Umpire.

### Inputs
Phase 1 durable bytes; Phase 2 native adapter; source-authority router; mount/binding runtime.

### Deliverables
- native attachment/mount contract;
- request-bound mount receipt;
- Character ID → subject slot/reference mapping;
- hash continuity evidence;
- supported/unsupported capability declaration;
- reproducibility test.

### Execution steps
1. Select one approved source.
2. Retrieve exact bytes from Phase 1.
3. Attach through native ChatGPT-supported path.
4. Record request ID/reference association.
5. Bind Character ID to intended subject slot.
6. Verify input bytes/hash continuity where technically observable.
7. Execute controlled reference-based generation.
8. Record output instance.
9. Repeat from fresh context.
10. Document unsupported receipt granularity honestly.

### Director weakness check
Setup Man may prove attachment plumbing without proving identity semantics. Librarian/Warden must reject “attached” as equivalent to “correctly bound.”

### Premortem
native UI/tool changes, inaccessible mount identifier, implicit use of wrong image, subject-slot ambiguity, no machine-readable hash receipt, hidden fallback to semantic prompt.

### Tests
Single reference, wrong reference, duplicate attachment, missing attachment, fresh-context repeat, request replay, source hash mismatch.

### Acceptance gate
A zero-spend native request demonstrably consumes the intended current source and produces request-bound subject-reference evidence sufficient for the active generation boundary.

### HOLD conditions
Native route cannot prove reference use/binding at a safe level; only semantic prompting is observable.

### Rollback
Return native adapter to unsupported/HOLD; No-Render remains valid.

### Downstream handoff
Phase 4 high-risk character proof.

### Evidence receipt
`PHASE_3_NATIVE_REFERENCE_MOUNT_ACCEPTANCE.md`.

---

## Phase 4 — High-Risk Single-Character Vertical Slice

### Mission
Prove the three historical failure characters individually before certifying easier characters.

### Authority
- **Authoritative Director:** Groundskeeper.
- **Support:** Pitching Coach, Librarian, Beat Writer for visual brief clarity, Analyst.
- **Counterweights:** Warden blocks stale traits; Umpire independently reviews; Librarian verifies source.
- **Final acceptance:** Umpire.

### Required order
1. Austin Byars / HMB.
2. Phillip Pitts / TDS.
3. Wilson Look / D0nkey K0ng.

### Inputs
Phases 1–3 receipts; current character canon; negative locks.

### Deliverables
Per character: governed request, exact source receipt, native mount receipt, output receipt, QA sheet, defect ledger, retry ceiling.

### Execution steps
1. Lock current positive/negative traits.
2. Generate one controlled neutral scene.
3. Inspect body/species/silhouette/props.
4. Record failures by category.
5. Repair prompt/adapter only if authority remains unchanged.
6. Retest until PASS or HOLD.
7. Repeat next high-risk character.

### Director weakness check
Groundskeeper may privilege throughput and “good enough.” Warden/Umpire must enforce exact negative locks and reject visual drift even when aesthetically strong.

### Premortem
HMB wrong Belt Keeper face/body; TDS wrong head count/body architecture; Wilson centaur regression; semantic team-name redesign; output looks attractive but wrong.

### Tests
Positive locks, retired-state negatives, no unrelated props, one-character isolation, fresh repeatability, output-instance linkage.

### Acceptance gate
All three historical failure cases independently PASS current Character QA.

### HOLD conditions
Any of the three cannot meet current canon through native route within retry ceiling.

### Rollback
Discard outputs; no canon changes.

### Downstream handoff
Phase 5 multi-character binding.

### Evidence receipt
Three individual vertical-slice acceptance receipts + combined phase receipt.

---

## Phase 5 — Multi-Character Binding & Contamination Tests

### Mission
Prove identity/reference binding survives multi-subject scenes and adversarial input conditions.

### Authority
- **Authoritative Director:** Warden.
- **Support:** Setup Man, Analyst, Groundskeeper, Pitching Coach.
- **Counterweights:** Groundskeeper challenges over-blocking; Setup Man separates binding defects from transport defects; Analyst measures false rejection.
- **Final acceptance:** Umpire.

### Inputs
Phase 4 accepted characters; mount/binding contracts; 12 source registry.

### Deliverables
2/3/6/12-subject test suite; contamination matrix; rejection-reason taxonomy; accepted-binding receipts.

### Execution steps
1. Establish 2-character control.
2. Reverse input order.
3. Inject wrong hash/right filename.
4. Inject right hash/wrong Character ID.
5. Duplicate slots/mount IDs.
6. Test Belt transfer, ObiWan Belt contamination, TDS head drift, Wilson centaur regression.
7. Scale to 3, 6, then 12.
8. Measure correct rejection vs over-rejection.
9. Repair binding layer only.

### Director weakness check
Warden may make system safe but unusable. Groundskeeper/Analyst must prove valid workloads continue to pass.

### Premortem
subject swap, blended faces/bodies, shared props, order-sensitive mapping, one bad subject contaminating all outputs, false-positive security rejection.

### Tests
All adversarial cases above plus order invariance and repeated-run consistency.

### Acceptance gate
Valid mappings pass; every contamination fixture fails closed with correct reason; input order does not change identity mapping.

### HOLD conditions
Any silent contamination or high false-rejection rate.

### Rollback
Revert binding changes; preserve single-character path.

### Downstream handoff
Phase 6 QA harness and Phase 7 certification.

### Evidence receipt
`PHASE_5_MULTI_CHARACTER_BINDING_ACCEPTANCE.md`.

---

## Phase 6 — Character QA & Evaluation Harness

### Mission
Make Character QA repeatable, evidence-backed, and calibrated to actual human visual judgment.

### Authority
- **Authoritative Director:** Analyst.
- **Support:** Groundskeeper, Librarian, Beat Writer, Warden.
- **Counterweights:** Umpire and Groundskeeper challenge proxy metrics; Librarian challenges stale rubric inputs.
- **Final acceptance:** Umpire.

### Inputs
Phase 4/5 outputs, character canon, failure history.

### Deliverables
12 per-character QA contracts; positive/negative lock library; scoring/evidence schema; human review workflow; FP/FN calibration set.

### Execution steps
1. Convert canon locks into inspectable traits.
2. Separate machine-checkable vs human-visual checks.
3. Build known-pass/known-fail fixtures.
4. Calibrate thresholds.
5. Measure false positive/negative.
6. Link every QA result to output instance and source receipt.
7. Define override with rationale and counter-signoff.

### Director weakness check
Analyst may optimize metrics that correlate poorly with “looks like the right character.” Umpire/Groundskeeper require real visual inspection and failure examples.

### Premortem
metric gaming, vague subjective criteria, outdated locks, QA detached from output instance, reviewer inconsistency.

### Tests
Known-pass/known-fail calibration, inter-review consistency, stale-canon mutation, missing receipt rejection.

### Acceptance gate
12 QA contracts exist; calibration demonstrates acceptable FP/FN; no QA PASS without linked output + authority evidence.

### HOLD conditions
Uncalibrated scoring or material disagreement between metric and human review.

### Rollback
Retain manual Umpire review as governing gate.

### Downstream handoff
Phase 7 all-12 certification.

### Evidence receipt
`PHASE_6_CHARACTER_QA_HARNESS_ACCEPTANCE.md`.

---

## Phase 7 — All-12 Source Certification

### Mission
Certify every current character through the same governed path.

### Authority
- **Authoritative Director:** Librarian.
- **Support:** Groundskeeper, Setup Man, Analyst, Warden.
- **Counterweights:** Warden challenges identity leakage; Analyst challenges incomplete proof; Groundskeeper challenges unusable process.
- **Final acceptance:** Umpire.

### Inputs
Phases 1–6 receipts.

### Deliverables
12-row certification matrix; 12 source/mount/output/QA receipts; unresolved-gap list.

### Execution steps
Run identical certification workflow for every Character ID; no implied coverage from shared archetypes.

### Director weakness check
Librarian may consider provenance completeness sufficient. Counterweights require actual renderability and QA.

### Premortem
one “easy” owner skipped, stale source silently accepted, inconsistent QA depth, provider-specific exception.

### Tests
12/12 matrix completeness, missing-row failure, hash mutation, cross-owner swap.

### Acceptance gate
12/12 explicit certification receipts PASS.

### HOLD conditions
Any owner uncertified.

### Rollback
Certification state remains per-character; no global activation.

### Downstream handoff
Phase 8 overview + Phase 9 consumers.

### Evidence receipt
`PHASE_7_ALL_12_CERTIFICATION_ACCEPTANCE.md`.

---

## Phase 8 — Corrected 12-Character Overview Rebuild

### Mission
Create a current convenience overview without allowing it to become identity authority.

### Authority
- **Authoritative Director:** Groundskeeper.
- **Support:** Beat Writer, Librarian, Analyst.
- **Counterweights:** Librarian verifies panel provenance; Warden blocks authority creep; Umpire performs visual acceptance.
- **Final acceptance:** Umpire + Commissioner visual approval if aesthetics are ambiguous.

### Inputs
Phase 7 certification matrix only.

### Deliverables
12-panel overview; panel metadata; artifact hash; explicit `DERIVED_OVERVIEW_NOT_PRIMARY_AUTHORITY`; invalidation rule.

### Execution steps
1. Lock deterministic panel order.
2. Compile each panel from certified current state.
3. Attach Character ID/source version/hash metadata.
4. Render overview.
5. QA every panel independently.
6. Record overview artifact hash.
7. Mark resolver prohibition.
8. Add invalidation trigger on source supersession.

### Director weakness check
Groundskeeper may let convenience become shortcut. Librarian/Warden must ensure no downstream resolver points to the overview.

### Premortem
one stale panel, metadata detached from panel, overview becomes de facto source, future redesign fails to invalidate sheet.

### Tests
Panel count/order, metadata completeness, resolver negative test, invalidation simulation.

### Acceptance gate
12/12 visually current; metadata complete; production resolver rejects overview as source.

### HOLD conditions
Any stale panel or consumer dependency on overview.

### Rollback
Retain prior overview as historical only; consumers unaffected.

### Downstream handoff
Phase 9 consumer integration.

### Evidence receipt
`PHASE_8_DERIVED_OVERVIEW_ACCEPTANCE.md`.

---

## Phase 9 — Consumer Integration

### Mission
Make every active consumer use the same reference-authority resolver.

### Authority
- **Authoritative Director:** Architect.
- **Support:** Groundskeeper, Librarian, Setup Man, Beat Writer.
- **Counterweights:** Umpire checks authority boundaries; Groundskeeper checks production usability; Librarian detects local forks.
- **Final acceptance:** Umpire.

### Inputs
Certified resolver + Phase 7/8 outputs.

### Deliverables
Memo, Novel, Story Room, visual-preproduction, publication-fidelity, World/Atlas integration changes; local-lookup deprecation list.

### Execution steps
Inventory consumer lookups → route through shared resolver → remove/disable local authority shortcuts → add compatibility mapping for historical releases → run cross-consumer consistency tests.

### Director weakness check
Architect may unify too aggressively and break historical release replay. Librarian/Groundskeeper protect release-time context and operability.

### Premortem
hidden local lookup, historical artifact rewritten, circular dependency, consumer-specific hack reintroduced.

### Tests
Same Character ID resolves same current source across all active consumers; historical release replay remains frozen; local lookup mutation fails.

### Acceptance gate
No active consumer maintains independent current character-reference authority.

### HOLD conditions
Any hidden fork or historical regression.

### Rollback
Per-consumer adapters restore prior lookup while shared resolver remains candidate.

### Downstream handoff
Phase 10 CCP v2 reconciliation.

### Evidence receipt
`PHASE_9_CONSUMER_CONVERGENCE_ACCEPTANCE.md`.

---

## Phase 10 — Character Control Plane v2 Release Reconciliation

### Mission
Determine whether proven runtime capabilities justify promoting CCP v2.

### Authority
- **Authoritative Director:** Architect.
- **Support:** Librarian, Warden, Setup Man, Groundskeeper.
- **Counterweights:** Closer challenges unnecessary migration; Umpire rejects premature promotion; Librarian checks authority continuity.
- **Final acceptance:** Umpire; Commissioner/Jake only for explicit canon/control-plane promotion if required by current governance.

### Inputs
R15 criteria; Phases 1–9 evidence; current CCP v2 files.

### Deliverables
R15 audit; delta matrix; migration plan; rollback; consumer compatibility proof; promote/hold recommendation.

### Execution steps
Audit every release condition → map satisfied evidence → test migration shadow mode → test rollback → independent audit → explicit promotion decision.

### Director weakness check
Architect may favor elegant successor architecture. Closer/Umpire demand demonstrated value and zero authority ambiguity.

### Premortem
promotion because infrastructure “looks ready,” hidden consumer incompatibility, duplicated authority during migration.

### Tests
Shadow parity, rollback, consumer compatibility, authority single-source assertions.

### Acceptance gate
Either explicit **PROMOTE** with all gates green or explicit **HOLD** with remaining gaps. No ambiguous partial activation.

### HOLD conditions
Any R15 failure or Commissioner-required decision absent.

### Rollback
Current Character Canon/runtime remains controlling.

### Downstream handoff
Phase 11 publication-fidelity proof can consume whichever authority is legitimately active.

### Evidence receipt
`PHASE_10_CCP_V2_RECONCILIATION_DECISION.md`.

---

## Phase 11 — Real Publication-Fidelity Proof

### Mission
Prove the repaired pipeline can create a real current-week page meeting publication quality.

### Authority
- **Authoritative Director:** Groundskeeper.
- **Support:** Beat Writer, Architect, Analyst, Setup Man.
- **Counterweights:** Umpire, Warden, Beat Writer editorial quality, Architect anti-template review.
- **Final acceptance:** Umpire.

### Inputs
Certified character pipeline; current World/Atlas; current Week 4 fact scope; Publication Fidelity contract.

### Deliverables
Rebuilt LLC × HMB “CONVICTION” acceptance fixture; full-res composite; 390px proof; QA ledger.

### Execution steps
Resolve exact current references → hydrate current world → native render → deterministic typography → Character QA → World QA → editorial/composition QA → mobile QA → publication-fidelity scoring.

### Director weakness check
Groundskeeper may mistake technically correct for publishable. Beat Writer/Umpire judge narrative specificity and visual editorial quality.

### Premortem
correct characters in generic card, weak world binding, UI-like lower panel, illegible mobile hierarchy, stale Week 4 fact.

### Tests
Full-res, 390px, character QA, world continuity, fact freshness, F1–F10 publication fidelity.

### Acceptance gate
TECHNICAL + CHARACTER + WORLD + PUBLICATION_FIDELITY + MOBILE all PASS.

### HOLD conditions
Any QA failure. No Week 4 release implication.

### Rollback
Discard fixture; production state unchanged.

### Downstream handoff
Phase 12 activation.

### Evidence receipt
`PHASE_11_REAL_PAGE_ACCEPTANCE.md`.

---

## Phase 12 — Production Activation + Release Gate

### Mission
Authorize the repaired character pipeline for real Schemin production.

### Authority
- **Authoritative Director:** Closer.
- **Support:** Groundskeeper, Setup Man, Librarian, Analyst.
- **Counterweights:** Umpire has completion veto; Warden security veto; Architect anti-fork review; Groundskeeper confirms operational readiness.
- **Final acceptance:** Umpire + required project release authority.

### Inputs
Phases 1–11 receipts.

### Deliverables
Production readiness receipt; allow/deny switch; runbook; rollback; incident response; CI; Health Evidence; Trace v1.2 instrumentation; release-evidence entry.

### Execution steps
Assemble evidence → verify no P0/P1 gaps → enable candidate in controlled scope → observe → rollback drill → full regression → independent audit → activate.

### Director weakness check
Closer may over-prioritize closure. Umpire/Warden must block unsupported activation regardless of schedule.

### Premortem
activation before all consumers migrated, rollback untested, stale source after activation, health metrics show green while visuals drift.

### Tests
Activation/disable toggle, rollback drill, consumer smoke, trace continuity, health failure injection, release evidence validation.

### Acceptance gate
All required gates green, rollback proven, no critical paid-provider dependency, independent Umpire PASS.

### HOLD conditions
Any unresolved P0/P1 gap or failed rollback.

### Rollback
Immediate production deny switch; restore prior safe/no-render behavior.

### Downstream handoff
Phase 13 operations.

### Evidence receipt
`PHASE_12_PRODUCTION_ACTIVATION_RECEIPT.md`.

---

## Phase 13 — Operations, Monitoring & Learning

### Mission
Prevent recurrence and make redesign/supersession automatically invalidate stale production state.

### Authority
- **Authoritative Director:** Librarian — because source supersession/provenance drives invalidation.
- **Support:** Analyst, Groundskeeper, Setup Man, Warden.
- **Counterweights:** Analyst challenges non-actionable monitoring; Groundskeeper requires operational remediation; Warden challenges silent drift; Closer checks that monitoring produces decisions.
- **Final acceptance:** Umpire.

### Inputs
Activated pipeline, Trace, Health Evidence, incident ledger, source registry.

### Deliverables
hash-drift checks; supersession fanout; stale-overview invalidation; contamination regression schedule; incident mining; provider-cost drift check; QA FP/FN review; periodic 12/12 audit; learning ledger; automatic retest triggers.

### Execution steps
Define event triggers → attach invalidation fanout → implement monitors → create action routing → run simulated redesign → verify affected packets/overview/certification invalidate → schedule periodic audit → feed lessons into gap registry.

### Director weakness check
Librarian may build excellent records without corrective action. Analyst/Groundskeeper must tie every alert class to owner, SLA, and remediation.

### Premortem
dashboard-only monitoring, stale alert ignored, redesign does not invalidate derived overview, provider-cost drift silently creates spend assumption.

### Tests
hash drift simulation, supersession simulation, stale overview invalidation, failed-generation incident replay, cost-class mutation, QA threshold drift.

### Acceptance gate
Every monitored failure class has a tested detection → owner → action → closure loop.

### HOLD conditions
Alerts without remediation path or untested invalidation.

### Rollback
Disable noisy monitor without changing production authority; retain manual periodic audit.

### Downstream handoff
Permanent operations; future character redesign starts controlled re-certification.

### Evidence receipt
`PHASE_13_OPERATIONS_LEARNING_ACCEPTANCE.md`.
