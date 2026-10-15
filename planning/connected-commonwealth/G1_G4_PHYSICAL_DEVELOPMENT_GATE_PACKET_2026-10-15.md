# Connected Commonwealth — G1–G4 Spatial Development Gate Packet

**Date:** 2026-10-15  
**Tracker:** #189 under #186 / parent #175  
**Authority:** 23 Commissioner-approved world-development decisions; `PROJECT_CONTROL_REGISTRY.md`; World Engine V1.1 / Atlas Control Plane V2.  
**State:** MULTI-GATE DESIGN + READ-ONLY PROTOTYPE; **NO NEW PHYSICAL CANON OR PRODUCTION ACCEPTANCE**.  
**Depends on:** G0 PR #187 with character guard repair. This is a stacked PR; it must not race ahead of G0 acceptance.

## Mission boundaries / anti-fork guarantee

- Existing `world/data/physical_zones.json`, `locations.json`, `routes.json`, `owner_domains.json`, `current_world_state.json`, `world_state_events.json` remain the only active World Engine truth for these fields.
- Do not create a new registry with separate authoritative REG/LOC/ROUTE coordinates. Any future metric geometry becomes a governed extension to canonical spatial authority, versioned and ID-reconciled.
- All seven physical regions, twelve primary owner homelands, existing 18 routes and 23 active locations are preserved.
- The `schemin-local-v1` `[x,y]` is **abstract layout**, not real feet, miles, hectares, elevation, EPSG coordinates, survey-grade geometry or source for real-world walking ETA.
- Published Weeks 1–5 are historical; do not reissue or edit their artwork, stories, scores or receipts during a physical-world design gate.
- `scheminnovel` Netlify belongs to the Living Novel preview pipeline. No Netlify deployment or site build requirement is added to World/Atlas.

## G1 — Metric Fidelity Specification (architecture proposal, pending Commissioner dimensions)

### Proposed coordinate doctrine

One canonical **secondary-world measurement namespace** under the existing spatial control plane, with:
1. Versioned *global* planar or terrain-local projected frame once approved; explicit origin, axis orientation, unit meters, elevation datum, uncertainty class, tectonic/hydrologic assumptions and provenance.
2. Nested property-local axes for building plans and site models, tied to approved canonical `LOC-*` IDs; local origins may be drafted without asserting geographic placement until reconciled.
3. Governed transform table from presentation `schemin-local-v1` abstract layout to future metric space, requiring empirically/canon-supported control pairs, QA residuals and versioned approval. **DO NOT** derive a meter-per-layout-unit factor from maps by eye.
4. Explicitly `UNKNOWN` for every unapproved longitude/latitude-equivalent, route length, elevation, parcel polygon, setback, road width, interior size or building height. No hidden scalar defaults.
5. `effective_world_time`, `recorded_at` and `source_reference` for changes, preserving archived model versions and prior publication snapshots.
6. Validation invariants: zone containment, location/owner identity, route/path endpoints, watershed direction, landform feasibility, region adjacency, finite dimensions only once approved, non-overlap rules once surveyed-style parcels exist.

### Architectural options offered for approval (no world size is selected)

- **Frame A:** One calibrated Commonwealth projected spatial reference after macro-region scale is justified by canon and travel constraints.
- **Frame B:** Property-local meter frames first; global transform remains `UNRESOLVED` until macro calibration.
- **Preferred staged program:** define the schema and local frame contracts now; defer real-scale filling until the Atlas/World authority and Commissioner approve reference scale and consistent terrain parameters.

This is consistent with interview Q16=C, Q21=C+D-future, not an approval of actual continent dimensions or 3D simulation.

### G1 exit gate

Document approved map units, frame definition, provenance ledger, schema migration plan, unknown-value policy, generated-view compatibility and a single actual distance/geometry pilot supported by user-approved canon source. Reject if the proposal is a free-standing World OS or purports to retrofit `schemin-local-v1` directly into meters.

**Current:** CONTRACT CANDIDATE; METRIC APPROVAL HOLD.

## G2 — Trade Jedi Mountain Base evidence/site architecture

### Canon evidence ledger

| Source | Established detail | What it does NOT prove |
|---|---|---|
| `LOC-TRADE-JEDI-MOUNTAIN-BASE` | Permanent location, Upper Valleys, `[69,69]` abstract, high ridge, war-room overlook | Acres, site bearing, height, GPS, road width |
| `world/location-control-plane/.../CARD.json` | Existing high-ridge and war-room-overlook sublocation handles; weather and access context | Full interior floor plans or surveyed property corners |
| `ROUTE-EASTERN-ASCENT` | Home-to-Mountain-Lake-Bridge route; foot/mount/wagon; exposed grade | Mileage, duration, vehicles or all-season open road |
| `LOC-BRIDGE-MOUNTAIN-LAKE` | Bridge and lake as known landmark; historically connected | Direct waterfront parcel ownership or lakehouse in Trade Jedi domain |
| `chronicles/production/reference-packets/environments/ENV-TRADE-JEDI-MOUNTAINS/PACKET.md` | Draft North-Georgia-inspired high-ridge atmosphere; timber/stone strategy room, long windows, paper table, cool morning | Approved renderer-grade environment refs (packet explicitly DRAFT) |
| `canon/characters/CHARACTER_REGISTRY.yaml` | Trade Jedi owner identity and **NO belt** | Character source-byte mount or portrait likeness acceptance |

### Three noncanonical site-arrangement alternatives for collaboration

**A — Ridgeline overlook above Eastern Ascent:** War-room occupies an upper approach overlook on a high ridge; access from an existing topological route. Pros: most conservative skyline reading and war-room panorama. Risks: exposure, grading and access-road feasibility. Unknown: ridge orientation, contour positions, road grade.

**B — Sheltered high-ridge spur with secondary valley service approach:** Preserve the required high ridge and overlook, but position ancillary operational functions on a lower bench; access logically descends from the known route. Pros: operational estate/ecology, coherent daily maintenance. Risks: proposed new service arrangements might go beyond published scenes. Unknown: acreage, bench slope, existing forest footprint.

**C — Ridge overlooking the mountain-lake watershed (not a proven lakefront estate):** Same high ridge/war-room placement but test view and weather relation to the bridge/lake setting. Pros: narrative/world connection to the lake/bridge lore. Risks: landmark visibility has **not** been canonically demonstrated; do not add lake view, water rights or shoreline parcel by inference.

**No option is the selected site.** Founder approval required for the chosen arrangement and each first specific metric measurement; additional evidence may eliminate options rather than voting from aesthetics alone.

### G2 conceptual property-system inventory, all detailed dimensions UNKNOWN

- Entry road connection and access control; approach, grade, seasonal closure and weather drainage.
- Terrain model, ridgeline/wooded landscape, defensible sightlines, ecological footprint and hydrological runoff.
- Primary residence and war-room overlook; rooms based on existing draft timber/stone strategy reference, not assumed completed blueprint.
- Power, water, waste, structural support, maintenance/storage, climate resilience and emergency access are required design questions, **not approved buildings**.
- Dog companion accommodation and character-safe staging only after body/companion reference binding.
- Sub-locations inherit `LOC-TRADE-JEDI-MOUNTAIN-BASE` rather than becoming arbitrary new permanent `LOC-*` IDs.

### G2 exit

Source-labeled alternative matrix, visual-reference provenance, Commissioner site selection, spatial frame/datum, reviewed asset list, character-canon sample scene, architectural site/floor plans and independent checks. Current state: **CANON SOURCES RESOLVED / SITE AND MEASUREMENT HOLD**.

## G3 — End-to-End Prototype (real incremental implementation, partial gate)

### Delivered read-only operation on development branch

Extended **existing** `world/atlas/interactive/build_interactive_atlas.py` (not new web app) and its deterministic `SCHEMIN_ATLAS_INTERACTIVE.html`. Users select active `LOC-*` origin and destination, click **Trace established roads**, inspect highlighted current-route network and route IDs. The default pair is the existing Trade Jedi Base → Mountain Lake Bridge. The Atlas still exposes existing structural plates.

Parallel developer/CI preview: `python world/atlas/interactive/read_only_route_preview.py LOC-TRADE-JEDI-MOUNTAIN-BASE LOC-BRIDGE-MOUNTAIN-LAKE`. Returns actual hop IDs, permanent landmark names, approved structural references and explicit `null` for distance, ETA, acreage and footprint. No scene render, property polygon or canon write.

**QA scope:** all 12 owner homes reach a central approved location via active route graph; rejects editorial `CAND-*`, unknown IDs, dangling endpoints and disconnected travel; source-linked view deterministic; proposed metric fields absent/nullable only.

### G3 NOT YET ACCEPTED

The desired G3 contract is:
1. map selection from the existing Atlas — **available on development branch**;
2. route tracing against actual World routes — **implemented for undirected topology only**;
3. actual site and building inspection with approved measured site geometry — **HOLD** (G1/G2 incomplete);
4. cinematic illustration using approved mounted environment + character source bytes — **HOLD**;
5. independent final visual/artifact inspection and publication proof — **HOLD**.

A topology preview is **not** verified physical travel at a given speed/mode, not proof all roads are traversable at any season, and not a digital twin.

## G4 — 12-owner development prioritization matrix (candidate ordering, not new canon)

| Owner / team | Existing location | Canon status | Physical development focus | Key dependency |
|---|---|---|---|---|
| Trade Jedi / ObiWan | `LOC-TRADE-JEDI-MOUNTAIN-BASE` | Permanent | Pilot ridge-site, war-room and transport geometry | G1 coordinate contract, G2 site approval |
| D0nkey K0ng | `LOC-DK-HIGHLAND-STRONGHOLD` | Interpretive | Highland roads, martial property, body-scaled infrastructure | Current gorilla-centaur guard, actual reference mount |
| Red Leopards | `LOC-RED-RUINS` | Permanent | Eastern escarpment ecology, ruins/settlement linkage | Settlement relationship unresolved |
| Mud Dogs | `LOC-MUD-DOGS-SWAMP` | Permanent | Waterlogged terrain, boardwalk/causeway access | Hydrology and wetland seasonal route QA |
| Three Dreaded Snake | `LOC-TDS-WATERFALL-TEMPLE` | Permanent | Waterfall escarpment, ritual spaces and shared march | Exact three-head anatomy/POV canon; road/falls conditions |
| Chili Cheesers | `LOC-CHILI-STABLE` | Permanent | Tableland range, stable service, road/water logistics | Final fictional site-name; Dark Horse |
| Dr. Duckhook | `LOC-COUNTRY-CLUB-JACKSON` | Permanent | Country-club estate, wetland edge and access/repair | Public/private use unresolved; seasonal flood |
| The LLC | `LOC-LLC-BOARDROOM` | Permanent | Mercantile HQ linked to port district | Historic intrusion and current repair state |
| Slob on my Dobb | `LOC-SLOB-FOOTHILL-CAMP` | Provisional | Mobile foothill camp / road staging | Final site name; avoid freezing mobile camp as mansion |
| His Majesty's Blood | `LOC-BELT-KEEPER-KEEP` | Provisional | Cliff keep, ruler/singular accommodation | Civil jurisdiction and naming unresolved |
| El Niño | `LOC-STORM-BOWL` | Provisional | Storm-safe coastal civic venue | Atmospheric/embodied distinction and venue purpose |
| Seven Deadly Chins | `LOC-CHINS-ROAD-COMMONS` | Provisional | Public roadside commons and infrastructure | Final name, actual commons tenure |

**Suggested development order for the Bullpen review (not adopted as canon):**
- Group 1: Trade Jedi → Bridge → DK/upper-valley network: first spatial co-visibility + shared access benchmark.
- Group 2: Mud Dogs → Duckhook → TDS: same watershed, varied mobility/infrastructure requirements.
- Group 3: Red Leopards → Belt Keeper → El Niño: escarpment, coast, severe-weather exposure.
- Group 4: Chili → Seven Chins → LLC → Slob: range/commons/port/mobile camp variation.
The order is **operational prioritization**, not narrative character importance. Reprioritize based on actual Weekly Memo/Novel demand, canon source completeness and renderer readiness.

## Multi-gate QA and disposition

| Gate | Production status | What can be reviewed now | Mandatory remaining evidence |
|---|---|---|---|
| G0 source baseline | Draft PR #187, CI for code green | 23 decisions + precise registered data | Independent authenticated Umpire/owner resolution |
| G1 spatial law | **DESIGN CANDIDATE** | Units/migration/uncertainty doctrine | Commissioner-approved reference system and metric proof |
| G2 Trade Jedi property | **CONCEPT OPTIONS ONLY** | Canon-first site alternatives and dependency dossier | Selected approved plot, spatial constraints, architectural/raster QA |
| G3 interactive route trial | **PARTIAL EXECUTABLE PROTOTYPE** | Read-only Atlas route trace and structural link | Metric property inspection, cinematic actual render and independent review |
| G4 owner program | **INVENTORY + CANDIDATE SEQUENCE** | 12/12 dependencies and proposed cohorts | Reviewed priority sequence, property-specific source and gate receipts |

**Production promotion is blocked.** Do not merge G1/G2 proposals as if they are approved fictional structures. Merge of read-only engineering/view-only improvements requires passing CI on exact head and legitimate PR reviews. This packet does not claim a real Bullpen meeting or authenticated Umpire invocation.