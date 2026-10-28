# Audience website execution ledger
Plan: docs/superpowers/plans/2026-10-22-schemin-audience-website.md
Branch: feat/commonwealth-audience-site

E01: baseline atlas 6/6 pass. No current reader application found in tracked files on main. Source checkout isolated in a fresh clone.
Ruling: use productions/audience-site for this cross-system presentation consumer; no new top-level directory or parallel canon. Independently checked against Architecture V2.
Ruling: deliver a buildless static application over canonical JSON and eligible source editions; no runtime backend or new paid dependencies.
Ruling: adapt reading from preserved archived manuscripts because current reader application is absent; do not invent inkjs capability or twelve accepted POV paths.
Ruling: Week 4–6 archived PDFs are source editions, not newly promoted releases. Public labels must preserve that distinction and Week 5 artwork-review identity.
Ruling: build a public website under explicit audience-viewing intent; site source hosting mirror contains generated public presentation only, while canonical source and authority remain in schemin-26.
E02–E08: data and frontend implementation in progress with bounded separate owners.

E01 complete: source rebased onto current main 7afe7ef0; no existing reader app on this branch; atlas baseline 6/6 pass.
E02 complete: 12 exact portrait crops hash-verified; 23 locations and 18 routes; 5 memo editions/110 pages; 4 exact archival manuscripts. Released Week2/3 recovered from canonical Library identities, fresh hashes, sizes and page-count verification. Actual memo resolver selects Week3 as latest released.
E03–E08 implemented: public home, ensemble, atlas/list/deep links, character/homeland, internal memo pagination, archive library, version-isolated local reading progress. Desktop and 375px embedded-browser viewport inspected. No horizontal overflow in tested mobile views. Founder experience acceptance remains pending.
E09 independent code review found two P2 defects: skip-link hash route and unpinned location provenance. Both fixed; source pin test observed failing then passed. Browser reproduced #main unavailable state before fix; replay now preserves page and focuses main. Keyboard atlas selection and direct location reload passed. Progress test observed source-version isolation failure then 4/4 green.
Fresh tests: catalog 9/9 including recovered sources, progress 4/4, publication 11/11, architecture 4/4, execution-control 8/8, rewrite 3/3; manifest/architecture/one-world validators and memo resolver pass.
Ruling: exact released Week2/3 originals remain in existing Library storage outside Git. Optional explicit source directory is required to rebuild their pages; default repository build has 75 source-edition pages, full deployment has 110. This closes the latest released memo journey without mislabeling newer source editions.
Ruling: preserved legacy manuscript text is exposed only as archive edition, never as the new twelve-POV rewrite.
Deferred limitation: memo pages are raster reading views with page-title alt text; full textual accessibility is not certified.
Deferred minor: public location projection retains some already-public unused canonical metadata; no confidential content found.
E10: public Sites access configured under explicit audience-viewing instruction; source sync and deployment in progress. Rollback procedure documented; live rollback not rehearsed.

E10 deployed: public https://schemin-commonwealth.jakekaloper.chatgpt.site; Sites returned terminal succeeded, deployment appgdep_6ada6d691004819191637b02d7e16cb7, saved version appgprj_6ada6ac1df0881918e9a8cfe1fa0c3e2~appgver_a356a1590e488191963a18107b0f2f53, hosting source commit ba974e17cf430f06c31838ebcd950c345de73e4e.
Full generated artifact: 136 files, 36,454,400-byte deployment archive, five memo issues/110 pages. No QA iframe page in deployed bundle.
Path-scoped repository merge gate completed: execution-control and resilience suites pass (8 and 9 tests respectively).
Mainline merge remains pending PR CI and founder experiential review; public first edition is deployed independently. No merge or rollback rehearsal is claimed.


## 2026-10-28 — Commonwealth website convergence mission, P0–P7 gate reconciliation

Founder command: resume existing PR #237, maintain PR #236 upstream and Week 7 PR #256 as separate owning lane; do not start parallel site or override Memo OS.

**P0 — AUTHORITY VERIFIED:** GitHub PR metadata on 2026-10-28: #237 open/draft, head `feat/original-website-artwork` at `0fcf8feab9401afb3196f40cedb6bfe41a1e064f`, base `feat/commonwealth-audience-site-20261022`; #236 open/draft at `ca8c43dd5750e0abc7ae9bab55fc93c9c5e8dfa8`; #256 open/draft at `f16edc0bf3f1981ed663e6660a9bc2770df4cc8a`. Existing board synthesis in `planning/audience-site/audit-2026-10-22/WHOLE_SITE_AUDIT.md` is expressly simulated; no authenticated 18-Director meeting recorded in this execution.

**P1 — LIVE SITE UNVERIFIED:** Public fetch of https://schemin-commonwealth.jakekaloper.chatgpt.site returned cache miss; connected Browser action returned originating-browser-context unavailable. No new screenshots, device tests, broken-route claims or live deploy receipts were obtained. Earlier historical deployment record is not a fresh smoke test.

**P2 — WEEK 7 HOLD:** `memo-os/week-7/WEEK_7_V52RC_INTAKE_2026-10-27.md` still documents provisional adapter-normalized evidence, source-native lineage or quarantine disposition absent, Steward ACK absent, CANONICAL_SNAPSHOT_LOCK / FACT_LOCK blocked and independent release certification missing. PR #256 contains draft 22-folio material, not a certified completed issue. Stage only privately until release evidence, exact art/page review, 1080x1920 output verification and Founder signoff.

**P3 — ARCHIVE HOLD:** `docs/publications/WEEKS_04_06_ARCHIVE_INTAKE_AND_BINARY_GATE_2026_10_22.md` confirms byte-verification for three PDFs but not final league-shared equivalence. Published-status reconciliation must occur through existing Publication Manifest authority, not the audience app.

**P4/P5 — EXISTING IMPLEMENTATION:** Audit documents working page families and partial Atlas/profile/readability repair. Remaining route compositions, atlas positional artwork, source-reviewed memo-to-character connections, exact released-PDF access and comprehensive accessible text remain unaccepted. No new visual acceptance or world/canon promotion.

**P6 — TEST/RELEASE HOLD:** This execution used read-only GitHub metadata/source inspection and wrote this evidence-only ledger update. No source-code repair, new CI run, browser tests, independent Umpire authentication, mainline merge or deployment verification is asserted.

**P7 — DISPOSITION:** This is a partial gate reconciliation, not completion of P0–P7. Resume scoped implementation on PR #237 when an authenticated build/browser runtime is available. Mandatory next proof is current production browser smoke (desktop/390px), exact archive-release status and Week 7 release prerequisites; continue nondependent accessibility and layout repairs. Never silently promote publication.
