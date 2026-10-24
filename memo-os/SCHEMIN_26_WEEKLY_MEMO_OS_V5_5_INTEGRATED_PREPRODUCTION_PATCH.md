# SCHEMIN '26 WEEKLY MEMO OS — V5.5 INTEGRATED PREPRODUCTION PATCH

**Status:** BINDING — ACCEPTANCE PASSED 2026-09-29  
**Authority:** Weekly Memo OS / Bullpen  
**Origin:** Week 3 post-production V2 retrospective  
**Supersedes:** V5.4 only after all acceptance gates pass. V5.3/CCCP remain character authority beneath this patch.

## 1. Purpose
Move consistency upstream without reducing creative ambition or creating a second OS. V5.5 integrates the surviving V2 controls into the existing V5.4/V5.3 state machine.

## 2. Authority and temporal canon
Every run records a TEMPORAL_CANON_RECEIPT: active character registry/reference version, effective date and continuity overlay used for each appearance. Current production uses current CCCP authority. Historical releases are audited against their release-time canon and are not retroactively failed by later redesigns.

Character model:
IMMUTABLE IDENTITY + CONTINUITY OVERLAY + PAGE STATE.
Scene state may change pose/action/expression/light; it may not mutate identity or silently reset continuity.

## 3. Persistent Schemin World Control Plane
Schemin is one persistent universe. Before Story Room load:
- WORLD_ATLAS: approved macro/regional/local locations and relative geography;
- WORLD_STATE_LEDGER: entering environmental state and prior consequences;
- provisional/new-location register.

Published image-model scenery is evidence, not automatic canon. Intentional persistent elements require Atlas approval. Exact fantasy mileage is not required.

## 4. Personalized Story Intelligence
Before Story Room collect supported wagers, league-chat jokes, deliveries, dialogue, rivalries, trades, traditions, recurring objects and meaningful locations. Classify each as VERIFIED FACT / COMMISSIONER-SUPPLIED FACT / EDITORIAL JUDGMENT / STORY / FICTIONALIZATION. Repetition never upgrades provenance.

## 5. Complete-issue previsualization
Finished page generation is prohibited until a COMPLETE ISSUE PREVIS exists. For every planned page record:
page function; chapter beat; fact dependencies; characters/reference IDs; continuity in/out; world location; dominant camera/composition; foreground/midground/background; art:text ratio; copy budget; deterministic data layer; previous/next-page relationship; mobile risk.

The board audits issue rhythm before art. Repetition is a review condition, not an automatic aesthetic failure.

## 6. Compact Page Design Packet
One compact packet per page inherits chapter/world/character state rather than duplicating it. It resolves:
NARRATIVE JOB; FACT SCOPE; OWNER→CHARACTER; ACTIVE REFERENCES; CONTINUITY OVERLAYS; FORBIDDEN MUTATIONS; WORLD LOCATION/STATE; CAMERA/F-M-B; ART:TEXT; COPY BUDGET; IMAGE TELLS; PROSE TELLS; DETERMINISTIC DATA; ADJACENCY; MOBILE RISK; REQUIRED QA.

## 7. Dependency-aware production
Preferred order is dependency-driven, not necessarily page-number order:
FACT/EVIDENCE → TEMPORAL CANON → CHARACTER/CONTINUITY → WORLD CONTROL PLANE → PERSONALIZED INTELLIGENCE → STORY ROOM → ISSUE ARCHITECTURE → ISSUE PREVIS → PAGE PACKETS → ENVIRONMENT/ANCHOR REFERENCES → DEPENDENT ART → DETERMINISTIC DATA → TRANSITIONS → COVER/CLOSING → QA.

## 8. Character final-raster certification
Reference attachment is necessary but not sufficient. CHARACTER_QA certifies the FINAL RASTER:
OWNER MATCH; ACTIVE CANON; SPECIES/BODY; SILHOUETTE; FACE/HEAD; WARDROBE; PROPS/COMPANIONS; PALETTE; CONTINUITY STATE; RETIRED DESIGN ABSENT; CROSS-CONTAMINATION ABSENT; FORBIDDEN MUTATIONS ABSENT; THUMBNAIL RECOGNITION.
Any FAIL = PAGE_REJECT unless commissioner explicitly changes canon.

## 9. World Geography QA
Every visual scene must PASS:
atlas location resolved or NEW/PROVISIONAL; terrain compatible; scale/horizon coherent; persistent landmarks stable; entering WORLD_STATE inherited; consequences recorded; no unexplained reset/relocation; generated decoration not silently canonized.

## 10. Visual Rhythm QA
Track camera distance, geometry, character scale/count, environment prominence, text density, headline footprint, parchment usage, deterministic-data footprint, palette/light and emotional intensity. Consecutive pages should not accidentally repeat the same dominant grammar. Multi-page chapters require functional progression, not duplicate posters.

## 11. Prose/visual complementarity
Every Page Packet answers:
WHAT IMAGE COMMUNICATES THAT PROSE DOES NOT;
WHAT PROSE COMMUNICATES THAT IMAGE CANNOT.
Material redundancy returns to composition/copy.

## 12. Deterministic data boundary
V5.4 firewall remains binding. Scores, records, standings, schedules, bids, transaction amounts, rankings, exact names and derived arithmetic are deterministically composited from FACT_LOCK. Image-model text is never system-of-record data.

## 13. Mobile-first copy budget
Copy density is budgeted in preproduction and tested at actual phone scale before Page Lock. Desktop legibility is insufficient.

## 14. Immutable approved-asset receipt
Every commissioner-approved page master stores immutable asset identity, approval timestamp/state, source/provenance and release mapping. Approved assets cannot be silently regenerated or replaced.

## 15. Integrated state machine
DATA_REFRESH → FACT_LOCK → TEMPORAL_CANON_LOAD → CHARACTER_LOCK → CONTINUITY_LOAD → WORLD_ATLAS_LOAD → WORLD_STATE_LOAD → PERSONALIZED_INTELLIGENCE → STORY_ROOM → ISSUE_ARCHITECTURE → ISSUE_PREVIS → PAGE_PACKETS → REFERENCE/ENVIRONMENT_RESOLUTION → DEPENDENCY_AWARE_PRODUCTION → DETERMINISTIC_DATA_LAYER → FACT_QA → CHARACTER_RASTER_QA → CONTINUITY_QA → WORLD_GEOGRAPHY_QA → MOBILE_QA → ORIGINALITY_QA → PAGE_LOCK → ISSUE_RHYTHM_AUDIT → PDF_ASSEMBLY → RENDER_AUDIT → RELEASE_RECEIPT → WORLD/CONTINUITY_UPDATE.

## 16. Anti-bureaucracy
Do not add literal-distance cartography, mandatory dialogue, fixed page counts, camera quotas, duplicate QA forms or automatic scenery canonization. A control survives only if it prevents a meaningful defect, detects it materially earlier, or reduces rework.

## 17. Promotion gate — SATISFIED 2026-09-29
The executable acceptance suite was run, audited, hardened, and rerun. Final result: **11/11 PASS** with known Week 3 failure detection and zero encoded known-pass regressions.

Promotion required and achieved:
1. detects all encoded Week 3 known-failure fixtures;
2. produces zero unexpected failures on encoded known-pass fixtures;
3. validates temporal-canon behavior;
4. validates asset/release invariants;
5. is rerun after bug-fix/polish with all tests passing.


## 18. Promotion receipt
Acceptance evidence: `memo-os/tests/V5_5_ACCEPTANCE_RUN_REPORT.md`.
V5.5 is now the controlling production-hardening patch above V5.4/V5.3. V5.3/CCCP remains authoritative for current character resolution where specified.


## 19. Cover sandbox acceptance learning — 2026-10-02

The accepted Week 4 cover sandbox is capability evidence only: **SANDBOX_ACCEPTED / NON_CANON / NON_PUBLICATION / NON_RESULT / NOT_THE_OFFICIAL_WEEK_4_COVER**.

Durable cover controls:
1. **Cover ≠ matchup opening scene.** A cover requires an issue-level editorial thesis earned from current evidence.
2. **Story-first hierarchy:** STORY → CHARACTERS → CHARACTER RELATIONSHIP → WORLD → ENVIRONMENTAL DETAIL.
3. **Reference controls identity, not staging.** A recurring character must not mechanically inherit the pose/composition of its reference image or prior cover. Pose novelty is a QA dimension.
4. **Behavior is continuity.** Expression, eyeline, posture, action and companion behavior must support the scene. A technically correct character acting emotionally wrong is a material defect.
5. **Companions count.** Canonical companions receive scene-state QA; species/appearance alone is insufficient.
6. **Actual-pixel QA is mandatory.** Prompt compliance is not proof. Inspect final raster anatomy, silhouette, pose, expression, interaction, world continuity, deterministic text boundary and story readability.
7. **Beautiful ≠ PASS.** Visual polish cannot override identity, anatomy, continuity, emotion or story failures.
8. **Iterative acceptance:** RENDER → INSPECT → DEFECT → DOMAIN OWNER → CORRECT → RERENDER → REINSPECT. Do not approve merely because a later image is prettier.
9. **Sandbox/canon firewall:** a sandbox may prove capability but cannot mutate results, World Evolution, Living Novel canon, league history, publication manifest, official page register, Story Lock or Cover Lock.
10. **Official-cover reset:** successful sandbox thesis/copy (including “NOW THE TARGET”) is not automatically eligible for the real Week 4 cover. Real production restarts from current Week 4 evidence → Commissioner context → Story Room → issue-level thesis → character/world resolution → Cover Lock → render → visual QA → publication gate.
