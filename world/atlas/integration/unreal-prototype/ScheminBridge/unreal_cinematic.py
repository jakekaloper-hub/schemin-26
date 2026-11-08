import unreal
asset="/Game/ScheminPreview/Cinematics/TradeJedi_Overview_Sequence"
if unreal.EditorAssetLibrary.does_asset_exist(asset):
    raise RuntimeError("Sequence exists; refusing overwrite")
tools=unreal.AssetToolsHelpers.get_asset_tools()
seq=tools.create_asset("TradeJedi_Overview_Sequence","/Game/ScheminPreview/Cinematics",
    unreal.LevelSequence,unreal.LevelSequenceFactoryNew())
if not seq: raise RuntimeError("Sequence creation failed")
seq.set_display_rate(unreal.FrameRate(24,1))
seq.set_playback_start(0)
seq.set_playback_end(240)
unreal.EditorAssetLibrary.save_loaded_asset(seq)
print("SCHEMIN_CINEMATIC_SEQUENCE_CREATED "+asset)
