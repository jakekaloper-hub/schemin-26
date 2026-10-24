# Week 7 — Integrated Geoscience and Existing-Engine Coexistence Review
Status: TECHNICAL DESIGN REVIEW / COMPOSITE ADVISORY LENSES / NOT ACTIVE GEOGRAPHY
Evidence: world/data/locations.json, routes.json, physical_zones.json, current_world_state.json, atlas_location_candidates.json, PHYSICAL_ATLAS_V1.md, LOCATION_CONTROL_PLANE_ARCHITECTURE_V1.md, FUTURE_LOCATION_UNLOCK_FRAMEWORK_V1.md.
Bullpen governance: jakekaloper-hub/bullpen/docs/EXTERNAL_ADVISORY_PROGRAM_V1.md; composite lenses are NOT real persons or authenticated ConsultEngine invocations.

## Decision: nested feature handles, not six autonomous LOCs
Current branch registers six CAND records as potential sites. These are NOT active location records and do not appear as real geography. For each, define an eventual derived handle `SUB::{PARENT_LOC}::{SLUG}` using the existing Location Control Plane. The parent LOC retains physical zone, abstract position, climate, owner, division overlay, route, current state and provenance. Candidate registry remains editorial until event justification, scientific feasibility, and explicit promotion. Do not create six new coordinates or duplicate regional roads. If permanent independently addressable site is not justified, keep as sublocation handle.

## Consulting Engine proposal — stable role identifiers
These are proposed **COMPOSITE_SPECIALIST** adapters to the existing Bullpen External Advisory Program, NOT new Directors, not named scientists, and not registered in live ConsultEngine:
- `geo_geomorphology_slope`: geomorphologist / engineering-geology composite. Sources to research: USGS landslide hazards, engineering geology and rock mechanics references. Reviews escarpment lithology assumptions, drainage, slope stability, foundations, erosion, cliff safety. Limits: cannot certify site without surveys.
- `geo_hydrology_watersheds`: catchment hydrologist / wetland hydrogeomorphologist composite. Sources to research: USGS water science, NOAA precipitation/flood frameworks, wetland hydrology references. Reviews runoff, floodplain, seasonal connectivity, sediment and headwaters. Limits: no quantified flood recurrence without climate/hydrology data.
- `geo_landscape_ecology`: landscape ecologist / habitat-planning composite. Sources to research: ecological landscape connectivity and habitat assessment literature. Reviews habitat, deer range plausibility, land disturbance, clearing footprint, invasive risk. Limits: no species census or real-world hunting permit assertion.
- `geo_landscape_architecture`: landscape architect / sports-ground planning composite. Sources to research: professional site-planning and sports-surface design references, Andrew Green public golf design documentation for design questions only. Reviews circulation, drainage, sightlines, turf/ground management, accessibility, and adaptive reuse. Limits: no attribution of direct involvement.
- `geo_transport_topology`: GIS / transportation-network composite. Sources: World Engine routes, graph and Location Control Plane schemas. Reviews parent-child graph and traversability; does not infer mileage or time from abstract coordinates.

ConsultEngine route: The Closer -> Scout/Librarian evidence freeze -> 5 independent composite review packets -> World/Atlas Architect reconciliation -> Umpire. A persona profile alone does not constitute a runtime call. IDs should be proposed in a Schemin project adapter and only registered in Bullpen core after its separate governance/tests.

## Parent integration matrix
| Candidate | Parent LOC | Derived handle proposal | Physical mechanism | Existing world dependency | Gate |
|---|---|---|---|---|---|
| CAND-W7-RED-CLIFF-HALFCOURT | LOC-RED-RUINS | SUB::LOC-RED-RUINS::CLIFF-HALFCOURT | storm-coast escarpment terrace; bedrock/stable fill unknown | rain escarpment road; ruin state; storm runoff | slope stability, sports material, GOTW home override |
| CAND-W7-JEDI-CLIFF-DUEL | LOC-TRADE-JEDI-MOUNTAIN-BASE | SUB::LOC-TRADE-JEDI-MOUNTAIN-BASE::DUEL-TERRACE | Upper Valleys ridge, wind exposure, possible freeze/thaw | Eastern Ascent, high ridge/war-room overlook | fall hazards, visitor access, beam/bar engineering |
| CAND-W7-TDS-FALLS-GOLF | LOC-TDS-WATERFALL-TEMPLE | SUB::LOC-TDS-WATERFALL-TEMPLE::GOLF-LOOP | wet escarpment headwaters, soil saturation and sediment | Falls Path, waterfall/temple footprint | drainage, temple avoidance, feasible clearings, tech |
| CAND-W7-DK-STRONGHOLD-HALL | LOC-DK-HIGHLAND-STRONGHOLD | SUB::LOC-DK-HIGHLAND-STRONGHOLD::HOSPITALITY-HALL | highland structure; winter/wind exposure | stronghold access and native construction | interior continuity and El Niño weather mode |
| CAND-W7-MUD-BUCK-TRACK | LOC-MUD-DOGS-SWAMP | SUB::LOC-MUD-DOGS-SWAMP::BUCK-CORRIDOR | deltaic wetland hydrology, cypress channel/raised ground | Delta Causeway, prior swamp scars, seasonal flooding | ecology, dry passage, Chili incoming route |
| CAND-W7-SLOB-MANCAVE-POKER | LOC-SLOB-FOOTHILL-CAMP | SUB::LOC-SLOB-FOOTHILL-CAMP::MANCAVE-TABLE | foothill camp interior on stable elevated ground | Hearthroad via camp; established man cave evidence | interior reference, currency/technology, LLC route |

## Scientific integration — site-specific recommendations
1. Red court: existing stable platform should be established before any hoop design. Avoid building on unsupported escarpment rim, unstable colluvium, or archaeological ruin fabric. Runoff must drain away from playable surface and protected ruins; mist is weather conditional. The distant cliff should remain a topographic background, not imply an impossible overhang. Parent remains LOC-RED-RUINS. GOTW neutral-site exception remains a separate governance requirement.
2. Jedi terrace: inherit ridge and high-elevation wind. Do not invent exact elevation or line of sight to the historic bridge. Keep stable approach, setback from cliff edge, and separate safe acrobatic fixture location. A gymnastic bar is not assumed to be part of the ancient base.
3. TDS golf: proposed three-hole loop is a **scale hypothesis**, not surveyed buildable area. Use existing dry benches and naturally open areas; avoid excavating the waterfall channel, headwaters or temple foundation. Bunkers require sand supply, drainage and maintenance; avoid assuming turf tolerates continuous shade/saturation. Site may ultimately reduce to one practice hole if no viable loop exists.
4. DK hall: favor adaptive reuse inside established stronghold rather than a new external building. Check room adjacency, ventilation, roof drainage and climate/weather intrusion. No unsupported modern hospitality infrastructure.
5. Mud deer corridor: use elevated browse edges and seasonal wetland passages. A 14-point buck is a story-specific individual, not proof of regional species density. Avoid irreversible habitat modification. The camera clearing and blinds are temporary features; access through Delta Causeway alone does not establish Chili's complete travel path.
6. Slob poker: reuse the already published man cave, treating table as furnishing rather than new geography. Check floor loading, access, smoke/ventilation, light, exit, and canon-appropriate money/card system. Helicopter is not supported by current transport modes.

## Causal cross-site integrity
- These six sites are **not connected by a new road network**. Their parents already sit in the canonical regional graph. Visitor paths must be computed on existing routes; internal approach remains a feature-level design question.
- No fabricated metric distance, coordinate, soil type, rock type, vegetation species census, flood probability, construction materials or technology unlock.
- Historical scar/repair/weather state must hydrate from current_world_state and world_state_events at the time of use.
- A render, script, memo page or consultant recommendation never promotes a CAND to LOC.
- Future site usage should resolve parent LOC first; candidate feature remains provisional until accepted. Preserve previous Atlas card references and visual grounding.

## Acceptance tests required
A. Schema validation for six CAND entries against schemas/atlas-location-candidate.schema.json.
B. Parent LOC exists, matching zone, no duplicate CAND IDs, no newly created LOC or route for these candidates.
C. All six proposed SUB handles follow Location Control Plane grammar; none treated as active.
D. World Packet compilation at parent LOC for relevant characters/consumer; note candidate not accepted by active resolver.
E. Full visitor multi-hop route, current-state/hydrology/weather, inhabitant and visual-reference audit.
F. Scientific feasibility review must distinguish plausible, conditional and unsupported physical assumptions.
G. Umpire independent test receipts and approval before any active promotion.

## Verdict
STRUCTURAL COEXISTENCE: supported by existing engine architecture.
REGISTERED CANDIDATES: yes, on draft branch.
SCIENTIFIC FIELD VALIDATION: not performed; no geotechnical or hydrologic survey exists.
AUTHENTIC CONSULTENGINE INVOCATION: not performed; five composite IDs proposed.
ACTIVE MAP PROMOTION: blocked pending normal gates.
