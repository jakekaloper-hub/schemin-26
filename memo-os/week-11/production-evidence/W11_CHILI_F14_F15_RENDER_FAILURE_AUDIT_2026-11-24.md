# Week 11 Chili / ObiWan — failed render handoff and repair gate
**Observed November 24, 2026. Status: REJECTED working candidates; NOT publication masters.**

## Decision and scope
Jake explicitly rejected the Week 11 P15 production image for loss of established manuscript/transcripting and the established illustrated-memo workflow. P14 also remains a provisional candidate, not an accepted folio. This is a production/render/QA error, **not** evidence the existing Week 11 manuscript or folio planning is missing. Do not generate the next page automatically. Jake gives page-by-page art direction. User's "no folio references" rule prohibits visible F14/P14 identifiers on the printed artwork; it does NOT prohibit titles, masthead, byline, screenplay-derived narration, dialogue, or verified scores.

## Exact evidence reviewed
- Source narrative: [Nov 24 selected director's cut](../preproduction/W11_RESULT_LOCKED_SIX_STORYLINES_DIRECTORS_CUT_2026-11-24.md#G03).
- Print lettering: [F14–F16](../preproduction/W11_READER_LETTERING_2026-11-24.md).
- Commissions: [F14, F15, F16](../preproduction/OPEN_BOARD_PAGE_REHEARSAL.md#folio-14).
- Production camera and phone specs: [35-shot register](../preproduction/W11_ALL_35_VISUAL_DIRECTOR_SHOT_SPECS_2026-11-23.md).
- Comparator: Week 10 exact-source `W10-P05/P06/P07/request.json` at GitHub commit `6ece345f5791d21684dedb902cb356084d84b40e` requires integrated complete headline/deck/body, source-qualified typography, approved references, 390px proof, and no page-number labels.
- Governing hardening: `memo-os/SCHEMIN_26_WEEKLY_MEMO_OS_V5_5_INTEGRATED_PREPRODUCTION_PATCH.md` sections on per-page complete-issue previs, actual raster QA and iteration.
- Closer's existing production routing: [direction](W11_CLOSER_PRODUCTION_DIRECTION_2026-11-24.md); no new production lead or duplicate PR created.

## Local candidate observations
Two generated image files were inspected as actual raster files (not as accepted output in the repository):
| Candidate | Local source filename | Measured pixels | SHA-256 | Finding |
|---|---|---|---|---|
| F14 | `off_the_board_at_the_rainy_carnival.png` | 941 × 1672 | `c11528e404c83a46632a45f187c684e0da0f1e5106d5d3f348f83d870fe80713` | Some title, deck, body and notice present; still below production target and not identity/atlas/phone accepted |
| F15 | `a_cinematic_hyper_realistic_highly_detailed_rain.png` | 941 × 1671 | `9bf433558a2b4a0303cfe9c5feceae3dbb1300041f377e452e35d120574e9c62` | Standalone scene image with no title, matchup line, approved narrative/dialogue or masthead; throws/target/hinge causality not verifiably clear; below production target |
The local files are NOT represented as durable repository masters and are not blessed by this receipt.

## Failure mechanism (observed)
1. Operator skipped generation of a per-page **exact publication-copy + design + identity + source + QA** render request, despite Week 10's working pattern.
2. A very short visual-only image description was sent to the image renderer. It omitted the source reader lettering and the performance manuscript.
3. The actual preferred October 22 Brandon "Chili Outlaw" image is approved in semantic authority but missing at its registered repository target; exact renderer bindings for both protagonists and approved cinematic venue plate were still unresolved.
4. Result not checked for target 1080 × 1920 native resolution, 390 × 693 mobile readability, exact lettering, character identity, tank mechanism or continuity before being shown as an apparent deliverable.
5. The absence of *visible production page IDs* was incorrectly conflated with an absence of editorial typography.

## Restoration contract — apply to every folio, begin with F15
- **Beat Writer / production design:** compile exact reader lettering (title, full franchise matchup line, approved narration and dialogue, source facts) from the Nov 24 source. The director's cut governs additional performance/camera action; any additional printable prose derived from it is an editorial change, not a silent rewrite. F15 reader copy: `The Chili Cheesers at ObiWan Jacoby`; `From the Wolf Brand Chili seat Jake called, “Safest place to stand is right behind the target.” Brandon turned the ball in his hand. “Sit tight.” One throw. The seat dropped.` Include the displayed title `The Safest Seat` and issue's appropriate masthead.
- **Production / camera:** low, clear ball → painted target → hinged seat → tank sightline; ONE unaided Brandon throw; Jake is the sole person submerged, with a visible palm and face behind the window, in thick red-brown Wolf Brand Chili NO BEANS, not rainwater. Retain the P14 rainy carnival's approved components and this scene's exact Eastern Ascent venue handle.
- **Character / Librarian:** use actual authenticated current reference bytes and renderer subject bindings, especially Brandon's Commissioner-preferred Oct 22 override; do not certify identity from prose-only substitutes. Jake: Trade Jedi, no title belt. Brandon: human Chili Outlaw, decorated black cowboy hat and crimson coat. Never invent render reference provenance.
- **Designer / compositor:** follow the Week 10 integrated printed-page contract, not a film still or separate poster; set exact names, dialogue and prose with deterministic typography when needed. No visible production identifiers, slug, folio number, placeholder, debug label or PDF framing.
- **GM / Umpire / QA:** inspect actual native 1080 × 1920 PNG, downsampled 390 × 693 proof and continuity against F14/F16 and Week 10 published precedent. Save both rasters with source hash, copy/text review, identity and venue review, corrections and separate acceptance decision. Image dimensions and phone proof are hard gates. Never count the present F14/F15 as final, nor infer steward/Commissioner approval.

**Exit:** Only resume P15 generation on Jake's new instruction. Closer owns queue, Setup Man coordinates, named production disciplines retain their commissioned roles. No publication lock, Fact Lock, visual acceptance or GitHub release is asserted.
