"""CCCP v1 deterministic character resolver. Repository-native; fail closed."""
REGISTRY = {
"CHAR-JAKE-KALOPER": {"owner":"Jake Kaloper","team":"ObiWan Jacoby","identity":"The Trade Jedi","aliases":[],"version":"1.0"},
"CHAR-KEVIN-ZEEK": {"owner":"Kevin Zeek","team":"Red Leopards","identity":"The Predator Board","aliases":[],"version":"1.0"},
"CHAR-JORDAN-HOLLINGSHEAD": {"owner":"Jordan Hollingshead","team":"Slob on my Dobb","identity":"Frat-Bro Berserker","aliases":["Fart Star","Win Ugly"],"version":"1.0"},
"CHAR-DAVID-BABB": {"owner":"David Babb","team":"The LLC.","identity":"Hostile Takeover","aliases":["The LLC"],"version":"1.0"},
"CHAR-WILSON-LOOK": {"owner":"Wilson Look","team":"Donkey Kong","identity":"Arsenal Gorilla Centaur Warrior","aliases":["Baker Moore Purdy","Arsenal Gorilla Warrior","Arsenal Centaur","Philosopher-Warrior"],"version":"2.1","superseded":[]},
"CHAR-PHILLIP-PITTS": {"owner":"Phillip Pitts","team":"Three Dreaded Snake","identity":"The Podium Shadow","aliases":[],"version":"1.0"},
"CHAR-BRANDON-PRYOR": {"owner":"Brandon Pryor","team":"Chili Cheesers","identity":"The Chili Outlaw","aliases":[],"version":"1.0"},
"CHAR-MANNING-WELTY": {"owner":"Manning Welty","team":"El Niño","identity":"The Weather System","aliases":["El Nino"],"version":"1.0"},
"CHAR-AUSTIN-BYARS": {"owner":"Austin Byars","team":"His Majesty's Blood","identity":"The Belt Keeper","aliases":["The Immortal","That's Fantasy"],"version":"1.0"},
"CHAR-BOBBY-MITCHELL": {"owner":"Bobby Mitchell","team":"Mud Dogs","identity":"Swamp-Born Menace","aliases":[],"version":"1.0"},
"CHAR-ZACH-WILSON": {"owner":"Zach Wilson","team":"Dr. Duckhook","identity":"King of the Impossible Lie","aliases":[],"version":"1.0"},
"CHAR-BEN-WHIPPLE": {"owner":"Ben Whipple","team":"Seven Deadly Chins","identity":"The People's Champ","aliases":["Blue-Collar Spoiler"],"version":"1.0"},
}
def _norm(s): return " ".join(str(s).strip().lower().replace("’","'").split())
def resolve_character(query):
    q=_norm(query); hits=[]; retired=[]
    for cid,r in REGISTRY.items():
        active=[cid,r["owner"],r["team"],r["identity"],*r.get("aliases",[])]
        if q in {_norm(x) for x in active}: hits.append((cid,r))
        if q in {_norm(x) for x in r.get("superseded",[])}: retired.append((cid,r))
    if len(hits)==1:
        cid,r=hits[0]; return {"status":"CURRENT_CANON_RESOLVED","character_id":cid,**r}
    if len(hits)>1: return {"status":"HUMAN_REVIEW_REQUIRED","reason":"AMBIGUOUS_ACTIVE_ALIAS","candidates":[x[0] for x in hits]}
    if len(retired)==1:
        cid,r=retired[0]; return {"status":"CURRENT_CANON_RESOLVED","character_id":cid,**r,"input_state":"SUPERSEDED_ALIAS","warning":"Retired identity cannot seed render."}
    return {"status":"HUMAN_REVIEW_REQUIRED","reason":"UNKNOWN_OR_UNMAPPED_ALIAS","query":query}
