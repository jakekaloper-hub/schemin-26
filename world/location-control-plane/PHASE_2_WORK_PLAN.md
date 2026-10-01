# SCHEMIN '26 UNIVERSE ATLAS — PHASE 2 WORK PLAN

**Date:** 2026-09-30
**Status:** ACTIVE PRODUCTION GATE
**Phase:** Homeland, Settlement & Location Card Production
**Authority:** World Engine V1.1 + Atlas Phase 1 + Commissioner Phase 2 authorization

## Mission

Turn existing Schemin geography into renderer/prose-addressable production infrastructure.

Phase 2 does not expand the active map. It compiles existing authority into:
- 12 Homeland Cards;
- 23 Active Location Cards;
- parent/sub-location handles;
- reference-availability records;
- generation-ready World Packets;
- Memo OS and Novel OS adapters;
- executable QA.

## Prime doctrine

> Atlas cards join authority; they do not own authority.

Source ownership remains:
- League Data Platform -> verified league facts;
- Character Canon -> principal character identity/body;
- World Engine -> physical geography, routes, divisions, owner-domain placement;
- World State -> persistent damage/weather/history;
- Memo OS -> weekly illustrated treatment;
- Novel OS -> literary manifestation and POV constraints;
- Location Control Plane -> deterministic compilation only.

## Non-goals

Phase 2 will not:
- activate any of the 48 Phase 1 CAND-* concepts;
- create new LOC-* records;
- invent political borders;
- resolve unsupported proper names;
- fabricate approved environment images;
- silently reconcile upstream Character/Novel/World disagreements;
- replace the Character Control Plane;
- render final artwork.

## Production gates

### Gate A — Authority & schema
Deliver:
- authority/consumer interpretation matrix;
- Location Control Plane architecture;
- schemas for Homeland Card, Location Card and World Packet.

### Gate B — Homeland Cards
Produce 12 machine-readable cards from owner_domains + active world/character authority.

### Gate C — Location Cards
Produce 23 machine-readable cards from locations + zones + routes + world-state + historical events.

### Gate D — Sublocation/reference plane
Create:
- deterministic sub-location handles from existing persistent landmarks;
- location visual-reference registry;
- explicit MISSING/HUMAN_REVIEW_REQUIRED behavior.

### Gate E — Compiler/adapters
Implement:
- resolve_location;
- resolve_homeland;
- compile_world_packet;
- relationship classification;
- Memo adapter;
- Novel adapter.

### Gate F — QA and release
Run:
- structural validation;
- source-coverage validation;
- candidate firewall;
- championship firewall;
- scenario regression matrix;
- repository CI;
- Umpire/Closer release review.

## Hard release criteria

- 12/12 Homeland Cards resolve.
- 23/23 active locations resolve.
- 0 Phase 1 candidate sites promoted.
- 0 unknown LOC IDs accepted.
- 0 missing zone/route references.
- 0 silent current-state resets.
- 0 character-body claims authored by Location Control Plane.
- visual reference status is explicit for every active location.
- unresolved load-bearing fields return HUMAN_REVIEW_REQUIRED.
- championship-only candidate remains inaccessible to active-location resolver.
- Memo and Novel packets both consume the same location ID while applying different consumer constraints.

## Build/test cadence

For each gate:

BUILD
→ STATIC QA
→ DEFECT LEDGER
→ FIX
→ POLISH
→ RETEST
→ NEXT GATE

## Exit condition

Phase 2 passes only when an upstream production system can request a known location ID and receive a deterministic packet that answers:
1. where the scene is;
2. what physical rules apply;
3. how participants arrive;
4. what history/state persists;
5. what visual facts are locked;
6. what is unknown;
7. what the generator is forbidden to invent.

**Phase 2 objective:** make geography callable.
