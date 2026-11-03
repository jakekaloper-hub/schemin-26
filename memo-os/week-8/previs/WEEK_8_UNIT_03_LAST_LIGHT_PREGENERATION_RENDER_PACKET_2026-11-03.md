# Week 8 — Unit 03: The Last Light, Part I — Render Preflight

**Status: SOURCE-RECONCILED / CHARACTER RENDER INPUTS NOT YET MOUNT-PROVEN / NOT FINAL-RENDER RELEASED.**
**Working unit:** 03 of 20; generation order G1-02. **Canvas:** 1080 × 1920 PNG (9:16), x=90..990 and y=140..1760 provisional type safe zone. **Issue design authority:** Published 31-page Week 7 Official Memo, then Memo OS V5.2-RC and current Founder directives. **PR:** #272, branch `week8-storyboard-dependency-gate-20261102`.

## 1. Exact source contracts

- Scene: `memo-os/week-8/previs/WEEK_8_29_COMPOSITION_PACKETS_2026-11-02.json`, **W08-10-01** and **W08-10-02**. Both remain `qa: NOT RUN`.
- Manuscript: `memo-os/week-8/WEEK_8_SESSION_E_29_SCENE_MANUSCRIPT_DRAFT_2026-11-03.md`, same two identifiers. **DRAFT_NEEDS_EDITORIAL_COPYFIT**; not an approved final copy lock.
- Supporting interpretation: `memo-os/week-8/WEEK_8_THE_LAST_LIGHT_FULL_PREPRODUCTION_BENCHMARK_2026-11-02.md`.
- Parent Atlas setting: **LOC-MUD-DOGS-SWAMP**, Southern Wetlands, **PERMANENT_CANON**. “Blackwater Cut” is a proposed named subsite, **NOT ADMITTED**, so do not print it as geographic canon.
- ESPN outcome is provider-decided: Duckhook 174.06, Mud Dogs 100.88; this first page **does not reveal the result**. Player scoring breakdown remains unverified.

## 2. Source asset authority and binding receipts

| Subject | Owner / ID | Approved commissioner lineup crop (visual baseline; not primary supersession) | SHA-256 (recomputed on authorized Mac) | Primary historical source | Renderer mount |
|---|---|---|---|---|---|
| Mud Dogs | Bobby Mitchell / `CHAR-BOBBY-MITCHELL` | `canon/characters/assets/lineups/2026-10-18-crops/CHAR-BOBBY-MITCHELL.png` | `d88f6ffdde967d0dee2ec350f0d9314f2e8b4da4dd9b8d8d1890bc28d6fae736` | `17E68E6F-7825-460F-A612-734BE1E2A543.jpeg`; approved historical expected SHA `4ad8693d7f155f2ee99722f87eb74ea99490eebdfe0b30ca2f17f05004e7cf12`; registered native handle `file_00000000b0f081f585aae4372c880d72` | **NOT PROVEN** |
| Dr. Duckhook | Zach Wilson / `CHAR-ZACH-WILSON` | `canon/characters/assets/lineups/2026-10-18-crops/CHAR-ZACH-WILSON.png` | `c0ac1b3314c32b8e85c82045268c21a0d9c52525c2fd8ad869aaff449b4cf36a` | `5B8C182F-FEBF-40A3-8DDA-1B4B62386B10.jpeg`; approved historical expected SHA `c8124a1f1146c0acc65b5e82d1c21289afd6a74a8ac2046895e39794619dcefb`; registered native handle `file_00000000684c81f88ac9e7373dbf8479` | **NOT PROVEN** |

**Actual verification done on 2026-11-03:** Both lineup crop PNG bytes exist in GitHub and on the authorized Mac checkout, and the Mac-recomputed crop SHA-256 matches the Commissioner-approved October 18 lineup registry. Both PNG crops were visually opened and inspected. Exact historical PRIMARY JPEG paths return GitHub 404 and are absent from the checked local repo; prior first-party Library IDs exist in the manifest, but direct raw-byte materialization was refused in this session. **This is not a successful renderer subject-mount receipt.** A checksum of a derived crop does not turn it into a new primary-reference supersession.

**Binding gate:** When generation is authorized, supply the actual approved source images as real image inputs (the exact registered native Library handles if resolvable by the generation route, or approved byte-backed references if that route supports them). The generation request must include both subjects. The renderer's response or audited submission must prove both references were passed. Text prompts mentioning the characters, Git SHA strings, or source paths alone do **NOT** meet this gate. If references cannot be mounted, do not generate character-bearing artwork.

**Character identity checks:**
- Mud Dogs: one huge four-legged rabid swamp dog/wolf, mud and moss-caked, wet matted fur, chain/collar, diseased teeth, blue/orange marking permitted by older master canon. NEVER a man, human hunter, ordinary dog, leopard, armor soldier, or other species.
- Duckhook: upright anthropomorphic white duck golfer, orange bill, country-club attire, conspicuous golf equipment. NEVER human, generic duck, doctor, or substitute mascot.
- **Headwear conflict resolution gate:** Master character prose / older preproduction benchmark mention a camouflage/floral bucket hat, while the October 18 Commissioner-approved visual lineup and published Week 7 page 11 visibly portray a **green golf cap**. Do not mix two generations of design. For a Week 7-matched visible appearance, use the newer visually approved cap; if the exact current primary source proves a Commissioner-superseding bucket design, reconcile through the existing character authority before rendering. No free-form invented headwear.
- The Week 7 original art depicts the characters in distinct scenes; it is **a style/appearance comparator**, not an automatic primary asset promotion.

## 3. Visually inspected published Week 7 benchmark

Authorized Mac source: `~/Desktop/Desktop - Jake’s MacBook Pro/Fantasy Football/Pro Schemin'/2026 Memos/Weeks/official/Schemin_26_Official_Week_7_Memo.pdf` (31 pages). Actual pages **11** (Duckhook feature) and **20** (Mud Dogs swamp feature) rendered and visually inspected on 2026-11-03 using PDFKit, 720×1080 review rasters at `/tmp/schemin_week7_benchmark_p11.png` and `/tmp/schemin_week7_benchmark_p20.png`.

Carry forward: premium lifelike character depiction; believable inhabited, physically coherent Southern Wetlands; quiet ornate masthead / versus banner; carefully silhouetted principal subjects; luminous weather/light; powerful editorial serif display; compact legible two-column narrative at the bottom. Improve: do NOT copy an identical page composition or reuse a fixed split-screen; more cinematic waterline camera discovery, a clearer environment-first overture and wider typographic breathing room. Week 7 was 2:3; adapt its craft to new 9:16 without stretching.

## 4. Composition to render after mount-gate

**Title:** `THE LAST LIGHT` — Part I.

**Frame A: discover geography.** Low waterline 9:16 scene skims a dark swamp channel with submerged roots, suspended humidity, late copper light, coherent cypress canopy and natural dusk shadows. Do not add map labels, legends, territory colors, novel settlements, unexplained boats, or invented permanent damage.

**Frame B: find both subjects in one inhabitable space.** Mud Dogs occupies raised ground across/along a coherent bank at left/midground; not floating, standing upright, or clipping through water. Duckhook is visible across the same navigable watercourse at the opposite approach, physically proportioned, golf attire and equipment clearly recognizable. Give equal POV *narrative importance*, without two isolated cutout portraits.

**Frame C: cue the pursuit.** Muddy marks and a surface disturbance in the scene foreground logically point toward the narrowing channel and the page-04 sequence; avoid false battle damage, inappropriate weaponry, or impossible routing.

**Lighting/texture:** Warm dying orange reflections against blue-black twilight, detailed wet fur, duck feathers, muddy roots and chain metal. Maintain readable silhouettes; no oversaturated fantasy colors or generic AI effects. Distinct visual rhythm from published Week 7 layout while matching publication-grade craftsmanship.

**Suggested page geometry (provisional, must be tested on actual raster):**
- 140–220: brand / compact encounter title strip with Mud Dogs and Duckhook, genuine identity artwork if used.
- 220–1160: uninterrupted environment-led cinematic illustration.
- 1170–1360: feature serif headline placed over a deliberately quiet region.
- 1380–1710: exact two-paragraph copy in balanced two columns, safe x90..990. No AI-produced lettering in the image plate; overlay deterministic typography.
- No score receipt on this opening page. Keep all printed text within the established safe zone; do not force an infeasible font size.

## 5. Verbatim provisional manuscript content (not final locked copy)

**W08-10-01:**

> The swamp held the last copper of the evening on its surface. Along the raised ground, Mud Dogs waited with wet fur and a heavy chain, the immense beast nearly indistinguishable from the dark earth until he moved. Across the channel, Dr. Duckhook's white feathers and unlikely golf attire marked a figure who seemed spectacularly out of place. The water between them was quiet, but not empty.

**W08-10-02:**

> The first disturbance could have been mistaken for a branch falling into the water. Then another mark appeared along the wet edge of the channel, and the hunt became specific. Mud Dogs followed what the ground would tell him. Duckhook advanced with the awkward determination of someone whose equipment had been designed for an entirely different kind of course.

**Copy rule:** Above are EXACT from source Section E. Do not insert an invented quote, headline blurb, score, or description as official copy. Copy may be professionally line-edited only with a separately recorded source revision. All typography must be checked on an actual output at phone reading size.

## 6. Go/no-go checks

- [x] Scene IDs and manuscript passage matched to 29-packet Week 8 source.
- [x] Approved October 18 presentation crops found, visually inspected, and SHA verified on authorized Mac.
- [x] Actual Week 7 pages 11 and 20 inspected as visual comparators (not full independent visual QA).
- [x] Parent swamp location established; tentative subsite held provisional.
- [ ] Actual historical primary source bytes reverified **or** accepted native handle attached to generator with proof; both subject bindings not yet demonstrated.
- [ ] Duckhook hat/wardrobe appearance compared against actual conditioned source output.
- [ ] Actual 1080×1920 raster proof with no generated text and deterministic copy overlay.
- [ ] Copyfit legibility, pixel dimensions, character identity, source-copy accuracy and atlas continuity inspection.
- [ ] Authenticated Umpire/Founder acceptance.

**DISPOSITION:** READY AS A SOURCE-GROUNDED PRE-GENERATION BRIEF, **NOT** an approved final PNG, character-binding pass, independent QA, or release authorization.
