import unreal,json
from pathlib import Path
asset="/Game/ScheminPreview/Generated/Commonwealth_Navigation_Hub"
sub=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
if not sub.load_level(asset):raise RuntimeError("Level loading failed")
actors=unreal.EditorLevelLibrary.get_all_level_actors()
ground=next((a for a in actors if a.get_actor_label()=="NAVIGATION_HUB_WALKABLE_DEMO_GROUND"),None)
spawns=[a for a in actors if isinstance(a,unreal.PlayerStart)]
if ground is None or not spawns:raise RuntimeError("Ground or spawn absent")
component=ground.static_mesh_component
collision=component.get_collision_enabled()
loc=ground.get_actor_location()
scale=ground.get_actor_scale3d()
spawn=spawns[0].get_actor_location()
result={"level":asset,"actor_count":len(actors),"ground_collision":str(collision),
"ground_z":loc.z,"ground_scale_z":scale.z,"spawn_z":spawn.z,
"spawn_above_ground_center":spawn.z>loc.z,
"play_in_editor_tested":False,"traversal_verified":False}
p=Path(unreal.Paths.project_dir())/"ScheminBridge/generated/navigation_collision_audit.json"
p.write_text(json.dumps(result,indent=2)+"\n")
if "NO_COLLISION" in str(collision).upper():raise RuntimeError("Ground collision disabled")
if not result["spawn_above_ground_center"]:raise RuntimeError("Spawn invalid")
print("SCHEMIN_NAV_COLLISION_AUDIT_PASS")
