# SCHEMIN '26 WEEKLY MEMO OS — V5.6 PUBLICATION INTEGRITY PATCH

**Status:** RELEASE CANDIDATE / NOT ACTIVE  
**Authority:** Weekly Memo OS / Bullpen  
**Parent:** V5.5 Integrated Preproduction Hardening  
**Purpose:** convert V5.5's strong preproduction discipline into publication-level release control without replacing the existing five-plane architecture.

## 1. Precedence

Until acceptance passes, V5.5 remains the controlling build.

V5.6 may become controlling only after:
1. all V5.6 acceptance fixtures pass;
2. no retained V5.5 regression fails;
3. independent QA signs the release;
4. Project Control Registry is explicitly updated.

## 2. Design objective

The Memo OS must behave like a publication studio, not a page generator.

V5.6 adds publication-integrity controls:
- Release Registry
- Page Production Contract
- Canon Packet Gate reinforcement
- World/Encounter binding
- Fact / Story / Myth separation
- Closing/Final Word publication standard
- Runtime Bootstrap Resolver
- Generation Intent Firewall + artifact-class QA
- Reference Mount Receipt
- Renderer-Addressable Asset Contract

These controls integrate existing V5.5, World Engine V1.1, character canon, SCK, and independent QA. They do not create a new control plane.

## 3. Publication identity

A released Memo is identified by an immutable release record. Drafts, tests, replays, regenerated pages, and candidate PDFs may never silently replace a published issue.

The official Week 2 memo remains the gold-standard benchmark until explicitly superseded by Commissioner action.

## 4. Production-before-generation law

No finished page generation may begin until the page has:
- FACT dependencies resolved or explicitly blocked;
- STORY role resolved;
- temporal canon receipt;
- Character Packet where applicable;
- World/Encounter location resolved;
- Page Production Contract completed;
- required QA list declared.

## 5. Three-layer evidence model

### FACT
League-state, schedule, scoring, standings, transactions, roster state, verified data.

### STORY
Editorial interpretation, rivalry framing, pacing, humor, callbacks, consequences.

### MYTH
Universe geography, lore, character mythology, persistent locations, symbolic worldbuilding.

Rules:
- STORY may interpret FACT but not rewrite it.
- MYTH may dramatize FACT but not contradict it.
- FACT changes reopen dependent STORY/MYTH artifacts.
- generated text is never a system-of-record for FACT.

## 6. Page Production Contract

Every planned page must carry a compact contract containing:
- page ID / issue ID / role;
- narrative job;
- fact dependencies;
- owner/character dependencies;
- temporal canon version;
- encounter/world location;
- continuity in/out;
- image-tells / prose-tells split;
- art:text ratio;
- deterministic data requirements;
- mobile risk;
- adjacency/rhythm function;
- failure conditions;
- required QA gates.

The contract is stored before render.

## 7. Canon Packet enforcement

Continuity-critical art must resolve:
OWNER → CANONICAL CHARACTER → CURRENT TEAM NAME → ACTIVE TEMPORAL CANON → APPROVED VISUAL REFERENCE.

Wrong species/body architecture, retired design, missing invariant, owner mismatch, cross-character contamination, or rename-driven redesign is release-blocking.

The final raster, not the prompt, is the object being certified.

## 8. World/Encounter binding

Every narrative visual scene resolves through World Engine V1.1.

Required:
- encounter venue;
- division/home/neutral logic;
- route/path where required;
- terrain/climate compatibility;
- entering World State;
- persistent landmark continuity;
- consequence/update note after publication.

The world determines the image; the image does not determine the world.

## 9. Narrative studio loop

Preferred sequence:

DATA → STORY ROOM → ART DIRECTION → RENDER → NARRATIVE REWRITE → DETERMINISTIC DATA COMPOSITE → QA → PAGE LOCK.

Narrative rewrite after art is required where the art creates meaningful visual information that should change the prose.

## 10. Final Word standard

Every standard weekly issue includes a closing module unless Story Budget records an explicit alternative.

The closing must resolve:
- league temperature;
- most consequential weekly turn;
- what remains unresolved;
- transition into the next issue/week;
- narrator voice consistent with the publication.

It should feel like a chapter close, not a dashboard footer.

## 11. Release Registry

No issue may be called RELEASED without a registry entry containing:
- release ID;
- season/week;
- publication timestamp;
- canonical filename/artifact identity;
- page count;
- benchmark status;
- source manifest;
- QA/release receipt;
- supersession relationship.

## 12. Final-PDF-as-truth

Page-level QA is necessary but insufficient.

After PDF assembly:
- render every page;
- inspect phone-scale legibility;
- compare factual data against Fact Lock;
- verify character/canon state;
- detect duplicate/missing pages;
- verify issue rhythm;
- verify release registry mapping.

Only this rendered artifact may be certified.

## 13. Anti-bureaucracy

V5.6 must not duplicate V5.5 controls under new names.

A new field/gate survives only if it:
- blocks a known failure;
- detects a defect earlier;
- preserves release identity;
- reduces Jake intervention;
- materially improves publication consistency.

## 14. Runtime bootstrap

Substantial Weekly Memo runs must resolve current authority from the Project Control Registry and persisted runtime evidence before work begins. Historical fixtures and chat assumptions may not masquerade as current production state.

Controlling contract: `RUNTIME_BOOTSTRAP_RESOLVER_V1.md`.

## 15. Generation intent and artifact-class integrity

Every generative-media call is derived from a locked Page Production Contract and receives an immutable Generation Intent Packet. Before Character QA, Generation Intent QA rejects the wrong artifact class, wrong scene, missing required subject, or prohibited dashboard/UI/workflow substitution.

Controlling contract: `GENERATION_INTENT_FIREWALL_V1.md`.

## 16. Reference mounting and renderer-addressable assets

Character-bearing generation must prove required canonical references were actually mounted. Successful generation is not sufficient for ART_LOCK: the exact candidate bytes must be durably addressable, hashed, lineage-linked and independently inspectable.

Controlling contracts:
- `REFERENCE_MOUNT_RECEIPT_V1.md`
- `RENDERER_ADDRESSABLE_ASSET_CONTRACT_V1.md`

## 17. Targeted QA sequence

For generated narrative art, the preferred gate order is:

```text
GENERATION_INTENT_QA
→ CHARACTER_QA
→ WORLD_CONTINUITY_QA
→ STORY/COMPOSITION_QA
→ TYPOGRAPHY/DETERMINISTIC_DATA_QA
→ FULL_RES_QA
→ 390PX_MOBILE_QA
→ ART_LOCK / PAGE_LOCK
```

A failure returns to the nearest responsible checkpoint. A wrong artifact class does not reopen Fact Lock; a mobile typography defect does not automatically regenerate approved art.

## 18. Promotion gate

V5.6 remains RELEASE CANDIDATE until:
- Week 2 controlled reconstruction suite passes;
- V5.5 11/11 retained regressions remain green;
- controlled failure injection proves targeted reopen;
- release registry invariants pass;
- character/world/fact authority tests pass;
- independent release audit passes;
- no critical defect remains open;
- runtime bootstrap rejects stale OS/week/checkpoint fixtures;
- Generation Intent QA rejects wrong-artifact fixtures;
- required character references are proven mounted before generation;
- renderer-addressable asset identity/hash/inspection invariants pass.
