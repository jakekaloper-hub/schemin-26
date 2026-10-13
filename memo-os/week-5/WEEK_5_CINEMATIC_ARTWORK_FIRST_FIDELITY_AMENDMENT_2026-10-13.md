# Week 5 — Commissioner Cinematic Visual Fidelity & Artwork-First Production Amendment

**Authority:** Commissioner binding directive, 2026-10-13. **Scope:** Existing Week 5 Memo OS, PR #152 and P001–P032; no new operating system. This amendment supersedes all conflicting Week 5 "PDF-first production," "assembled PDF is the deliverable," "vector/extractable text in PDF," "Bullpen PDF assembly," and "compressed physical pagination" language in earlier packets. Their history is retained as benchmark/proof-only documentation.

## 1. Contract correction: output per page, no assembled PDF

**Bullpen production output:** one complete, self-contained **1024 × 1536 pixel portrait PNG** per approved physical page, including cinematic illustration, branded masthead, page-specific headline, legible integrated narrative typography, verified visual results/graphics where applicable, and final framing. Use opaque PNG, sRGB-appropriate colors, numbered exact page identifiers, and provide a directly viewable individual artifact, not a PDF.

**Workflow:** authoritative scene/character/Atlas/manuscript sources → image/reference-conditioned illustration → deterministic text, scores, labels, graphics and branding overlaid on the image canvas → flattened final **PNG** → full-size and 390px phone render inspection → character/scene/fact/type QA → independent Umpire page acceptance → Commissioner receives numbered page image. **The Commissioner** will independently compile approved page images into a shareable PDF. Do not make a production PDF, export PDF pages, require fonts/text extraction from a PDF, or measure a PDF byte budget as Week 5 production deliverables.

**Internal composition:** intermediary image-only backgrounds, transparent text overlays and type layout files may be retained for revisions. They are **not** substitutes for the complete flattened PNG the Commissioner needs. Titles/captions/scoreboard names must be deterministic and visually proofed in the final raster rather than delegated to generative text hallucination. For 390px preview, scale the final image down and inspect; don't swap in an unrepresentative PDF preview.

**Physical-page budget:** keep **32 currently indexed source P001–P032** in sequence, with each source ID initially mapping to a separate finished PNG. A greater page count is permitted only after an explicitly approved amendment adding mapped source IDs; do not silently skip, merge, reduce or relocate an approved beat. 21-page compression is an obsolete experiment, not a target or ceiling.

## 2. Actual official Week 4 image benchmark — inspected evidence

Commissioner provided the official `Pro_Schemin_26_Week_4_Official_Memo(3).pdf`, 33 pages, inspected by PyMuPDF on 2026-10-13. **Source file SHA-256:** `1fc322a3eb0e8b43499ee4556c715ba4c00a8c388e7a92a904954a35f0482124`; **121,338,910 bytes**. The artifact is 33 pages, each a **single 1024 × 1536 rasterized page image**, placed in a logical 576 × 864 PDF page; **zero extractable text characters** on the pages. It is evidence of an image-page-first publication pipeline (its PDF metadata identifies deterministic raster-to-PDF assembly). The uploaded source PDF is a session attachment, **not claimed to be committed to this GitHub repository**.

**Qualitative visual benchmarks tied to real reference pages:**
- W4 **P1–P3**: edge-to-edge cinematic cover; vista with parchment-textured editorial column; scoreboards integrated over a detailed environment with divisional framing, inset character crops, clear result hierarchy.
- W4 **P4–P8**: dedicated prose-first overture, four-image GOTW journey, continuity of hill/castle/bridge, dramatically changing camera distance, foreground weapon impact and consistent character silhouettes. Frame compositions carry movement, geographic scale and final result visually.
- W4 **P9–P12**: swamp ecology and continuous wetland light/weather; narrative overture precedes visually progressive contest, with legible nested environment props.
- W4 **P13–P16**: resort/coast and golf environment, daylight/sunset variation, foreground props and changing character staging; payoff score panel is part of the illustrated scene.
- W4 **P17–P20**: cave/tavern, neon identity details, crowd/room props and distinct recurring character faces; escalating page-to-page interactions with different shots.
- W4 **P21–P24**: ornate Pitty's Book hall with atmospheric waterfalls, tickets, liability books, characters and layered green/gold financial displays; theatrical story and readable type rather than a flat receipt table.
- W4 **P25–P28**: changing skies and storm escalation, intimate domestic start then dynamic weather destruction; separate page compositions avoid monotonous repeated layouts.
- W4 **P29–P33**: illustrated three-division state-of-realm display; twelve-team power ranking hierarchy integrated into architecture; dedicated Pitty ledger, Week 5 promo and memorable Final Word with visual object continuity.

**Fidelity bar:** Week 5 should **meet or exceed** this actual issue's visual depth, lighting dynamics, sense of scale, continuity of owner identity, environmental diversity and integration of headlines/narrative/panels. Compare each candidate page to specific appropriate W4 page(s), not generic prompts. Assess at actual 1024×1536 size **and** 390px width. No quantitative computer-vision score alone certifies artistic equivalence.

## 3. Six locked cinematic settings

1. **Dark Wizard Chess** — P004–P007; temporary monumental chessboard within `LOC-COMPACT-NEUTRAL-GROUNDS`; one exactly three-headed serpent body and the actual Belt Keeper; no permanent capture of neutral ground.
2. **Save the Swamp** — P008–P011; `LOC-MUD-DOGS-SWAMP`; wetland household, bulldozers, partial local damage, Mud Dogs' emotional exit, bounded aftermath.
3. **A Storm Comes to Town** — P012–P015; `LOC-CHILI-STABLE`; Chile Outlaw's spoiled chili pot, Dark Horse and arriving El Niño weather; no sheriff.
4. **David vs Goliath** — P016–P019; `LOC-COUNTRY-CLUB-JACKSON`; true duck-faced Dr. Duckhook with fused-right-arm driver vs one **four-legged** gorilla/Arsenal centaur body.
5. **After the Storm** — P020–P023; `LOC-SLOB-FOOTHILL-CAMP`; rainy-dusk real Jeeps and genuine muddy foothills, no unapproved trucks.
6. **Champions' Joust** — P024–P027; `LOC-RED-RUINS`; temporary medieval tournament architecture, no belt on ObiWan Jacoby, original clever herald/crowd easter egg, no film-copied frames.

P001 Commissioner-locked cover: **The LLC. / Mike Ditka tribute, memorial first.** Keep. P030 Pitty's Book: leave betting fields empty until Commissioner provides actual data on 2026-10-14; match Week 4 P21–P24 for visual architecture and P31 for ledger legibility without inventing wagers.

## 4. Per-image qualification and refusal rules

For **owner-character imagery**, resolve the 12 distinct original Commissioner assets in `production-evidence/WEEK_5_CHARACTER_SOURCE_ASSET_RECEIPTS_2026-10-13.json`. Original raw SHA-256 and Git blob integrity have been separately verified for all 12. **Not yet verified:** the actual image generator's mounted reference bytes, each owner→rendered subject binding and pixel-level identity. Production cannot mark an owner page `READY_FOR_RENDER` or `LOCKED` without provider attachment/conditioning evidence and independent art QA. No fabricated renderer-mount certificate. If unavailable, test a compatible renderer under an isolated limited proof, with no mutation of canon or new provider fees by default.

For **environment-only composition tests** (no recognizable owner characters), a sandbox proof can proceed while owner reference conditioning is unresolved. Mark `VISUAL_PROOF_ONLY` and explicitly prevent `APPROVED_FINAL_PAGE`, `render_eligible` promotion or official distribution claims. Compare the actual rendered image, not a text description, to corresponding Week 4 reference pages before greenlighting a full page.

**Final image acceptance, in order:** (1) exact page ID & image dimensions; (2) approved story/verified facts and no unsupported winner-specific assertions; (3) correct owner-specific mounted references if owner visible; (4) correct anatomy, equipment & temporal canon; (5) correct Atlas venue/location transitions; (6) distinctive cinematic depth/composition vs relevant Week 4 exemplars; (7) final pixel-integrated brand/headline/body/score text legible at 390px; (8) cross-page visual and narrative continuity; (9) independent Umpire image-specific written QA and evidence receipt. Fail => repair/retest **that page**; no false-green release.

## 5. Bullpen role ownership

- **Closer / Clubhouse Manager:** maintain sole mission authority and page-level gate status; no simulated Director signoffs.
- **Visual Direction Lead:** image anatomy, cinematic storytelling, lens, light, texture, composition, W4 side-by-side fidelity checks.
- **Librarian / Atlas:** current exact character asset, SHA-256, scene-state, host geography and adjacent-page consistency.
- **Beat Writer / Author Council:** deliberate choice of narrative-to-visual division; no statistics disguised as dramatic prose.
- **Scout:** ESPN/NFL facts and winning POV; all six ESPN `winner` fields last seen `UNDECIDED`, so fantasy Fact Lock remains conditional.
- **Groundskeeper:** per-PNG typography compositing, 390px readability, correct file naming, preservation of original manuscript/layout source. **Not a Bullpen PDF assembler.**
- **Independent Umpire:** actual per-image acceptance with reviewer/session/evidence provenance; simulation must be labeled.

## 6. State / next operating action

**IMPLEMENTED:** binding controlling image-first requirements and authentic Week 4 benchmark read. **NOT YET CERTIFIED:** actual owner-reference-conditioned renderer, final accepted P001 art, independently accepted Week 5 page, winner-POV fantasy Fact Lock, Pitty receipts, final 32-page compilation (Commissioner-owned). PR #152 remains draft; no publication claims.

Begin with reference-safe, environment-only **P002 atmospheric composition** as a visual proof and compare visually against official W4 P2 (worldbuilding) and W4 P4/P9/P25 (editorial atmosphere). Then prove the real owner-specific reference mechanism with the P001 The LLC. asset before any final cover image. Continue true one-page-at-a-time acceptance after required gates, keeping artwork physically separate for Commissioner PDF compilation.
