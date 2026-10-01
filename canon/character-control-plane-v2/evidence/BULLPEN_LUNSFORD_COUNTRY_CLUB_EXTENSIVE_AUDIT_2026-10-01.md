# BULLPEN × JEFF LUNSFORD CONSULTING AUDIT — Country Club Character-Control Incident

**Date:** 2026-10-01
**Scope:** rejected Country Club renderer proof; Schemin '26 Character Control Plane; Memo OS V5.6 RC; lessons imported from private FLA institutional record.
**Mode:** extensive cross-domain incident audit.
**Decision:** STOP ART remains in force. No prompt-only retry.

## 1. External-consultant lens: Jeff Lunsford / FLA

This audit uses the recorded Jeff Lunsford consulting corpus in the private Fantasy League Artworks repository as consulting precedent; it does not fabricate a new live quote or meeting with Jeff.

Relevant FLA lessons:
1. Jeff's AI/content review established that plausible-looking output can pass structural/voice gates while the wrong route or wrong facts are active. His remedy was routing-correctness assertions and evaluation that verifies the actual conditioning path, not just output appearance.
2. Jeff distinguished outputs from defensible AI IP: the durable asset is the structured evaluation/decision history showing what was tested, what failed, what changed, and why.
3. FLA's Librarian record captures Jeff's governance principle that a session should not close complete when required knowledge artifacts are unfiled; otherwise continuity silently diverges.
4. The FLA record repeatedly treats unvalidated fallback paths as theoretical, not operational.

Applied here: a renderer accepting twelve references is not evidence that twelve character identities were bound. The system tested transport, then inferred control. That inference was invalid.

## 2. Incident statement

The rejected raster failed two independent top-level contracts:
- wrong artifact class: four-panel comic/page instead of one Page-1 illustration;
- wrong characters: semantic reconstructions rather than canonical identities.

The more serious defect is character control. The raster demonstrates that reference attachment alone does not establish identity preservation.

**Character QA ruling: 0/12 PASS.**

## 3. Bug register

### BUG-CHAR-001 — Reference Presence ≠ Reference Binding — P0
**Observed:** twelve references attached; no proof that reference N controlled character slot N.
**Owner:** Character Control + Production/Media Engineering.
**Fix:** typed binding manifest: reference hash → character ID → subject slot → output instance.
**Test:** intentionally swap two refs; evaluator must detect and fail the swapped identity.

### BUG-CHAR-002 — Ensemble Cardinality Jump — P0
**Observed:** pipeline jumped from zero renderer identity proof directly to twelve subjects.
**Owner:** Creative Production + Character Control.
**Fix:** 1 → 2 → 4 → 12 staged stress ladder.
**Test:** identity score cannot regress below threshold at each cardinality.

### BUG-CHAR-003 — Semantic Mascot Reconstruction Accepted Too Late — P0
**Observed:** duck/gorilla/chili/reptile semantics appeared, but exact identity was lost.
**Owner:** Visual Continuity + Standards.
**Fix:** semantic resemblance explicitly scores zero for identity certification.
**Test:** adversarial generic duck/gorilla/cowboy/reptile outputs must fail.

### BUG-CHAR-004 — No Per-Subject Output Instance Ledger — P0
**Observed:** no deterministic mapping from twelve expected characters to twelve output instances.
**Owner:** Production Engineering.
**Fix:** ensemble manifest with exactly twelve registered subject slots.
**Test:** duplicate, missing, thirteenth figure, or ambiguous figure blocks.

### BUG-CHAR-005 — No Crop-Level Character QA — P0
**Observed:** full ensemble inspected after generation; no twelve independent crops.
**Owner:** Visual QA.
**Fix:** auto/manual 12-crop receipt tied to slot IDs.
**Test:** 12/12 required; 11/12 = fail.

### BUG-CHAR-006 — Character Negative Locks Too Weak — P0
**Observed:** negative rules prevented only selected regressions, not wholesale reconstruction.
**Owner:** Character Control.
**Fix:** positive identity invariants + prohibited mutations + silhouette/body/face/form markers.
**Test:** exact-reference comparison, not keyword checklist.

### BUG-CHAR-007 — Current Renderer Has No Proven Identity-Preservation Contract — P0
**Observed:** interface accepted refs but behavior resembled a shared inspiration pool.
**Owner:** CAIO / Production Engineering.
**Fix:** formally characterize provider reference semantics; if subject-level binding unsupported, prohibit native 12-character ensemble generation.
**Test:** controlled A/B with same prompt and different single ref must track the intended identity.

### BUG-CHAR-008 — Compositing Fallback Missing — P0
**Observed:** pipeline assumes one-shot ensemble renderer.
**Owner:** Creative/Production Engineering.
**Fix:** environment plate + controlled character layers/groups + deterministic composition.
**Test:** preserve each approved identity through final composite.

### BUG-INTENT-001 — Artifact-Class Router Failure — P0
**Observed:** Page-1 illustration request became four-panel comic.
**Owner:** Memo OS / Generation Intent Firewall.
**Fix:** route assertion before renderer invocation: PAGE_1_SINGLE_ILLUSTRATION_ONLY.
**Test:** comic/grid/dashboard/page outputs automatically reject.

### BUG-INTENT-002 — Story Context Overexposure — P1
**Observed:** renderer apparently received enough full-story context to illustrate Pages 1–4.
**Owner:** Context Compiler.
**Fix:** least-context packet: renderer receives only current page scene, not full four-page treatment.
**Test:** Page 1 generation contains no later-page Chili payoff, window break, or scoreboard.

### BUG-TYPE-001 — Generative Typography Boundary Breach — P0
**Observed:** titles, captions, speech bubbles, labels and scoreboard generated in raster.
**Owner:** Information Design + Production.
**Fix:** zero editorial text passed to image renderer; reserve geometry only.
**Test:** text-detection inspection; any editorial copy in art fails.

### BUG-WORLD-001 — Generic Venue Substitution — P1
**Observed:** plausible country club, not certified Country Club of Jackson.
**Owner:** Universe OS + Atlas.
**Fix:** location packet must expose renderer-usable invariant landmarks/spatial relationships, not only prose.
**Test:** environment plate QA independent of characters.

### BUG-WORLD-002 — Image Could Mutate World Truth — P1
**Observed risk:** invented clubhouse details could be mistaken for canon.
**Owner:** World Engine.
**Fix:** diagnostic/generated environmental details remain noncanonical unless separately promoted.
**Test:** provenance label on every scene asset.

### BUG-PROV-001 — Durable Binary Layer Still Open — P0
**Observed:** current-context references materialize, but durable fresh-context asset retrieval remains unproven.
**Owner:** Librarian + Production Engineering.
**Fix:** binary-capable persistent store + stable URI + SHA re-verification.
**Test:** fresh-context fetch 12/12 with exact hashes.

### BUG-PROV-002 — Commissioner Promotion Receipt Not Yet a Durable Asset Receipt — P0
**Observed:** identity/hash authority exists, storage does not.
**Owner:** Librarian.
**Fix:** separate authority manifest from storage/mount manifest.
**Test:** cannot ART_LOCK from authority receipt alone.

### BUG-QA-001 — Gate Ordering Allowed Expensive Bad Raster — P0
**Observed:** renderer executed before single-subject binding proof.
**Owner:** Standards.
**Fix:** Character Binding Gate precedes ensemble generation.
**Test:** orchestration refuses 12-subject job until C1/C2 evidence exists.

### BUG-QA-002 — False-Completion Language Risk — P0
**Observed:** prior milestone language said mount/reference attachment “worked,” which could be read as character lock success.
**Owner:** Executive Control + Standards.
**Fix:** controlled vocabulary: ATTACHMENT_ACCEPTED, BINDING_PROVEN, CHARACTER_PASS are distinct states.
**Test:** status schema rejects ambiguous “mount works” completion.

### BUG-QA-003 — No Adversarial Identity Tests — P1
**Owner:** Standards + Character Control.
**Fix:** wrong-ref, swapped-ref, generic-semantic, duplicate, omitted, transformed-body, retired-canon fixtures.
**Test:** all must hard fail.

### BUG-ARCH-001 — One-Shot Renderer Is a Hidden Single Point of Failure — P0
**Owner:** Architecture / CAIO.
**Fix:** renderer capability matrix and compositing route.
**Test:** provider incapable of identity binding automatically routes to layer/composite workflow.

### BUG-ARCH-002 — Context Contract Is Untyped — P1
**Observed:** story, typography, world, character refs and page objective can bleed together.
**Owner:** Architecture.
**Fix:** typed Page Generation Contract with explicit allowed fields per renderer.
**Test:** schema rejects scoreboard/dialogue/full-story fields for Page-1 art call.

### BUG-OBS-001 — No Generation Trace Showing Which Ref Influenced Which Subject — P1
**Owner:** Observability.
**Fix:** persist generation request manifest, ref list, subject slots, provider response IDs, crop QA and defect codes.
**Test:** every output trace reconstructible.

### BUG-LEARN-001 — Incident Learning Not Yet Wired into Acceptance Suite — P0
**Owner:** Memo OS QA + Librarian.
**Fix:** convert this incident into executable regression fixtures.
**Test:** future pipeline cannot promote with same failure class.

## 4. Director-by-director accountability

### Executive Control / Alex Ward
**Missed:** allowed “renderer accepted refs” to read too close to milestone completion.
**Correction:** enforce typed status vocabulary and dependency truth.

### Chief of Staff / Caroline Reeves
**Missed:** next work unit should have been C1 binding proof, not another ensemble attempt.
**Correction:** dependency graph must put Character Binding ahead of ensemble rendering.

### Executive Editor / Claire Bennett
**Missed:** no editorial reason to expose four-page copy to Page-1 renderer.
**Correction:** renderer gets page-local visual beats only.

### Managing Editor / Marcus Hale
**Missed:** production handoff bundled story treatment instead of page-scoped assignment.
**Correction:** one assignment packet per page.

### League Intelligence / Ethan Cole + staff
**Result:** Week 4 factual context was not the cause.
**Correction:** keep league facts out of art renderer unless visually necessary; Page 4 scoreboard remains deterministic.

### Football Analytics / Nathan Price + staff
**Result:** no causal failure.
**Correction:** projections and standings must remain downstream deterministic data; do not spend renderer context on them.

### Editorial / Grant Sullivan, Jack Donovan, Olivia Hart, Rebecca Sloan
**Missed:** dialogue/copy was allowed to contaminate visual generation.
**Correction:** write copy, but hand renderer visual action only.

### Creative Director / Adrian Vale
**Missed:** attempted ensemble complexity exceeded proven renderer capability.
**Correction:** choose production method based on identity-preservation evidence, not desired shot complexity.

### Character & Visual Continuity / Sofia Marin
**Missed:** negative locks substituted for positive identity binding.
**Correction:** own C1–C7; no ensemble authorization without 12/12 binding evidence.

### Information Design / Noah Kim
**Missed:** deterministic typography boundary was specified but not operationally enforced.
**Correction:** renderer packet contains reserved text-safe geometry only.

### Standards / Eleanor Price
**Missed:** Character Binding Gate absent before generation.
**Correction:** independent veto moves upstream; 0/12 proof now blocks all ensemble art.

### Fact Check / Lucas Grant
**Result:** factual scoreboard was broadly correct, but should never have been generatively rendered.
**Correction:** verify deterministic Page 4 data only.

### Editorial QA / Emma Torres
**Missed:** artifact-class failure should have been structurally impossible before image creation.
**Correction:** preflight request payload, not just final raster.

### Production / Victor Lang
**Missed:** no fallback production architecture when one-shot generation fails identity preservation.
**Correction:** implement environment/layer/composite route.

### Visual QA / Lena Park
**Missed:** no mandatory 12-crop inspection artifact.
**Correction:** 12 labeled crops are a release prerequisite.

### Universe / Atlas directors
**Missed:** venue truth was prose-heavy and renderer-unaddressable.
**Correction:** produce visual/spatial environment packet and independent environment plate QA.

### Librarian
**Missed:** authority, transport, mount and identity-binding states were too easy to conflate.
**Correction:** separate receipts and preserve this incident as institutional regression evidence.

### CAIO / AI systems
**Missed:** provider reference semantics were assumed rather than benchmarked.
**Correction:** characterize provider behavior experimentally and route around unsupported subject binding.

## 5. Lunsford-style challenge questions now made mandatory

Before claiming a visual capability is operational:
1. What exactly did we test?
2. What alternate failure could still produce this apparently successful result?
3. Which route/provider/conditioning branch actually executed?
4. What evidence proves the intended identity, not merely a plausible output?
5. What regression fixture prevents this bug from returning?
6. Is the fallback tested or merely present?
7. Can a fresh operator reproduce the result from persisted evidence?

## 6. Remediation program

### Phase A — freeze and instrument
- STOP ART ensemble retries.
- add typed states: ATTACHMENT_ACCEPTED / BINDING_PROVEN / CHARACTER_PASS.
- persist provider request/response trace.
- add incident fixtures.

### Phase B — C1 single-character binding benchmark
For all 12, render controlled neutral identity test from exactly one canonical ref at a time. No story, no text, no environment complexity.
Output: reference + raster + crop + Character QA receipt.

### Phase C — interaction stress ladder
Only after 12/12 individual PASS:
- 2-character interaction tests;
- 4-character interaction tests.
Measure identity retention.

### Phase D — route decision
If native renderer retains identity: proceed toward 12.
If any systematic degradation: switch to deterministic compositing. No repeated prompt tweaking.

### Phase E — Country Club production
- canonical environment plate;
- deterministic 12-slot ensemble manifest;
- controlled character layers/groups;
- composite;
- 12 crop audit;
- World/Story QA;
- typography post-process;
- 390px QA.

### Phase F — institutional close
- executable regression suite;
- defect closure receipts;
- fresh-context reproducibility;
- independent QA;
- only then reopen V5.6 Gate 8.

## 7. Promotion criteria
No Country Club ensemble generation may be called successful until:
- 12/12 individual identity tests PASS;
- chosen multi-character route has passed interaction stress;
- exactly 12 output instances map to exactly 12 character IDs;
- 12/12 final crops PASS;
- no generative editorial typography;
- canonical Country Club QA PASS;
- durable source retrieval PASS;
- independent Standards certification PASS.

**Verdict:** the system currently has a strong canon registry but an unproven character-rendering control plane. The next engineering target is not a better ensemble prompt. It is measurable reference-to-subject binding and a deterministic compositing fallback.
