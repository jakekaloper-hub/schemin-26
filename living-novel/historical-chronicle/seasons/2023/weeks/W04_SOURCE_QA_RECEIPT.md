# 2023 Historical Chronicle — Week 4 Source, Production and Editorial QA Receipt

**Disposition:** NONCANON / DRAFT / SOURCE-CONCORDANCE PRECHECK / INDEPENDENT EDITORIAL HOLD.  
**Owning PR / branch:** #243 / `novel/historical-epic-2015-2026`.  
**Literary output:** [*The Price of the Other Bank*](W04.md), approximately **4,497 whitespace-separated words including header, source notes and historical handoff**, consisting of an original opening, six source-paired scenes and an aftermath. The prose is original fiction rather than a sports recap. This count is from in-memory pre-write segmentation, **not** a professional manuscript word-count certificate.

## Archival foundation and negative authority

Authoritative 2023 historical extract: `living-novel/production/full-rewrite-2026/evidence/G01_2023_FULL_WEEKLY_MATCHUPS.json`; Git blob `ded119cde5c660f87f197f269b8d6ddd2a11316a`. Provider attribution embedded: `Flaim ESPN 1417621`. Historical owner joins and original raw ESPN SHA remain **UNKNOWN**. The six rows cover twelve unique historical team slot IDs; home and away are contest fields, **not physical Atlas venues**. Every theatrical setting, merchant lease, debt, food shortage, civic act, injury, weather implication, supporting character, utterance and effect is **PROPOSED FICTION**.

| Scene / plot movement | Source home (slot) / points | Source away (slot) / points | Winner / margin |
| --- | --- | --- | --- |
| I — Ninety-day lease | Red Leopards (2), **166.78** | Benedict Coomhersnatch (5), **152.06** | Red Leopards, **14.72** |
| II — Jake signs a limited witness statement | Benedict Kenobi (1), **103.24** | The Blew Waffle's (7), **160.64** | The Blew Waffle's, **57.40** |
| III — Market oil sold to release flour | Two Dreaded Snake (6), **97.08** | Mixon it up for a week (10), **173.50** | Mixon it up for a week, **76.42** |
| IV — Arbitration without an actual ruling | The LLC (4), **170.62** | Arm Chair GM (11), **177.22** | Arm Chair GM, **6.60** |
| V — Amphitheater quarried for toll-station material | The KING of the Octagon Village (3), **90.92** | El Niño (9), **189.06** | El Niño, **98.14** |
| VI — Contested second charter copy | Eggs Benedict (12), **130.50** | Benedict Arnold (8), **106.98** | Eggs Benedict, **23.52** |

Source score/margin fields were individually transcribed and checked against the authenticated repository archive in the production writer preflight. This check did **not** execute the Python unit tests; CI evidence must be separately observed. For the historical **slot-1** candidate, Week 1–4 results are all losses: 113.02, 113.35, 183.46 and 103.24 points respectively; Week 4 losing margin is 57.40. This is **not proof** that the associated historical account was operated by the real Jake Kaloper.

## Novel OS/Atlas/character limits

- **Principal interior viewpoint:** Jake / `CHAR-JAKE-KALOPER` as an expressly **user-attested historical literary candidate, not provider-authenticated ownership**. His thoughts concern the fictional world only. Supporting merchants, ferrymen, clerks, musicians and inhabitants appear through observation or dialogue, without independent principal POV chapters. No retired institutional principal POV appears.
- **Unverified owners:** None of the five other historical contest pairs is represented as having directly caused the invented lease, hearing, bread shortage, demolition or archive dispute. Four separate Benedict banners are not collapsed into one owner. `Two Dreaded Snake` uses its year-correct banner but not later morphology; El Niño is neither personified nor assigned an owner biography.
- **Geography:** Landing, city, ferry, market, amphitheater, library, granary and council remain unnamed and without approved location IDs. All physical travel and distances are proposed, **HISTORICAL ATLAS HOLD**, with no assertion that archived home/away fields prove a venue.
- **Time:** New narrative begins only after the invented Week 3 road dispute. No character learns any Week 5+ result. The six archived sports verdicts are dramatized as circulated notices across a fictional week; this arrangement **does not assert the actual calendar date/time each fantasy result was finalized**.
- **Protected canon:** The draft touches neither `living-novel/manuscript/PROLOGUE_DRAFT_V1.md` nor Chapters I–III and does not revise the separately held 2023 causal novel chapter `The Fourth Address`.
- **Coverage:** 2023 regular-season historical chronicle now has 24 of 84 recorded pairings rendered in prose, Weeks 1–4; postseason is not started. Four weeks of companion history must not be mistaken for four canonical novel chapters.

## Technical verification plan / receipts

New test `living-novel/historical-chronicle/qa/test_2023_fourth_week.py` defines **nine** cases: immutable archival Git blob, six rows, twelve slots, substantive six-scene prose, exact winning and losing scores/margins, slot-1 four-game history, POV/time negative guards, manifest append and four hard-canon Git blob hashes. The pre-existing Week 3 suite was amended to allow a longer season manifest without weakening its original first-three-weeks invariants. Novel OS CI now has a named Week 4 test step.

**Observed GitHub Actions after receipt composition:** At exact tested commit `5066a69f72e9a765fdf8f625281b963f16d2ee21`, [Novel OS CI #40843878646](https://github.com/jakekaloper-hub/schemin-26/actions/runs/40843878646) completed **success**; the named **Week 4** and **Week 3 compatibility** steps separately report **success**. [Cross-Domain Authority CI #40843878752](https://github.com/jakekaloper-hub/schemin-26/actions/runs/40843878752), [Bullpen Runtime CI #40843878618](https://github.com/jakekaloper-hub/schemin-26/actions/runs/40843878618) and [Repository Merge Gate #40843878758](https://github.com/jakekaloper-hub/schemin-26/actions/runs/40843878758) also completed **success** at the same SHA. The Week 4 suite contains **nine Python unittest cases**; a successful named CI step is GitHub's observed execution outcome. These green checks do not prove prose quality, authenticated owner identities, Atlas compliance, independent Umpire approval, or Founder release authorization. Later receipt/checkpoint-only commits must not be described as tested by these earlier runs.

## Adversarial literary review — production self-critique, not independent endorsement

1. **Stronger cost, still risky moral symmetry.** Varn has a concrete economic argument (unpaid debt and public works), and the damaged kitchen, amphitheater and shoreline cannot be repaired by a righteous sentence. However, six public documents/decisions could still form the repetitive civic-equity pattern seen in Week 1–3. A skeptical editor should test whether the human connection survives without the charter exposition.
2. **Antagonist needs depth.** Varn acts decisively and helps an injured carter, but he remains identifiable chiefly by his concession. A later novel revision might give him non-expository relationships and a contradiction that wounds somebody he actually values.
3. **Protagonist agency is not sufficient proof of literary maturation.** Jake changes a receipt and makes two contested texts public, actions that do not free the ferry. An editor should examine whether his solution reproduces the earlier 'accurate document' motif too closely, and whether Week 5 requires action beyond another posted notice.
4. **World geography ungrounded.** The compact fictional civic landscape might contradict established 2023 Atlas constraints; no approval has been sought or received. Review travel/time plausibility before transplanting any setting to canon.
5. **Strict POV ambiguity.** This installment deliberately remains inside Jake's field of perception for every narrative encounter. Independently examine whether any sentence inadvertently becomes omniscient or assigns real owner-private feelings. None of the named civilians has a sanctioned principal POV.
6. **Chronology and symbolism.** Week 4 outcomes are listed across the fiction's days without a claim to real scoring time. Verify that no character knows a subsequent competitive result, and that El Niño's contest banner never becomes literal human agency.

**Independent Umpire/editorial state:** No submitted independent PR review was present at the start of this continuation. A PR comment asking for scrutiny does not equal acceptance. Founder-only canon promotion, publication, human-owner authentication, Atlas and independent author/Umpire decisions remain **HOLD**.

## Next eligible production work

After observing Week 4 CI and repairing any actual failures, write **2023 Week 5** if source-cleared and no higher-priority eligible task supersedes it; begin with the unresolved economic consequences rather than another generic arbitration, and keep the protagonist's fictional actions independent from the real person's private life.
