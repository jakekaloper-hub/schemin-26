# 2023 Chronicle Opening — Source & Editorial QA Receipt
**Mission:** Issues #214/#215 / R53 #211 · PR #243 (DRAFT) · **NOT CANON / NOT RELEASE-CLEARED**

## Actual output and provenance
- Prologue: [The Cloth Nobody Owned](../PROLOGUE.md), approximately **1,222** word-regex tokens in the authored markdown.
- Week 1: [Six Knots](W01.md), approximately **3,602** word-regex tokens in the authored markdown, six individually written scene passages plus connecting aftermath. The figures include frontmatter and headings and do not represent a professional copyedited word count.
- Archival primary evidence: `living-novel/production/full-rewrite-2026/evidence/G01_2023_FULL_WEEKLY_MATCHUPS.json`, blob `ded119cde5c660f87f197f269b8d6ddd2a11316a`, labeled Flaim ESPN league 1417621. Historical raw ESPN SHA absent; owner identity unverified. The narrative does not turn a recorded `home` flag into a physical venue.

| 2023 W1 | Certified winner (archival slot) | Loser (archival slot) | Winning score | Losing score |
| --- | --- | --- | ---: | ---: |
| I | Benedict Arnold (8) | Two Dreaded Snake (6) | 130.94 | 79.68 |
| II | The KING of the Octagon Village (3) | Benedict Kenobi (1) | 190.74 | 113.02 |
| III | Benedict Coomhersnatch (5) | Arm Chair GM (11) | 144.28 | 119.34 |
| IV | Red Leopards (2) | The LLC (4) | 149.76 | 121.06 |
| V | El Niño (9) | The Blew Waffle's (7) | 178.70 | 86.86 |
| VI | Mixon it up for a week (10) | Eggs Benedict (12) | 129.24 | 96.19 |

## Observed technical validation
- Added `living-novel/historical-chronicle/qa/test_2023_opening_week.py` and a named Novel OS CI step plus path trigger.
- **Seven tests passed** as shown in job log of [Novel OS CI #40830388504](https://github.com/jakekaloper-hub/schemin-26/actions/runs/40830388504), at tested source commit `d4a12d81288bc1c42b52199dcbf5e7364429761c`. Checks: source blob, six twelve-slot pairing, score/home-away/winner/margin transcription, four protected manuscript hashes, word/section thresholds, POV language guard, chronicle/saga separation.
- At that same tested commit, [Cross-Domain Authority CI #40830388527](https://github.com/jakekaloper-hub/schemin-26/actions/runs/40830388527), [Bullpen Runtime CI #40830388453](https://github.com/jakekaloper-hub/schemin-26/actions/runs/40830388453), and [Repository Merge Gate #40830388528](https://github.com/jakekaloper-hub/schemin-26/actions/runs/40830388528) completed successfully.
- Authenticated main/PR-branch file readback found matching blob hashes for the protected Prologue and Chapters I–III, not touched in this production pass. A green technical check **does not** establish literary merit, owner lineage, historical Atlas legality or Umpire acceptance.

## Adversarial editorial questions — unresolved, not a simulated review
1. Do six encounters centered on one invented public awning create too much single-location compression of a league-wide Week 1, even though the scenes represent reactions to six separate certified results rather than claiming actual shared physical venues?
2. Are the bench/cord/tally themes insufficiently differentiated from the archival-bureaucracy motifs of the 2018–2023 causal chapters? Does the Week 1 manuscript need additional independent social stakes, risk, relationship and irreversible cost?
3. Does proposed historical Jake's use of `CHAR-JAKE-KALOPER` meet the year-specific temporal and owner-source requirements? Current evidence says **NO AUTHENTICATED 2023 HUMAN OWNER BINDING**; keep candidate in draft.
4. Does the prospective fictional awning/market environment conflict with the existing 2023 Gallery/Night Registry development material or approved world geography? **NOT CLEARED**.
5. Would a more grounded environment with canon-approved location IDs produce stronger prose without projecting contemporary territories into 2023?
6. Was the archival 2023 Two Dreaded Snake banner inadvertently conflated with later TDS morphology? The text explicitly avoids this, pending independent source review.

## Disposition
**Technical source/negative-guard checks: PASS on tested SHA. Literary/character/Atlas/Umpire/founder gates: HOLD.** No review submissions, owner attestations, canon promotion, merge, publication or ESPN refresh are claimed.

**Next eligible prose task:** Write six distinct 2023 Week 2 Chronicle entries grounded in the same archive; shift the story's dramatic center beyond repeated repair/tally images, and continue the causal novel separately without overwriting the existing `The Fourth Address` V1.
