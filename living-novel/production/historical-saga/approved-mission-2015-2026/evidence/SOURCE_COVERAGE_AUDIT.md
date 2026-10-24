# Source and coverage audit — historical saga

Baseline read: `8fcb77191955f413fe970154d47632770f923055`. This is a reproducible repository audit, not a new provider retrieval, authenticated Director review, canon acceptance, or claim that manuscripts are complete.

## Result

The eleven historical extracts contain **1,117 returned rows**. Deduplication by season, matchup period, participants and bracket tier produces **1,055 paired contests**, **38 unpaired source rows (one documented bye; 37 bye candidates)**, and **24 repeated display rows**. Unpaired rows retain their evidence status; a missing opponent is not invented. The 2021 Dewars White Label W15 bye is explicitly reported in `living-novel/history/HISTORICAL_PRESSURE_LEDGER.md`; the other 37 remain bye candidates. The 2022 G04 story-room specifically cautions that Red Leopards’ unpaired W15 row needs bracket documentation for its bye/placement interpretation. Repeated multiweek aggregates count once, with every source observation retained. No conflicting duplicate observations were found.

| Season | Returned rows | Regular paired | Postseason paired | Unpaired | Repeated display rows |
|---|---:|---:|---:|---:|---:|
| 2015 | 102 | 78 | 12 | 0 | 12 |
| 2016 | 102 | 78 | 12 | 0 | 12 |
| 2017 | 97 | 78 | 17 | 2 | 0 |
| 2018 | 97 | 78 | 17 | 2 | 0 |
| 2019 | 97 | 78 | 17 | 2 | 0 |
| 2020 | 97 | 78 | 17 | 2 | 0 |
| 2021 | 105 | 84 | 15 | 6 | 0 |
| 2022 | 105 | 84 | 15 | 6 | 0 |
| 2023 | 105 | 84 | 15 | 6 | 0 |
| 2024 | 105 | 84 | 15 | 6 | 0 |
| 2025 | 105 | 84 | 15 | 6 | 0 |

These are **observed-source denominators**, not a certification that no external fixtures are missing. The 2015/2016 regular seasons end at scoring week 13, with postseason aggregates displayed in weeks 14/15 and 16/17. The 2017–2020 regular seasons have thirteen observed weeks; 2021–2025 have fourteen. Bracket-tier counts in each JSON include consolation contests and retain actual source tier names. The source does not justify assigning today's bracket structure to any older year.

Each historical season JSON includes title outcome from `G01_2015_2025_FLAIM_VERIFIED_CHAMPIONSHIP_ROUNDS.json`, preserved as a historical team label/slot outcome. It does not license assigning that title to a current human owner. Provider transcriptions and local hashes are clearly distinguished from original provider bytes or provider payload checksums.

## Identity and writing boundary

`living-novel/history/OWNER_LINEAGE.md` and `living-novel/research/DATA_GAPS_AND_LIMITS.md` explicitly distinguish historical slots from real ownership. The G01 extracts do not supply verified owner history. Some 2017 rows lack numeric team IDs and contain encoding artifacts; their exact labels remain preserved rather than silently corrected. Name-only deduplication is restricted to the same season and period; it does not infer cross-year identity.

No general claim that historical events were personal experiences of today's twelve characters is licensed here. `R53/EVIDENCE_AND_ERA_REGISTER_V1.md` likewise keeps past slot attribution unresolved. Existing 2022/2024/2025 literary pilots are proposals, not identity proof. A current verified POV may encounter a historical record without claiming personal participation, subject to the actual scene knowledge envelope, canon, and event cutoff. Historical principal scenes requiring missing identity or era geography remain blocked locally; evidence indexing and unaffected contemporary scenes can continue.

## 2026 cutoff and gap

The current-season ledger contains **36 observed W1–W6 paired fixtures**, using:

- W1/W2: Novel weekly evidence ledgers (winner-first summaries; home/away unresolved from those sources).
- W3: `memo-os/week-3/WEEK_3_FINAL_EVIDENCE_SNAPSHOT_06.md` (explicit decided results).
- W4: `living-novel/production/week-04-05/WEEK_04_05_FLAIM_FACT_SNAPSHOT_2026-10-14.json` (all six decided, explicitly superseding earlier provisional observations), corroborated by `living-novel/production/chapter-04/PROVIDER_FINALITY_RECHECK_2026-10-14.md`.
- W5: final result banner lock dated October 13 (six explicit decided results).
- W6: `memo-os/week-6/WEEK_6_FLAIM_REVERIFICATION_AND_HANDOFF_CONVERGENCE_2026-10-20.md` (six explicit decided results; transcribed snapshot).

Thus **36 decided repository receipts** are represented. The initial audit selected an obsolete W4 provisional source; expanded source reconciliation found the October 14 decided readback and corrected the ledger, preserving the provisional path as superseded lineage. This is a material correction: ObiWan’s final W4 result is 157.33–139.67, not the early 151.33–83.57 observation. All six final W4 fields now come from the decided source, not inference from later standings. W6 is the latest final event cutoff found here, not a declaration of current live-provider state. The same October 20 receipt lists W7 fixtures as UNDECIDED. No future outcomes, playoffs, championship or completed-season epilogue are supplied for 2026.

## Existing prose is not unwritten

`EXISTING_TEXT_INVENTORY.json` records actual paths, file hashes, word counts including headers, and explicit status lines for historical season prose, R53 work, existing main manuscripts and rewrite candidates. Word count is inventory metadata only. Each historical fixture retains available existing manuscript candidates; no file is overwritten. For 2015, weekly draft presence is preserved without claiming every scene passes canon, POV, literary, or event-level review. The postseason file is merely a candidate location, not proof that all consolation fixtures are written. 2016's existing prologue, closing text and W1 draft remain discoverable. R53 pilots remain pilots.

`accepted_locations: []` means this audit has **not independently accepted event-level literary coverage**; it does not revoke existing hard canon or label the existing project unwritten. The whole-book authority matrix controls acceptance. Mapping accepted passages to events requires a separate literary/authority review, particularly where superseded narrator rules conflict with legacy prose.

## Missing, absent and pending

- **Present:** every extracted fixture observation and all listed source hashes, including duplicate display weeks.
- **Present but unpaired:** source rows without an opponent; retain their scores and UNDECIDED flag as bye candidates, not losses or played games.
- **Missing evidence:** historical owner binding, period geography/divisions, complete historical transaction records, independent full-schedule certification, and any newer 2026 provider events after the repository cutoff.
- **Not yet occurred/verified:** future 2026 results. Do not create missing-game rows for them.
- **Pending acceptance:** literary mapping, substantive manuscripts, reader integration and independent editorial review. This audit does not mark any of those PASS.

## Validation performed

Command: `python -m unittest discover -s living-novel/production/historical-saga/approved-mission-2015-2026/evidence -p 'test_coverage.py' -v`

Result: **8 tests passed**. Checks account for every observation, distinguish 2015's two-week final from two contests, exclude unpaired rows from played counts, retain repeated opponents in separate periods, require W4 finality provenance and preserve its superseded observation, distinguish the one documented bye from unresolved unpaired rows, and prevent manuscript presence from becoming literary acceptance.

Regenerate with `python living-novel/production/historical-saga/approved-mission-2015-2026/evidence/build_coverage.py`. The builder does not fetch sources, modify source manuscripts, run services, or promote canon.

## Independent review corrections

Event IDs prefixed `ESPN1417621` are mission-generated join keys, **not provider-assigned fixture IDs**. Stability is limited to the frozen ordered source. Source paths, hashes and JSON pointers carry provenance. Two rows (2017 P03 E018 and 2018 P15 E088) have equal displayed scores with source winner HOME. Their result qualification now flags this explicitly. Preserve that winner; do not claim a numerical winning margin, a draw, or an undocumented tiebreak. The eighth regression checks both cases.
