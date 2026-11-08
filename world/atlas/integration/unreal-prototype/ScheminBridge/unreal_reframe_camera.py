import unreal,json,math
from pathlib import Path
level="/Game/ScheminPreview/Generated/Commonwealth_Cinematic_Capture"
if not unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).load_level(level):raise RuntimeError("load failed")
actors=unreal.EditorLevelLibrary.get_all_level_actors()
cam=next((a for a in actors if a.get_actor_label()=="COMMONWEALTH_CAPTURE_CAMERA"),None)
if not cam:raise RuntimeError("camera absent")
target=unreal.Vector(0,0,50)
start=unreal.Vector(-1900,-2100,1050)
delta=target-start
rotation=unreal.Rotator(math.degrees(math.atan2(delta.z,math.hypot(delta.x,delta.y))),math.degrees(math.atan2(delta.y,delta.x)),0)
cam.set_actor_location(start,False,False)
cam.set_actor_rotation(rotation,False)
unreal.EditorLevelLibrary.save_current_level()
receipt={"camera":[start.x,start.y,start.z],"look_at":[target.x,target.y,target.z],"rotation":[rotation.pitch,rotation.yaw,rotation.roll],"target":"first interpretive region exhibit","canon_promoted":False}
(Path(unreal.Paths.project_dir())/"ScheminBridge/generated/camera_reframe_receipt.json").write_text(json.dumps(receipt,indent=2))
print("CAMERA_REFRAMED",receipt)
