# Schemin '26 — Enforcement Policy Coverage Matrix V1

**Document class:** control support  
**Authority / owner:** Librarian + Umpire  
**Version:** 1.0  
**Status:** ACTIVE  
**Effective date:** 2026-09-28

| Policy | Domain | Severity | Mode | Enforced failure class | Current state |
|---|---|---|---|---|---|
| SYS-001 | Enforcement kernel | BLOCK | MERGE | malformed/duplicate policy registry; missing validator/source authority | ENFORCED |
| CANON-001 | Character canon | BLOCK | MERGE | owner/title drift; missing invariants; wrong master/visual lock | ENFORCED |
| AUTH-001 | Authority/supersession | BLOCK | MERGE | duplicate active masters/registries; resurrected handoffs; malformed archive quarantine | ENFORCED |
| TEMP-001 | Temporal state | BLOCK | MERGE | V1–V3 losing superseded status; V4 losing parent distinction; Mercer history becoming standing instruction | ENFORCED |
| FIREWALL-001 | Mercer firewall | BLOCK | MERGE | private Mercer grades/calls/valuations entering public creative surfaces | ENFORCED |
| PROMPT-001 | Prompt governance | BLOCK | MERGE | active prompt references retired canon/title/handoff paths | ENFORCED |
| PUB-001 | Publication | RELEASE_BLOCK | RELEASE | explicit RELEASED claim without release-registry evidence | ENFORCED |
| EXC-001 | Exceptions | BLOCK | MERGE | malformed, expired, unauthorized or impossible exception | ENFORCED |
| DATA-001 | Data Gateway | WARN | AUDIT | PR #12 hardening not integrated / data-live & freshness contract incomplete | ENFORCED AS WARNING |
| SEC-001 | Security | BLOCK | MERGE | token/private-key/private ESPN credential signatures | ENFORCED |
| HIST-001 | Historical evidence | BLOCK | MERGE | TO VERIFY/history map promoted into stale current identity authority | ENFORCED |
| INDEX-001 | Index integrity | BLOCK | MERGE | missing active indexes or retired authority referenced by active index | ENFORCED |

## Known manual / external controls

Some controls cannot yet be fully machine-enforced from this branch:
- repository visibility is resolved by Commissioner approval of public architecture; security/private-data controls remain mandatory;
- branch-protection admin settings;
- exact binary materialization of the Commissioner-approved character plate;
- official Week 2 source is recovered; exact raw-byte GitHub import remains a transport task;
- recovery of the original V5.1 patch;
- real post-merge ESPN data/live operational proof.

These remain explicit external gates, not hidden PASS assumptions.
