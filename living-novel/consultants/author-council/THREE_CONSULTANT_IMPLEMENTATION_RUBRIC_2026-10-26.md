# Commonwealth Inklings — Three-Consultant Implementation Rubric

Date: 2026-10-26
Status: PROPOSED / NOT APPROVED / NOT A LIVE CONSULTENGINE TRANSCRIPT
Scope: existing Bullpen ConsultEngine, Novel OS, Memo OS, eight author methodology profiles and twelve production reference profiles.
Parent PR: #254.

## Evidence provenance
Based on canonical Bullpen THREE_CONSULTANT_EVIDENCE_DOCTRINE_V1, TIM_VEIL_ADVISORY_LENS_V1 and TIM_VEIL_18_DIRECTOR_OPPORTUNITY_REVIEW_V1. These are synthesized recommendations based on existing published-method evidence, NOT three freshly executed ConsultEngine calls, endorsements or statements by Tim Veil, John Ezzell or Jeff Lunsford.

## Modeled consultant perspectives — require actual engine verification
### Tim Veil technical lens — lead
- Freeze a deterministic set of workshop fixtures: same evidence packet, expected routing, source SHA, eight-advisor IDs, and 12 specialist reference IDs.
- Benchmark a small fixed workload before and after orchestration; capture cost, latency, failure recovery, output schema validity, dissent retention and reproducibility.
- Reuse existing ConsultEngine interfaces, model/provider fallback and trace events. Do not adopt BenchBase or Bloviate as dependencies; adapt their reproducibility concepts.
- Fail closed for missing evidence, invalid advisor IDs, hallucinated canon, provider failure and unlicensed third-party code.
- Demand independently rerunnable tests and a clean-context Umpire review.

### John Ezzell enterprise architecture lens
- Map ownership and data contracts across Bullpen, Novel OS and Memo OS before changing code.
- Preserve canonical registries and source-of-truth boundaries; no parallel OS or duplicate consultant engine.
- Require explicit migration and backward-compatibility checks for old Full Seven engagement receipts and new Full Eight requests.
- Define narrow handoff schemas: frozen brief -> independent findings -> reconciliation ledger -> one approved packet -> domain-specific output.

### Jeff Lunsford operating lens
- Pilot a real chapter and a real memo matchup before expanding the workflow.
- Measure usable output improvement and time-to-approved-brief against current manual process.
- Limit routine panels to 2–4 author lenses and 1–3 visual lenses, reserving full council for architectural decisions.
- Avoid paid tooling, unnecessary coordination overhead, and workshops without a specific deliverable.

## Proposed 100-point decision rubric
Architecture compatibility 25; reproducible engineering/testability 25; demonstrated creative output quality 20; canon/provenance/security 15; efficiency/maintenance 15.
Recommended approval threshold >=85/100 AND all hard gates pass. This threshold is a proposed governance choice, not existing policy.
Hard gates: correct ESPN and Atlas evidence, 12-owner POV, character identity, source attribution, no invented human consultations, zero unaudited dependency imports, independent Umpire acceptance.

## Ordered implementation gates
G0: reconcile PR #254 against main and inspect active Bullpen runtime; preserve unrelated dirty worktrees.
G1: invoke actual consultExternalAdvisor for jeff_lunsford, john_ezzell, tim_veil with identical frozen brief; archive real provider outputs and provenance. If provider unavailable, BLOCK consultation and label any synthesis modeled.
G2: Closer reconcile contradictions into one decision register; Founder approves rubric before implementation.
G3: implement minimum viable workshop using existing registries, router and ConsultEngine, without replacing runtime.
G4: run frozen Novel OS and Memo OS pilots, baseline comparison, fail-closed cases and regressions.
G5: Warden/license review, independent Umpire, CI, PR review and merge only if green.
G6: record lessons and verify main-branch readback.

## Open decisions for Founder approval
- Is >=85/100 the right score threshold?
- Are two pilots (one chapter and one memo matchup) sufficient?
- Should full eight consultation require an explicit architecture trigger?

No execution or production merge is authorized by this proposed rubric alone.
