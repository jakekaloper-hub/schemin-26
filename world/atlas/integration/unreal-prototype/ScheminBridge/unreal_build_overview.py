"""Atlas abstract-location overview in Unreal. NOT metric geography."""
import json
from pathlib import Path
import unreal
root=Path(unreal.Paths.project_dir())/"ScheminBridge"
m=json.loads((root/"generated/world_preview_manifest.json").read_text())
assert m["coordinate_space"]=="schemin-local-v1 (abstract, non-metric)"
assert len(m["locations"])==23
asset="/Game/ScheminPreview/Generated/Commonwealth_Atlas_Overview"
if unreal.EditorAssetLibrary.does_asset_exist(asset):
 raise RuntimeError("overview already present, do not overwrite")
if not unreal.EditorLevelLibrary.new_level(asset):
 raise RuntimeError("cannot create overview")
mesh=unreal.load_asset("/Engine/BasicShapes/Cube.Cube")
for loc in m["locations"]:
 x,y=loc["atlas_position_abstract"]
 actor=unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.StaticMeshActor,unreal.Vector(float(x)*100,float(y)*100,0))
 actor.static_mesh_component.set_static_mesh(mesh)
 actor.set_actor_scale3d(unreal.Vector(0.5,0.5,1))
 actor.set_actor_label("ABSTRACT_"+loc["id"]+"_"+loc["render_classification"])
 actor.set_editor_property("tags",["ScheminPreview","AbstractCoordinates","NoCanonPromotion"])
unreal.EditorLevelLibrary.save_current_level()
unreal.log("SCHEMIN_OVERVIEW_23_LOCATIONS_CREATED")
