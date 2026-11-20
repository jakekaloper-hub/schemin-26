# 2023 Chronicle — Week 5 Source Concordance and Literary QA

**State:** NONCANON / SOURCE-JOINED / LITERARY SELF-REVIEW / HISTORICAL ATLAS HOLD / INDEPENDENT UMPIRE NOT ACCEPTED.  
**Owning branch/PR:** `novel/historical-epic-2015-2026` / #243.  
**Work:** [*The Boat Without a Name*](W05.md), 5463 whitespace-separated words including manuscript frontmatter, source headings and final handoff; six individually dramatized historical encounters, opening and aftermath. This count is not a professional editorial word-count certification.

## Controlling evidence and its limits

Archival source: `living-novel/production/full-rewrite-2026/evidence/G01_2023_FULL_WEEKLY_MATCHUPS.json` at Git blob `ded119cde5c660f87f197f269b8d6ddd2a11316a` (Flaim / ESPN league 1417621 labeled extract). The original raw ESPN provider SHA is not available. Only historical team banners, slots, matchup winners and two-point-decimal scores are treated as league evidence. Human-owner identity joins are **not authenticated**, including the proposed Jake / slot-1 connection (user-attested). Competition home/away indicators are **not physical venues**. Civilian behavior, food shortages, river flooding, debt, charter conditions, visual settings, family relationships, and the improvised boat are all **fictional proposals**.

| Literary encounter | Archived home / points | Archived away / points | Winner / margin |
| --- | --- | --- | --- |
| 1: A Market that Would Not Move | Red Leopards (#2) 141.44 | Mixon it up for a week (#10) 149.96 | Mixon it up for a week (#10), 8.52 |
| 2: Four Hands on One Stone | Benedict Coomhersnatch (#5) 110.46 | Benedict Arnold (#8) 106.12 | Benedict Coomhersnatch (#5), 4.34 |
| 3: The First Victory and the River | Benedict Kenobi (#1) 182.48 | Two Dreaded Snake (#6) 129.42 | Benedict Kenobi (#1), 53.06 |
| 4: The Cost of a Seat | The Blew Waffle's (#7) 181.19 | Arm Chair GM (#11) 186.06 | Arm Chair GM (#11), 4.87 |
| 5: A Song Taken Apart | Eggs Benedict (#12) 158.76 | The KING of the Octagon Village (#3) 161.84 | The KING of the Octagon Village (#3), 3.08 |
| 6: The Boat Without a Name | El Niño (#9) 97.02 | The LLC (#4) 161.56 | The LLC (#4), 64.54 |

All six rows and twelve unique slot IDs were transcribed directly from the same pinned source blob, not derived from 2026 records. The slot-1 historical sports record across Weeks 1–5 is four defeats followed by Week 5's **182.48–129.42** first victory (margin **53.06**, standing **1–4**); this is **not** provider-verified historical ownership. No fantasy score is made the physical cause of any fictional event.

## Continuity, temporal law, and manuscript containment

The previous Week 4 ends with a chain closing the public landing, a threatened kitchen, damaged amphitheater, unpaid repairs and competing charter texts. This Week 5 does **not** resolve those matters with a cleaner document. The fictional river's rising water destroys the operational ferry and forces a concrete change: Jake steps over the chain to release a trapped mooring, Varn cuts the shackle under pressure, the ferryman's daughter organizes the improvised punt, a destroyed public bench becomes timber and Varn assumes temporary personal responsibility. The ferry stays lost; the toll concession and public debt stay unresolved. These are invented narrative consequences, not archive facts or preapproved historical geography.

Only `CHAR-JAKE-KALOPER` carries limited interior viewpoint; all secondary people are depicted through actions and reported speech. Five surgical edits after the initial manuscript commit replaced inferred internal states of the apprentice, constable, daughter and singer with directly perceptible behavior or reported statements. Additional independent scrutiny of focalization is still required. The year-correct `Two Dreaded Snake` banner is never assigned later visual morphology; El Niño is an archive banner, not a personified, speaking storm. Four Benedict team names remain separate labels. Week 6+ outcomes are excluded from character knowledge.

No modification was made to the first four Chronicle weekly manuscripts, the 2023 causal chapter *The Fourth Address*, or the four protected hard-canon manuscript files on `main`. The protected files were directly re-read from the PR branch and their Git blob identifiers matched the known `main` hashes (Prologue `5ef240b3`, Chapter I `26a17f05`, Chapter II `30fcf23a`, Chapter III `49e1fd1c`). The 2023 regular-season companion Chronicle now has **30 of 84** archived pairings in draft prose, Weeks 1–5; postseason is not drafted.

## Executable regression and observed evidence

Added `living-novel/historical-chronicle/qa/test_2023_fifth_week.py` with **11** cases for archive bytes, six outcomes and twelve slots, six nontrivial scenes, exact winner/margin formatting, the 0–4 to 1–4 slot-1 record, future-result exclusion, POV/source limits, preservation of Week 4 bytes, season-manifest coverage and protected hard-canon bytes. Adjusted Week 3/Week 4 continuity tests narrowly to support an appended fifth week without weakening their original prefix/source facts; registered a named Week 5 CI step.

At **`4906d2db386f621b241aba09148b586b6473f320`**, GitHub Actions **Novel OS CI #40851677622** completed **success**, including the separately named Week 3, Week 4 and Week 5 steps; Cross-Domain Authority CI #40851677737, Bullpen Runtime CI #40851677716 and Repository Merge Gate #40851677624 also succeeded. This proof applies to that exact commit only. A later five-edit prose revision at `96bc2be5f2cb4142f8fe532b22a4cdc65c86e7b4` requires its own exact-head CI readback; do not treat the earlier success as a certificate for later bytes.

## Adversarial literary review — SELF-CRITIQUE, NOT INDEPENDENT ACCEPTANCE

**Continuity risk:** The prior episode's chain, Varn's debts and the amphitheater reappear extensively. The changed object of dramatic attention is the sacrificed ferry and a risky crossing, but the accumulated public-infrastructure motifs risk becoming repetitive when these companion installments are read consecutively. Review the full Weeks 1–5 reading sequence for narrative velocity and whether Jake's long involvement has displaced other characters' agency.

**Moral simplification risk:** Varn assists at the dangerous shackle and waives a temporary crossing charge, but the compromise could make him a convenience rather than an antagonist with genuine self-interest. Test whether his creditor obligations and personal guarantee are properly earned by previously shown terms rather than invented to manufacture a reversible cliffhanger.

**Independent supporting-character agency:** Mara decides to move the windlass wheel, the apprentice brings stone without permission, Sena yields food and timber, the singer dismantles his triumphal song, and the ferryman's daughter refuses to let Jake board the punt. An editor should test whether they each retain goals independent of teaching Jake a moral. The daughter notably directs the decisive crossing; Jake remains ashore.

**Historical and geographic caution:** A river rising rapidly without rain at the landing is plausible in some conditions, but no historical climate, reach, travel distance, settlement name or 2023 Atlas placement has been authenticated. Never present the river as a canonical place or imply El Niño's archival score created the weather. Contest scores appear via fictional notices; this does not attest exact ESPN finalization times.

**POV and temporal audit:** No non-Jake principal internal POV has been intentionally written. Some external chronicle sentences may still read as omniscient, requiring independent line-edit evaluation. No prospective Week 6 sports result is included as knowledge of Week 5 characters. No actual historical owner motive, conduct, trade or personal biography is inferred.

**Proof vs approval:** Automated checks establish deterministic source and safety assertions, not literary excellence, authenticated historical identities, independent Umpire consent or Founder release authorization. This draft is **not merge-ready** and **not canon/published**.

## Continuation

1. Observe exact-SHA Actions for the latest prose and metadata commits and repair any real failure.
2. Ask an independent reviewer/Umpire for source fidelity, POV, time, dramaturgy and Atlas objections; a PR comment is a request, not acceptance.
3. Continue Week 6 only from its own six verified archive rows, carrying forward a noncanonical lost ferry, temporary punt and unresolved concession without fixing geographic positions.
4. Preserve Founder-only approval and publication holds.
