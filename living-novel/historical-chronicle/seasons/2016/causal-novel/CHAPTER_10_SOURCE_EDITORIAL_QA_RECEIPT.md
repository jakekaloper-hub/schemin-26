# Chapter X — source and adversarial editorial self-review (NONCANON)

**Scope:** Existing draft PR #243, *The Board with the Hidden Crack*, 2016 Commonwealth causal novel. This is a writer-side assessment and technical verification ledger, **not an independent Authors Council, Character, Atlas, Librarian, or Umpire approval**. Founder publication and canon approvals remain HOLD.

## Deliverables and source pins

- Source chapter: `THE_BOARD_WITH_THE_HIDDEN_CRACK_CHAPTER_10_NONCANON.md`, Git blob `88bb693c735c4e999ecb6db396dabe71a85a768c`; **4,974 whitespace-delimited words, including notes**. Five causal movements, one fictional Jake/CHAR-JAKE-KALOPER limited interior POV. Existing file was present on PR branch at the beginning of this verification/recovery run; do not misrepresent it as newly written in this review action.
- Reader: `READING_COPY_CAUSAL_CHAPTERS_01_10_NONCANON.md`, Git blob `d1b8c25977afc8f44124da62b5f5da30c1527d38`; chapter source manifests and ten source-exact components. The reader's existing manifest has a non-semantic blank line before its ninth row: polish later only under versioned edit, not a source fact.
- Immutable predecessor: `READING_COPY_CAUSAL_CHAPTERS_01_09_NONCANON.md` (blob `cac0da28530f7d040b3856c2666ee975ef0617f3`), with prior chapter blob pins unchanged.
- Historical evidence: `living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json`, Git blob `6dbec1fe2537139f3a97c6a78250e2bae082a518`. This is **retained Flaim/ESPN transcription**, not fresh 2026 authenticated league data. Association of the historical scoring slot with the real person Jake is **not provider-authenticated**.
- Authority: `living-novel/whole-book/WHOLE_BOOK_SOURCE_AUTHORITY_MATRIX_V1.md`; `living-novel/os/NOVEL_CAUSAL_CHAPTER_ARCHITECTURE_V1.md`; current Founder-exclusive twelve-owner POV rule (older Edrin/Edin/Oren permissions superseded).
- Protected 2026 hard manuscript paths remain outside mutation scope: `living-novel/manuscript/PROLOGUE_DRAFT_V1.md`, `CHAPTER_01_THE_FIRST_ANSWER.md`, `CHAPTER_02_WHAT_COMES_BACK.md`, `CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md`.

## Causality, staging and POV

**Entering state:** After Chapter IX's personally financed but incomplete false-summons correction and after archived 2016 Week 13, *before* any postseason results enter story knowledge. Jake's promised shelter contribution has not been paid, the supplier invoice remains open, east rooms are cordoned, dubious grain is uncertified, the great wheel is unfinished and unturned, the missing claimant is unidentified, the sealed message is unopened, and the lower crossing and stranded cart remain unsafe/unresolved.

**Dramatic question:** When urgent private need collides with paid craft standards, will Jake try to pass unsound work as acceptable—and what is the actual material price of telling the truth too late?

**Five movements:**
1. Shelter provisions run short and supplier declines further credit without partial payment; Jake cannot simply undo the cost of public corrections.
2. Daughter of wheelwright hires Jake for accepted threshold boards at an explicit piece rate; she independently controls the order and sets conditions. Separate laborer's older claim remains disputed.
3. A boy discovers a hidden crack; Jake momentarily hides it and then discloses it, prompting inspection and rejection.
4. The daughter pays for accepted work, refuses gratuitous delivery, and reserves judgment about future employment. The boy refuses to supply Jake with exculpatory praise.
5. At the shelter Mara accepts only a voluntary portion of the insufficient wage, refuses to equate a contribution with supplier debt discharge, and asks for an ordinary morning water-jar task.

**Agency:** Daughter, worker, boy, Mara, and old woman exercise independent observable decisions; no claim to their private consciousness or unverified owner identity. Jake's concealment is not resolved into instant social absolution; imperfect disclosure has employment consequences.

**Facts firewall:** No fictive prices, routes, materials, institutions, weather or character relationships should be treated as authenticated 2016 Commonwealth/Atlas history. This manuscript does not assert a new league score, result, trade, winner, owner-to-character binding or postseason event.

## Ten-point adversarial literary challenge

1. **Repetitive moral pattern.** Chapters VIII–X all dramatize precision, truth and limited permission. Their themes are coherent but risk collapsing into case studies in ethical restraint rather than unfolding irreducible human conflict. Require developmental edit for one scene that advances desire and conflict without a spoken moral lesson.
2. **Agency under stress.** Jake's decision to turn the split board face-down is a genuine failure rather than a model answer; preserve this blemish. Avoid rewriting it as accidental innocence.
3. **Daughter's professional autonomy.** She has contractual authority over these boards and her own payment, but no proven or signed *great-wheel* commission. The test stool and limited trial must not become a certified mechanical design.
4. **Work/payment economics.** A piece rate for **accepted** boards and a separate clearing task are distinctly agreed; older unpaid timber wages remain separately disputed. Verify period labor conventions before publishing; no real monetary amounts are asserted.
5. **Physical believability.** A split that closes under lowered load, a dull tapped note, changing grain and cut dimensions require woodwork review; whether the crack survives safe inspection and whether a merchant would reject the threshold are narrative propositions, not engineering proof.
6. **Staging.** The boy arrives with a latch for a different upper storehouse door; he does not enter or repair the forbidden lower stair. High-lane walking does not certify lower-crossing safety.
7. **Sparse world texture.** Scene geography remains concentrated in yard, shelter and fork. Future chapter should leave these staging cycles for a new dramatic environment without silently inventing approved Atlas geography.
8. **Repetition of ledger scene.** Mara's closing money conversation parallels earlier shelter accounting. A later chapter should foreground bodily action, a relationship irreversibly changing, and an external stake rather than another explanation of unsettled debts.
9. **Unknown identity safeguards.** Singer's destination, missing claimant and their possible connections remain unknown; private chest remains inaccessible and sealed message unopened. No puzzle closure by implication.
10. **Period knowledge.** The chapter is sequentially after 2016 W13 notice, but the retained source does not authenticate real calendar day, climate, owner identity or postseason foreknowledge. No owner-only interior POV beyond Jake.

## Observed technical failure and repair

At PR branch head `8661fa1e7cac189aeb71102b0b82b7aee8f4c693`, four GitHub workflows were observed: Cross-Domain Authority CI, Bullpen Runtime CI and Repository Merge Gate **SUCCESS**; Novel OS CI run **#41020811890 FAILED** in the named 2016 Chapter Ten validation step, with **12 of 13 tests passing and one failing**.

The assertion expected the literal phrase `not provider-authenticated` while the chapter already states the logically equivalent, stronger negation `no human Jake-to-2016 team-slot association is provider-authenticated`. This is a brittle test assertion, not an archival or manuscript error. Updated `living-novel/historical-chronicle/qa/test_2016_causal_chapter_ten_reader.py` to validate the explicit full negative statement rather than editing fiction merely for a test. Repair commit: `3393494ee8b74f726c0276d5e616b77fef11f0c9`.

**Verification policy:** GitHub workflow success after the repair, including exact checkpoint-inclusive head, must be observed before claiming a pass. Unit test source, readback and a triggered workflow are not by themselves green evidence. No independent literary/Character/Atlas/Umpire approval observed. No merge, publication, financial transaction, or hard-canon promotion authorized.

## Next literary gate

Continue causal Chapter XI with an exterior, relationship-altering scene and a new cost, not another ledger or timber lesson. Keep only one of the twelve approved owners as principal interior POV (fictional Jake in this 2016 lane); label all year-specific material culture and geographies provisional. Maintain every open loop without conflating two chests or assigning the unknown claimant an identity.

**Disposition: NONCANON, DRAFT, editorial and independent Umpire HOLD.**
