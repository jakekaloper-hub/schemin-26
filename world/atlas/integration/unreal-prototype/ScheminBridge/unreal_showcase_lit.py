"""Non-destructive lit copy of Commonwealth showcase, no canon promotion."""
import unreal
src="/Game/ScheminPreview/Generated/Commonwealth_Regional_Showcase"
dst="/Game/ScheminPreview/Generated/Commonwealth_Regional_Showcase_Lit"
if unreal.EditorAssetLibrary.does_asset_exist(dst):
    unreal.log("SCHEMIN_LIT_MAP_ALREADY_EXISTS")
else:
    if not unreal.EditorAssetLibrary.duplicate_asset(src,dst):
        raise RuntimeError("Could not duplicate Commonwealth map")
sub=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
if not sub.load_level(dst):raise RuntimeError("Could not load lit map")
actors=unreal.EditorLevelLibrary.get_all_level_actors()
if not any(isinstance(a,unreal.SkyLight) for a in actors):
    sky=unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.SkyLight,unreal.Vector(0,0,400))
    sky.set_actor_label("COMMONWEALTH_PREVIEW_Skylight")
if not any(isinstance(a,unreal.SkyAtmosphere) for a in actors):
    atmosphere=unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.SkyAtmosphere,unreal.Vector(0,0,0))
    atmosphere.set_actor_label("COMMONWEALTH_PREVIEW_Atmosphere")
if not any(isinstance(a,unreal.ExponentialHeightFog) for a in actors):
    fog=unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.ExponentialHeightFog,unreal.Vector(0,0,0))
    fog.set_actor_label("COMMONWEALTH_PREVIEW_Fog")
for a in actors:
    if isinstance(a,unreal.DirectionalLight):
        a.set_actor_rotation(unreal.Rotator(-42,-28,0),False)
unreal.EditorLevelLibrary.save_current_level()
unreal.log("SCHEMIN_LIT_SHOWCASE_SAVED")
