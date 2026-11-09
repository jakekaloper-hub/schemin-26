# Week9 — executable input handoff and isolated P05 reference kit

This advances the existing35-page package, not the layout, canon, result or image-approval state.

## Actual fresh observation

`FLAIM_WEEK9_STATUS.json` transcribes the successful explicit ESPN1417621 /2026 /Week9 Flaim scoreboard response in this continuation. All6 winners remain UNDECIDED; current scores match the prior captured score values. Projections are source observations, not final points. The dry run correctly produces zero proposed winners or page updates and returns exit3 (waiting), not a successful final-result merge. This narrow check does not recertify older player, transaction or standings data.

## Two executable commands

From repository root, using Python3 and the standard library only:

```sh
python3 memo-os/week-9/prepare_production_inputs.py result-preview   --observation PATH_TO_FRESH_CAPTURE.json --output NEW_REVIEW_OUTPUT.json
python3 memo-os/week-9/prepare_production_inputs.py page-kit   --page W09-P05 --output NEW_EMPTY_DESTINATION
```

The first command validates the source and emits a NEW candidate/report file. It never edits the canonical page register, picks an authoritative winner, changes release flags, makes a network request, or schedules future work. Exit0 means a structurally reconciled proposal; exit3 means waiting/reconciliation required; exit2 is invalid invocation or file failure. Reading the output's status/errors is mandatory. A fresh export has a new input hash; a later stat correction therefore produces a new review rather than silently overwriting accepted pages.

### Source capture contract

Use the same shape as the stored actual Flaim response: `request` has league_id, season_year, week; `recorded_at_utc` includes timezone; `matchups_response` is the actual success/data payload; `representation` describes how the fields were collected. Always requestWeek9 explicitly even after the current-week pointer advances. Do not rewrite metadata to make old observations look fresh.

For a final candidate, add `lineup_evidence` with the same league_id/season_year/week, its own recorded_at_utc and genuine source_ref, plus `rows` using the existing Week9 normalized starter fields: fantasy_team_id, player_id, name, lineup_slot, points, started. The known ten-slot configuration must be accounted for for all12teams. No invented zero-valued player fills an empty slot. Missing/vacant-slot or inconsistent data returns to the source owner for explicit handling. The local candidate collection-window policy is15minutes; this is a conservative workflow check, not an ESPN guarantee.

The tool refuses wrong fixtures/host swaps, missing or duplicate teams, wrong week/season, non-finite scores, current-versus-final total conflicts, score/winner contradictions, ambiguous ties, missing/stale starter evidence, wrong slots and sums. It copies exactly one EXISTING finale paragraph into each proposed finale update only after successful reconciliation. If any later validation fails, all partial updates are discarded atomically. Genuine final ties still need the actual league tiebreak and an appropriate editorial treatment.

Official standings/seeds, transaction states, injuries, editorial rankings, forecasts and the full-issue final narrative still require their respective evidence/editorial checks. They appear as explicit per-page follow-through work, never inferred from a scoreboard. Issue268/source acceptance is not bypassed by passing local arithmetic tests.

## P05 — concrete one-page inputs

Open `P05_SINGLE_PAGE_INPUTS/REVIEW.html` or the matching ZIP. The kit contains9 files: two exact approved image bytes, their two appearance-authority JSON records, exact current draft copy, CURRENT layout_spec, isolated commission, manifest and review HTML. The two subjects are Duckhook and ObiWan only. No all12-character board, unrelated chapter, live score or unsupported outcome is included.

The manifest verifies every bundled file hash. It deliberately prefers the latest convergence `layout_spec`, not the earlier `proof_preparation.layout` still retained in historical metadata. No identity approval is reopened. This is reference staging and scope isolation, not proof that an image model received either file or reproduced the identities. The known failing whole-context route remains stopped. No paid provider/declined connection was enabled.

The kit source is pinned to the base commit recorded in VERIFICATION.json. Linking this derivative into the active page does not change its cast, pose sequence, copy, layout or status. The exporter also supports the already-planned P20 proof input lane, but this pass exports only P05, preserving existing queue order.

## Actual validation and limitations

Seventeen targeted tests cover rejection behavior, exact ending proposals, no source mutation, rollover handling, deterministic repeatability and image digest checks. Their fabricated result values exist only inside clearly labeled unit-test fixtures; no synthetic league result is stored as production data. Existing Week9 tests remain binding. The new test suite is added to existing Memo CI, not a new approval system.

This pass generated zero new scene images. The downloaded ZIP is a source-input kit, NOT a finished PNG, repaired poster, renderer success, Fact/Art Lock or publication approval. Next actual image step still requires a supported exact-reference provider route and visible output review. Before that, final-result collection can be staged through the new command without repeating the entire planning thread.
