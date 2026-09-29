# Week 4 Flaim League-State Receipt V1

**Authority:** League Data Platform / Librarian  
**Evidence class:** PROVIDER OBSERVATION  
**Provider adapter:** Flaim → ESPN  
**Captured at:** 2026-09-29T17:58:54.693Z  
**League:** Pro Schemin' Football League — ESPN 1417621  
**Season / matchup period:** 2026 / Week 4  
**Status:** VALIDATED PROVIDER RECEIPT — NOT PERPETUALLY LIVE

## Provenance

Machine receipt:
`../../data/provider-receipts/flaim/1417621/2026/week-4/2026-09-29T175654Z.json`

Validator:
`../../data-gateway/flaim_adapter.py`

This capture was acquired through the authorized Flaim connector and normalized from its ESPN provider reads.

## League contract observed

- 12 teams
- H2H points
- 2 keepers
- current matchup period: Week 4
- six Week 4 matchups
- all 12 current rosters returned
- recent transaction window returned 47 rows

## Standings observation

| Rank* | Team | Record | PF | PA |
|---:|---|---:|---:|---:|
| 1 | D0nkey K0ng | 3-0 | 480.96 | 357.69 |
| 2 | Red Leopards | 2-1 | 471.20 | 368.12 |
| 3 | Seven Deadly Chins | 1-2 | 406.74 | 409.20 |
| 4 | The Chili Cheesers | 2-1 | 431.09 | 440.07 |
| 5 | Mud Dogs | 2-1 | 383.06 | 416.25 |
| 6 | ObiWan Jacoby | 2-1 | 401.34 | 376.60 |
| 7 | Slob on my Dobb | 1-2 | 471.74 | 424.11 |
| 8 | Dr. Duckhook | 1-2 | 396.45 | 472.93 |
| 9 | The LLC | 1-2 | 395.32 | 448.00 |
| 10 | El Niño | 1-2 | 390.10 | 436.51 |
| 11 | Three Dreaded Snake | 1-2 | 385.93 | 446.93 |
| 12 | His Majesty's Blood | 1-2 | 380.78 | 398.30 |

*Rank is Flaim's current ESPN standings sort field. It is not a postseason finish.

## Week 4 matchup/projection observation

All scores were 0–0 / winner UNDECIDED at capture.

| Home | ESPN projection | Away | ESPN projection | Projection edge at capture |
|---|---:|---|---:|---|
| D0nkey K0ng | 130.74 | ObiWan Jacoby | 160.87 | ObiWan Jacoby +30.13 |
| Mud Dogs | 140.20 | Three Dreaded Snake | 130.07 | Mud Dogs +10.13 |
| Red Leopards | 142.73 | Dr. Duckhook | 142.49 | Red Leopards +0.24 |
| Slob on my Dobb | 160.78 | The Chili Cheesers | 157.93 | Slob on my Dobb +2.85 |
| The LLC | 133.32 | His Majesty's Blood | 133.57 | His Majesty's Blood +0.26 |
| El Niño | 138.42 | Seven Deadly Chins | 147.29 | Seven Deadly Chins +8.86 |

These projections are **provider observations at capture time**, not predictions authored by Schemin and not a final GOTW decision.

## Current roster coverage

| Team ID | Team | Players returned |
|---:|---|---:|
| 1 | ObiWan Jacoby | 17 |
| 2 | Red Leopards | 19 |
| 3 | Slob on my Dobb | 18 |
| 4 | The LLC | 19 |
| 5 | D0nkey K0ng | 18 |
| 6 | Three Dreaded Snake | 19 |
| 7 | The Chili Cheesers | 17 |
| 8 | His Majesty's Blood | 18 |
| 9 | El Niño | 17 |
| 10 | Mud Dogs | 17 |
| 11 | Seven Deadly Chins | 18 |
| 12 | Dr. Duckhook | 19 |

Roster presence proves fantasy-roster membership at capture time. IR/bench/starting slots do **not** independently prove current medical status.

## Transaction observation

Flaim source: `mTransactions2`

Returned rows: **47**

Observed counts:
- completed add rows: 12
- completed waiver rows: 12
- failed waiver rows: 10
- trade rows: 2
- trade-proposal rows: 3

Provider limitation:
`structured_details_incomplete=true`

Therefore:
- waiver/add/drop evidence may be used with row-level provenance;
- FAAB bids may be used when present;
- trade existence may be observed;
- exact trade assets may **not** be called provider-verified when `trade_sides` is missing;
- Week 3 Commissioner-supplied trade terms remain separately classified until reconciled.

## Week 4 Fact Scope impact

| Fact class | State after Flaim capture |
|---|---|
| current team names | PROVIDER OBSERVATION — refreshed |
| current standings | PROVIDER OBSERVATION — refreshed |
| current Week 4 schedule/status | PROVIDER OBSERVATION — refreshed |
| current roster membership | PROVIDER OBSERVATION — refreshed for all 12 |
| Week 4 ESPN projections | PROVIDER OBSERVATION — refreshed |
| recent adds/waivers/FAAB | PROVIDER OBSERVATION — refreshed |
| exact trade assets | PARTIAL / UNRESOLVED where directional detail is absent |
| player medical/injury availability | OPEN — roster slot is insufficient |
| GOTW designation | OPEN — editorial decision remains gated |

## Freshness

Consumers must recompute age from `2026-09-29T17:58:54.693Z`.

Do not describe this receipt as live after its applicable freshness SLO expires.

## Librarian verdict

**PASS as provider evidence.**

**NOT sufficient by itself to close Week 4 Fact Lock.**
