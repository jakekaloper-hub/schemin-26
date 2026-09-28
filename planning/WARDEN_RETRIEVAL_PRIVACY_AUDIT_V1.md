# Schemin '26 — Warden Retrieval & Privacy Audit V1

**Document class:** review
**Authority / owner:** Warden
**Version:** 1.0
**Status:** ACTIVE — PR #15
**Effective date:** 2026-09-28

## Scope

Targeted audit of:
- committed-secret indicators;
- runtime credential handling;
- Mercer/private-strategy leakage into public creative production;
- high-risk retrieval surfaces.

## Findings

### W-01 — No obvious committed credential found in targeted scan
Targeted repository search included common indicators such as private-key headers, GitHub token prefixes, ESPN private-cookie names, password assignments and API-key assignments.

Observed `api_key` use in `living-novel/os/transports/renderer_transport.py` is runtime environment-variable handling for `RUNPOD_API_KEY`, not a committed credential.

This is a targeted scan, not a full-history secret-scanner certification.

### W-02 — Mercer-to-Chronicle firewall contamination found and fixed
`chronicles/proof-of-concept/prologue/PROLOGUE_PRESEASON_EVIDENCE_AND_EMOTIONAL_SPINE.md` imported private Mercer grades/judgments into a Chronicle evidence packet.

Risk:
- private GM evaluation could become public league/world canon;
- retrieval could treat Mercer opinion as league fact;
- later narrative agents could inherit strategic/private analysis.

Fix:
- retained public ESPN/draft evidence;
- removed Mercer grades and private valuation conclusions;
- inserted explicit firewall language;
- normalized current character titles.

### W-03 — Memo OS firewall doctrine is correct
`memo-os/SCHEMIN_26_WEEKLY_MEMO_OS_V5_2_RC_MUTUAL_IMPLEMENTATION_PATCH.md` explicitly excludes Mercer private recommendations, valuations and exploitation conclusions from public Memo production.

The defect was downstream compliance, not absence of doctrine.

### W-04 — Runtime secrets remain environment-bound
Renderer transport expects `RUNPOD_ENDPOINT_ID` and `RUNPOD_API_KEY` at runtime. No hard-coded value was found in the audited file.

## Retrieval rule

Public creative domains may cite:
- verified league facts;
- published public artifacts;
- Commissioner-approved canon;
- public historical evidence.

They may not automatically import:
- Mercer grades;
- trade targets;
- private valuations;
- opponent exploitation;
- manager-specific negotiation intelligence;
- private recommendations.

If Mercer-derived material is deliberately cleared for public use, the receiving artifact must state the approved public fact/interpretation rather than cite Mercer as authority.

## Warden verdict

**PASS WITH CONTINUING MONITORING.**

One real firewall defect was found and repaired. No obvious committed secret was found in the targeted current-tree scan.
