import unreal
src="/Game/ScheminPreview/Generated/Commonwealth_Regional_Showcase_Lit"
dst="/Game/ScheminPreview/Generated/Commonwealth_Editorial_Preview"
if not unreal.EditorAssetLibrary.does_asset_exist(dst):
 if not unreal.EditorAssetLibrary.duplicate_asset(src,dst):raise RuntimeError("duplicate failed")
level=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
if not level.load_level(dst):raise RuntimeError("load failed")
actors=unreal.EditorLevelLibrary.get_all_level_actors()
if not any(isinstance(x,unreal.CineCameraActor) for x in actors):
 camera=unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.CineCameraActor,unreal.Vector(8200,-9700,4800))
 camera.set_actor_label("Commonwealth_Editorial_Overview_Camera")
 camera.set_actor_rotation(unreal.Rotator(-27,35,0),False)
unreal.EditorLevelLibrary.save_current_level()
print("EDITORIAL_SCENE_SAVED actors="+str(len(actors)))
