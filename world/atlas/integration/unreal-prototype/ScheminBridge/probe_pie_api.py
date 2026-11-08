import unreal,json
from pathlib import Path
names=["register_slate_post_tick_callback","unregister_slate_post_tick_callback","UnrealEditorSubsystem","get_game_world","EditorLevelSubsystem"]
out={}
for name in names:out[name]=hasattr(unreal,name)
if out["UnrealEditorSubsystem"]:
 t=unreal.UnrealEditorSubsystem
 out["UnrealEditorSubsystem_methods"]=[x for x in dir(t) if "world" in x.lower() or "pie" in x.lower()]
out["LevelEditorSubsystem_methods"]=[x for x in dir(unreal.LevelEditorSubsystem) if "play" in x.lower()]
Path(unreal.Paths.project_dir()+"/ScheminBridge/generated/pie_api_probe.json").write_text(json.dumps(out,indent=2))
print(out)
