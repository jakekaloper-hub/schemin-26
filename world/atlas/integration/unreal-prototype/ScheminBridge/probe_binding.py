import unreal
x=unreal.MovieSceneObjectBindingID()
print("BINDING_MEMBERS",[v for v in dir(x) if "guid" in v or "binding" in v or "space" in v or "sequence" in v])
print("BINDING_HELP",unreal.MovieSceneObjectBindingID.__doc__)
print("SECTION_HELP",unreal.MovieSceneCameraCutSection.set_camera_binding_id.__doc__)
