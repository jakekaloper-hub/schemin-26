# WEEKLY MEMO REGRESSION SUITE V2

Status: CANDIDATE TEST CONTRACT

## Character tests
- C01 ObiWan: no championship belt unless active canon explicitly changes.
- C02 D0nkey K0ng: resolve design from active temporal canon receipt; never use retired design.
- C03 TDS: exactly one reptilian humanoid; continuity overlay must not silently reset.
- C04 El Niño: nonhuman weather elemental.
- C05 Mud Dogs: monstrous swamp canine, not normal pet.
- C06 Duckhook: anthropomorphic white duck golfer.
- C07 HMB: Belt Keeper identity survives team rename.
- C08 Chili: Chili Outlaw + Dark Horse association preserved when scene calls for companion.
- C09 Every character-bearing final raster has owner resolution + active reference + continuity state + PASS certification.
- C10 No cross-character contamination.

## Temporal canon tests
- T01 Every release stores canon version/effective date for each appearance.
- T02 Later redesigns do not retroactively fail prior releases.
- T03 Retired designs cannot enter new production after effective date.

## World tests
- W01 Every scene resolves to existing atlas location or NEW/PROVISIONAL.
- W02 Persistent landmarks retain identity and plausible relative geography.
- W03 Entering WORLD_STATE is inherited.
- W04 Damage/consequence cannot silently reset.
- W05 Generated decorative detail is not canon without Atlas approval.
- W06 Terrain transitions require world logic.
- W07 Ensemble/map geography cannot infer league division membership from art.

## Issue-previs tests
- P01 Complete  issue board exists before finished art.
- P02 Adjacent pages are checked for repeated dominant camera/layout/text grammar.
- P03 Multi-page chapter has distinct setup/escalation/consequence functions.
- P04 Image and prose responsibilities are non-redundant.
- P05 Copy budget is evaluated at phone scale before final generation.

## Fact/data tests
- F01 Scores match Fact Lock.
- F02 records reconcile with outcomes/standings.
- F03 PF/PA and standings arithmetic recompute.
- F04 Pittsy ledger recomputes independently.
- F05 wager amount/provenance classification exists.
- F06 Week 4 matchup labels match verified schedule.
- F07 editorial power ranking is not represented as standings.
- F08 generated image text is never authoritative for deterministic league data.
- F09 commissioner-supplied fact remains labeled as such in evidence layer.

## Asset/release tests
- A01 Approved page master has immutable asset identity/receipt.
- A02 Approved page cannot be regenerated silently.
- A03 release manifest page count equals final PDF page count.
- A04 every PDF page maps to one locked page master.
- A05 final PDF renders without clipping/corruption.
- A06 mobile-readability gate passes rendered final PDF, not only source image.

## Week 3 fixtures
- R01 TDS Pages 3-4 against TDS_POST_HAIRCUT_v1 MUST FAIL continuity.
- R02 Week 3 DK centaur against release-time canon MUST PASS; against post-2026-09-29 new-production canon MUST be RETIRED, not retroactively failed.
- R03 Chili/Duck pages MUST preserve commissioner-supplied Sonic/dialogue provenance.
- R04 Red Leopards/Slob wager must remain commissioner-supplied unless external evidence exists.
- R05 Pages 1-21 count MUST equal release manifest 21.
- R06 issue-previs simulation MUST flag repeated matchup-page headline/parchment grammar as a review condition, not automatic aesthetic failure.

## Acceptance
A regression is valuable only if it catches a known failure or protects a binding invariant. Tests that generate noise without changing a production decision are candidates for deletion.
