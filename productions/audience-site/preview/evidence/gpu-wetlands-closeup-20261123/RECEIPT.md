# Physical-GPU Southern Wetlands closer perspectives — November 23, 2026

**Status:** `CANDIDATE_NOT_APPROVED` · unmerged · unpublished · no spectator deployment.

## Actual produced assets

- **12 new physical-device PNGs**, 1440 × 813, for the existing Country Club of Jackson, Podium Shadow Waterfall Temple and Mud Dogs Swamp locations. Each sequence is **two moving + two paused** frames. Companion `inspection.html` presents the four frames for each site; `manifest.json` pins every PNG SHA-256, camera, source revision, device and place ID.
- Rendered on the actual **Apple M3 Pro**, Chrome ANGLE Metal, with preferred `three-webgl2` from the unpublished observer source at exact Git parent `fb7a0091af71912e616fffb840c9deb6da1cb3b2`. This evidence does not claim the later artifact-only commit was rendered.
- Through Chrome's `Input.dispatchMouseEvent` mouse-wheel event, each real spectator camera approached its selected source location. Distances: Jackson **60.84 → 43.81**, Temple **51.80 → 37.30**, Mud Dogs **53.31 → 38.38** (approximately 28% closer). Source camera targets, yaw and pitch stayed unchanged; camera remained held through moving and paused capture comparisons. The canvas/event path was used, not a direct state mutation.
- The existing no-login first-frame journey independently observed **23 current source locations**, Jackson's recorded history and exact-view return, whole-world return, a recorded end-of-Week-3 World State, El Niño loss → synthetic `GLOBAL_CALM`, ordinary water time advancing in calm, historical replay freeze, explicit pause, original catalog unchanged, **zero console/runtime errors and zero external network requests**.
- **All three** moving-frame pairs changed SHA-256, while all three paused pairs were byte-identical. All **12** persisted screenshot hashes were independently recalculated and matched `manifest.json`. The source-only observer generated at that exact revision had SHA-256 `f6a968d628c1115b625f717b76a2a11c1498420dd2ee1e214a3ae0d41099c833`, containing **zero original memo JPEGs** and `publicationAuthorized=false`.

## Verification boundaries

This is **closer *whole-scene* temporal evidence**, not isolated, pixel-attributed river/waterfall displacement proof; nearby foliage/ambient scene motion may contribute to moving-frame changes. The visual forms are still noticeably stylized/low-poly, not validated hyperrealism, final founder art, or independently approved production design. The weather scenario is synthetic and not a current league/weather feed. All source Atlas coordinates, identities, topology, history, shared Eastern clock, water/weather rules, access, historical replay and authorizations remain controlled by unchanged application sources.

The new `--wetlands-closeup-dir` mode is optional, creates a **new nonexistent evidence destination only**, and fails closed on unavailable GPU, camera zoom, changed/paused sequence mismatches, canonical source mutation or browser errors. It does not modify the original `--wetlands-temporal-dir` flow. No third-party AI credits, new paid service, principal-character generation, new OS, credentials, canonical writeback, merge, deployment, independent Tim Veil/Umpire consultation or automation changes were involved.

Reproduce from the same source-built `observer.html` after the pinned Three.js 0.187.0 offline vendoring:

```sh
node productions/audience-site/preview/tools/webgl2-journey-smoke.mjs /absolute/path/to/unpublished/observer.html --wetlands-closeup-dir /new/nonexistent/evidence/output
```

Test suite: `node --test productions/audience-site/preview/tests/*.test.mjs`, `npm --prefix productions/audience-site test`, and `python3 -m unittest discover -s productions/audience-site/preview/tests -p 'test_*.py'`. CI status is recorded separately against the **final pushed commit**; no earlier run's CI proves a future commit.
