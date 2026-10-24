# G0 — Connected Commonwealth Physical Development Baseline & Gap Reconciliation

**State:** SOURCE INVENTORY COMPLETED / PROPOSAL PREPARED / G0 INDEPENDENT ACCEPTANCE HOLD  
**Date:** 2026-10-15  
**Issue:** #186; parent Commonwealth expansion mission #175  
**Baseline:** `main@c6fccb5ed27328c2a82c7369fb44dec34d9cb4a2`  
**Change branch:** `mission-186-commonwealth-physical-g0`  
**Approved direction:** `G0_COMMISSIONER_WORLD_DEVELOPMENT_VISION_2026-10-15.md` (23 interview decisions).  
**Scope:** source-backed assessment, controlled cross-OS proposal, and explicitly separate bounded character-canon correction. No world-size, parcel, building or route-length assertions are authorized by this report.

## 1. Executive verdict

The Commonwealth is **not an empty new project**. World Engine V1.1, Universe OS V1.2 / Atlas Control Plane V2, World Engine JSON stores, Atlas Phase 1–5, Location Control Plane, seven-zone geography, twelve owner homelands and routes already exist. Recent #175 phases produced engineering context and rehearsals across Memo, Novel and visual consumers. Full publication acceptance remains separate and incompletely proven; see `planning/connected-commonwealth/PHASE_5_7_ACCEPTANCE_REPORT.md` and `PHASE_4_PRODUCTION_ACTIVATION_RECEIPT.md`.

The approved 23-question vision asks for additional **metric fidelity, property/ecosystem definition, persistent approved cinematic environment assets and eventual 3D**. Those details must extend the existing one-world control plane, not establish independent GIS/canon stores or silently make existing abstract coordinates into miles.

### Verified snapshot inventory (JSON / registries on the baseline)

| Asset class | Observed evidence | Boundary |
|---|---:|---|
| Physical regions | 7 `world/data/physical_zones.json` | Macro-regions / abstract bounds, not geographic surveys |
| Active `LOC-*` locations | 23 `world/data/locations.json` | 8 permanent, 12 provisional, 3 interpretive |
| Active `ROUTE-*` edges/records | 18 `world/data/routes.json` | Qualitative routes, travel modes and hazards; not measured lengths |
| Character owner domains | 12 `world/data/owner_domains.json` | All twelve have primary `LOC-*` anchors |
| Settlement texture contexts | 7 `world/data/settlements.json` | Explicit RELEASE_CANDIDATE, inferred unnamed texture, not cities promoted by name |
| Location relationship graph | 59 `world/data/location_relationship_graph.json` | Derived graph / RELEASE_CANDIDATE; not alternative geographic truth |
| Editorial candidate locations | 48 `world/data/atlas_location_candidates.json` | NOT active geography; candidate promotion requires governance |
| Existing structural environment plates | 23 `world/environment-references/plates/**` | Diagrammatic structural references, not cinematic approvals |
| Atlas viewer | `world/atlas/interactive/SCHEMIN_ATLAS_INTERACTIVE.html` | Existing read-only map; not a metric 3D digital twin |
| Temporal world-state event records | 7 `world/data/world_state_events.json` | Events retain provenance and explicit classification |

**Connectivity check performed from authoritative 18 route chains:** all 23 existing active locations were found in one undirected topological component, with no dangling route endpoints in this snapshot. This establishes graph connectivity only. It does **not** prove travel duration, direction, physical feasibility at a specific season, transport capacity, exact road distance or surface conditions.

**Metric check:** `world/data/physical_zones.json` explicitly declares `schemin-local-v1 (abstract, non-metric)`. The current active location records contain abstract `[x, y]` positions, but no vetted metric parcel boundaries, building footprints, common elevation datum or real-world mileage. Do not rescale 0–100 positions to kilometers or feet without a Commissioner-approved migration model.

## 2. Twelve-owner location register (baseline, not proposals)

| Owner character | Canonical primary location | Physical region | LOC evidence class | Particular open question/constraint |
|---|---|---|---|---|
| ObiWan Jacoby / Trade Jedi | `LOC-TRADE-JEDI-MOUNTAIN-BASE` | Upper Valleys | PERMANENT | Final fictional place-name; property size/elevation/buildings unknown |
| Red Leopards / Predator Board | `LOC-RED-RUINS` | Eastern Storm Coast | PERMANENT | Relationship to ordinary settlement unresolved |
| Slob on my Dobb / Frat-Bro Berserker | `LOC-SLOB-FOOTHILL-CAMP` | Upper Valleys | PROVISIONAL | Final name; mobile-camp tenure, facilities and road access to develop |
| The LLC / Hostile Takeover | `LOC-LLC-BOARDROOM` | Inner Sea Littoral | PERMANENT | Commercial building/site measurements unknown; preserve intrusion/repair memory |
| D0nkey K0ng / Arsenal Gorilla Centaur Warrior | `LOC-DK-HIGHLAND-STRONGHOLD` | Upper Valleys | INTERPRETIVE | Final proper place-name; current morphology is ONE gorilla-upper + four-legged equine lower body |
| Three Dreaded Snake / Podium Shadow | `LOC-TDS-WATERFALL-TEMPLE` | Southern Wetlands | PERMANENT | Wet escarpment/waterfall systems; one body, exactly three serpent heads |
| Chili Cheesers / Chili Outlaw | `LOC-CHILI-STABLE` | Western Tablelands | PERMANENT | Final fictional name; The Dark Horse; shared march with TDS |
| His Majesty's Blood / Belt Keeper | `LOC-BELT-KEEPER-KEEP` | Eastern Storm Coast | PROVISIONAL | Final name / civil jurisdiction; belt ownership distinct from domain sovereignty |
| El Niño / Weather System | `LOC-STORM-BOWL` | Eastern Storm Coast | PROVISIONAL | Civic function unresolved; storms must not all be deemed El Niño |
| Mud Dogs / Swamp-Born Menace | `LOC-MUD-DOGS-SWAMP` | Southern Wetlands | PERMANENT | Site/ecology and wetland mobility require physical design |
| Seven Deadly Chins / People's Champ | `LOC-CHINS-ROAD-COMMONS` | Central Basin | PROVISIONAL | Final place-name and actual commons/road structures pending |
| Dr. Duckhook / King of the Impossible Lie | `LOC-COUNTRY-CLUB-JACKSON` | Southern Wetlands | PERMANENT | Public/private access unclear; maintenance/cleanup continuity required |

**Important distinctions:** character-domain status is stored separately (interpretive in the owner-domain register), while associated location status varies. Character identity is established by `canon/_INDEX.md` and `canon/characters/CHARACTER_REGISTRY.yaml`, not extracted from old environment narration. Division placement is a League-cultural overlay, not citizenship, biome or land ownership.

## 3. Trade Jedi first-site evidence dossier

**Owner** `CHAR-JAKE-KALOPER` / ObiWan Jacoby / Trade Jedi. **Home** `LOC-TRADE-JEDI-MOUNTAIN-BASE`. **Region** `REG-UPPER-VALLEYS`. **Abstract Atlas point** `[69,69]` (not GPS). **Domain** territorial-strategic; Burgers cultural overlay. **Persistent physical features** high ridge; war-room overlook. **Functional environment** North-Georgia-inspired forested upland, timber/stone strategy room, long windows, working table and mountain view as outlined in `chronicles/production/reference-packets/environments/ENV-TRADE-JEDI-MOUNTAINS/PACKET.md` (draft visual references, not approved cinematic plates). **Hard character law** youthful blond human Trade Jedi, earth-tone layers, green sword and golden retriever, NO championship belt; exact source-byte rendering gate remains separately enforced.

**Existing route:** `ROUTE-EASTERN-ASCENT` connects `LOC-TRADE-JEDI-MOUNTAIN-BASE` → `LOC-BRIDGE-MOUNTAIN-LAKE`; modes foot/mount/wagon; steep grades and weather exposure. From that bridge, `ROUTE-UPPER-BASIN-CONNECTOR` reaches `LOC-LEAGUE-CHAMBER`. This is a **valid proposed prototype path through existing route records**, not a measured driving itinerary. `ROUTE-BLACK-CLIFF` separately connects the Belt Keeper's Keep to the Trade Jedi base.

**Not established:** boundaries, acreage, ownership deeds, slopes and contours, building footprints, road widths, elevation datum, interior floor plan, compass-true camera vectors, route miles/hours, utility networks, final site address/name or approved cinematic exterior reference. No number may be promoted during G0.

**First collaborative design options for G1/G2:** compare ridge-overlook, protected-valley and mountain-lake-adjacent site arrangements only after reconstructing canonical sightlines and constraints; each alternative must honor the existing high ridge/war-room overlook, region, known route, mountain-lake bridge relationship, watershed, and likely access road. Proposals remain non-canon.

## 4. Metric / engineering precision proposals (G1 decision, NOT CURRENT CANON)

**Option A — Calibrated regional coordinate extension:** retain `schemin-local-v1` as presentation-only abstract coordinates; adopt a separately versioned **projected metric world coordinate reference** under World Engine governance, with declared origin, axis orientation, meters, dimensional scale and source-specific confidence. Map active LOC IDs with validated transform records. No relabeling abstract [x,y] as metric data.

**Option B — Local surveyed-style site spaces nested in coarse regions:** assign approved local origin, rotation and meters for each property when developed; transformation to world reference remains provisional until continental calibration. Supports accurate buildings before continental distances exist, but must not imply route mileage until integrated.

**Recommended future combination:** A + B, staged. World/Atlas authority supplies coordinate-frame proposal and uncertainty policy; Commissioner chooses dimensions. Each property would require elevation datum, terrain mesh provenance, parcel perimeter, footprint/floor schedule, access alignment, utility constraints, view corridors, route interface, effective chronology and exact source approvals. Architectural plans must be flagged fictional design geometry rather than real surveyed engineering certifications.

**Non-goal:** use actual Atlanta/North Georgia lat/lon or real county property boundaries as fictional-world truth.

## 5. Production and consumer integration inventory

- **World Engine** remains active source for REG/LOC/ROUTE/owner domains/state under `world/data/`.
- **Universe Resolver / Atlas** derive containment, season overlays, route/hydrology/horizon relationships; the Interactive Atlas is a read-only view.
- **Location Control Plane** derives 12 Homeland Cards, 23 Location Cards and reference status; it cannot promote canon.
- **Environment References** have 23 structural plates; current cinematic reference approval must not be assumed.
- **Memo OS** consumes fact-locked league event + location/home-host/travel identity; forward-only Commonwealth publication policy does not rewrite old issues.
- **Living Novel** uses owner-only principal POV, causal narrative and historical world state; #182 rewrite commission is not a finished published book.
- **Visual production** consumes typed world packets and verified character reference bindings; prompts/raster cannot create spatial authority.
- **World Evolution** is dry-run-first; canonical APPLY after approved evidence + gates, with historical versioning.
- **Connected Commonwealth work under #175** has merged code and staged rehearsal receipts, but its own Phase 5–7 report explicitly marks complete publication acceptance blocked.

## 6. Risk / discrepancy register

| ID | Severity | Finding | Controlling action | Current state |
|---|---|---|---|---|
| G0-R01 | CRITICAL | Active `world/data/owner_domains.json` forbade centaur anatomy for Wilson despite Oct 2 approved gorilla-centaur identity; `validate_world.py` wrongly enforced it | Correct current active world/derived records, replace stale validator/test, retain historical release snapshots | PATCH ON G0 BRANCH, CI NOT YET VERIFIED |
| G0-R02 | HIGH | Metric scale and exact travel distances absent | Propose versioned metric migration; no distance claims until Commissioner/Atlas approval | G1 DESIGN DECISION OPEN |
| G0-R03 | HIGH | Property bounds, building/site elevations and interiors unregistered | Trace reference provenance, design options, approve flagships, build measurable site only after G1 | G2 OPEN |
| G0-R04 | HIGH | Structural plates not cinematic approved reference bytes | Source reference proof + permanent IDs + independent visual QA | BLOCKED FOR FINAL RENDER |
| G0-R05 | HIGH | Authenticated Bullpen Director and Umpire signoffs not demonstrated by sim boards | Authenticate and record actual invocation/attestation or label HOLD | NOT VERIFIED |
| G0-R06 | HIGH | Merged Commonwealth rehearsals do not prove final assembled Memo page or Novel manuscript integration | Exercise actual publisher with approved live reference/fact-lock receipts and independent QA | EXISTING #175 HOLD |
| G0-R07 | MEDIUM | V1.1 historical exports and old docs contain superseded gorilla-only statements | Treat as dated evidence; correct forward-facing active docs; no destructive rewrite of historical releases | HISTORICAL EXCEPTIONS DOCUMENTED |
| G0-R08 | MEDIUM | Named/unnamed civilization distinctions and private land claims can be conflated | Maintain inferred settlement texture vs verified LOC/civic/government status | FIREWALL REQUIRED |
| G0-R09 | MEDIUM | Story art may imply permanent walls, roads, geography from one cinematic panel | Environment/style view cannot mutate world; promote through evidence-first ledger | GATE REQUIRED |
| G0-R10 | MEDIUM | Old abstract coordinates may be mistaken for GPS/miles | Add units/version/unknown annotations at next spatial-model gate | G1 OPEN |

## 7. Proposed G1→G4 exit evidence

**G1 Spatial specification:** 7-zone topology unchanged or explicit approved migration; coherent reference frame/units/transform, elevation/watershed doctrine, source confidence, tested routes and owner anchor compatibility. Unknown miles remain unknown until supported.

**G2 Trade Jedi flagship:** approved site alternatives reviewed; Commissioner selects; detailed fictional parcel and building layout; environmental asset receipts; approved reference view set; historic state/version; no forced default lake/ridge acreage.

**G3 Demonstrator:** Atlas selection of `LOC-TRADE-JEDI-MOUNTAIN-BASE` → trace `ROUTE-EASTERN-ASCENT` to `LOC-BRIDGE-MOUNTAIN-LAKE` → inspect approved property/site and structures → produce controlled art with verified environment + character assets → independent scene-level QA. Explicit user-facing statuses for absent cinematic references or measurement uncertainty.

**G4 Scale-out:** jointly prioritize other eleven homes using source maturity, connected geography, production frequency, environmental variety and complexity, without creating parallel atlas/canon systems.

## 8. G0 gate disposition

- **EVIDENCE REVIEWED:** active locations, routes, domains, regions, settlement contexts, world-event records; relevant prior release and production receipts.
- **STATIC CHECK PERFORMED:** 12/12 owner home IDs resolve; 23 LOC IDs connected through authoritative 18-route graph; 0 dangling route endpoints found; 23 location canon statuses partition 8/12/3.
- **PATCH STAGED:** narrow forward-facing DK character-canon consistency update, regression replacement, derived records. No artwork/published Memo change.
- **NOT VERIFIED:** remote GitHub CI, live authenticated Directors/ConsultEngine, independent Umpire acceptance, approved metric projection, approved site, pixel-perfect Week 5 character reference montage, cinematic rendering.
- **NO CANON PROMOTION:** G0 source inventory and design options are not new physical-world truth.
- **DECISION:** **REVIEW PACKET PREPARED — G0 REMAINS HOLD** until CI and authority/independent gates produce actual receipts; then request Commissioner decision for G1.

**Linked authority:** `PROJECT_CONTROL_REGISTRY.md`, `world/governance/WORLD_DATA_OWNERSHIP_MATRIX_V1.md`, `world/atlas/PHYSICAL_ATLAS_V1.md`, `world/data/*.json`, `canon/_INDEX.md`, `planning/connected-commonwealth/PHASE_5_7_ACCEPTANCE_REPORT.md`.