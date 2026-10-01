# FUTURE LOCATION UNLOCK FRAMEWORK V1

**Status:** PHASE 1 GOVERNING WORKFLOW
**Purpose:** Allow ten remaining memo cycles, playoffs, championship and future seasons to reveal new geography without turning every generated background into permanent canon.

## 1. Two-store law

Schemin uses two distinct layers:

### Active World Store
Authoritative live locations under world/data/locations.json.

Only promoted sites receive a canonical LOC-* record.

### Candidate Store
Creative/provisional proposals under world/data/atlas_location_candidates.json.

Candidate entries:
- may be researched;
- may be assigned a likely physical zone;
- may be held for a future matchup;
- may be used in preproduction;
- are **not** active geography.

A candidate never becomes canon merely because it appears in a brainstorming document.

## 2. Candidate lifecycle statuses

### APPROVED_ACTIVE_CANON
The concept has been promoted into the active World Engine location store. Candidate entry becomes a pointer/provenance record only.

### PROVISIONAL_CANON
A site exists in controlled story-world evidence but still has unresolved placement/function details.

### FUTURE_UNLOCK_CANDIDATE
A designed site with plausible world placement and story utility, reserved for a future event or reveal.

### RARE_NEUTRAL_CANDIDATE
A non-owner venue intentionally available for unusual GOTWs, rivalry escalations, special wagers, playoffs or one-off spectacle.

### HISTORICAL_ONLY
A site/image exists as released history but is not available as a normal current venue.

### AMBIENT_REGIONAL_FLAVOR
A recurring category or background feature, not a uniquely mapped site.

### REJECTED_FOR_DRIFT
The concept conflicts with world physics, technology, character canon or the anti-gimmick law.

### HOLD_FOR_LATER_EVIDENCE
Potentially useful, but missing a prerequisite such as technology, route, ontology or institutional justification.

## 3. Location classes

- OWNER_HOME
- OWNER_SUBLOCATION
- RECURRING_INSTITUTION
- COMMERCIAL_LEISURE
- ORDINARY_NEUTRAL
- RARE_NEUTRAL
- GOTW_NEUTRAL
- PLAYOFF_NEUTRAL
- CHAMPIONSHIP_ONLY
- HISTORIC_LANDMARK
- BATTLE_SCAR_REMNANT
- TEMPORARY_EVENT_SITE
- TRANSIT_NODE
- MEDICAL_RECOVERY
- EDUCATION_COLLEGIATE
- SPORT_RECREATION
- INDUSTRIAL
- FUNERARY_MEMORIAL
- FESTIVAL_FAIRGROUND

Classes describe function; they do not override canon status.

## 4. Unlock paths

### Path A — Existing-location reuse
Use when the story naturally fits a current LOC-* site.
No new geography is created.

### Path B — Sub-location reveal
A memo may reveal a clubhouse room, road, dock, grove, market lane or training yard within an existing location/domain.

Requirements:
- parent LOC-*;
- inherited physical zone;
- inherited route access unless a new internal path is necessary;
- no contradictory terrain.

A sub-location becomes separately mapped only if reuse value justifies it.

### Path C — Candidate activation
Use a pre-registered candidate when the weekly story creates a reason for it to appear.

Requirements:
- candidate status permits activation;
- event class permits the site;
- likely zone/route are coherent;
- character/location packet is available;
- Umpire finds no conflict.

### Path D — New site proposal
When a real weekly event needs a place not already modeled:
1. Scout verifies event facts.
2. Beat Writer states the story function.
3. Architect checks existing locations for reuse.
4. Only if reuse fails may a new candidate be created.
5. Candidate receives class/status/zone hypothesis/provenance.
6. It can be used provisionally in preproduction.
7. Publication does not automatically make every background detail canon.

## 5. Promotion ladder

### Level 0 — Idea
No ID. Brainstorm only.

### Level 1 — Registered candidate
Receives CAND-* ID and lifecycle status.

### Level 2 — Production-cleared candidate
Has:
- compatible zone;
- event-class fit;
- technology fit;
- route hypothesis;
- anti-drift constraints;
- no duplicate active site.

### Level 3 — Published site evidence
A released memo/novel scene establishes some combination of:
- site existence;
- visual grammar;
- event memory;
- landmark.

This still does not establish every generated detail.

### Level 4 — Provisional active location
Receives LOC-* in world/data/locations.json after:
- placement is resolved;
- route access exists;
- reuse value is demonstrated;
- provenance is attached.

### Level 5 — Permanent recurring canon
Requires durable value across time. Typical evidence:
- repeated use;
- institutional importance;
- owner-home necessity;
- major historic event;
- explicit Commissioner lock.

## 6. Historical landmark conversion

An event site becomes a historical landmark when at least one is true:
- the event changed persistent world state;
- the site becomes shorthand for a known rivalry/event;
- a scar/remnant physically persists;
- later characters deliberately revisit or reference it;
- Commissioner explicitly preserves it.

Examples already eligible for landmark treatment:
- Bridge at the Mountain Lake;
- Mire Hill Battlefield;
- Country Club of Jackson contamination/humiliation memory;
- Alpine Wager Route;
- Arsenal Barbershop;
- Southern Speedway;
- LLC Storm City.

Historical memory is separate from venue availability. A battlefield may remain a landmark without becoming a routine matchup site.

## 7. Scar/remnant law

Possible persistence states:
- ACTIVE_DAMAGE
- CONTAMINATED
- REPAIRED_WITH_SCAR
- RESTORED
- MEMORIALIZED
- ABANDONED
- REBUILT
- TEMPORARY_EFFECT_RESOLVED

A future pristine scene must not ignore an active durable consequence.

## 8. Future-week workflow

For every weekly matchup:

1. verify home/away and event class;
2. resolve default venue;
3. check current world state;
4. ask whether existing venue supports the story;
5. if not, search candidate registry;
6. if candidate fits, activate provisionally;
7. if none fits, propose new candidate;
8. generate using world packet;
9. after publication, Scout + Librarian classify what became evidence;
10. Architect writes only accepted deltas into active world state.

## 9. Surprise-preservation law

Do not preassign all remaining 2026 matchups to locations.

The Atlas should create **capacity**, not predetermine the season.

Reserve enough rare sites that future upsets, injuries, wagers, rivalries, trades and humiliations can reveal believable new corners of the world.

## 10. Championship reservation

A CHAMPIONSHIP_ONLY candidate may be designed before the championship but must obey:
- no participant-specific decoration until finalists are known;
- no winner iconography before result;
- no championship scene before the actual championship event;
- no use for ordinary regular-season encounters;
- location may be institutionally known but visually “unlocked” only by the championship.

Current Phase 1 preferred reservation:
**CAND-CHAMP-LAST-FIELD — The Last Field**

It remains a candidate until the championship gate.

## 11. Retirement / supersession

Candidates can be retired without rewriting history.

Active locations may be superseded only when:
- canon changed explicitly;
- location was destroyed/closed/moved through story-world events;
- duplicate records are reconciled.

Never delete provenance merely to clean the map.

**Core rule:** the map grows through governed memory, not generative accumulation.
