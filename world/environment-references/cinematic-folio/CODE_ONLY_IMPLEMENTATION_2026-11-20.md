# Commonwealth Folio Studio — Code-Only Integration and Verification

**Date:** November 20, 2026 (Eastern)
**Branch:** feat/commonwealth-cinematic-loc-folio-20261120 / draft PR #337
**Status:** FRONTEND + BACKEND IMPLEMENTED; NO NEW IMAGES; NO CANON PROMOTION.

## Source-first reconciliation

This implementation reads the existing main World Engine, owner/domain, division, Atlas, route, approved structural environment references, and world-state files, then adds an explicit read-only interface over pinned, unmerged PR source evidence. It **does not create a second governing World Engine**.

### Main authority

| Domain | Authority | Folio treatment |
|---|---|---|
| Three divisions | world/data/divisions.json | 3 groups × 4 members; League overlays, not separate sovereign nations |
| Twelve owner homes | world/data/owner_domains.json | Character ID, team, division, permanent/provisional homeland mapping |
| Seven regions | world/data/physical_zones.json | Physical-zone extents and real terrain/climate constraints; coordinates abstract |
| 23 active locations | world/data/locations.json | Stable LOC IDs, region, home relationships, landmarks and source cards |
| 18 mainland routes | world/data/routes.json | Route endpoints and intermediate locations used for topology |
| Temporal state | world/data/current_world_state.json + world_state_events.json | World-state snapshot explicitly dates **end of Week 3, 2026**, not verified Week 11 state |
| 23 reference diagrams | world/environment-references/plates and LOCATION_REFERENCE_REGISTRY.json | Approved **STRUCTURAL** SVG copies, SHA256-checked, not cinematic environment approvals |
| 48 legacy candidates | world/data/atlas_location_candidates.json | Editorial only, unpromoted |

### Unmerged source branches (pinned snapshots)

| PR | Commit pin | Evidence role |
|---|---|---|
| #322 | b32ecbc46e82133f7197fc8802a85e6b59abc44a | Proposed Island mainland causeway, 23 nodes, 45 links, 9 venues; no physical map coordinates or Last Field supersession |
| #324 | 8b7ee0f8e5ed8f57c7efb88c4dff15601e883323 | 155 exact source identifiers, including 40 newer editorial candidates and 44 Island handles |
| #325 | b7bee20d0fc49aa8c04426545fb25de16eee09c2 | 147 exact source identifiers, including 44 different new candidates and 32 Island venue/node handles |
| #339 | ea0b84624b034edceed836890aabe965bf5be3ab | Reconciliation: 103 shared, 52 unique to #324, 44 unique to #325, **199 union identifiers — NOT 199 approved physical locations** |
| #253 | 1e0089170ee6d4ac9cd829ad1f10a70472147904 | 12 internal character portrait paths/hashes; image bytes NOT copied; approval HOLD |
| #314 | cd5814904fba3bb0d6f51490b30eb854684ffdd8 | Existing candidate 23-site audience observer models; referenced not duplicated/promoted |

The Island's bridge is a **proposed** physical crossing in a full 23-node/45-edge precinct plan. The offshore Last Field proposal still conflicts with the existing Central Basin Last Field candidate. The Folio displays the complete source-linked bridge but does not modify the active map.

## Backend

- bridge/build_pinned_bridge.py reads exact Git commits via git show, extracts 199 identifiers, captures Island graph, venue profiles and reference metadata, calculates source hashes and fails if ID concordance differs.
- bridge/DRAFT_SOURCE_BRIDGE.proposal.json is an offline-consumable, source-hashed preview snapshot. No draft item is autoactivated.
- build_folio.py is a standard-library compiler. It validates 3 divisions × 4 teams, 12 distinct home bindings, seven physical regions, 23 LOCs, 18 legal routes, 48 main candidates, the 199-code concordance, Island graph connectivity and zero approved cinematic masters.
- site/data/world.json is a deterministic derived frontend payload; it cannot overwrite any original authority file.
- site/assets/structural/ contains exactly 23 byte-identical approved STRUCTURAL SVGs copied from main source.
- The code-only CI workflow is .github/workflows/commonwealth-folio-studio-ci.yml.

## Frontend

- site/index.html is a local standalone Folio Studio.
- site/app.js implements six interactive screens: World Atlas, Three Divisions, 23 Location Folios, proposed Island bridge, unmerged PR concordance and source evidence.
- site/styles.css is a responsive, accessible, dark editorial interface using local system fonts.
- Mainland Atlas is a schematic rendering of coordinates in Schemin-local-v1. It is **not** GPS, a surveyed coastline, or actual border geometry. Divisions do not create borders.
- Postseason Island is a separate unmeasured network schematic with a three-link mainland gateway or all 45 proposed links; the nine venue cards and all 23 topology nodes are source-specific.
- Cross-PR proposal UI clearly distinguishes current active LOC, existing editorial CAND and unmerged proposals. It never converts a candidate to mainline LOC.
- No raster portraits are packaged. Original twelve-character gallery reference authority is retained as source metadata only.

## Run locally without image generation

From the root of schemin-26:

    python3 world/environment-references/cinematic-folio/build_folio.py --check
    python3 -m http.server 8891 --bind 127.0.0.1 --directory world/environment-references/cinematic-folio/site

Visit http://127.0.0.1:8891/ on the same machine. **This is a local preview, not a deployment or public site.**

To intentionally refresh derived data only after verifying the input mainline source change:

    python3 world/environment-references/cinematic-folio/build_folio.py
    python3 world/environment-references/cinematic-folio/build_folio.py --check

Source changes that invalidate the current count or map constraints fail closed for adjudication. The pinned bridge refresh requires authenticated local Git access to the exact source commits and is never executed by the normal build.

## Executed checks

- Compiler deterministic regeneration: PASS. Exactly 3 divisions, 12 homes, 7 regions, 23 active sites, 18 mainland routes, 48 main candidates, 199 cross-PR handles, 23 Island nodes and 45 edges.
- Python unittest source/authority tests: 13/13 PASS, including structural asset SHA256 byte-for-byte parity and a no-raster-assets assertion.
- Node syntax test of frontend: PASS.
- Real local Chrome 157 DevTools test: PASS. Six metric cards, 23 site cards, 7 region cards, 12 homeowner cards, 9 postseason venue cards, 199 candidate records. Section navigation, one-item location search, 44 PR325-only filter matches and Island toggle 3-to-45 link expansion all passed; zero browser exceptions.
- A JavaScript reserved-name collision with native window.location was caught in the initial real-browser run, repaired, and verified in a fresh tab. No failure was disguised.
- No generated PNGs, JPEGs, WEBPs, photographic masters, historic pictures, public deployments, new World LOC IDs, mainline commits or post-season championship outcomes.

## Holds and non-goals

1. Mainline Atlas, routes, story status and character canon remain unchanged; PR #337 is DRAFT.
2. The official World Engine state is as-of end of Week 3. Later historical/environmental changes require real source work before being represented as current.
3. Postseason Island geometry and mainland anchoring remain proposals; no inferred mileage, bridge loads, coastline or Last Field canon replacement.
4. The two differing 40/44 candidate sets remain separate until explicit source/Founder adjudication; exact-ID union is not proof of the same physical location.
5. Cinematic visual reference status is still 0/23 approved; no new images generated or reviewed for promotion.
6. Independent Umpire, human visual approval and deployment gates remain outstanding.

**Verdict:** Code-only backend and frontend foundation is implemented and locally tested against the actual established mainland, twelve owner homes, historical state constraints and proposed postseason route plan. Further image production remains prohibited under the existing visual audit hold.
