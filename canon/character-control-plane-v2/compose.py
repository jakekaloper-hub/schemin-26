from dataclasses import asdict
from models import CharacterRecord,Layer,LAYER_WRITE_POLICY
def compose(record:CharacterRecord,layers:list[Layer]):
    state=asdict(record); state["_weekly_story_state"]={}; state["_scene_state"]={}; trace=[]
    for layer in layers:
        allowed=LAYER_WRITE_POLICY[layer.kind]
        illegal=set(layer.changes)-allowed
        if illegal: raise ValueError(f"{layer.kind} cannot write {sorted(illegal)}")
        if layer.kind=="EXPLICIT_COMMISSIONER_OVERRIDE" and not layer.provenance:
            raise ValueError("commissioner override requires approval provenance")
        if layer.kind=="WEEKLY_STORY_STATE": state["_weekly_story_state"].update(layer.changes)
        elif layer.kind=="SCENE_STATE": state["_scene_state"].update(layer.changes)
        else: state.update(layer.changes)
        trace.append({"kind":layer.kind,"fields":sorted(layer.changes),"provenance":layer.provenance})
    return state,trace
