# TEMPORAL POV STATE SCHEMA V1

Status: ACTIVE FOUNDATION CONTRACT

## State key
Every character-state record is uniquely resolved by:
CHARACTER_ID + BOOK_TIME + STATE_VERSION.

## Required fields
### Identity
- character_id
- identity_authority_version
- team_name_at_time
- visual_state_at_time
- provenance

### Evidence state
- record
- roster/resource state
- keeper/pick capital
- availability
- verified transactions
- relevant historical anchors

### Narrative state
- current_want
- immediate_pressure
- vulnerability
- unresolved_obligation
- active_story_promises

### Knowledge envelope
- known_facts
- unknown_facts
- public_information
- private_information_authorized_for_fiction
- beliefs
- interpretations
- forbidden_future_knowledge

### Relationships
Each edge is directional:
- other_character_id
- evidence_anchor
- current_posture
- unresolved_event
- leverage_or_dependency
- last_material_change

### World state
- location
- home_geography
- institutional ties
- material constraints
- story_objects

### POV contract
- eligibility: PRIMARY | SECONDARY | OBSERVED | OFF_PAGE_ACTIVE
- perceptual_priorities
- voice_constraints
- blind_spots
- permitted_inference
- forbidden_inference

### Causal transition
- triggering_event
- decision_or_response
- voluntary_cost
- involuntary_cost
- direct_consequence
- relationship_delta
- resource_delta
- belief_delta
- world_delta
- next_unresolved_pressure

## Truth labels
FACT
SUPPORTED_CAUSATION
COMMISSIONER_CONTEXT
POV_BELIEF
INTERPRETATION
STORY_POSSIBILITY
UNKNOWN

POV_BELIEF may contradict FACT in-character but cannot overwrite FACT in state.

## Hindsight firewall
At Book-Time T, a POV may consume only evidence with available_time <= T plus authorized prior beliefs. Future results, later injury diagnoses, later transactions and retrospective interpretations are inaccessible.

## Ensemble law
Every principal receives a state transition each weekly cycle, even if transition is NO_MATERIAL_CHANGE. Prose exposure is selective.

## Scene admission test
A proposed internal POV scene must answer YES to at least one:
1. internal knowledge changes the reader's understanding;
2. a consequential choice cannot be understood externally;
3. the POV creates meaningful dramatic irony;
4. a relationship changes differently from each side;
5. the character's perception of place/resource/history materially shapes action.

Otherwise use OBSERVED or OFF_PAGE_ACTIVE.

## Literary doctrine
Mythic depth comes from inherited state exerting present pressure.
Political depth comes from choices under finite resources and incomplete information.
Neither is achieved by archaic diction, imitation, lore volume or gratuitous POV multiplication.
