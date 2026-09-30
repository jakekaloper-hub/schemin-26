# Schemin '26 Member AI Gateway

**Status:** IMPLEMENTATION PHASE 1 / NOT CERTIFIED

This directory implements the first vertical slice of the Member AI Gateway Master Execution Contract V1.

## Authority boundary
- Schemin is the member-facing product.
- SCK remains the sole internal cross-domain control plane.
- This gateway is an access/service boundary, not a second Bullpen.
- External clients receive capabilities, never Director authority.
- Ordinary member capabilities are read-only with respect to canonical Schemin state.
- Private Mercer context is excluded unless a future explicitly authorized private-domain capability is added.

## Phase 1 scope
1. principal/client/scope model;
2. authorization-aware capability registry;
3. transport-independent response envelope;
4. semantic capability contracts for `capabilities.list`, `league.current_state`, `league.history`, `owner.identity`, `pittys_book.inputs`;
5. contract tests before provider/SCK wiring.

## Explicitly out of scope
Public signup, billing, generic multi-league SaaS, repository mutation APIs, Mercer sharing, automatic canon mutation, or exposing Bullpen Directors as tools.

## Evidence state
File existence is not certification. Phase 1 advances only through executable tests and independent QA.
