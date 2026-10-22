# Frank Masi unit-stills integration — evidence and release hold (2026-10-21)

**PR:** https://github.com/jakekaloper-hub/schemin-26/pull/227
**Verified head before this evidence-only commit:** `cae215a0b6c246992845c7df5455622965513f61`.
**Status:** CODE AND CI PASS ON VERIFIED HEAD / INDEPENDENT VISUAL QA HOLD / NOT ACTIVE / NO MERGE.

## Executed

- Added a documented Frank Masi unit-stills reference with separation of cited professional practice from project-derived photographic heuristics.
- Created optional Tier-1 validation and metadata forwarding in `living-novel/os/adapters/comfyui_adapter.py`.
- Added `living-novel/os/adapters/test_frank_masi_unit_stills.py` and a dedicated execution step in `.github/workflows/novel-os-ci.yml`.
- Kept legacy jobs valid when no unit-stills review is present. The new review does not relax reference, object, character, Atlas or QA controls.
- Repaired two escaped-newline syntax issues revealed by CI, plus malformed workflow YAML. Failure investigation produced real corrective commits, not presumed green.

## Verified CI on head cae215a

GitHub Actions reported **completed/success**:
- Novel OS CI (including new unit-stills tests)
- Schemin Project Mission CI
- Cross-Domain Authority CI
- Weekly Memo Authority CI
- Bullpen Runtime CI
- Repository Merge Gate

These prove the configured automated suites ran successfully; they do not prove visual quality, live model binding, or independent acceptance.

## Explicit hold conditions

1. **Netlify:** deploy preview `6ad9096447528bd547db00b0` failed: `Deploy directory 'novel/book' does not exist`. Deployment configuration is outside this photography patch; no silent Netlify correction authorized.
2. **Memo OS:** its live Page Design Packet producer has not yet been changed to automatically hydrate the optional review; documentation and guidance are not runtime routing proof.
3. **Real A/B rendering:** no comparable, renderer-produced before/after assets, reference/mount evidence, measured scores or approval receipts have been produced.
4. **Character control:** previously stated character-binding and source-byte holds remain in force; avoid character-bearing 'test' art until exact references are available and approved.
5. **Independent Umpire:** no independently recorded approval was obtained.

## Next legal acceptance sequence

Resolve Memo OS wiring against owning V5.5 packet generator without changing its published authority or historical memo; add deterministic routing tests; capture eligible approved environmental/still-image A/B render pairs (character-free if character gates unresolved); independently review Atlas, optical composition, typography and continuity; reconcile Netlify configuration under its own owner; require Umpire acceptance; rerun all affected CI; only then consider merging.

**No false green.** This report documents execution and remaining evidence requirements, not a production activation receipt.
