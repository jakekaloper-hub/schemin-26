# Weekly Memo OS — Index

**Authority:** Weekly Memo OS  
**Knowledge steward:** The Librarian

## Load order

1. `SCHEMIN_26_WEEKLY_MEMO_OS_V5_5_INTEGRATED_PREPRODUCTION_PATCH.md` — binding integrated preproduction/world/temporal-canon hardening, promoted after Week 3 acceptance testing
2. `SCHEMIN_26_WEEKLY_MEMO_OS_V5_4_ACCEPTANCE_TEST_HARDENING_PATCH.md` — binding production hardening learned from the full Week 2 test
3. `SCHEMIN_26_WEEKLY_MEMO_OS_V5_3_CHARACTER_REFERENCE_ENFORCEMENT_PATCH.md` — binding character-reference, continuity-state, Fact Lock separation, and QA hard gates
4. `SCHEMIN_26_WEEKLY_MEMO_OS_V5_GOLD_STANDARD_STUDIO_PATCH.md`
5. `SCHEMIN_26_WEEKLY_MEMO_OS_V5_2_RC_MUTUAL_IMPLEMENTATION_PATCH.md`
6. `SCHEMIN_26_WEEKLY_MEMO_GOLD_STANDARD_PRODUCTION_MANUAL.md`
7. `SCHEMIN_26_WEEKLY_MEMO_MASTER_INITIATION_PROMPT.md`
8. `../canon/SCHEMIN_26_MASTER_CHARACTER_CANON.md` — includes binding v2.0 Reference-Plate Execution Patch
9. `../chronicles/standards/CHARACTER_VISUAL_LOCK_GATE.md` — release-blocking character QA

## Commissioner Creative DNA v1 — approved preferences, subordinate to V5.5

- `creative-dna/COMMISSIONER_CREATIVE_DNA_V1.md` and `creative-dna/COMMISSIONER_CREATIVE_DNA_V1.json` capture four Commissioner-selected patterns from Weeks 3–5; the examples govern composition/editorial goals, **not** obsolete character likeness or release authority.
- Every future weekly issue starts its issue previs/page packet with this conditioning layer. Load it together with Fact Lock, temporal canon, current character source references, World Atlas and the existing release gates. Unused/missing recurring rankings/opening modules require an explicit omission reason.
- `creative-dna/validate_creative_dna.py` and CI reject structural packet drift (12 ranking rows, prior-week movement, reused result portraits, margins, event/world links), but do not substitute for final-raster Character QA, mobile QA or the independent Umpire.
- The Week 5 19-page review assembly is a visual exemplar only; its 21-page publication provenance remains subject to the governing release manifest and Issue #164.

## V5.6 publication-integrity salvage

- `V5_6_CURRENT_MAIN_RECONCILIATION_V1.md` — current-main reconciliation and HOLD decision.
- Nine V5.6 publication-integrity contracts are active as additive controls beneath V5.5; they do not promote V5.6.
- `MEMO_RELEASE_REGISTRY_SPEC_V1.md` is a superseded pointer; Publication Manifest + Release Evidence own that concern.

## Status notes

- V5.5 is the controlling production-hardening patch after passing the Week 3 retrospective acceptance suite (11/11 after bug-fix/polish/retest).
- V5.5 integrates rather than replaces V5.4/V5.3: temporal canon receipts, final-raster character certification, persistent World Atlas/World State, personalized story intelligence, complete-issue previs, compact Page Design Packets, visual-rhythm/world-geography QA, and immutable approved-asset receipts.
- V5.4 remains binding beneath V5.5.
- V5.3 remains the controlling character-reference enforcement patch beneath V5.4 and is binding.
- V5 remains the controlling production-plane doctrine except where V5.3 hardens character/fact/continuity QA.
- V5.2-RC governs cross-OS orchestration during acceptance testing.
- V5.2-RC is not automatically permanent until its stated experiments / acceptance criteria are satisfied.
- The approved Week 2 memo is the historical gold-standard issue and remains canonical for Week 2. The current/latest benchmark is resolved from the Publication Manifest; as of this control state it is the released Week 3 memo. Blank-canvas testing must isolate same-week benchmark creative content until after generation.

## Missing source artifact

The exact original V5.1 Data Hardening Patch has not yet been recovered into this repo. Its adopted behavior is represented by V5.2-RC, the Subagent V5.1 response, and Data Gateway material.

## Character rendering invariant

Every Memo OS visual containing a league character MUST execute `OWNER RESOLUTION → CHARACTER_PACKET_LOCK → REFERENCE-ATTACHED GENERATION → CHARACTER QA`. The approved twelve-owner lineup/reference plate and Master Character Canon are an indivisible canon packet. Team name or prose alone may never generate a character. Missing reference packet or failed Character QA blocks publication.

## Week 2 acceptance-test lessons now permanent

- Build narrative matchups across as many pages as the story earns; do not force one-card recaps.
- Maintain a persistent continuity ledger across pages and future issues.
- Use deterministic typography for exact league data; generated factual text is untrusted.
- Default to native mobile portrait masters and reject accidental ratio drift.
- Page existence is not Page Lock; all required QA gates must pass.
- Ensemble/map pages require stricter reference resolution because they have elevated character-drift risk.
- Generate the final QA ledger only after the assembled PDF has been rendered and audited.


## Memo reference resolution\n\n- Explicit `Week N` requests resolve only the canonical RELEASED artifact for Week N.\n- `latest`, `current`, `benchmark`, `most recent`, and unspecified benchmark requests resolve through `../governance/publication-manifest/memo_reference_resolver.py`.\n- Search similarity never outranks structured publication authority.\n- Missing/unreleased explicit weeks fail closed; they never substitute an older memo.\n- Future release promotion must move `CURRENT_BENCHMARK` to the newly released highest week while preserving prior issues as historical canon.\n\n## Current production cycle

- Week 3: closed / immutable release evidence.
- Week 4: preproduction open at `week-4/_INDEX.md`; finished art remains blocked until V5.5 upstream gates pass.


## Shared resilience control

Weekly Memo consumes `../governance/resilience/README.md` and `../governance/resilience/PRODUCTION_CHECKPOINT_STANDARD_V1.md` for interrupted-run recovery and fresh-session handoff. These controls record reusable stage evidence but do not redefine the V5.5 state machine, Fact Lock, character authority, page acceptance, or release gates.

Creative conditioning coverage is registered in `../governance/resilience/CREATIVE_CONDITIONING_REGISTRY_V1.json`.

## Forward PNG geometry (2026-10-28)

**Binding for new commissions (including unfinished Week 7 and Week 8 onward):** Every Memo OS Page Design Packet, render prompt, complete-issue previs, page master and PNG acceptance receipt MUST inherit `output_format: PNG`, `output_width_px: 1080`, `output_height_px: 1920`, `output_aspect_ratio: 9:16` from `memo-os/PAGE_PRODUCTION_CONTRACT_V1.md`. Treat 1080×1920 as the final master, not a historical 1024×1536 composition stretched or arbitrarily cropped to fit. Keep character references, narrative copy, score/data typography, composition safe zones and Commissioner approvals intact. Providers may deliver an exact-ratio larger master resampled uniformly, but any ratio mismatch, crop, text loss or reference drift is a QA failure. Run `memo-os/native_png_contract.py` on actual PNG bytes before PAGE_LOCK; full-resolution character/world/copy inspection and 390px mobile QA remain mandatory. Already-published issues and their archived page packets are immutable historical evidence, not active defaults. No API or new provider is required for this policy change.
