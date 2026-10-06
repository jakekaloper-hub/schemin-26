# Week 4 Pre-Art QA Lock Receipt

**Status:** PRE-ART QA PASS / FLAIM FINALITY ONLY CONTENT HOLD
**Publication:** memo.2026.week-04
**Issue:** 27 pages
**Authority:** Commissioner + Bullpen domain Directors

## Ruling

Everything that can be locked and QA'd **before image generation** is now treated as frozen:

- 27-page order and page count;
- story beats and matchup genres;
- page-specific visual direction;
- character IDs, identity requirements, expected reference hashes and rejection states;
- Week 4 character overrides;
- entering world state and geography constraints;
- page-to-page continuity;
- written-material purpose and text hierarchy;
- deterministic fact slots;
- forbidden bridge pages;
- pre-render rejection conditions;
- mobile/page composition intent;
- manual `generate page N` dispatch behavior.

The **only content input still open** is the authoritative Flaim/ESPN result refresh and the deterministic values derived from it.

Those final values may populate:
- final scores/winners/margins;
- final records/standings;
- final player-level causal facts already called for by the locked story;
- Power Rankings values;
- State of the Realm values;
- Pittsy's Book settlement;
- World State Delta durable-consequence selections.

They may **not** reopen or redesign any page.

## Two-stage QA model

### Stage A — PRE-ART QA

Must PASS before any page is generated.

Checks:
1. correct page packet retrieved;
2. correct Character_ID(s);
3. correct expected SHA-256 reference authority;
4. page-specific character override applied;
5. world/venue rules resolved;
6. story beat matches Mission Review lock;
7. composition/visual job defined;
8. written-material job defined;
9. deterministic data slots identified;
10. rejection conditions present;
11. previous/next-page continuity understood;
12. no forbidden bridge-page logic;
13. finality-dependent fields either populated from Fact Lock or explicitly blank.

**Week 4 Stage A verdict: PASS**, subject only to final data population after G1.

### Stage B — POST-GENERATION RASTER QA

Runs on each generated PNG before Jake saves/locks it.

Checks:
1. actual character anatomy/identity matches authority;
2. no stale/reference contamination;
3. correct props/objects;
4. correct world/environment;
5. correct scene beat;
6. no forbidden objects;
7. no critical text hallucination;
8. mobile readability;
9. page-to-page visual continuity;
10. no composition drift.

If any check fails:
**PAGE_RASTER_FAIL / REGENERATE BEFORE PAGE_LOCK**.

If all checks pass:
**PAGE_LOCKED_PNG**.

## Jake's operating workflow

After Flaim Fact Lock:

1. Jake says: `generate page 1`.
2. Bullpen resolves Page 1 from the official packet.
3. Stage A pre-art preflight is re-read, not redesigned.
4. Page is generated.
5. Stage B raster QA runs immediately.
6. If FAIL: repair/regenerate automatically.
7. If PASS: return the final PNG and mark Page 1 `PAGE_LOCKED_PNG`.
8. Jake saves the PNG locally.
9. Jake says: `generate page 2`.
10. Repeat through Page 27.

Jake does not paste prompts. Jake does not restate canon.

## Final assembly workflow

After all 27 PNGs are `PAGE_LOCKED_PNG`:

1. Jake uploads or supplies the 27 final PNGs.
2. Groundskeeper verifies 1–27 completeness/order.
3. Publication Design normalizes page dimensions for one consistent mobile/iPhone reading aspect.
4. No art is regenerated during assembly.
5. Umpire performs full-issue audit on the exact ordered set.
6. Compile a single PDF.
7. Validate page order, crop, readability, metadata and file integrity.
8. Closer freezes exact PDF + SHA-256.

## Prohibited behavior

- no creative rewrite after Fact Lock;
- no page-count changes;
- no re-opening Story Room;
- no generic character substitution;
- no skipping raster QA because the prompt was correct;
- no PDF assembly until every expected PNG is present and individually locked.
