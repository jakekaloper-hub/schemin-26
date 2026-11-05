# Producer source, continuity and developmental QA — The Name Beneath the Gold

**2026-11-02 | PR #243 | DRAFT / NONCANON / EDITOR SELF-CHALLENGE ONLY; NOT INDEPENDENT AUTHOR OR UMPIRE ACCEPTANCE**

## Observed production
- Read Schemin main at `e989c4436ecbd7f6ba9db1362d6e8bd186ebaf80` and Bullpen main at `86889a59efb0e7dcdc37eef639981944dc77ed67`. Inspected Novel OS matrix, causal chapter architecture, 12-character POV register, historical chronology source policy, Bullpen command/lifecycle and execution controls. Checked #210, #211, #214, #215, #219; PR #188 (merged), #243 (open draft), #252 and #261 (open draft). Existing fifteen-part checkpoint used; old manuscripts not modified.
- **Actual 5,417-source-word chapter**, including front matter and handoff; **4,955 narrative-before-handoff words**. Six movements: Jake → Austin → Jake → Austin → Jake → Austin. Chapter blob `3c920a249aebb8f9b244d5e70027843a00708dad`.
- **Actual assembled 81,549-source-word, sixteen-part developmental reading edition**. Inserted the new chapter as **Part 3** between the original Austin/Jake opening pair and the original Zach chapter; all fifteen prior reader wrappers remain **byte-exact**. New reader blob `1910482c32d4c02c3b0f2b7f70a517c64e6a6abd`. Original fifteen-part reader blob `df42a31981d0017de410eaac3fb83f64454fed38` preserved.
- 26 new deterministic regression tests in `test_2025_sixteen_part_developmental_bridge.py`, wired to `.github/workflows/novel-os-ci.yml` at implementation commit `5975c706d80583d6d889d0682ed525551bc56d40`. At the time this QA is created **exact-commit CI has not been observed as passing**; status must be fetched and recorded separately. These tests cannot judge novel quality or authenticate the historical owner mapping.

## Dramatic admission and actual revision achieved
**Question:** Will a new champion and the former champion correct a public image that flatters one and rewrites the other, even when correction costs them both?

**Entering state:** Jake has certified the 2025 loss and surrendered the current insignia; Austin has won the 2025 final and holds the Belt. The opening pair already establishes each man's private relation to 2024 and 2025. No direct fictional meeting had yet tested their stated principles against another person.

**Revision of the reading experience:** Part 3 places them in direct conflict *before* the more geographically dispersed ensemble chapters. A patron's proposed wall image turns the official year-specific team names into an apparent uninterrupted personal reign, while an older depiction falsely converts a verified defeat into a literal kneeling gesture. Neither character has exclusive moral standing: Jake permitted glorification of his 2024 victory, and Austin initially benefits from an erased prior name. The patron's withheld contribution creates a real material cost; the correct result stays immutable. Jake relinquishes the misleading emblem; Austin cancels the commission and funds the workers already engaged. Both depart with a worse public story and no guaranteed reconciliation.

**Ending state:** The proposed hall facing remains braced and unfinished, the 2024 and 2025 competition truth unchanged, patron support lost, the character rivalry unresolved. The new fictional hall and its commission have no Atlas or institutional canon standing. This replaces no previous prose and does **not** cure all structural issues of the larger manuscript.

## Evidence/fiction firewall
- Competitive source events remain **2024 final ObiWan Jacoby 187.52 to The King 161.68**; **2025 semifinal The Immortal 152.20 to Dr. Duckhook 151.80**; **2025 final The Immortal 161.07 to ObiWan Jacoby 109.56**.
- Names The King and The Immortal are year-specific historical team-eight labels. ESPN/Flaim score evidence does **NOT** independently bind Austin or Jake to those historical real-person manager accounts. This draft uses current fictional owner-character labels provisionally.
- Painter, steward, patron, Hall of Names, damage to mural, dialogue, emotional interpretations and artistic gestures are wholly invented. No fabricated real-life owner conduct, league scandal, historical match, trade, travel route, claim of land sovereignty, or 2026 result is presented as evidence.
- Only CHAR-JAKE-KALOPER and CHAR-AUSTIN-BYARS receive limited interior; one new POV not introduced. Austin retains the Belt; Jake does not possess it. No Edrin/Edin/Oren interior, no humanized El Niño, no invented protected trophy memorial biography.

## Adversarial findings; no independent approval
1. **HIGH — Repetition:** Both existing openings end with lesson that scores do not define a whole life. The new meeting risks restating this thesis. Its added dramatic value depends on the interpersonal accusation, distinct wrongs, material cost and unresolved animosity. A future line edit should remove repeated abstract maxims and increase the consequences of the patron's withdrawal.
2. **HIGH — Economics/World:** A ceremonial fund and a funded entrance are unapproved institutional proposals. The mason's wages are shown as a finite obligation, but exact price and feasibility are invented; the unfinished facing is not a verified location packet. Atlas/World architects need to validate the place or keep the story noncanonical.
3. **HIGH — Temporal location:** The scene assumes a possible meeting after both previous private post-final episodes and before the later shelter scene, without establishing an actual geography or historical venue. That *relative order* is a proposed author sequence, not a verified itinerary.
4. **HIGH — Owner lineage:** Neither 2024-to-2025 team-label continuity nor the 2026 character register proves historical human manager ownership. No owner-account authentication was added.
5. **MEDIUM — Opposition:** The patron's terms are somewhat too convenient a foil. Improve the patron's economic argument and avoid reducing him to a disposable villain in developmental revision.
6. **MEDIUM — POV:** Jake and Austin have distinct interests and interior framing, but both lapse into polished metaphysical language. A later author edit should sharpen Jake's strategizing and Austin's ritual restraint, vary rhythmic sentence patterns and preserve ambiguity.
7. **HIGH — Whole-book limitations:** This source-exact edition is still a large anthology and is NOT a developmentally integrated book; many chronology gaps, repetitive appeals to duty, isolated owners, 2016's consecutive single-owner POV imbalance and archive/reader export issues remain.
8. **RELEASE HOLD:** No independent Authors Council, Umpire, Historian, Character/Atlas, Founder acceptance, PR merge, publication or deployment is evidenced by this QA.

## Technical guardrails
The new test file checks all source SHA-1 blobs, 16 exact wrappers, the insertion at index 3, preservation of 15 original wrappers and prior editions, 12 distinct registered owners, six legal interior movements, 2024/2025 score anchors and name-time boundaries, noncanon/manager-ID policy, protected 2026 Prologue and Chapters I–III and the separate 2016 reader.

GitHub Actions results must be observed on the exact final checkpoint SHA before marking a technical pass. Green checks would not constitute literary signoff.

## Next literary action
Conduct an actual line-level compression/revision pass of Parts 1–3 as one connected sequence (not more summary). Then decide how to interleave kitchen, road, hall and harbor without guessing a shared Atlas route; prove a few cross-character choices have consequences outside their own chapter. Separately address the 2016 72-consecutive-Jake-limited-reader structural defect using verified owner history. Hold all canonical and publication gates.
