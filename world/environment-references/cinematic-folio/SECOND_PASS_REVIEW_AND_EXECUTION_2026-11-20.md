# Commonwealth Cinematic Location Folio — Second-Pass Bullpen Review and Code Receipt

**Date:** November 20, 2026
**Scope:** Full code-only second pass of PR #337 (source-bound backend, frontend, Island preview, location reference governance, offline build, tests, and documentation).
**Original code head reviewed:** daa20ae954903d269d96d5f014f746b08f04f4b6
**Primary source of execution evidence:** SECOND_PASS_AI_CONSULT_RECEIPT_2026-11-20.json + real code changes/test logs.
**Authority:** Existing World Engine on main; unmerged geography remains read-only and candidate/status labeled. No image generation.

## Actual Bullpen routing and invocation — source/role claims kept distinct

Canonical Bullpen Core compileIntent mapped the commission to **strengthen**. Canonical routeTask evaluated material-counterweight plans using its *existing* 18-Director registry, not a copied Schemin roster.

| Problem lane | Primary | Activated counterweights | Actual second-pass actions |
|---|---|---|---|
| Code/CI/source link correctness | The Architect | **The Setup Man + The GM** | Architect, Setup Man and GM received separate local ConsultEngine AI-role calls; implemented minimal link and browser-test fixes. |
| Source provenance/duplicate authority | The Librarian | **The Clubhouse Manager + The Closer** | Librarian, Clubhouse Manager and Closer received separate local AI-role calls; preserved single derived Folio data layer, source-pinned PR proposals and rejected canon promotion. |
| Reader/story-time/POV continuity | The Beat Writer | **The Scout + The Librarian** | Beat Writer, Scout and Librarian received separate local AI-role calls; source-derived eleven-season Island timeline, no invented 2026 result or present-world-date claim. |
| Independent challenge function | The Umpire | Evaluated separately in this mission | One local AI-role review; source facts and images remain unapproved until actually independently cleared. |

**Nine distinct Director-model roles were actually invoked:** Architect, Setup Man, GM, Librarian, Clubhouse Manager, Closer, Beat Writer, Scout, and Umpire. The Warden appeared in one canonical *secondary route*, but no Warden model call occurred; do **not** count that as an acted reviewer. Other 18-Director seats were not called because they had no demonstrated material task authority.

**Production role:** project-local **Visual Direction Lead**, bounded AI review using the Dylan Cole environment-design reference-bench entry. The production specialist registry specifies CREDIT_SOURCE_IDENTIFIED with METHOD-SPECIFIC VERIFICATION PENDING. Neither Dylan Cole nor any other named filmmaker was contacted; production analysis was a local model-generated method discussion, not independent professional approval.

**Inklings:** one project-local editorial AI analysis used three method lenses: Le Guin for lived culture and POV separation; Sanderson for reader legibility of systems/rules; Tolkien for geography and accumulated history. No living/deceased author participated, no separate individual Inklings worker agents were proven, and no new story or images were produced. This is not an eighth-member council meeting.

All local model consultations used Bullpen ConsultEngine where Director calls are documented, and local Ollama gemma3:4b for these bounded reviews. Responses remain **advisory suggestions**, and several recommendations required factual correction.

## Review dispositions against actual code and source

| Topic | Observed code/source issue | Decision | Implemented or held |
|---|---|---|---|
| Draft-file source hyperlink bug | Source Evidence tab used linkToSource with default main for Folio-branch files, while PR sources pointed to PR landing pages instead of immutable file versions. | **ACCEPT** | Link Folio files to the exact Folio branch; link each unmerged source file to its pinned full commit; main World Engine source files still point to main. Tested in Chrome. |
| Historical Island place continuity | UI initially displayed nine arenas but only an aggregate 11-season count; reader could not distinguish verified football history from proposed physical ground assignments by year. | **ACCEPT WITH SOURCE BOUNDARY** | Consume eleven 2015–2025 annual venue program records straight from pinned PR #322. Add season selector/chronology cards; make sport truth vs proposed venue chronology explicit. No 2026 fixture winner or Island physical approval inferred. |
| Location-card discovery | Clicking an individual site in the 23-card grid refreshed a distant inspector below the grid with no viewport movement, leaving users unsure if the action succeeded. | **ACCEPT** | Scroll into the source-bound selected-location inspector on card selection; no new visual asset. |
| Client runtime QA | CI only ran JavaScript parse/syntax checks; first iteration of initial Folio had a browser-only global location-name conflict that parse checking alone missed. | **ACCEPT** | Add actual Chrome DevTools browser smoke in GitHub CI; assert 23 LOC, 12 owner cards, 7 regions, 199 codes, 9 venues, 45 Island links, 11 historic season cards, source hyperlinks, and 390px responsive overflow. |
| SHA256 capability | One AI response claimed SHA256 itself provides no integrity guarantees. This conflates byte integrity with source authority. | **REJECT AS STATED** | Preserve legitimate SHA256 byte checks and immutable cross-PR source commit pins; acknowledge hashes do not establish canon accuracy or publication permission. No new hash store. |
| Main World Engine Week 3 snapshot | AI responses proposed automatic synchronization to a later assumed current-world state. No verified replacement was inspected; current input is explicitly dated end of Week 3, 2026. | **REJECT UNSUPPORTED UPGRADE** | Preserve date cutoff in every UI and source contract; only documented later source evidence may change it. |
| Product instrumentation rollout | GM lens suggested one-week user analytics and user-completion monitoring. The UI is a private local code-only preview, not a real deployed product with user traffic. | **HOLD FOR OPTIONAL FUTURE DEPLOYMENT** | Replace unsupported metrics claims with deterministic usability/browser acceptance now. No analytics SDK or external tracking. |
| Duplicate Folio authority | 23 source cards, PR #324/#325 proposals and Island PR #322 could be treated as a new parallel World Engine. | **REJECT PARALLEL AUTHORITY** | Single derived build_folio compiler; main remains authoritative. PR snapshot remains marked UNMERGED; Source Evidence tab states exact location and commit. |
| Inklings "historical full world" suggestion | A unified 2015–2026 visual time slider would require historical physical-state sources not currently verified for all 23 LOC sites. | **ACCEPT WITH ADAPTATION / HOLD EXPANSION** | Implement only the existing 11-year Island source program; main places remain dated to actual Week3 world-state events. No invented historical architecture. |
| Character references | Separate PR #253 twelve-portrait library is internal and renderer QA held; Folio must not republish images. | **KEEP HOLD** | Only source pointers retained; no image bytes copied or character images generated. |
| Video/PNG or public deployment | User explicitly requests backend/frontend coding only. | **BLOCK IMAGES/DEPLOYMENT** | No PNG/JPEG/WebP, still 0/23 approved cinematic masters, no published new site, draft PR #337 unmerged. |

## Exact source integration decisions

- Main: world/data/divisions.json, owner_domains.json, locations.json, physical_zones.json, routes.json, current_world_state.json, world_state_events.json, Location Cards and structural reference registry.
- Island: PR #322 exact source b32ecbc46e82133f7197fc8802a85e6b59abc44a. Proposed 23-node/45-edge causeway, nine permanent/heritage venue records, source-derived 2015–2025 annual venue program; no measured mainland connection.
- Atlas proposals: PR #324 155, PR #325 147, PR #339 exact 199 code-ID union (103 shared), none automatically promoted.
- Character source: PR #253 twelve source identity references, internal review only.
- Inklings: living-novel/consultants/author-council/_INDEX.md and PR #322 Inklings production unit describe advisory method lenses and project-local functional work; not independently executing individual human experts.
- Cinema reference: memo-os/cinematography/PRODUCTION_SPECIALIST_REFERENCE_BENCH_V1.json, which disallows canon override and release approval.
- Counterweights: canonical jakekaloper-hub/bullpen runtime/counterweights.js, never copied into Schemin.

## Regression gates

1. Run deterministic source build twice: build_folio.py --check and SHA256 reference parity.
2. Run the new Python tests, plus existing World Environment Reference and Location Control Plane regression suites.
3. Run Node frontend parse check.
4. Run browser_smoke.mjs in actual Chrome DevTools: 6 views, correct controls, exact source links and Island year filter, 390px viewport no horizontal overflow.
5. Run CI to completion on exact commit and inspect workflow results; avoid claiming CI green before results.
6. Verify no newly generated/committed raster files and unchanged main World Engine.
7. Keep PR #337 DRAFT; source/canon approval, Island Last Field reconciliation, independent review and publication remain separate gates.

**Review result:** practical corrections implemented and locally retested; this document does not claim release, image approval, independent human participation, or full multi-era canonical visual atlas certification.
