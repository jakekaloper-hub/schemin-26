"""Create a non-canonical walkable geometry test map with PlayerStart.
No claim of fully playable map until PIE runs on Mac.
"""
import unreal
asset="/Game/ScheminPreview/Generated/TradeJedi_Walkable_Test"
if unreal.EditorAssetLibrary.does_asset_exist(asset):
 unreal.log("WALKABLE_ALREADY_EXISTS")
else:
 if not unreal.EditorLevelLibrary.new_level(asset):raise RuntimeError("new level failed")
 cube=unreal.load_asset("/Engine/BasicShapes/Cube.Cube")
 specs=[("PREVIEW_walkable_ground",(0,0,-100),(25,25,1)),
 ("PREVIEW_high_ridge",(800,200,100),(5,2,3)),
 ("PREVIEW_overlook",(-700,100,100),(5,5,2))]
 for name,pos,scale in specs:
  actor=unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.StaticMeshActor,unreal.Vector(*pos))
  actor.set_actor_label(name)
  actor.static_mesh_component.set_static_mesh(cube)
  actor.set_actor_scale3d(unreal.Vector(*scale))
 start=unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.PlayerStart,unreal.Vector(0,0,100))
 start.set_actor_label("PREVIEW_TEST_PLAYER_SPAWN")
 light=unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.DirectionalLight,unreal.Vector(0,0,700))
 light.set_actor_label("PREVIEW_TEST_SUN")
 unreal.EditorLevelLibrary.save_current_level()
 unreal.log("WALKABLE_PREVIEW_ASSET_SAVED")
