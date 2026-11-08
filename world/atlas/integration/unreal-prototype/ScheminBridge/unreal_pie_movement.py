"""PIE runtime pawn movement probe; reports BLOCKED unless motion observed."""
import json, unreal
from pathlib import Path
out=Path(unreal.Paths.project_dir())/"ScheminBridge/generated/pie_movement_evidence.json"
result={"status":"BLOCKED","pie_started":False,"pawn_found":False,"movement_verified":False}
try:
 editor=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
 if not editor.load_level("/Game/ScheminPreview/Generated/Commonwealth_Navigation_Hub"):
  raise RuntimeError("level load failed")
 # Editor scripting PIE request. Commandlet runtimes may lack a game viewport.
 if not hasattr(editor,"editor_request_begin_play"):
  raise RuntimeError("PIE API unavailable in this UE runtime")
 editor.editor_request_begin_play()
 result["pie_requested"]=True
 result["status"]="PENDING_RUNTIME_TICKS"
except Exception as exc:
 result["error"]=str(exc)
finally:
 out.write_text(json.dumps(result,indent=2)+"\n")
 print("SCHEMIN_PIE_PROBE",result["status"])
if result["status"]=="BLOCKED":raise RuntimeError(result.get("error","PIE not verified"))
