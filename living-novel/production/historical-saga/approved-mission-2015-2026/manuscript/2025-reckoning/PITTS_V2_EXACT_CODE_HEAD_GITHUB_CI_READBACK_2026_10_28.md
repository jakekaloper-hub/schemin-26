# Pitts 2025 V2 — exact-code-head CI readback (2026-10-28)

**Status:** TECHNICAL PASS FOR CODE HEAD; EDITORIAL/CANON/DEPLOY RELEASE HOLD.

## Exact technical evidence
- Tested **source-code head**: `9b2660c548ad145ab86a9bfcce21e2ba918cc9d9`, existing draft PR [#243](https://github.com/jakekaloper-hub/schemin-26/pull/243), branch `novel/historical-epic-2015-2026`.
- [Novel OS CI run 40773908274](https://github.com/jakekaloper-hub/schemin-26/actions/runs/40773908274) — **completed SUCCESS**. Its job `123118056908` includes named **Validate 2025 historical Pitts eight-scene candidate (noncanon)** step, **SUCCESS**. Job log explicitly records **7 tests, OK**. Tests: source postseason pairing/score checks, POV order, original seven-scene text-body preservation, insertion identity, story-time/no retired narrator, protected Chapter I git blob guard, and release/owner/venue disclaimer.
- [Cross-Domain Authority CI run 40773908071](https://github.com/jakekaloper-hub/schemin-26/actions/runs/40773908071) — **completed SUCCESS**.
- [Repository Merge Gate run 40773908130](https://github.com/jakekaloper-hub/schemin-26/actions/runs/40773908130) — **completed SUCCESS**.
- [Bullpen Runtime CI run 40773907959](https://github.com/jakekaloper-hub/schemin-26/actions/runs/40773907959) — **completed SUCCESS**.
- The explicit test was added to existing `.github/workflows/novel-os-ci.yml` and is triggered by changed historical-production candidate paths. No parallel novel OS was created. A Python raw-string escape error was detected during initial file inspection and corrected *before* the tested head; the final CI run is the post-correction head.

## Holds / separate outcomes
- Exact commit status also reports **netlify/scheminnovel/deploy-preview = FAILURE** at this same code SHA. This is a separate deployment failure; no preview/publication success is claimed. The draft remains noncanonical and is **not released**.
- The subsequent `HISTORICAL-SAGA-20261028-2025-PITTS-V2.json` checkpoint-only update is a documentation change after the tested code head, not a re-run of the named test at the later docs SHA. State successful checks as **code-head evidence**, not all-future-commits approval.
- None of these checks evaluates literary merit, corroborates raw human historical owner attribution, certifies proposed 2025 geography, or supplies an independently authenticated Umpire decision. **Zero PR review submissions** observed when the review request was placed. Founder canon/publication approval remains required.
- Production output is **2,780 words of new Pitts fictional prose**; expanded eight-scene reading candidate **7,288 words**. Do not call it a whole 2025 season or a published novel.

**Next:** independent source/Atlas/literary review of the full eight-scene candidate, then a source-scoped proposed scene register for Phillip without weakening the existing Jake/Austin review contract.