# Week 7 — Three-PNG Independent Preflight

**Date:** 2026-10-27. **Scope:** P005–P007 source-bound composites committed as feb3b1c9. **Status:** EXPERIMENTAL ONLY / CINEMATIC ART HOLD.

## Actual artifact checks
- All three files exist, decode as PNG, and have 1024×1536 RGB image geometry.
- The existing receipt records embedded approved crop SHA256 values for TDS and Duckhook.
- Source-bound compositor used those exact crops in the SVG rasterization; no AI-generated character identity was substituted.
- Four acceptance tests (including prior P005 fail-closed gate tests) passed under standard unittest discovery.
- These files are compositing prototypes. They do not depict the fully authored, cinematic character interactions and physical staging required by the three separate original packets.
- The source-bound crop attachment in a local SVG is **not** a provider-side image generation attachment or subject-binding receipt.

## Umpire-style disposition
**PASS:** file existence, image geometry, source-bound local composition evidence, correct labeling as non-final.
**REJECT FOR FINAL ART:** generic composite does not satisfy the P005–P007 source-specific cinematic visual standard; no demonstrated scene-specific likeness preservation in a generative renderer; no real final-page 390px visual QA or typography.
**HOLD:** provider admission under `planning/render-adapter/provider_policy_v1.json`, actual two-subject binding and output provenance, Atlas acceptance and independent authenticated Umpire.

## Next engineering work
1. Inventory supported local/native/optional external image providers and their actual reference-image capabilities without silently spending credits.
2. Admit only providers returning independently corroborable attachment, subject-binding and output-lineage evidence. Do not weaken `renderer_capabilities.py` or `provider_attachment_receipt.py`.
3. Once provider is accepted, render P005 using the original exact packet, then P006 and P007 sequentially with character/Atlas/continuity review.
4. Record each provider's failed/passed evidence; if no provider meets the strict contract, retain a precise external capability hold rather than manufacture acceptance.

This is a source-grounded technical countercheck, not a separately authenticated Bullpen Umpire signature.
