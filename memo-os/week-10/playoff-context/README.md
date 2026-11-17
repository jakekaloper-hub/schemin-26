# Week 10 analytics and FFHub production handoff

**Current production:** the final-results and design/personalization work in
PR #315 is preserved. The reviewed harvest is now selected on P28/P30/P31;
PNG production remains paused. Start with the current
[production entrypoint](../preproduction/README.md) and
[execution report](../production-evidence/playoff-harvest-20261117/EXECUTION_REPORT.md). The earlier analytics audit
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
| `Schemin_26_Week_10_Reviewed_Playoff_Harvest.json` | Reviewed protected source for this integration: all twelve POVs, all twenty captures, sixty retained binary witness entries plus one official-tie example. Exact checksum is in `preproduction/playoff-harvest.json`. It corrects the unqualified Mud must-win-out wording and omits the unsuccessful LLC search trial. |
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
| P28 — divisions | `SELECTED_CHANGE`: D0nkey K0ng's two named wins secure Burgers; Red Leopards winning all four secures Wings. Existing banner composition is retained. |
| P29 — scoring form | Preserve the existing disclosed 70/30 descriptive formula. It is independent of vendor odds and the Schemin scoring model. |
| P30 — playoff road | `SELECTED_CHANGE`: all twelve alive/none clinched; nine wins safe, eight not automatic; Mud can qualify through a division or shared berth. Visible record scenarios exclude tied future games; any further Mud loss eliminates. |
| P31 — next six | `SELECTED_CHANGE`: preserve all six fixtures and stakes; add the dated, attributed ObiWan/Chili win-or-loss estimates from the two selected vendor runs. |
| P35 — GOTW preview | Supporting schedule/record context only. Existing selection, history, character work and lineup sourcing remain editorial/provider decisions. |

The integration's [`playoff-harvest-consumption.json`](../preproduction/playoff-harvest-consumption.json) records actual copy pointers and hashes,
protected/public source checksums and current render-request hashes. A
matching existing statement is `SUPPORTS_EXISTING_COPY`; it does not require a
new page or a prose rewrite. P31 now selects one paired vendor callout:
ObiWan 52% with a Week 11 win / 13% with a loss; Chili 58% / 21%.
Other vendor values remain research. The harvest does not
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
It validates typed source identities and page bindings, allows only supported
descriptive source metrics, and screens their selected copy pointers. Matching
absent identities, invalid binding purposes, or forecast fields under generic
display labels cannot establish acceptance. Native proof text and unselected
prompt instructions remain under their separate Memo review path; the default
full readiness audit retains its broader copy and prompt checks.
`run_weekly.py` remains an evidence generator whose successful exit is not a
final production approval. See the subsystem README for its source/diagnostic
commands and freshness requirements.

## Ownership and next action

Scout accepts sources; Analyst verifies derived numbers and the selected
proofs; Memo Editor selects existing-page use; Groundskeeper rebuilds changed
mirrors; Librarian preserves provenance; independent Umpire checks the actual
selected copy and requests. GM/Closer coordinates the handoff. The Founder
retains artwork and publication authority.

Complete the Bullpen-led preproduction review; PNG execution is paused under
the latest user direction. When that stage resumes, use the existing
individual-folio sequence. Do not restart
source recovery or re-run an already answered scenario merely to demonstrate
activity. Reopen affected bindings only when source facts, selected wording or
the relevant assumptions change. Future weekly intake follows
[FFHUB_INTAKE_CONTRACT.md](../../../data-gateway/playoff-context/FFHUB_INTAKE_CONTRACT.md).
