import unreal
level="/Game/ScheminPreview/Generated/Commonwealth_Cinematic_Capture"
sequence_path="/Game/ScheminPreview/Cinematics/Commonwealth_Camera_Preview"
sub=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
if not sub.load_level(level):raise RuntimeError("cinematic level unavailable")
camera=next((x for x in unreal.EditorLevelLibrary.get_all_level_actors() if x.get_actor_label()=="COMMONWEALTH_CAPTURE_CAMERA"),None)
if not camera:raise RuntimeError("source camera missing")
if unreal.EditorAssetLibrary.does_asset_exist(sequence_path):
 sequence=unreal.load_asset(sequence_path)
else:
 tools=unreal.AssetToolsHelpers.get_asset_tools()
 sequence=tools.create_asset("Commonwealth_Camera_Preview","/Game/ScheminPreview/Cinematics",unreal.LevelSequence,unreal.LevelSequenceFactoryNew())
if not sequence:raise RuntimeError("sequence creation failed")
sequence.set_display_rate(unreal.FrameRate(24,1))
sequence.set_playback_start(0)
sequence.set_playback_end(240)
binding=sequence.add_possessable(camera)
if not binding:raise RuntimeError("camera binding failed")
cut=sequence.add_track(unreal.MovieSceneCameraCutTrack)
section=cut.add_section()
section.set_range(0,240)
binding_id=unreal.MovieSceneObjectBindingID()
binding_id.set_editor_property("guid",binding.get_id())
section.set_camera_binding_id(binding_id)
unreal.EditorAssetLibrary.save_loaded_asset(sequence)
print("SCHEMIN_CAMERA_SEQUENCE_SAVED")
