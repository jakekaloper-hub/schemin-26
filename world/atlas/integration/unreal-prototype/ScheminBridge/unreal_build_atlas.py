"""Editor commandlet: create isolated schematic proxy levels, one per Atlas location.
Only writes /Game/ScheminPreview/Generated; does not replace existing maps.
"""
import json,hashlib
from pathlib import Path
import unreal
root=Path(unreal.Paths.project_dir())/"ScheminBridge"
manifest=json.loads((root/"generated/world_preview_manifest.json").read_text())
assert manifest["kind"]=="UNREAL_WORLD_PREVIEW_NOT_CANON"
assert manifest["source_sha256"]=="d3aa0d5fca9bf120ad8f1ecc6267f0cbce54bdf83b8117c0328c8d13cd0aeaeb"
assert manifest["source_commit"]=="7afe7ef0fcf24e25d67ca8c85d4e6e36e03a78e3"
assert len(manifest["locations"])==23
mesh=unreal.load_asset("/Engine/BasicShapes/Cube.Cube")
if not mesh:raise RuntimeError("missing primitive cube")
built=[];skipped=[]
for loc in manifest["locations"]:
 path="/Game/ScheminPreview/Generated/"+loc["unreal_map_name"]
 if unreal.EditorAssetLibrary.does_asset_exist(path):
  skipped.append(loc["id"]);continue
 if loc["characters_allowed"] is not False or loc["spatial_scale_approved"] is not False:
  raise RuntimeError("preview safety contract broken")
 if not unreal.EditorLevelLibrary.new_level(path):raise RuntimeError("cannot create "+path)
 def cube(name,pos,scale):
  a=unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.StaticMeshActor,unreal.Vector(*pos))
  a.set_actor_label(name)
  a.static_mesh_component.set_static_mesh(mesh)
  a.set_actor_scale3d(unreal.Vector(*scale))
  a.set_editor_property("tags",["ScheminPreview","NoCanonPromotion"])
 cube("PREVIEW_GROUND_ABSTRACT_NOT_METRIC",(0,0,-100),(12,12,1))
 cube("PREVIEW_SOURCE_CLASS_"+loc["render_classification"],(0,0,10),(1,1,1))
 for i,landmark in enumerate(loc.get("landmarks",[])[:4]):
  cube("PREVIEW_LANDMARK_"+str(i)+"_"+landmark[:42],((i-1)*350,350,100),(1.5,1.5,2))
 unreal.EditorLevelLibrary.save_current_level()
 built.append(loc["id"])
unreal.log("SCHEMIN_ATLAS_BUILT "+str(len(built))+" SKIPPED "+str(len(skipped)))
(root/"generated/atlas_build_receipt.json").write_text(json.dumps({"built":built,"skipped":skipped,"kind":"UNREAL_SCHEMATIC_PREVIEW_ONLY"},indent=2)+"\n")
