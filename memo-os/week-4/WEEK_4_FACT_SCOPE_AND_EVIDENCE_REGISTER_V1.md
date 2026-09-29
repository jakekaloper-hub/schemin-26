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
| player availability/injury status | **OPEN** | roster/IR placement is not medical verification |
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

Story Room remains blocked on unresolved medical/injury evidence, exact trade-asset reconciliation where needed, continuity/world entry, and personalized story intelligence.
