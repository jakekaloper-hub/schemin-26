import unreal,json
from pathlib import Path
root=Path(unreal.Paths.project_dir())
level="/Game/ScheminPreview/Generated/Commonwealth_Regional_Showcase_Lit"
if not unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).load_level(level):
 raise RuntimeError("showcase cannot load")
out=root/"ScheminBridge/generated/rendered_showcase_preview.png"
# Screenshot task requested through Unreal automation API. A screenshot request is NOT proof of rendered frames.
unreal.AutomationLibrary.take_high_res_screenshot(1280,720,str(out),None,False,False)
report={"level":level,"requested_output":str(out),"screenshot_requested":True,"render_verified":False}
(root/"ScheminBridge/generated/render_request.json").write_text(json.dumps(report,indent=2)+"\n")
print("SCHEMIN_SCREENSHOT_REQUESTED")
