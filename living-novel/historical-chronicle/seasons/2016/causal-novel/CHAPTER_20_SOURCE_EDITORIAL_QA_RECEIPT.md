# Chapter XX — Source and Editorial QA Receipt (NONCANON)

**Draft:** THE_CLOTH_THAT_WOULD_NOT_STAY_FOLDED_CHAPTER_20_NONCANON.md
**Reader:** READING_COPY_CAUSAL_CHAPTERS_01_20_NONCANON.md
**PR:** #243 on novel/historical-epic-2015-2026
**Date:** 2026-10-30
**Status:** Local author-side source/continuity review only; independent Authors Council, Character Canon, Atlas, Librarian and Umpire acceptance **NOT OBSERVED**.

## Observed work and testing

- Actually authored Chapter XX, **6,281 whitespace-delimited words including source notes**, five fully dramatized movements.
- Generated one continuous, noncanonical **20-chapter reading manuscript of 103,660 whitespace-delimited words**, including source metadata, manifest and editorial notes.
- Git blob of Chapter XX: **45ef477a74006e14ed9fc83ccf43966aeca2f098**.
- Git blob of assembled reader: **b150c37f0d8adda70359bb8a53d05079b9212631**.
- Chapter XIX reader prior blob: **98ab302848f4f3ed97d36cb3f1d4396a6529e004**, preserved. All first nineteen chapter manifest rows and extracted source components match previous reader exactly.
- Newly authored **15 Python regression tests** in test_2016_causal_chapter_twenty_reader.py; local runner executed full matching reader suite, **211 tests / zero failures**, prior to checkpoint, including previous 196 tests. Command: python3 -m unittest discover -s living-novel/historical-chronicle/qa -p 'test_2016_causal_chapter*reader.py' -q. Test suite is **not enrolled in GitHub CI**.
- Protected 2026 hard Prologue and Chapters I–III are byte-pinned in the local regression fixture; the retained 2016 archive is pinned to blob 6dbec1fe2537139f3a97c6a78250e2bae082a518. No edits to these protected paths or archive. Full suite reports local integrity, not fresh ESPN authentication.
- No verified 2016 score, historical owner slot assignment, trade, championship, real-person motive or future storyline asserted by this chapter.

## Independent-acceptance objections to be resolved

1. **Mara agency / major narrative change:** Her estranged sister Senn arrives, bringing a proposed family textile and a paid three-day inspection of a distant loom. Mara's departure is actual on-page action, not Jake's imagined consequence. However, this extends a significant unapproved family-history subplot and must pass period Character Canon and Author review.
2. **Avoiding protagonist-centered fable:** Esi retains the book and keys; she independently manages debt, receipts, shelter access and morning work. The dialogue can still read as instructing Jake; revision should trim a few explicit moral explanations and preserve Esi's conflict with both sisters.
3. **Senn characterization:** She has a tangible professional need, financial constraint, family hurt and incomplete grasp of the work. Challenge whether her arrival and repeated verbal reversals feel too conveniently timed after Chapter XIX.
4. **Daughter's occupational independence:** Her work remains for a separate buyer, and she quotes terms before contemplating travel. She is not retrospectively assigned an Atlas-approved workshop or the unapproved great-wheel commission's completion.
5. **Len's dramatic weight:** Len has an injured eye and a self-made carved bird, now with a brief reference to a brother. This is *fictional*, should not imply established family lineage or a clinically verified injury, and deserves later independent development.
6. **Material culture:** Dye bands, old shuttle, brass pin, loom beam and warped textile are plausible narrative devices only; specialized period-tech/material inspection is still pending. No distant lower-valley road or weaving shed should be considered approved Atlas geography.
7. **Temporal cutoff:** The action follows the night at western eave and spans the next daylight, evening and following dawn. No future 2016 Week 14 or playoff outcomes appear in story knowledge.
8. **Account continuity:** Esi enters only a bounded **one-coin partial payment**. Old supplier claim, original pledge remainder, earlier labor credits, unsafe grain, east room closure, great wheel, mill fire, missing claimant/chest/message, ticket refunds, bridge/cart, courier disposition and seasonal work offer remain unresolved.
9. **Authorial voice:** Important strengths are physical detail, two distinct sisters, a real departure and the visible ledger payment. Key weaknesses: perhaps too many lines functioning as aphoristic corrections and a final scene that risks telegraphing the theme; independent editor should challenge.
10. **Evidence boundary:** The 2016 record is an existing transcription, **not** provider authentication linking Jake to historical league slot 1; the depicted social, legal, family, route and craft events are invented proposals.

## Mandatory release holds

NONCANON / independent Authors Council/Librarian/Character Canon/Atlas/Umpire review not yet obtained. Founder-only canon, merge/publication approvals withheld. Do not auto-promote or overwrite the 2026 Prologue or Chapters I–III; do not call local green tests an independent editorial PASS.

**Continuation:** Review the family-subplot implications and move Chapter XXI into a new causal branch independent of the shelter account table, or first complete targeted deep revision if independent review finds significant defects. Never infer W14/postseason outcomes from fiction.
