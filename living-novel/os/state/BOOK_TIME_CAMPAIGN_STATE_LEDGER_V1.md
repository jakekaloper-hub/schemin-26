# BOOK-TIME CAMPAIGN STATE LEDGER V1
**Status:** CONTROL PLANE / RETROFIT
**Book-time snapshots:** PRESEASON -> POST_W1 -> POST_W2 -> W3_OPENING

## Causal classification
Every transition MUST be one of FACTUAL_SEQUENCE, SUPPORTED_CAUSATION, INTERPRETATION, UNKNOWN.
Sequence alone never establishes causation.

## HMB regression spine
| Snapshot | State | Legal knowledge | Visibility |
|---|---|---|---|
| PRESEASON | Belt Keeper; JSN R2; Achane R15; no live R1 | keeper/draft evidence | ON_PAGE |
| POST_W1 | 0-1 after loss to ObiWan; Belt retained; keeper core remains campaign capital | preseason + certified W1 only | OFF_PAGE_ACTIVE / selective prose |
| POST_W2 | 0-2 after loss to El Niño; Belt retained; keeper core remains campaign capital; failed claims are separate resource evidence | through certified W2 only | OFF_PAGE_ACTIVE / selective prose |
| W3_OPENING | inherit POST_W2 state; W3 events remain gated until verified | no unresolved W3 outcome may be canonized | RESERVED |

## Twelve-owner persistence rule
For each owner maintain prior_state, verified_event, causal_classification, consequence, response, new_state, became_true_at, knowable_at, eligible_book_time, prose_visibility, unresolved_consequences, provenance, resolution_status.

A weekly delta of NO_MATERIAL_CHANGE is valid and does not erase prior state.

## Temporal firewall
W3 facts cannot mutate PRESEASON, W1, or W2 snapshots. Later significance may recall earlier lawful facts; it may not create retroactive omen or knowledge.

## Narrative restraint
State may be ON_PAGE, OFF_PAGE_ACTIVE, RESERVED_FOR_PAYOFF, RESOLVED, or SUPERSEDED. OFF_PAGE_ACTIVE is a first-class state, not missing data.
