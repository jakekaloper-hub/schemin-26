# Schemin '26 — Main Branch Visibility & Release Reconciliation

**Audit date:** 2026-11-20  
**Review window:** 2026-10-21 through 2026-11-20  
**Disposition:** AUDIT / BRANCH DISCOVERY; **not** a canon or publication promotion.

## One source-of-truth rule

- `main` is the canonical **accepted repository state**, not a claim that every file or artifact it contains is released. An artifact is released only through its owning source, canon, QA and publication gates.
- Open pull requests contain visible **in-progress/proposed** changes and must not masquerade as `main`. Draft, HOLD, noncanon and preview status remain binding.
- Old feature branches should not be deleted or merged merely for existing; compare unique commits and preserve provenance. A branch without an open PR is **not proof of missing work**.
- All new substantial work should enter a linked PR promptly, with explicit parent/base for stacked work. Never silently merge a stack or bypass independent QA.

## Live discovery entry points

- **Authoritative code:** [main](https://github.com/jakekaloper-hub/schemin-26/tree/main)
- **Current open PRs and draft candidates:** [all open pull requests](https://github.com/jakekaloper-hub/schemin-26/pulls?q=is%3Apr+is%3Aopen)
- **Branch list:** [branches](https://github.com/jakekaloper-hub/schemin-26/branches)
- **Daily read-only status report:** [Operational Convergence Drift Inventory workflow](https://github.com/jakekaloper-hub/schemin-26/actions/workflows/operational-convergence-inventory.yml) (latest workflow run -> `operational-pr-inventory` artifact and job summary).
- **Current main protection blocker:** [#330](https://github.com/jakekaloper-hub/schemin-26/issues/330)

The read-only inventory script, `governance/execution-control/pr_reconciliation.py`, now lists all remote branches, PR heads and nested bases, and reports unmatched branch refs. Its counts and names are **metadata only**; a comparison against `main`, last commit date, PR ancestry and source/provenance is still required before calling any code missing, stale, merged, or safe to delete.

## Snapshot before the visibility patch

At first inspection on 2026-11-20: **298 total branches; 32 open PRs (29 drafts, 3 non-drafts); 265 branches not used as a head or base of an open PR**. GitHub reported `main` at `5a6af79107a122b36299e6c34aec86c7d764b501` and **`protected: false`**.

While the audit ran, draft PRs [#324](https://github.com/jakekaloper-hub/schemin-26/pull/324) and [#325](https://github.com/jakekaloper-hub/schemin-26/pull/325) appeared for active Atlas branches. The previously untracked Week 11 story-room branch was then made visible as draft [#326](https://github.com/jakekaloper-hub/schemin-26/pull/326). This brought the open count to **35**; inventory counts will continue to change. Use the live entry points, not these dated baseline numbers, for a later checkup.

## Active dependency and HOLD register

| Workstream / accountable owning domain | GitHub PR graph | Audit ruling |
|---|---|---|
| Story Graph + Commonwealth reader — Architect, Librarian, Umpire | [#307](https://github.com/jakekaloper-hub/schemin-26/pull/307) → [#309](https://github.com/jakekaloper-hub/schemin-26/pull/309) → [#314](https://github.com/jakekaloper-hub/schemin-26/pull/314) | Checks reported green; independent code/Umpire signoff and website acceptance not complete. No merger of descendants first; no deployment claim. |
| Older Commonwealth reader candidate — Architect / Site | [#236](https://github.com/jakekaloper-hub/schemin-26/pull/236) → [#237](https://github.com/jakekaloper-hub/schemin-26/pull/237) | Historically stale donor path; [#309](https://github.com/jakekaloper-hub/schemin-26/pull/309) reports selective recovery rather than blind rebase. Requires provenance-based supersession disposition, not merge. |
| Week 10 → Week 11 story room — Memo OS / Librarian | [#315](https://github.com/jakekaloper-hub/schemin-26/pull/315) → [#326](https://github.com/jakekaloper-hub/schemin-26/pull/326) | Draft, PNG/publication paused; #326 is a one-commit stack over #315 at audit. |
| Current Week 11 sports intake — Data Gateway / Memo OS | [#313](https://github.com/jakekaloper-hub/schemin-26/pull/313) | Evidence intake under PUBLICATION HOLD and steward/QA gates; CI green does not create approved facts or images. |
| Historical intake lineage — Data Gateway | [#312](https://github.com/jakekaloper-hub/schemin-26/pull/312) | Open reviewable PR, but text explicitly requires independent technical review and lacks authenticated steward acceptance. No merge. |
| Postseason island — World / Atlas / Historical Scout | [#321](https://github.com/jakekaloper-hub/schemin-26/pull/321), [#322](https://github.com/jakekaloper-hub/schemin-26/pull/322) → [#325](https://github.com/jakekaloper-hub/schemin-26/pull/325) | Alternative/divergent historical proposals and staged expansion. **#322 preproduction validation failed** at audit. Reject blind canonical promotion. |
| Separate location summit — Atlas / Librarian | [#324](https://github.com/jakekaloper-hub/schemin-26/pull/324) | 111 dossiers and 40 additional candidate sites; independent audit/source/physical promotion gate still outstanding. Conflicts with stacked island proposals require explicit reconciliation. |
| Memo fixture release validator — Umpire / Memo OS | [#278](https://github.com/jakekaloper-hub/schemin-26/pull/278) | Draft with explicit real-raster QA and final acceptance HOLD; may be code-salvage candidate, not published-art acceptance. |

The connected repository already contains its Repository Merge Gate and path-scoped CI. Passing these checks is **necessary but not sufficient** for independent editorial, canonical, release or deployment acceptance. [#330](https://github.com/jakekaloper-hub/schemin-26/issues/330) tracks the enforceability gap in GitHub settings.

## Bullpen ownership and execution semantics

Canonical owners are defined in [Bullpen Core](https://github.com/jakekaloper-hub/bullpen), not recreated here:

- **Librarian:** evidence hierarchy, branch/PR provenance and dated inventory.
- **Architect / Setup Man:** merge mechanics, CI, branch dependencies, rules and technical repairs.
- **Umpire:** independently challenge promotion, unknown states, conflicts, reproducibility and release claims.
- **Closer:** final accepted integration, only after gates.
- **Scout, Memo OS, World/Atlas, Character and author/creative roles:** project-domain review where affected.

These are **routing responsibilities**; naming a role in a report is not evidence an independently invoked agent performed a review.

## Contract for future "check up / check repository" requests

1. Read the exact latest `main` head and controlling `PROJECT_CONTROL_REGISTRY.md`.
2. Refresh all open PRs, draft flags, base/head ancestry, checks, reviews, and explicit HOLD notes. Read the newest daily branch inventory.
3. For recent branches outside PR chains, compare unique commits and content against `main`; open a visible draft PR for material active code, or document historic/redundant disposition. No premature deletion.
4. Merge only review-approved, source-correct, nonconflicting work with exact-head CI and owning release gates. Retarget stacked descendants only after parents land.
5. Identify held material by GitHub URL, responsible domain, exact blocker and next verifiable gate. Never call it available on `main` until it is.
6. Update the dated audit record when material findings change; preserve older evidence and never silently rewrite canon.

**Repository mutation in this patch:** read-only branch discovery, automated reporting/tests and a visible navigation/decision record. It does not change league data, creative canon, world geography, published memos, or a site's deployment.
