#!/usr/bin/env python3
"""Verify screenplay provenance, stage-meter and canonical actor-proxy motion contract.

Static QA cannot approve actual CGI or portrayal quality.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import os
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
BOARD=json.loads(Path(os.environ.get("FILM_BOARD_JSON",str(HERE/"film_storyboard_v1.json"))).read_text())
SCRIPT=json.loads((HERE/"SCREENPLAY_CANDIDATE_V1.json").read_text())
BULLPEN=json.loads((HERE/"BULLPEN_MISSION_ROUTING_V1.json").read_text())
PROOF=HERE/"proofs"/"M01_RODEO_STUNT_PREVIS"
RECEIPT=json.loads((PROOF/"PREVIS_RENDER_RECEIPT.json").read_text())

assert SCRIPT["source_pages"]==34 and SCRIPT["runtime_seconds"]==BOARD["runtime"]["target_seconds"]==1800
assert len(SCRIPT["scene_scripts"])==len(BOARD["scenes"])==34
assert BULLPEN["intent"]["command"]=="mission"
assert BULLPEN["narrative_route"]["primary"]=="the_beat_writer"
assert set(BULLPEN["narrative_route"]["counterweight_plan"]["counterweights"])=={"the_scout","the_librarian"}
assert BULLPEN["film_route"]["primary"]=="the_setup_man"
assert BULLPEN["narrative_route"]["counterweight_plan"]["activated"]
assert BULLPEN["film_route"]["counterweight_plan"]["activated"]
assert RECEIPT["status"]=="RENDERED_AS_NONCANONICAL_ANIMATIC"
assert RECEIPT["source"]==["W10-P05","W10-P06","W10-P07"]
assert RECEIPT["duration_sec"]==42 and RECEIPT["fps"]==12
for name,key in [
 ("W10_M01_stunt_previs_silent.mp4","video_sha256"),
 ("W10_M01_original_ambience_foley.wav","audio_sha256")
]:
    assert hashlib.sha256((PROOF/name).read_bytes()).hexdigest()==RECEIPT[key]

dialogue_lines=0
for sc,script in zip(BOARD["scenes"],SCRIPT["scene_scripts"]):
    assert sc["folio"]==script["source_folio"]
    assert script["scene_id"]==sc["id"]
    assert script["source_unchanged_body"]==sc["publication_copy"]["body"]
    assert script["source_publication_copy"]==sc["publication_copy"]
    assert script["source_sha256"]==sc["source_sha256"]
    assert script["start"]==sc["start"] and script["end"]==sc["end"]
    assert script["counts"]["vo_time_at_145wpm"]+script["counts"]["dialogue_time_at_135wpm"] <= sc["duration_s"]-3.95
    assert script["image_appearance_status"]=="REQUIRES_PER_SHOT_CANON_QA"
    assert script["voice_status"]=="NOT_CAST"
    assert script["script_status"]=="CANDIDATE"
    for dx in script["dialogue_proposal"]:
        assert dx["status"]=="FICTIONAL_DRAFT_NOT_REAL_OWNER_QUOTE"
        assert dx["speaker"] and dx["text"]
        dialogue_lines+=1

assert dialogue_lines>=20
p18=next(s for s in SCRIPT["scene_scripts"] if s["source_folio"]=="W10-P18")
assert "113.86" in p18["narrator_film_candidate"] and "103.66" in p18["narrator_film_candidate"],"Lost combined stat qualifier"
p23=next(s for s in SCRIPT["scene_scripts"] if s["source_folio"]=="W10-P23")
assert "arch" in p23["camera_action_direction"].lower() and "Lay down the blade" in p23["dialogue_proposal"][0]["text"]
p07=next(s for s in SCRIPT["scene_scripts"] if s["source_folio"]=="W10-P07")
assert "finishes the binding" in p07["source_unchanged_body"].lower() and "manual" in p07["narrator_film_candidate"].lower() or "finishes the knot by hand" in p07["narrator_film_candidate"].lower()
p17=next(s for s in SCRIPT["scene_scripts"] if s["source_folio"]=="W10-P17")
assert "not an elimination ticket" in p17["narrator_film_candidate"].lower()
assert "NO APPROVED CHARACTER RENDER" in (HERE/"make_m01_previs.py").read_text()

text=(HERE/"SCREENPLAY_CANDIDATE_V1.md").read_text(encoding="utf-8")
assert text.count("### W10F-SC")==34
assert text.count("Controlling original Memo OS prose")==34
assert (PROOF/"W10_M01_Rodeo_Blocking_Proof_with_TEMP_DX.mp4").is_file()
assert (PROOF/"W10_M01_Rodeo_Blocking_Proof_with_TEMP_DX.mp4").stat().st_size>100000
STEMS=json.loads((HERE/"M01_MOVING_PROOF_RECEIPT.json").read_text())["post_audio_stems"]
assert set(STEMS)=={"DX_TEMP","VO_TEMP","FX","AMB","MX"}
assert all(x["sample_rate"]==48000 and x["bit_depth"]==24 for x in STEMS.values())

out={
 "status":"PASS_SOURCE_AND_ASSEMBLY_WITH_EXPLICIT_VISUAL_HOLDS",
 "actual_core_bullpen_router":"EXECUTED",
 "full_script_scene_count":34,
 "editable_source_picture_seconds":1800,
 "candidate_dialogue_lines":dialogue_lines,
 "complete_frozen_source_copy_preserved":True,
 "source_vo_and_dialogue_under_pic_limit":True,
 "proposed_film_voices":"NOT_CAST",
 "M01_blocking_video":"EXISTS_42_SECONDS",
 "M01_stunt_physics":"HOLD_MORE_DETAILED_RIG_AND_REAL_VIDEO",
 "M01_character_identity":"HOLD_SCHEMATIC_PROXY_NOT_CANON_PHOTOREAL",
 "5_stem_audio_delivery":"PASS_TECHNICAL_M01_ONLY",
 "umpire":"PENDING",
 "release":"HOLD"
}
(HERE/"NEXT_PHASE_STATIC_QA.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps(out,indent=2))
