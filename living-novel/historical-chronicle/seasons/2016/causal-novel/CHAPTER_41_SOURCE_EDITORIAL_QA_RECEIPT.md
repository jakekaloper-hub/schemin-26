# Chapter XLI — source and author-side editorial QA receipt (NONCANON / HOLD)

**Working title:** *The Marks at the Crossroads*. **Mission:** Founder-authorized Commonwealth Novel production; existing branch `novel/historical-epic-2015-2026`, draft PR #243. This is a continuation of Chapter XL, not a restart. **Execution date:** 2026-10-31. **Review posture:** author-side technical checks only; no independent author, Atlas, Librarian or Umpire verdict received.

## Authorities read before drafting

- `living-novel/whole-book/WHOLE_BOOK_SOURCE_AUTHORITY_MATRIX_V1.md`, main: active hard canon is the 2026 Prologue and Chapters I–III; draft causal novels remain noncanonical.
- `canon/characters/TWELVE_CHARACTER_NARRATIVE_POV_REGISTER_V1.md`, main: only the twelve owner/character principals are eligible for new or revised interior POV; this candidate retains proposed fictional Jake (CHAR-JAKE-KALOPER) as sole interior focalizer, without authenticating a 2016 owner slot.
- `living-novel/os/SESSION_CONTEXT.md` and `governance/execution-control/TASK_REGISTRY_V1.json`, main: reuse the current novel workstream and durable checkpoint; no new Novel OS.
- Bullpen `docs/COMMAND_SYSTEM_V2.md` and `runtime/lifecycleEngine.js`, main: reversible research → writing → testing → auditing → independent examination; do not simulate authenticated board participation.
- Prior `HISTORICAL-SAGA-20261031-2016-CAUSAL-CH40-FORTY-CHAPTER-READER.json`, Chapter XL and its source-exact 40-chapter reading copy, and retained 2016 matchup archive. No new league result is asserted.

**Intake main refs:** Schemin `40b4ff8a4ab5f15bd8e986329472b31494cc09c0`; Bullpen `86889a59efb0e7dcdc37eef639981944dc77ed67`. **Existing draft branch intake HEAD:** `e0c14b1ae1e637dd256d50decb0d8462b8e1fe11`.

## Actual literary production

- New six-movement chapter: `THE_MARKS_AT_THE_CROSSROADS_CHAPTER_41_NONCANON.md`, **7,884 whitespace-separated words including frontmatter and editorial handoff**, Git blob `4526f2c278167c43630aa10732f10e47a8fb1ef1`.
- New fully assembled reading copy: `READING_COPY_CAUSAL_CHAPTERS_01_41_NONCANON.md`, **237,708 whitespace-separated words including source manifest and notes**, Git blob `14ce93a324f62cf00307625c486bdbc17e4dd5f4`. Forty-one source chapters appear once, exact extracted source text matches every authored file and manifest SHA.
- Old 40-chapter reader preserved unchanged, Git blob `ecc93dfe2100ed68f9aa49e59c0427fc2dbf6295`.

**Causal turn:** The rumor that Ina's six-person private accommodation is public lodging induces Sela and her children to turn from an uncertain route. An improvised street gathering tries to oblige homeowners to accept travelers, but nobody establishes a lawful shelter order. Hessa refuses to surrender collective agency, Corin declines to enforce a supposed public count, and the dyework apprentice voluntarily departs with his tools. Sela chooses a separate outdoor camp without certified safety. Ina loses a skilled worker while her dye business remains suspended; the incomplete chalk door becomes a contested symbol rather than an official sign.

## Observed checks

- **PASS:** 19/19 chapter-specific Python regressions after an initial test-only phrase assertion incorrectly expected text present in the *reader's causal chain* rather than the *chapter*. The assertion was corrected without changing the manuscript. This failure and repair are preserved as author-side process evidence.
- **PASS:** 951/951 tests in `python3 -m unittest discover -s living-novel/historical-chronicle/qa -p 'test_*.py' -q` on the connected local Mac checkout, against this exact working tree before committing.
- **PASS:** 41/41 manifest source chapters embedded byte-for-byte as text, corresponding Git blob hashes matching, prior 40-reader unchanged, source archive preserved, and pinned protected canonical Prologue/Chapters I–III blobs unchanged.
- **GitHub CI / independent review:** PENDING separate exact-commit verification and independent acceptance. Local tests do not constitute GitHub CI or an Umpire verdict.

## Literary red-team objections and honesty boundary

1. **Single-POV concentration:** This saga strand continues to focus on Jake even while all twelve canonical owners remain its only eligible principal POVs. A technically lawful sole POV is not a complete twelve-POV literary achievement. **HOLD for polyphony work.**
2. **Civic rhetoric:** The public count and consent vocabulary may sound too contemporary for unapproved period institutions; an independent historical/editorial reading is necessary. The crowd is not a legislature; the vote never becomes enforceable law.
3. **Narrative recurrence:** The blue scrap and chalk door reprise earlier rumors, counterfeit notices and misdirection. This episode attempts a different irreversible cost—the apprentice's autonomous departure—but developmental editors should challenge whether this is enough differentiation.
4. **Physical geography / shelter:** The new family camps on an unspecified patch whose terrain, night conditions, water and safety are unverified. Do not treat it as an approved Atlas place.
5. **Character inheritance:** Lysa, Corin and Daro draw only on prior fictional Chapters XXXIII–XXXIV. Their acts are not verified historical owners' psychology or real 2016 events.
6. **Open economic outcome:** Apprentice employment and separate work opportunity are unknown; Ina's pending dry orders and wet-work restart are not solved by a late heroic rescue. The 21-night six-person agreement, cart with one side absent, water uncertainty, damaged awning, freight mystery and smoke cause remain persistent.

**Independent acceptance:** NOT RECEIVED. **Historical owner-slot authentication:** NOT RECEIVED. **Period Character/Atlas acceptance:** NOT RECEIVED. **Founder-only canon and publication approval:** NOT GRANTED. **No merge, canon promotion or publication authorized.**

**Next eligible task:** Advance Chapter XLII from the apprentice's departure and Sela's independent camp decision; stop returning to false-document mechanics as the dominant plot engine. Investigate a legitimately eligible additional canonical owner POV only if the historical period owner/character binding is established; do not sneak a supporting character's interior thoughts into the narrative.
