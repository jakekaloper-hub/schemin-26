# Week 3 — Final Event Delta Checklist V1
**Purpose:** answer “What changed?” before asking “Who won?”

## Trigger
Run after the final NFL action affecting Week 3 appears complete, then continue until ESPN/Flaim provider state and standings are authoritative/stable enough for Fact Lock.

## League-wide pass — all 12 teams
For each team compare against the latest preserved Week 3 evidence snapshot:
1. score and projection delta;
2. lineup slot / started-state delta;
3. new player points or scoring correction;
4. injury / inactive / availability event;
5. keeper involvement and keeper cost/control where verified;
6. bench consequence materially altered by final scoring;
7. new add/drop/waiver/failed bid/trade lifecycle row;
8. transaction-to-start/result relationship where directly supported;
9. provider winner/result state;
10. record / PF / PA / standings rollover;
11. long-arc continuity-out requirement;
12. new world/character continuity implication.

## Monday-sensitive targeted checks
- Mud Dogs — Saquon Barkley.
- Red Leopards — DeVonta Smith.
- Seven Deadly Chins — D'Andre Swift.
- El Niño — Jalen Hurts and Eagles D/ST.
Also rescan all rosters for less-prominent Monday players and late lineup changes rather than assuming the targeted list is exhaustive.

## External verification trigger
If the final-day scan reveals a new injury/availability event that is materially relevant, verify with official team/NFL or high-quality current reporting before promoting it beyond LEAGUE observation.

## Causal firewall
A score delta does not establish the play that caused it, the exact chronology, managerial intent, or why a team won. Preserve numerical and provider facts separately from interpretation.

## Fact-Lock readiness
FACT_LOCK may begin only after:
FINAL FLAIM/ESPN CAPTURE → PLAYER/LINEUP VERIFICATION → FINAL 12-TEAM EVENT DELTA PASS → PROVIDER RESULT VERIFICATION → POST-WEEK STANDINGS VERIFICATION.

If any authoritative field remains unresolved, mark the dependency and keep downstream result-dependent production blocked.
