# ENCOUNTER VENUE RESOLVER V1

**Status:** COMMISSIONER-LOCKED / WORLD ENGINE V1.1  
**Purpose:** Make matchup geography deterministic enough that the map governs the story.

## 1. Required inputs

Every Encounter must resolve:
- verified matchup;
- verified home team / away team when provider exposes home/away;
- division membership;
- event class;
- home-domain location;
- entering world state;
- available route from away origin;
- approved neutral pool when applicable.

If home/away evidence is unavailable, the resolver returns **VENUE_UNRESOLVED** rather than inventing a host.

## 2. Regular-season rule

### REGULAR / DIVISIONAL
Default venue = **home team's environment**.

The Story Room may choose a fresh sub-location inside the home domain, but it must inherit:
- physical zone;
- division relationship;
- owner-domain material culture;
- local inhabitants;
- climate;
- routes;
- existing state.

Example:
A home matchup for a Wings owner is staged in that owner's established home environment on the Wings League layer, not in a generic “Wings kingdom.”

## 3. Major-matchup rule

### GAME_OF_THE_WEEK
Default = approved neutral site.

### PLAYOFF
Default = approved neutral site.

### CHAMPIONSHIP
Default = approved neutral site.

A home-domain override requires explicit Commissioner/Story Room approval and a recorded reason. “Looks cooler” is not sufficient.

Neutral does not mean placeless. The neutral site must exist somewhere in the Schemin physical world, have access routes, climate and state, and be entered in the Location Register.

## 4. Neutral-site pool

Initial approved/provisional neutral network:
- LOC-LEAGUE-CHAMBER — institutional neutral venue.
- LOC-COMPACT-NEUTRAL-GROUNDS — open neutral Encounter grounds in the Central Basin.
- LOC-BRIDGE-MOUNTAIN-LAKE — may serve as neutral only when story significance warrants and state permits.
- other sites may be admitted through normal Location Register governance.

The championship may receive a distinct neutral venue later, but it cannot be improvised in final art.

## 5. Home environment registry

2026 default anchors:
- ObiWan Jacoby → LOC-TRADE-JEDI-MOUNTAIN-BASE
- D0nkey K0ng → LOC-DK-HIGHLAND-STRONGHOLD
- Three Dreaded Snake → LOC-TDS-WATERFALL-TEMPLE
- Mud Dogs → LOC-MUD-DOGS-SWAMP
- Red Leopards → LOC-RED-RUINS
- Slob on my Dobb → LOC-SLOB-FOOTHILL-CAMP
- Chili Cheesers → LOC-CHILI-STABLE
- Dr. Duckhook → LOC-COUNTRY-CLUB-JACKSON
- The LLC → LOC-LLC-BOARDROOM
- His Majesty's Blood → LOC-BELT-KEEPER-KEEP
- El Niño → LOC-STORM-BOWL / approved atmospheric manifestation zone
- Seven Deadly Chins → LOC-CHINS-ROAD-COMMONS

## 6. Route requirement

The away side must have an approved route or route chain to the venue. The manuscript need not narrate the journey, but the graph must support it.

If no path exists:
**BLOCK PRODUCTION → CARTOGRAPHY RESOLUTION REQUIRED.**

## 7. State requirement

The venue inherits prior state before the Encounter.

A burned hall is still burned.
A flooded road may still be closed.
A contaminated Country Club requires cleanup/restoration before pristine reuse.
A major neutral ground retains scars unless a restoration event exists.

## 8. Venue-selection hierarchy

1. Verified League matchup/home-away truth.
2. Major-event neutral-site rule.
3. Owner home-domain registry.
4. World Atlas / travel graph.
5. Current World State.
6. Story Room sub-location choice.
7. Visual composition.

Visual generation is last and has no venue-selection authority.
