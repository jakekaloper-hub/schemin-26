# ATLAS EXPANSION DATA MODEL ADDENDUM V1

**Status:** PHASE 1 ARCHITECTURE
**Purpose:** Add future-location capacity without creating a second active-world source of truth.

## 1. Existing authority remains unchanged

Active physical world:
- world/data/physical_zones.json
- world/data/locations.json
- world/data/routes.json
- world/data/divisions.json
- world/data/current_world_state.json
- world/data/world_state_events.json

The candidate registry is **not** part of active geography until promotion.

## 2. Candidate registry

New file:
world/data/atlas_location_candidates.json

Schema:
schemas/atlas-location-candidate.schema.json

A candidate record must include:
- id;
- working_name;
- lifecycle_status;
- location_class;
- likely_physical_zone_ids;
- event_eligibility;
- activation_trigger;
- story_functions;
- technology_translation;
- canon_notes;
- source_provenance.

Optional:
- division_affinity_ids;
- related_active_location_ids;
- inspiration;
- championship_only;
- rare_use;
- prerequisites;
- rejection_reason.

## 3. ID law

Candidate IDs:
CAND-[A-Z0-9-]+

Active locations:
LOC-[A-Z0-9-]+

A CAND ID never changes meaning in place.

When promoted:
- create new LOC ID;
- candidate gains promoted_location_id;
- candidate status becomes APPROVED_ACTIVE_CANON;
- retain candidate provenance.

## 4. Status separation

Candidate lifecycle status is separate from active location canon status.

Candidate lifecycle:
- APPROVED_ACTIVE_CANON
- PROVISIONAL_CANON
- FUTURE_UNLOCK_CANDIDATE
- RARE_NEUTRAL_CANDIDATE
- HISTORICAL_ONLY
- AMBIENT_REGIONAL_FLAVOR
- REJECTED_FOR_DRIFT
- HOLD_FOR_LATER_EVIDENCE

Active location canon:
- PERMANENT_CANON
- PROVISIONAL_CANON
- INTERPRETIVE_CANON
- TEMPORARY_SITE
- VISUAL_METAPHOR
- SUPERSEDED

Do not collapse these enums.

## 5. Promotion transaction

Promotion is an explicit write transaction:

CANDIDATE
→ evidence review
→ zone resolution
→ route resolution
→ duplication check
→ technology check
→ event-class check
→ LOC record
→ world-state initialization
→ candidate backlink
→ QA

No renderer or story writer may perform this mutation implicitly.

## 6. Site-trigger fields

Recommended candidate fields:

### event_eligibility
Examples:
- REGULAR
- DIVISIONAL
- GOTW
- PLAYOFF
- CHAMPIONSHIP
- WAGER_EVENT
- NOVEL_INTERLUDE
- NON_MATCHUP

### activation_trigger
Human-readable gate such as:
- "actual 2026 championship only"
- "Commissioner selects rare-neutral venue"
- "weekly story requires medical recovery scene"
- "published event creates recurring college-town setting"

### prerequisites
Examples:
- route path exists;
- no owner controls site;
- technology translation accepted;
- related active location state hydrated.

## 7. Duplication detection

Before creating a new candidate or location, compare:
- social function;
- physical zone;
- event class;
- owner relationship;
- visual identity;
- historical function.

If an active site can absorb the need as a sub-location, prefer reuse.

Example:
Do not create a second sportsbook merely because a page needs wagering. Pittsy's Book already owns the recurring League-bookmaking function.

## 8. Historic-state model

A location can accumulate:
- event memories;
- scars;
- contamination;
- repairs;
- memorials;
- closures;
- changed access;
- reputation.

These remain world-state records, not new location IDs unless physical identity actually changes.

## 9. Championship-only flag

A candidate with championship_only=true:
- cannot be selected by ordinary venue resolver;
- cannot appear in regular/GOTW/playoff eligible lists;
- may be visually preplanned but not published as the championship scene;
- activates only when the championship event exists and finalists are verified.

## 10. Rare-use flag

rare_use=true means:
- valid candidate;
- intentionally excluded from ordinary fallback;
- selection requires narrative/event justification.

This preserves surprise value.

## 11. Atlas-layer treatment

Candidate geography is an editorial/planning layer:
- hidden by default;
- never presented as final map truth;
- useful for board planning and future unlock capacity.

## 12. Technology compatibility

Each candidate must declare technology_translation.

Values may include:
- NATIVE_PREMODERN
- FUNCTIONAL_ANALOGUE
- REQUIRES_TECH_UNLOCK
- REJECTED_TECH_DRIFT

This allows the Commissioner to evolve the world's technology later without corrupting current canon.

## 13. Future evolution

If the Commissioner later raises the technology ceiling:
1. update World Design Principles through explicit governance;
2. reevaluate HOLD_FOR_LATER_EVIDENCE candidates;
3. do not retroactively pretend prohibited technology always existed unless history is explicitly revised;
4. preserve earlier functional analogues as historical/cultural forms where useful.

**Architect ruling:** candidates create optionality; active JSON creates reality.
