#!/usr/bin/env python3
"""Fail-closed verification of Week 10 film board facts, timing, references, advisory status."""
from pathlib import Path
import hashlib
import json
from collections import Counter

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
PRE=ROOT/"memo-os/week-10/preproduction"
j=json.loads((HERE/"film_storyboard_v1.json").read_text())
original=json.loads((PRE/"render-inputs/manifest.json").read_text())
delivery=json.loads((HERE/"SHOT_DELIVERY_REGISTER.json").read_text())
reconciled=json.loads((HERE/"METHOD_LENS_RECONCILIATION.json").read_text())
assignment=json.loads((HERE/"METHOD_LENS_WORKSHOP_INPUT.json").read_text())

assert j["status"]=="CANDIDATE_NO_RENDER_OR_RELEASE_APPROVAL"
assert j["runtime"]["target_seconds"]==1800 and j["runtime"]["target_timecode"]=="00:30:00"
assert len(j["scenes"])==original["page_count"]==34
assert j["scene_order"]==[x["page_id"] for x in original["pages"]]
assert j["scene_order"][18]=="W10-P34" and j["scene_order"][-2:]==["W10-P35","W10-P33"]
assert "W10-P32" not in j["scene_order"]
assert j["runtime"]["shot_count"]==186
assert j["runtime"]["verified_source_primary_beats"]==66
assert j["runtime"]["memo_copy_words"]==2278

cursor=0
shots=[]
refs={}
seen_source=set()
for p,s in zip(original["pages"],j["scenes"]):
    assert s["folio"]==p["page_id"]
    assert s["order"]==p["reading_position"]
    assert s["start_s"]==cursor
    path=PRE/p["request"]
    assert hashlib.sha256(path.read_bytes()).hexdigest()==s["source_sha256"]==p["request_sha256"]
    pkt=json.loads(path.read_text())
    assert pkt["publication_copy"]==s["publication_copy"],"Source copy mutated"
    assert pkt["scene"]["encounter"].get("venue_id")==s["setting"]["venue_id"]
    assert len(pkt["scene"]["visual_storytelling"]["shots"])==s["source_primary_beats"]
    for source in pkt["scene"]["visual_storytelling"]["shots"]:
        seen_source.add(source["id"])
    assert s["narration_at_145wpm_s"]+8<=s["duration_s"]
    assert s["characters"]==p["characters"]
    t=cursor
    for sh in s["shots"]:
        assert sh["start_s"]==t and sh["end_s"]>t
        assert sh["may_change_canon"] is False
        assert sh["source_beat_id"] in [beat["id"] for beat in pkt["scene"]["visual_storytelling"]["shots"]]
        assert sh["asset_status"]=="CANDIDATE_UNRENDERED"
        shots.append(sh["id"])
        t=sh["end_s"]
    assert t==s["end_s"]
    assert sum(sh["duration_s"] for sh in s["shots"])==s["duration_s"]
    cursor=t
    for ref in s["reference_images"]:
        assert len(ref["sha256"])==64
        prior=refs.setdefault(ref["path"],ref["sha256"])
        assert ref["sha256"]==prior,"Reference hash conflict"
assert cursor==1800
assert len(shots)==len(set(shots))==186
assert len(seen_source)==66

missing=[]; mismatched=[]
for path,sha in refs.items():
    f=ROOT/path
    if not f.is_file(): missing.append(path)
    elif hashlib.sha256(f.read_bytes()).hexdigest()!=sha: mismatched.append(path)
assert not missing, f"Missing source visual reference bytes: {missing[:4]}"
assert not mismatched, f"SHA-256 mismatch in source visual references: {mismatched[:4]}"

assert delivery["shot_count"]==186 and delivery["film_target_seconds"]==1800
assert [x["shot_id"] for x in delivery["delivery_files"]]==shots
assert all(x["picture_status"]=="NOT_RENDERED" and x["audio_status"]=="NOT_RECORDED" for x in delivery["delivery_files"])
assert all(len(x["audio_stems"])==5 for x in delivery["delivery_files"])

assert assignment["review_mode"].startswith("SIMULATED_")
assert reconciled["status"]=="CANDIDATE_PENDING_INDEPENDENT_REVIEW" and reconciled["umpire"]=="PENDING"
assert len(reconciled["selected_advisors"])==20
assert len(reconciled["accepted"])==17 and len(reconciled["dissent"])==3
registry=json.loads((ROOT/"living-novel/consultants/ADVISOR_REGISTRY_V1.json").read_text())
bench=json.loads((ROOT/"memo-os/cinematography/PRODUCTION_SPECIALIST_REFERENCE_BENCH_V1.json").read_text())
assert set(registry["author_council"]["core_eight"]).issubset(set(reconciled["selected_advisors"]))
assert len(bench["profiles"])==12
assert all(p["name"] in reconciled["selected_advisors"] for p in bench["profiles"])
assert hashlib.sha256((PRE/"render-inputs/manifest.json").read_bytes()).hexdigest()==assignment["evidence_sha"]

html=(HERE/"storyboard_viewer.html").read_text(encoding="utf-8")
assert html.count('<details class="scene"')==34
assert html.count('<article class="shot"')==186
assert html.count("LAYOUT SCHEMATIC")==186
assert "CANDIDATE" in html
print(json.dumps({"status":"PASS_STATIC_CONTRACT_ONLY","duration_seconds":cursor,
 "original_folios":34,"source_shots":len(seen_source),"planned_storyboard_panels":len(shots),
 "verified_local_source_reference_files":len(refs),"reference_sha_failures":len(mismatched),
 "source_copy_modified":False,"modeled_advisory_lenses":20,"held_dissent":3,
 "pixel_quality":"NOT_TESTED","render_status":"NOT_RENDERED","Umpire":"PENDING"},indent=2))
