# ATLAS VISUAL HIERARCHY SPECIFICATION V1

**Status:** PHASE 2 PRODUCTION SPEC

## Purpose

Define map/detail zoom levels so production can reveal detail without confusing editorial candidates, active locations and scene-scale features.

## Levels

### L1 — WORLD
Seven physical zones and principal macroform.

### L2 — REGIONAL
Watersheds, ranges, coast, major route families and zone adjacency.

### L3 — CULTURAL
Burgers / Wings / Pizza nonexclusive overlays.

### L4 — CIVIL
Settlement networks, institutions, markets and shared corridors where established.

### L5 — OWNER DOMAIN
Twelve owner-domain relationships and primary home anchors.

### L6 — ACTIVE LOCATION
The 23 current LOC-* records.

### L7 — LOCAL FEATURE
SUB::* feature handles derived from persistent landmarks.
These are not new LOC records.

### L8 — HISTORICAL STATE
Scars, contamination, repairs, memorials and event-state overlays.

### L9 — EDITORIAL CANDIDATES
CAND-* future-unlock layer.
Hidden by default and never rendered as current canonical geography.

## Rendering law

A renderer may zoom in/out across levels 1–8 without mutating geography.

Level 9 is planning-only unless a candidate passes the Phase 1 promotion workflow.

## Labeling law

Reader-facing maps need not expose internal IDs.
Production/previs maps should retain IDs for deterministic joins.

## Scale-change law

Moving from L6 to L7 reveals detail.
It does not create a new settlement, road, biome or political boundary.

**Visual hierarchy doctrine:** zoom reveals; it does not invent.
