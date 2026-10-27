# Week 7 — Unified Editorial Layout and 390px Copyfit Preflight

**Status:** DETERMINISTIC DESIGN SPEC / NO RASTER QA / NOT ARTWORK. Derived from the actual Week 6 reviewed-PDF benchmark, not a claim of fresh inspection of PDF bytes. Week 6: 23 physical 2:3 portrait pages, image-only PDF, small dense text on several pages, repeated heavy headers, physical/printed folio mismatch.

## Four existing-compatible template families
1. **Cover (P001):** One restrained Schemin masthead, THE MIRACLE PUTT title, small week label and deterministic result strip. Dominant illustration with clear ball/cup/TDS heads and Duckhook recognition. Do not print narrative body over busy water.
2. **Cover Letter (P002):** Distinct letterhead and byline, single-column reading order, no sports result banner. Letter explains editorial purpose; Opening Drive dramatizes the week.
3. **Recurring departments (P003–P004, P023–P028):** Stable top rail, readable data tables, restrained rules, consistent labels. Standings and rankings require deterministic text and source receipts. Pittsy exact quote must be controlled typography.
4. **Matchup feature (P005–P022):** Consistent title, small matchup ID and deterministic result treatment; phase name is metadata, not automatically a huge Overture/Escalation/Payoff banner. Distinct POV, camera and text-safe region on each page.

## Layout tokens — candidate, not a new Memo OS
- Canvas: 2:3 portrait; physical 512×768 pt Week 6 reference, target illustration source 1024×1536.
- Safe margin: 5% on all edges, including bottom folio label.
- Masthead/title hierarchy: masthead, chapter title, small matchup metadata, body; avoid duplicate banners.
- Body type: use a deterministic editorial layer, not image-model lettering. Do not enforce a minimum tiny point size without phone-scale test.
- Score typography: controlled source fields, never invented into illustration.
- Printed folio: exactly one unique physical-page-to-folio mapping, P001–P028 candidate. Verify after any page split.
- Text accessibility: retain exact source copy in searchable/selectable PDF layer at assembly; avoid Week 6 all-image-only limitation.
- Visual rhythm: establish geography → change camera distance/axis → decisive payoff, rather than repeating hero portrait framing.

## Copyfit preflight (text-only, not visual proof)
| Page | Original words | Current candidate words | Decision |
|---|---:|---:|---|
| P005 | 278 | 137 | Art-led golf arrival; watercourse and character gear visualized |
| P006 | 254 | 138 | Competitive escalation readable in body language and props |
| P008 | 252 | 134 | Haunted atmosphere carried by shutters, lantern and wind |
| P011 | 247 | 132 | Unlit lightsaber and training ground communicated visually |
| P014 | 233 | 133 | Deer tracks and wetland ground conveyed by image |

These reductions are source-synchronized and pass word-count triage. **No actual 390px raster was generated or reviewed.** No final font or page-count lock is granted.

## Per-page acceptance gates
- All headings and body text legible at 390px display width.
- Character identity and full required anatomy visible.
- All numeric/quote text exact and deterministic.
- Clear foreground/midground/background, coherent action and Atlas geography.
- No repeated heavy banner treatment unless story-specific.
- Physical page count equals manifest; printed folio labels are correct.
- Umpire must review real output before READY_FOR_RENDER or LOCKED as appropriate.

**Next executable visual step:** render non-artwork deterministic layout proofs using current copy, then inspect at 390px; no final cinematic artwork authorized by this mission.
