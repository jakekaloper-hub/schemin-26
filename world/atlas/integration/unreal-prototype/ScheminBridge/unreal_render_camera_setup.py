"""Prepare dedicated UE cinematic capture level with camera, without attempting headless screenshot."""
import unreal
src="/Game/ScheminPreview/Generated/Commonwealth_Regional_Showcase_Lit"
dst="/Game/ScheminPreview/Generated/Commonwealth_Cinematic_Capture"
if not unreal.EditorAssetLibrary.does_asset_exist(dst):
 if not unreal.EditorAssetLibrary.duplicate_asset(src,dst):raise RuntimeError("duplicate failed")
if not unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).load_level(dst):raise RuntimeError("cannot load")
actors=unreal.EditorLevelLibrary.get_all_level_actors()
if not any(a.get_actor_label()=="COMMONWEALTH_CAPTURE_CAMERA" for a in actors):
 camera=unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.CineCameraActor,unreal.Vector(-2400,-3000,1700))
 camera.set_actor_label("COMMONWEALTH_CAPTURE_CAMERA")
 camera.set_actor_rotation(unreal.Rotator(-20,45,0),False)
unreal.EditorLevelLibrary.save_current_level()
print("COMMONWEALTH_CINEMATIC_CAPTURE_MAP_READY")
