#!/usr/bin/env python3
"""Fail source preflight if any of the six Week 11 matchup-ending pages lacks a verifiable final-result banner contract. This DOES NOT inspect pixels."""
import json
from pathlib import Path

BASE=Path(__file__).resolve().parent
def load(filename):
    return json.loads((BASE/filename).read_text(encoding="utf-8"))

contracts=load("W11_SIX_MATCHUP_FINAL_RESULT_BANNER_CONTRACT_2026-11-24.json")["endings"]
allpages=load("W11_ALL_35_INTEGRATED_RENDER_INPUTS_2026-11-24.json")["pages"]
cuts=load("W11_POST_MNF_ALL_35_FOLIO_SELECTED_CUTS_2026-11-24.json")["folios"]
actii=load("W11_ACTII_P09_GOLD_STANDARD_14_FOLIO_ART_DIRECTION_2026-11-24.json")["folios"]
byfolio={x["internal_folio_id"]:x for x in allpages}
bycut={x["folio"]:x for x in cuts}
byact={x["id"]:x for x in actii}
expected_ids=["F11","F13","F16","F18","F20","F22"]
assert [x["folio"] for x in contracts]==expected_ids, "six consecutive game payoff IDs must be exact"
for c in contracts:
    page=c["folio"]
    fact=bycut[page]["complete_event_data"]
    winning = fact["away"] if fact["winner"]==fact["away"]["name"] else fact["home"]
    losing = fact["home"] if fact["winner"]==fact["away"]["name"] else fact["away"]
    expected=f'{winning["name"]} {winning["score"]:.2f}  •  {losing["name"]} {losing["score"]:.2f}'
    assert c["exact_banner"]==expected, page+" official score mismatch"
    artifact=byfolio[page].get("final_result_banner",{})
    assert artifact.get("required") is True and artifact.get("text")==expected, page+" missing required final-score packet"
    act=byact[page].get("closing_score_banner",{})
    assert act.get("required") is True and act.get("exact")==expected, page+" missing finale art direction"
    assert artifact.get("real_image_check"), page+" missing independent actual-pixel review obligation"
    assert artifact.get("no_page_ids") is True, page+" printed production page number prohibited"
p11=load("render-inputs/W11-P11/request.json")
assert p11.get("final_score_banner",{}).get("mandatory") is True, "P11 request lacks mandatory score plaque"
assert p11["final_score_banner"]["exact_source_display"]==contracts[0]["exact_banner"], "P11 prompt mismatch"
assert "RENDER HARD VETO — ENDING SCORE BANNER" in p11["prompt"], "P11 missed render instruction"
print("PASS: 6/6 canonical winner/loser score-banner source handoffs and 2-decimal data; P11 render hard veto present")
print("NOTE: actual image acceptance remains human/independent QA and must not be inferred from this PASS")
