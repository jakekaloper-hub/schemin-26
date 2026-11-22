#!/usr/bin/env python3
"""Produce an evidence receipt for one noncanonical moving stunt and five audio stems."""
from pathlib import Path
import json,hashlib,wave,subprocess
import imageio_ffmpeg
HERE=Path(__file__).resolve().parent
OUT=HERE/"proofs/M01_RODEO_STUNT_PREVIS"
name="W10_M01_Rodeo_Blocking_Proof_with_TEMP_DX.mp4"
video=OUT/name
assert video.is_file() and video.stat().st_size>200000
stems={}
for key in ("DX_TEMP","VO_TEMP","FX","AMB","MX"):
    wav=OUT/f"W10_M01_{key}_48k24.wav"
    assert wav.is_file()
    with wave.open(str(wav),"rb") as w:
        assert w.getframerate()==48000 and w.getsampwidth()==3
        duration=w.getnframes()/w.getframerate()
        assert abs(duration-42)<0.05,(key,duration)
        stems[key]={"path":str(wav.relative_to(HERE)),"sample_rate":48000,
             "bit_depth":24,"duration_seconds":duration,"bytes":wav.stat().st_size,
             "sha256":hashlib.sha256(wav.read_bytes()).hexdigest()}
ff=imageio_ffmpeg.get_ffmpeg_exe()
r=subprocess.run([ff,"-hide_banner","-i",str(video)],capture_output=True,text=True)
info=r.stderr
assert "960x540" in info,info[-1500:]
assert "12 fps" in info,info[-1500:]
assert "Audio: aac" in info,info[-1500:]
assert "Duration: 00:00:42" in info,info[-1500:]
receipt={
 "schema":"schemin.week10.movie_proof_receipt.v1",
 "id":"SCHEMIN-W10-M01-42SEC-STUNT-PREVIZ-20261122",
 "status":"MEDIA_EXISTS_NONCANONICAL_QA_ONLY",
 "source_stages":["W10-P05","W10-P06","W10-P07"],
 "source_actual_beats":8,
 "source_shot_plan_count":19,
 "original_scene_duration_seconds":179,
 "proof_compressed_duration_seconds":42,
 "video":{"relative_path":str(video.relative_to(HERE)),"bytes":video.stat().st_size,
   "sha256":hashlib.sha256(video.read_bytes()).hexdigest(),
   "pixels":"960x540","fps":12,"tracks":"one video and one mixed AAC audio"},
 "post_audio_stems":stems,
 "script_source":"SCREENPLAY_CANDIDATE_V1.json",
 "project_source":"memo-os/week-10/preproduction/render-inputs",
 "render_technology":"Local PIL/NumPy 2D actor proxies + imageio-ffmpeg and macOS system TEMP voices; original procedural Foley/music",
 "external_compute_charges":0,
 "local_model_weights_downloaded_for_this_proof":False,
 "QA":{
  "source_gate_orientation":"CORRECTED_LEFT_SCREEN",
  "four_legged_silhouette":"SCHEMATIC_SUPPORTED_NOT_CHARACTER_QA",
  "rope_torso_route":"SCHEMATIC_SUPPORTED_NOT_STUNT_QA",
  "manual_knot":"NOT_ACCURATELY_RIGGED_HOLD",
  "full_canon_character_likeness":"HOLD",
  "lip_synced_dialogue":"NOT_TESTED",
  "editable_5_audio_buses":"PASS_TECHNICAL",
  "scene_duration_coverage":"42_SECOND_TEST_NOT_179_SECOND_FULL_M01",
  "photorealistic_film":"NO",
  "umpire":"PENDING",
  "release":"HOLD"
 }
}
(HERE/"M01_MOVING_PROOF_RECEIPT.json").write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"movie_file":receipt["video"]["relative_path"],"duration":42,
 "pixels":receipt["video"]["pixels"],"stem_count":len(stems),"video_sha":receipt["video"]["sha256"],
 "status":receipt["status"]},indent=2))
