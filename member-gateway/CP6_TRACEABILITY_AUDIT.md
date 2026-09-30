# CP6 — Requirement / Defect Traceability Audit

**Checkpoint:** CP6 Release-Candidate Hardening  
**Status:** AUDIT BASELINE  
**Rule:** design correction is not runtime closure. A defect is runtime-closed only when implementation and executable evidence cover it.

| Defect | Control / disposition | Evidence state | Later owner if deferred |
|---|---|---|---|
| GW-D001 baseline drift | current project-control docs reloaded before CP6 | TESTED BY PROCESS | Librarian |
| GW-D002 legacy FLA router reuse | Service Core/SCK contracts built independently | IMPLEMENTED+TESTED | — |
| GW-D003 certification ambiguity | explicit NOT_CERTIFIED / staged evidence | IMPLEMENTED+TESTED | Umpire |
| GW-D004 attribution vocabulary | authority_status + qa_status | IMPLEMENTED+TESTED | Librarian/Umpire |
| GW-D005 execution vs delivery | separate workflow/delivery state | IMPLEMENTED+TESTED | — |
| GW-D006 Gateway-as-product | Gateway documented as access boundary | IMPLEMENTED | Agent CP9 |
| GW-D007 intent/authority coupling | capability auth precedes execution | IMPLEMENTED+TESTED | Warden |
| GW-D008 Commissioner/admin conflation | Jake commissioner; no admin class/capability | PARTIAL | CP10 |
| GW-D009 input-only authorization | live client recheck + outflow gate | IMPLEMENTED+TESTED | — |
| GW-D010 re-resolution drift | typed SCK handoff / shared run identity | PARTIAL | CP7/CP11 |
| GW-D011 over-orchestration | semantic capabilities; no Director API | IMPLEMENTED+TESTED | — |
| GW-D012 success ambiguity | workflow/delivery states | IMPLEMENTED+TESTED | Analyst CP15 |
| GW-D013 raw defect count ambiguity | defect escape metrics designed | DEFERRED TELEMETRY | CP15/19 |
| GW-D014 premature SLO | no arbitrary latency SLO | IMPLEMENTED POLICY | Analyst |
| GW-D015 search-authority conflation | Truth Plane required; retrieval not gateway truth | PARTIAL | CP8 |
| GW-D016 generated self-canonization | no mutation/canon capability | IMPLEMENTED+TESTED SURFACE | CP12 |
| GW-D017 canon modality ambiguity | not in first Pittsy slice | OUT OF SLICE | future character capability |
| GW-D018 monolithic bootstrap | capability discovery model | IMPLEMENTED CORE | CP7/9 |
| GW-D019 architecture-first onboarding | member job/capability design | PARTIAL | CP9 |
| GW-D020 connection-count vanity | no connection KPI | IMPLEMENTED POLICY | Analyst |
| GW-D021 call-cost fixation | targeted recovery doctrine | PARTIAL | CP11/15 |
| GW-D022 unbounded consumption | idempotency exists; rate/concurrency limits pending | PARTIAL | CP7/12 |
| GW-D023 retain-everything | minimal run ledger | PARTIAL | CP12/19 retention audit |
| GW-D024 public/open-source conflation | explicit doctrine | POLICY ONLY | Commissioner General CP13/14 |
| GW-D025 access/redistribution conflation | provider rights not assumed | POLICY ONLY | Commissioner General CP13/14 |
| GW-D026 AI rights shortcut | provenance preserved | PARTIAL | Commissioner General |
| GW-D027 principal collapse | human/member/client split | IMPLEMENTED+TESTED | — |
| GW-D028 client permanence | revoke/rotate tests | IMPLEMENTED+TESTED | — |
| GW-D029 role proliferation | no Gateway Director #19 | IMPLEMENTED POLICY | — |
| GW-D030 Director-domain drift | Scout Master excluded from resilience | CORRECTED+DOCUMENTED | Closer |
| GW-D031 premature commercialization | explicitly out of scope | IMPLEMENTED POLICY | — |
| GW-D032 speculative SaaS | narrow Jake/Pitts slice | IMPLEMENTED POLICY | — |
| GW-D033 transport-as-architecture | transport-independent Service Core | IMPLEMENTED+TESTED CORE | CP7 |
| GW-D034 resilience ownership ambiguity | CP6-19 owner map | IMPLEMENTED CONTRACT | CP11 |
| GW-D035 overbuild | narrow capabilities/vertical slice | IMPLEMENTED | — |
| GW-D036 state-store conflation | run ledger separate from truth/provider state | PARTIAL | CP11/12 |

## CP6 blockers vs deferrals

No item marked PARTIAL or DEFERRED may be silently represented as production-closed.

Expected pre-RC implementation checkpoints:
- CP7 closes transport-facing portions of D010/D018/D022/D033.
- CP8 closes current Truth Plane portions of D015.
- CP9 closes member UX portions of D006/D019.
- CP10 closes D008.
- CP11 closes resilience/economics portions of D010/D021/D034/D036.
- CP12 closes security portions of D016/D022/D023/D036.
- CP13 independently determines whether policy/rights items are sufficient for the exact release scope.

GW-D017 remains outside the initial Pittsy slice because the first release does not expose a character-rendering capability. It becomes mandatory before any external character-rendering capability is promoted.
