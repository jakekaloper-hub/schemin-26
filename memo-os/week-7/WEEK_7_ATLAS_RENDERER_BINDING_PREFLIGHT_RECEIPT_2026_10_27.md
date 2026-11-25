# Week 7 — Atlas Acceptance and Renderer Binding Preflight Receipt

**Date:** 2026-10-27 · **PR:** #256 · **Mode:** no render, no publish, no merge.
**Execution evidence:** isolated checkout `~/Developer/ai/week7-source-acceptance` at PR branch commit `592feb79`; existing source registries and test suites inspected locally. Newer PR source receipts are additive; no active Atlas registry or character canon was modified.

## 1. Atlas location-control: actual tests
`python3 world/location-control-plane/qa/test_location_control_plane.py` → **15 tests, exit 0**. The suite covers active location resolution, candidate firewall, associated relationships, sublocation inheritance and visual-reference required blocking.

### Source-grounded dispositions
- **TDS golf:** parent `LOC-TDS-WATERFALL-TEMPLE` is PERMANENT_CANON, Southern Wetlands. Its registered handles include waterfall, temple stone and dense vegetation. Temporary compact golf green is **not** registered. HOLD for event-space approval; no new persistent location.
- **DK tower:** `LOC-DK-HIGHLAND-STRONGHOLD` exists; training court is a registered feature. Broad tower opening for four-legged centaur body is **not** established by the card. HOLD geometry and wind action.
- **ObiWan training:** `LOC-TRADE-JEDI-MOUNTAIN-BASE` exists; mountain training story is source-compatible, but throw geometry and visitor route direction remain preflight items.
- **Mud/Chili:** `LOC-MUD-DOGS-SWAMP` permanent parent, registered mud channels and raised ground. Cypress clearing is **not** registered; may be proposed as a temporary scene under existing parent, not promoted.
- **Red/HMB:** `LOC-COMPACT-NEUTRAL-GROUNDS` exists as PROVISIONAL_CANON neutral encounter ground in Central Basin. Features are open ceremonial field, arbiter pavilion and arrival roads. **No basketball court is registered.** Candidate parent ONLY; neutral court still HOLD. HMB-to-Red-Ruins route does not confer neutral venue eligibility.
- **Slob/LLC:** `LOC-SLOB-FOOTHILL-CAMP` exists, but man-cave interior is not a registered feature. HOLD interior approval. No LLC-to-Slob route found in current registered graph.
- **Pittsy:** `LOC-PITTSYS-BOOK` is Central Basin in machine and published location register, conflicting with Founder-approved locked jungle establishment. HOLD; do not silently relocate.

## 2. Renderer binding: actual source inspection
- `canon/characters/NATIVE_RENDER_REFERENCE_BINDING_V1.json` status: `PARTIAL_NATIVE_REFERENCE_BINDING_DK_VISUAL_CONFLICT_HOLD`. It documents native handle IDs but explicitly says raw byte materialization and mounted SHA receipts are unproven; DK registered handle is stale bipedal morphology.
- `canon/characters/renderer_capabilities_v1.json` status: `NO_PRODUCTION_ROUTE_PROVEN`; current ChatGPT renderer reference-image consumption exists but per-subject binding and mount-hash receipts are not exposed.
- `memo-os/RENDERER_ADDRESSABLE_ASSET_CONTRACT_V1.md` requires durable asset ID, content hash, source lineage, exact bytes for independent inspection and release-eligible manifest.
- Actual local crop hashes: 12/12 verified in previous receipt. **This is NOT renderer subject binding.**
- `PYTHONPATH=canon/characters/runtime python3 -m unittest discover -s canon/characters/tests -p test_renderer_capability_evidence.py` → **2 tests, exit 0**. These validate capability evidence logic, not actual reference conditioning.

## 3. Gate classification
| Gate | Status |
|---|---|
| Character crop source bytes | PASS 12/12 (previous real receipt) |
| Atlas control-plane regression | PASS 15/15 |
| Renderer evidence regression | PASS 2/2 |
| Renderer reference-image per-subject binding | HOLD — no production receipt |
| Temporary golf green, tower aperture, cypress clearing, man-cave | HOLD — no approved feature handles |
| Red/HMB neutral basketball court | HOLD — neutral parent exists, no court |
| Pittsy jungle vs Central Basin | HARD HOLD |
| LLC visitor route | HOLD |
| Fact Lock / Power Rankings / final standings | HOLD |
| Actual 1024×1536 image QA / 390px final visual | NOT RUN |
| Independent authenticated Umpire acceptance | NOT RUN |

## 4. Next authorized work
Do not rewrite source registry to force green. Existing Atlas authority can adjudicate temporary scene spaces, but **the test suite passing does not approve a new subsite**. Existing renderer evidence explicitly blocks claiming a subject-bound production route. A real renderer adapter receipt or equivalent host-supported mount/subject-binding proof is required before any character-bearing artwork. Keep all 28 folios PLANNED/HOLD, no merge, no render, no publication.

**IMPLEMENTED:** source reconciliation and audit receipt. **TESTED:** 17/17 selected Atlas/renderer tests. **AUDITED:** actual control-plane and renderer capability sources. **PROMOTED:** draft PR only. **BLOCKED:** listed above. **REMAINING:** governed venue dispositions, renderer capability proof, factual source acceptance, independent Umpire.
