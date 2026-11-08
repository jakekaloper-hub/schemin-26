# Commonwealth Atlas Unreal pipeline
Source is fixed to an exact-byte canonical world/data/locations.json snapshot at commit 7afe7ef0.
Run: python3 -m ScheminBridge.build_world_manifest
Then execute ScheminBridge/unreal_build_atlas.py inside UnrealEditor-Cmd using -run=pythonscript.
Generated Unreal levels use abstract proxy primitives, not metric cartography or completed environment art.
All 23 locations are exposed for inspection; 8 permanent, 12 provisional, 3 interpretive.
Character assets and world-state mutation are prohibited in this preview lane.
Do not merge/publish into canon without governing validation and Umpire review.
