# Developmental editorial and evidence review — *The Stone That Could Not Win*

**2026-11-02 | PR #243 | Producer-side self-challenge, not independent Authors Council or Umpire review | NONCANON / HOLD**

## Executed literary operation, not a plan

The prior source-exact 2025 sixteen-part reader consisted of **81,549 source words** including chapter metadata. Its first three parts contributed **5,001 + 983 + 5,417 = 11,401** words: Austin's private title aftermath, Jake's private surrender of the insignia, and their later confrontation over a flattering false monument. The original chapter bodies are preserved at their existing paths.

This run wrote the **4,894-source-word / 4,643-narrative-word** six-movement alternate opening, `THE_STONE_THAT_COULD_NOT_WIN_AUSTIN_JAKE_2025_DEVELOPMENTAL_NONCANON.md` (Git blob `893056edeb514dcea60e1e3a77d34af7620d47b3`). It is an **actual new fiction text** with alternating focalization Austin → Jake → Austin → Jake → Austin → Jake, not an outline or proposal-only packet.

The new **14-part, 75,042-source-word assembled reader**, `READING_COPY_2025_TWELVE_VOICES_FOURTEEN_PARTS_COMPRESSED_OPENING_NONCANON.md` (Git blob `7d9ca508d925493723478d02e0afc97d2276bdd9`), replaces the three opening chapters **for reading order only** with the integrated chapter and preserves the other 13 prior original source wrappers byte-for-byte. It is a second available *candidate reading*, not a destructive edit of the sixteen-part manuscript. The new reading reduces source volume by **6,507 words** and keeps the same twelve principal owner-character POVs.

## Why this is a developmental change rather than added anthology

- **Original repeated condition:** Both private opening chapters separately reasoned through the meaning of winning and losing. The later Austin–Jake encounter reopened the same ideas. In the cut, a carpenter's unpaid inscription and a lodging obligation put pressure on Austin *before* the newly certified Belt arrives; Jake's administrative surrender and a remembered kneeling portrait generate a concrete reason to investigate the false facing.
- **Escalation through another will:** The patron's practical motivation—rail, latch, entrance repair—remains credible. A correct name is not a cost-free victory. The foreman refuses a vague instruction and insists on wages and a specific mechanical job. Neither the patron nor the workers are perspective narrators.
- **Price and irreversible choice:** Austin will not buy safer structure with a misleading cross-year inscription. He directs the household to pay already accrued labor from ceremony funds, honors thirty-six fictional sleeping places and accepts a closed west gallery and unfinished facing. The patron withdraws the larger gift but authorizes narrower braces separately, preserving opposition without caricaturing him.
- **Jake's causal weakness:** He initially seeks leverage, admits he benefited from the painter's implied kneeling, is ordered away from an unsafe scaffold by a trained worker, and cannot patch the material problem with a token emblem. He loses a pleasing image but does not regain custody, status, or friendship.
- **Closing object:** The temporary board across a leaking facade is a physical limit to the argument, not another administrative meeting. Two seasonal records remain discrete; the Belt remains with Austin.

## Source-to-fiction firewall

**Verified sporting anchors only:** 2024 ObiWan Jacoby beat team-eight name **The King** 187.52–161.68; 2025 **The Immortal** beat Dr. Duckhook 152.20–151.80 in the semifinal and ObiWan Jacoby 161.07–109.56 in the final. Source references: `living-novel/history/HISTORICAL_PRESSURE_LEDGER.md`, `living-novel/history/CHAMPIONSHIP_SUCCESSION.md`, the preceding `THE_NAME_BENEATH_THE_GOLD_SOURCE_EDITORIAL_QA_2026-11-02.md`, and `living-novel/historical-chronicle/INDEX.md`. The 2025 team-eight historical **manager-owner field is not independently authenticated**, so using Austin's fictional 2026 owner-character identity in this historical scene remains a provisional continuity hypothesis, *not* verified player identity.

**Proposed entirely fictional:** architecture, weather, patrons, carpenters, scaffold, clerks, chair, repairs, payment amounts/financing, shelter promises, material incidents, their relative chronology, dialogue, public reactions, private sensations, and all social/world rules. Hall/route/period Atlas location IDs are **not** assigned by this text. This is not an allegation about the real owners' conduct, historic trades, or league transactions.

**POV gate:** Strictly `CHAR-AUSTIN-BYARS` and `CHAR-JAKE-KALOPER` interior in the six movements, with eleven other canonical character owners appearing only in subsequent original parts. No Edrin/Edin/Oren viewpoint, no extra principal narrator, and no 2026 match result. This historical draft has no permission to rewrite `living-novel/manuscript/PROLOGUE_DRAFT_V1.md` or `CHAPTER_01`–`03`.

## Producer's adversarial literary findings — unresolved

1. **High: institutional specificity still provisional.** The west rail, Hall arrangements and ceremonial fund may conflict with future period-correct Atlas and world authority. No precise terrain or travel relationship with the kitchen, wetlands or coast has been verified.
2. **Medium: compressed arc may omit useful original atmosphere.** Original Austin chapters attended closely to ordinary labor and narrow-victory psychology. This cut retains the ash bucket, shared passage, worker pay, lodging and conditional chair, but loses some long-form interior depth. An independent editor must compare what was cut, not approve merely because it is shorter.
3. **Medium: dramatic diction sometimes remains aphoristic.** The use of names and records, a necessary motif, can become repetitive. The patron has an economic case; more lived distinctions between the two protagonists' syntax and physical behavior may strengthen a subsequent line edit.
4. **High: historical manager binding / timeline.** Neither a 2026 character ID nor later in-world creative history binds a real historical ESPN account in 2024–25. The fictional confrontation's position before the ensemble is a developmental hypothesis, not confirmed geography or an itinerary.
5. **High: following 13 parts remain structurally uneven.** This edition removes one major repetition in the opening, but the reader remains partly an anthology of consequence-scenes with gaps in inter-character timing. The 2016 72-consecutive-Jake-limited manuscript still needs separate reconstruction.
6. **Release hold:** Literary self-review, deterministic content tests and passing GitHub CI—if observed—are **not independent** Author Council, Historian, Character Canon, Atlas or Umpire acceptance. No Founder acceptance, merge, publication or hard-canon promotion.

## Technical proof scope

New `living-novel/historical-chronicle/qa/test_2025_fourteen_part_compressed_opening.py` contains **23 deterministic regression cases** and is invoked in the existing `.github/workflows/novel-os-ci.yml` job. It checks exact Git blob identities for the chapter and reader, unchanged older edition, all 14 source wrappers' fidelity, thirteen preserved bodies, 12 registered principal owners, exactly six alternated POV movements, historical numeric anchors, negative retired-narrator guard, source words and noncanon firewall, plus frozen protected 2026 manuscript and 2016 reader blobs.

The producer must cite exact observed GitHub job conclusions. A test failure requires repair and rerun; no source says that this prose has passed independent literary review.

**Next literary edit after this run:** test the opening's voice contrast and material cost under independent editorial challenge; then make a similarly substantive, cross-arc transition **within** the 2025 reader rather than append another isolated vignette. Reconcile 2016 owner identities before rewriting any of its 72 limited-Jake passages.
