"""Attempt MRQ execution with real RHI; output acceptance remains external."""
import unreal,json
from pathlib import Path
root=Path(unreal.Paths.project_dir())
report={"status":"NOT_RENDERED","sequence":"/Game/ScheminPreview/Cinematics/Commonwealth_Camera_Preview"}
sub=unreal.get_engine_subsystem(unreal.MoviePipelineQueueEngineSubsystem)
queue=sub.get_queue();queue.delete_all_jobs()
job=queue.allocate_new_job(unreal.MoviePipelineExecutorJob)
job.job_name="Commonwealth_OneFrame_Render_Probe"
job.map=unreal.SoftObjectPath("/Game/ScheminPreview/Generated/Commonwealth_Cinematic_Capture.Commonwealth_Cinematic_Capture")
job.sequence=unreal.SoftObjectPath("/Game/ScheminPreview/Cinematics/Commonwealth_Camera_Preview.Commonwealth_Camera_Preview")
cfg=job.get_configuration()
o=cfg.find_or_add_setting_by_class(unreal.MoviePipelineOutputSetting)
o.output_directory=unreal.DirectoryPath(str(root/"ScheminBridge/generated/mrq_frames"))
o.file_name_format="Commonwealth_{frame_number}"
o.output_resolution=unreal.IntPoint(640,360)
o.use_custom_playback_range=True
o.custom_start_frame=0
o.custom_end_frame=1
cfg.find_or_add_setting_by_class(unreal.MoviePipelineImageSequenceOutput_PNG)
report["job_prepared"]=True
try:
 executor=sub.render_queue_with_executor(unreal.MoviePipelineInProcessExecutor)
 report["executor_started"]=executor is not None
 report["status"]="EXECUTOR_REQUESTED_NOT_VERIFIED"
except Exception as exc:
 report["status"]="BLOCKED";report["error"]=str(exc)
(root/"ScheminBridge/generated/mrq_execution_probe.json").write_text(json.dumps(report,indent=2)+"\n")
print("MRQ_EXECUTION_PROBE",report["status"])
