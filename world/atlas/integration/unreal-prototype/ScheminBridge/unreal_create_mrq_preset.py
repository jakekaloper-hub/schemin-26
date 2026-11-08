import unreal
name="Commonwealth_OneFrame_Preset"
folder="/Game/ScheminPreview/Cinematics"
full=folder+"/"+name
if unreal.EditorAssetLibrary.does_asset_exist(full):
 cfg=unreal.load_asset(full)
else:
 cfg=unreal.AssetToolsHelpers.get_asset_tools().create_asset(name,folder,unreal.MoviePipelinePrimaryConfig,unreal.MoviePipelinePrimaryConfigFactory())
if not cfg:raise RuntimeError("cannot create MRQ preset")
out=cfg.find_or_add_setting_by_class(unreal.MoviePipelineOutputSetting)
out.output_directory=unreal.DirectoryPath("/Users/jakekaloper/Developer/ai/Schemin_UE_Prototype/ScheminBridge/generated/mrq_frames")
out.file_name_format="Commonwealth_{frame_number}"
out.output_resolution=unreal.IntPoint(640,360)
out.use_custom_playback_range=True
out.custom_start_frame=0
out.custom_end_frame=1
cfg.find_or_add_setting_by_class(unreal.MoviePipelineImageSequenceOutput_PNG)
cfg.find_or_add_setting_by_class(unreal.MoviePipelineDeferredPassBase)
unreal.EditorAssetLibrary.save_loaded_asset(cfg)
print("MRQ_PRESET_SAVED")
