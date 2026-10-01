# WEEKLY WORLD EVOLUTION CONTRACT V1

## Machine enforcement

Every request is validated against `world/evolution/schemas/world-evolution-request.schema.json` before semantic validation. Schema failure is FATAL and no mutation is allowed.

## Required request envelope

- schema_version
- transaction_id
- week
- season
- source_release
- release_verified
- operations[]
- approvals

## Approvals

For state/history APPLY:
- umpire = true
- closer = true

For candidate promotion request:
- umpire = true
- closer = true
- commissioner = true

No tool may infer approvals from context.

## Operation types

### APPEND_WORLD_STATE_EVENT
Adds an evidence-backed event to the historical state-event ledger.

### SET_LOCATION_STATE
Replaces the explicit additional current-state list for an existing LOC.

### REGISTER_CANDIDATE_EVIDENCE
Records verified released evidence in `CANDIDATE_EVIDENCE_LEDGER.json` after Umpire + Closer approval.
It does not change lifecycle status or activate geography.

### REQUEST_CANDIDATE_PROMOTION
Creates a promotion plan only.
The Phase 5 engine does not silently insert LOC records.

### REGISTER_NEW_CANDIDATE
May create a candidate proposal in a transaction plan.
It cannot use APPROVED_ACTIVE_CANON.

## Dry-run law

DRY RUN is the default mode.

Dry-run output must contain:
- validation findings;
- proposed state events;
- proposed current-state changes;
- candidate evidence;
- candidate promotion plans;
- dependent rebuild targets;
- mutation_allowed.

## Apply law

Apply mode may write governed Class A state/history files and the non-promoting candidate-evidence ledger. State/history apply then executes deterministic derivative rebuild fanout (Location Cards → structural plates → Interactive Atlas).

Candidate promotion stays a separately reviewed location transaction because it affects:
- locations;
- routes;
- atlas topology;
- location cards;
- structural references;
- venue resolver behavior.

## Idempotency

transaction_id must be unique.
event IDs must be unique.
Reapplying a recorded transaction must fail closed.

## Failure rule

Any FATAL finding:
- mutation_allowed = false
- no state file writes
- no candidate promotion
- HUMAN_REVIEW_REQUIRED


## Promotion semantic enforcement

Promotion planning also enforces candidate lifecycle status, rejection reason, event eligibility, technology state, declared prerequisites, route resolution, collision checks and championship locks. A rejected/held/ineligible candidate cannot be reported ready merely because approvals are present.
