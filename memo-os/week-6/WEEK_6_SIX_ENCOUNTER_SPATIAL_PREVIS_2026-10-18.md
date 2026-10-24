# Week 6 — Spatial Previsualization and Action Continuity Packet
Date: 2026-10-18
Lifecycle: PREPRODUCTION SPECIFICATION / REVIEW REQUIRED, NOT RENDER CLEARED
Scope: six verified ESPN Week 6 matchups; all outcomes remain undecided at the last FLAIM fact lock.
Authority: existing Memo OS, Location Control Plane, World Engine, Character Control Plane, Encounter Venue Resolver, Novel OS, World Evolution. NO PARALLEL OS.

## Mission order
/bullpen mission --schemin-26 --week 6 --spatial-previsualization --reuse-canonical-os --six-encounters --character-lock --dry-run --test --audit --no-false-green

This is a documented handoff and executable design specification, not an authenticated invocation of separate Directors. Director/Umpire signoffs require actual receipts.

## Evidence receipt / technical baseline
Read live source files on 2026-10-18: world/data/locations.json, world/data/routes.json, world/data/current_world_state.json, world/location-control-plane/registries/LOCATION_REFERENCE_REGISTRY.json, world/location-control-plane/compiler/location_control_plane.py, world/encounters/ENCOUNTER_VENUE_RESOLVER_V1.md and world/atlas/phase-1/FUTURE_LOCATION_UNLOCK_FRAMEWORK_V1.md.
An independently evaluated graph traversal across the 18 registered route objects found a valid chain for each of six away-origin/home-target pairs. This is a graph-connectivity check only, NOT execution of Location Control Plane compiler or dynamic travel feasibility, route capacity, weather hazard testing, distance, or elevation simulation.
Every host location is registered. Slob's LOC is PROVISIONAL_CANON. All six registry records state MISSING_APPROVED_VISUAL_REFERENCE. Source coordinate space is abstract NON-METRIC: no accurate lengths, speeds, slopes, area, water depth, carrying capacity, or load calculations can be inferred.
Current-world-state file remains as_of end_of_week_3_2026. Week 4 and Week 5 released/story events are not automatically promoted physical changes.

## Six route receipts (success = graph connectivity, not safe travel)
1. GOTW: D0nkey K0ng Highland Stronghold > Arsenal Barbershop > Slob Foothill Camp > Bridge Mountain Lake > Red Leopard Ruins, via DK Highland Link / Hearthroad / Rain Escarpment. Home-domain GOTW needs COMMISSIONER-DIRECTED VENUE OVERRIDE entered in existing resolver.
2. Duckhook home: Storm Bowl > LLC Storm City > League Chamber > DK Mud Hill > Country Club of Jackson, via Storm Coast / Port-Basin / Basin Market / Delta Causeway.
3. Slob home: Trade Jedi Mountain Base > Bridge Mountain Lake > Slob Foothill Camp, via Eastern Ascent / Hearthroad.
4. Chili home: Chins Road Commons > Chili Stable, via Western Range.
5. Mud home: Belt Keeper Keep > Trade Jedi Mountain Base > Bridge Mountain Lake > League Chamber > DK Mud Hill > Mud Dogs Swamp, via Black Cliff / Eastern Ascent / Upper Basin / Basin Market / Delta Causeway.
6. TDS home: LLC Boardroom > LLC Storm City > League Chamber > DK Mud Hill > Mud Dogs Swamp > TDS Waterfall Temple, via Inner Sea Quay / Port-Basin / Basin Market / Delta Causeway / Falls Path.

## Previsualization contract (all six)
Each scene uses a parent LOC plus, when approved, a derived SUB feature. The plan must contain: (a) top-down adjacency diagram; (b) accessible participant and spectator ingress; (c) three persistent environmental anchors; (d) elevation section; (e) safe action zones and hazards; (f) minimum two consistent camera axes; (g) before/during/after object tracker; (h) winning and losing outcome branches; (i) route/state/reference proof; (j) named blockers. No image is authoritative merely because it looks cinematic.
A diagram denotes relative relationships only until metric engineering evidence is available. The user-approved story premise is a creative lock, not proof that engineered feature bytes exist.

## Matchup 1 — RED LEOPARDS (HOME) vs D0NKEY K0NG (AWAY): FOOTBALL GOTW
Parent: LOC-RED-RUINS, Eastern Storm Coast. Commissioner creative direction LOCK: Manchester United vs Arsenal football, Red Leopard in United football kit, ONE gorilla-centaur DK with FOUR equine legs in Arsenal football kit; Red home-domain pitch. Red's jungle ruins, predator banners, stormward terrain are mandatory.
Candidate derived scene features: SUB::LOC-RED-RUINS::SOCCER-TERRACE, western/away stone tunnel, home entrance, two terraces, pitch runoff, supporter market. Do NOT insert these handles in active registry merely because brainstorm uses them.
Top-down axis: [arrival via Rain Escarpment] -> [gated home/away circulation] -> [terraced pitch rectangle] -> [ruin wall / forest rim]. Goal A and Goal B at opposite short ends; supporters segregated from field. Use at least a goal-line low camera and a high oblique stadium view, with same goal orientation.
Section: test stepped benches, retaining walls, drainage and slope before dimension assignment. No fake regulation measurements based on abstract Atlas units. Field-action choreography must account for centaur motion, animal feet, traction, pitch surface, turning radius and goal/match rules; do not force bipedal soccer anatomy.
Pre: visiting Arsenal contingent, tense tunnel, rivalry banners. During: competitive football, physical crowd and shot mechanics. After: winner-dependent callback Red/Beckham 1999 curling goal vs Arsenal OR DK/Thierry Henry 2000 volley vs United; user-approved iconic inspirations, NO predicted result and no real player in scene.
Gate: record home-domain GOTW exception in existing Encounter Venue Resolver authority; verify stadium feature fit and access; verify separate reference-backed render identities. New permanent stadium LOC is NOT justified by this week alone.

## Matchup 2 — DUCKHOOK (HOME) vs EL NINO (AWAY): JACKSON INVITATIONAL
Parent: LOC-COUNTRY-CLUB-JACKSON, Southern Wetlands. Existing landmarks: clubhouse, golf grounds, water hazards. Existing Week 3 chili-dog contamination is remembered; cleanup status requires reconciliation.
Derived proposal: SUB::LOC-COUNTRY-CLUB-JACKSON::18TH-HOLE-CART-LOOP.
Top-down sequence: eighteenth green -> spectator/portrait terrace -> clubhouse banquet approach -> bounded golf-cart path -> existing water hazard; maintain consistent one-way chase route and an escape shoulder.
Pre: Duckhook celebrates Week 5 giant-slaying with celebrity tournament, portrait and tournament trophy. During: El Niño arrival, weather trouble, runaway trophy cart, escalating public humiliation and hazardous path toward water. After: Duckhook victory/comeback OR El Niño upset/weather-dominated scene. Portrait and trophy are continuous tracked objects, not teleporting props.
Engineering: cart lane width, plausible vehicle cornering and braking, slope/drainage, water separation and spectator evacuation all UNVERIFIED; do not create a new permanent storm event/damage from imagery. Weather System must retain approved ontological design.

## Matchup 3 — SLOB (HOME) vs OBIWAN (AWAY): FOOTHILL FIX
Parent: LOC-SLOB-FOOTHILL-CAMP, Upper Valleys, PROVISIONAL_CANON. Existing anchors: tailgate yard, rough training ground.
Derived proposal: SUB::LOC-SLOB-FOOTHILL-CAMP::DODGEBALL-COURT.
Top-down: public approach -> staging/waiting -> rectangular packed-earth court -> visible officials platform -> mud runoff area -> distant timber spectator rail. Camera A sees fair hit and official simultaneously; Camera B sees crowd, Slob, ObiWan, animal companions and penalty ledger continuity.
Pre: Slob 2-3 despite league-leading points, ObiWan 4-1, biased officiating setup, mocking 2025 runner-up trophy (historical runner-up only, ObiWan NEVER wears belt). During: fraudulent calls, dog-whistle theft, mockery backfires, spectator platform jeopardy without automatic injury. After: Slob 3-3 upset OR ObiWan 5-1 and public exposure of rigged officiating.
Engineering: minimum unobstructed court, clear spectator boundary, stable elevated judging point, projectile trajectories and collision exclusion. No invented permanent damage; pit bull and retriever identity remain distinct.

## Matchup 4 — CHILI (HOME) vs CHINS (AWAY): CHILI DOG RODEO
Parent: LOC-CHILI-STABLE, Western Tablelands. Existing anchors: stable, pit smoke, Dark Horse enclosure.
Derived proposal: SUB::LOC-CHILI-STABLE::RODEO-CORRAL.
Top-down: stable -> food market / delivery table -> gate -> barrel course -> wagon track arc -> livestock holding corral -> perimeter escape lane. Preplan the runaway wagon's travel from start to stop before image staging.
Pre: misdelivered recurring chili dog, unexplained label, Chins' raccoon. During: contest escalates into runaway wagon and horse chase, overturned stalls, endangered spectator rail, opportunistic rescue. After: Chili 4-2 victory at home OR Chins 3-3 upset and Chili 3-3; sender of package remains UNKNOWN until story proof.
Engineering: horse/animal behavior, wagon speed and turning, separation from crowd and food preparation fires; avoid modern mechanized rodeo technology, no inferred actual external prank.

## Matchup 5 — MUD DOGS (HOME) vs HMB (AWAY): BLACKWATER DEED JOB
Parent: LOC-MUD-DOGS-SWAMP, Southern Wetlands. Existing anchors: mud channels and raised ground. Prior Week 5 LLC survey/takeover is a released narrative concept, NOT established legal ownership.
Derived proposal: SUB::LOC-MUD-DOGS-SWAMP::BARGE-CHANNEL (channel/landing feasibility unresolved).
Top-down: causeway arrival -> swamp loading/landing -> navigable main channel bend -> small craft side approach -> constricted barge crossing -> raised landing / exit. Place two vessels in explicit relative positions each beat.
Pre: rumored company papers, Mud desperate after three losses, Belt Keeper travels to swamp. During: attempted interception of document barge, night boarding, collision/rope hazard, escape choices. After: Mud 3-3 defends reputation OR HMB 4-2 continues recovery; championship Belt never transfers, property title NOT adjudicated by fantasy result.
Engineering: navigable draft/depth, beam and channel width, current, river fog visibility, anchor/boarding reach, watercraft class. All unmeasured. Storm/flood effects cannot be promoted without World Evolution receipt. No automatic Blackwater Gaming Barge promotion.

## Matchup 6 — TDS (HOME) vs LLC (AWAY): FALLS PROTOCOL
Parent: LOC-TDS-WATERFALL-TEMPLE, Southern Wetlands. Existing anchors: waterfall, temple stone, dense vegetation. TDS ONE reptile body EXACTLY THREE heads, post Week 2 hair temporal lock.
Derived proposal: SUB::LOC-TDS-WATERFALL-TEMPLE::FALLS-APPROACH; hypothetical behind-falls vault HOLD pending authored reason and structural/geological viability.
Top-down: Falls Path arrival -> negotiation terrace -> upper stone passage -> footbridge -> possible waterfall recess -> return route. Camera A: bluff-wide layout to preserve access; Camera B: perpendicular bridge confrontation with same waterfall flow direction.
Pre: LLC corporate acquisition presentation after strong Week 5, TDS humiliation in magical chess, unsigned proposal. During: covert document/heist attempt, three heads watch multiple approaches but one body cannot split, bridge jeopardy, briefcase switch. After: TDS 3-3 repels intrusion OR LLC 3-3 follows up huge prior score; no real title/temple transfer and no invented magical vault canon.
Engineering: bridge anchoring, load-bearing feasibility, slippery rock, plunge-pool safety, mist visibility, stream direction; vault not approved merely for spectacle.

## Production priorities
P0: reconcile existing Week 6 GOTW Commissioner override and all six FLAIM pairings; preserve user-selected five story foundations. 
P1: compile six actual Location Control Plane world packets through compiler and archive stdout/results; map existing approved character-source bytes and identify missing location visuals.
P2: geometric top-down plan and section for Red football pitch, Mud channel and Falls Temple bridge; then simpler three event-feature plans.
P3: action test: entrances, scene-state positions per beat, object ledger and two camera angles; author room verifies humor, stakes and result forks.
P4: test with actual existing world/qa + memo tests, run independent Librarian/Atlas/Umpire acceptance, then only promote eligible feature/location records.
DO NOT build new OS; do not generate final art until reference/character QA is satisfied.

## Gate table — truthful current state
IMPLEMENTED: six specification packets consolidated in one preproduction document; host LOC references; scene choreography and candidate SUB handles (documentation only).
TESTED: structured 18-route graph traversal from six away origins to six host LOC targets, all six connected. This is a read-only independent graph traversal, not compiler CI.
AUDITED: semantic host/canon and visual-reference statuses read from authority; blocked items noted.
NOT TESTED: actual LCP compiler run, authored metric plans, bridge/stadium/hydrodynamic simulations, mobile PDF artifacts, temporal visual comparisons.
BLOCKED: six missing approved environment-image references; current world-state only through Week 3; geometry and safe action parameters missing; GotW home venue override not integrated into machine resolver; speculative vault not approved.
NO FALSE GREEN: this proposal is NOT READY FOR FINAL RENDER and includes no independent Umpire signoff.