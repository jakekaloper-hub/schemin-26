import unreal
path="/Game/ScheminPreview/Generated/TradeJedi_Walkable_Test"
sub=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
if not sub.load_level(path):raise RuntimeError("Unable to load Commonwealth starter level")
actors=unreal.EditorLevelLibrary.get_all_level_actors()
labels={a.get_actor_label() for a in actors}
need={"PREVIEW_walkable_ground","PREVIEW_high_ridge","PREVIEW_overlook","PREVIEW_TEST_PLAYER_SPAWN","PREVIEW_TEST_SUN"}
if not need.issubset(labels):raise RuntimeError("Missing actors: "+str(need-labels))
spawns=[a for a in actors if isinstance(a,unreal.PlayerStart)]
if len(spawns)<1:raise RuntimeError("No player spawn")
print("COMMONWEALTH_STARTER_VERIFIED actor_count="+str(len(actors))+" spawn_count="+str(len(spawns)))
