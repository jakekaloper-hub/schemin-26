# LOCATION CONTROL PLANE — AUTHORITY & CONSUMER INTERPRETATION MATRIX V1

**Status:** PHASE 2 BINDING CONTROL
**Purpose:** Prevent Location Cards from becoming a shadow canon or silently reconciling upstream differences.

## Authority order by field

| Field | Primary authority | Location Control Plane behavior |
|---|---|---|
| league result / matchup / home-away | Data Gateway / verified league evidence | consume only; never infer |
| character identity/body | Character Canon | reference character ID only; never redesign |
| owner-domain relationship | World Engine owner_domains | compile |
| physical zone | World Engine physical_zones | compile |
| division overlay | World Engine divisions | compile |
| active location identity | World Engine locations | compile |
| route | World Engine routes / travel graph | compile |
| current damage/state | current_world_state + world_state_events | hydrate |
| recurring landmarks | active location record | compile |
| horizon visibility | landmark_visibility | compile |
| weather propagation | weather_regions | compile |
| Memo treatment | Memo OS | consumer overlay only |
| Novel manifestation/POV | Author Room / Novel OS | consumer overlay only |
| approved character visual bytes | Character reference system | require separately |
| approved location visual bytes | Location reference registry | require separately |
| candidate geography | Atlas Phase 1 candidate store | blocked unless explicit candidate workflow |

## Consumer-specific differences

The same World Packet may receive consumer overlays.

### Weekly Memo OS
May:
- use visual metaphor;
- compress travel visually after route validation;
- emphasize matchup humor;
- stage a home-ground sub-location.

May not:
- move the location;
- erase current state;
- alter principal character canon;
- promote generated scenery.

### Novel OS
May:
- reveal ordinary life;
- explore local history already supported;
- use POV-specific knowledge envelopes;
- translate matchup facts into an Encounter form.

May not:
- treat Memo visual shorthand as literal world fact;
- invent unsupported history to complete a card;
- override current character/world authority.

### Visual Production
May:
- choose camera/lens/time-of-day;
- stylize approved environment grammar;
- select allowed sub-location handle.

May not:
- create a new permanent landmark;
- alter terrain/zone;
- ignore state damage;
- infer a location reference from text when approved bytes are required.

## Known interpretation seams

### El Niño
World Engine permits governed manifestation modes.
Living Novel currently constrains El Niño to natural/mobile storm treatment with no interior POV/dialogue.

Rule:
- base card stores World Engine authority;
- NOVEL consumer overlay applies the stricter Novel rule;
- Location Control Plane does not globally rewrite World Engine.

### Character visual evolution
Historic locations may preserve events tied to superseded visual identities.

Rule:
- location history persists;
- current Character Canon controls new depictions;
- Location Control Plane stores character IDs, not historical body reconstruction.

### Existing draft environment packets
Chronicles environment packets may be useful evidence/creative references.

Rule:
- DRAFT or unapproved packets are not APPROVED_VISUAL_REFERENCE;
- exact approved bytes must be resolvable before a packet can claim render-ready environment reference status.

## Unknown-field law

Unsupported fields use one of:
- UNKNOWN
- OPEN_TERRITORY
- NOT_APPLICABLE
- HUMAN_REVIEW_REQUIRED

The compiler must not substitute plausible invention for missing evidence.

## Failure policy

Return HUMAN_REVIEW_REQUIRED when:
- location ID is unknown;
- requested sub-location handle is unknown;
- required route cannot resolve;
- consumer asks candidate site through active-location resolver;
- required visual reference bytes are unavailable for a workflow that mandates them;
- upstream authorities materially conflict on a load-bearing field.

**Control doctrine:** ambiguity is surfaced, not beautified away.
