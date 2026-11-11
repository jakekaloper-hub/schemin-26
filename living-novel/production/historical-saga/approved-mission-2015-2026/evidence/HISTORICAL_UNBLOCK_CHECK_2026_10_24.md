# Historical production unblock check — 2015–2025

**Initial outcome: provider-side source research advanced; owner-dependent historical drafting remained held. The broader blanket reading is corrected by the later authority audit below.** No historical manuscript was declared complete in this check. The new contemporary sequences are separately identified as 2026 and do not discharge historical coverage.

## Fresh evidence acquired

On 2026-10-24 the connected Flaim session identified the intended Pro Schemin football league. `get_ancient_history(platform=espn)` returned all eleven requested historical seasons, 2015–2025. Root then called `get_league_info` separately for every one of those seasons. All eleven calls succeeded; no refresh, league setting mutation, lineup action or service change occurred.

Exact structured tool responses, serialized as JSON, are preserved under `provider-readback/YYYY_LEAGUE_INFO.json`; `READBACK_INDEX.json` includes their SHA-256 digests. These are genuine captured tool results. They are **not raw ESPN HTTP response bytes**, nor retroactively substituted evidence for the older G01 fixture extracts.

All eleven responses contain twelve team entries, but **zero populated ownerName/teamOwners/owners fields**. A team abbreviation such as Jake, ZEEK, BABB or a familiar team name is retained as a source label, not promoted to an immutable owner identity. The history-list user's team slot likewise does not authenticate every historical season's ownership. No automatic character binding was created.

The provider's actual `scoringSettings.matchupPeriods` corroborate the period distinction used by the fixture audit:

| Years | Period structure returned | Postseason period length returned |
|---|---|---|
| 2015–2016 | 1–13 each span one scoring week; period 14 spans weeks 14/15; period 15 spans weeks 16/17 | 2 |
| 2017–2020 | 1–16 each span one scoring week | 1 |
| 2021–2025 | 1–17 each span one scoring week | 1 |

This corroborates why duplicated 2015/2016 display weeks must not become separate contests. It does not establish every bracket slot, resolve the 37 unpaired-row interpretations, or certify every historical fixture is present. `schedule.playoffSeedingRule` also varies: TOTAL_POINTS_SCORED in the 2015/2016 responses, H2H_RECORD in later responses. Do not substitute the current format for those source values.

The historical status envelopes contain mixed-era metadata (for example the requested 2015 response includes activation/waiver dates in 2025). Preserve that mismatch visibly. Do not use an envelope timestamp as proof of a 2015 event or overwrite season-specific result evidence with it.

## Existing-adapter corroboration attempt

The repository already provides `data-gateway/adapters/espn-public.js`; it retains team `ownerIds` when the upstream public response supplies them. Root invoked its read-only `fetchHistoricalLeague('1417621', 2015)` rather than creating a replacement ingestion system. The adapter's existing bounded retries ended with:

```
ESPN_TIMEOUT
getaddrinfo EAI_AGAIN lm-api-reads.fantasy.espn.com
```

**Action:** public historical ESPN read for 2015 via the existing adapter.
**Outcome:** failed network/DNS read; no data acquired, no state mutated. This was not an authorization denial, and no credentials were requested. No alternate credential path or bypass was attempted. A functional authorized transport could rerun the existing adapter, but a successful fetch would still need evidence that any returned owner IDs apply to the requested historical year and resolve to the approved character identities.

## Binding conflict and exact scope of the hold

`living-novel/history/OWNER_LINEAGE.md` and the championship machine index explicitly mark historical attribution unresolved. Individual Jake/Kevin character sheets contain historical interpretive associations, but R53's evidence and red-team records keep owner-era corroboration open. Those associations can guide research and preserve old pilot value; they cannot silently convert personal historical experience into verified fact.

The affected action is **drafting personal historical scenes in 2015–2025 as if a current canonical owner-character's historical presence were established**. The missing dependency is a source-backed, season-effective historical team/owner/character mapping (including departures, replacements and renames), plus period-valid world context wherever the scene relies on it. The hold is evidentiary, not a request for routine execution permission. Names, scores, aliases, present ownership and a general authorization to write fiction do not fill it.

Bounded invented dialogue, civilians and connective events remain available once the principal's temporal license is established. They cannot fabricate that license. An explicit Founder-approved **fictional historical casting rule**, if one is later supplied, would have to remain distinguishable from actual human ownership and be reconciled with the exclusive principal-POV canon before use. No such rule is assumed here.

## Chronological resume path

1. Start at 2015, where the existing prologue, thirteen regular-week drafts, postseason and epilogue already exist. Preserve their lineage and use the 90-contest observed denominator, not 102 returned rows.
2. Resolve the first scene's historical principal and period-world packet from corroborating evidence. If resolved, revise that exact old scene into enacted principal fiction and carry its consequence into the next unit; do not discard the season and restart from blank files.
3. Repeat 2016 onward with each year's own schedule, byes/consolation evidence, current scene-status inventory and source-to-prose joins. Unresolved ownership blocks only the affected personal scene; do not invent absent records or call existing text unwritten.
4. Complete each season's dramatic opening and consequence-bearing ending after source/continuity validation. A title row, chronicle summary or pilot is not that deliverable.
5. Keep the 2026 continuation lane separate. Its current source cutoff is Week 6; its draft event links are listed in `../CANDIDATE_EVENT_LINKS.json`. Do not count those links toward the eleven historical seasons.


## Subsequent broader authority audit — narrow correction

A later search of accepted manuscripts, approval receipts, character records and historical drafts found stronger evidence than the provider fields alone. See `HISTORICAL_BINDING_AUDIT_2015_2021.*`, `HISTORICAL_BINDING_AUDIT_2022_2025.*` and `../review/HISTORICAL_BINDING_REVIEW.md`.

Active hard-canon Chapter I explicitly places Jake and Austin against 2024/2025 title records and recounts the named 2025 semifinals and final. The Prologue supplies the named 2024/2025 final pairings. These support **event-specific fictional personal associations**, not verified real human-owner histories. The original blanket stop was therefore too broad for those exact accepted story facts. Bounded NONCANON expansion of Jake's 2024 title aftermath and the three specified 2025 postseason events can proceed with explicit proposed historical staging and a full scene packet. No whole-year ownership, earlier career or unmentioned fixture is thereby licensed.

The broader early-year audit did not establish an exact principal-as-owner interval for 2015–2021. It retained slot-lineage leads, inspected supplementary images and recorded contradictions; that is an unresolved narrow evidence dependency, not proof that no source exists anywhere. Kevin's 2022 association remains disputed/interpretive under the reviewed authorities.

At the parent's request, root also made one bounded repeat invocation of the existing public ESPN adapter. It again ended `ESPN_TIMEOUT / getaddrinfo EAI_AGAIN lm-api-reads.fantasy.espn.com`. An alternate read-only web fetch of the official 2024 `mTeam`/`mSettings` URL reported that the URL was not accessible through that tool. Neither route returned a payload; no raw ownership conclusion follows from those failures. These were failed reads, not a definitive missing-source finding or permission bypass. No further retry loop was run.
