# Week 10 analytics and FFHub production handoff

**Current production:** PR #315 finalized the existing 34 full-folio inputs at
`14b1ad0c56752c7f0ee965843963b0e0de03184f`. Start with its
[production entrypoint](https://github.com/jakekaloper-hub/schemin-26/blob/14b1ad0c56752c7f0ee965843963b0e0de03184f/memo-os/week-10/preproduction/README.md). The earlier analytics audit
of `96bf06f` is historical; its stale-copy findings do not describe this newer
production source. Artwork and publication still follow existing Memo authority.

**Two retained workstreams:** the actual November 17 TheFFHub scenario harvest
and the independent Schemin analytics implementation. Both have a place in Memo
OS, with their different methods and acceptance boundaries retained.

## Retained evidence

| Artifact | Role and current use |
|---|---|
| `Schemin_26_Week_10_Playoff_Briefing.md` | The recent FFHub research briefing, recovered intact. Editorial reference for the existing playoff and next-week pages. |
| `Schemin_26_Week_10_Playoff_Scenarios.json` | Actual raw vendor tables: 18 named scenarios, initial/restored baselines; accepted-source observations and separately calculated mathematical witnesses. Schema `schemin.playoff_scenario_packet.v1`. |
| `Schemin_26_Week_10_Analytics_Checkpoint.zip` | Protected handoff checkpoint: recovered evidence, independent review, source/copy bindings, retained Schemin input/rules/diagnostic/report/packet and a hash manifest. Repository code remains in Git. |
| `MEMO_ANALYTICS_PACKET.json` under the checkpoint's `schemin/production-review/` | Dated Schemin descriptive candidate checkpoint based on the earlier previs. It is historical review evidence, not the current production manuscript or a permanent fresh input. |
| `preproduction/playoff-witnesses-final.json` | The production branch's independently checked exact-proof path, paired with final league facts. Its existing acceptance is separate from the Schemin forecast model. |

The protected source artifacts are retained outside the public repository.
Retrieve them by these exact names and verify the checkpoint manifest before
reuse. No private storage locator or authenticated payload is required in Git.

## How this supports the current pages

| Existing page | Evidence use |
|---|---|
| P27 — standings | Accepted final official standings; FFHub's displayed ranking never replaces provider seeds. |
| P28 — divisions | Accepted division membership and remaining divisional fixtures. |
| P29 — scoring form | Preserve the existing disclosed 70/30 descriptive formula. It is independent of vendor odds and the Schemin scoring model. |
| P30 — playoff road | The recovered exact-witness research supports the existing qualification-status and next-loss wording; bind it to the current copy and production proof. |
| P31 — next six | Match scenario premises and verified loss-survival/elimination evidence to the actual next-week fixtures and current stakes copy. |
| P35 — GOTW preview | Supporting schedule/record context only. Existing selection, history, character work and lineup sourcing remain editorial/provider decisions. |

The independent recovery review records actual copy pointers and hashes. A
matching existing statement is `SUPPORTS_EXISTING_COPY`; it does not require a
new page or a prose rewrite. Vendor percentages remain available as labeled
research, unselected for the current production copy. The harvest does not
establish vendor calibration. Schemin's separate forecast hold does not decide
whether another model is valid.

## Using additional Schemin analytics

The reusable runner supplies descriptive all-play, weekly-median, scoring and
remaining-schedule comparisons. Forecast fields stay withheld by the Memo
adapter. If the Editor selects an additional value, generate a current packet,
reconcile the selected copy and its mirrors, then run from the repository root:

```sh
python memo-os/playoff_context_preflight.py \
  --packet /path/to/private/MEMO_ANALYTICS_PACKET.json \
  --previs memo-os/week-10/preproduction/issue-previs.json \
  --render-inputs memo-os/week-10/preproduction/render-inputs
```

A nonzero result holds consumption of that additional packet. The command does
not undo the production branch's separately accepted final facts/proofs or
approve artwork. It uses current time and has no historical-time override.
`run_weekly.py` remains an evidence generator whose successful exit is not a
final production approval. See the subsystem README for its source/diagnostic
commands and freshness requirements.

## Ownership and next action

Scout accepts sources; Analyst verifies derived numbers and the selected
proofs; Memo Editor selects existing-page use; Groundskeeper rebuilds changed
mirrors; Librarian preserves provenance; independent Umpire checks the actual
selected copy and requests. GM/Closer coordinates the handoff. The Founder
retains artwork and publication authority.

Continue the existing individual-folio production sequence. Do not restart
source recovery or re-run an already answered scenario merely to demonstrate
activity. Reopen affected bindings only when source facts, selected wording or
the relevant assumptions change. Future weekly intake follows
[FFHUB_INTAKE_CONTRACT.md](../../../data-gateway/playoff-context/FFHUB_INTAKE_CONTRACT.md).
