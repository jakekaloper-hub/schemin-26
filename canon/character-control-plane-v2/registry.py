from models import CharacterRecord
def norm(s:str)->str: return " ".join(s.strip().lower().replace("’","'").split())
def compile_index(records:list[CharacterRecord]):
    by_id={}; index={}; retired={}
    for r in records:
        if r.character_id in by_id: raise ValueError("duplicate character_id: "+r.character_id)
        by_id[r.character_id]=r
        for value in (r.owner,r.current_team,r.identity,*r.aliases):
            k=norm(value)
            if k in index and index[k]!=r.character_id: raise ValueError("active alias collision: "+value)
            index[k]=r.character_id
        for value in r.retired_aliases:
            k=norm(value)
            if k in retired and retired[k]!=r.character_id: raise ValueError("retired alias collision: "+value)
            retired[k]=r.character_id
    return by_id,index,retired
def resolve(query:str,records:list[CharacterRecord]):
    by_id,index,retired=compile_index(records); q=norm(query)
    if q in index: return {"status":"CURRENT_CANON_RESOLVED","record":by_id[index[q]],"input_state":"ACTIVE"}
    if q in retired: return {"status":"CURRENT_CANON_RESOLVED","record":by_id[retired[q]],"input_state":"SUPERSEDED_ALIAS","warning":"retired identity cannot seed render"}
    return {"status":"HUMAN_REVIEW_REQUIRED","reason":"UNKNOWN_OR_UNMAPPED_ALIAS"}
