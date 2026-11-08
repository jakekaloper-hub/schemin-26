"""Headless UE verification of key preview assets and scene safety."""
import unreal,json
from pathlib import Path
paths=[
"/Game/ScheminPreview/Generated/Commonwealth_Atlas_Overview",
"/Game/ScheminPreview/Generated/Commonwealth_Route_Overview",
"/Game/ScheminPreview/Generated/Commonwealth_Navigation_Hub",
"/Game/ScheminPreview/Generated/Commonwealth_Regional_Showcase_Lit",
]
e=[]
sub=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
for p in paths:
 item={"asset":p,"exists":bool(unreal.EditorAssetLibrary.does_asset_exist(p))}
 if item["exists"]:
  item["loadable"]=bool(sub.load_level(p))
  if item["loadable"]:
   actors=unreal.EditorLevelLibrary.get_all_level_actors()
   item["actor_count"]=len(actors)
   item["has_player_start"]=any(isinstance(a,unreal.PlayerStart) for a in actors)
 else:item["loadable"]=False
 e.append(item)
out=Path(unreal.Paths.project_dir())/"ScheminBridge/generated/world_scene_audit.json"
out.write_text(json.dumps({"scenes":e,"rendered_preview_verified":False,"gameplay_verified":False},indent=2)+"\n")
if any(not x.get("loadable") for x in e):raise RuntimeError("Required scene missing or load failed")
print("WORLD_SCENE_AUDIT_PASS",len(e))
