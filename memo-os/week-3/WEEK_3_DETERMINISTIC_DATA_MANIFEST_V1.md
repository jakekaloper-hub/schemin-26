# Week 3 Deterministic Data Manifest V1
**Rule:** generated art is never system-of-record typography. Final data pages execute ART_BACKGROUND → DETERMINISTIC_TEXT_COMPOSITE → FACT_QA.

## Core fields
|Field|State before Fact Lock|Resolution|
|---|---|---|
|`{{W3_M01..M06_HOME_TEAM}}` / `AWAY_TEAM`|AVAILABLE|verified schedule/team IDs|
|`{{W3_M01..M06_HOME_SCORE}}` / `AWAY_SCORE`|PRE-FACT|final Flaim/ESPN|
|`{{W3_M01..M06_WINNER}}`|BLOCKED|derive only after final provider status|
|`{{W3_M01..M06_MARGIN}}`|DERIVED/BLOCKED|`abs(home_score-away_score)`|
|`{{POST_W3_RECORD_TEAM_01..12}}`|BLOCKED|pre-W3 record + authoritative W3 result|
|`{{POST_W3_PF_TEAM_01..12}}` / `PA`|BLOCKED|authoritative standings/final scoring|
|`{{W3_HIGH_SCORE_TEAM}}` / `VALUE`|DERIVED/BLOCKED|max of 12 final team scores|
|`{{W3_LOW_SCORE_TEAM}}` / `VALUE`|DERIVED/BLOCKED|min of 12 final team scores|
|`{{W3_CLOSEST_MARGIN}}`|DERIVED/BLOCKED|min of six final margins|
|`{{W3_LARGEST_MARGIN}}`|DERIVED/BLOCKED|max of six final margins|
|`{{W4_M01..M06_HOME_TEAM}}` / `AWAY_TEAM`|AVAILABLE|verified Week 4 schedule bridge|
|`{{W4_TEAM_RECORDS}}`|BLOCKED|post-W3 standings|
|`{{W4_GOTW}}`|EDITORIAL/BLOCKED|only after Week 3 consequences|
|`{{WAIVER_AMOUNT_*}}`|AVAILABLE where verified|transaction evidence register|
|`{{PLAYER_W3_POINTS_*}}`|PRE-FACT until completion|final player detail|

## Arithmetic evidence
Every derived field stores its source inputs and formula in QA evidence. Never infer closest/highest/largest visually from a designed page.

## Typography
Exact names, scores, records, bids, standings, schedules, margins and rankings must be compositor-controlled. Raster generation may reserve space but may not be trusted to spell/render these facts.
