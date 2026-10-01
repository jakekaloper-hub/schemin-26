# WEEKLY MEMO OS — LOCATION CONTROL PLANE INTEGRATION PATCH V1

**Status:** BINDING WHEN ATLAS PHASE 2 IS ACTIVE
**Does not replace:** Weekly Memo OS V5.5

## Purpose

Make V5.5's world-before-image requirement deterministic.

## Preproduction sequence

VERIFIED HOME/AWAY
→ EVENT CLASS
→ VENUE RESOLVER
→ LOCATION CONTROL PLANE
→ MEMO LOCATION PACKET
→ CHARACTER RENDER CONTRACT
→ STORY ROOM
→ PAGE BRIEF
→ GENERATION

## Required call

For every location-bearing page, preproduction must resolve an active LOC-* or separately approved candidate workflow before image prompting.

Memo adapter:
world/location-control-plane/adapters/memo_adapter.py

## Hard rules

- CAND-* cannot enter active venue resolution implicitly.
- unresolved LOC/SUB handles block.
- current world state must hydrate.
- character visual authority remains separate.
- missing approved location image bytes do not prevent semantic art direction, but a workflow requiring exact environment image grounding must block.
- generated scenery cannot write back to canon automatically.

## Week-to-week writeback

After release:
Scout → Librarian → Architect classify any new site evidence.
Only accepted deltas reach active World Engine/state stores.

**Memo integration doctrine:** the page brief receives a world packet; it does not invent one.
