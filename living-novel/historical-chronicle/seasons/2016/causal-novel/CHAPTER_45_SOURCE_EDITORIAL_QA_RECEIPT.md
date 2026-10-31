# Chapter XLV — source and author-side editorial QA (NONCANON / HOLD)

**Chapter:** *The Road That Would Not Wait*. **Date:** 2026-10-31. **Branch:** `novel/historical-epic-2015-2026`. **Owning PR:** #243.

## Resumption and authority receipt
- Resume from Chapter XLIV, existing draft PR #243 head `8bcec65cda2594f90faa64c36a871f0d75179060` and the chapter-44 durable checkpoint; do not restart from main or revise its protected opening.
- Schemin main readback `40b4ff8a4ab5f15bd8e986329472b31494cc09c0`; Bullpen main readback `86889a59efb0e7dcdc37eef639981944dc77ed67`. Reviewed `living-novel/whole-book/WHOLE_BOOK_SOURCE_AUTHORITY_MATRIX_V1.md`, Novel OS session and book architecture, POV register, execution task registry and Bullpen command/lifecycle registry. Reviewed open #210/#211/#214/#215/#219, PR #243, #252, #261 and closed #188; #264 remains separate noncanonical rewrite candidate.
- The retained 2016 weekly archive blob `6dbec1fe2537139f3a97c6a78250e2bae082a518` is historical evidence, **not** owner-to-slot authentication. No ESPN results or actual-owner private motives were introduced.

## Actual writing, assembly and review
- Six connected fictional movements; **4,664 whitespace words including metadata/editorial handoff**. New source file `THE_ROAD_THAT_WOULD_NOT_WAIT_CHAPTER_45_NONCANON.md`, Git blob `e39363bcf373019193d1d299a9509bcb589eb9ba`.
- Continuous forty-five-chapter reader `READING_COPY_CAUSAL_CHAPTERS_01_45_NONCANON.md`, **263,852 whitespace words including manifest and chapter notes**, Git blob `839c6bba9df3e20a07c5048368ad43d4641e1208`.
- **Observed in-memory JS assembly PASS**: manifest 1–45 ordered, 45 begin and 45 end markers, one terminal marker; source text of all prior 44 embedded chapters preserved byte-exact after boundary stripping and new source embedded exactly.
- Prior reader `READING_COPY_CAUSAL_CHAPTERS_01_44_NONCANON.md` remains frozen, Git blob `e83303d18e0485a4cc811d7ac9c12b42f28a58be`.
- Added 20 on-disk Python regressions in `living-novel/historical-chronicle/qa/test_2016_causal_chapter_forty_five_reader.py`; at checkpoint creation **NOT YET RUN**. No test PASS or independent review is claimed until observed on exact committed SHA.

## Literary turning point
A three-person traveling company earns one evening's lodging and performance at Fara's table house. Nella's longing to hear other places creates a material mother-daughter disagreement with Sela; the child refuses a public summons to repeat her donkey-king role. Eren produces a fictive doorway with no road or wall, while maintaining the ban on using her speculative red-sky painting as historical evidence. Iven's company leaves without taking a child or securing a new itinerary. The desire to travel remains alive and unresolved.

## Adversarial author-side challenges — not Authors Council/Umpire acceptance
1. A visiting troupe can resemble another arrivals-and-shelter episode; assess whether new family dramatic pressure changes the narrative architecture enough.
2. Sela's caution and Nella's hunger for new places need independent emotional weight; an adult's refusal must not be reduced to arbitrary obstruction.
3. The door play may mirror Jake's false testimony too neatly; inspect for thematic overstatement and excessive protagonist self-reflection.
4. Historical performer arrangements, instruments and compensation are invented and require period-review. Fara's physical courtyard and any travel route are not approved Atlas facts.
5. Meric, Eren and Hessa retain outward observable agency, yet the manuscript remains singular Jake-interior. Eleven historical owner-to-slot associations remain unauthenticated. Do not add unauthorized POV.
6. Earlier fictional Sela net-mender and displaced mother have a **name collision**; no identity merger is asserted or justified.
7. Still unresolved: Orrel's false/corrected packet receipt, Pell's lost offer and ruptured trust, second horse/cart/freight, four coins retained by Jake and four advanced for the floor, travelers' destinations, Hessa's sister, Ina's dye suspension, short awning, closed kiln, Esi letter receipt, and Jake's outstanding shelter debt.

## Technical/release disposition
- Assembly: PASS (in-memory JS only).
- New Python tests and full historical regression suite: PENDING observed execution.
- GitHub exact-SHA workflows: PENDING observed readback.
- Independent Authors Council, historical Librarian, Character Canon, Atlas and Umpire signoffs: NOT RECEIVED.
- Founder-only canon/publishing gates: CLOSED. **NO MERGE. NO CANON PROMOTION. NO PUBLICATION.**
