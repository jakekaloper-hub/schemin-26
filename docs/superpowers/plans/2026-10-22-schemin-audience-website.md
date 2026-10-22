# Schemin Audience Website Execution Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox syntax for tracking.

**Goal:** Deliver an immersive public viewing experience connecting approved Schemin publications, the Twelve, the canonical atlas and eligible novel reading.
**Architecture:** Reuse canonical domain data and publication authority through a derived website build. Inspect existing components before fixing application placement or selecting a framework; preserve one world and one manuscript authority.
**Tech Stack:** Verified inputs currently include Python builders/resolution and HTML/CSS/JavaScript atlas presentation. Website framework, reader integration and hosting are decisions in Task E01; no installed framework or funded host is assumed.
**Spec:** Schemin_26_Ten_Day_Bullpen_Summit.md, especially decisions D01–D14 and its acceptance matrix. This companion execution summit operationalizes those recommendations; it does not create founder design approval.

Prepared October 22, 2026. Status: execution planning completed; implementation tasks remain pending.
Intended repository plan location after placement reconciliation: docs/superpowers/plans/2026-10-22-schemin-audience-website.md. This delivered document has not been committed there.

## Global constraints
- Public viewing with no required account and no audience editing authority.
- One World Model. One Spatial Control Plane. Many Views. No Forked Geography.
- Zero incremental spend; verify actual existing service access before selecting hosting.
- Published content must have eligible source identity; public repository presence is not release authority.
- No approved manuscript rewrite, character redesign or geography mutation for website presentation.
- No autoplay sound or mandatory intro sequence.
- Three visitor journeys: latest eligible memo; newcomer to approved reading; atlas to character to publication and back.
- Twelve overview where eligible material permits; do not fabricate twelve complete reading paths.
- Creator and final gatekeeper must be different roles.
- The ten simulated summit days are deliberation sessions, not elapsed implementation days or delivery promises.

## Review focus
1. Invalid or corrupt saved reading state must not crash the reader or jump to an unrelated publication.
2. A direct chapter/location URL, browser reload, back and forward must retain a coherent location and return path.
3. A missing or unresolved released memo must not silently select a draft or a different explicitly requested week.
4. A URL such as ?editorial=1 must not expose excluded candidate records in the public website payload.
5. Long titles, missing optional artwork and small screens must preserve usable navigation and readable content.

## Execution evidence behind this plan
Canonical Bullpen board and plan commands were compiled using the retrieved real runtime and dependencies. The execution board routed to Architect, Closer and Groundskeeper. The plan routed to Architect, Setup Man and GM, with Setup Man/GM counterweights activated against unnecessary engineering complexity. Three independent bounded analysts returned engineering, product and adversarial-review contributions. Dialogue below synthesizes those contributions; it is not an authenticated recording of Director meetings.

Commands actually compiled:
- /bullpen board Website execution planning summit: architecture, delivery dependencies, independent QA and publication integration.
- /bullpen plan Website execution plan: ordered engineering tasks, accountable owners, tests, repair loops and deployment readiness; summit simulation only.

New repository inspection:
- world/atlas/interactive/build_interactive_atlas.py reads canonical world JSON and produces a standalone HTML atlas. Its source has a fixed 340px sidebar, click-only marker handlers and an embedded candidate_catalog exposed through an editorial query option. These are source observations, not browser-tested defects.
- world/atlas/interactive/test_interactive_atlas.py checks counts, generated output, candidate marker separation and reference links. These tests were read, not run. They do not establish mobile or keyboard usability.
- governance/publication-manifest/memo_reference_resolver.py exposes resolve_memo_reference(request, manifest=None) and authority_packet(request, manifest=None). It rejects unresolved explicit weeks, ambiguous current benchmark authority and stale benchmark authority.
- docs/architecture/REPOSITORY_ARCHITECTURE_V2.md requires placement review before creating a new top-level directory. No new website root is assumed in this plan.
- governance/execution-control/TASK_REGISTRY_V1.json was partially inspected. Its task vocabulary differs from generic runtime states; preserve its existing schema instead of replacing statuses. A full duplicate-task check is still required.
- Current inkjs application paths and readiness have not been verified. Search results mention the prototype but are not implementation evidence.

## Summit II — ten simulated working days
Daily operating schedule: 09:00 readback; 09:30 proposal/challenge; 11:15 working session; 13:00 revision; 14:45 decision; 15:30 owner/dependency handoff. Times are America/New_York and are not scheduled events.

### Day 1 — Establish the starting line
Architect: “Before assigning frontend tasks, we must find the existing application, atlas, reader and publication contracts.”
GM: “Do not turn that into a full repository archaeology project.”
Librarian: “Start with relevant current authorities and tasks. Expand only for a real gap.”
Umpire: “The earlier summit is a brief, not proof of reusable software.”
Closer: “E01 is bounded reconnaissance with an exit artifact, not an indefinite audit.”

Revised motion: inventory the exact components needed by the three visitor journeys, record current revision and run the baseline checks in isolation.
Decision X01: no root framework or directory selected from assumption.
Owner: Architect. Output: integration findings, exact file map and baseline results.
Next-day input: actual eligible source candidates and unresolved dependencies.

### Day 2 — Bind content to the build
Librarian: “Every selected publication needs a canonical ID, source and eligibility basis.”
GM: “Can the demo use a newer PDF if the manifest still points to an older issue?”
Scout: “Not silently. Resolve the mismatch through owning publication controls.”
Architect: “The resolver already fails on stale benchmark authority. The website should consume that contract.”
Closer: “A blocker on the latest label must not prevent work on explicitly verified historical content.”

Decision X02: E02 emits a derived public catalog. It cannot promote content. Failed latest resolution blocks that feature; it does not invent a substitute.
Owner: Librarian; engineering implements adapter; Scout checks resolution.
Output: exact proof content list and deterministic validation cases.

### Day 3 — Resolve the application boundary
Architect: “A new frontend might simplify the shell.”
Setup Man: “What observed incompatibility requires another application?”
GM: “Reuse the data, but do not preserve an interface that misses the experience.”
Librarian: “New top-level placement requires review; use an existing owner when appropriate.”
Closer: “Evaluate reuse, adaptation and a thin new shell against the same journey requirements.”

Decision X03: E01 selects the smallest compatible implementation and records why alternatives were rejected. No second geography or character database.
Owner: Architect; Setup Man and GM challenge.
Output: exact files, dependency versions where relevant, build and test commands, hosting prerequisites.
Carryover: unverified hosting remains a release dependency, not an architecture certainty.

### Day 4 — Freeze the experience contract
Visual perspective: “We need real artwork before layout acceptance.”
Architect: “Placeholders help construct components.”
GM: “Temporary construction assets cannot establish visual quality.”
Beat Writer: “Use the actual reading text too. Titles, image composition and paragraph length change the design.”
Closer: “E03 will specify desktop and phone behavior with the selected assets.”

Decision X04: approve the concrete three-journey design packet before implementing its product behavior. Keep functional and experiential acceptance distinct.
Owner: GM with creative authority. Output: screen specifications, navigation and interaction states.
Revision: add second-content template reuse to avoid a bespoke one-character dead end.

### Day 5 — Build one complete audience journey
Architect: “Shell, catalog, routes, atlas, character and reader are separate modules.”
GM: “The first integration checkpoint must still traverse all of them.”
Setup Man: “Use small commits with targeted checks so a broken adapter does not obscure the shell.”
Umpire: “A build passing is evidence for a build, not visitor acceptance.”
Closer: “E04 through E07 converge into one integrated preview.”

Decision X05: integration proceeds using stable interfaces; no separate department demos count as the connected proof.
Owner: Architect. Output: homepage → location → character → publication → coherent return.
Carryover: secondary templates follow immediately after the primary journey works.

### Day 6 — Repair atlas presentation without forking the world
Architect: “The existing source includes the candidate catalog in the HTML. Hiding its panel does not remove the payload.”
Librarian: “Public site selection must decide what is eligible independently of the authoring atlas.”
GM: “We need touch and keyboard interaction, not just circles with click handlers.”
World perspective: “Keep canonical IDs and abstract coordinates. Presentation cannot create physical distances.”
Closer: “Preserve the authoring atlas; add a public projection or a compatible adapter.”

Decision X06: E05 excludes editorial candidates from public output, provides an accessible location list, and validates public marker identities.
Owner: Architect; world-domain review and independent QA.
Output: functional exploration with public-safe data and stable location links.

### Day 7 — Prove reader and memo behavior
Beat Writer: “Publication text must remain identical to its accepted source apart from presentation.”
Architect: “Reader progress needs a versioned key; stale chapter state must not corrupt another edition.”
GM: “And visitors must reach the latest eligible memo from the homepage without understanding our release terminology.”
Umpire: “Test direct URLs and reloads, not just sequential clicks.”
Closer: “E06 and E07 own these failure classes.”

Decision X07: use current reader capabilities where verified; isolate optional POV behavior rather than inventing routes. Local progress must degrade gracefully when storage is unavailable.
Owners: Architect for behavior, Librarian/Beat Writer for content.
Output: tested issue access and accepted chapter reading.

### Day 8 — Prove repeatability and first-edition coverage
GM: “One deep journey is insufficient if every next page requires custom code.”
Architect: “Then render a second location, character and publication through the same contracts.”
Groundskeeper: “How does a Wednesday publication become a site update?”
Librarian: “Through selected, eligible records and a reproducible build.”
Closer: “Make expansion measurable before launch.”

Decision X08: E08 tests template reuse, creates eligible-content coverage and defines first-edition population. No endless proof polishing.
Owner: GM for coverage; Architect for reuse.
Output: source-to-page coverage table; included and excluded items with reasons.

### Day 9 — Reject, repair and retest
Umpire: “A screenshot cannot prove history navigation. A unit test cannot prove the map is usable on a phone.”
Architect: “Separate deterministic checks, browser journeys and human visual review.”
GM: “A technically valid but generic presentation returns to creative revision.”
Setup Man: “A content change should invalidate dependent evidence, not restart unrelated work.”
Closer: “All defects receive owner, severity, reproduction and retest condition.”

Decision X09: E09 runs independent review. Failed gates route to bounded repair; no self-certified release.
Output: evidence tied to exact revision and a resolved or explicitly held defect list.
Founder visual acceptance remains separate and pending an actual preview.

### Day 10 — Rehearse release and commit the handoff
Setup Man: “We need a known artifact, hosting configuration, smoke checks and a recoverable prior version.”
Bookkeeper: “Verify existing access and limits; do not depend on expiring credits.”
Warden: “Public bundle inspection must confirm no privileged credentials or edit capability.”
GM: “Do not call a merged PR a deployed site.”
Closer: “E10 is release preparation and rehearsal. Promotion claims require their own evidence.”

Decision X10: keep implementation, tests, review, merge, deployment and public smoke checks as distinct states.
Output: reviewable implementation backlog below, release packet requirements and next executable task.

## File and interface map
Existing sources retain authority:
- world/atlas/interactive/build_interactive_atlas.py and test_interactive_atlas.py — source builder and baseline tests.
- world/data/locations.json, routes.json, physical_zones.json — canonical spatial inputs.
- governance/publication-manifest/memo_reference_resolver.py — memo authority adapter input.
- governance/publication-manifest/PUBLICATION_MANIFEST_V1.json — publication records.
- governance/execution-control/TASK_REGISTRY_V1.json — existing task control; schema preserved.
- Current reader entry points — E01 must resolve them before reader-specific file edits.

Proposed website component boundaries, exact parent directory assigned in E01:
- content/selection.json — selected canonical IDs and source references; no independent release authority.
- build/public_catalog.py — validates eligibility, relationships and public field projection.
- src/navigation.js — stable URLs/history and return handling.
- src/atlas.js — public atlas controls consuming projected data.
- src/reader.js — adapter to verified reader and defensive progress storage.
- src/pages/ — homepage, Twelve, character, memo and library presentation.
- src/styles.css — shared responsive visual tokens and page treatments.
- tests/test_public_catalog.py — authority and projection assertions.
- tests/journeys.spec.js — browser integration and failure scenarios.
- README.md — exact build/update/preview/rollback instructions.

These are proposed responsibilities, not claims that these files exist. E01 produces a revised exact file map before E04–E08 become implementation-ready. It may reuse existing equivalents instead of creating these filenames.

Internal website contract:
PublicCatalog = {schemaVersion:1, buildRevision:string, characters:CharacterSummary[], locations:LocationSummary[], publications:PublicationSummary[], links:ContentLink[]}.
CharacterSummary = {ownerId:string, name:string, imageUrl?:string, href:string}.
LocationSummary = {locationId:string, name:string, href:string, ownerIds:string[]}.
PublicationSummary = {publicationId:string, kind:"memo"|"novel", title:string, href:string, sourceRef:string, sourceVersion:string}.
ContentLink = {fromId:string, toId:string, relation:"located_in"|"features"|"reading"}.
These are derived website types, never replacements for canonical schemas. Source-version evidence must use the actual accepted version mechanism, not a fabricated hash.
ReaderProgress = {schemaVersion:1, publicationId:string, sourceVersion:string, position:string}.
Catalog must exclude internal candidate catalogs, private analysis and unsupported links. HTML rendering must escape source strings and allow only intended link schemes.

## Implementation backlog
All tasks are proposed/PENDING. Owners name accountable domains, not deployed autonomous workers.

### E01 — Inspect, baseline and lock exact execution map
Owner Architect; reviewers Setup Man, Librarian and GM. Dependencies: none.
- [ ] Resolve existing website/reader work in the full task registry and current branch; reuse matching work.
- [ ] Read governing placement rules and inspect atlas, reader, manifests, assets and relevant CI.
- [ ] Run python3 world/atlas/interactive/test_interactive_atlas.py in an isolated checkout. Record actual failures; historical count assertions are not automatically current truth.
- [ ] Run the current reader’s actual documented tests, after discovering its location; record command, revision and output.
- [ ] Select repository placement, implementation approach and build/test commands; do not add a top-level folder without required placement review.
- [ ] Produce exact file map and implementation estimates grounded in findings.
Exit: reviewer can reproduce baseline and understand every subsequent proposed path. Failed baseline is recorded and repaired within scope or explicitly isolated.

### E02 — Publishable content projection
Owners Librarian + Architect; reviewer Scout/Umpire. Depends E01.
Consumes canonical manifest/world identities; produces PublicCatalog through build_public_catalog(selection, sources) -> dict.
- [ ] Write test_explicit_week_never_falls_back: a manifest with no released requested week raises MemoReferenceError.
- [ ] Write test_latest_requires_current_authority: stale/ambiguous benchmark rejects latest.
- [ ] Write test_public_projection_omits_candidates: candidate_catalog and CAND-* records are absent from public output.
- [ ] Write test_public_links_resolve: every ContentLink endpoint exists and every emitted destination is eligible.
- [ ] Run targeted tests and observe failures before adapter implementation.
- [ ] Implement the projection using existing memo resolver; reject broken eligibility and unknown IDs.
- [ ] Run targeted checks and inspect public catalog; commit the implementation with its tests.
Exit: deterministic eligible catalog with source evidence and no invented relationships.

### E03 — Concrete design handoff
Owner GM/creative; reviewer engineering for feasibility, founder for intended visual direction. Depends E01 and selected E02 inputs.
- [ ] Specify homepage, atlas/location, character, memo and reader at 390px and 1440px widths.
- [ ] Specify focus, loading, unavailable content, missing optional artwork and reduced-motion states.
- [ ] Map all three visitor journeys to real eligible sources.
- [ ] Review actual asset crops and reading samples.
- [ ] Record concrete design decisions and unresolved founder judgments.
Exit: design is reviewable without imagining missing screens. This task produces design, not code or claimed founder approval.

### E04 — Responsive shell and navigation
Owner Architect; reviewer independent QA. Depends E01/E03 and applicable design handoff.
Produces parseRoute(url) -> Route, navigate(route, options) -> void; exact framework binding fixed by E01.
- [ ] Add deep-link/history test: load character/location/publication URL directly; back/forward returns coherently.
- [ ] Add long-title and missing-optional-art scenario; navigation remains visible at 390px.
- [ ] Implement shell, intended URL routes, navigation and coherent error destinations.
- [ ] Run browser journey subset and inspect desktop/mobile; commit.
Exit: stable shell that supports real destinations without public edit controls.

### E05 — Public atlas adapter
Owner Architect; reviewers world-domain authority and QA. Depends E02/E04.
Consumes public locations and routes; produces renderAtlas(container, catalog, onSelect) -> cleanup().
- [ ] Test public HTML/data contain no editorial catalog, including when ?editorial=1 is supplied.
- [ ] Test every public marker maps to an existing active location ID.
- [ ] Test keyboard and touch selection update the detail view and reading links.
- [ ] Adapt existing builder/presentation or create a derived public projection; preserve authoring atlas behavior.
- [ ] Run baseline atlas checks plus public adapter checks and mobile inspection; commit.
Exit: useful accessible exploration, abstract coordinate framing and correct relationships.

### E06 — Memo index and issue access
Owners Architect + Librarian; reviewer QA/Scout. Depends E02/E04.
Consumes PublicationSummary; produces issue routes and latest link bound to resolver evidence.
- [ ] Test explicit week absent: no substitution and no draft link.
- [ ] Test latest eligible issue navigation from homepage.
- [ ] Test PDF/mobile opening and missing artifact error; no broken active CTA.
- [ ] Implement memo archive, issue access and artifact treatment.
- [ ] Run tests and inspect actual memo access on phone-size viewport; commit.
Exit: returning league member can find and access the correct released issue.

### E07 — Novel reader integration and progress
Owners Architect + Beat Writer; reviewer QA/Librarian. Depends E01/E02/E04.
Produces loadProgress(publicationId, sourceVersion) -> ReaderProgress|null and saveProgress(progress) -> boolean.
- [ ] Test corrupt storage, unsupported version and unavailable storage; return null/false without crashing.
- [ ] Test progress cannot cross publication or source-version boundaries.
- [ ] Test direct chapter link, reload, return navigation and accepted text fidelity.
- [ ] Adapt verified existing reader; expose only supported accepted POV paths.
- [ ] Run current reader regression plus integration checks; commit.
Exit: comfortable approved reading with truthful progress and POV promises.

### E08 — Template reuse and first-edition coverage
Owners GM + Architect; reviewer Librarian/QA. Depends E05/E06/E07.
- [ ] Render a second character, location and publication with the same templates and contracts.
- [ ] Produce coverage table of eligible inputs, rendered routes and explicit exclusions.
- [ ] Populate the Twelve and eligible archive/reader coverage without bespoke duplicate authority.
- [ ] Validate every interactive destination and source reference.
- [ ] Run relevant content/route regression and commit.
Exit: proof scales through content, not custom page rewrites. Broader first-edition scope remains tracked.

### E09 — Independent QA and repair
Owner independent reviewer; creators own repairs. Depends E04–E08.
- [ ] Record exact revision, generated artifact and execution environment.
- [ ] Run three visitor journeys at 390x844 and 1440x900; check keyboard, reduced motion, history, reload and unavailable content.
- [ ] Inspect actual rendering, console/network errors, source correctness and public bundle.
- [ ] Log failures with severity, owner, reproduction and required retest.
- [ ] Repair affected implementation and rerun affected tests plus justified regression.
- [ ] Present working preview for founder experience assessment separately from technical gate.
Exit: no unresolved release-blocking failure; no fabricated user satisfaction or independent approval.

### E10 — Release readiness, recovery and promotion
Owner Setup Man; reviewers Warden, Bookkeeper and independent QA. Depends E09; public release additionally depends applicable owner/repository approvals.
- [ ] Verify current hosting access, compatibility and zero-incremental-spend fit.
- [ ] Produce clean build artifact tied to exact commit and eligible catalog.
- [ ] Document deploy, direct-link handling, asset paths, updates and rollback to known artifact/version.
- [ ] Rehearse rollback on a preview/test target where supported; otherwise record exact limitation rather than claim success.
- [ ] Prepare PR with concrete behavior, tests and limitations; merge only within authorization and repository gates.
- [ ] Deploy only within authorized scope; verify public home, atlas, reader and issue links.
Exit: distinguish PR-ready, merged, preview deployed and public smoke verified. A merged commit alone is not a live website.

## Gates, failure control and task state
G0 sources: eligible content and reachable assets; missing eligibility blocks dependent content.
G1 architecture: actual reuse findings and exact file map; unsupported framework assumptions stop implementation.
G2 design: concrete real-content experience and applicable review; placeholders cannot pass visual review.
G3 integration: clean build and connected journey; broken core path returns to creator.
G4 QA: required independent checks and founder experience assessment recorded separately.
G5 release: verified public scope, current access, reproducible update and recovery evidence.

Use canonical execution-control vocabulary and schema. Runtime PENDING/RUNNING/PASSED/FAILED/BLOCKED concepts must be mapped through the existing adapter to registry statuses; do not overwrite COMPLETE/READY/NOT_STARTED conventions blindly.
Every task carries ID, one accountable owner, reviewer, dependencies, acceptance, evidence, next action and blockers. Evidence binds to current revision; a failed child prevents parent acceptance.

P0: exposed credential, unintended editing authority or prohibited publication; stop exposure/release and repair.
P1: broken core journey, wrong canon/publication, lost required reading behavior; repair before release.
P2: material mobile/accessibility/navigation problem; repair before acceptance unless a specific residual limitation is explicitly accepted.
P3: minor cosmetic defect; prioritize visible value and avoid indefinite polishing.
After changes, invalidate only dependent evidence where defensible. No repeated full rebuild/review without a new failure or changed input.

## Dependency and capacity plan
Critical path: E01 → E02/E03 → E04 → E05/E06/E07 → E08 → E09 → E10.
E02 and design exploration can overlap after verified sample sources. E05–E07 can run independently after E04 interfaces stabilize. Parallel ownership does not imply available workers or paid capacity.
Simulated days organize planning discussions. Delivery estimates are produced after E01 and revised only when new evidence changes effort. No calendar completion date is promised.

## Self-review and handoff
Coverage: all three journeys, Twelve context, archive, atlas, reader, view-only boundary, budget, update, rollback and founder experience have owning tasks.
Review-focus mapping: progress E07; history E04/E07; unresolved memo E02/E06; candidate payload E02/E05; long titles/missing art E03/E04.
Interfaces are proposed presentation contracts, not canonical replacements. Exact implementation locations remain intentionally gated by E01; downstream tasks are not falsely represented as code-ready before that inspection.
This is a staged execution plan and summit record. It has not executed implementation tests, certified designs, merged changes or deployed a site.

Next executable action: E01, current-state inspection and exact implementation mapping. The current user request authorizes the execution-planning summit; it does not require starting the website build during this turn.

