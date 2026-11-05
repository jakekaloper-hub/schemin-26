# Commonwealth Historical Chronicle — 2023 Week 9 archival and editorial HOLD

**Artifact:** [*The Ash Beneath the Road*](W09.md). **5,867 whitespace-delimited words**, including the source preface, all six large connected narrative scenes, opening, aftermath and closing note. **NONCANON / NOT MERGED / NOT PUBLISHED**. Historical Chronicle coverage candidate: **54 of 84** regular-season contests, Weeks 1–9. The independent editorial/Atlas/Umpire/canon holds remain in force; technical CI evidence is reported separately below, and no authenticated independent Director invocation is asserted.

## Exact source-to-scene concordance

Source: `living-novel/production/full-rewrite-2026/evidence/G01_2023_FULL_WEEKLY_MATCHUPS.json`, Git blob `ded119cde5c660f87f197f269b8d6ddd2a11316a`, `year=2023`, label `Flaim ESPN 1417621`. `weeks[week=9].matchups` contains six distinct contests, archive slots 1–12 appearing once each. Source carries no human owner IDs; raw ESPN provider SHA is unavailable.

| W9 scene | Archived home / score | Archived away / score | Winner (archive slot) | Margin |
|---|---|---|---|---|
| I / A Measure Too Small to See | The LLC (4), 136.16 | Two Dreaded Snake (6), 135.78 | The LLC (4) | 0.38 |
| II / The Room That Could Not Be Won | Arm Chair GM (11), 144.12 | Benedict Kenobi (1), 137.40 | Arm Chair GM (11) | 6.72 |
| III / A Song with No Hero | Red Leopards (2), 84.64 | The Blew Waffle's (7), 146.73 | The Blew Waffle's (7) | 62.09 |
| IV / Iron for a Different Use | Benedict Arnold (8), 72.10 | The KING of the Octagon Village (3), 139.12 | KING (3) | 67.02 |
| V / The Far Bank Answers | Mixon it up for a week (10), 127.52 | Benedict Coomhersnatch (5), 145.22 | Benedict Coomhersnatch (5) | 17.70 |
| VI / The Weight of an Unlit Window | El Niño (9), 152.88 | Eggs Benedict (12), 150.34 | El Niño (9) | 2.54 |

**Winner slot sequence:** 4, 11, 7, 3, 5, 9. Proposed user-attested Jake / archive slot 1: loses W9 and reaches **3–6** after 9; records are competitive facts, not evidence of bodily action or motivation in the proposed fictional city. Distinct Benedict banners do not establish real-world lineage. Historical El Niño is not treated as a person or a real meteorological event. Archive home/away is **not** a place on the fictional Atlas.

## Novel and world-boundary assertions

This installment is a **companion Chronicle**, not an automatic causal Book One chapter. Jake (`CHAR-JAKE-KALOPER`) is the **only proposed interior POV**; the prose does not authenticate that archive slot 1 is a real-person source join. Sena, Mara, the ferrywoman, courier, apothecary, singer, examiner, keeper and others act and speak but receive no independent principal internal narrative. No Edrin/Edin or Oren focalization; no personification of El Niño; no 2026 costumes, morphology, sports-owner psychology or future Week 10+ results imported.

All physical and social world elements are **fictional proposals requiring historical Atlas/Universe approval**: unnamed river, far bank, unsafe punt, upper road, foundry, coal warehouse, observatory ward, household light system, defective stove, examiner decisions, medicine inventory and lender/creditor relations. The Week 8 right-to-refuse clause remains provisional; there is **no ratified law or secure wage fund**. The punt remains grounded. One examined batch yields two cautiously usable medical packets and one condemned; no miraculous cure or fictional historical treatment claim. Far-bank objects and a witness message are **not** consent to a creditor charter or a crossing.

## Causal and craft handoff — self-assessment ONLY

The previous manuscript ended with an unlit bell, untreated financial obligations, promised examination of medicine, an unratified labor-right declaration and an unheard opposite shore. The new text shifts primary consequences into human work: an openly logged emergency coal transfer, an examiner's limited goods release, a kitchen accident that refutes a patron's triumphal commission, a makeshift hinge made by a cartwright rather than Jake, a child's verified-by-courier message from her mother, and voluntary light stations constrained by the people tending them. Jake's recurring failure is to mistake evidence or a single representative signal for adequate action. The narrow 0.38 contest and the 6.72 slot-one loss are not made to cause those events.

A **material weakness** remains: after eight earlier installments, the city still has recurring inventories, written documents, denied passage and ledger argument; the series risks turning civic process into its dominant dramatic vocabulary. The text uses bodily work and human limitation to counter this but requires an **independent** literary assessment before acceptance. Further adversarial checks should ask:

1. Does the scene rhythm allow genuinely dissimilar encounters, or merely substitute fuel and light for the prior weeks' records and petitions?
2. Does Jake remain the causal protagonist, or do the strongest decisions belong disproportionately to Mara, the singer and the ferrywoman? If the latter, sharpen Jake's costly agency without breaching the exclusive-twelve-owner POV rule.
3. Is the examiner's ability to release two packets medically and contractually plausible *inside this fictional secondary world*? No clinical efficacy is asserted, but details warrant sensitivity and technical review.
4. Do the upper bend, hill, foundry, observatory ward and far-bank sightlines coexist on any approved historical Atlas? **Not approved.**
5. Is the mother-message scene earned by the previous Week 8 lens scene, without converting a partial contact into a too-easy restoration of the family?
6. Is the new scattered light system a distinct governing choice rather than a bell-network symbol rebranded, especially after the separate 2021 *Keeper of the Unlit Lamps* chapter?
7. Can six source-scored miniatures be assembled into a compelling season-sized narrative without exhausting reader interest or repeating scoreboards?

## Technical gate

Added `living-novel/historical-chronicle/qa/test_2023_ninth_week.py` (**12** unit/regression cases) for pinned extract SHA, scores, six disjoint pairings, winner order, per-scene source match, substantive length, 3–6 slot-one result, provenance and future-knowledge firewall, the preceding W08 Git blob, append-only 54/84 coverage, active POV/Atlas/release holds, and protected four-file main-canon Git blob locks. Registered a named W9 step in `.github/workflows/novel-os-ci.yml`. Previous W3–W8 compatibility assertions now permit W9 append-only continuity; their original source, scene and negative checks remain.

**Observed exact-tested-code CI:** GitHub Actions all **completed successfully** at commit `c9f634af9bd08410223c6672d9604cd3d2e43922` (the W9 source/continuity/manuscript/test/receipt changes plus the repaired non-tautological upstream-limit assertion). Runs: [Novel OS CI #40884407407](https://github.com/jakekaloper-hub/schemin-26/actions/runs/40884407407), [Bullpen Runtime CI #40884407422](https://github.com/jakekaloper-hub/schemin-26/actions/runs/40884407422), [Cross-Domain Authority CI #40884407540](https://github.com/jakekaloper-hub/schemin-26/actions/runs/40884407540) and [Repository Merge Gate #40884407370](https://github.com/jakekaloper-hub/schemin-26/actions/runs/40884407370). The named W9 step and W1–W8 Chronicle compatibility steps passed; the 12 new W9 unittest assertions also passed in observed job logs for the preceding `8e4edea...` run, then received a stronger actual-archive-limits assertion and successful re-run at `c9f634a...`. The next metadata/checkpoint commits require their **own final-head CI readback**.

**CI / independent review disposition:** TECHNICAL SUCCESS at the listed tested SHA only. This does **not** establish independent literary quality, source identity authentication, historic Atlas approval or canon/publication authority. [Independent Authors Council / Atlas / Umpire review requested](https://github.com/jakekaloper-hub/schemin-26/pull/243#issuecomment-6498323999); **no independent review or acceptance has been received**. Founder-only canon, merge and publication remain **HOLD**.

**Next eligible production:** Week 10 six-match source read and substantial scenes (or verified independent literary revision of the existing nine-week block), preserving protected Prologue and Chapters I–III and all preceding Chronicle texts. Source the next week's results afresh and maintain story-time knowledge boundaries.
