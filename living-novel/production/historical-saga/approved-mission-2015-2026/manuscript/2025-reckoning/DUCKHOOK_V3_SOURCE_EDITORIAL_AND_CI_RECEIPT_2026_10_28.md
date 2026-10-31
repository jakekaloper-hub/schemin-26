# 2025 Historical Reckoning — Duckhook V3 source, editorial and CI receipt

**Date:** 2026-10-28 UTC · **Status:** NONCANON / EDITORIAL HOLD · **Branch:** `novel/historical-epic-2015-2026` · **PR:** #243

## Work actually produced

- **New standalone original prose:** `THE_LINE_HE_LEFT_VISIBLE_DUCKHOOK_NONCANON.md`, approximately 2,288 whitespace-delimited words at first commit (minor temporal wording revised afterward). Zach/Dr. Duckhook's deliberately narrow after-loss teaching episode occurs following the 2025 semifinal and before the 2025 final; it does not import later results.
- **Full assembled alternate reading:** `THE_PLACE_LEFT_EMPTY_EXPANDED_V3_NONCANON.md`, approximately 9,541 whitespace-delimited words at first assembly (minor temporal wording revision afterward), nine scenes in order **Jake → Austin → Zach → Phillip → Jake → Austin → Jake → Austin → Jake**. This is explicitly a **developmental collection**, not an accepted causal chapter. All eight original V2 scene bodies are retained exactly.
- **Scoped scene register:** `SCENE_REGISTER_V3.json`, with per-scene historical event IDs, principal identity, story-time cutoff, raw-human-owner UNKNOWN and 2025 historical venue PROPOSED_UNAPPROVED. Existing `SCENE_REGISTER.json` and both original reading candidates remain unchanged.
- **Executable test:** `review/test_2025_reckoning_v3.py`, 10 deterministic tests admitted to existing Novel OS CI. Corrected Python slash/regex escaping in a same-run edit before passing CI; no failing run is represented as passing.

## Source receipts / factual firewall

| Authority | Repository byte evidence | Scope |
| --- | --- | --- |
| `living-novel/whole-book/WHOLE_BOOK_SOURCE_AUTHORITY_MATRIX_V1.md` (main) | Git blob `67fcd669dc7b43393f2d15e93545301961dd81e4` | Protected hard canon, source hierarchy and non-promotion law |
| `living-novel/history/PLAYOFF_MATCHUP_EVIDENCE_2022_2025.json` (main) | Git blob `9ac3eb65a621399d2cd4bf6600c11680a87ebb20` | Existing history transcription, **not** a fresh ESPN read |
| `living-novel/characters/11_ZACH_WILSON.md` (main) | Git blob `331434aab16bd715ba1ae383a34aa75f214d8c4a` | Zach's Duckhook principal identity and 2025 0.40 semifinal burden |
| `living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md` (main) | Git blob `26a17f05eb0565e7648c29add03ee9580ec933c3` | Named 2025 Austin/Duckhook fictional encounter, not raw historical human-owner binding |
| `THE_PLACE_LEFT_EMPTY_EXPANDED_V2_NONCANON.md` (PR #243) | Git blob `bcacc25f638e114f922075846fe4220b8cfd09a7` | Eight preserved scene bodies |

**Bounded historical results only:** ObiWan Jacoby 174.38 vs Three Dreaded Snake 153.20; The Immortal 152.20 vs Dr. Duckhook 151.80; The Immortal 161.07 vs ObiWan Jacoby 109.56. No past or future team results are created in prose. Invented practice equipment and officials are *not* facts about ESPN or the owners.

## Exact-code-head technical verification

At `4680aac9d827c522cb6accfa9938db65b05cb73f`, the four observed GitHub Actions workflows **completed SUCCESS**:

- [Novel OS CI #40781162841](https://github.com/jakekaloper-hub/schemin-26/actions/runs/40781162841), job `123142899215`, includes **10 V3 tests, OK** in named `Validate 2025 historical Duckhook nine-scene collection V3 (noncanon)` step.
- [Cross-Domain Authority CI #40781162840](https://github.com/jakekaloper-hub/schemin-26/actions/runs/40781162840), SUCCESS.
- [Bullpen Runtime CI #40781162722](https://github.com/jakekaloper-hub/schemin-26/actions/runs/40781162722), SUCCESS.
- [Repository Merge Gate #40781162565](https://github.com/jakekaloper-hub/schemin-26/actions/runs/40781162565), SUCCESS.

These tests establish deterministic source/assembly/scope gates only, **not** literary quality, Atlas acceptance, provider freshness or independent Umpire approval. Documentation/checkpoint commits after `4680aac9` are not retroactively described as tested.

All four protected main manuscripts (Prologue and Chapters I–III) were fetched from main and the branch and found to have **identical Git blob SHA at the time of this run**. No hard-canon edit, merge or deployment was performed.

## Self-adversarial editorial findings — not independent review

1. **Potential rhythm defect:** A long additional aftermath interrupts the two-semifinal-to-final escalation. Duckhook's choice must affect the thematic structure enough to earn its place; a shorter standalone companion may be preferable.
2. **Four-carrier exception:** A nine-scene composite with Jake, Austin, Zach and Phillip exceeds the Novel OS causal-chapter default of 1–3 primary POV carriers. Until an explicit architecture exception is approved, keep the V3 **reading collection** separate; do not silently label it Book One canon.
3. **Thematic overlap:** Both Phillip and Zach use preserved evidence of defeat to make a concrete choice. An independent editor should decide whether this echo deepens the volume or becomes repetition.
4. **World/chronology hypothesis:** Demonstration equipment, steward, hall, pupils, and tournament compound are fictional inventions. The "tomorrow" implication was removed to avoid asserting a one-day semifinal-to-final turnaround. No 2025 Atlas venue acceptance is claimed.
5. **Owner evidence:** Character association exists in hard fiction; it does not establish real-world private psychology, raw human-account ownership or historical appearance/equipment.
6. **Technical limitations:** Structural regression cannot establish prose excellence, dramatic necessity, or source-to-world spatial feasibility.

## Independent Umpire / Founder holds

**Independent Umpire/Author Council review: NOT ACCEPTED OR EXECUTED IN THIS RUN.** A PR comment requests actual review; never count the request as a verdict. Founder-only canon promotion, public release, irreversible action and external spend remain HOLD. A failed Netlify deploy-preview status was reported earlier on this PR; no successful preview was observed or asserted.

## Next continuation

1. Resolve independent story-structure feedback and the four-POV collection-vs-chapter gate; preserve V2 and V3 as separate candidates.
2. If V3 proves overlong, retain *The Line He Left Visible* as a standalone source-bound companion and keep the eight-scene V2 ordering.
3. Continue substantial source-cleared historical prose in an unblocked owner/event lane, not unsupported earlier slot-owner inferences.
4. Run current-code-head CI and record exact receipts after substantive changes; do not promote canon without authorization.
