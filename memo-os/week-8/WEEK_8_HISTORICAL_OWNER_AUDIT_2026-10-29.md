# Week 8 Historical Owner Audit — Ownership Is Time-Scoped

**Verdict:** Historical matchup scores and slot-pair records are source backed. **Current-owner personal head-to-head records are NOT VERIFIED.** This is a correction to any phrasing that pairs a current owner's name with an 11-season aggregate.

## Critical finding: 2025 team 5 identity requires resolution
- 2026 current canonical team 5: **Wilson Look / D0nkey K0ng** (source: `living-novel/history/OWNER_LINEAGE.md`).
- A 2025 historical Fantasy League Artworks archive's `TEAMS` array identifies **Baker Moore Purdy** with `owner_name: "Wilson Epworth"` (source: `jakekaloper-hub/fantasy-league-artworks/scripts/heal-pro-schemin-week1.js`).
- The script's owner_name is a provider-facing display handle in a repair artifact, not an authenticated historical ESPN account GUID. It **does not prove** that Wilson Epworth and Wilson Look are the same person or different people. Do not equate them, and do not infer a specific takeover year.
- The same archive's `MATCHUPS` array was previously quarantined because it mixes era names and returns twelve alleged weekly matchups for a 12-team league; **do not use that array for results**.
- User cautions that Wilson Look has not owned this franchise slot for its entire existence. Treat 2015–2025 team 5 results as **slot history only**, not his lifetime record.

## Source-only 2015–2025 slot H2H corrected after 2022 ingestion
| 2026 home/away slot IDs | Historical slot results (first slot W–L) |
|---|---:|
| 6 / 7 | 9–4 |
| 1 / 9 | 6–7 |
| 2 / 4 | 8–6 |
| 5 / 11 | 9–4 |
| 3 / 8 | 3–9 |
| 10 / 12 | 7–7 |

**78 regular-season rows total.** These must be labeled **ESPN slot rivalry records**, never as e.g. "Wilson Look is 9–4 versus Ben Whipple", because owner history is unverified.

## Historical-owner gate contract
Every historical result must carry `season`, `week`, `team_id`, `historical_team_name`, `owner_account_id` (nullable), `owner_display_name` (nullable), `person_identity` (nullable), `owner_membership_source`, `confidence`, and `status`. Current owner registry provides only current labels. Do not derive a historical person from same numeric team slot or similar names. Co-managers, transfers and account handoffs need season-scoped evidence. Exact entry/exit seasons remain unknown unless recovered from membership records.

Historical-owner proof requires a season-specific membership snapshot tying stable ESPN owner/account identifiers to franchise/team slot and corroboration of handle-to-person resolution. The 2025 repair script offers a **lead**, not proof. During uncertainty, publish vintage-name results with the label "historical slot", and omit owner-only lifetime titles, dynasty counts, and owner H2H claims.

**Owner-level fact lock: BLOCKED.** Do not merge or publish as owner-verified until steward/history review. Preserve original source ledgers, and supersede their owner-attribution implications with this audit.
