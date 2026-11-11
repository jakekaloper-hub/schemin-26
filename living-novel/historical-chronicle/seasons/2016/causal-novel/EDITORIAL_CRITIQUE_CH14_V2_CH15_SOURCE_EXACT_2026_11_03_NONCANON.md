# 2016 Developmental Reading — Fire Aftermath / Passage Editorial Challenge

**Date:** 2026-11-03. **Producer-side analysis, NOT an independent Authors Council or Umpire review. NONCANON / HOLD.**
**Working branch:** `novel/historical-epic-2015-2026` (PR #243). Authoritative main source matrix: `living-novel/whole-book/WHOLE_BOOK_SOURCE_AUTHORITY_MATRIX_V1.md`, Git blob `67fcd669dc7b43393f2d15e93545301961dd81e4`.

## Text actually produced and carried forward

- Chapter XIV revised candidate `WHAT_WAS_LEFT_IN_THE_YARD_THE_DAY_NOT_ENTERED_CH14_V2_NONCANON.md`, blob `6ab6b5cd3faeb5b926f4fba35d5e870772b2d7a9`, **7,318 source words** including metadata. The retained unmodified XIV has blob `f76ec3ae5245bccf57a8df2a3f3d76001319c68e`.
- Sixth movement *The day not entered*: **2,099 newly written source words**. Dramatic question: Can a laborer remain an identifiable claimant when damaged institutions treat inability to work as absence? Jake proposes speculative timber proceeds as compensation; the injured worker refuses a false equivalence. The keeper reads his actual outstanding record and creates a third category for work *to be measured*, which is neither wages earned nor wages paid. Jake loses a potential freight shift after remaining in the yard; he cannot recast this as an end to any old debt.
- Eleven-part composite `READING_COPY_2016_CAUSAL_CH01_14_ELEVEN_PARTS_THE_DAY_NOT_ENTERED_NONCANON.md`, Git blob `d3efc3531330eb959570a3828ca909ba4f75a28f`, source-only **69,102 words**.
- Twelve-part composite `READING_COPY_2016_CAUSAL_CH01_15_TWELVE_PARTS_PASSAGE_WITHOUT_TITLE_NONCANON.md`, Git blob `50463f970f76a6908e286f6cf4f9db09b03eac44`, source-only **75,224 words**, preserving the unmodified Chapter XV, *The Passage No One Could Sell*, Git blob `5bac0a5028acf452790c61ec41391660e86abb9e`.
- Earlier consolidated chapter sources for original positions I–XIII are kept unchanged; the twelve-part reader is source-exact rather than a new commissioned rewrite of each scene.

## Technical proof and limits

A direct source/manifest comparison during assembly verified 11 and 12 consecutive wrappers, matching author body bytes after newline trim, corresponding Git blob locators, and source-word arithmetic. The two GitHub file readbacks matched the submitted edition content.

Added `living-novel/historical-chronicle/qa/test_2016_twelve_part_passage_reader.py` with 12 unittest cases, and appended the corresponding dedicated step to `.github/workflows/novel-os-ci.yml`. GitHub Actions commit `ffa77821861c89ff7840e99699bae6e7851be481` **failed one test assertion**: test 09 sought the phrase “no general road access,” although the manuscript accurately said “do not constitute general road access.” The recorded logs show 11 tests passing and one assertion failing. Corrected the *test expectation*, not the manuscript, in commit `b02f6cee1b8952e3056ff82e7e83f3bc7809f709`. **Do not treat that correction as green until the new exact-commit run completes.**

Both branch and main protected 2026 Prologue and Chapters I–III were separately fetched on 2026-11-03: all four blob identities matched. No hard-canon modification.

## Independent editorial questions — actionable, not signed off

1. **Specificity vs didacticism.** The injured worker's refusal and the keeper's damp ledger materially resist the protagonist's urge to rule by gesture. But the recurring formulation “not payment / not a promise / not a settlement” may become repetitive after earlier shelter, contract, printing and freight scenes. Test whether the speech is embedded in lived reactions or turns into another administrative parable.
2. **Causality and timing.** V2's sixth movement happens the morning after the end of XIV's original evening; XV begins on a later voluntary walk after carrying water. The transition is plausible, but an editor should verify whether Jake's missed freight shift, the mill's new work-to-measure category and the daughter's untested bench become operative later, rather than disposable motifs.
3. **Worker agency.** The injured worker tells the keeper to record that he *heard* the debt without accepting it. The woman with red hands presses for her own entry. Keep this agency distinct from Jake's moral awakening; neither laborer exists merely to teach him.
4. **Physical/financial plausibility.** Some timber is set aside for potential short bracing while other salvage is offered for sale. No sale, wage payment, structural clearance, documented work commission, injury reimbursement, or mill reopening occurs. Independent review must challenge any unsafe proximity to unstable masonry and whether temporary pay-record practices make sense within an as-yet-unratified fictional institutional system.
5. **Geography discontinuity risk.** XV's quay, orchard steps, ferry and separate damaged bridge are hypothetical; they must not silently become the same place as the earlier lower crossing, nor an authenticated Atlas route. The period Atlas needs to approve or reject all physical location links before canon promotion.
6. **Historical/POV firewall.** Retained 2016 ESPN archive evidence and adapter-reported standings do not supply a complete manager-account join. The two Austin-named team slots are distinct. All new or revised interior narration remains fictional `CHAR-JAKE-KALOPER`, with other people's actions externally observed. There is no new human owner attribution, fictional result or 2016 postseason character foreknowledge. Twelve owner identities remain the only eligible principal viewpoints; no additional POV may be invented.
7. **Novel structure.** Twelve manuscript parts remain within a broader original 72-chapter Jake-limited candidate. Source-exact assembly alone is not literary acceptance. A complete developmental rewrite should test whether the repeated limits-of-authority motif accumulates into a larger adversarial plot rather than exhausting its dramatic force. No promise of equal chapter allocation to each league owner is required by the governing causal architecture.

## Release determination

**Producer-side verdict:** substantial noncanonical development, technically verifiable, eligible for independent scrutiny. **Not** independently accepted, character/Atlas-certified, historically owner-authenticated, tested green at the latest commit (until CI explicitly says so), merged, or published. Founder-only canon and publication authority remains reserved.
