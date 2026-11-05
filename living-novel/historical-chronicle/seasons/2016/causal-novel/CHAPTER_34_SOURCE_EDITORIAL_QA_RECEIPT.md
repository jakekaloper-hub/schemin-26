# Chapter XXXIV — Source / Literary QA (NONCANON, INDEPENDENT REVIEW HOLD)

**Production date:** 2026-10-31. **Existing branch:** `novel/historical-epic-2015-2026` / draft PR #243. **Status:** author-side challenge and executable assembly checks; **not independent acceptance**.

## Delivered literary material

- Chapter: [*The Bees in the Wedding Arch*](THE_BEES_IN_THE_WEDDING_ARCH_CHAPTER_34_NONCANON.md), **7,684 whitespace words** including introductory provenance and editorial handoff, **five new narrative movements**.
- Chapter Git blob: `6793680804005b9af165cf26b63d1d52c34c233e`.
- Continuous [34-chapter reading copy](READING_COPY_CAUSAL_CHAPTERS_01_34_NONCANON.md): **190,543 whitespace words** inclusive of metadata and component notes, with all 34 chapter source passages embedded under SHA-pinned delimiters.
- New reader Git blob: `0822c85b9cf936fe319701b16c74726e6a1a0441`. Previous 33-chapter reader blob `72f7b9ae92627cc5bc8f63562a710b9a26d959d0` remains unchanged.
- Historical evidence authority: `living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json`, Git blob `6dbec1fe2537139f3a97c6a78250e2bae082a518`, unchanged. **2016 team-owner slot binding remains unverified.** No new Flaim/ESPN facts were invented.

## Continuity and actual causal change

Chapter XXXIII ends with an unperformed wedding, Lysa leaving with Serra, Corin holding an unfinished ring, a paid feast consumed and two families still at odds. In XXXIV, an incidental **invented** bee swarm gathers on the green arch left over Fara's gate. The attempted move requires Keret's actual craft rather than an omen argument; the arch's unsafe tie prevents preserving it. The physically observable consequence is the arch's removal and Fara's reclaiming her doorway, without implying the marriage took place or assigning metaphysical meaning. Corin chooses to contradict Daro's demand to keep the arch. Lysa returns to the settlement on her own terms, allows her rope to be used, and refuses to turn the bees into consent. Their brief conversation acknowledges the hurt and their unequal assumptions without creating reconciliation or remarriage.

Jake alone carries limited interior narration as the **proposed** historical CHAR-JAKE-KALOPER. Secondary-world people have spoken and enacted independent choices, but have no privileged internal viewpoint or automatic owner identification. The sealed kiln, previously bounded wages, unpaid shelter debt, Mev/Esi delivery uncertainty, missing Pell/driver/horse/freight, mare-care uncertainty and empty-cart recovery uncertainty remain open. The narrative invents no scoring facts or approved geography.

## Author-side adverse editorial examination (not authenticated Authors Council)

1. **Symbolic convenience:** A swarm on the failed wedding arch could resemble authorial intervention designed to make a tidy moral illustration. Consider moving the incident away from the arch or showing natural constraints that deprive it of verdict status. The current treatment explicitly denies a sign interpretation and centers the beekeeper's craft; independent readers must judge whether this is sufficient.
2. **Character texture:** Daro risks functioning as a single-note pressure figure, and Keret risks explaining the chapter's theme through professional aphorisms. Serra's limited change of behavior and Corin's admission are intentionally incomplete, yet may feel too expedient after the previous chapter. Lysa's desire to stay in her home settlement and preserve her work is observable but needs richer, independent future action.
3. **Beekeeping and period material plausibility:** Swarm behavior, daytime temperatures, seasonality, basket handling, sting first aid and stability of a new colony are proposed dramatic details rather than field-verified practice or period-correct Atlas facts. An experienced apiarist and Atlas reviewer should test this sequence before approval. The keeper **does not claim** all bees recovered or a stable hive.
4. **Narrative rhythm:** Long stretches of bystander dialogue and the crowd's interpretations could repeat the previous wedding's public argument or the earlier shadow-play's community-meaning debate. Consider deleting explanatory lines and deepening Jake's own consequential choices without commandeering the supporting characters' decisions.
5. **Causal/legal scope:** Fictional wedding customs, bee folklore, property, work roles, community social sanctions and routes must not be treated as binding Commonwealth institutions. No real 2016 owner intentions, trades, scores, titles or historical geography are inferred.
6. **Character and canon firewall:** The twelve exclusive principal POV rule, protected Prologue/Chapters I–III, current lineup, Atlas and source matrix outrank this provisional historical text. The previous archive and reader remain unmodified. Never characterize self-review as independent review.

## Observed local verification; remote CI not yet claimed

On the authorized connected Mac, an isolated clone was checked out clean at **prior PR head `cfcb346589b2322ba7d671d184945a6514630318`**. After preparing the new files:

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v living-novel/historical-chronicle/qa/test_2016_causal_chapter_thirty_four_reader.py` — **15 tests passed**, 0 failures (observed).
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s living-novel/historical-chronicle/qa -p 'test_2016_causal*.py'` — **432 tests passed**, 0 failures (observed).
- The test suite validates all 34 source passages, Git blobs, exact reader assembly, preserved prior reader, protected 2026 Prologue and Chapters I–III and retained 2016 evidence. Its semantic checks are negative governance guards, not a literary assessment.

**Remaining acceptance gates:** GitHub CI at the final pushed SHA, independent Author Council / Librarian / historical period Character Canon / Atlas / Umpire decisions, 2016 historical owner authentication and Founder-only canon/publication approval. The existing Netlify preview has previously failed; this receipt makes no claim of resolution. **DRAFT / NONCANON / NO MERGE / NO CANON PROMOTION / NO PUBLICATION.**
