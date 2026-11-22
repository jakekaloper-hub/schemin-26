# Week 10 — 30-minute film storyboard

**State:** drafted and source-validated storyboard; **not** an approved screenplay, character render, image/video master or release.

## Open the visual storyboard

Open `storyboard_viewer.html` in your browser from this repository checkout. It includes **all 34 original folios in their controlling reading order, 186 shot-panel layout diagrams, original source narration, camera blocking, movement, timecodes, reference-image thumbnails when locally available, and location/audio continuity notes**. Expand each scene to inspect its panels. **Diagrams are explicitly illustrative blocking schematics, not generated frames.**

Read `PRODUCTION_BIBLE.md` for the 30-minute act structure, specialist/Inklings methodology workshop, inherited Bullpen Director ownership, film-production requirements, license/compute constraints and release gates.

Inspect `METHOD_LENS_RECONCILIATION.json` for the mechanically validated simulated advisory pass. The three held method challenges are stunts, compositing/VFX, and sound rights/separate stem implementation. The review does **not** claim actual participation by the named professionals or external author figures.

## Regenerate and audit

Run from any directory in a full `schemin-26` checkout:

```bash
python3 memo-os/week-10/film-30m/build_storyboard.py
python3 memo-os/week-10/film-30m/render_viewer.py
python3 memo-os/week-10/film-30m/reconcile_method_lenses.py
python3 memo-os/week-10/film-30m/build_handoff.py
python3 memo-os/week-10/film-30m/validate_board.py
```

The generator enforces original request SHA-256 hashes, 34-page source order, 66 source camera beats and exact 1,800-second target. It makes no model inference requests and incurs no GPU charges.

## Canon and chronology

The source remains the 34-folio final Week 10 Memo OS preproduction package on `memo-week10-preproduction-20261116` (PR #315), with W10-P32 omitted and W10-P34 at reading position 19. The new film board lives in a separate proposal branch and does not rewrite existing folio requests, source facts, P01 art direction or page approval states.

Source references are inherited, not implicitly verified as publicly distributable character images. Original folios have a **1080×1920 portrait design**; the film's proposed **16:9 at 1920×1080** requires separate per-shot reblocking. Performance, casting, audio, frame QA, rights and actual final film rendering remain future production gates.

## Prior hosted inference proof (not source artwork)

The isolated Week 10 bridge proof in the Mac desktop folder `Week_10_Film_Proof_2026-11-22` verified two short Wan 2.2 clips, two audio samples and a 14.25-second mixed test cut. It had two unique shots reused for export testing and hit the Hugging Face free ZeroGPU limit; it is **not** counted among the approved source imagery or 186 completed moving shots.

## File manifest

- `film_storyboard_v1.json` — full 30-minute scene and shot source ledger
- `storyboard_viewer.html` — offline storyboard display, 186 schematic shot panels
- `build_storyboard.py`, `render_viewer.py` — deterministic generators
- `METHOD_LENS_WORKSHOP_INPUT.json`, `METHOD_LENS_RECONCILIATION.json` — 8 author lenses + 12 production lenses; modelled, validated and **independent Umpire pending**
- `reconcile_method_lenses.py` — use existing Inklings reconciliation contract
- `PRODUCTION_BIBLE.md` — story, scene budget, team routing, audio and post gates
- `SHOT_DELIVERY_REGISTER.json` — shot deliverables, available references and status (generated separately)
- `AUDIO_AND_PERFORMANCE_PLAN.md` — soundtrack/ADR needs and scene-local sound cues
- `validate_board.py` — reproducible integrity check

**Owner/authority:** Beat Writer + Memo OS proposes; Bullpen router and counterweights, Atlas/Character, independent Umpire, Closer and Founder must approve appropriate gates. No exact real-person consult, release or storyboard sign-off is implied.
## November 22 continuation — executed screenplay and moving proof

- **Screenplay:** `SCREENPLAY_CANDIDATE_V1.md` and `.json`: 34 scenes, exact original 30-minute picture clock, 24 provisional fictional (not real league owner) dialogue lines, film VO and 186 shot directions. Source publication copy is preserved in the JSON. Script requires independent editorial and performance approvals.
- **Actual local 20-lens reviews:** `LOCAL_MODEL_20_LENS_INPUT.json`, `LOCAL_MODEL_20_LENS_RAW.jsonl`, `LOCAL_MODEL_20_LENS_RECONCILIATION.json`, `SCREENPLAY_REVIEW_DECISIONS.md`. Twenty actual local Qwen3 inference calls used eight registered Inklings method domains and twelve filmmaking method domains, **without contacting those real individuals**. Editorial counterweight rejected unsupported new canon; the Umpire is still pending.
- **Visual M01 motion:** `proofs/M01_RODEO_STUNT_PREVIS/W10_M01_Rodeo_Blocking_Proof_with_TEMP_DX.mp4` (42s at 960×540, 12fps, 2D schematic only) and frame 22 check. No claim of cinematic or canonical character likeness. A corrected rear-left gate and a demonstrable torso lasso path were visually checked; manual tying/physics remains a HOLD.
- **Sound post:** Five independently exported 48kHz/24-bit PCM stems (DX, VO, FX, AMB, MX), temporary local system TTS auditions, original procedural ambient and effects. Stem WAVs and raw takes are kept in the local Mac review package, not in Git. `M01_MOVING_PROOF_RECEIPT.json` holds SHA-256 and media probes.
- **Source data:** `FILM_GRAPHICS_SOURCE_V1.json` preserves 15 fact-heavy pages' publication copy for future native typography, not generated as an image.
- **Proof:** `NEXT_PHASE_STATIC_QA.json` and `NEXT_PHASE_EXECUTION_REPORT.md`. Bullpen's canonical command router really ran and produced `BULLPEN_MISSION_ROUTING_V1.json`, but independent Director/worker, Umpire and real human consultant signoff has **not** occurred.

This is a completed *preproduction continuation*, **not a finished 30-minute motion picture**. Source 34-folio memo, record results, and reader publication states remain untouched.
