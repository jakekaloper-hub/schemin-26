# Member AI Gateway — Checkpoint Program CP6–CP19

**Status:** ACTIVE PROGRAM / CP6 RUNNING  
**Branch:** `feat/member-ai-gateway-phase1`  
**Promotion rule:** every checkpoint executes PLAN → IMPLEMENT → TEST → INDEPENDENT AUDIT → DEFECT REPAIR → RETEST → EVIDENCE FREEZE → PROMOTE/BLOCK.

No downstream checkpoint inherits PASS. No production claim may exceed executable evidence.

## Command map

| Domain | Bullpen authority | Program responsibility |
|---|---|---|
| Executive promotion | The Closer | promotion/block decisions, cross-domain arbitration |
| Operations | The Groundskeeper | cadence, workflow lifecycle, recovery, pilot operations |
| Architecture | The Architect | topology, boundaries, state separation |
| Runtime | The Setup Man | adapters, transport, deployment/runtime contracts |
| Security | The Warden | authn/authz, revocation, isolation, outflow, secrets |
| Independent QA | The Umpire | adversarial tests, regression, certification veto |
| League truth | The Scout | ESPN/Flaim/Data Gateway freshness and truth contracts |
| Knowledge | The Librarian | provenance, status/version resolution, supersession |
| Analytics | The Analyst | clean-task completion, defect escape, pilot telemetry |
| Economics | The Bookkeeper | retries, duplicate work, recovery/cost controls |
| Rights | Commissioner General | provider/publication rights and public/private boundary |
| Member UX | The Agent | onboarding, capability discovery, understandable failure states |
| Growth | Scout Master | controlled adoption only after reliability; not resilience |

## CP6 — Release-Candidate Hardening
**Lead:** Closer. **Owners:** Architect, Setup Man, Warden, Librarian. **Independent gate:** Umpire.

Deliverables:
1. trace implemented controls against the 36 design defects;
2. classify each item IMPLEMENTED / TESTED / DEFERRED / OUT-OF-SCOPE;
3. reconcile branch against current Project Control Registry, Authority Matrix and Source of Truth;
4. run all Gateway tests plus existing Bullpen regression CI;
5. freeze exact commit evidence and deferred-requirement register.

Exit: no unknown critical requirement; all deferred items have owner + later checkpoint; CI green. Promotion is only to hardened implementation candidate.

## CP7 — AI Transport Integration
**Lead:** Setup Man. **Architecture:** Architect. **Security:** Warden. **QA:** Umpire.

Implement one thin AI-native adapter, MCP-first only if current supported authentication/tool contracts validate cleanly. Transport may expose semantic capabilities but never Directors, raw providers, canonical mutation or private domains.

Tests: capability discovery, auth before invocation, schema validation, unknown-tool fail-closed, disconnect behavior, transport cannot alter Service Core authority.

Exit: same Service Core tests pass through adapter; transport-specific tests green.

## CP8 — Live Truth Integration
**Lead:** Scout. **Runtime:** Setup Man. **Provenance:** Librarian. **QA:** Umpire.

Exercise current ESPN/Flaim acquisition through existing Data Gateway into the Gateway. Do not let Member Gateway fetch providers independently.

Tests: fresh success, provider failure, LKG fallback, stale metadata, contract break, provenance, no overwrite of LKG on invalid capture.

Exit: fresh current-state claim only when freshness evidence proves it; degraded states explicit.

## CP9 — Real Pitts Acceptance
**Lead:** Agent. **Ops:** Groundskeeper. **Truth:** Scout. **Security:** Warden.

Connect Pitts's actual external client to approved capabilities. First job: current Pittsy's Book inputs. Schemin supplies governed inputs; Pittsy owns lines/odds/wagers/ledger/presentation.

Tests: real auth, capability discovery, one successful job, duplicate submission, understandable stale/degraded response, no Mercer/repo mutation/Director access.

Exit: Pitts completes the job without manual architecture knowledge or privilege leakage.

## CP10 — Jake Acceptance + Private Isolation
**Lead:** Warden. **Product:** Agent. **QA:** Umpire.

Exercise Jake's Commissioner client while preserving Commissioner/admin distinction and Mercer-private separation.

Tests: Commissioner capabilities, member-equivalent shared path, explicit denial of Mercer through shared Gateway, no cross-member private context, no accidental admin mutation.

Exit: broader Jake access does not weaken member boundaries.

## CP11 — Failure & Recovery Certification
**Lead:** Groundskeeper. **Runtime:** Setup Man. **Truth:** Scout. **Cost:** Bookkeeper. **QA:** Umpire.

Chaos/failure matrix: provider outage, malformed capture, SCK dependency block, transport disconnect, delivery retry, duplicate/replay, run-store interruption, stale fallback, partial dependency failure.

Exit: smallest invalid subtree is retried; completed authoritative work is not unnecessarily rerun; unrelated capabilities remain isolated.

## CP12 — Security Certification
**Lead:** Warden. **Independent attack:** Umpire.

Production threat suite: impersonation, revoked/rotated client, scope escalation, injection, provider-as-instruction, private-context smuggling, cross-member leakage, mid-run revocation, replay, secret exposure, unauthorized outflow, repo mutation attempts.

Exit: critical false authorization = zero in certification suite; security ambiguity fails closed.

## CP13 — Independent Umpire Certification
**Lead:** Umpire only. Producers provide evidence but do not certify themselves.

Build requirement → implementation → test → evidence traceability. Re-run exact candidate. Verify no PASS exceeds evidence. Review CP6 deferred register.

Exit: CERTIFY or BLOCK exact commit.

## CP14 — Formal Release Candidate
**Lead:** Closer. **Release controls:** Groundskeeper + Umpire + Warden.

Freeze exact certified commit/tag/status. Update durable docs and project-control entry. No feature changes after freeze without reopening relevant gates.

Exit: formal RC, not production.

## CP15 — Controlled Pilot
**Lead:** Groundskeeper. **Member UX:** Agent. **Metrics:** Analyst. **Security:** Warden.

Pilot population: Jake + Pitts. Run real member jobs for a bounded period. Measure clean-task completion, retries, defects, freshness, latency, cost, manual rescue and security events.

Exit: enough representative evidence to judge promotion; all pilot defects logged.

## CP16 — Pilot Remediation
**Lead:** Closer/Groundskeeper by defect domain. **QA:** Umpire.

Route each pilot defect to owning Director. Repair smallest affected dependency, add regression test, rerun impacted suites plus full release suite.

Exit: no unresolved promotion-blocking pilot defect.

## CP17 — Production Promotion
**Lead:** Closer. **Veto:** Umpire/Warden/domain authority where applicable.

Promote only exact certified/remediated version. Merge/release controls, rollback point, project-control update, production evidence receipt.

Exit: Gateway ACTIVE for approved initial member population.

## CP18 — League Rollout
**Lead:** Agent. **Security:** Warden. **Ops:** Groundskeeper. **Analytics:** Analyst. **Growth:** Scout Master only after reliability is demonstrated.

Add members via durable human identity + delegated client + authorized scopes. No copied monolithic Bullpen prompt. Capability discovery drives onboarding.

Exit: approved league cohort onboarded without weakening isolation or supportability.

## CP19 — Post-Launch Governance
**Lead:** Groundskeeper + Analyst. **Executive:** Closer. Domain owners retain their authority.

Continuously evaluate clean task completion, Jake-discovered preventable defects, defect escape stage, freshness, authorization failures, duplicate work, recovery, cost and member friction. Feed defects into versioned regression and targeted patches.

Exit: this checkpoint is an operating loop, not a one-time terminal PASS.

## Promotion doctrine

CP6–CP13 prove the system. CP14 freezes it. CP15–CP16 prove it with real users and repair findings. CP17 activates it. CP18 broadens access. CP19 governs it.

Commercialization remains outside this program unless separately authorized after reliable league operation.
