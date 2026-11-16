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
