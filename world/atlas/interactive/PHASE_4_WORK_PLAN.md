# ATLAS PHASE 4 — CANONICAL INTERACTIVE WORLD ATLAS

**Status:** ACTIVE PRODUCTION GATE

## Mission
Turn the active World Engine into a deterministic, portable, interactive Atlas for production and reader-facing exploration.

## Canonical view
Shows:
- 7 physical zones;
- 23 active LOC-* sites;
- 18 active routes;
- Division filtering;
- current/historical world-state overlays;
- location detail panels;
- links to Phase 3 structural reference plates.

## Editorial view
May expose the 48 CAND-* concepts only as a catalog grouped by likely zone/status.
No candidate receives an invented point coordinate.
The championship-only candidate remains visibly editorial and cannot appear as an active map marker.

## Coordinate law
Abstract positions are topology/QA coordinates only.
The interactive Atlas must label itself non-metric and non-Earth.

## Deliverables
- deterministic standalone HTML Atlas;
- no external runtime dependencies;
- active layer controls;
- Division filter;
- world-state toggle;
- location detail panel;
- structural reference links;
- editorial candidate catalog;
- deterministic build test;
- CI integration;
- release receipt.

## Hard invariants
- active map = 23 locations;
- active routes = 18;
- zones = 7;
- candidate markers on canonical map = 0;
- candidate count = 48;
- The Last Field active marker = 0;
- renderer cannot mutate world data.
