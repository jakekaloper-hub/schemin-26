# 2025 ESPN/Flaim team-slot and podium readback — 2026-11-01

**Status:** LIVE CONNECTOR READBACK / HISTORICAL DATA / REVIEW ONLY; NOT historical human-owner authentication or manuscript-canon promotion.

**Connection and scope:** Flaim Fantasy, connected ESPN football league 1417621, explicit season_year 2025. Queried get_ancient_history(platform=espn) to establish the available historical season; then get_league_info(platform=espn, sport=football, league_id=1417621, season_year=2025); then get_standings with the same params. Tool responses reported success=true, seasonId=2025, size=12, seasonPhase=season_complete and seasonComplete=true. No paid external capability was authorized or invoked. Data below preserves the returned 2025 display names; whitespace after the Chili Cheesers display name is not a new separate team.

| 2025 ESPN team slot | Season-specific display name | Regular-season W–L | Verified finalRank | Verified postseason state |
|---:|---|---:|---:|---|
| 1 | ObiWan Jacoby | 10–4 | 2 | runner_up |
| 2 | Red Leopards | 6–8 | 11 | missed_playoffs |
| 3 | Slob on my Dobb | 4–10 | 8 | missed_playoffs |
| 4 | The LLC | 4–10 | 10 | missed_playoffs |
| 5 | Baker Moore Purdy | 9–5 | 5 | eliminated |
| 6 | Three Dreaded Snake | 10–4 | 3 | eliminated |
| 7 | The Chili Cheesers [source has trailing space] | 6–8 | 7 | eliminated |
| 8 | The Immortal | 9–5 | 1 | champion |
| 9 | El Niño | 4–10 | 12 | missed_playoffs |
| 10 | Mud Dogs | 6–8 | 9 | missed_playoffs |
| 11 | Seven Deadly Chins | 6–8 | 6 | eliminated |
| 12 | Dr. Duckhook | 10–4 | 4 | eliminated |

All twelve team outcomes returned outcomeConfidence=explicit. The returned standings order itself is **not** final ranking: this table uses the distinct finalRank field, not the sortable rank. The provider team context returned teamId, teamName and abbreviation; it did **not** expose a historical human manager-account ID or ownerName binding in the sampled responses. Therefore 2025 team-slot identity is now directly confirmed, but attribution of a named real league owner to a historical slot remains **UNKNOWN**.

## Reconciliation for the living novel

- 2025 team-slot 6 = Three Dreaded Snake, 10–4, finalRank 3. This independently supports the archived historical dossier's season record and podium.
- 2025 team-slot 8 = The Immortal, champion; team-slot 1 = ObiWan Jacoby, runner-up; team-slot 12 = Dr. Duckhook, finalRank 4.
- Existing archived bracket ledger living-novel/history/PLAYOFF_MATCHUP_EVIDENCE_2022_2025.json additionally provides precise semifinal and final scores. This fresh readback **did not itself retrieve those particular match scores**; preserve the separate archived provenance.
- The old world/history/2025/2025_OWNER_TEAM_ALIAS_MAP.md still contains many TO VERIFY entries; this record narrows the **team-name** gap only. Do not automatically edit its human-owner associations or backdate 2026 visual props.
- The four-voice 2025 reader remains **NONCANON**, with real-person-to-character attribution and era-specific Atlas geography unapproved. The six-movement Phillip chapter's stage, theft, masks and speeches remain fictional proposals, not discoveries from ESPN.
- No source-to-canon promotion; independent Historical Librarian, Character, Umpire and Founder acceptance pending.

**Next historical verification:** If obtainable, request ESPN historical manager account owner IDs or season-specific management changes, cross-reference current canonical owner registry without trusting team names, and record per-year proof. A string such as KING or ZEEK in an abbreviation is not an authentication of a person.
