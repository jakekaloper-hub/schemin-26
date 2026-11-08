import unreal
p="/Game/ScheminPreview/Maps/TradeJediMountain_Preview"
sub=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
if not sub.load_level(p): raise RuntimeError("Failed loading preview")
actors=unreal.EditorLevelLibrary.get_all_level_actors()
labels=[a.get_actor_label() for a in actors]
required={"PREVIEW_ground_not_canonical","PREVIEW_high_ridge_proxy","PREVIEW_war_room_overlook_proxy"}
missing=required-set(labels)
if missing: raise RuntimeError("Missing preview actors: "+str(missing))
print("SCHEMIN_LEVEL_VERIFIED actors="+str(len(actors))+" required="+str(len(required)))
