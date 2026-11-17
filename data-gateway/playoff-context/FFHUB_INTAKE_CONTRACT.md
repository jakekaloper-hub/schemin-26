# TheFFHub evidence in weekly Memo production

TheFFHub is an external scenario source alongside Schemin's own derived
analytics. Its captured tables do not become provider truth, a calibrated
Schemin forecast, or an exact proof by being imported. The supported workflow
is a retained manual UI capture; no supported vendor API or unattended sync
has been established.

## Required handoff

Scout retains the actual vendor run and accepted league snapshot. Analyst
checks the matching league, season, completed week, future fixtures, division
berths and tiebreak assumptions. Record the source time, selected winners for
every scenario, baseline and restored baseline, raw displayed tables, and the
vendor's visible settings. Keep the complete input privately when disclosure
has not been authorized. A summary without its raw scenario rows is incomplete.

The recovered Week 10 artifact uses `schemin.playoff_scenario_packet.v1`:

| Field | Consumption rule |
|---|---|
| `as_of`, `league_id`, `season`, `through_week` | Match the operative issue and accepted source cutoff; recheck for later corrections. |
| `finalized_standings`, `completed_game_ledger` | Reconcile to accepted ESPN/Flaim facts; the vendor is not their authority. |
| `vendor_experiment.runs` | Preserve every scenario's selected winners and raw table. A changed baseline is sampling variation, not automatically a real-world change. |
| `team_povs` | Trace summaries back to the captured runs; vendor qualification estimates remain labeled estimates. |
| `exact_evidence` | Independently replay constructive witnesses or the appropriate exact calculation. Sampled 0% or 100% never proves elimination or a clinch. |
| `mathematical_scope`, `limitations` | Carry tie/outcome assumptions, score construction and model limitations with the claim. |
| `memo_binding` | Proposed page placement only. Verify the actual selected copy and current render request before claiming use. |

`qualified_team_ids` in witness artifacts identifies a qualifying set. Do not
interpret array position as an official seed unless a separate seeding check
has established that contract.

## Selection and page consumption

Memo Editor selects useful findings in the existing page budget. Record one
of `SUPPORTS_EXISTING_COPY`, `SELECTED_CHANGE`, `REFERENCE_ONLY`, or
`NO_MATERIAL_CANDIDATE` for each relevant page. Bind the decision to the exact
copy pointer and its hash, source artifact hash, and actual request hash.
Supporting an already accepted statement does not require rewriting it.
Changed copy must pass the existing mirror rebuild and final copy checks.

Keep three evidence classes separate:

- Accepted league facts and descriptive comparisons.
- Third-party simulation estimates, explicitly attributed to TheFFHub with
  their scenario premise and date; they have no automatic publication approval.
- Independently verified mathematical claims, with their proof and scope.

Schemin's own `HOLD_BASELINE_NOT_BEATEN` applies to its model. It neither
validates nor invalidates a vendor model. The current Schemin Memo adapter has
no forecast-release mechanism and must not be used to relabel vendor estimates
as accepted internal output. Exact proofs also use their own verification path.

## Repeatable weekly use

1. Resume the current issue and accepted facts; do not restart source recovery
   when a current final snapshot already exists.
2. Recover the retained FFHub packet before running duplicate scenarios.
   Refresh only when its cutoff, settings or the question has changed.
3. Compare its facts/rules with the current issue and replay only the proofs
   needed for selected wording. Recheck full seed order only if seeds are used.
4. Record source-to-copy decisions, then reconcile changed copy and actual
   render requests through the existing Memo workflow.
5. Independent Umpire checks the selected claims and copies. Existing artwork
   review and Founder release authority remain controlling.

For additional Schemin descriptive values, use
`memo-os/playoff_context_preflight.py` with the explicit packet, operative previs
and render-input directory. Its result concerns consumption of that packet;
it does not revoke a separate accepted production source/proof workflow.

Week 10's retained artifact names and current production linkage are in
`memo-os/week-10/playoff-context/README.md`.
