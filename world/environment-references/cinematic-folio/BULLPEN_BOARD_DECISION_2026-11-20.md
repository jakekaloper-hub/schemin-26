# Bullpen Board Decision — Commonwealth Cinematic Location Folio
**Meeting / commission date:** November 20, 2026 (America/New_York)
**Disposition:** FOUNDER MISSION ACCEPTED FOR DRAFT PREPRODUCTION; **VISUAL REFERENCE PROMOTION HOLD**
**Owning repository:** `jakekaloper-hub/schemin-26`
**Origin:** Founder's four attached cinematic panoramas and request to build visual assets for all coded Commonwealth locations, past → present → future.

## 1. Rewritten Founder directive (production-ready)

> **/bullpen mission — Commonwealth Cinematic Location Folio**
>
> Read the established Schemin '26 World Engine, Atlas, Location Control Plane, location cards, route graph, seven physical zones, historical Memo OS evidence and environment-reference authority before rendering. Convert **every active LOC-* location ID** into a **reusable, hyper-realistic, 16:9 cinematic PNG environment master** matching the large-scale aerial landscape quality of the four images I supplied. Create a cohesive sequence of **seven geographical establishing panoramas** plus 23 LOC-specific master plates, then location details and source-evidenced **historical 2015–2026 state variants** where the landscape changed. Each asset must be permanently addressable by its existing code, with render metadata, source trace, terrain/route/water continuity, controlled naming, approval history, and reusability for the weekly Memo OS, Commonwealth Atlas, Novel OS, animations/film, and future projects.
>
> Show the Commonwealth as a geographically connected, inhabited civilization, **not an ungrounded fantasy map, island collage or composite of random biomes**. Keep landmarks, owner domains, cities, institutions, and environmental scars spatially and temporally coherent. The four provided panoramas are creative fidelity references rather than automatic canon-defining map plates; their embedded captions do not prove site identity or location. Use deterministic overlays for `LOC-*` labels rather than asking image-generation models to invent place lettering.
>
> Route the mission through canonical Bullpen authority with local Visual Development and continuity specialists. Generate source-hydrated candidate assets in geographic batches, independently QA each candidate, and promote only approved bytes to the cinematic reference registry. No new `LOC-*` geography, 2026 result, permanent world change, island relocation or false Director sign-off is permitted. Keep `CAND-*` proposals separate, including the draft postseason island in PR #322. Persist work and evidence to the existing GitHub repository; do not create a parallel Atlas or halt on routine reversible work.

## 2. Board invocation provenance and limits

**Executed:** The connected Mac's standalone Bullpen `createBullpen` / `consultation.conveneBoardMeeting` was called with a local `gemma3:4b` Ollama-compatible model for five actual AI Director-model submissions: Librarian, Architect, Beat Writer, Umpire, Closer.

- Time receipt (UTC): `2026-11-20T19:24:39.730Z`
- Explicit Director responses: **5/5 returned**, **0 provider errors**.
- Local full JSON receipt: `/tmp/schemin_locfolio_board_20261120.json` on the connected Mac (not committed into Git).
- Full board receipt SHA-256: `4799fc2fc20dfebacda02c87fba2c80c5d773b9aa5c7d5e819d2eb395813eac1`.
- Canonical route was computed separately with `routeTask` and material counterweights. It returned **Umpire primary; Analyst/Architect/Beat Writer/Bookkeeper secondary; Architect+Closer counterweights**.
- Route receipt SHA-256: `c23ea3f13e8265d12769c5b0f7815093b2f2064c25278cc4a21647a5ce1f7852`.
- The five explicitly convened Director AI submissions are distinct from the broader route participant set. No uncalled role is counted as an independent submission.
- These were **local AI-role consultations, not independent human Directors, published-author participation, authenticated human counsel, or an approved Umpire production sign-off**. Content is below critically adjudicated against source records.

## 3. Reviewed Director positions and disposition

| Domain | Submission and material concern | Adjudicated board instruction |
|---|---|---|
| Librarian | Source authority and provenance will drift when benchmark imagery and historical states meet many location identifiers. | **ACCEPT**: single ID-indexed manifest; every asset binds current location card, referenced structural plate, original source evidence and historical state; **REJECT** ungated reassignment of style images to LOC identities. |
| Architect | Place-data integrity, deterministic naming and downstream reusability need automated validation. | **ACCEPT WITH SCOPE CONTROL**: consume existing World Engine, 23 structural plate URIs and Reference Registry; add minimum needed checkable manifest and acceptance script; **REJECT** treating existing Atlas infrastructure as unimplemented. |
| Beat Writer | Visual atmosphere alone cannot prove 2015–2026 continuity. | **ACCEPT**: material scars, event memory, repair, chronology and contextual witnesses define historical variants. Do not invent owner tenure or carry a contemporary object backward in time. |
| Umpire | Artistic quality criteria and no-auto-promotion gate remain subjective without testable controls. | **ACCEPT FOR PROMOTION**: enforce IDs/paths/metadata mechanically and require human-visible quality review for imagery; **REJECT** stopping reversible inventory, briefing or candidate generation merely to invent a new governance OS. |
| Closer | Manage complexity and stage production rather than yield 23 disconnected attractive pictures. | **ACCEPT**: seven regional plates, 23 individual masters, historical evidence-gated variants; site-review pilot before full batch. **REJECT** unsupported numeric director-hour estimates and inaccurate claim that founder images are historical map truth. |
| Counterweight: Architect vs. Umpire | Governance risks slowing useful reversible work. | **DECISION CHANGED**: use lightweight machine-checkable manifest immediately; preserve the image-approval gate; do not launch a separate framework or stall early render candidates. |
| Counterweight: Closer vs. Umpire | Misinterpretation of release gates as a prohibition on all draft progress. | **DECISION CHANGED**: production preparation can proceed; final cinematic reference promotion still blocks pending real review. |

## 4. Evidence the Board actually reviewed (repository-grounded)

- `world/data/locations.json` contains **23 active LOC IDs**, statuses 8 PERMANENT_CANON, 12 PROVISIONAL_CANON, 3 INTERPRETIVE_CANON.
- `world/location-control-plane/registries/LOCATION_REFERENCE_REGISTRY.json` has **23 structural reference entries** and **0 approved cinematic** references.
- `world/data/atlas_location_candidates.json` has **48 separate editorial CAND IDs**. These are not a queue of authorized active site masters.
- `world/production/CANONICAL_WORLD_PLATE_SPATIAL_BLUEPRINT_V1.md` fixes seven-zone placement, 23 LOC positions in abstract map space and governing route adjacency.
- Existing visual authority `world/environment-references/ENVIRONMENT_REFERENCE_AUTHORITY_V2.md` expressly requires independent approval of true cinematic reference bytes.
- Founder sample images supplied in this conversation are each **1672×941 pixels**, close to 16:9, not permanent GitHub image assets.
- Separate draft PR #322 proposes postseason island geography and Last Field relocation from an earlier Central Basin hypothesis. **No live map promotion** in this mission.

## 5. Explicit outputs and file contracts

**Foundational deliverables:** seven `REG-*` establishing panoramas + 23 individual LOC cinematic master PNGs = **30 baseline images**, followed by site-specific ground/detail plates and evidence-backed historical variants. This is a floor for place coverage, not a claim that renders exist.

**Single-plate contract:** immutable LOC ID; name; physical region; canon tier; structural reference path; source card path; dominant visible landmarks; access and hydrology; spatial direction/view; atmosphere and season; visible scars; human-scale settlement; no unsupported character identity; timestamp/era; source SHA and prompt/camera version; file SHA-256; asset dimensions; renderer/provider metadata; reviewer, QA result, status and supersession pointer.

**Persistent naming:** `world/environment-references/cinematic-folio/plates/<LOC-ID>/` with `CANDIDATE_MASTER_16x9.png` pending review, and `history/<verified-time-or-event>/` for controlled historical state. Derive production-ready compositional variants without changing place identity.

**Seven-zone flight sequence:** Northern Spine → Upper Valleys → Central Basin → Western Tablelands → Southern Wetlands → Eastern Storm Coast → Inner Sea Littoral, with wide transitional panoramas where actual route/terrain graph permits. This sequence is **editorial reading order**, not a license to rearrange geographic adjacency.

**Timeline:** render as-of-2026 baseline first with exact supported state; only add 2015–2025 before/after where the factual story packet supports it. Historic illustrations and their release records are input evidence, not automatically current visual canon.

## 6. Acceptance scoring (proposed, not an existing certified metric)

| Dimension | Max score | Real review evidence |
|---|---:|---|
| LOC and physical geography fidelity | 25 | Correct zone, terrain, climate, major landmark position and meaningful camera ground |
| Spatial relationships, roads and hydrology | 20 | Grounded route/causeway/water flow, sightlines and settlement connectivity |
| Landmark identity / architecture | 20 | Recognizable location-specific forms and materials, not interchangeable buildings |
| Hyper-real cinematic fidelity | 15 | Convincing lighting, scale, atmosphere, details and visual depth compared with Founder images |
| Temporal/world-state continuity | 10 | Verified era, damage/repair and appropriate technologies |
| Provenance/reusability | 10 | Asset ID, dimensions, source references, SHA, metadata, indexed approved status |

**Pilot acceptance candidate threshold:** 90/100 for a master proposed for promotion; any unsupported geography, false `LOC` assignment, made-up historical fact, invalid filename or missing source packet is an **absolute fail** irrespective of score. Human inspection is mandatory: a numerical score cannot certify itself.

## 7. Implementation phases and accountable handoffs

1. **SOURCE PACK GATE** — Librarian + Architect: enumerate 23 current LOC IDs, their cards, 23 structural URIs, route/region bindings; review candidate store firewall and historical state. The seed manifest is already committed in this PR.
2. **CINEMATIC LOOK LOCK** — project-local Visual Development + Beat Writer: analyze four provided reference images as style benchmarks; define repeatable lens, scale, lighting, material and detail priorities. Confirm visual text is added in post, not treated as grounded generated text.
3. **PILOT RENDERS** — produce independent candidates for `LOC-LEAGUE-CHAMBER`, `LOC-TRADE-JEDI-MOUNTAIN-BASE`, `LOC-MUD-DOGS-SWAMP`, `LOC-RED-RUINS` and an appropriate regional panorama. These exercise civic, upland, wetland and storm-coast extremes.
4. **DIRECT REVIEW / REPAIR** — independently inspect actual PNG pixels against semantic and structural source packets and supplied visual quality standard. Apply revisions to failing candidates, no silent canon promotion.
5. **REST OF THE WORLD** — render 19 remaining LOC masters + six remaining region panoramas by biome; group in navigable folios with consistent titles, geography and asset manifest.
6. **HISTORICAL EVOLUTION** — research verified temporal deltas by LOC and date/event, generate only supported before/after states, preserve historical supersession and avoid invented 2015 owner residency.
7. **CONSUMER INTEGRATION** — after proper approval, bind cinematic URI into the existing reference registry and add using-site references in Memo OS, Novel OS, Atlas and film. Keep existing structural references intact.
8. **FINAL INDEPENDENT REVIEW** — pixel-level QA, checksums/manifest parity, actual consumer resolution, provenance and publication receipts; Closer coordinates, Umpire separately gates.

## 8. Current disposition and prohibitions

**COMPLETED IN THIS BRANCH:** mission README; exhaustive 23-record manifest, all linked to active source IDs and their approved structural plate paths; source-grounded board decision and execution contract.

**NOT COMPLETED:** seven region PNGs; 23 LOC master PNGs; historical image variants; byte-level visual QA; approval, site publication, or changes to the canonical cinematic registry.

**HOLD:** No claim that the four supplied sample images are the genuine geological identity plates for the captions they happen to contain. No photo-derived mountain/river/road rearrangements. No `CAND-*` promotion or change to PR #322. No approval of unsurveyed modern infrastructure elsewhere on the mainland. No assertion of real human consultant participation. This document is a board-received **development ruling**, not final image authorization.

---

## Appendix — complete active LOC folio coverage (23)

### Northern Spine — REG-NORTHERN-SPINE
- `LOC-RED-SLOB-ALPINE-ROUTE` — Alpine Wager Route (PROVISIONAL_CANON)

### Upper Valleys & Foothills — REG-UPPER-VALLEYS
- `LOC-TRADE-JEDI-MOUNTAIN-BASE` — Trade Jedi Mountain Base (PERMANENT_CANON)
- `LOC-ARSENAL-BARBERSHOP` — Arsenal Barbershop (PERMANENT_CANON)
- `LOC-SLOB-FOOTHILL-CAMP` — Slob Foothill Camp (PROVISIONAL_CANON)
- `LOC-BRIDGE-MOUNTAIN-LAKE` — Bridge at the Mountain Lake (PROVISIONAL_CANON)
- `LOC-DK-HIGHLAND-STRONGHOLD` — D0nkey K0ng Highland Stronghold (INTERPRETIVE_CANON)

### Central River Basin — REG-CENTRAL-BASIN
- `LOC-CHINS-ROAD-COMMONS` — People's Champ Road Commons (PROVISIONAL_CANON)
- `LOC-LEAGUE-CHAMBER` — League Chamber (PROVISIONAL_CANON)
- `LOC-PITTSYS-BOOK` — Pittsy's Book (PROVISIONAL_CANON)
- `LOC-DK-MUD-HILL` — Mire Hill Battlefield (PROVISIONAL_CANON)
- `LOC-SOUTHERN-SPEEDWAY` — Southern Speedway (PROVISIONAL_CANON)
- `LOC-COMPACT-NEUTRAL-GROUNDS` — Compact Neutral Grounds (PROVISIONAL_CANON)
- `LOC-LEAGUE-ARCHIVE` — League Archive (INTERPRETIVE_CANON)

### Western Tablelands — REG-WESTERN-TABLELANDS
- `LOC-CHILI-STABLE` — Chili Outlaw Stable (PERMANENT_CANON)
- `LOC-TDS-CHILI-SHARED-MARCH` — TDS–Chili Shared March (INTERPRETIVE_CANON)

### Eastern Forest & Storm Coast — REG-EASTERN-STORM-COAST
- `LOC-STORM-BOWL` — Storm Bowl (PROVISIONAL_CANON)
- `LOC-RED-RUINS` — Red Leopard Ruins (PERMANENT_CANON)
- `LOC-BELT-KEEPER-KEEP` — Belt Keeper Rune Keep (PROVISIONAL_CANON)

### Southern Wetlands & Delta — REG-SOUTHERN-WETLANDS
- `LOC-MUD-DOGS-SWAMP` — Mud Dogs Swamp (PERMANENT_CANON)
- `LOC-COUNTRY-CLUB-JACKSON` — Country Club of Jackson (PERMANENT_CANON)
- `LOC-TDS-WATERFALL-TEMPLE` — Podium Shadow Waterfall Temple (PERMANENT_CANON)

### Inner Sea Littoral — REG-INNER-SEA-LITTORAL
- `LOC-LLC-BOARDROOM` — LLC Mercantile Boardroom (PERMANENT_CANON)
- `LOC-LLC-STORM-CITY` — LLC Port City Storm District (PROVISIONAL_CANON)

**Separate deferred inventories:** 48 editorial `CAND-*` (including `CAND-CHAMP-LAST-FIELD`) and 58 parent/sub-location handles must be handled by their own governed candidate/sub-location protocols rather than mislabeled as 71 independent active `LOC-*` masters.
