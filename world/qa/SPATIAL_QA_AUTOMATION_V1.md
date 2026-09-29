# SPATIAL QA AUTOMATION V1

**Status:** IMPLEMENTED — PURE-STDLIB FIRST PASS

The World Engine now has executable validation for:
- physical adjacency symmetry;
- division team coverage;
- Wings = chicken-wings semantic lock;
- division→zone references;
- location→zone/division references;
- abstract-position containment within assigned physical-zone bounds;
- route endpoint integrity;
- location route references;
- 12/12 owner-domain coverage;
- owner→primary-location consistency;
- current character hard locks relevant to world/domain integration;
- state-event provenance and location integrity;
- current-world-state location integrity.

## Geometry policy

V1 deliberately avoids Earth latitude/longitude and exact mileage.

The validator uses `schemin-local-v1` abstract bounds to catch impossible placement and broken references. Turf/GeoJSON remains a future implementation option once more exact geometry is useful.

## Adversarial fixtures

The suite injects known-bad mutations for:
- generic bird-wing substitution;
- duplicate/missing division membership;
- impossible location placement;
- broken route endpoint;
- missing state location;
- removed Wilson Look negative lock;
- removed Phillip Pitts three-head lock.

Expected behavior: every known-bad fixture fails.

**PHASE 9 GATE:** controlled by CI result.
