# R46 — SIMULATED FULL BOARD: Chronological Historical Seasons, Twelve-owner Epic and Author Memory
**Date:** 2026-10-17. **Scope:** Founder update to R45; existing Bullpen, Novel OS, Universe Atlas, Memo OS and Flaim/Gateway only. **Status:** simulated debate and committed implementation direction, NOT authenticated Director attendance, canonical historical fiction, completed backfill, Umpire pass, merge or publication.

## Correct the problem statement
The previous board placed read-only author memory first but did not adequately specify WHAT must be remembered and reconstructed across old seasons. The Founder now explicitly wants every recovered season interpreted as a **chronologically sound, full ensemble season of evolving stories**: each week has matchups/verified outcomes and potential character developments; all twelve participating owner identities/period avatars must be independently verified, or marked UNKNOWN and mapped as historical team roles rather than falsely assigning current owners. A season has a central narrative arc, twelve independent story tracks, other people's consequences, institutional/world changes, active mysteries and intentional gaps. The writers creatively dramatize missing non-scoreboard history, with firm source-versus-fiction boundaries. **2026 Weeks 1–5 are a process reference/prototype, not literal events to copy into 2022.** Book One's era and publication order remain unconstrained by the archive.

## Existing engines board must reuse
- `data-gateway/HISTORICAL_GATEWAY_ACTIVATION_FINDING.md` identifies FLA `espnAgent.js`, `ingestionAgent.js`, `backfill-historical.js` primitives. **DO NOT use score-max heuristic champion detector**; its historical champion fallback is explicitly quarantined.
- `living-novel/research/DATA_GAPS_AND_LIMITS.md`: 2015–2025 weekly matchups, seasons, standings, playoff data, draft boards generally recoverable. **Historical transactions and reliable historical owner names are NOT provider-recoverable**; refrain from invented adds, trades, owner associations.
- `living-novel/os/NOVEL_OS_PHASE_7_LIVE_SEASON_ENGINE_V1.md`: source → verification → significance → history → character/world → story architecture → scene → manuscript → continuity → canon.
- `living-novel/whole-book/LIVE_NOVEL_CONTINUATION_CONTRACT_V1.md`: SCENE NOW/BANK/BACKGROUND/MEMO ONLY, not one chapter per week.
- `world/history/WORLD_MEMORY_ENGINE_V1.md`, Atlas owner domains/regions, Bullpen Memory Architecture and Novel Phase 4 Continuity checks.
- R37–R42 twelve characters and connections, R43–R44 author context schema and manual proof, R45 convergence critical path. All are developmental documents, not extra canonical engines.

## Second board summit — disputed issues and binding development rulings
**Closer:** “The book isn't a retelling of 2026 alone and it's not twelve separate autobiographies. The system must reconstruct the Commonwealth's eras, show how ordinary people lived, and let each source-season produce a dramatic ensemble.”
**Scout:** “We can recover 2015–2025 weekly scores and standings plus draft boards, not full emotional lives or historical transactions. Backfill and verify each *season-week-matchup* source with hashes, champion bracket validation and identity uncertainty.”
**Librarian:** “Everything has an era and an as-of date. A 2022 character cannot recall a W2 2026 prank, 2025 title or post-haircut state. Proposed historical fiction must remain separate from source events and current world state.”
**Beat Writer:** “The 2026 weekly Memo treatment is a sample of a **creative transformation method**, not a narrative template to replay word-for-word. Give each old season a compelling central question, escalating midpoint, 12 owner trajectories, personal stakes, failures and irreversible choices; the season can span many scenes even when the score's entire causation is unknown.”
**Universe/Atlas:** “Historical seasons need reconstructed in-world conditions, livelihoods, jurisdictions, travel, artifacts and social memory. Never assume 2026 place conditions existed in 2015. Deep history can predate the ESPN archive but is fiction, not invented league data.”
**Character Director:** “Twenty-four years of literal unchanged characters are not justified. Use period-specific states; unresolved owner slots get historically named team roles, not a forced cast of current 2026 identities. If the same twelve protagonists are intended in a fictional historic episode, the Author Room must explicitly reconcile that as an approved adaptation, not source fact.”
**ConsultEngine literary lens:** “Every one of twelve gets long-term independence across the saga. **Not** equal word count in every week or necessarily all twelve personally participating in every archival season. A surprising championship result is an endcap, not an entire novel plot.”
**Memory Architect:** “R43's packet should include season/year/week/matchup stage, narrator's knowledge cutoff, aliases and character temporal state, contemporaneous world history, script/draft decisions and long-term payoffs. Extend the existing adapter, don't invent another operating database.”
**Visual Lead:** “Period-specific illustrations need both owner reference and era/time-state; stable geography and novel scene variants must be source-linked and approved.”
**Umpire-style skeptic:** “Avoid calling extrapolated fictional political change a verified result; don't auto-promote plans into canon; no full-historical completeness until source readback/identity proof and testing.”

**Consensus:** The historical chronology gap is **P0 alongside** memory retrieval. It is not a reason to postpone memory; the memory adapter must read verified historical episodes, not just current-week story notes. The next work sprint has **two parallel inputs**: validated 2015–2025 chronological episode index and read-only author context resolver.

## Chronological archival-to-fiction pipeline
1. **ESPN/FLAIM Historical Retrieval**: season year, regular/playoff weeks, matchup ID, team slot/name, actual results, draft/standings where present, source hash, fetched-at, parser version, source ref. Never infer trades or personal dialogue.
2. **Season Evidence Freeze**: complete week-by-week schedule plus confirmed champion via bracket/final placements. Missing matchups, questionable owner alias or transactions marked UNKNOWN; fail closed for any unsupported championship claim.
3. **Historical Identity/Time Resolution**: map owner only when independently proven; attach season-specific visual/ontology history where verified; keep `historical_team_id` distinct from `owner_character_id`.
4. **Historical World State Reconstruction**: read-only current Atlas + approved historical deltas, candidate settlements, social trade routes and institutions with source/proposal statuses; no automatic 2026-state backfill.
5. **Author Room Season Dossier**: one season-wide controlling conflict; participant/character views; weekly encounter/causal register; public power transitions, nonparticipants' second-order consequences; mysteries and recurring objects; what is only suggested by outcomes.
6. **Twelve Character Histories**: for 2026 current POVs, full authorized participation. For earlier seasons, preserve twelve principal throughlines over the *overall saga*, but gate assignment to earlier slots until identities are proven; period-only team names may be background evidence instead.
7. **Script and Story Drafts**: choose high-leverage events, create three-to-six multi-POV scenes per dramatic movement; human-scale stakes, dialogue and opposite interpretations; ordinary civilians are non-POV characters. Do not write one chapter for every weekly box score.
8. **Memory and Continuity**: load AUTHOR_DRAFT packet for scene time; verify no future knowledge, unseen event presented as direct memory, impossible travel, wrong owner state, slipped published versus draft text, or lore-object retrojection.
9. **World Impact and Art**: accepted story affects world state only via existing World Evolution approval; render with character-specific reference bytes and historic Atlas permission; link art to exact scene and time.
10. **Editorial / Publication**: authentic blind readers, independent Umpire, Founder canon approval, GitHub CI, PR merge, continuous manuscript build, image QA and verified publication.

## Exemplary 2022 mini-season architecture (PROPOSED, not a retrospective claim)
**Source skeleton:** Red Leopards 13–1 regular season, third; El Niño 7–7 regular season, championship winner after beating Red 116.32–97.96 in the semifinal. Season 2022 has other owners and matchups: **retrieve the actual season/week records before naming them**.
- **Opening movement:** Current Red brand is not proof of 2022 owner identity. The cultural confidence depicted in R33 is a fictional proposition, not a proven 2022 merchant contract.
- **Escalation:** Use consecutive *actual* 2022 matchups to investigate which teams' fortunes changed, who met whom, and what consequences could plausibly propagate. Do not invent matchup outcomes from a final record.
- **Midpoint:** As regular-season dominance grows, consider opposing viewpoints and civilian costs without magically attributing them to competitors whose owner IDs are unknown.
- **Postseason movement:** Verified El Niño semifinal win reverses Red's expectancy. Other certified finals determine title order, not an assumed singular 'destiny'.
- **Aftermath:** World memory can carry an approved interpretation forward, but 2026 characters' firsthand memories of 2022 remain authorization-dependent. Future readers can learn historical events out of order; characters cannot.

## Master plan modification to R45
**P0A — Verified Historical Chronicle Index:** 2015–2025 season-week-matchup evidence and honest per-season identity gaps. First recover one season end-to-end (2022), then scale older/adjacent years via existing runner. Retrieve and validate, not manually fabricate absent scores.
**P0B — Author Memory Adapter:** existing R43 read-only integration, now keyed by `evidence_season`, `evidence_week`, `book_time`, `known_by_character_at`, `historical_team_slot` and `character_identity_provenance`; join verified Chronicle and manuscript/story-state only.
**P1 — Historical Season Story Room:** season-scale synopsis + real week/matchup fact sheet + twelve owner/saga impact table + proposed worldbuilding + arcs + dialogue and unresolved plot promises.
**P2 — Multi-era Narrative Atlas:** story/region/world memory layer only; historical setting states marked proposed and cannot overwrite current base geography.
**P3 — Substantive prose + reference art:** all chosen years and characters selected by dramatic causality, not equidistribution.
**P4 — Independent reader/Umpire, Founder, merge, publish:** do not claim until authenticated evidence exists.

## Acceptance gates: failure cases
- 2022 draft knows about 2026 W2 returned parcel -> FAIL.
- 2023 figure remembers 2025 title -> FAIL.
- 2018 current Belt Keeper claimed owner of team 8 without evidence -> FAIL.
- Unverified historical adds/drops named as certified -> FAIL.
- Highest combined score assumed title-winning matchup -> FAIL.
- Season synopsis with twelve protagonist names but no twelve grounded arcs -> FAIL literary completeness.
- 2026 map applied to historic road without evidence/proposed label -> FAIL.
- Beautiful manuscript but no real source hashes, approved canon or art references -> HOLD.
- 2022 score result altered for branching adventure -> FAIL.

## Deliverables and ownership
- Scout/Architect: exact 2022 historical matchup-by-week source extract, raw hash and bracket/standings consistency report from existing FLAIM/Gateway.
- Librarian/Architect: one adapter-backed chronologically bounded Author Context Packet for 2022 and the existing post-W4 Wilson packet, both source-attributed.
- Beat Writer/ConsultEngine: one season-wide 2022 Story Room dossier including all evidence-supported historical participants, current owner links with UNKNOWNs, six distinct cross-arc causal proposals and three dialogue-intensive scene briefs.
- Universe/Atlas/Visual: historical 2022 setting and proposed institution overlay audit without mutating base world.
- Umpire: independent mechanical/literary acceptance receipt only after actual review.
- Closer: reconcile with R45 and prevent parallel stacks.

**Definitive simulated board decision:** START historical full-season chronology and author-memory implementation **NOW, together**. This changes P0 dependency order but does not reopen the project's North Star, choose Book One's era, approve speculative history, or claim merge/publication.
