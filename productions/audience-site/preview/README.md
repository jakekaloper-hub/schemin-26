# Commonwealth observer — existing-site integration

Private candidate, not a public release or visual approval. This ports the existing
regional-study host into the owning audience-site system; it does not replace the
World Engine, Atlas, publication model, or public catalog authority.

## Reproduce the existing site + observer

Python 3.12+ and Node 22; run from a complete repository checkout. Obtain
Three.js **0.187.0** with `npm pack three@0.187.0 --ignore-scripts` and put the
package's `build/three.core.js`, `build/three.module.js`, and `LICENSE` at
`preview/vendor/three.core.js`, `preview/vendor/three.module.js`, and
`preview/vendor/THREE-LICENSE.txt`. The builder rejects any hash mismatch.
The existing renderer-evidence workflow performs that preparation and preserves
the license, dependency receipts, exact source revision, and private build artifact.

```sh
python3 productions/audience-site/scripts/build-observer-site.py --output /tmp/commonwealth-preview
python3 -m http.server --directory /tmp/commonwealth-preview 8000
```

Open the existing site's **World preview** navigation entry. `observer.html` is
also self-contained and can be opened offline. The existing publication catalog
is built with its existing eligibility rules. No deployment is performed.

## Private artwork is opt-in, never inferred

The repository/CI build includes **zero original memo images**. It preserves all
23 source-defined location controls and does not promise unavailable stories.
The default deliberately ignores any mounted private-art folder.

A separately supplied private edition may be included locally only by explicitly
providing both arguments below. The compiler verifies every image hash and keeps
the source folios unchanged. Do not commit that asset folder or compiled output.

```sh
python3 productions/audience-site/preview/build_preview.py \
  --catalog /tmp/commonwealth-preview/observer-candidate.json \
  --output /tmp/commonwealth-private-edition.html \
  --private-editions --art /absolute/path/to/private-edition-art
```

## Verify

```sh
npm --prefix productions/audience-site test
node --test productions/audience-site/preview/tests/*.test.mjs
python3 -m unittest discover -s productions/audience-site/preview/tests -p 'test_*.py' -v
```

Renderer tests require the prepared vendor bytes. Existing catalog/Story Graph
and authority checks remain in their existing workflows. The renderer-evidence
workflow additionally builds the combined site twice, verifies byte-stable observer
HTML, and rejects private-image payloads or source-revision/date substitution.

## Optional real-WebGL2 first-frame and spectator-journey smoke

This extra regression catches browser-only Three.js/GLSL initialization failures
that source-level Node tests cannot detect. On a local machine with **Node 22+**
and installed Chrome (set `CHROME_BIN` if not in the macOS or Linux default
location), first build the **unpublished**, source-only observer as above, then:

```sh
node productions/audience-site/preview/tools/webgl2-journey-smoke.mjs /tmp/commonwealth-preview/observer.html
```

The script uses the built-in Node WebSocket with Chrome DevTools Protocol and
isolated temporary Chrome profile; it installs no browser dependency. It fails
closed on Canvas fallback, zero WebGL2 frames, missing Atlas sites, shader/runtime
errors, unexpected external requests, broken Jackson source-history return,
incorrect synthetic global calm, frozen ordinary water, or broken explicit pause.
It prints a single machine-readable `WEBGL2_JOURNEY_SMOKE_PASS` result with the
observed GPU. This is **opt-in device evidence**, not a GitHub Actions GPU test,
Founder-approved art, live-weather proof, public release, or hardware benchmark.

## Opt-in GPU candidate captures for visual inspection

After the unchanged offline observer build, add `--capture-dir` with a **new,
nonexistent** local directory to the physical-GPU smoke command:

```sh
node productions/audience-site/preview/tools/webgl2-journey-smoke.mjs \
  /tmp/commonwealth-preview/observer.html \
  --capture-dir /tmp/commonwealth-private-candidate-captures
```

Only after all first-frame, source-history/return, calm-water and explicit-pause
assertions pass does this emit four PNGs: unlabeled world and the three
**source-defined Southern Wetlands** site views (Jackson, Podium Shadow Waterfall
Temple and Mud Dogs Swamp). The JSON manifest records source revision, observed
physical GPU, location IDs, PNG pixel dimensions and SHA-256. Existing output
directories fail closed; evidence is never overwritten. Captures reproduce
*observed frames*, not deterministic water phases; do not compare PNG hashes
across reruns as a visual regression oracle.

An inspectable four-view **source-only** GPU sample is retained at
`evidence/gpu-southern-wetlands-20261121/`; its manifest pins the pre-change
observer source snapshot and per-image hashes. No image is wired into the site.

The screenshots are private, read-only **CANDIDATE_NOT_APPROVED** hardware
inspection evidence, not final artwork, independent art acceptance, canonical
geography, live weather, a published site, or publication authorization.

## Optional physical-GPU waterfall temporal evidence

For a separate, **new** output directory (never overwrites existing evidence),
the same standalone smoke also supports a mutually exclusive temporal mode:

```sh
node productions/audience-site/preview/tools/webgl2-journey-smoke.mjs \
  /tmp/commonwealth-preview/observer.html \
  --temporal-dir /tmp/commonwealth-temple-global-calm-frames
```

This retains the standard first-frame, 23-site, Jackson history/return,
source-integrity, synthetic El Niño global-calm and explicit-pause checks. It
then revisits the **existing** Podium Shadow Waterfall Temple source location
and captures two hardware-WebGL2 PNG frames from a settled, consistent camera
approximately one second apart while ordinary water time advances despite
global weather calm. Its source-revision-pinned manifest records individual
frame hashes, water times, actual GPU and source location.

The screenshots demonstrate **observed scene-frame differences**, not an
isolated pixel-level proof that only waterfall water changed; other candidate
scene animation may contribute. Synthetic calm is not a live weather reading.
This mode is optional engineering/art inspection evidence only, does not
change the observer's runtime, and does not confer Founder art acceptance,
performance certification, publication or deployment.

## Honest boundaries

The regional assets remain visualization candidates. The source's recorded
`as_of` is retained, not promoted to current world state. Shared-clock lighting
is illustrative; weather demonstrations use synthetic inputs, not a live feed.
Ordinary water movement is independent of global-calm weather; explicit pause
stops motion. The visitor has no avatar or authority over inhabitants or canon.

Historical reading, when privately supplied, suspends the camera and restores its
exact viewpoint. Public publication permission, final art acceptance, physical-
phone/hardware-GPU verification, independent review, merge and deployment remain
separate gates. This source port does not certify any of them.
