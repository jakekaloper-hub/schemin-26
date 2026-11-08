"""Unreal route overview; abstract schematic only, no playable path claim."""
import json, math
from pathlib import Path
import unreal
root=Path(unreal.Paths.project_dir())/"ScheminBridge/generated"
world=json.loads((root/"world_preview_manifest.json").read_text())
graph=json.loads((root/"travel_graph_preview.json").read_text())
assert graph["metric_navigation"] is False
locations={x["id"]:x for x in world["locations"]}
asset="/Game/ScheminPreview/Generated/Commonwealth_Route_Overview"
if unreal.EditorAssetLibrary.does_asset_exist(asset):
 unreal.log("SCHEMIN_ROUTE_OVERVIEW_ALREADY_EXISTS")
else:
 if not unreal.EditorLevelLibrary.new_level(asset): raise RuntimeError("level creation failed")
 mesh=unreal.load_asset("/Engine/BasicShapes/Cube.Cube")
 def block(name,x,y,z,sx,sy,sz,yaw=0):
  actor=unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.StaticMeshActor,unreal.Vector(x,y,z))
  actor.set_actor_label(name[:95]);actor.static_mesh_component.set_static_mesh(mesh)
  actor.set_actor_scale3d(unreal.Vector(sx,sy,sz))
  actor.set_actor_rotation(unreal.Rotator(0,yaw,0),False)
  actor.set_editor_property("tags",["ScheminPreview","AbstractNonMetric","NoCanonPromotion"])
 for loc in world["locations"]:
  x,y=loc["atlas_position_abstract"]
  block("ATLAS_"+loc["id"],x*120,y*120,0,1.5,1.5,2)
 count=0
 for route in graph["routes"]:
  seq=route["location_sequence"]
  for start,end in zip(seq,seq[1:]):
   ax,ay=locations[start]["atlas_position_abstract"]
   bx,by=locations[end]["atlas_position_abstract"]
   dx=(bx-ax)*120;dy=(by-ay)*120
   length=math.hypot(dx,dy)
   if length<1:continue
   angle=math.degrees(math.atan2(dy,dx))
   block("ROUTE_PROXY_"+route["route_id"]+"_"+str(count),(ax+bx)*60,(ay+by)*60,-30,length/100,0.20,0.15,angle)
   count+=1
 unreal.EditorLevelLibrary.save_current_level()
 unreal.log("SCHEMIN_ROUTE_OVERVIEW_BUILT "+str(count)+" segments")
