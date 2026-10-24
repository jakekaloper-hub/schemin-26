# Week 4 Director Ownership Declarations

**Status:** PRE-PUBLICATION HARDENING / NO ART GENERATION

Each gate has exactly one named owner. Counterweights independently challenge the owner.

| Gate | Owner | Counterweight | Controlling authority | Current status |
|---|---|---|---|---|
| G1 Result Lock | Scout | Umpire | fresh Flaim/ESPN finality | HOLD_EXTERNAL / CONTROL PASS |
| G2 Pitty's Book | Pitty desk | Scout | current ticket ledger + prior official baseline | HOLD_EXTERNAL / CONTROL PASS |
| G3 Power Rankings | Power Rankings desk | Scout + Beat Writer | Fact Lock + prior published ranking baseline | WAITING_ON_FACT_LOCK / CONTROL PASS |
| G4 State of Realm | Scout | Beat Writer + World / Atlas | final records/standings + current story authority | WAITING_ON_FACT_LOCK / CONTROL PASS |
| G5 Matchup Story Authority | Beat Writer | Librarian | WEEK_04_STORY_AUTHORITY_REGISTER.json | WAITING_ON_FACT_LOCK / CONTROL PASS |
| G6 World State Delta | Librarian | World / Atlas Director | current G5 story + final consequence | WAITING_ON_FACT_LOCK / CONTROL PASS |
| G7 Page Packets | Groundskeeper | Architect | current story-authority receipt/hash + Fact/World/Character inputs | WAITING_ON_STORY_LOCK / CONTROL PASS |
| G8 Art Production | Visual Direction Lead | CAIO + Librarian | current G7 packet + exact refs + Umpire + Closer | BLOCKED / CONTROL PASS |
| G9 Publication Design | Publication Design | Scout | deterministic factual layers | WAITING_ON_RENDER / CONTROL PASS |
| G10 Author Council | Author Council | Beat Writer | current story register + current packets | WAITING_ON_CURRENT_PACKETS / CONTROL PASS |
| G11 Umpire | Umpire | INDEPENDENT | assembled issue vs current story register | WAITING_ON_ASSEMBLY / CONTROL PASS |
| G12 Release | Closer | Umpire + Groundskeeper evidence pack | G1-G11 evidence receipts | BLOCKED / CONTROL PASS |

## Required declarations

- **Scout:** stale or UNDECIDED provider state cannot self-promote to finality.
- **Pitty desk:** incomplete tickets or arithmetic mismatch cannot settle.
- **Power Rankings desk:** stale records/prior ranks fail; TDS FROM #12 stays separate from weekly movement.
- **Beat Writer:** each matchup must resolve from current story authority, not older planning.
- **Librarian:** superseded branches cannot seed production.
- **World / Atlas:** no venue/transition/world mutation is invented for visual convenience.
- **Character / CAIO:** current Character ID/hash/reference route must survive final raster QA.
- **Visual Direction:** cinematic quality cannot substitute for current story fidelity.
- **Groundskeeper:** no packet is READY without current story-authority receipt/hash.
- **Architect:** stale-hash and bypass prevention is executable, not advisory.
- **Publication Design:** image generation never owns critical factual text.
- **Author Council:** stale jokes, redundant pages, generic spectacle and page inflation must be challenged.
- **Umpire:** schema PASS is insufficient; semantic/current-authority mismatch is blocking.
- **Closer:** no PASS_TO_PRODUCTION until owner PASS + counterweight PASS + Umpire PASS + current evidence receipts.

## Current Closer ruling

PR #116 hardening has passed all required CI, merged, and survived authoritative post-merge readback.

`PRE_PUBLICATION_READINESS = APPROVED`
`STORY_AUTHORITY_HARDENING = PASS`
`DIRECTOR_CROSS_REFERENCE = PASS`
`UMPIRE_INTERNAL_HARDENING = PASS`
`ART_GENERATION = HOLD`

The remaining art hold is execution/external: Week 4 provider finality is still UNDECIDED and production-time render/reference proof remains required at Gate 8.
