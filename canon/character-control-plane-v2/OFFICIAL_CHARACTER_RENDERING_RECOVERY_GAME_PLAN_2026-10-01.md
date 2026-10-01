# OFFICIAL GAME PLAN — Character Rendering Control Recovery
## Bullpen × Jeff Lunsford Institutional Consulting Deep Dive

**Date:** 2026-10-01
**Program:** Schemin '26 / Character Control Plane v2 / Memo OS V5.6 RC
**Incident:** Country Club of Jackson “Calm Before the Storm” first renderer proof
**Status:** OFFICIAL REMEDIATION PLAN — ART FREEZE
**Authority:** Executive Control + Character Control + Standards
**Consulting basis:** recorded Jeff Lunsford consulting corpus in private Fantasy League Artworks (FLA). This document applies his documented principles; it does not claim a new live Jeff session.

---

## 0. Executive decision

Do not generate another twelve-character Country Club ensemble until the system proves that its chosen rendering route can preserve canonical identities.

The incident is not primarily a prompt-writing problem. It is a capability-verification, routing, context-contract, asset, QA, and observability problem.

**North-star contract:**

CANONICAL BYTES
→ DURABLE LOCATOR
→ VERIFIED HASH
→ CHARACTER ID
→ SUBJECT SLOT
→ PROVIDER/ROUTE
→ OUTPUT INSTANCE
→ CROP
→ CHARACTER QA
→ COMPOSITE
→ FINAL 12-CROP QA
→ PAGE QA
→ LOCK

No arrow may be inferred from the previous arrow merely succeeding.

---

## 1. What the Lunsford corpus changes

### L1 — Plausible output is not proof of correct routing
In FLA's AI/content consulting review, Jeff challenged systems where structurally valid output could be produced by the wrong prompt/scoring route. The resulting FLA doctrine added routing-correctness assertions rather than trusting output plausibility.

**Schemin translation:** an image that looks “roughly like the league” is not evidence that canonical reference A controlled subject A.

### L2 — Outputs are not the compounding asset; evaluation history is
FLA's Prompt Decision History records failure signal, alternatives, chosen implementation, measurement, and co-sign authority.

**Schemin translation:** every character-rendering route decision must have a benchmark record. “Prompt seemed better” is not evidence.

### L3 — A fallback that exists but has not been validated is theoretical
FLA's artAgent/fal.ai path was explicitly treated as unvalidated until real test images and quality-floor evidence existed.

**Schemin translation:** native multi-reference generation, staged group generation, and compositing are candidate routes until benchmarked.

### L4 — Canonical identity needs one read model
FLA's Character Artwork UX audit found split-brain identity paths: rich brain data vs legacy team fields, with Creation Studio sometimes ignoring the richer source.

**Schemin translation:** every art route must consume the same canonical Character Packet resolver. No prompt path may independently reconstruct identity from team names, prose, old canon, or semantic archetypes.

### L5 — Provider behavior is not interchangeable
FLA's artAgent doctrine notes that providers differ in aesthetic defaults and prompt conditioning; provider swaps require review.

**Schemin translation:** reference-image semantics must be characterized per renderer/provider. A provider that accepts image inputs may still not support deterministic subject binding.

### L6 — Close the knowledge loop
FLA Librarian doctrine from the Lunsford program says completion without filing required knowledge creates silent continuity divergence.

**Schemin translation:** no remediation phase closes without receipts, benchmark results, defect disposition, and updated regression tests.

---

## 2. Program outcomes

This program is complete only when Schemin can answer with evidence:
1. Can the renderer preserve each of the 12 canonical characters individually?
2. At what subject cardinality does identity retention degrade?
3. Does the provider support explicit reference-to-subject binding or only shared reference conditioning?
4. Which route is production-safe: native ensemble, staged groups, or deterministic compositing?
5. Can a fresh execution reproduce the same reference bytes and route?
6. Can QA identify swaps, duplicates, omissions, generic reconstructions, retired canon, and extra figures?
7. Can Page 1 be produced with exactly 12 certified identities in the canonical Country Club environment, without generative typography?

---

## 3. Workstreams and domain ownership

### WS-A — Asset & provenance
**Lead:** Librarian
**Co-owners:** Production Engineering, Character Control
**Deliverables:** durable binary store; stable locator; SHA-256; fresh retrieval receipt; authority/storage/mount receipts kept separate.
**Exit:** 12/12 fresh-context exact-byte retrieval.

### WS-B — Canonical Character Resolver
**Lead:** Sofia / Character & Visual Continuity
**Co-owner:** Architecture
**Deliverable:** one typed Character Packet per owner with source hash, positive identity invariants, prohibited mutations, temporal canon, approved visual references.
**Exit:** all generation routes consume only this resolver.

### WS-C — Provider capability characterization
**Lead:** CAIO / AI Systems
**Co-owners:** Production, Standards
**Deliverable:** renderer capability matrix: image-ref acceptance, per-subject binding support, max reliable cardinality, identity retention, style transfer behavior, text leakage, policy/fallback behavior.
**Exit:** route capabilities proven empirically.

### WS-D — Generation Intent & context isolation
**Lead:** Memo OS / Production
**Co-owners:** Editorial, Information Design
**Deliverable:** typed page-local generation contract. No full-story leakage, scoreboard data, editorial copy, or future-page beats.
**Exit:** schema prevents prohibited fields.

### WS-E — Character benchmark & QA
**Lead:** Standards + Visual QA
**Co-owner:** Character Control
**Deliverables:** individual, pair, group, adversarial, and crop-level evaluation set.
**Exit:** documented thresholds and hard fails.

### WS-F — World/Atlas rendering
**Lead:** Universe OS + Atlas
**Co-owner:** Creative
**Deliverable:** canonical Country Club Environment Packet + environment plate test.
**Exit:** environment certified independently from characters.

### WS-G — Compositing route
**Lead:** Production / Creative
**Co-owners:** Information Design, Visual QA
**Deliverable:** environment plate + character layers/groups + deterministic slot composition.
**Exit:** viable fallback proven before native ensemble is trusted.

### WS-H — Observability & institutional learning
**Lead:** Executive Control + Librarian
**Co-owners:** CAIO, Standards
**Deliverables:** generation trace, decision log, incident fixtures, status vocabulary.
**Exit:** every future output can be reconstructed from persisted evidence.

---

## 4. Phase plan

### PHASE 0 — Freeze, baseline, and preserve
**Objective:** prevent accidental repetition and preserve the failed raster as a regression fixture.

Actions:
- maintain STOP ART for 12-character ensemble;
- tag failed raster diagnostic-only;
- freeze current 12 canonical hashes and Character IDs;
- register all 21 incident bugs;
- add explicit state vocabulary:
  - SOURCE_BYTES_AVAILABLE
  - DURABLE_SOURCE_VERIFIED
  - REFERENCE_ATTACHED
  - SUBJECT_BINDING_PROVEN
  - CHARACTER_QA_PASS
  - ENSEMBLE_QA_PASS
  - PAGE_LOCK
- prohibit ambiguous “mount worked” language.

**Exit:** baseline receipt + bug ledger + state schema.

### PHASE 1 — Durable asset closure
**Objective:** close the remaining R4 transport weakness.

For each of 12:
canonical bytes → durable binary-capable store → stable locator → fresh-context fetch → SHA-256 compare.

Tests:
- missing asset;
- corrupted byte;
- wrong hash;
- swapped locator;
- stale superseded asset.

**Exit:** 12/12 fresh retrieval PASS. Anything else blocks.

### PHASE 2 — Single-character binding benchmark (C1)
**Objective:** establish whether each reference can control one output identity.

Test conditions:
- one reference only;
- neutral/simple background;
- no story;
- no text;
- fixed aspect ratio;
- minimal pose variation;
- no team-name semantic description that could let the model fake the identity without using the image.

For each character persist:
input hash, Character ID, provider, request manifest, output ID/hash, QA crop, Character Control verdict, defect codes.

**Acceptance:** 12/12 individually certifiable. Generic semantic resemblance = FAIL.

**Adversarial control:** rerun selected prompts with reference removed. If output remains essentially the same semantic mascot, reference conditioning is weak and route is not trusted.

### PHASE 3 — Pairwise binding benchmark (C2)
**Objective:** detect cross-character contamination.

Use six controlled pairs, including difficult morphology combinations:
- Duckhook × Chili;
- TDS × DK;
- ObiWan × HMB;
- Slob × Chins;
- Red × Mud Dogs;
- LLC × El Niño.

Tests:
- swap reference order;
- swap subject slot;
- alter positions;
- ask for interaction without changing identity.

**Acceptance:** both identities pass independently in every selected output; zero swaps/merges.

### PHASE 4 — Four-character stress benchmark (C3)
**Objective:** determine identity-retention curve.

Three groups of four; repeat with foreground/midground/background placements.

Metrics:
- 12 expected identity instances;
- identity pass rate;
- duplicate rate;
- omission rate;
- cross-character leakage;
- morphology mutation;
- reference-order sensitivity.

**Decision gate:**
- if identity retention is 100% and reproducible, native ensemble remains candidate;
- any systematic degradation routes production to compositing. Do not solve by prompt escalation.

### PHASE 5 — Provider/route decision
CAIO + Standards issue a formal route ruling:

**Route A: Native 12-character ensemble** only if provider demonstrates deterministic enough binding through Phase 4 and a 12-subject preflight.

**Route B: Staged groups** if 3–4 character groups preserve identity but 12 does not.

**Route C: Deterministic compositing** if multi-character identity preservation is unreliable.

The safest route wins; not the most convenient.

Record using FLA Prompt Decision History format:
failure → alternatives → chosen route → measurement → co-sign.

### PHASE 6 — Country Club world plate
Before characters:
- hydrate canonical Country Club of Jackson packet;
- lock geography, clubhouse/golf-course spatial cues, terrain, weather/time, hosting context;
- generate/construct environment plate;
- World QA independently certifies it;
- invented details remain noncanonical unless promoted.

**Exit:** WORLD_PLATE_LOCK.

### PHASE 7 — Deterministic ensemble manifest
Exactly 12 slots.

Each slot contains:
- slot ID;
- Character ID;
- source hash;
- screen position;
- depth;
- scale;
- occlusion maximum;
- action;
- interaction partner;
- required visible identity markers;
- prohibited mutations.

Specific story requirements:
- Duckhook and Slob are Country Club hosts;
- Chili prank on Duckhook;
- TDS beside Chili laughing;
- LLC participates in the eventual bad-tee-shot/property-damage story beat according to the four-page storyboard;
- El Niño is occupied with work calls;
- remaining principals receive distinct social/golf actions;
- exactly 12 principals; no extras masquerading as league owners.

### PHASE 8 — Page 1 production
Only Page 1.
No scoreboard. No later-page payoff. No generated dialogue. No editorial typography.

Depending on Route Decision:
- native ensemble;
- staged group layers;
- or deterministic composite.

### PHASE 9 — Twelve-crop Character QA
Generate a labeled QA crop for every slot.

**Hard law:** 12/12 PASS. 11/12 = PAGE FAIL.

Adversarial checks:
- retired DK centaur;
- generic gorilla;
- generic duck golfer;
- single-headed TDS;
- separate snakes;
- ObiWan belt;
- generic medieval HMB;
- Chili cowboy without canonical identity;
- generic leopard/dog/corporate mascot;
- duplicate/extra/omitted figure.

### PHASE 10 — Page QA
After Character PASS:
Generation Intent → World → Story/Composition → typography boundary → full-res → 390px.

Typography is deterministic post-generation.

### PHASE 11 — Four-page story production
Repeat the certified method page-by-page.

Page 4 receives deterministic Flaim Week 4 matchup scoreboard after fresh data refresh. The scoreboard is not image-model text.

### PHASE 12 — Regression & V5.6 Gate 8 closeout
Convert incident into executable fixtures:
- reference omitted;
- swapped refs;
- wrong current canon;
- duplicate character;
- missing character;
- extra character;
- wrong artifact class;
- generative typography;
- world substitution;
- stale asset;
- wrong hash;
- full-story leakage.

Independent Standards audit. Gate 8 remains blocked until all required real-production evidence is green.

---

## 5. Measurement framework

### Character Identity Score
This is not a beauty score. Binary certification is primary.

For diagnostic analysis:
- source identity/form fidelity;
- face/head/body morphology;
- signature gear/silhouette;
- color/material fidelity where identity-bearing;
- prohibited mutation absence;
- cross-character contamination absence.

**Certification remains PASS/FAIL.** A weighted average cannot rescue one wrong character.

### Ensemble metrics
- expected principals: 12;
- certified principals: must equal 12;
- duplicates: 0;
- omissions: 0;
- extras presented as principals: 0;
- identity swaps: 0;
- retired-canon regressions: 0;
- generated editorial text: 0.

---

## 6. Stop conditions

Stop and return upstream immediately if:
- a source hash cannot be verified;
- provider cannot demonstrate single-subject reference conditioning;
- a pair merges identities;
- cardinality causes repeatable degradation;
- output contains generic semantic substitutes;
- any subject cannot be mapped uniquely;
- Country Club environment conflicts with Atlas;
- renderer produces text;
- wrong artifact class appears.

No “one more prompt” retries without a recorded hypothesis and test.

---

## 7. Official acceptance definition

The character-control incident is closed only when:
1. 12/12 canonical bytes durable and fresh-retrievable;
2. 12/12 individual binding tests PASS;
3. interaction/cardinality route characterized;
4. production route formally selected from evidence;
5. Country Club world plate PASS;
6. deterministic 12-slot manifest complete;
7. final Page 1 contains exactly twelve uniquely mapped canonical principals;
8. 12/12 final crops PASS;
9. no generative typography;
10. full-res and 390px QA PASS;
11. incident regression suite PASS;
12. independent Standards certification filed.

Until then:
**Character Control Plane v2 remains unproven for this ensemble use case. V5.6 Gate 8 remains BLOCKED.**

---

## 8. Immediate execution queue

1. **Librarian/Production:** close durable 12-byte fresh retrieval.
2. **Character Control:** compile 12 typed C1 Character Packets from current approved references.
3. **CAIO:** write provider capability test harness/manifest.
4. **Standards:** define C1 binary identity rubric and adversarial controls.
5. **Production:** execute first single-character benchmark only after 1–4 are ready.
6. **Bullpen:** audit result, fix defect, retest; continue character-by-character.
7. Do not reopen Country Club ensemble generation until the route decision gate.

**Program doctrine:** prove the capability at low cardinality, measure degradation, then choose the production architecture. Do not ask a prompt to compensate for a renderer capability that has not been demonstrated.
