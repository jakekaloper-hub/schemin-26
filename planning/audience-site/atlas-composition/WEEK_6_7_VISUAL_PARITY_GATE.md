# Commonwealth Audience Site — Week 6/7 Visual Parity Gate

**Date:** 2026-10-28  
**Status:** VISUAL PRODUCTION SPECIFICATION / NOT ARTWORK / NOT FOUNDER ACCEPTANCE  
**Owner:** existing audience-site PR #237; no parallel map or world authority.

## Controlling creative benchmark

The website artwork should be at least as finished, cinematic and geographically legible as the published Week 6 and Week 7 memo illustrations, especially their Commonwealth Atlas/world-map spreads. This is a **visual quality comparison** and never permission to lift inconsistent placement, labels, property boundaries or character likenesses from an illustration.

Before accepting any new site panorama, obtain the **actual** Week 6 map image (PDF physical p.5, `THE COMMONWEALTH ATLAS`; and physical p.23 `FINAL WORD`) from the exact issue matching SHA-256 `1d9b1b6915bf4b757a927c33719ab1cbd9f8f8eb93523e8103d3d8e2bd1a61c8`, and the corresponding exact Week 7 map image(s) from accepted Week 7 source artwork. The Week 7 final issue and page identifiers must be established from the source, **not guessed**. Maintain visually inspectable reference crops and source hashes in the review packet. The Week 6 benchmark narrative exists in `memo-os/creative-dna/WEEK_6_2026_REVIEWED_ISSUE_VISUAL_BENCHMARK.md` on current main. This document is not substitute pixel evidence.

## Atlas: dual-layer deliverable

1. **Production painting (visual layer):** cohesive illustrated landscape with intentional lighting, terrain depth, landmarks, hydrology, atmospheric perspective, texture, cinematic storytelling and regional distinction; no floating rectangular region blocks, anonymous dots or unfinished technical wireframe in the audience-facing overview.
2. **Deterministic overlay (functional layer):** 23 governed location anchors, 18 ordered registered routes, seven regions, readable region/place names, hover/focus/click targets, route provenance and mobile discoverability. Paint must never reposition underlying canonical anchors. The overlay must remain legible with the painting unavailable or images disabled.

The finished map is an authored **single coherent composition** constrained by `world/production/CANONICAL_WORLD_PLATE_SPATIAL_BLUEPRINT_V1.md`, its 2000×1400 planning guide, `ANCHOR_MATRIX.json` and source records; the guide SVG is only a positional underlay, never finished art.

Preserve Northern Spine high north, western dry tablelands, eastern storm/forest coast, central civic basin, southern wetlands, inner sea littoral; honor watersheds, 23 positions, all 18 routes and settlement context. Coordinates are schemin-local non-metric: no invented coastline precision, acreage, distance, elevation or property claim. Avoid duplicate landmarks, erroneous venue transfers and isolated owner kingdoms.

## Website production standards

- **Home:** authored hero composition should deliver the memo's cinematic sense of scale and scene depth; not a plain masthead above empty content.
- **Atlas + seven regions + 23 destinations:** each requires grounded environmental character and visual hierarchy, with map positions/biomes aligned; no generic fantasy stock art.
- **Twelve character profiles:** character-bearing imagery requires canonical reference assets and identity/morphology gate; decorative environment art does not imply character approval.
- **Six memo/issue views and Library:** use approved original covers as immutable edition artwork; web framing and reader presentation should match the illustrated editorial quality without replacing original content.
- **Responsive:** inspect desktop, tablet and 390px phone at both hero and map scale; include readable named location controls without pinch-only interaction.
- **Accessibility:** overlays remain keyboard operable, contrast readable over light/dark terrain, alternate text states context, reduced-motion supported.

## Mandatory artwork acceptance evidence

A composition is `GENERATED` only when bytes exist, `SOURCE_REVIEWED` only after source/Atlas/character cross-check, `INTEGRATED` only when rendered by the actual site, and `BROWSER_VERIFIED` only with desktop/mobile screenshots. None implies `FOUNDER_ACCEPTED`.

Required side-by-side sheet: Week 6 p.5 / p.23 actual images; actual Week 7 Atlas image(s); new website full Atlas at desktop; same at 390px; region closeup; label/route overlay. Evaluate:
- cinematic finish, legibility, artistic consistency;
- seven-region environmental distinctions;
- exact count/placement and semantic accuracy of 23 anchors and 18 route chains;
- recognizable source landmarks and no invented physical geography;
- tap/focus usability and labels at 390px;
- fidelity to the actual week artwork without mechanically copying its editorial layout.

**Stop conditions:** unresolved source images, nonmatching location/route/biome, mismatched character imagery, overlap/hidden labels, artwork only mounted as a masthead, broken mobile map interaction, absent browser proof, or unrecorded Founder acceptance. Each blocks final visual release; they do not block independent non-visual website fixes.

## Next implementation batch on PR #237

1. Source-hash retrieve actual Week 6 and Week 7 map PNGs and issue/folio metadata; create comparison proof.
2. Commission one whole-world **coordinated positional illustration**, using canonical guide for composition; review all 23 anchors and seven regions before integration.
3. Composite painting **under** the existing interactive map; retain deterministic SVG/HTML overlay and allow no positional interpolation based on generated pixels.
4. Verify desktop and 390px map interactions, then iterate artwork until visual parity is independently reviewed; Founder decides final visual acceptance.
5. Only then scale the approved pipeline to 7 region scenes, 23 destinations and other site route families.

**Explicitly not complete:** this gate is an actionable quality contract, not a generated map or a claim that Week 6/7 source images were mounted, tested or visually matched.
