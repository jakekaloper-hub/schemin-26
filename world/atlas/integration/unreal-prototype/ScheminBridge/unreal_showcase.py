import json,math,random
from pathlib import Path
import unreal
root=Path(unreal.Paths.project_dir())/"ScheminBridge"
data=json.loads((root/"generated/region_environment_packets.json").read_text())
world=json.loads((root/"generated/world_preview_manifest.json").read_text())
asset="/Game/ScheminPreview/Generated/Commonwealth_Regional_Showcase"
if unreal.EditorAssetLibrary.does_asset_exist(asset):
 raise RuntimeError("Already exists; no overwrite")
if not unreal.EditorLevelLibrary.new_level(asset):
 raise RuntimeError("Cannot create showcase")
cube=unreal.load_asset("/Engine/BasicShapes/Cube.Cube")
cylinder=unreal.load_asset("/Engine/BasicShapes/Cylinder.Cylinder")
sphere=unreal.load_asset("/Engine/BasicShapes/Sphere.Sphere")
def put(label,xyz,scale,mesh=cube):
 a=unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.StaticMeshActor,unreal.Vector(*xyz))
 a.set_actor_label(label[:100])
 a.static_mesh_component.set_static_mesh(mesh)
 a.set_actor_scale3d(unreal.Vector(*scale))
 a.set_editor_property("tags",["ScheminPreview","NoCanonPromotion"])
 return a
# Seven distinct interpretive region stations; positions are exhibit spacing, not Atlas geography.
for i,reg in enumerate(data["regions"]):
 ox=(i%4)*6500
 oy=(i//4)*6500
 rid=reg["region_id"]
 put("EXHIBIT_"+rid,(ox,oy,-120),(50,50,1))
 terms=" ".join(reg["terrain_source_terms"]).lower()
 for j in range(12):
  x=ox-1800+(j%4)*1050
  y=oy-1200+(j//4)*1100
  if "wetland" in terms or "rivers" in terms or "bays" in terms:
   put(rid+"_water_or_causeway_PROXY_"+str(j),(x,y,-18),(7,3,0.6))
   put(rid+"_raised_bank_PROXY_"+str(j),(x+140,y+190,95),(3,2,1.6))
  elif "mountain" in terms or "ridge" in terms:
   put(rid+"_ridge_PROXY_"+str(j),(x,y,250+(j%3)*95),(3,3,6+(j%3)*2))
  elif "grassland" in terms or "frontier" in terms:
   put(rid+"_tableland_PROXY_"+str(j),(x,y,70),(7,5,1.3))
  else:
   put(rid+"_upland_PROXY_"+str(j),(x,y,130+(j%2)*40),(4,4,2.5))
  if "forest" in terms:
   put(rid+"_tree_trunk_PROXY_"+str(j),(x+100,y+80,250),(0.6,0.6,5),cylinder)
   put(rid+"_canopy_PROXY_"+str(j),(x+100,y+80,540),(2.2,2.2,2),sphere)
 put("REGION_INFO_"+rid,(ox,oy,220),(2,2,3))
# Third Person player spawn and simple lighting.
p=unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.PlayerStart,unreal.Vector(0,0,160))
p.set_actor_label("Commonwealth_Exhibit_PlayerStart")
sun=unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.DirectionalLight,unreal.Vector(0,0,1500))
sun.set_actor_label("Commonwealth_Exhibit_Sun")
unreal.EditorLevelLibrary.save_current_level()
unreal.log("COMMONWEALTH_SHOWCASE_SAVED "+str(len(data["regions"]))+" REGIONS")
