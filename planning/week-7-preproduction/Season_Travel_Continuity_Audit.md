# Schemin — Season Travel and Encounter Continuity Audit

**Read-only source audit · 24 October 2026 · Week 7 open development**

**Recommendation:** build each encounter from the characters’ last supported whereabouts, motives and onward itinerary—not a weekly reset to their homes. The creative room should recommend locations; dot should supply evidence, alternatives and continuity checks. This document is an editorial proposal, not an authenticated Director meeting, venue lock, canon promotion or production release.

## 1. What the existing world already permits

The canonical Atlas distinguishes **seven physical zones** from **three nonexclusive league-division overlays**. The user’s three-region language should not silently overwrite that taxonomy: ask the creative room to reconcile its regional framing against these existing layers.

Keep these separate for every character:

- **Residence/home anchor:** persistent affiliation; not changed merely to shorten a journey.
- **Host domain:** territory within which an ordinary home encounter may occur.
- **Last supported whereabouts:** the latest approved scene or other location evidence, with time and confidence.
- **Current transit/camp:** a temporary position, not a new residence.
- **Encounter venue:** the precise shared setting, including neutral or regional sublocations.
- **Division and physical zone:** different classifications, neither a substitute for whereabouts.

Ordinary matchups default to the home domain, **not necessarily the residence or front door**. Existing location feature handles can support fresh staging within that domain. The special-event system also already defines **Tier 1 STORY-NEUTRAL LOCAL SITE**—for example, a road stop, market or fairground—with a **recorded venue override**. Therefore a justified crossroads is possible without inventing a competing Atlas, but travel inconvenience does not silently authorize changing the venue.

GOTW, playoffs and championships default to neutral venues, subject to access, neutrality and event eligibility. Rare/championship candidates are not generic weekly shortcuts. A playoff itinerary must branch around unknown qualification and opponents rather than predicting them as fact.

## 2. Evidence quality matters before routing

The currently inspected world-state file is explicitly **end of Week 3, 2026**. It is not a verified Week 6 character-location ledger. The Week 7 provider-normalized receipt contains Week 6 and Week 7 matchups, standings and transactions; it does not supply a full future-season itinerary.

A Week 6 fixture establishes a likely encounter context, **not proof that the character remained there, returned home, or departed at a particular hour**. Reconcile the final approved Week 6 scene, epilogue and any subsequent movement before committing a Week 7 origin. Do not promote an old draft, proposed deed transfer or bridge event into canon. El Niño is an environmental influence here, not a speaking road traveler needing a human itinerary.

The travel graph’s `min_hours` are conservative narrative **lower bounds**, not measured travel durations. Summing them tests obvious impossibility; it does not establish departure time, arrival, rest, weather delay, transport capability or an overnight camp. A six-hour edge does not mean a six-hour finished journey.

## 3. Actual Week 7 cases to challenge

The figures below are calculated from the current approved graph. They are **editorial feasibility calculations, not executed production validation or established character travel**.

### A. HMB at Red — GOTW: do not presume a return to the Keep

Week 6 placed HMB’s matchup at Mud; Red’s was at Red. If the approved last scene leaves HMB near Mud, the connected path to Red is:

**Mud → Mire → Chamber → Lake Bridge → Red**, lower-bound sum **25 hours**.

If an actual intervening scene establishes HMB at the Keep, **Keep → Obi → Lake Bridge → Red** sums **30 hours**. Using that second path by default invents a home reset.

This Week 7 matchup is GOTW, so neutral staging is already the governing default. The **Compact Grounds** are a registered neutral candidate reachable from Mud via Mire and Chamber, sum **8 hours**, and from Red via Lake Bridge and Chamber, sum **19 hours**. This is a concrete alternative for the creative room to test—not a venue selection or guarantee of fairness.

**Reconstruction questions:** What draws both parties there independently? What did Week 6 cost HMB physically or emotionally? Does Red travel by choice, summons, bargain or necessity? Does the location serve the rivalry rather than merely reduce miles? What onward commitments would make this meeting a plausible stop? Do not write those future commitments until their fixtures or story evidence are verified.

### B. Chins at Obi — separate closure from road access

Week 6 put Chins’ matchup at Chili and Obi’s at Slob. Obi’s possible return **Slob → Lake Bridge → Obi** sums **9 hours**, but a return still requires support.

From Chili to Obi, the graph’s shortest connected route sums **28 hours** through Commons, Pittsy, Speedway, Mire, Chamber and Lake Bridge. **Only if Pittsy is explicitly excluded** does the shortest alternative become **37 hours**, via Shared March, Temple, Mud, Mire, Chamber and Lake Bridge. The prior 43-hour route via Commons/Jackson is connected but is not the shortest alternative.

Pittsy’s business closure is **not proof its public route is impassable**. Resolve the conflicting location/access evidence before imposing a detour or building the plot on it.

**Reconstruction questions:** Where did Chins actually finish the prior story? Is there a supported reason Obi is still traveling? Could a registered home-domain approach, ridge or overlooked waypoint stage the encounter? If neutral territory genuinely improves both motivations and onward continuity, use the existing Tier 1 override process. Do not invent a new mountain pass to repair an avoidable assumption.

### C. LLC at Slob — distinguish a branch from a fact

From the prior Week 6 Temple context, **Temple → Mud → Mire → Chamber → Lake Bridge → Slob** sums **22 hours**. From LLC’s Boardroom, **Boardroom → Storm City → Chamber → Lake Bridge → Slob** sums **16 hours**, but that alternative requires evidence of an intervening return.

The useful creative choice is not “22 versus 16.” It is what LLC carried away from the Temple, why the journey matters, and whether the proposed encounter respects Slob’s host domain or has a justified override. A transit camp may explain the route without becoming LLC’s permanent home.

## 4. Recommended rolling itinerary record

Add an **editorial, nonpromoting itinerary overlay** beside existing World/Memo/Novel packets, rather than replacing those systems. One row per character per story beat should include:

`character | evidence/time cutoff | last supported scene/location | origin confidence | intention | departure window | route edges and minimum bound | mode/access constraints | rest/camp/weather assumptions | proposed venue/parent domain | venue rule/override status | arrival window | next verified obligation | future branches | unresolved contradiction | approval state`

Use three horizons:

1. **Established past:** approved scenes and verified results; contradictions remain explicit.
2. **Near-term proposed movement:** Week 7 alternatives, not locked until evidence and story review agree.
3. **Future planning:** verified fixtures where available; otherwise unknown opponents/locations and conditional playoff branches. Do not fabricate a schedule to make a route tidy.

Compare candidate venues by both travelers’ total burden, the larger individual burden, physical access, seasonal conditions, motive, host significance and onward continuity. A geometric halfway point is not automatically accessible or narratively neutral. Plan through the season when source fixtures are supplied, while leaving outcome-dependent branches open.

## 5. New-site contract: reuse before expanding geography

First test registered locations and existing parent feature handles. Examples already supported include Obi’s **high ridge / war-room overlook**, Mud’s **channels / raised ground**, and Jackson’s clubhouse, grounds and water features. Their parent supplies zone, climate, culture, routes and current state.

If a genuinely new site is needed, use the existing candidate registry and schema. Required fields include candidate ID, working name, lifecycle status, class, likely physical zones, event eligibility, activation trigger, story functions, technology translation and source provenance. Add related active locations and prerequisites where applicable.

Keep travel-specific editorial details in the separate itinerary proposal, not unsupported schema fields: parent connection, ingress/egress, plausible travel bounds, capacity, neutrality risks, autumn treatment, future reuse, and the story problem it solves. **Candidate means candidate.** It must not appear as active geography or receive invented route edges until the existing approval/promotion process admits it.

## 6. Practical reuse and remaining gaps

Reuse the Atlas and travel graph; venue resolver and Tier 1 exception; Location Control Plane; Memo/Novel adapters; candidate registry; and existing chronology/knowledge/continuity gates.

The inspected Location Control Plane compiler establishes registered-location and **primary-homeland connectivity** and carries event fields. That alone does not prove last-scene chronology, actual travel time, rest, future scheduling or a season-long route. Its semantic-QA-ready status is not permission to lock or publish a scene. This is a bounded observation about the inspected compiler, not a claim that no other repository safeguard exists.

**Before Tuesday production:** resolve last supported whereabouts, distinguish hypothetical paths from actual movement, verify future fixtures as available, compare all six encounter pitches against these checks, and return failed pitches to the author/production simulation for reconstruction. Keep Sunday action and Monday-night outcomes open; regional autumn should shape scenes without inventing snow or forcing Week 8 Halloween intensity into Week 7.

**Unverified / not performed:** visual map inspection, complete future schedule, exact departure/rest clocks, final Week 6 scene-to-location reconciliation, route-access resolution at Pittsy, live runtime execution, GitHub changes, canon promotion or publishing. No blocker requires the user to choose a creative venue; the simulated creative room can recommend constrained alternatives while evidence gaps remain visible.

## Canonical sources

Source snapshot: `jakekaloper-hub/schemin-26`, main commit `e999e44d5fcea301036a8e1176dd462690dcd981`.

- [Atlas taxonomy and domain rules](https://github.com/jakekaloper-hub/schemin-26/blob/e999e44d5fcea301036a8e1176dd462690dcd981/world/atlas/ATLAS_V1.md)
- [Route and travel model](https://github.com/jakekaloper-hub/schemin-26/blob/e999e44d5fcea301036a8e1176dd462690dcd981/world/atlas/ROUTE_AND_TRAVEL_MODEL_V1.md)
- [Travel graph](https://github.com/jakekaloper-hub/schemin-26/blob/e999e44d5fcea301036a8e1176dd462690dcd981/living-novel/os/geography/world_travel_graph_v1.json)
- [Venue resolver](https://github.com/jakekaloper-hub/schemin-26/blob/e999e44d5fcea301036a8e1176dd462690dcd981/world/encounters/ENCOUNTER_VENUE_RESOLVER_V1.md)
- [Special-event tiers, including story-neutral local sites](https://github.com/jakekaloper-hub/schemin-26/blob/e999e44d5fcea301036a8e1176dd462690dcd981/world/atlas/phase-1/SPECIAL_EVENT_VENUE_SYSTEM_V1.md)
- [Current world state](https://github.com/jakekaloper-hub/schemin-26/blob/e999e44d5fcea301036a8e1176dd462690dcd981/world/data/current_world_state.json)
- [Week 7 normalized evidence](https://github.com/jakekaloper-hub/schemin-26/blob/e999e44d5fcea301036a8e1176dd462690dcd981/memo-os/week-7/WEEK_7_PROVIDER_NORMALIZED_EVIDENCE_2026-10-24.json)
- [Location compiler](https://github.com/jakekaloper-hub/schemin-26/blob/e999e44d5fcea301036a8e1176dd462690dcd981/world/location-control-plane/compiler/location_control_plane.py)
- [Candidate schema](https://github.com/jakekaloper-hub/schemin-26/blob/e999e44d5fcea301036a8e1176dd462690dcd981/schemas/atlas-location-candidate.schema.json)
