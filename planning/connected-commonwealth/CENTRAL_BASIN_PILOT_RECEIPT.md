# Mission #175 — Central Basin Cross-Format Pilot

**Status:** READ-ONLY PROTOTYPE / TESTED LOCALLY / UNPUBLISHED / NOT CANON-PROMOTED.
**Simulated review:** World/Atlas, Librarian, Beat Writer, Visual Direction, Architect and Umpire lenses only; no authenticated Director call or independent attestation.

## Actual source anchors
- `LOC-LEAGUE-CHAMBER` — PROVISIONAL_CANON; records desk and map wall; neutral institutional space.
- `LOC-LEAGUE-ARCHIVE` — INTERPRETIVE_CANON; record halls, ledger vaults, courier court.
- `LOC-PITTSYS-BOOK` — PROVISIONAL_CANON; ledger boards, settlement desk; recurring bookmaking function.

All are in `REG-CENTRAL-BASIN`. Their individual `source_provenance`, `canon_status`, and `open_questions` are retained in the generated packet. Neither provisional nor interpretive status is silently promoted.

## Route receipts
1. Archive → Chamber: `ROUTE-ARCHIVE-CHAMBER`, direct.
2. Chamber → Pittsy's Book: `ROUTE-BASIN-MARKET`, existing graph path Chamber → DK Mud Hill → Southern Speedway → Pittsy's Book. This is an Atlas path, **not** evidence of shortest real-world travel time, route distance, or an adjacent street.

## Memo scene demonstration (proposed text, not verified league event)
**Headline:** *A Tuesday in the Basin*
At the League Chamber, the records desk and map wall anchor the institutional setting. The Archive's record halls and courier court support an adjacent records-and-movement thread along the approved Archive–Chamber Processional. Pittsy's Book brings ledger boards and its settlement desk into the same broader Basin economy, connected by the existing Basin Market Road. Markets, transport and ordinary work continue beyond any weekly contest.

This is environment-focused editorial treatment only. It does not report a score, transaction, wager or new League event.

## Novel scene demonstration (proposed prose, not published manuscript)
The Basin had business even on days when the League had none to announce. Around the Chamber, records accumulated and travelers crossed the institutional approach; the Archive kept its halls and courier court in order. Farther along the recorded Market Road, Pittsy's Book had ledgers and a settlement desk of its own. No named passerby becomes a new character. This setting may be witnessed by an approved one-of-twelve owner POV in a later verified scene, but the present packet assigns no POV or new plot fact.

## Reusable machine output
`world/engine/central_basin_pilot.py:build_central_basin_pilot()` produces:
- `shared_world_facts`: all three existing anchors, source provenance, canonical graph route receipts, ordinary-life and economic context;
- `memo_packet`: contextual scene treatment;
- `novel_packet`: contextual scene treatment with twelve-owner-only POV rule;
- `atlas_view` and `environment_art_view`: same context ID; character rendering disabled.

The two packets reuse one `shared_world_facts` value; they do not maintain separate geographic truth.

## QA
`python3 world/qa/test_central_basin_pilot.py`: **5/5 PASS** — exact anchors, direct Archive route, indirect Book route, shared Memo/Novel facts, POV/character-art restrictions.

## Remaining
Malformed-source and seasonal-divisions fixtures, actual downstream production pipeline calls, independent acceptance, CI and release promotion. No principal character image, new LOC/ROUTE, canon mutation or published story.
