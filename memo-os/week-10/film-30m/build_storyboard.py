#!/usr/bin/env python3
"""Reproducible source-linked 30:00 Week 10 film storyboard. Non-canon preproduction."""
from __future__ import annotations
import hashlib
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE = ROOT / "memo-os/week-10/preproduction"
MANIFEST = SOURCE / "render-inputs/manifest.json"
OUT = HERE / "film_storyboard_v1.json"
TARGET_SECONDS = 1800
WPM = 145

def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))

def tc(value: int) -> str:
    h, rem = divmod(value, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

def act_for(position: int) -> str:
    if position <= 4: return "00_PROLOGUE"
    if position <= 7: return "01_RODEO"
    if position <= 10: return "02_STORM"
    if position == 11: return "03_WEATHER"
    if position <= 14: return "04_TEMPLE"
    if position <= 17: return "05_SWAMP"
    if position <= 19: return "06_RESULTS"
    if position <= 22: return "07_BIRTHDAY"
    if position <= 25: return "08_THRONE"
    return "09_AFTERSHOCK"

ACTS = {
"00_PROLOGUE": ("Public memory", "Record pavilion, discreet civic sounds, weather rising", "Low original orchestral thesis", "Paper, footfalls, standard ratchet"),
"01_RODEO": ("Highland rodeo", "Wet arena, gusty galleries, warm sheltered lanterns", "Plucked strings and percussion; score drops before catch", "Boots, four hooves, rope, wet dirt, hand-tied knot"),
"02_STORM": ("Storm Coast → Forgotten Court", "Coastal rain first; inland squall later, no instant geography", "Bowed low strings and damaged-theme reprise", "Sandbags, surface runoff, long branch crack, rim contact"),
"03_WEATHER": ("Upper Basin connector", "Regional coastal water, inland road wind, later wetland channels", "Spacious three-region sonic bridge", "Stone, wagon fabric, lake wind, delayed runoff"),
"04_TEMPLE": ("Waterfall temple", "Waterfall and household hush interrupted by localized machine noise", "Sparse unsettling pulse; intentional silence at plea", "Compressor/jackhammer stop; speaker knob; drill returns"),
"05_SWAMP": ("Southern wetland delivery", "Bark against steady road/engine sound; raised road stays passable", "Restrained rhythmic motif, then quiet", "Dog barks, wheels on firm strip, still-loaded truck receding"),
"06_RESULTS": ("Arbiter records", "Paper and quiet pavilion, not combat", "Measured, almost bare documentary bed", "Ledger pages, ink, carved result board"),
"07_BIRTHDAY": ("Jackson hospitality", "Established warm gathering with appropriate room acoustics", "Small original comedic ensemble; let reveal breathe", "Paper wrap, box, meal presentation, distinct cake contact"),
"08_THRONE": ("Mountain field throne", "Mountain weather, sheltered chair, separate exterior battery", "Low brass and suspended strings; silence at surrender refusal", "Battery break, chair/boots on stairs, signal, lightning"),
"09_AFTERSHOCK": ("Results, crossing, closing", "Legible editorial data shifts into ominous roads and home weather", "Opening-theme reprise dissolving into unresolved motif", "Pages, bridge wind, restrained evening camp cloth")
}
WEIGHTS = {"00_PROLOGUE":1.2, "01_RODEO":3.3, "02_STORM":3.2,
"03_WEATHER":2.3,"04_TEMPLE":3.2,"05_SWAMP":3.0,"06_RESULTS":1.1,
"07_BIRTHDAY":3.0,"08_THRONE":4.1,"09_AFTERSHOCK":1.2}
OVERRIDES = {"W10-P01":2.5,"W10-P02":1.7,"W10-P03":0.8,
"W10-P04":0.8,"W10-P35":3.5,"W10-P33":2.4}

def movement(camera: str, kind: str) -> str:
    camera = camera.lower()
    if kind == "opening": return "Stable orienting push or completely fixed geography master"
    if kind == "exit": return "Hold consequence; next scene enters on a motivated L-cut"
    if kind == "insert": return "Tactile macro or same-axis insert; no new set or props"
    if kind == "coverage": return "Slow performance hold or continuity-preserving reverse, no extra plot"
    if any(k in camera for k in ("low","upward")): return "Stabilized low push with silhouette and eyeline lock"
    if any(k in camera for k in ("wide","high","oblique")): return "Crane or slow tracking master with static spatial anchors"
    if any(k in camera for k in ("tight","close","detail")): return "Restrained micro-dolly; preserve physical action"
    if any(k in camera for k in ("lateral","side")): return "Lateral tracking keeping actors and prop path compatible"
    return "Purposeful static framing or subtle dolly, not unmotivated drone movement"

def distribute(total: int, weights: list[float]) -> list[int]:
    raw = [total * w / sum(weights) for w in weights]
    result = [math.floor(x) for x in raw]
    for index in sorted(range(len(weights)), key=lambda i: (raw[i]-result[i],-i),reverse=True)[:total-sum(result)]:
        result[index] += 1
    if sum(result) != total or not all(z>0 for z in result):
        raise AssertionError("Invalid distribution")
    return result

manifest = load(MANIFEST)
assert manifest["page_count"] == 34 and manifest["stage"] == "GRAYSCALE_FOLIO_PROOF_INPUTS"
readings = [p["reading_position"] for p in manifest["pages"]]
assert readings == list(range(1,35)), "Do not relabel or reorder existing folios"

source_rows = []
for page in manifest["pages"]:
    source_path = SOURCE / page["request"]
    actual_sha = hashlib.sha256(source_path.read_bytes()).hexdigest()
    assert actual_sha == page["request_sha256"], f"Frozen request hash mismatch: {page['page_id']}"
    packet = load(source_path)
    assert packet["page_id"] == page["page_id"]
    beats = packet["scene"]["visual_storytelling"]["shots"]
    assert len(beats) == page["visual_beat_count"]
    act = act_for(page["reading_position"])
    base = math.ceil(page["copy_words"] * 60 / WPM) + 8
    source_rows.append({"page":page,"packet":packet,"beats":beats,"act":act,
        "base":base,"weight":OVERRIDES.get(page["page_id"],WEIGHTS[act])})
base_sum = sum(r["base"] for r in source_rows)
extra = TARGET_SECONDS-base_sum
assert extra > 0
extras = distribute(extra,[r["weight"] for r in source_rows])
for row, e in zip(source_rows,extras):
    row["duration"] = row["base"] + e

scenes = []
cursor = 0
for row in source_rows:
    p, request, beats, act = row["page"],row["packet"],row["beats"],row["act"]
    vis, env = request["scene"]["visual_storytelling"],request["scene"]
    scene_duration = row["duration"]
    shot_plan = [
       {"kind":"opening","role":"establishing_anchor","source_id":beats[0]["id"],
        "camera":env["camera_and_composition"],
        "action":"Orient the audience in the already described location: "+env["background"],
        "point":"Establish correct time, weather, light and landmark; no new event."},
    ]
    for beat in beats:
        shot_plan.append({"kind":"source","role":beat["role"],"source_id":beat["id"],
             "camera":beat["camera"],"action":beat["action"],
             "point":beat["new_information"],"time_relation":beat.get("time_relation"),
             "pov_owner_ids":beat.get("pov_owner_ids",[])})
    shot_plan.append({"kind":"insert","role":"material_proof","source_id":beats[-1]["id"],
       "camera":"Detail in the same physical space",
       "action":"Existing foreground/material only: "+env["foreground"],
       "point":"Ground the fiction in tactility and allow Foley/editorial breath."})
    if scene_duration >= 58:
        shot_plan.append({"kind":"coverage","role":"reaction_or_silent_space","source_id":beats[-1]["id"],
           "camera":"Same-axis reverse/hold, preserve sequence time logic",
           "action":"Continue already sourced movement or pause: "+beats[-1]["action"],
           "point":"Preserve character choice without adding unscripted events."})
    shot_plan.append({"kind":"exit","role":"causal_sound_bridge","source_id":beats[-1]["id"],
       "camera":"Consequence / next scene transition",
       "action":vis.get("page_turn_out","Hold the established consequence."),
       "point":"Visual and audio bridge; source geography remains intact."})
    coeff = [2.2 if s["kind"]=="source" and s["role"]=="dominant"
      else 1.7 if s["kind"]=="source"
      else 1 if s["kind"]=="opening" else .65 if s["kind"]=="insert" else .8
      for s in shot_plan]
    durations = distribute(scene_duration,coeff)
    shots = []
    position = cursor
    for i,(s,duration) in enumerate(zip(shot_plan,durations),start=1):
        status = "PENDING_MOTION_TEST" if s["kind"]=="source" and act not in {"00_PROLOGUE","06_RESULTS","09_AFTERSHOCK"} else "STILL_OR_MOTION_EDITORIAL_CHOICE"
        shots.append({
          "id":f"W10F-{p['page_id'][-3:]}-S{i:02d}",
          "source_beat_id":s["source_id"],"source_kind":s["kind"],"role":s["role"],
          "start_s":position,"end_s":position+duration,"start":tc(position),
          "end":tc(position+duration),"duration_s":duration,
          "camera":s["camera"],"movement":movement(s["camera"],s["kind"]),
          "blocking":s["action"],"dramatic_purpose":s["point"],
          "time_relation":s.get("time_relation"),"pov_owner_ids":s.get("pov_owner_ids",[]),
          "lighting_lock":env["background"],"sound_cue":ACTS[act][3],
          "asset_status":"CANDIDATE_UNRENDERED","recommended_capture":status,
          "source_request":f"memo-os/week-10/preproduction/{p['request']}",
          "may_change_canon":False
        })
        position+=duration
    assert position == cursor+scene_duration
    encounter = env["encounter"]
    refs = [{"path":z["repo_path"],"sha256":z["sha256"],
        "role":z.get("role"),"character_id":z.get("character_id")}
        for z in request.get("reference_images",[])]
    scenes.append({
      "id":f"W10F-SC{p['reading_position']:02d}","folio":p["page_id"],
      "order":p["reading_position"],"title":p["title"],"act":act,
      "start_s":cursor,"end_s":position,"duration_s":scene_duration,
      "start":tc(cursor),"end":tc(position),"characters":p.get("characters",[]),
      "source_primary_beats":len(beats),"board_shot_count":len(shots),
      "narration_words":p["copy_words"],"narration_at_145wpm_s":math.ceil(p["copy_words"]*60/WPM),
      "publication_copy":request["publication_copy"],
      "narration_and_dialogue":"Original memo body is source VO, not 30-minute screenplay. New character dialogue requires writing, canon checks and explicit editorial approval.",
      "source_request":f"memo-os/week-10/preproduction/{p['request']}",
      "source_sha256":p["request_sha256"],
      "setting":{"venue_id":encounter.get("venue_id"),"set_id":encounter.get("set_id"),
           "venue_type":encounter.get("venue_type"),"provisional":encounter.get("provisional_location"),
           "landmarks":encounter.get("persistent_landmarks",[]),"atlas_promotion":encounter.get("formal_atlas_promotion")},
      "composition":env["camera_and_composition"],
      "continuity_in":env.get("continuity_in",[]),"continuity_out":env.get("continuity_out",[]),
      "time_logic":vis.get("time_logic"),"forbidden_mutations":env.get("forbidden_mutations",[]),
      "transition":vis.get("page_turn_out"),
      "sound":{"scene_name":ACTS[act][0],"ambience":ACTS[act][1],
           "original_music_brief":ACTS[act][2],"foley":ACTS[act][3]},
      "reference_images":refs,"stage":"STORYBOARD_CANDIDATE_NOT_ART_LOCK",
      "shots":shots
    })
    cursor=position
assert cursor==TARGET_SECONDS
counts = {act:sum(s["duration_s"] for s in scenes if s["act"]==act) for act in ACTS}
payload={
 "schema":"schemin.week10.film_storyboard.v1","title":"WEEK 10 — THE COMMONWEALTH CUT",
 "status":"CANDIDATE_NO_RENDER_OR_RELEASE_APPROVAL","date":"2026-11-22",
 "sources":{"branch":"memo-week10-preproduction-20261116",
   "manifest":"memo-os/week-10/preproduction/render-inputs/manifest.json",
   "shots":"memo-os/week-10/preproduction/VISUAL_STORYTELLING_PASS_2026-11-17.md",
   "facts":"memo-os/week-10/preproduction/facts.json",
   "page_policy":"Source Memo OS preproduction keeps PNG generation paused."},
 "runtime":{"target_seconds":TARGET_SECONDS,"target_timecode":tc(TARGET_SECONDS),
   "scene_count":len(scenes),"shot_count":sum(len(s["shots"]) for s in scenes),
   "verified_source_primary_beats":sum(s["source_primary_beats"] for s in scenes),
   "memo_copy_words":sum(s["narration_words"] for s in scenes),
   "memo_spoken_at_145wpm_s":math.ceil(sum(s["narration_words"] for s in scenes)*60/WPM),
   "timing_method":"Copy reading minimum at 145 wpm + 8s per scene + balanced screen action weighting",
   "seconds_by_act":counts,
   "visual_format":"Candidate film 16:9 1920x1080 at 24 fps, require human reblocking from source 1080x1920 folios",
   "sound_format":"Editable separate narration, dialogue, effects, atmosphere and original score stems; not yet recorded."},
 "authority":{"source_truth":"Completed ESPN/Flaim Week 10 fact lock and source publication_copy",
   "authors":"Inklings published-method lenses only, no real-world human consultation",
   "production_bench":"12 published-method lenses only, no human advisors contacted",
   "Bullpen":"Proposed roles and gates require actual director/Umpire execution",
   "promotion":"NO AUTOMATIC CANON OR PUBLICATION APPROVAL"},
 "scene_order":[s["folio"] for s in scenes],"scenes":scenes
}
OUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"file":str(OUT),"scenes":len(scenes),"shots":payload["runtime"]["shot_count"],
 "source_beats":payload["runtime"]["verified_source_primary_beats"],
 "runtime_seconds":cursor,"words":payload["runtime"]["memo_copy_words"],
 "by_act":counts},indent=2))
