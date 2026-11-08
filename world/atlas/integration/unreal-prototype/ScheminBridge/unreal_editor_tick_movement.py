"""Run inside interactive Unreal Editor via Python console, not headless commandlet."""
import json,math,time,traceback
from pathlib import Path
import unreal

DEST=Path(unreal.Paths.project_dir())/"ScheminBridge/generated/pie_ticking_movement_evidence.json"
LEVEL="/Game/ScheminPreview/Generated/Commonwealth_Navigation_Hub"
state={"phase":"LOAD","tick_count":0,"status":"RUNNING","pie_started":False,"pawn_found":False,"movement_verified":False,"distance_cm":0.0}
callback=None
def save():
    DEST.write_text(json.dumps(state,indent=2)+"\n")
def finish(status,error=None):
    global callback
    state["status"]=status
    if error:state["error"]=str(error)
    save()
    if callback is not None:
        unreal.unregister_slate_post_tick_callback(callback)
        callback=None
    unreal.log("SCHEMIN_PIE_MOVEMENT_"+status)
def tick(delta):
    try:
        state["tick_count"]+=1
        if state["tick_count"]>900:
            finish("BLOCKED","Timed out without measured pawn movement")
            return
        editor=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
        if state["phase"]=="BEGIN":
            editor.editor_request_begin_play()
            state["phase"]="WAIT_PIE"
            return
        worlds=unreal.EditorLevelLibrary.get_editor_world()
        # Only PIE worlds qualify, not editor-world actors.
        game=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
        if not game:return
        state["pie_started"]=True
        pc=unreal.GameplayStatics.get_player_controller(game,0)
        pawn=pc.get_pawn() if pc else None
        if pawn is None:return
        state["pawn_found"]=True
        current=pawn.get_actor_location()
        if state["phase"]=="WAIT_PIE":
            state["initial_xyz"]=[current.x,current.y,current.z]
            state["phase"]="MOVING"
            state["moving_ticks"]=0
        if state["phase"]=="MOVING":
            pawn.add_movement_input(unreal.Vector(1,0,0),1.0,False)
            state["moving_ticks"]+=1
            if state["moving_ticks"]>=90:
                start=state["initial_xyz"]
                state["final_xyz"]=[current.x,current.y,current.z]
                distance=math.dist(start,state["final_xyz"])
                state["distance_cm"]=round(distance,2)
                state["movement_verified"]=distance>=50
                finish("PASS" if state["movement_verified"] else "BLOCKED",None if state["movement_verified"] else "Movement below 50cm")
    except Exception as exc:
        finish("BLOCKED",traceback.format_exc())
# Register callback only in a real ticking Editor session.
if not unreal.EditorAssetLibrary.does_asset_exist(LEVEL):
    raise RuntimeError("Navigation Hub asset missing")
editor=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
if not editor.load_level(LEVEL):
    raise RuntimeError("Unable to load navigation hub")
state["phase"]="BEGIN"
save()
callback=unreal.register_slate_post_tick_callback(tick)
unreal.log("SCHEMIN_PIE_TICK_PROBE_ARMED")
