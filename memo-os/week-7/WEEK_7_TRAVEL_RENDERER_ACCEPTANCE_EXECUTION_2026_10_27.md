# Week 7 — Travel and Renderer Gate Execution Receipt

**Date:** 2026-10-27 · **PR:** #256 · **Mode:** non-rendering, no publication, no merge. This receipt corrects the previous LLC route false-negative.

## Root cause and actual repair
Earlier travel checks treated only `route.from` and `route.to` as graph vertices. The existing `world/data/routes.json` also has `via_location_ids`. In particular `ROUTE-HEARTHROAD` runs from Arsenal Barbershop to Bridge Mountain Lake **via LOC-SLOB-FOOTHILL-CAMP**. A graph traversal that omits intermediate stops falsely reports LLC-to-Slob as unreachable.

**Correct traversal:** expand each registered route into adjacent segments along `[from, ...via_location_ids, to]`, without creating new edges beyond those existing route segments. This is a read-only graph algorithm correction, not a change to world canon.

## Travel findings
| Encounter | Traveler and source assumption | Existing registered segments | Reachability |
|---|---|---|---|
| TDS / Duckhook | Duckhook: Country Club of Jackson → TDS Waterfall Temple | DELTA-CAUSEWAY (via DK Mud Hill) → FALLS-PATH | GRAPH PATH FOUND |
| DK / El Niño | El Niño is a weather manifestation, not necessarily a person traveling on roads | Storm/weather-region propagation requires World Engine verification | CONDITIONAL |
| ObiWan / Chins | Chins Road Commons → Trade Jedi Mountain Base | BASIN-MARKET → UPPER-BASIN-CONNECTOR → EASTERN-ASCENT | GRAPH PATH FOUND |
| Mud Dogs / Chili | Chili Stable → Mud Dogs Swamp | TDS-CHILI-SHARED-MARCH → FALLS-PATH | GRAPH PATH FOUND |
| Red / HMB | Red Ruins and Belt Keeper Keep → proposed Compact Neutral Grounds | Red: RAIN-ESCARPMENT → UPPER-BASIN-CONNECTOR → COMPACT-GROUNDS. HMB: BLACK-CLIFF → EASTERN-ASCENT → UPPER-BASIN-CONNECTOR → COMPACT-GROUNDS | GRAPH PATH FOUND for both |
| Slob / LLC | LLC Boardroom → Slob Foothill Camp | INNER-SEA-QUAY → PORT-BASIN-CONNECTOR → UPPER-BASIN-CONNECTOR → HEARTHROAD (via Slob camp) | **GRAPH PATH FOUND — previous blocker resolved** |

Route edges are sourced from the existing graph. Traversal treats the recorded edges as bidirectional for reachability only; the registry does not explicitly prove all directional permissions. Travel modes, weather/seasonal closures, previous established positions and arrival timing require further acceptance. In particular LLC's journey involves storm gates, port traffic, river crossings, seasonal mud and ridge traffic; it must not be described as instantaneous.

The October 25 Story, Environment and Remaining-Season Travel Workbook was not found as a directly accessible file in the inspected local checkout. Its absence means week-to-week exact previous-position reconciliation is NOT independently certified by this receipt.

## Renderer capability — actual existing contract review
- Twelve October 18 approved character crops have been byte-verified against manifest SHA256 in the preceding acceptance receipt.
- `canon/characters/NATIVE_RENDER_REFERENCE_BINDING_V1.json` records `PARTIAL_NATIVE_REFERENCE_BINDING_DK_VISUAL_CONFLICT_HOLD`; native file handles are not equivalent to freshly mounted approved presentation crops.
- `canon/characters/renderer_capabilities_v1.json` records `NO_PRODUCTION_ROUTE_PROVEN`; the available native renderer does not expose deterministic per-subject binding, mounted-byte hash or subject-binding receipts.
- `memo-os/RENDERER_ADDRESSABLE_ASSET_CONTRACT_V1.md` requires durable output identity, inspectable bytes, hashes and reference lineage. No render occurred, so no output receipt exists.
- The native binding registry's DK registered handle depicts a retired bipedal morphology. The approved October 18 four-legged gorilla-centaur crop is authoritative for current depiction. **Do not reuse stale handle for DK.**

**Conclusion:** Actual source bytes PASS; deterministic renderer subject-binding proof HOLD. No replacement renderer built and no acceptance gate weakened.

## Atlas venue and Pittsy
Founder approved all six Week 7 encounter scenes; existing `WEEK_7_FOUNDER_SIX_VENUE_SCENE_AUTHORIZATION_2026_10_27.md` controls Memo OS staging. This does not create permanent locations or resolve the distinct Pittsy's Book Central Basin vs jungle institution conflict. No silent relocation or invented branch.

## Test receipts
Previous local test executions: character provenance 13/13, scene direction 11/11, Masi routing 3/3, location control 15/15, renderer capability evidence 2/2, Creative DNA validator exit 0. The present graph investigation is an executed read-only traversal, not a separately registered World OS test suite. Independent authenticated Umpire NOT RUN.

## Status
**IMPLEMENTED:** Existing route graph interpreted with via nodes; LLC reachability false-negative resolved in evidence. **TESTED:** Actual graph traversal and previous suites. **AUDITED:** Native renderer binding limits and stale DK handle. **PROMOTED:** Evidence receipt in PR #256 only. **BLOCKED:** directional/seasonal route acceptance, Oct25 travel workbook, renderer subject-binding receipts, Pittsy institution, final Fact Lock, independent Umpire. **REMAINING:** update packet route annotations and run targeted regression; no render/publish/merge.
