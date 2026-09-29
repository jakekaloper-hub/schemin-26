# CCCP T05–T16 SENIOR EXECUTION PLAN v1

status: APPROVED_PLAN / EXECUTION_NOT_IMPLIED
owner: Bullpen
rule: Every gate executes BUILD → TEST → AUDIT → POLISH → BUGFIX → RETEST → DOMAIN SIGN-OFF → LEDGER UPDATE.

## Three pre-execution gaps

### G1 — durable reference binaries
**Current:** 12/12 Commissioner references are approved, mapped and SHA-256 fingerprinted. Conversation assets are not durable repository URIs.
**Closure contract:** ingest exact source bytes into `canon/characters/assets/<CHAR-ID>/primary/`; verify SHA-256 equals Commissioner register; fetch bytes from a fresh repository context; record Git blob SHA + path + content hash in each REFERENCE_MANIFEST; perform renderer injection smoke test.
**Gate owner:** Librarian + Architect + Visual Director.
**Pass condition:** 12/12 byte-for-byte verified and renderer-addressable outside the approval conversation.
**Fail closed:** no path/hash fabrication.

### G2 — Austin Byars visual modernization
Legacy image remains PRIMARY IDENTITY AUTHORITY, not quality ceiling. Build a 2026 high-quality master reference preserving Belt Keeper identity: towering supernatural humanoid champion; shadowed/hooded head; glowing eyes; layered black armor/cloak; championship belt; medieval/rune sword. Do not derive king/vampire/blood-creature anatomy from team name.
**Pipeline:** identity extraction → art brief → controlled generation → identity QA → visual-quality QA → Jake approval → promote new image to PRIMARY_HIGH → legacy image becomes SUPPLEMENTAL/HISTORICAL identity evidence.
**Gate owner:** Character Director + Visual Director; Jake approves promotion.

### G3 — Phillip Pitts visual modernization
Legacy image remains PRIMARY IDENTITY AUTHORITY. Build a 2026 high-quality master reference preserving ONE powerful reptilian humanoid BODY with THREE distinct serpent HEADS, green/gold scales, glowing eyes, dreadlock-like extensions, dark #3 identity. Never three separate snakes, single-headed reptile, Medusa or human.
**Pipeline:** same as G2.
**Gate owner:** Character Director + Visual Director; Jake approves promotion.

## T05 — Environment / Object / Companion linkage
Build machine-readable links per Character ID. Separate identity-critical objects from optional scene dressing. Validate Dark Horse, golden retriever, raccoon, pit-bull, weapons/props and environment anchors. Never invent UNKNOWN companions.
**Tests:** object bleed, companion bleed, environment-causes-redesign.
**Sign-off:** Continuity Director.

## T06 — Deterministic resolver + supersession
Implement one resolver for owner/current team/historical alias/Character ID. Return active package/version/reference IDs and supersession state.
**Tests:** all 12 owners; all known aliases; Baker Moore Purdy; The Immortal; That's Fantasy; stale centaur terms; ambiguous inputs.
**Sign-off:** Architect + League Historian.

## T07 — Render Contract compiler
Compile per depicted character: ID + active version + reference + invariants + negative locks + objects/companions + allowed scene variables.
**Tests:** single, pair, six-character, twelve-character contracts; no cross-packet leakage.
**Sign-off:** Visual Systems Director.

## T08 — Character QA engine
Machine-readable QA with PASS / REGENERATE / HUMAN_REVIEW_REQUIRED only. Major identity/reference failure blocks publication.
**Tests:** species/body, head/face, silhouette, wardrobe, props, companion, retired design, provenance, contamination.
**Sign-off:** Umpire/QA.

## T09 — Weekly Memo OS integration
Replace local character definitions with CCCP resolver calls/contracts. Memo may author story state, never identity.
**Regression:** Week 2/3 scenarios, renamed teams, matchup ensemble pages.
**Sign-off:** Memo OS Director + Umpire.

## T10 — Chronicles integration
Route Chronicle character resolution through CCCP while preserving historical manuscripts as evidence.
**Regression:** Prologue/Chapter I reference resolution and superseded Wilson state.
**Sign-off:** Chronicles Director.

## T11 — Living Novel integration
Route Novel OS/Flaim identity adapter through CCCP. Narrative epithets may not mutate visual identity.
**Regression:** owner lineage, aliases, prose-only references.
**Sign-off:** Novel Director.

## T12 — Other visual pipeline integration
Wire Xcode/web/app/live-look/spotlight/cover/animation-video entry points to resolver + Render Contract. Inventory unknown consumers.
**Sign-off:** Architect + Visual Systems + Closer.

## T13 — Alias / stale-canon adversarial suite
Attack with stale names, retired identities, contradictory prose, missing refs, team-name redesign prompts.
**Required:** Baker Moore Purdy, Arsenal Centaur, Wilson-as-centaur, ObiWan+belt, The Immortal, That's Fantasy, old Chili.
**Sign-off:** Red Team + QA.

## T14 — Multi-character contamination suite
Deliberately mix props, species, companions, wardrobe and reference ordering across 2/6/12-character scenes.
**Pass:** zero identity leakage; ambiguous reference assignment fails closed.
**Sign-off:** Red Team + Visual Director + QA.

## T15 — Controlled visual acceptance
After G1/G2/G3 and T06–T08: individual sheets, pairs, six-owner ensemble, twelve-owner universe composition. Tests are not canon until approved.
**Pass:** 12/12 identity QA + ensemble contamination QA; Austin/Pitts modernization approved.
**Sign-off:** Visual Director + Jake for new master-reference promotion.

## T16 — Regression + release certification
Run full suite from raw alias request to publication gate. Verify ledgers, manifests, hashes, resolver, compiler, QA, downstream integrations and historical preservation.
**Release criteria:** no unresolved P0/P1; 12/12 portable references; 12/12 package/QA PASS; all consumers routed; red-team PASS; ledger current.
**Sign-off:** Umpire + Closer; Jake approves CCCP v1.0 ACTIVE.

## Dependency graph
G1 → T07/T15/T16 renderer certification
G2 + G3 → T15 → T16
T05 → T07
T06 → T07 → T08
T08 → T09/T10/T11/T12
T09–T12 → T13/T14
T13/T14 + G1/G2/G3 → T15
T15 → T16

## Post-work execution record
Every gate must commit: BUILD_ARTIFACT, TEST_REPORT, AUDIT_REPORT, FIX_LOG, RETEST_RESULT, DOMAIN_SIGNOFF, LEDGER_UPDATE, RESIDUAL_RISKS. Missing any item = gate HOLD.
