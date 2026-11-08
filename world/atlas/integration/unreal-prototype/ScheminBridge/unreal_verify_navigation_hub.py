import unreal
p="/Game/ScheminPreview/Generated/Commonwealth_Navigation_Hub"
if not unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).load_level(p):
 raise RuntimeError("Navigation hub cannot load")
actors=unreal.EditorLevelLibrary.get_all_level_actors()
labels={a.get_actor_label() for a in actors}
needed={"NAVIGATION_HUB_WALKABLE_DEMO_GROUND","NAVIGATION_HUB_PLAYER_START","NAVIGATION_HUB_SUN","NAVIGATION_HUB_SKYLIGHT"}
if not needed.issubset(labels): raise RuntimeError("Missing actors: "+str(needed-labels))
markers=[x for x in labels if x.startswith("ATLAS_")]
routes=[x for x in labels if x.startswith("ROUTE_PROXY_")]
if len(markers)!=23 or len(routes)<18:raise RuntimeError("Atlas graph actors incomplete "+str((len(markers),len(routes))))
print("NAV_HUB_VERIFIED markers="+str(len(markers))+" segments="+str(len(routes))+" actors="+str(len(actors)))
