# Chapter XXIII V2 — The Width of a Blanket: Producer Editorial and Source QA

**Date:** 2026-11-03. **Status:** NONCANON / DRAFT / INDEPENDENT EDITORIAL HOLD. This is a producer-side challenge, not an independent Authors Council, Historical Librarian, Character Canon, Atlas or Umpire acceptance.

## Actual work and provenance

- Existing continuation is Schemin draft PR #243, branch `novel/historical-epic-2015-2026`; do not make a parallel Novel OS, reset the historical branch or merge.
- Original Chapter XXIII is intact: `THE_ROOM_BEYOND_THE_THRESHOLD_CHAPTER_23_NONCANON.md` (Git blob `d30c325ab05acf462693067e427bce9b069e0325`; 5,510 whitespace words including handoff).
- New developmental alternative: `THE_ROOM_BEYOND_THE_THRESHOLD_WIDTH_OF_A_BLANKET_CH23_V2_NONCANON.md`, source Git blob `1d00c5f4706e9fc006aac4ba560b87ce67fe5511`, 7,781 whitespace words including metadata. Inserted narrative scene “The width of a blanket”: **1,966** whitespace words including heading.
- Prior assembled reader: nineteen parts, causal Chapter positions I–XXII, Git blob `3826d48edce0339dfb8008dc27a2a4fa00ea9dc4`, 128,850 source words including metadata.
- New assembled reader: `READING_COPY_2016_CAUSAL_CH01_23_TWENTY_PARTS_BLANKET_AT_THRESHOLD_V2_NONCANON.md`, twenty source-pinned parts over causal Chapters I–XXIII; **136,631 component source words including metadata**. Parts 1–19 were carried over as exact source-identified bodies; part 20 is V2. Manifest gives individual source blobs and word counts.
- Historical 2016 ESPN/Flaim archive remains `G01_2016_FULL_WEEKLY_MATCHUPS.json` Git blob `6dbec1fe2537139f3a97c6a78250e2bae082a518`. No new score, opponent, manager, ownership binding, championship, trade, competition date or location asserted. Proposed fictional Jake is not authenticated to a particular 2016 slot.
- The 2026 Prologue/Chapters I–III remain identical to `main`: respective blobs `5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0`, `26a17f05eb0565e7648c29add03ee9580ec933c3`, `30fcf23a3eb8872fa0fb4dff029fe30044141121`, `49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc` (dual-ref readback).

## Causal purpose, not another ledger chase

At the public meeting in Chapter XXIII, the mother asks for a privacy screen. The new sequence stages an inexpensive trial with her own blanket and rope; it sags, obstructs the food passage and creates a genuine collision between children's privacy and the cook's duty to serve people safely. The plan is disassembled before supper. Tern has not accepted paid construction, and Chapter XXIV can still begin with the carpenter's inappropriate hinges. The children make and lose a temporary private place and ask specific, practical questions; their mother, not Jake, determines what access can be sacrificed.

Nell appears as a working craftsperson who has her own next engagement, will discuss seams only with explicit payment and **retains the second repaired bedding length**. Esi neither extracts free work nor silently pays the unpaid soap balance. The first bedding length remains with the shelter. The flour previously spilled from a measured, accepted delivery is not restored; the cook distinguishes the present pot from next mixing's uncertain yield. The older supplier invoice, Jake's pledge and separate missing-ledger questions stay open.

The public notice is posted by Esi and Tern in existing Section I; Jake does not gain credit for it. Sola left of her own accord earlier in the chapter; the stranger's clog is not certified as hers or evidence of injury. The original Chapter XXIV return-for-work plot remains possible. Esi maintains key control and operations; Len's impaired eye and carved bird remain unresolved; Mara remains away with Senn. Jake is the sole limited interior focalizer and is explicitly a fictional member of the twelve-owner principal cast. No institutional or supporting-character interior POV was licensed.

## Independent-adversarial questions and non-acceptance

1. **Space/Atlas — HIGH:** A west wall sleeping place, dining passage, table, bench, water jars, exterior gate and potentially a kitchen fire need a physically feasible relation in a period-approved plan. The trial curtain can create a bottleneck only if these elements are in a consistent geometry. No geographic or architectural canon is established by prose.
2. **Narrative repetition — HIGH:** Chapter XXI used a withheld linen length; Chapter XXII used spilled flour; Chapter XXIII now reprises both. The new scene must earn its emotional register as a different power struggle (privacy versus common space), not a disguised fourth paper/measurement lesson. Evaluate whether the closing child-height mark overstates the book's witness motif; consider cutting it in independent line edit.
3. **Nell's autonomy — HIGH:** She should have independent goals and material consequences, not merely be deployed to teach Jake noninterference. The new dialogue gives her a forthcoming paid engagement, control of her work and remaining soap claim. Whether that is sufficient is an **open literary question**.
4. **Timing and labor — MEDIUM:** Does the afternoon trial, kitchen count, later supper and first watch fit original Chapter XXIII's day, the cook's labor and Chapter XXIV's proposed screen? It has not been verified by period Atlas or an external editor.
5. **Literary temperature — MEDIUM:** The child’s joke about a smaller bowl is a human break in a procession of accounting disputes. An editor should test whether later descriptions explain the scene's meaning too explicitly.
6. **Historicity/owner binding — BLOCKED:** Verifiable 2016 league results are separate from fictional transactions and cannot license other owners' identities or their private motives.
7. **Independent release gate — BLOCKED:** No submitted independent review, umpire verdict or Founder publication/canon authorization is evidenced. The passing/failing status of CI must be read at exact commit, not inherited.

## Technical coverage

`living-novel/historical-chronicle/qa/test_2016_twenty_part_blanket_reader.py` contains twenty source-exact, regression, continuity and noncanon-barrier tests; `.github/workflows/novel-os-ci.yml` invokes it explicitly. Report an actual PASS only after inspecting an exact-commit workflow and its dedicated step/log. A producer-side analysis does not certify independent review.

**Disposition: developmental fiction ready for independent challenge, not canon. NO MERGE / NO PUBLICATION / NO CANON PROMOTION.**
