# Commonwealth Observer World — first implementation boundary

Status: implementation candidate; not a finished visual experience, public release, or new OS.
Authority: Jake's answers and delegated defaults in PR #309 comment 6900676650, explicitly reopened November 15, 2026; continuation authorized in the next user message.
Base: PR #309, 9b5953c6cb189e4b6bf272965e8631910df6c462. Existing source authorities remain unchanged.

## Product direction
A spectator observes an inhabited Commonwealth. There is no avatar, resident greeting, interaction that changes residents, location unlocking, or visitor-caused history. Crest-led readiness precedes a brief skippable cinematic reveal. Initial world view has no labels. Existing places remain present regardless of visitation. Observation moves among aerial, overhead, panoramic and ground viewpoints. Reader input never unexpectedly moves the camera.

## Approach and this tranche
Preserve the current audience-site branch. Add small framework-free presentation modules under its existing src directory; build a private derived catalog from World Engine files. This is the bounded next step under the completed interview, not approval to replace the world view with generic UI. Existing app.js is deliberately not replaced: no acceptable world-scale visual assets/camera geometry have yet been mounted in this tranche.

Alternatives rejected: a second World Engine, a simulated game, or another isolated Last Putt reader. A diagram/debug canvas is not a publication-grade world and is not delivered as one.

## Exact behavior
- All PERMANENT_CANON, PROVISIONAL_CANON and INTERPRETIVE_CANON LOC records are projected with their original status. Editorial CAND records are excluded, never promoted. Projection does not authorize public release.
- Critical-asset completion signals control LOADING -> REVEALING -> EXPLORING. Reduced motion/returning visits skip the reveal, not readiness. Failure yields FALLBACK and explicit retry; no fake percentage or universal preloading guarantee.
- Inspect affects labels/view preference only. Unsupported world-changing actions fail. Reader eligibility is a trusted upstream catalog input, not client-side authorization or a public-data security boundary.
- One shared America/New_York clock, including daylight-saving offset. This module does not compute sunrise or connect a weather provider.
- LIVE mode: latest finalized VERIFIED loss means a global clear/calm weather-effects override. Latest VERIFIED win produces localized storm presence. More consecutive verified wins cover more source-defined zones. Ties/stale/ambiguous/missing data never become wins or losses.
- Candidate tuning: one extra zone per known consecutive win, in WX-EASTERN-STORM propagation_order, capped at supplied geography. Missing earlier weeks produce a lower-bound streak with streakComplete=false, not fabricated history. This does not invent new zones.
- Historical mode requires its own verified presentation snapshot and ignores current outcome/weather. No modern condition repaints an old issue.
- No storm effect writes permanent damage, closes a route, changes manuscript canon, or invokes World Evolution APPLY. The new live presentation rule is not a metaphysical rewrite of the older El Nino ontology.

## Source integrity
The derived catalog carries exact git HEAD, per-file SHA-256, and current_world_state.as_of. It does not relabel that older as-of as present-day truth. Live league/weather adapters, solar model, approved world composition, renderer readiness adapter and real camera geometry remain explicitly NOT_CONNECTED/NOT_MOUNTED/missing. User-visible 'live' claims remain unavailable until connected evidence supports them.

## Bullpen evidence boundary
The canonical execution skill, intent compiler and router source were inspected. Domain work is performed inline by this assistant; no separate Director worker or independent Umpire approval is claimed. Bullpen Core is a private repository; this environment has no direct network clone and no authenticated cross-repository runtime checkout. Canonical runtime invocation remains unexecuted, not simulated. Existing domain/counterweight concerns constrain the work: no overengineering, no false freshness, no inferred authority, no visitation-based world changes.

## Next visual gate, not hidden implementation
The full-world master must preserve existing Atlas topology and pass a label-free first-arrival review at desktop and phone sizes. The first reveal may not show missing textures, placeholders or labels. Approved low-detail whole-world composition comes before detailed location streaming. Characters are occupied, not facing a profile camera. Real solar/light, weather and verified-result adapters require separate source-bound integration. No new image was generated or existing visual approved by these tests.

## Acceptance for this tranche
Executable tests prove pure behavior; repository integration proves actual source consumption and unchanged canon bytes. Full inherited audience/Story Graph tests must run in CI because the local environment contains a patch overlay, not a complete repository clone. Independent review, visual QA and deployment remain separate and open.
