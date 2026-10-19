# Mission #121 — Schemin '26 persistence and authority integration
Status: CANDIDATE / NOT ACTIVE / NOT ACCEPTED
Owner: Bullpen Closer; knowledge authority: Librarian; independent acceptance: Umpire.
Upstream: https://github.com/jakekaloper-hub/bullpen/issues/121
Upstream candidate: https://github.com/jakekaloper-hub/bullpen/pull/141

## Reuse, never replace
This is a project adapter contract, not a new OS or alternate registry. Authority remains:
- PROJECT_CONTROL_REGISTRY.md and SCHEMIN_26_PROJECT_MISSION.md for project-wide routing.
- governance/execution-control/TASK_REGISTRY_V1.json for normalized task state, subject to source-grounded reconciliation.
- League Data Platform/FLAIM for sports facts, with lock timestamps and undecided outcomes preserved.
- canon/ and approved character lineup for identities; original hashes and renderer HOLD gates remain binding.
- Memo OS for production, Novel OS for manuscript, Atlas for geography.
- governance/release-evidence and publication manifest for release resolution, with derived indices unable to promote canon.

## Required retrieval envelope
Every project-context response must carry: repo, exact path, branch/ref, commit SHA or file blob SHA, retrieval timestamp, authority owner, project scope, evidence status (FACT/PROPOSAL/CONFLICT/STALE/BLOCKED), and applicable controlling gate. Missing attestation is UNKNOWN, never VERIFIED. Authorization filtering occurs before retrieval; no cross-project copy of domain authority.

## Persistence contract
Use Bullpen's receipt classifier for artifact GitHub status and its mission evidence gate only when implemented and verified. DISCUSSED, SIMULATED, CREATED_LOCAL, PUSHED_BRANCH, OPEN_PR, MERGED_MAIN, OPERATIONALLY_VERIFIED are distinct. A merged code PR does not authorize publication, canon promotion, or live runtime acceptance. Never report durable completion without GitHub main readback and domain acceptance.

## Initial witnessed contradiction — hold pending adjudication
The 2026-10-19 repository read found governance/execution-control/TASK_REGISTRY_V1.json describing CHAR-PORT-001 as COMPLETE, asserting 12/12 materialized approved references and setting CHAR-PORT-002 READY. PROJECT_CONTROL_REGISTRY.md instead records Phase 1 Exact Source-Byte Portability HOLD because the active context lacks an authorized raw-byte export/materialization path; renderer binding C1/T15/T16 remain HOLD.
These are not automatically equivalent claims: an earlier source-recovery completion may coexist with a later context-specific renderer-access failure. Librarian must retrieve hashes, dated proofs, branch state and the owning Director's gate ruling, then classify each claim. Until adjudicated, no renderer readiness or publication claim may derive solely from the task registry.

## Integration acceptance tests
1. Fresh ChatGPT/Codex session retrieves current domain authority with commit/blob SHA and citation.
2. Two independent source snapshots with different gating states yield CONFLICT or scope-qualified statuses, not silent overwrite.
3. Unverified PR/branch receipt cannot produce MERGED_MAIN or OPERATIONALLY_VERIFIED.
4. Real Week 6 Memo lookup prefers actual branch/path and rejects fabricated master packet.
5. Twelve owner identities and approved appearance references resolve without bypassing raw-byte/render HOLD.
6. ESPN undecided results cannot become decided without a fact-lock source.
7. Novel scenes and Atlas locations cite approved canon, without project-boundary leakage.
8. Manifest resolution never publishes an unpublished release.
9. Replay of indexing event is idempotent; restart after partial work resumes or truthfully BLOCKS.
10. End-to-end twice: artifact -> pushed branch -> PR -> CI -> independent review -> main readback -> fresh-session Librarian retrieval, with no simulated signoffs.

## Rollout rules
No change to canonical JSON registry or publication manifests without owner review and exact change receipts. Candidate adapter stays non-binding until Bullpen #121 runtime acceptance, Schemin domain gate verification, Umpire independent signoff and merge into main. Preserve all existing HOLDs.
