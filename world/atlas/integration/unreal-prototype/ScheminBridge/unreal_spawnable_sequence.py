import unreal,math
level="/Game/ScheminPreview/Generated/Commonwealth_Cinematic_Capture"
if not unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).load_level(level):raise RuntimeError("level unavailable")
name="Commonwealth_Spawnable_Camera"
folder="/Game/ScheminPreview/Cinematics"
path=folder+"/"+name
if unreal.EditorAssetLibrary.does_asset_exist(path):raise RuntimeError("already exists")
seq=unreal.AssetToolsHelpers.get_asset_tools().create_asset(name,folder,unreal.LevelSequence,unreal.LevelSequenceFactoryNew())
seq.set_display_rate(unreal.FrameRate(24,1));seq.set_playback_start(0);seq.set_playback_end(24)
cam=unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.CineCameraActor,unreal.Vector(-1900,-2100,1050))
cam.set_actor_label("TEMP_SPAWNABLE_SOURCE_CAMERA")
delta=unreal.Vector(0,0,50)-cam.get_actor_location()
rot=unreal.Rotator(math.degrees(math.atan2(delta.z,math.hypot(delta.x,delta.y))),math.degrees(math.atan2(delta.y,delta.x)),0)
cam.set_actor_rotation(rot,False)
binding=seq.add_spawnable_from_instance(cam)
cut=seq.add_track(unreal.MovieSceneCameraCutTrack)
section=cut.add_section();section.set_range(0,24)
bid=unreal.MovieSceneObjectBindingID()
bid.set_editor_property("guid",binding.get_id())
section.set_camera_binding_id(bid)
unreal.EditorAssetLibrary.save_loaded_asset(seq)
unreal.EditorLevelLibrary.destroy_actor(cam)
print("SPAWNABLE_CAMERA_SEQUENCE_CREATED")
