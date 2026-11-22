#!/usr/bin/env python3
"""Material and sound cue manifests for a non-rendered source-linked movie storyboard."""
from __future__ import annotations
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
data=json.loads((HERE/"film_storyboard_v1.json").read_text(encoding="utf-8"))

files=[]
for scene in data["scenes"]:
    for shot in scene["shots"]:
        files.append({
         "shot_id":shot["id"],"scene":scene["id"],"source_folio":scene["folio"],
         "source_beat_id":shot["source_beat_id"],"start":shot["start"],"end":shot["end"],
         "duration_s":shot["duration_s"],
         "output_picture_expected":"renders/"+scene["id"]+"/"+shot["id"]+"_v001.mov",
         "source_asset_reference_paths":[r["path"] for r in scene["reference_images"]],
         "source_asset_reference_sha256":[r["sha256"] for r in scene["reference_images"]],
         "picture_status":"NOT_RENDERED",
         "first_pass_route":"SOURCE_BEAT_MOTION_TEST" if shot["recommended_capture"]=="PENDING_MOTION_TEST" else "EDITED_STILL_OR_COVERAGE_TEST",
         "audio_stems":[
           "audio/DX/"+scene["id"]+".wav",
           "audio/VO/"+scene["id"]+".wav",
           "audio/FX/"+scene["id"]+".wav",
           "audio/AMB/"+scene["id"]+".wav",
           "audio/MX/"+scene["id"]+".wav"
         ],"audio_status":"NOT_RECORDED",
         "look_status":"NEEDS_APPROVED_SET_PLATE",
         "canon_status":"SOURCE_LINKED_NOT_PIXEL_APPROVED",
         "composite_status":"NEEDS_RENDER_RECEIPT_AND_QA",
         "source_request":scene["source_request"],
         "rights_status":"REVIEW_REQUIRED"
        })
delivery={"schema":"schemin.week10.film_delivery.v1","status":"PLANNED_NOT_PRODUCED",
 "film_target_seconds":1800,"picture_target":"16:9 / 1920x1080 / 24 fps candidate",
 "audio_target":"48kHz 24-bit WAV stems DX/VO/FX/AMB/MX, not produced",
 "shot_count":len(files),"scenes":34,"delivery_files":files,
 "promotion_rules":["Every shot must have accepted source reference bytes and regionally correct appearance",
 "No generation receipt implies approved human likeness, story truth, visual QA or rights",
 "Do not promote until independent Umpire, Closer and Founder gates"] }
(HERE/"SHOT_DELIVERY_REGISTER.json").write_text(json.dumps(delivery,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
start = [
 "# Week 10 film — audio, performance and dialogue worklist",
 "",
 "**Status:** sound design proposal, no produced performances or locked dialogue. The 30:00 storyboard clock is a picture/editing hypothesis.",
 "",
 "Memo copy contains **2,278 words**, roughly **15:43 at 145 words/minute**. Do not attempt to fill the entire 30:00 by continuous VO; the remainder is visual drama, music, deliberate silence, document readability and any later approved dialogue. Any approved new spoken lines must displace some VO/pauses or the picture clock must be re-timed and locked anew.",
 "",
 "**Audio master buses:** DX character/ADR, VO official narrative, FX Foley, AMB atmosphere, MX original score. Target five separately editable 48-kHz, 24-bit WAV stem families at picture lock. Keep sound generation/voice rights separate from the visual model license.",
 "",
 "## Dialogue policy",
 "",
 "A finished film needs a **screenplay and casting/voice lock**, because the memo is not a scripted 30-minute dialogue film. Exact official owner statements are retained only when present in controlling source; otherwise any fictional character lines are proposals requiring screenplay authorship, source/canon QA, pronunciation/casting review and user approval. This packet **does not invent quotations** from the league owners or from the named publication-method advisors.",
 "",
 "M01 Rodeo: audience laugh, voiced impression only after editorial approval; prioritize lasso/hooves/body reaction and embarrassed breath, not extra unsourced jokes.",
 "M02 Storm: Red's effort and Niño's challenge are physical; rain and broken-hoop Foley carry most of the scene. No unsourced 2022 flashback dialogue.",
 "M03 Temple: source contains a father's request and deliberate refusal but not a required verbatim line; produce a draft script after the three-head character lock; stage the silence as the center of the sequence.",
 "M04 Swamp: treat bark and steady diesel as the dialogue. No newly invented driver confrontation.",
 "M05 Birthday: owner-to-owner spoken banter can be drafted later, but the distinction between burger reveal and cake contact is mandatory. Do not invent a real owner quote.",
 "M06 Throne: dramatize offer, refusal and signal only after a sourced fictional dialogue packet. Do not add an offscreen victory declaration or move the lightning to a nonexistent battery.",
 "Sports desks and conclusion: official results must be accurately spoken or typeset, not hallucinated by generation. Week 11 remains preview, not a completed outcome.",
 "",
 "## Timeline cue ledger",
 "",
 "| Time | Folio / scene | Sound setting | Score / performer objective |",
 "|---|---|---|---|",
]
for scene in data["scenes"]:
    start.append("| "+scene["start"][3:]+"–"+scene["end"][3:]+" | "+scene["folio"]+" · "+scene["title"].replace("|","/")+" | "+scene["sound"]["ambience"].replace("|","/")+" | "+scene["sound"]["original_music_brief"].replace("|","/")+" |")
start += [
 "",
 "## Critical sound tests",
 "",
 "- Temple: at P13, demonstrate a real machinery stop before listener hope, then the separate speaker action before tool restart. Sound is causal, not mere wallpaper.",
 "- Rodeo: verify sound matches the torso loop closure, slippery skid and post-fall manual knot; do not score an invisible neck catch.",
 "- Storm: three acoustic environments with different wetness/exposure; no geographically impossible simultaneous rain wall.",
 "- Swamp: establish hound at road edge, truck on stable surface; no collision or acceleration sound.",
 "- Birthday: separate prop sound for gift reveal and later cake contact; keep audience reaction plausible for established room.",
 "- Throne: differentiate destroyed first battery from still-active second battery and ground lightning in its surviving source.",
 "- Editorial graphics: remain legible; allow read time or use approved source-specific voiceover.",
 "- Original score only, unless license documentation is attached. Do not synthesize a copyrighted song as a placeholder.",
 "- Chatterbox/Wan test assets in the Mac proof folder are NOT cast voices or canonical shot approvals.",
 "",
 "## Post handoff / ADR record",
 "",
 "For each accepted scene deliver: dialogue transcript + final performer permission if applicable; voice reference provenance; per-take timestamps; pronunciation sheet for owner/realm names; sample-accurate sync; unprocessed dry DX; production Foley; separated surround/stereo ambience; MX composer source and rights; final subtitle file and descriptive transcriptions. If shot timing changes, rebuild the 30:00 source-linked edit and check all 186 shot boundaries.",
]
(HERE/"AUDIO_AND_PERFORMANCE_PLAN.md").write_text("\n".join(start)+"\n",encoding="utf-8")
print(json.dumps({"assets":len(files),"scene_audio_lines":len(start),"files":["SHOT_DELIVERY_REGISTER.json","AUDIO_AND_PERFORMANCE_PLAN.md"]},indent=2))
