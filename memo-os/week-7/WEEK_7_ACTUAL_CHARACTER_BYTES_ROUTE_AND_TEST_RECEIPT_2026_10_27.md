# Week 7 — Actual Source-Byte and Atlas Route Acceptance Receipt

**Date:** 2026-10-27 · **PR:** #256 · **Execution:** isolated local Git worktree `~/Developer/ai/week7-source-acceptance` at commit `592feb79`, retrieved from remote branch without modifying the existing Schemin working checkout. **Scope:** real character crop SHA checks, registered route graph reachability and existing Memo OS tests. **No artwork, merge or publication.**

## Character asset-byte verification — PASS 12/12
Loaded `canon/characters/APPROVED_LINEUP_2026_10_18.json`, opened every referenced crop on disk, calculated SHA256 of actual bytes and compared to manifest. **All twelve match**.

| Character ID | Bytes | SHA256 equality |
|---|---:|---|
| CHAR-JAKE-KALOPER | 320465 | PASS |
| CHAR-WILSON-LOOK | 336378 | PASS |
| CHAR-PHILLIP-PITTS | 331140 | PASS |
| CHAR-AUSTIN-BYARS | 328843 | PASS |
| CHAR-BRANDON-PRYOR | 230390 | PASS |
| CHAR-JORDAN-HOLLINGSHEAD | 237136 | PASS |
| CHAR-ZACH-WILSON | 225523 | PASS |
| CHAR-KEVIN-ZEEK | 245679 | PASS |
| CHAR-BOBBY-MITCHELL | 324719 | PASS |
| CHAR-BEN-WHIPPLE | 313601 | PASS |
| CHAR-DAVID-BABB | 280004 | PASS |
| CHAR-MANNING-WELTY | 322217 | PASS |

**Boundary:** These are locally verified source files, not proof of generator-specific image-reference attachment or independent visual likeness QA. The approved lineup crops remain presentation references; do not silently supersede primary identity authority.

## Atlas route graph traversal — source evidence
Read `world/data/routes.json`, treating each registered route as bidirectional for a **reachability test only**. Route travel direction, seasonality, transport eligibility and World OS state still require acceptance.

| Traveler | From → To | Registered path | Status |
|---|---|---|---|
| Duckhook | Country Club of Jackson → TDS Waterfall Temple | ROUTE-DELTA-CAUSEWAY → ROUTE-FALLS-PATH | Graph path FOUND |
| Chins | Chins Road Commons → Trade Jedi Mountain Base | ROUTE-BASIN-MARKET → ROUTE-UPPER-BASIN-CONNECTOR → ROUTE-EASTERN-ASCENT | Graph path FOUND |
| Chili | Chili Stable → Mud Dogs Swamp | ROUTE-TDS-CHILI-SHARED-MARCH → ROUTE-FALLS-PATH | Graph path FOUND |
| HMB | Belt Keeper Keep → Red Ruins | ROUTE-BLACK-CLIFF → ROUTE-EASTERN-ASCENT → ROUTE-RAIN-ESCARPMENT | Graph path FOUND, **does not approve neutral court** |
| LLC | LLC Boardroom → Slob Foothill Camp | none in registered graph | **HOLD** |

All six cited segments in the first three journeys are `INTERPRETIVE_CANON`, not newly ratified permanent travel rights. This graph search is not a fully validated travel itinerary.

## Existing Memo OS tests — actual executions
From the isolated worktree:
- `PYTHONPATH=memo-os/tests python3 -m unittest discover -s memo-os/tests -p test_validate_character_provenance.py` → **13 tests, exit 0**.
- `PYTHONPATH=memo-os/tests python3 -m unittest discover -s memo-os/tests -p test_scene_direction.py` → **11 tests, exit 0**.
- `PYTHONPATH=memo-os/tests python3 -m unittest discover -s memo-os/tests -p test_frank_masi_packet_routing.py` → **3 tests, exit 0**.
- `python3 memo-os/creative-dna/validate_creative_dna.py --packet memo-os/week-7/WEEK_7_CREATIVE_DNA_PROVISIONAL_PACKET_2026_10_27.json` → `PASS: creative DNA registry and candidate structural packet (NOT final visual/release QA)`, exit 0.

An initial combined unittest command failed due to import-path setup. It was corrected by using the repository test directory in PYTHONPATH; no source-code change or validator weakening was needed.

## Remaining hard gates
- Renderer source-image attachment/subject binding and independent likeness inspection not run.
- TDS temporary golf course, DK tower opening, Mud/Chili cypress clearing, Slob man-cave interior not ratified as approved event-spaces.
- Red/HMB neutral court still lacks accepted Atlas site; HMB-to-Red-Ruins graph route does not resolve it.
- Pittsy's Book Central Basin location versus Founder jungle establishment remains unresolved.
- LLC route to Slob camp not found in registered graph.
- FLAIM Week 7 provider winner remains UNDECIDED in last live read; rankings and State of Realm Fact Lock pending.
- No actual illustrated 1024×1536 PNG and 390px final-page QA. No authenticated independent Umpire acceptance.

**Disposition:** Character crop SOURCE BYTES PASS 12/12; existing tests PASS 27/27 plus Creative DNA structural validator; route graph partial; full pre-render certification HOLD.
