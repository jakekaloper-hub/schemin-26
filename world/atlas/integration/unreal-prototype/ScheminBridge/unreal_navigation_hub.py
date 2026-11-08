"""Create walkable demonstration next to abstract Atlas visual markers; not metric travel."""
import unreal
src="/Game/ScheminPreview/Generated/Commonwealth_Route_Overview"
dst="/Game/ScheminPreview/Generated/Commonwealth_Navigation_Hub"
if not unreal.EditorAssetLibrary.does_asset_exist(dst):
 if not unreal.EditorAssetLibrary.duplicate_asset(src,dst):raise RuntimeError("Cannot duplicate route map")
sub=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
if not sub.load_level(dst):raise RuntimeError("Cannot load navigation hub")
actors=unreal.EditorLevelLibrary.get_all_level_actors()
labels={a.get_actor_label() for a in actors}
cube=unreal.load_asset("/Engine/BasicShapes/Cube.Cube")
def proxy(name,pos,scale):
 if name in labels:return
 a=unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.StaticMeshActor,unreal.Vector(*pos))
 a.set_actor_label(name);a.static_mesh_component.set_static_mesh(cube)
 a.set_actor_scale3d(unreal.Vector(*scale))
 a.set_editor_property("tags",["ScheminPreview","AbstractNonMetric","NoCanonPromotion"])
proxy("NAVIGATION_HUB_WALKABLE_DEMO_GROUND",(0,0,-180),(18,18,1))
if not any(isinstance(a,unreal.PlayerStart) for a in actors):
 p=unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.PlayerStart,unreal.Vector(0,0,160))
 p.set_actor_label("NAVIGATION_HUB_PLAYER_START")
if not any(isinstance(a,unreal.DirectionalLight) for a in actors):
 l=unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.DirectionalLight,unreal.Vector(0,0,1500))
 l.set_actor_label("NAVIGATION_HUB_SUN")
if not any(isinstance(a,unreal.SkyLight) for a in actors):
 l=unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.SkyLight,unreal.Vector(0,0,1000))
 l.set_actor_label("NAVIGATION_HUB_SKYLIGHT")
unreal.EditorLevelLibrary.save_current_level()
print("NAVIGATION_HUB_CREATED")
