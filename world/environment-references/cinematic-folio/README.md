# Commonwealth Cinematic Location Folio — Production Entry Point

**Status:** DRAFT / CODE-ONLY FOLIO STUDIO IMPLEMENTED / NO APPROVED CINEMATIC MASTERS

**SECOND-PASS CODE AND EDITORIAL REVIEW (2026-11-20):** [Review, counterweight, production-method, Inklings and implementation receipt](SECOND_PASS_REVIEW_AND_EXECUTION_2026-11-20.md). Source Evidence links now honor main vs Folio branch vs pinned PR files; the Island carries an evidence-labeled 2015–2025 season viewer; Chrome browser smoke covers actual source links, timelines and a 390px viewport. No new image assets were created.

**CODE-ONLY IMPLEMENTATION (2026-11-20):** The source-bound compiler, standalone responsive Folio Studio interface, exact-source draft Island causeway preview, 199-code cross-PR geography concordance, and checksummed 23 approved structural SVG copies are implemented. These are **reused structural references, not new generated pictures**. See [implementation and test receipt](CODE_ONLY_IMPLEMENTATION_2026-11-20.md). Open the local preview by running the repository-root command:

    python3 world/environment-references/cinematic-folio/build_folio.py --check
    python3 -m http.server 8891 --bind 127.0.0.1 --directory world/environment-references/cinematic-folio/site

The frontend has six searchable/interactive sections and represents the actual 3×4 divisions, 12 homes, 23 main locations, seven regions and 18 mainland routes. Separate draft overlays read the 23-node/45-edge postseason causeway and PR #324/#325/#339 proposal concordance. **No code path produces artwork, merges drafts or promotes cinematic-reference authority.**

**STOP-PRODUCTION VISUAL QA HOLD (2026-11-20):** Three actual image attempts failed review, including two hallucinated infographic/atlas posters. The manifest has been corrected to `SOURCE_INDEX_ONLY` (23/23), not `SOURCE_PACK_READY`. **Do not generate another image or declare any cinematic master without first satisfying the corrective per-site source/hydration and prompt gates.** See [the visual audit](AUDIT_VISUAL_FAILURE_AND_STOP_GATE_2026-11-20.md). No automatic canon promotion or candidate image registration.
**Commissioned:** 2026-11-20
**Asset class:** hyper-realistic geographic and architectural PNG reference plates
**Original source:** Founder-provided four 1672×941 16:9 aerial landscapes, including Championship Island, Central River Basin, mountain lake/uplands and western-to-southern wetlands. The image files exist in the originating conversation, **not** yet as durable repo assets.

## Mission: revised Founder directive

> Bullpen, execute a source-controlled **Commonwealth Cinematic Location Folio** for *every active LOC-* entry. Match the visual realism, landscape scale, camera treatment, atmospheric lighting, architectural presence and legibility of the four Founder reference images. Establish physical world continuity through seven macro-regional panorama plates plus one unique, high-detail, 16:9 master landscape for each of the 23 active LOC IDs. Connect their roads, hydrology, terrain, travel constraints and institutions exactly as governed by the Atlas. Preserve visual history with versioned, evidence-gated 2015–2026 environment-state variants only where source evidence supports them. Make the result reusable by Memo OS, Novel OS, Commonwealth Living World Atlas, film and future world production through durable ID-based paths, render manifests, provenance and visual QA. Never turn a creative backdrop into new live canon or silently promote the unmerged postseason island concept. Continue reversible implementation; treat independent reference promotion and major Atlas changes as gates.

## What counts as a deliverable

1. **Seven macro-landscape establishing plates** (non-LOC overview assets): Northern Spine, Upper Valleys & Foothills, Central River Basin, Western Tablelands, Eastern Forest & Storm Coast, Southern Wetlands & Delta, Inner Sea Littoral. These are geographic orientation tools, not seven standalone fantasy kingdoms.
2. **23 distinct LOC master establishing PNGs**, each a large-scale place, never a generic reusable shared background. The machine-readable source inventory is [LOC_FOLIO_MANIFEST.proposal.json](LOC_FOLIO_MANIFEST.proposal.json).
3. **Second-angle or local-ground plates** for sites whose major landmark identity cannot be read in a single master.
4. **Historical visual states** only when documentary world or memo evidence establishes an actual era, event scar, restoration or persistent material change. Separate unchanged identity from approved changed state.
5. **Metadata sidecars, QA receipts and approved reference registry promotion**, after explicit image inspection. Draft files are candidates only, not visually authoritative.

Do not generate 23 pictures and call them final without reviewing individual spatial compliance. Do not assume all locations existed unchanged in every year. Do not design all candidates as if they were active canonical sites.

## Authority and inventory

- Primary geography: `world/data/locations.json` — 23 active `LOC-*`.
- Sixteen- and later-era timeline: living novel history and relevant weekly Memo OS published records; verify location histories individually.
- Governing coordinates: `schemin-local-v1`, **abstract and non-metric**; no invented travel times, distances or bridge dimensions.
- Governing relationships: `world/data/routes.json`, `world/atlas/ATLAS_V1.md`, `world/production/CANONICAL_WORLD_PLATE_SPATIAL_BLUEPRINT_V1.md`.
- Place-specific detail: `world/location-control-plane/locations/<LOC-ID>/CARD.json`, 12 Homeland Cards, 58 sublocation handles when relevant.
- Approved geometry references: `world/environment-references/plates/<LOC-ID>/STRUCTURAL_PLATE.svg` (23/23).
- Cinematic image gate: `world/environment-references/ENVIRONMENT_REFERENCE_AUTHORITY_V2.md`; currently **0/23 approved cinematic**.
- Nonactive geography: 48 `CAND-*` under `world/data/atlas_location_candidates.json`, including Central Basin `CAND-CHAMP-LAST-FIELD`. The Founder-directed *island relocation* is in draft PR #322 and cannot silently supersede that record.

## Image fidelity contract

**Positive:** 16:9 landscape matching the Founder benchmark; photorealistic aerial/oblique aerial lens; believable architecture anchored in geography; visible roads, waterworks, footpaths, agriculture, human-scale settlement and weathering; lived-in Commonwealth continuity; grand spectacle without fantasy-island collage; varied region-specific materials; foreground/midground/background separation; atmosphere with sunlight/cloud/shadow grounded in time and climate.

**Negative:** no hand-drawn atlas, poster montage, invented continent labels, disconnected islands, arbitrary volcanic/icy biomes, unsupported giant statues, duplicated generic castle/stadium, inaccurate owner domain, anachronistic technology beyond regional/current authority, noncanonical owner character bodies, imaginary fake teams, or AI-generated text as source truth. The Founder images contain scene labels: keep all **official location labels in a deterministic post-production overlay**, not unverified lettering baked into the reference master.

**Scale:** prioritize coherent landscape extent over forcing every place into one overview. One large 16:9 landscape per LOC allows landmark legibility; the seven macro panoramas communicate regional continuity. Benchmark input images measured at 1672×941; production exports can use a verified higher-resolution 16:9 size while preserving camera grammar.

## Folio state machine

`SOURCE_INDEX_ONLY → SOURCE_PACKET_READY → ART_BRIEF_READY → CANDIDATE_RENDER → VISUAL_QA_HOLD → APPROVED_CINEMATIC_REFERENCE`

On a QA failure: revise and rerender only the affected candidate. Store hashes, source IDs, technical prompt or camera brief, date, generator/model name if available, change reason, previous master/variant relationship, review signatures and exact asset dimensions. Keep `MISSING_APPROVED_CINEMATIC_REFERENCE` until an independent image-based acceptance and reference-register update actually happens.

## Example output layout (proposed; not yet created)

```text
world/environment-references/cinematic-folio/
  README.md
  LOC_FOLIO_MANIFEST.proposal.json
  BULLPEN_BOARD_DECISION_2026-11-20.md
  region-plates/REG-CENTRAL-BASIN/CANDIDATE_MASTER_16x9.png
  plates/LOC-TRADE-JEDI-MOUNTAIN-BASE/
    CANDIDATE_MASTER_16x9.png
    PLATE.json
    history/2026-Wxx/CANDIDATE_STATE_16x9.png
```

The manifest records **target paths**; an entry is not evidence that the PNG exists.

## Production order

**Gate 0 — Evidence hydration:** one world packet per LOC with actual location card, source-approved structural plate, current-state delta, physical region, route list, visible neighboring anchors, historical scars, visual restrictions. No generation from name alone.

**Gate 1 — Geographic coverage:** render one candidate region-level establishing image for each of the seven regions; confirm scene-to-scene terrain and water transitions with Architect/Librarian. No arbitrary geographic relayout.

**Gate 2 — LOC pilot:** select representative different-environment sites (Central Basin `LOC-LEAGUE-CHAMBER`, upland `LOC-TRADE-JEDI-MOUNTAIN-BASE`, southern `LOC-MUD-DOGS-SWAMP`, east coast `LOC-RED-RUINS`) for independent candidate masters, compare with provided references and structural cards, then revise production rubric.

**Gate 3 — Full LOC production:** complete all 23 candidates in defined batches with continuity checks and historical callback cataloguing.

**Gate 4 — Era variants:** source-grounded state changes only; don't infer fictional 2015–2025 owner continuity or unseen structures. Preserve timeline and supersessions.

**Gate 5 — Promotion and consumer bindings:** approved bytes + review evidence → registry `approved_cinematic_reference_uris` → Memo/Novel/Atlas consumers. No application/code changes to a derived service until image evidence and access constraints are verified.

## Domain routing

Canonical Bullpen Core is the organization of record. Source and visual authority are led by Librarian + project-local Visual Development; Architect governs geography/technical bindings; Beat Writer governs historical scene meaning; Umpire applies independent challenge; Closer synthesizes. Scout is requested for sports facts **only** if a period-specific scene makes sports-state claims. No fictitious 19th Director. Consult the board receipt, not an imagined unanimous sign-off.

## Immediate status

- Inventory and registry crosswalk: **seeded for 23/23**.
- Structural plates: **23/23 preexisting approved**.
- New master PNGs: **0 committed in this branch**.
- Approved cinematic references: **0/23**.
- Founder sample image bytes: **not copied into the repo**.
- Canon and candidate stores: **unmodified**.
- Island draft PR #322: **not merged/promoted**.
