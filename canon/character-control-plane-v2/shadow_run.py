from records import RECORDS
from registry import resolve
CASES={
"ObiWan Jacoby":("CHAR-JAKE-KALOPER","The Trade Jedi"),
"Red Leopards":("CHAR-KEVIN-ZEEK","The Predator Board"),
"Slob on my Dobb":("CHAR-JORDAN-HOLLINGSHEAD","Frat-Bro Berserker"),
"The LLC":("CHAR-DAVID-BABB","Hostile Takeover"),
"Baker Moore Purdy":("CHAR-WILSON-LOOK","Arsenal Gorilla Centaur Warrior"),
"Donkey Kong":("CHAR-WILSON-LOOK","Arsenal Gorilla Centaur Warrior"),
"Three Dreaded Snake":("CHAR-PHILLIP-PITTS","The Podium Shadow"),
"Chili Cheesers":("CHAR-BRANDON-PRYOR","The Chili Outlaw"),
"El Nino":("CHAR-MANNING-WELTY","The Weather System"),
"The Immortal":("CHAR-AUSTIN-BYARS","The Belt Keeper"),
"That's Fantasy":("CHAR-AUSTIN-BYARS","The Belt Keeper"),
"His Majesty's Blood":("CHAR-AUSTIN-BYARS","The Belt Keeper"),
"Mud Dogs":("CHAR-BOBBY-MITCHELL","Swamp-Born Menace"),
"Dr. Duckhook":("CHAR-ZACH-WILSON","King of the Impossible Lie"),
"Seven Deadly Chins":("CHAR-BEN-WHIPPLE","The People's Champ"),
}
def run():
 failures=[]
 for q,(cid,identity) in CASES.items():
  x=resolve(q,RECORDS)
  if x.get("status")!="CURRENT_CANON_RESOLVED" or x["record"].character_id!=cid or x["record"].identity!=identity: failures.append(q)
 return failures
if __name__=="__main__":
 f=run()
 if f: raise SystemExit("shadow failures: "+repr(f))
 print("shadow contract PASS",len(CASES))
