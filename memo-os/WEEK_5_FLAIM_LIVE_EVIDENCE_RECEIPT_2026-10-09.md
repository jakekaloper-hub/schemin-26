# Week 5 — Live FLAIM Evidence Reconciliation Receipt

**Evidence captured:** 2026-10-09 approximately 14:42 America/New_York  
**Source:** Authenticated FLAIM connector → ESPN, league 1417621, season 2026, matchup period 5.  
**Status:** VERIFIED PROVIDER READ / PROVISIONAL SCORING / NOT WEEK 5 FACT LOCK  
**Mission:** [Issue #146](https://github.com/jakekaloper-hub/schemin-26/issues/146)  
**Authority:** Existing Memo OS V5.5, Data Gateway, Character Canon, World Engine; this receipt is subordinate evidence, not an OS.

## League context

12 teams; head-to-head points; current matchup period 5. All six ESPN matchup winner values: `UNDECIDED`. Scores below are **pointsByScoringPeriod["5"]**, not locked final matchup totals.

## Six matchups (home first)

| Home | Home scoring-period points | Away | Away scoring-period points | Home projection | Away projection | Result |
|---|---:|---|---:|---:|---:|---|
| Dr. Duckhook | 4.90 | D0nkey K0ng | 20.64 | 146.455904 | 138.16984477 | UNDECIDED |
| The Chili Cheesers | 0 | El Niño | 29.00 | 148.02322975 | 142.31967815 | UNDECIDED |
| Red Leopards | 0 | ObiWan Jacoby | 0 | 141.87196139 | 130.03258386 | UNDECIDED |
| Slob on my Dobb | 2.90 | Seven Deadly Chins | 17.30 | 142.55858584 | 140.69247914 | UNDECIDED |
| Three Dreaded Snake | 15.40 | His Majesty's Blood | 0 | 131.07438914 | 124.59688362 | UNDECIDED |
| Mud Dogs | 0 | The LLC | 0 | 129.19498016 | 155.29834194 | UNDECIDED |

**Critical discrepancy:** ESPN's `totalPoints` field was 0 on *every* side while `pointsByScoringPeriod["5"]` had nonzero values on some sides. Do not treat totalPoints=0 as proof no player has scored; do not treat scoring-period values as finalized matchup totals. Require a refreshed provider read and, where needed, player-level detail before promoting.

## Entering records (after Week 4)

- 3–1: Red Leopards, ObiWan Jacoby, D0nkey K0ng.
- 2–2: El Niño, Slob on my Dobb, The Chili Cheesers, His Majesty's Blood, Three Dreaded Snake, Mud Dogs.
- 1–3: The LLC, Dr. Duckhook, Seven Deadly Chins.

ESPN standings order and playoffSeed are provider standings data, **not** a verified postseason clinch. ESPN returned `madePlayoffs=true` for every team during the regular season; suppress this field from editorial clinch/elimination assertions.

## Week 5 transaction evidence

FLAIM returned 18 structured ESPN `mTransactions2` rows, including failed/unknown claims. Relevant confirmed completed transactions:
- The LLC: Will Shipley RB, winning waiver bid 51, Isaiah Davis dropped.
- Seven Deadly Chins: Keon Coleman WR, winning waiver bid 62, Ryan Flournoy dropped; Dohnte Meyers WR, winning bid 32, Chris Bell dropped.
- The Chili Cheesers: Jacoby Brissett QB, winning bid 5, Jaxson Dart dropped.
- Dr. Duckhook: Jaguars D/ST, winning bid 5, Bills D/ST dropped; Antonio Williams WR added, George Holani dropped.
- Red Leopards: Bo Nix QB added, Patriots D/ST dropped.
- D0nkey K0ng: MarShawn Lloyd RB added.
- Mud Dogs: Matt Gay K added, Harrison Butker dropped.
- Slob on my Dobb: Will Reichard K added.
- His Majesty's Blood: Mike Gesicki TE added.

Failed claims: HMB Brissett bid 4, Dohnte Meyers bid 6, Will Shipley bid 19, Keon Coleman bid 8; Duckhook Will Shipley bid 11; LLC Joe Mixon bid 51. A TDS Dohnte Meyers waiver row was `unknown`, **not** a confirmed acquisition. Transaction list scope is Week 5 matchup period, not a guaranteed complete calendar-date range.

## Preproduction priorities and gates

1. **Scout / Data Gateway:** Refresh ESPN Week 5 scores and resolve scoring-field semantics; player-detail check; immutable provider capture with timestamp.
2. **Librarian:** Resolve owner→character→current team names and temporal canon; current approved source-byte mounts required for any character-bearing art.
3. **World authority / Beat Writer:** Resolve verified home venue, travel, and six encounter stakes. Propose narrative hypotheses, never invent factual outcomes.
4. **Groundskeeper / Visual Lead:** Populate existing Week 5 packet registers, not a new OS. Keep deterministic scores/text outside generative hallucination paths.
5. **Pitty's Book:** Pending bookmaker ledger/receipts; no invented lines, bets or results.
6. **Umpire:** Independent checks on provenance, no-false-green, six matchup completeness, Week 4 release continuity and visual gate. Do not promote this receipt to Fact Lock.

## QA performed on this receipt

- 6 unique matchups / 12 unique team IDs: PASS (manual reconciliation against FLAIM response).
- All provider winners undecided: PASS.
- Provisional vs final distinction: PASS.
- Successful vs failed/unknown transactions distinguished: PASS.
- Runtime scoring discrepancy resolved: **BLOCKED**.
- Independent Umpire runtime invocation: **NOT EXECUTED**.
- Character renderer source-byte binding: **NOT VERIFIED**.
- Week 5 final results / Memo release: **NOT AUTHORIZED**.

**Status classification:** IMPLEMENTED = evidence receipt; TESTED = structural/manual checks only; AUDITED = author review only, NOT independent; PROMOTED = NO; BLOCKED = final Fact Lock and art; REMAINING_EXTERNAL_INPUT_REQUIRED = later ESPN final scoring, Pittsy's Book receipts, approved renderer bindings, independent QA.
