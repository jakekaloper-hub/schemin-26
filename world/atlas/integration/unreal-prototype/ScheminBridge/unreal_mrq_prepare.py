import unreal,json
from pathlib import Path
root=Path(unreal.Paths.project_dir())
report={"sequence":"/Game/ScheminPreview/Cinematics/Commonwealth_Camera_Preview","map":"/Game/ScheminPreview/Generated/Commonwealth_Cinematic_Capture","status":"BLOCKED"}
if not unreal.EditorAssetLibrary.does_asset_exist(report["sequence"]):raise RuntimeError("sequence absent")
if not unreal.EditorAssetLibrary.does_asset_exist(report["map"]):raise RuntimeError("map absent")
if not hasattr(unreal,"MoviePipelineQueueEngineSubsystem"):raise RuntimeError("Movie Render Queue plugin not enabled")
queue_sub=unreal.get_engine_subsystem(unreal.MoviePipelineQueueEngineSubsystem)
queue=queue_sub.get_queue()
queue.delete_all_jobs()
job=queue.allocate_new_job(unreal.MoviePipelineExecutorJob)
job.job_name="Commonwealth_Camera_Preview"
job.map=unreal.SoftObjectPath(report["map"]+"."+report["map"].split("/")[-1])
job.sequence=unreal.SoftObjectPath(report["sequence"]+"."+report["sequence"].split("/")[-1])
settings=job.get_configuration()
output=settings.find_or_add_setting_by_class(unreal.MoviePipelineOutputSetting)
output.output_directory=unreal.DirectoryPath(str(root/"ScheminBridge/generated/mrq_frames"))
output.file_name_format="Commonwealth_{frame_number}"
output.output_resolution=unreal.IntPoint(1280,720)
output.use_custom_frame_rate=True
output.output_frame_rate=unreal.FrameRate(24,1)
settings.find_or_add_setting_by_class(unreal.MoviePipelineImageSequenceOutput_PNG)
report.update({"status":"MRQ_JOB_PREPARED_NOT_RENDERED","job_count":len(queue.get_jobs()),"output_dir":str(root/"ScheminBridge/generated/mrq_frames")})
(root/"ScheminBridge/generated/mrq_preparation.json").write_text(json.dumps(report,indent=2)+"\n")
print("SCHEMIN_MRQ_JOB_PREPARED")
