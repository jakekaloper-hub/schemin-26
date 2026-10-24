# Week 4 Fact Scope & Evidence Register V1

**Status:** OPEN / PRE-FACT  
**Authority:** Memo OS Fact Desk + League Data Platform  
**Purpose:** define what is already locked, what must refresh, and what may not be inferred.

## Locked carry-in facts

Source: Week 3 Fact Lock.
- entering records/PF/PA are historical Week 3 close state;
- six Week 4 matchups are verified;
- divisions remain Burgers / Wings / Pizza as locked in Week 3;
- Week 3 outcomes may be referenced as history, not as Week 4 prediction.

## Current-week facts requiring refresh before Story Room

Current Flaim provider receipt: `WEEK_4_FLAIM_LEAGUE_STATE_RECEIPT_V1.md` captured 2026-09-29T17:58:54.693Z.

| Fact | Current state | Evidence |
|---|---|---|
| current roster membership | **REFRESHED / PROVIDER OBSERVATION** | all 12 current rosters returned through Flaim/ESPN |
| player availability/injury status | **OPEN / PROVIDER OBSERVATIONS AVAILABLE** | fresh DK roster statuses observed through Flaim/ESPN; these are not independent medical verification |
| completed trades and exact assets | **PARTIAL / UNRESOLVED** | transaction existence observed, but Flaim reports structured details incomplete and some trade rows lack directional assets |
| waiver/FAAB results | **REFRESHED / PROVIDER OBSERVATION** | 47-row transaction window includes completed/failed waivers and row-level FAAB bids |
| current Week 4 projections | **REFRESHED / PROVIDER OBSERVATION** | all six ESPN matchup projections captured |
| team names / rename check | **REFRESHED / PROVIDER OBSERVATION** | current 12-team provider map captured |
| provider matchup status | **REFRESHED / PROVIDER OBSERVATION** | Week 4, six matchups, all UNDECIDED at capture |
| keeper/resource consequences | **PARTIAL** | current keeper values/IDs available; material changes still require interpretation against prior state |

Each field must carry:
- source;
- fetched/captured time;
- freshness or temporal scope;
- confidence/status;
- discrepancy note when sources disagree.

## Unresolved carryover

Week 3 Fact Lock recorded a Sept. 28 Red Leopards/TDS trade with Commissioner-supplied asset terms while provider structured detail was incomplete. Do not upgrade every asset to independently provider-verified until roster/transaction reconciliation proves it.

## Forbidden pre-Fact claims

Until current refresh:
- no Week 4 injury certainty;
- no lineup certainty;
- no final projection-based winner framing;
- no "live" wording from cached state;
- no GOTW final designation;
- no Week 4 result/consequence prose;
- no assumption that a Week 3 roster is unchanged.

## Fact classification

Use:
- VERIFIED FACT
- COMMISSIONER-SUPPLIED FACT
- PROVIDER OBSERVATION
- EDITORIAL DERIVATION
- UNRESOLVED
- HISTORICAL FACT

Never promote repetition or narrative usefulness into evidence strength.


## Flaim integration note

Flaim is now a governed provider adapter under the Schemin Data Gateway. The machine receipt is validated by `data-gateway/flaim_adapter.py`.

This refresh does **not** convert cached evidence into perpetual live state. Recompute freshness from the receipt timestamp.

Story Lock remains blocked on unresolved medical/injury evidence where story-relevant, exact trade-asset reconciliation where needed, and incomplete current-week story evidence. W4-G5 continuity/world entry is already PASS; W4-G6 personalized intelligence is LIVE / PARTIAL PASS.


## 2026-10-01 W4-G6 personalization refresh

Fresh Flaim/ESPN observations used for the DK/HMB planning update:

### D0nkey K0ng — team 5
Current roster status observations:
- Breece Hall — Doubtful
- Dallas Goedert — Doubtful
- Terrance Ferguson — Doubtful
- Tyjae Spears — Questionable
- Alec Pierce — IR
- Tank Dell — IR
- Isiah Pacheco — IR

These are provider roster-status observations only. They support an editorial "battle-worn roster" frame but do not establish medical diagnosis, final Week 4 availability or lineup certainty.

Additional current resource observation:
- DK added Skyy Moore on 2026-09-30 through a completed Week 4 ESPN transaction.

### His Majesty's Blood — team 8
- verified Week 4 opponent: The LLC (team 4);
- current matchup state at refresh: 0.00–0.00 / UNDECIDED;
- HMB added Sam Darnold for $15 FAAB on 2026-09-30.

Commissioner-supplied beach activity and conditional cookie-face storytelling remain outside provider fact and are classified in the W4-G6 personalized-intelligence amendment.

### Freshness boundary
These observations are a 2026-10-01 current-provider read for this planning update. They do not become perpetual live state; later Story Lock must refresh any status that materially affects publication.


## 2026-10-02 live Week 4 synchronization

Fresh Flaim/ESPN provider observation captured during the cross-OS synchronization mission at approximately 2026-10-02T17:22Z.

### Live matchup state

All six provider winner flags remain `UNDECIDED`.

Current scoring-period observations:
- D0nkey K0ng 17.5 — ObiWan Jacoby 0.0
- Mud Dogs 0.0 — Three Dreaded Snake 0.0
- Red Leopards 0.0 — Dr. Duckhook 0.0
- Slob on my Dobb 21.8 — The Chili Cheesers 7.1
- The LLC 0.0 — His Majesty's Blood 12.9
- El Niño 0.0 — Seven Deadly Chins 17.3

These values supersede the 2026-10-01 pre-kickoff 0.00–0.00 snapshot for **current live planning only**. They are not final results.

Current standings remain the Week 3-close records because Week 4 has not completed.

### Current Week 4 transaction window

The provider returned 29 Week 4 transaction rows from `mTransactions2`; `structured_details_incomplete=true` remains in force.

Material observations for Story Room intake include:
- Dr. Duckhook — Ollie Gordon II $71 FAAB; Jaylen Wright $8; Bills D/ST $3.
- Slob on my Dobb — Mack Hollins $11; Browns D/ST $11.
- His Majesty's Blood — Sam Darnold $15.
- Three Dreaded Snake — 49ers D/ST $3 plus later completed additions.
- D0nkey K0ng — Skyy Moore added.
- Red Leopards — Raheim Sanders added.
- Seven Deadly Chins — multiple completed kicker changes.

Trade lifecycle rows exist, but exact directional assets remain unresolved wherever provider structured detail is incomplete.

### Cross-OS handoff

Current reconciliation:
- `WEEK_4_STORY_ROOM_CURRENT_STATE_RECONCILIATION_2026-10-02.md`
- `../../living-novel/weekly-ledger/2026_WEEK_04_LIVE_EVIDENCE_AND_SIGNIFICANCE.md`
- `../../world/atlas/integration/WEEK_4_CROSS_OS_LIVE_SYNC_RECEIPT_2026-10-02.md`

Persistent World/Atlas state is **not** advanced by this live evidence. Story Lock, final venues, issue architecture, finished art and publication remain blocked.
