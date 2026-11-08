import subprocess,pathlib,json,time
root=pathlib.Path.home()/"Developer/ai/Schemin_UE_Prototype"
engine=pathlib.Path.home()/"Desktop/Desktop - Jake’s MacBook Pro/UE_5.8/Engine/Binaries/Mac/UnrealEditor-Cmd"
args=[str(engine),str(root/"Schemin_UE_Prototype.uproject"),"/Game/ScheminPreview/Generated/Commonwealth_Cinematic_Capture","-game","-LevelSequence=/Game/ScheminPreview/Cinematics/Commonwealth_Camera_Preview.Commonwealth_Camera_Preview","-MoviePipelineConfig=/Game/ScheminPreview/Cinematics/Commonwealth_OneFrame_Preset.Commonwealth_OneFrame_Preset","-windowed","-resx=640","-resy=360","-nosplash","-unattended","-notexturestreaming"]
log=root/"ScheminBridge/generated/mrq_gameworld.log"
started=time.monotonic()
with open(log,"w") as f:
 try:
  result=subprocess.run(args,stdout=f,stderr=subprocess.STDOUT,timeout=75)
  status="EXITED";code=result.returncode
 except subprocess.TimeoutExpired:
  status="TIMED_OUT_TERMINATED";code=None
files=list((root/"ScheminBridge/generated/mrq_frames").glob("*")) if (root/"ScheminBridge/generated/mrq_frames").exists() else []
receipt={"status":status,"exit_code":code,"duration_seconds":round(time.monotonic()-started,1),"render_files":[str(x) for x in files],"frames_verified":False}
(root/"ScheminBridge/generated/mrq_gameworld_receipt.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(receipt)
