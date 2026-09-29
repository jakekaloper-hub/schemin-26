from dataclasses import asdict
from models import CharacterRecord,Layer,LAYER_WRITE_POLICY
def compose(record:CharacterRecord,layers:list[Layer]):
    state=asdict(record); trace=[]
    for layer in layers:
        allowed=LAYER_WRITE_POLICY[layer.kind]
        illegal=set(layer.changes)-allowed
        if illegal: raise ValueError(f"{layer.kind} cannot write {sorted(illegal)}")
        state.update(layer.changes); trace.append({"kind":layer.kind,"fields":sorted(layer.changes),"provenance":layer.provenance})
    return state,trace
