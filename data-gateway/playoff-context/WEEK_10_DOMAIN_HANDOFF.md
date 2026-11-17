# Week 10 playoff analytics — domain handoff

**Scope:** Connect the existing playoff-context capability to existing Memo OS consumers under the established Bullpen and publication authorities.

**Status:** Code and synthetic regression coverage are provided here. Forecast publication remains held. The full routing receipt is retained locally pending approval for disclosure; no external Director acknowledgement or publication approval is claimed.

## Project assignment

The Analyst is the primary owner of this quantitative work. This is an assignment within the existing organization, not a new Director or a change to Bullpen Core authority.

| Responsibility | Accountable authority | Required handoff |
|---|---|---|
| Source acceptance, league identity, rules, freshness and result finality | Scout / Data Gateway | Accepted input snapshot and rule evidence |
| Statistical method, metric definitions, uncertainty and model validation | Analyst / CAO | Reproducible calculation and explicit limitations |
| Runtime, source validation and consumer boundaries | Architect | Verified implementation and regression coverage |
| Candidate selection, wording and placement | Beat Writer / Memo Editor | Material evidence in existing page contracts |
| Production fit and provenance | Groundskeeper and Librarian | Preserved page structure and source-to-page trace |
| Independent acceptance and release | Umpire and existing Memo release authorities | Evidence-backed review and the normal release disposition |
| Cross-domain integration | GM / Closer | Coordinated handoff and explicit unresolved dependencies |

The public project references are [Bullpen responsibilities](../../bullpen/README.md), the [Bullpen Command Adapter V2](../../docs/architecture/BULLPEN_COMMAND_ADAPTER_V2.md), and the existing [Director project review](../../bullpen/SCHEMIN_26_BULLPEN_FULL_PROJECT_REVIEW.md). These preserve the distinction between canonical organization and Schemin-specific assignments.

## Existing Week 10 consumers

[PR #315](https://github.com/jakekaloper-hub/schemin-26/pull/315) remains the Week 10 production authority. The analytics adapter attaches candidate context to a derived copy of its existing previs. It does not add pages, replace approved copy, select GOTW, certify Fact Lock or advance release state.

| Existing page | Optional analytics context |
|---|---|
| W10-P27 | Official standings observations with source qualifiers |
| W10-P28 | Division context |
| W10-P29 | Disclosed descriptive scoring comparisons |
| W10-P30 | Playoff picture and separately classified evidence |
| W10-P31 | Remaining fixtures and next-week context |
| W10-P35 | Supporting GOTW stakes; selection remains editorial |

Later issues supply their own page bindings. The adapter checks league, season, issue week and unique page identities before attachment.

## Operating handoff

1. Scout accepts a complete, current source capture and the applicable league rules. The runner verifies cutoff, finality, identity, records, score totals and unstarted remaining fixtures.
2. Analyst runs the calculation and validation with recorded input, rule and code hashes, trial counts and random seed. Descriptive comparisons, probabilistic estimates and exact proofs retain separate classifications.
3. The Memo adapter rechecks freshness and identity. While forecast eligibility is false, it passes descriptive fields and removes model probabilities, simulated seed/win distributions and conditional leverage.
4. Memo Editor selects useful candidates in the existing page contracts. A sampled zero is not an elimination proof, and descriptive schedule effects do not establish skill or causation.
5. Independent review and the normal Memo production gates control acceptance and release. Passing synthetic tests does not establish predictive accuracy or publication approval. Missing optional analytics leaves the verified Memo production path usable.

The public code package excludes source captures, participant results, completed run reports and hydrated production packets. Authorized inputs and local run evidence remain separate from the reusable implementation. See [INTEGRATION_CONTRACT.md](INTEGRATION_CONTRACT.md), [EDITORIAL_POLICY.md](EDITORIAL_POLICY.md), and [ACCEPTANCE_REPORT.md](ACCEPTANCE_REPORT.md) for the operating boundaries.
