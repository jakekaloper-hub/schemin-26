# SETTLEMENT & INSTITUTION HIERARCHY V1

**Status:** PHASE 2 PRODUCTION MODEL
**Purpose:** Give every scene a scale address without inventing new political borders.

## Scale hierarchy

WORLD
→ PHYSICAL ZONE
→ REGIONAL NETWORK
→ SETTLEMENT / DOMAIN
→ ACTIVE LOCATION (LOC-*)
→ DERIVED FEATURE HANDLE (SUB::*)
→ SCENE

## Rules

### Physical zone
Causal geography: terrain, climate, movement.

### Regional network
Road/watershed/coastal relationships already represented by routes and zone adjacency.
Phase 2 does not assign new sovereign borders.

### Settlement / domain
May be:
- owner domain;
- city district;
- neutral institutional cluster;
- shared corridor;
- market/estate network.

A domain is a relationship to place, not proof of sovereignty.

### Active location
The canonical addressable unit in world/data/locations.json.

### Derived feature handle
A landmark or internal feature inherited from the parent LOC record.
It is not an independent location and cannot move independently.

## Institution classes

Existing and future locations may be classified functionally as:
- OWNER_DOMAIN
- LEAGUE_INSTITUTION
- COMMERCIAL
- HOSPITALITY
- SPORT_RECREATION
- TRANSIT
- INDUSTRIAL
- MEDICAL
- EDUCATIONAL
- MEMORIAL_FUNERARY
- CIVIC
- SHARED_CORRIDOR
- NEUTRAL_ENCOUNTER

This classification is descriptive only until present in active machine records.

## Anti-isolation test

A location packet should answer:
- which physical zone contains it;
- which routes reach it;
- which domain/institution relationship applies;
- which ordinary world systems surround it;
- whether it is home, shared, away or neutral for the participant.

If the scene can only explain the place through a fantasy-team joke, it fails the Stranger Test.
