# Flaim connected-account continuity audit

Retrieved read-only through the connected ESPN account on 2026-10-24. Flaim's `get_ancient_history` identified the same connected-account team ID, `1`, for every recovered Pro Schemin' Football League season from 2015 through 2025. `get_league_info` supplied the season-qualified team label and abbreviation. This is stronger than current-slot matching: it establishes that the connected account was attached to the listed historical team record in each returned season.

| Season | Connected-account team ID | Team label returned by Flaim | Abbreviation |
|---|---:|---|---|
| 2015 | 1 | Scruffy Looking Nerf Herders | Jake |
| 2016 | 1 | Scruffy Looking Nerf Herders | Jake |
| 2017 | 1 | Scruffy Looking Nerf Herders | Jake |
| 2018 | 1 | Obi-Wan Jacoby | Jake |
| 2019 | 1 | Obi-Wan Jacoby | Jake |
| 2020 | 1 | Obi-Wan Jacoby | Jake |
| 2021 | 1 | Obi-Wan Jacoby | Jake |
| 2022 | 1 | Obi-Wan Jacoby | Jake |
| 2023 | 1 | Benedict Kenobi | Jake |
| 2024 | 1 | ObiWan Jacoby | Jake |
| 2025 | 1 | ObiWan Jacoby | Jake |

Flaim also returned full historical standings, settings, draft results and the 2015 roster for the connected-account team. Those responses identify team records and results, but none exposes a historical `primaryOwner`, `owners`, `members`, or human owner-name field. The draft responses likewise did not include the optional `teamOwners` map. Therefore the audit does **not** upgrade any row to factual provider-verified ownership and does not assign other historical teams to current principals.

The user’s statement that their team is owned by Jake Kaloper is retained as a user-provided lead, not recast as an ESPN/Flaim owner field. Before claiming the exact human-owner fact in published history, obtain an explicit user attestation suitable for canon or a dated provider/commissioner owner record. Until then, this evidence may support a bounded connected-account/Jake narrative perspective only where the existing canon-authority matrix also permits it; it cannot license claims about opponents, departed members, replacement members, or historical ownership transitions.

This audit deliberately keeps team continuity, personal identity, and fictional character eligibility distinct. New and departed league members should be modeled only after a dated source identifies the change, or as clearly proposed non-personal connective material that does not state an unverified owner history.
