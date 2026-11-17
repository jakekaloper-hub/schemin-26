# Week 10 playoff harvest — executed preproduction integration

**The reviewed harvest is integrated into the existing Week 10 issue. PNG execution remains paused.** This work continues Schemin PR #315 and Bullpen mission #154; it does not create another issue plan or restart production research.

## What is now selected

| Existing folio | Implemented editorial change |
|---|---|
| W10-P28 — State of the Realm | D0nkey K0ng secures Burgers by beating ObiWan Jacoby in Week 12 and Three Dreaded Snake in Week 13. Red Leopards secures Wings by winning all four remaining games. Both routes occupy existing division callouts. |
| W10-P30 — The Playoff Road | All twelve teams remain alive; none has clinched. Nine wins guarantees a berth, while eight alone does not. Mud Dogs has both a division and shared-berth possibility. The visible record scenarios explicitly assume no tied games. |
| W10-P31 — The Next Six | All six fixtures and their competitive implications remain. One dated TheFFHub callout gives each team's playoff estimate after its own Week 11 win/loss: ObiWan Jacoby 52% / 13%; The Chili Cheesers 58% / 21%. It states that other games are simulated from season scores, excluding projections and NFL byes. |

The existing P30/P31 statement that another Mud Dogs loss eliminates the team is retained. The unqualified P28 claim that Mud must win all four is removed: a verified official-tie example qualifies Mud at 5–8–1. Any future tie must survive the league's configured weekly tiebreak; equal starter totals alone do not establish one.

These mathematical claims depend on the accepted seven-berth structure, division qualification and ESPN H2H assumptions. The vendor estimates are dated scenario outputs, not mathematical clinches, eliminations or evidence of forecast calibration. The separate Schemin descriptive adapter and its forecast hold are unchanged.

## Actual production consumption

The selected copy reaches `issue-previs.json`, storycards, illustrated briefs and nested briefs, folio plans, exact prompt text, the three actual requests and their manifest hashes. Human-readable issue, brief and folio mirrors carry the same copy. The selected department pages have no entries in the matchup-only director sequence file; that file remains unchanged.

[`playoff-harvest-consumption.json`](../../preproduction/playoff-harvest-consumption.json) binds six relevant page dispositions to exact copy pointers/checksums, current request checksums, the public source receipt and the protected complete-source checksum. P28/P30/P31 are `SELECTED_CHANGE`; P27/P35 are `REFERENCE_ONLY`; P29 is `NO_MATERIAL_CANDIDATE`. Existing status/loss claims supported by additional evidence are separately identified.

`integrate_playoff_harvest.py` provides a deterministic three-page synchronization operation. It rejects a changed finalized-facts checksum, preserves scenes and reference receipts, and retains the production pause. The existing broader reconciler now understands artifact-specific source locations and reapplies the accepted supplement after a later rebuild.

## Sources and review

League **1417621**, season **2026**, completed through **Week 10**. Canonical Memo facts were captured at 11:30 a.m. EST on November 17; the harvest's ESPN observation is 11:59 a.m.; the vendor session completed at 12:09:28 p.m. These are distinct receipts, not a single invented source time. The finalized standings, records and score totals reconcile.

The complete source is retained as **Schemin_26_Week_10_Reviewed_Playoff_Harvest.json**, SHA256 `9ec5f9c634326a68dab579051ba199fc766c16b21bde32e17aef4cf7dc7e3b1d`. It contains all twelve team perspectives, twenty vendor captures, sixty completed games, twenty-four future fixtures, sixty binary witness entries and one official-tie example. Witness counts describe stored examples, not unique outcomes or probabilities. The public repository contains selected values, assumptions, source checksums and review receipts; full raw inputs and private storage locators remain outside it.

Bullpen's canonical router was executed for source/analytics, editorial, implementation and acceptance scopes. Actual host agents performed Scout/Analyst, Beat Writer and independent Umpire reviews; the root host performed implementation, provenance and synthesis. Routing is distinct from consultation, and no external human Director acknowledgement is claimed. Bullpen retains domain authority and production leadership under the user's direction.

Review evidence: [Scout/Analyst](scout-analyst-review.json), [Memo editorial selection](memo-editorial-review.json), [initial Umpire scope correction](umpire-initial-review.json), [final independent acceptance](umpire-final-review.json), and [canonical routing receipt](bullpen-route-receipt.json).

## Verification and preserved work

- **49 tests passed**, covering existing final results, render contracts, sheet assembly, the concurrent composition/personalization pass, and nine harvest integration regressions. [Test output](tests.txt).
- Independent replay verified **all 61 retained witness entries** with zero qualification-set mismatches, all twenty vendor captures and all twelve teams' own-win/own-loss links. Qualified-team arrays are treated as sets, not official seed ordering.
- **31 unselected included requests are byte-identical** to production baseline `0343047b23b37a814340cafbcc7f830ebfe91919`. All 34 scenes, reference lists, geometry, composition and personalization are preserved. All 52 unique reference assets match their expected checksums. [Preservation receipt](preservation-check.json).
- Finalized facts, reading order, six-sheet grouping, character packet, landscape bible, director sequences and design/personalization registries remain unchanged. Optional P32 stays omitted. The concurrent P22 color-word correction remains intact.
- The historical design baseline is preserved. Its copy-invariance test now admits only the three separately reviewed harvest copies; every other copy, cast and geography check still uses the prior baseline.

The final package also preserves concurrent commit `3d80fc2a5944e45e1c250b1f42f0130f3f04ba20`, which adds design-review evidence and one personalization regression. It changes no sports source, page copy or render request. The 49-test result includes that new check.

## Current stage

Preproduction source/copy integration is complete and reviewable. The current manifest and production entrypoints explicitly keep PNG execution paused while Bullpen leads the next production decision. No artwork was generated, and actual pixel acceptance and Founder publication approval are not claimed.
