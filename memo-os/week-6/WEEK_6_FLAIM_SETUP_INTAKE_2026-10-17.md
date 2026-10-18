# Week 6 — FLAIM fact intake and initial preproduction boundary

**Date captured:** Saturday, 2026-10-17 (US Eastern). **Status:** INITIAL FACTUAL SETUP / RESULTS NOT DECIDED.  
**Canonical repo:** `jakekaloper-hub/schemin-26`; existing Weekly Memo OS V5.5, World/Atlas, Character Canon, release-evidence gates.  
**Connected source:** Flaim Fantasy → ESPN public league **1417621**, 2026 NFL fantasy Week 6, read-only calls `get_user_session`, `get_league_info`, `get_matchups` (Weeks 4–6), `get_standings` and `get_transactions` on 2026-10-17. A live chat receipt is not an independently signed publication receipt.

October 17 draft-PR runtime-canon repair note (NOT promoted to main): The obsolete NO_CENTAUR_ANATOMY World Engine validator requirement and live domain/homeland guards referenced in Section E1 have been corrected to require the four-legged Arsenal Gorilla Centaur Warrior. The historical intake below is preserved as captured; publication depends on approved merge, primary-reference recovery and visual QA.

## A. Week 6 six-fixture intake

**Score so far:** ESPN `currentPoints`, not `totalPoints` (which remains zero while undecided). All six have `winner=UNDECIDED`; no final winners. The projections are provider projections **at capture**, not facts or locked creative outcomes. Home/away from provider.

| # | Home | Away | Current points H–A | Projected H–A | ESPN result |
|---:|---|---|---:|---:|---|
| 1 | Red Leopards | D0nkey K0ng | 0.00–0.00 | 122.28–142.59 | UNDECIDED |
| 2 | Dr. Duckhook | El Niño | 0.00–0.00 | 139.81–136.17 | UNDECIDED |
| 3 | Slob on my Dobb | ObiWan Jacoby | 33.60–0.00 | 164.80–156.61 | UNDECIDED |
| 4 | The Chili Cheesers | Seven Deadly Chins | 8.00–13.70 | 137.62–138.18 | UNDECIDED |
| 5 | Mud Dogs | His Majesty's Blood | 0.00–52.82 | 117.01–134.10 | UNDECIDED |
| 6 | Three Dreaded Snake | The LLC | 10.50–0.00 | 117.70–153.51 | UNDECIDED |

**Validation:** exactly six pairings, each of the twelve ESPN team identities once. Projections and points must be refreshed after changes. Do not pass any unfinished score to the final-result scoreboard as final.

## B. Verified completed Week 5 consequences available to editorial

| Winner | Loser | Winner points | Loser points |
|---|---|---:|---:|
| Dr. Duckhook | D0nkey K0ng | 184.91 | 141.44 |
| The Chili Cheesers | El Niño | 183.53 | 156.70 |
| ObiWan Jacoby | Red Leopards | 154.42 | 110.42 |
| Seven Deadly Chins | Slob on my Dobb | 170.46 | 134.70 |
| His Majesty's Blood | Three Dreaded Snake | 113.45 | 85.34 |
| The LLC | Mud Dogs | 193.73 | 127.09 |

All six winner fields were `HOME` or `AWAY`, none `UNDECIDED`. This also independently confirms the score arithmetic appearing in the existing Week 5 distributed-edition audit, but does not retroactively certify Week 5's PDF or art.

## C. Standings as reported after Week 5 (before Week 6 decisions)

| Rank | Team | Record | Points for |
|---:|---|---|---:|
| 1 | ObiWan Jacoby | 4–1 | 713.09 |
| 2 | Red Leopards | 3–2 | 745.70 |
| 3 | His Majesty's Blood | 3–2 | 671.55 |
| 4 | D0nkey K0ng | 3–2 | 762.07 |
| 5 | The Chili Cheesers | 3–2 | 754.58 |
| 6 | Slob on my Dobb | 2–3 | 797.16 |
| 7 | The LLC | 2–3 | 727.92 |
| 8 | El Niño | 2–3 | 717.42 |
| 9 | Dr. Duckhook | 2–3 | 709.72 |
| 10 | Seven Deadly Chins | 2–3 | 683.40 |
| 11 | Three Dreaded Snake | 2–3 | 621.11 |
| 12 | Mud Dogs | 2–3 | 637.13 |

Rank is Flaim/ESPN standings order, **not** a Memo editorial power ranking.

## D. Transaction intelligence — bounded, not complete

Flaim returned 18 recent transactions for periods 5–6. Its response explicitly reports `structured_details_incomplete=true` and `possibly_truncated=true`; do not claim exhaustive league transaction coverage or create an invented trade narrative.

Evidence examples: TDS claimed Courtland Sutton for FAAB $7 on Oct 15; Red Leopards added Jameis Winston and Kimani Vidal on Oct 14; Chili added Pierre Strong Jr. on Oct 15; Slob added Jacob Cowing and Jalen Royals on Oct 16; Seven Deadly Chins added Kendrick Bourne on Oct 17. A trade-decline row for TDS has `trade_details_unavailable`, so **no player exchange or motivation is known** from this row.

## E. Six provisional preproduction lenses — NOT canon, not result scripts

1. **Red Leopards hosting D0nkey K0ng:** Both 3–2; both lost Week 5. DK visits the Leopards' verified home context.
2. **Dr. Duckhook hosting El Niño:** Duckhook's 184.91-point Week 5 win meets El Niño after a Week 5 defeat; country-club host continuity.
3. **Slob on my Dobb hosting ObiWan Jacoby:** Slob has league-high 797.16 points through Week 5 despite 2–3. Leader ObiWan travels to Slob's home; ObiWan carries no belt.
4. **The Chili Cheesers hosting Seven Deadly Chins:** Two Week 5 winners collide; Chili Outlaw/Dark Horse and Chins are locked, with no repeat of the prior high-noon conceit.
5. **Mud Dogs hosting His Majesty's Blood:** HMB arrives at Mud Dogs swamp after defeating TDS; HMB's belt ownership remains independent of weekly score.
6. **Three Dreaded Snake hosting The LLC:** TDS seeks recovery from 85.34-point Week 5; LLC enters following 193.73-point Week 5 victory; TDS exactly three heads, one body, post-haircut state.

Each pairing starts in the established **home team's** environment per World Engine V1.1. A neutral GOTW or special venue is **unselected** until explicitly approved. Every proposed scene must resolve real Atlas venue ID, approved away travel path, persistent state, twelve-owner reference packet and historical chronology before scene lock. The above dramatic premises are suggested editorial framings, not claims about what characters actually did.

## E1. Preliminary World Engine / Atlas host and route reconciliation

**Read-only source:** `world/encounters/ENCOUNTER_VENUE_RESOLVER_V1.md`, `world/data/owner_domains.json`, `world/data/locations.json`, `world/data/routes.json`, `world/data/current_world_state.json` (on main, 2026-10-17).

The following default home anchors come from the **existing twelve-owner location registry**, not new inventions. Preliminary route chains were found by undirected adjacency traversal across existing route endpoints and `via_location_ids`; this establishes **abstract graph connectivity only**. It is **not** a certified directed itinerary, passable route, chosen travel mode or current-week route-state approval.

| Home host / away visitor | Existing home location ID | Preliminary away-origin → host route ID chain |
|---|---|---|
| Red Leopards / D0nkey K0ng | `LOC-RED-RUINS` | `ROUTE-DK-HIGHLAND-LINK → ROUTE-HEARTHROAD → ROUTE-RAIN-ESCARPMENT` |
| Dr. Duckhook / El Niño | `LOC-COUNTRY-CLUB-JACKSON` | `ROUTE-STORM-COAST → ROUTE-PORT-BASIN-CONNECTOR → ROUTE-BASIN-MARKET → ROUTE-DELTA-CAUSEWAY` |
| Slob on my Dobb / ObiWan Jacoby | `LOC-SLOB-FOOTHILL-CAMP` | `ROUTE-EASTERN-ASCENT → ROUTE-HEARTHROAD` |
| Chili Cheesers / Seven Deadly Chins | `LOC-CHILI-STABLE` | `ROUTE-WESTERN-RANGE` |
| Mud Dogs / His Majesty's Blood | `LOC-MUD-DOGS-SWAMP` | `ROUTE-BLACK-CLIFF → ROUTE-EASTERN-ASCENT → ROUTE-UPPER-BASIN-CONNECTOR → ROUTE-BASIN-MARKET → ROUTE-DELTA-CAUSEWAY` |
| Three Dreaded Snake / The LLC | `LOC-TDS-WATERFALL-TEMPLE` | `ROUTE-INNER-SEA-QUAY → ROUTE-PORT-BASIN-CONNECTOR → ROUTE-BASIN-MARKET → ROUTE-DELTA-CAUSEWAY → ROUTE-FALLS-PATH` |

**Atlas approval gaps:** Validate connectivity against owning resolver's actual direction, transport capabilities, closures and evolving World State before publishing these as literal journeys. `current_world_state.json` is only stamped **end of Week 3**, not verified current for Week 6. The Country Club's Week 3 contamination/cleanup is unresolved; LLC's boardroom destruction/repair also remains under-specified. Do not depict either pristine or fully restored by default. The current `owner_domains.json` contains DK's stale `NO_CENTAUR_ANATOMY` guard, conflicting with the latest explicit four-legged Arsenal Gorilla Centaur canon; **character authority outranks the stale guard** and any scene involving DK must fail closed until the owning World records reconcile this inconsistency. A Game-of-the-Week designation could require an approved neutral site instead; no GOTW was selected in this intake.

## F. Week 6 production gates and known blockers

- **Facts / Scout:** six fixtures and current context retrieved; re-read results and standings at the actual weekly Fact Lock. No winners, point differentials, division crowns or implied playoff clinches from projections.
- **Story / Beat Writer:** build six differentiated setup→escalation→conditional-consequence concepts using prior released Week 5 effects. No unapproved geography, chronology reversals or extra principal POVs.
- **Canon / Librarian:** Wilson Look is one four-legged **Arsenal Gorilla Centaur Warrior** (not bipedal). TDS one body with exactly three serpent heads and post-haircut continuity. ObiWan Trade Jedi **no belt**. HMB Belt Keeper has the championship belt. Reconcile all remaining character packets through actual existing registry, not generic name prompts.
- **Art / Visual Lead:** final character-bearing generation remains **BLOCKED** by CHAR-PORT-002 raw-byte/hash/mount/subject-binding gates. Do not present drafted visual concepts as certified render output.
- **Atlas:** home venue, routes and environmental history require real ID resolution before Page Design Packet approvals; this intake does not create or promote locations.
- **Production / Groundskeeper:** all final scoreboard/statistical typography deterministic; 390px mobile QA, page-role continuity, true PDF bytes and exact printed page labels, final-raster subject QA and complete page set mandatory.
- **Release / Umpire:** no live authenticated Director consultation or independent Umpire acceptance occurred in this intake. Retain Week 6 as preproduction; never convert prose or simulated review into release PASS.

## Next handoff

Continue existing Week 6 production under Memo OS rather than create another OS: source refresh → facts separation → host/venue/route authority → 6 story packets → character-gate closure → controlled render C1 → page QA → final results → independent acceptance → Commissioner publication gate.

**Evidence status:** FLAIM/ESPN observed in connected live session, documented on a *review branch*. GitHub CI and Umpire review still required. No final artwork, PDF or release was produced.

## October 18 DK source gate — Red Leopards hosting DK

The old registered DK Week 3-cover JPEG depicts an upright Arsenal gorilla inconsistent with current four-legged Arsenal gorilla-centaur body canon. It is now ACTIVE_VISUAL_CANON_CONFLICT_HOLD even if original raw bytes are recovered. The October 12 four-legged illustration is an unpromoted candidate, not a substitute primary. Do not generate final Red Leopards versus DK art using the old source or candidate until explicit source-version and true binding plus generated-output acceptance gates pass.
