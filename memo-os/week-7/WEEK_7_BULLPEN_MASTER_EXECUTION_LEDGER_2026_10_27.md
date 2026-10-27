# Week 7 — Bullpen Master Execution Ledger

**State:** ACTIVE ENGINEERING / RENDER HOLD. **Source:** PR #256 at bd8f3a7. **No new storylines.**
**Execution:** isolated local worktree `~/Developer/ai/week7-renderer-gates`; do not modify dirty Bullpen checkout.

## Controlling source
Founder 34 decisions; six Revision 2 three-phase manuscripts; Founder six-venue authorization; 28-folio source-copy split and V2 packets; Miracle Putt P005–P007 pilot; fifteen other matchup and ten editorial cinematic input packets. Original sources remain authoritative.

## Stage gates and evidence
| Gate | Owner / counterweight | Acceptance proof | State |
|---|---|---|---|
| G0 source inventory | Librarian / GM | 28 candidate folios mapped to 3+15+10 existing render inputs; source refs | PASS inventory only |
| G1 two-subject binding | Architect / Umpire | renderer capability receipt, mounted-byte SHA, subject-to-reference map, durable output lineage | HOLD |
| G2 Atlas and characters | World / Scout | approved event subsites, route state, Oct18 active plates, correct DK anatomy | PARTIAL |
| G3 Miracle Putt pilot | Production / Visual | native 1024x1536 PNG from P005, with two subject receipts | NOT RUN |
| G4 raster QA | Visual / Copy | identity inspection, exact deterministic text, actual 390px downscale | NOT RUN |
| G5 independent Umpire | Umpire separate from implementer | signed evidence review with fail-closed verdict | NOT RUN |
| G6 remaining folios | Production / Librarian | gated batches, 28-folio coverage, hashes and revisions | NOT RUN |
| G7 publication | Release / Umpire | actual PDF, manifest, mobile, source and independent signoffs | NOT RUN |

## G1 hard requirements
- Reference A CHAR-PHILLIP-PITTS: `canon/characters/assets/lineups/2026-10-18-crops/CHAR-PHILLIP-PITTS.png`, SHA256 `0c6d6ee2cdd1c1f77c58cda2e5e25c0b482943279e433b16e14aa1277e201a65`.
- Reference B CHAR-ZACH-WILSON: `canon/characters/assets/lineups/2026-10-18-crops/CHAR-ZACH-WILSON.png`, SHA256 `c0ac1b3314c32b8e85c82045268c21a0d9c52525c2fd8ad869aaff449b4cf36a`.
- Existing `canon/characters/runtime/renderer_capabilities.py` must remain fail-closed. Current route `CURRENT_CHATGPT_IMAGE_RENDERER` has `NO_PRODUCTION_ROUTE_PROVEN`.
- Do not use stale DK library handle, generic text-to-image fallback, invented proof, or an unsupported provider.
- A source SHA match is not a mounted-reference or per-subject binding receipt.

## Independent Umpire review contract
Umpire must inspect implementation evidence independently from the authoring agent. Reject if no attached-reference lineage, if image identity drifts, if venue is unapproved, if final illustrated raster was not inspected, or if a provisional fact is described as certified. A simulated checklist is not an authenticated independent execution.

## Production timing policy
Start timing only when G1/G2 allow the P005 pilot. Record per-page actual start/end, provider, cost/credits, attempts, QA/revision duration. No estimated schedule or credit burn presented as measured fact. After first accepted pilot, forecast remaining 27 pages using observed median throughput and revision rate, with uncertainty range. No automated full-batch render before pilot acceptance.

## Operational commands
- Character tests: `PYTHONPATH=memo-os/tests python3 -m unittest discover -s memo-os/tests -p test_validate_character_provenance.py`
- Scene tests: `PYTHONPATH=memo-os/tests python3 -m unittest discover -s memo-os/tests -p test_scene_direction.py`
- Masi routing: `PYTHONPATH=memo-os/tests python3 -m unittest discover -s memo-os/tests -p test_frank_masi_packet_routing.py`
- Creative DNA: `python3 memo-os/creative-dna/validate_creative_dna.py --packet memo-os/week-7/WEEK_7_CREATIVE_DNA_PROVISIONAL_PACKET_2026_10_27.json`

## Recovery checkpoints
Source: PR #256. Current branch: mission/week7-renderer-gates-20261027. Preserve all original files. Track each attempted adapter by evidence receipt and failure reason. Never auto-promote to PASSED.
