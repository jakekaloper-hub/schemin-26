# Unlinked Branch Triage — 20 November 2026

This is a one-time domain/risk disposition for the **24** non-main branch names that did not match any same-repository pull-request record in the dated visibility snapshot. All compare numbers are relative to the `main` HEAD observed during the audit; concurrent changes may alter them.

**Interpretation:** `ahead` is Git commit ancestry, *not* necessarily unique content. Do not treat an unlinked or divergent branch as an approved release. `behind only` proves the branch is an ancestor of `main`, not that it may be deleted without archive-policy review.

| Branch | Compared with main | Classification / action |
|---|---|---|
| `character-12of12-integrity-2026-10-05` | 0 ahead / 1,418 behind | Already ancestor; no content promotion |
| `memo/week6-v52rc-intake-20261018` | 0 ahead / 1,282 behind | Already ancestor; no content promotion |
| `fix/memo-p0-steward-gates-20261029` | 2 ahead / 56 behind; **0 changed files** | No net tree change; source lineage check, no merge need evidenced |
| `data/live` | 232 ahead / 2,010 behind; 2 snapshot files | Intentional isolated data refresh surface; DO NOT wholesale merge |
| `governance/repository-visibility-20261120` | Audit branch, subsequently tracked by PR #333 | Inventory-time self-reference; expected to disappear after refresh |
| `mission/week7-renderer-gates-20261027` | 61 ahead / 62 behind; 57 files | **P1 selective salvage** — Week 7 renderer/QA receipts; compare against adopted newer Memo OS controls |
| `archive/week7-preproduction-library-20261026` | 1 ahead / 65 behind; 9 files | Historic source-preservation candidate; Librarian reconcile |
| `week7/phase4-editorial-20261027` | 3 ahead / 60 behind; 3 files | Week 7 editorial provenance; selectively archive or link |
| `preproduction/week-7-pittys-book-press-conference-20261026` | 1 ahead / 65 behind; 1 file | Historical Pittsy's Book candidate; not current episode release |
| `bullpen/week4-cover-sandbox-acceptance` | 1 ahead / 1,475 behind; 1 file | Old sandbox acceptance record; historical HOLD |
| `bullpen/week5-readiness-reconciliation` | 1 ahead / 1,308 behind; 2 control files | Superseded-control candidate; no Project Registry overwrite |
| `week5-readiness-reconciliation` | 1 ahead / 1,308 behind; 2 control files | Similar Week 5 control candidate; compare overlap with Bullpen branch |
| `memo/week4-publication-fidelity-acceptance` | 2 ahead / 1,506 behind; 2 files | Historical publication receipt candidate; gate review required |
| `week4-preart-lock-qa-2026-10-05` | 3 ahead / 1,405 behind; 3 files | Historical pre-art receipt; no retroactive publication |
| `week4-production-packet-revalidation-2026-10-05` | 1 ahead / 1,408 behind; 1 file | Historical packet; Commissioner/source review |
| `mission/week4-fresh-operator-evidence-2026-10-01` | 2 ahead / 1,522 behind; 2 files | Older source/ESPN evidence; preserve historical source date |
| `week5-preproduction-story-lock-20261011` | 3 ahead / 1,297 behind; 3 files | Historical story lock; compare against released Memo canon |
| `mission/chapter-i-golden-path-canary` | 3 ahead / 1,633 behind; 3 files | Historical Chapter I candidate, not auto-canonical |
| `strengthen/universe-os-v1-2-atlas-p1-hardening-2026-09-30` | 58 ahead / 1,533 behind; 57 files | **P1 World/Atlas supersession audit**; older subsystem source must not replace main |
| `universe-os-v1-2-atlas-v2` | 41 ahead / 1,630 behind; 41 files | Older ontology/Atlas proposal; World authority reconciliation |
| `world/canonical-world-plate-preproduction-2026-09-30` | 35 ahead / 1,633 behind; 33 files | Historical World plate; compare source receipt before reuse |
| `world/universe-ontology-travel-v2-2026-09-29` | 9 ahead / 1,689 behind; 7 files | Older travel/ontology; no unsafe overwrites |
| `world/universe-os-v1-2-2026-09-30` | 6 ahead / 1,633 behind; 6 files | Historical Universe exports; verify archival rather than promotion |
| `world/universe-os-v1-2-atlas-control-2026-10-01` | 59 ahead / 1,632 behind; 59 files | **P1 supersession review**; older control-plane implementation |

## Assigned next gates

- **Librarian:** record source disposition for the unique historical evidence and source-only materials; preserve in approved archive structure rather than delete.
- **Setup Man + Atlas/World owner:** diff and selectively test 4 larger World/Universe branches against current adopted World Engine, without reverting newer canon.
- **Memo OS owner + Scout:** compare the Week 7 renderer/production branches and provider receipts; do not upgrade unverified image/ESPN states.
- **Umpire:** independently challenge any release or canon promotion.
- **Closer:** integrate only passed, non-conflicting portions through bounded PRs.

No branch deleted, force-pushed, or indiscriminately merged. The recurring ledger is the live inventory; this document preserves the snapshot's evidence and judgments.
