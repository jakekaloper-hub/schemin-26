# Southern Wetlands day/night GPU comparison — 2026-11-24

CANDIDATE_NOT_APPROVED. Not a public release, founder art approval, live clock/weather observation, or independent QA.

Exact rendered source revision: `c3a94b76798c60712c2f7474ec3d8d1ab823eee5`. Observer HTML SHA-256: `7a4e06a45e24c3a3690bebe7bf3577c0e640ab92d92f2d6fa3a79efcb868714e`. No original private memo imagery; publicationAuthorized=false. Physical ANGLE Metal Apple M3 Pro, 1440×813 PNGs.

Open [inspection.html](inspection.html) locally for the three paired views. The manifest retains source identity, exact UTC synthetic clock values, camera, held water phase, frame counter and per-image hash. The optional harness changes Date only inside the disposable Chrome evidence session and restores it after each pair; the shipped spectator runtime is unchanged. The host computes its existing Eastern clock. Noon is 17:00Z, midnight 05:00Z on November 24, EST. A synthetic verified loss exercises GLOBAL_CALM, not actual league state. Water is explicitly paused only for the same-phase comparison, not by weather.

Whole-frame RGB comparison (8/255 channel change threshold, 1,170,720 pixels; mean encoded Rec.709-weighted RGB, not physical luminance):

| Place | Changed pixels | Noon mean | Midnight mean |
|---|---:|---:|---:|
| Jackson | 960,043 | 79.63 | 32.97 |
| Waterfall Temple | 973,561 | 84.51 | 32.98 |
| Mud Dogs Swamp | 978,197 | 80.41 | 31.62 |

These are actual screenshot comparisons, not isolated water/terrain attribution, pixel-perfect acceptance, or a performance benchmark. Same camera and water phase per pair, distinct PNG hashes, zero browser exceptions, console errors or external requests. Normal no-login journey, all 23 places, Jackson history and return, ordinary water advancement during synthetic GLOBAL_CALM and explicit pause all passed before emission.

Reproduce with the existing source-only observer build and pinned Three vendor setup:

```sh
node productions/audience-site/preview/tools/webgl2-journey-smoke.mjs /path/to/observer.html --wetlands-light-dir /new/private/evidence/directory
node --test productions/audience-site/preview/tests/gpu-wetlands-day-night-evidence.test.mjs
```

Fresh tests: focused 4/4, full renderer/spatial/history 594/594, audience 76/76, Python 17/17; syntax and diff checks passed. Canonical Bullpen command/router invoked from clean archive `70a7031b934d4525859cb5ceea4c247e18680a04`; Architect-led resume, Complexity Warrant constrained this to opt-in existing harness and immutable evidence rather than another renderer/clock subsystem. Inline execution, no independently invoked staff or acceptance claimed.
