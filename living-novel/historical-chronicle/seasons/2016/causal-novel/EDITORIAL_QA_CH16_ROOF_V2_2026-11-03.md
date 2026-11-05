# Chapter XVI V2 — developmental source and craft audit

**Date:** 2026-11-03. **Status:** Producer-side editorial assessment only. **NOT an independent Authors Council / Historian / Atlas / Umpire review. NONCANON / HOLD.**

## Source contract and protected authorities

- The story is a revision of original `THE_WORK_THAT_CROSSED_BACK_CHAPTER_16_NONCANON.md` (blob `134372fe502087a049f22871e0c9ac187d690059`) following original Chapter XV (blob `5bac0a5028acf452790c61ec41391660e86abb9e`). Original XVI is preserved.
- V2 revised source: `THE_WORK_THAT_CROSSED_BACK_THE_ROOF_THAT_TRAVELED_CH16_V2_NONCANON.md`, blob `cb0e438cd6c38dff913023e90c8c18eb94833741`. Existing I–V scene prose is unchanged before the new VI; title/metadata and editorial handoff are explicitly revised.
- The new VI adds **2,060 written prose words**. Revised XVI has **8,063 source words including metadata**. The source-pinned thirteen-part edition through original XVI contains **83,287 source words including chapter metadata**; 13/13 component bodies are manifested.
- One fictional Jake / `CHAR-JAKE-KALOPER` is the sole limited interior viewpoint. The 2016 Flaim archive `G01_2016_FULL_WEEKLY_MATCHUPS.json` (blob `6dbec1fe2537139f3a97c6a78250e2bae082a518`) does not authenticate a 2016 human manager-to-scoring-slot binding; no such inference is made.
- The approved Prologue and 2026 Chapters I–III are not edited. Their current branch Git blobs were compared against main and matched.

## What materially changes on the page

The already-established split boat awning now fails in rain after the river departure. Cargo protection requires the crew to arrest the boat, mend the cloth overhead, reset an iron case, and lower the edge of the cover. Pell appears as an experienced older carrier before his established Chapter XVII appearance. Deren loses part of the promised travel schedule; a damp **outer binding**, not an entire cargo bale, is marked for **later inspection**. The goods have not yet been accepted at the stone landing. Jake has done work but has not completed the two-day wage bargain or paid his old creditors.

This is a more dramatic bridge into Chapter XVII than a second moral argument about who owns a road: it forces Jake to learn from another worker, own a mistake without inventing certainty about a pre-existing wedge fault, and work within an imperfect crew. The role of Pell is concrete, not a newly licensed owner POV.

## Producer objections requiring an independent reader

1. **Rhythm and duplication.** Original Chapter XVI already reaches a reflective closure as the boat pulls into the river. The addition produces a second late-chapter rise and another coda. A developmental editor may prefer compressing the original ending instead of keeping both passages intact.
2. **Technical plausibility.** An awning patch, a loosened iron-case wedge and a lowered roof tie must be checked against coherent vessel geometry and period craft. These are narrative inventions, not verified Atlas engineering or historical facts.
3. **Wage consequence.** Delayed arrival and exposed freight are measurable costs; whether the wage bargain has enough lasting personal stakes to sustain Chapters XVII–XVIII remains an open literary question. Do not convert a conditional two-day wage into income received before the work ends.
4. **Continuity exactness.** Chapter XVII already contains Pell, the stone landing and an accusation that Deren's vessel arrived late. The revised account permits—but does not compel—a specific freight inspection result there. Do not silently make Deren's marked bale accepted or rejected.
5. **Public/private firewall.** None of the dialogue, motives, households, debts, boats or terrain are ESPN facts or authorized real-owner biographical claims. The fiction must stay classified as proposal pending period Character Canon and Atlas acceptance.

## Observed technical results

- At commit `4458dd5e6b10e007fcc045f82bb0a54409971aa1`, new regression **test_07** failed because an asserted metadata phrase did not match the edition's actual wording; this was a test assertion mismatch, not a manuscript defect.
- At corrected commit `62874ebab7932b61794d077b412a5dec5356b01d`, the new **eleven-test Chapter XVI / thirteen-part reader step PASSED** and GitHub workflows **Novel OS CI #41591730470, Cross-Domain Authority CI #41591730480, Bullpen Runtime CI #41591730522 and Repository Merge Gate #41591730513 succeeded**. This is producer-run technical proof only, not an independent literary review.

**Disposition:** HOLD for actual independent literary, Historical Librarian, Character Canon, period Atlas and Umpire scrutiny. No merge, release, publication, canon promotion or 2016 owner identity rebind authorized.
