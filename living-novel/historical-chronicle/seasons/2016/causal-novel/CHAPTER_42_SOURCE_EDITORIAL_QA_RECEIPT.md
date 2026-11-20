# Chapter XLII — source and author-side editorial QA (NONCANON / HOLD)

**Title:** *The Stage Beneath the Short Awning*. **Mission:** standing Founder-authorized Commonwealth Novel production mandate. **Repository/branch:** jakekaloper-hub/schemin-26 / novel/historical-epic-2015-2026. **Existing PR:** #243, draft. **Date:** 2026-10-31.

## Source and work-state reconciliation

- **Schemin main at intake:** 40b4ff8a4ab5f15bd8e986329472b31494cc09c0. **Bullpen main at intake:** 86889a59efb0e7dcdc37eef639981944dc77ed67. **Novel draft intake head:** e48020e53c5afa30bd5290e248e56006158e3dc4 (Chapter XLI).
- Read the current main Novel OS / MASTER_DIRECTIVE, WHOLE_BOOK_SOURCE_AUTHORITY_MATRIX_V1, TASK_CONTEXT_MATRIX_V1, TASK_REGISTRY_V1, TWELVE_CHARACTER_NARRATIVE_POV_REGISTER_V1, and Bullpen COMMAND_SYSTEM_V2 and lifecycleEngine.js. Reconciled issues #210/#211/#214/#215/#219 and PR #188 (closed), #252/#261/#243 (draft/open).
- Read Chapter XLI, its editorial receipt, source-exact 41-chapter assembled reader, and durable Chapter XLI checkpoint. Retained 2016 archive: G01_2016_FULL_WEEKLY_MATCHUPS.json (Git blob 6dbec1fe2537139f3a97c6a78250e2bae082a518). This is NOT a newly fetched ESPN record.
- Controlling preservation: approved 2026 Prologue and Chapters I–III on main are protected. No main-branch manuscript changes, period Atlas promotion, hard character canon, official 2016 Chronicle or release/publication changes are intended.

## Real literary production

- **New actual prose:** THE_STAGE_BENEATH_THE_SHORT_AWNING_CHAPTER_42_NONCANON.md — **8,180 whitespace-separated words including frontmatter/editorial handoff**, six connected fictional movements. Git blob 6294ffee1d478a493091a532451cdbb9f867f917.
- **New fully assembled reader:** READING_COPY_CAUSAL_CHAPTERS_01_42_NONCANON.md — **245,993 whitespace-separated words** including manifest/source notes. All 42 chapter texts are embedded and manifest-addressed, source-exact, with forty-one prior source entries retained. Git blob 92b280d66d5be876411bfa35f9f6b45e319d5519.
- **Prior reader preservation:** Chapter 1–41 reader blob 14ce93a324f62cf00307625c486bdbc17e4dd5f4, unchanged.
- **Chapter turn:** After Sela's children camp on unverified ground, Eren's speculative road-and-fire pictures become the occasion for a genuinely child-led stone-and-donkey performance at Fara's fire-shortened courtyard. Hessa and Sela refuse to serve as witnesses certifying the painter's imagined fire. Eren withdraws the red-fire painting from showing, not claiming true fire geography or destroying it. The former unnamed apprentice identifies himself as **Meric**, a unique fictional name checked against existing chapter sources after the initial candidate **Tavin** was found already in prior material; Meric takes a paid independent freestanding-panel job but does not return to Ina. Ina retains two unfinished dry orders.
- **Ending does not fake a repair:** Sela, Nella and Tam remain outdoors, no certified safe water, no guaranteed lodging. Hessa's six retain their bounded private room. Meric's second-day tabletop work remains proposed and separate, Eren's panels do not become archive or official map. No freight outcome, fire source, historic scoring-slot ownership, legal authority or canon event is solved by performance.

## Observed technical results — exact local working tree before commit

- **PASS:** 21/21 chapter-specific source-exact, continuity, negative fact-assertion, POV, hard-canon and archive tests after a first *test-only* assertion incorrectly expected the token "freestanding" in prose. The assertion was changed to verify the actually described "upright board"; no manuscript text was changed for that failure.
- **PASS:** 972/972 local Python tests using: python3 -m unittest discover -s living-novel/historical-chronicle/qa -p 'test_*.py' -q.
- **PASS:** 42/42 source/reader comparisons, manifest word counts, all source git blob identities, previous 41-reader preservation, official 2016 source archive blob and four protected hard-manuscript file hashes.
- **PENDING:** GitHub exact-final-commit CI review after push; independent Authors Council, Character Canon, Atlas, Librarian and Umpire review. Local Python PASS is NOT a release or independent literary verdict.

## Counterweight/editorial objections — AUTHOR SIDE only, not an independent Umpire

1. **Single-POV concentration:** This noncanonical causal strand remains heavily reliant on one Jake interior viewpoint, a major literary and twelve-owner polyphony deficit despite technical exclusivity compliance. Do not insert interior non-owner POV as a shortcut.
2. **Name collision detected and repaired:** "Tavin" belongs to different people in earlier 2016 fictional episodes, so the newly named former apprentice was renamed Meric *before assembly and test*. Check for other named-person collisions, particularly the earlier fictional Sela associated with a crossing and the later Sela who camps with two children. Chapter XLII preserves Chapter XLI's Sela but does not establish they are the same historical or fictional person; this potential continuity ambiguity requires reviewer attention before acceptance.
3. **Possible repetitiveness:** Jake has learned not to appropriate others' agency across many chapters. The children's self-directed comedy is a new narrative mechanism, but stronger change in Jake's own arc is still needed.
4. **Contemporary moral vocabulary:** The actors' commentary on representation and hired child performers risks reading as present-day social criticism; rework into coherent period institutions only after historical/Atlas authority.
5. **Tonal counterpoint:** Donkey/turnip comedy beside displacement and open fire peril may enlarge characters or feel sentimental and too convenient; independent literary challenge required.
6. **Physical and craft plausibility:** Three panels in a narrow courtyard, load-bearing feet, painted surface handling, dusk visibility, room/camp proximity, and Fara's shortened awning need independent spatial and craft verification. No invented official sites or distances.
7. **Independent contract realism:** Eren's paid frame supports and proposed second workday do not establish a functioning shop, guild, permanent patronage or future wages.
8. **Art as historical evidence:** A deliberately imagined red sky does not authenticate fire origin or route; its removal from public view must not be silently upgraded into approved Atlas truth.

**Gate disposition:** draft-only / NONCANON / INDEPENDENT EDITORIAL HOLD. Historical owner binding NOT AUTHENTICATED. Period Character Canon/Atlas signoff NOT RECEIVED. Authors Council/Librarian/Umpire verdict NOT RECEIVED. Founder canon/publication authorization NOT GRANTED. NO MERGE. NO CANON PROMOTION. NO PUBLICATION.

**Next:** Verify commit and four GitHub workflows; seek independent examination with specific editorial objections; advance Chapter XLIII with real character consequence instead of another rumor, tool repair, or aid ledger. Investigate period owner bindings before assigning any new interior viewpoint.
