"""Unreal Editor Python script: preview-only scene placement.
Run inside UE Python console after enabling Python Editor Script Plugin.
Does not replace the active map, publish assets or mutate Schemin canon.
"""
import hashlib
import json
from pathlib import Path
import unreal

ROOT=Path(unreal.Paths.project_dir())
MANIFEST=ROOT/"ScheminBridge/examples/trade_jedi_preview.json"
SNAPSHOT=ROOT/"ScheminBridge/canonical_locations_snapshot.json"
m=json.loads(MANIFEST.read_text())
s=SNAPSHOT.read_bytes()
expected="d3aa0d5fca9bf120ad8f1ecc6267f0cbce54bdf83b8117c0328c8d13cd0aeaeb"
assert hashlib.sha256(s).hexdigest()==expected,"source snapshot differs"
assert m["location_evidence"]["snapshot_sha256"]==expected
assert m["source_commit"]=="7afe7ef0fcf24e25d67ca8c85d4e6e36e03a78e3"
assert m["status"]=="PREVIEW" and m["canon_approved"] is False
assert m["characters"]==[] and m["asset_bindings"]==[]
assert m["espn_event"] is None and m["mutates_world_state"] is False
assert m["location_id"]=="LOC-TRADE-JEDI-MOUNTAIN-BASE"
assert m["source_location"]["coordinate_space"]=="schemin-local-v1 (abstract, non-metric)"
assert m["source_location"]["landmarks"]==["high ridge","war-room overlook"]

# Non-destructive scratch world; geometry is conceptual, not geographic fact.
asset_path="/Game/ScheminPreview/Maps/TradeJediMountain_Preview"
if unreal.EditorAssetLibrary.does_asset_exist(asset_path):
    raise RuntimeError("Preview map already exists; refusing to overwrite")
world=unreal.EditorLevelLibrary.new_level(asset_path)
if not world: raise RuntimeError("Could not create preview level")
mesh=unreal.load_asset("/Engine/BasicShapes/Cube.Cube")
if not mesh: raise RuntimeError("Unreal primitive cube missing")
positions=[
 ("PREVIEW_ground_not_canonical",unreal.Vector(0,0,-100),unreal.Vector(18,18,1)),
 ("PREVIEW_high_ridge_proxy",unreal.Vector(650,100,120),unreal.Vector(5,2,4)),
 ("PREVIEW_war_room_overlook_proxy",unreal.Vector(-600,-250,100),unreal.Vector(3,3,3))
]
for name,pos,scale in positions:
    a=unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.StaticMeshActor,pos)
    a.set_actor_label(name)
    a.static_mesh_component.set_static_mesh(mesh)
    a.set_actor_scale3d(scale)
    a.set_editor_property("tags",["ScheminPreview","NoCanonPromotion"])
unreal.EditorLevelLibrary.save_current_level()
unreal.log("SCHEMIN_PREVIEW_MAP_CREATED "+asset_path)
