# Schemin ’26 — Week 10 current production entrypoint

**Current state: all-six-sheet pre-generation audit executed; 34 source-bound full-folio inputs ready.**

Start with the [completed execution report](../production-evidence/recovery-20261116/COMPLETION_REPORT.md), then the [34-page input manifest](render-inputs/manifest.json). Earlier pass discussions and checkpoint holds remain historical records, not competing current render directions.

## Current authoring authority

- `issue-previs.json`: stable reading order, full scene/copy/cast contracts.
- `illustrated-page-briefs.json`: exact mirrored image and copy instructions.
- `storyboard-folio-plan-pass5.json`: reconciled full-folio proof ledger, not annotated-sketch instructions.
- `render-inputs/W10-Pxx/request.json`: each 1080×1920 page, complete copy, source-qualified facts and actual image paths/hashes.
- `character-world-packet.json`: recovered canonical crop bytes and current appearance overrides, with provenance.
- `storycards.json`, `director-sequences.json`, `landscape-set-bible-pass4.json`: synchronized current narrative, action and geography.

Opening Drive follows the published briefing-table/map/banner editorial composition. The rejected bridge-travel substitution is superseded. Both canonical 200-point characters appear on the cover. Individual full-page masters precede all sheet assembly.

## Verification

Run `python -m unittest -v test_render_contracts test_sheet_assembly` from this directory with Pillow installed. Twelve tests cover actual reference bytes, mirror equality, full copy, stable order, identity overrides, scoreboard pairings, provisional source scope, PNG geometry, grayscale and exact downstream compositing.

After individual page generation, run `assemble_review_sheets.py --masters <directory> --output <directory>`. It only scales existing complete page PNGs; it never invents or reinterprets scenes. No font files are distributed.

## Production boundaries

Sports are freshly checked but still provisional because the provider has not decided the matches. Proof generation and final publication are separate. No merge, release, real-person signoff or approval of nonexistent artwork is claimed.

The remaining publication-time work is event-dependent: refresh after provider finality, update all affected numbers and prose, and inspect actual generated output. Source recovery, published-art comparison, contract reconciliation, current-data audit and registered AI-role review have already been executed.
