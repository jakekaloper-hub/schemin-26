import unreal,json
from pathlib import Path
level="/Game/ScheminPreview/Generated/Commonwealth_Navigation_Hub"
if not unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).load_level(level):raise RuntimeError("Level not loadable")
actors=unreal.EditorLevelLibrary.get_all_level_actors()
spawn=next((a for a in actors if isinstance(a,unreal.PlayerStart)),None)
ground=next((a for a in actors if a.get_actor_label()=="NAVIGATION_HUB_WALKABLE_DEMO_GROUND"),None)
if not spawn or not ground:raise RuntimeError("Missing spawn or ground")
mode=unreal.load_asset("/Game/ThirdPerson/Blueprints/BP_ThirdPersonGameMode")
if not mode:raise RuntimeError("Third Person GameMode missing")
result={"level":level,"third_person_game_mode_asset":True,
"spawn":list(spawn.get_actor_location().to_tuple()),
"ground_collision":str(ground.static_mesh_component.get_collision_enabled()),
"pie_executed":False,"runtime_movement_verified":False,
"status":"PRECONDITIONS_PASS_RUNTIME_TEST_REQUIRED"}
out=Path(unreal.Paths.project_dir())/"ScheminBridge/generated/gameplay_preconditions.json"
out.write_text(json.dumps(result,indent=2)+"\n")
print("SCHEMIN_GAMEPLAY_PRECONDITIONS_PASS")
