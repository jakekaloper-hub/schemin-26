#!/usr/bin/env python3
"""Source-bounded, explicitly simulated methodology review using existing Inklings contract."""
from __future__ import annotations
import hashlib, json, importlib.util
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
COUNCIL=ROOT/"living-novel/consultants/author-council"
ADVISORS=ROOT/"living-novel/consultants/ADVISOR_REGISTRY_V1.json"
BENCH=ROOT/"memo-os/cinematography/PRODUCTION_SPECIALIST_REFERENCE_BENCH_V1.json"
EVIDENCE=ROOT/"memo-os/week-10/preproduction/render-inputs/manifest.json"

def item(n,advisor,page,observation,proposal,decision,rationale):
    return {"id":f"W10-FILM-REVIEW-{n:02d}","advisor":advisor,
    "source_anchor":f"memo-os/week-10/preproduction/render-inputs/{page}/request.json",
    "observation":observation,"proposal":proposal,"decision":decision,"rationale":rationale}

findings=[
item(1,"Doug Chiang","W10-P22","The field throne is an established place and its chair/battery/steps control blocking.",
"Build one shared dimensional set plate across P22-P24, with reusable stair and battery anchors; reject unrelated throne-room changes.","ACCEPT","A reusable set layout prevents jump cuts from altering what surrender means."),
item(2,"Dylan Cole","W10-P11","One storm presents regional differences; coast, bridge and wetland are not adjacent.",
"Maintain three distinct weather looks with explicit editorial time transition; use bridge master for orientation.","ACCEPT","Visual cohesion without fictional instant travel."),
item(3,"Joe Letteri","W10-P12","Three Dreaded Snake has exactly three heads on one body; other characters retain their species locks.",
"Preapprove silhouette, rig topology and motion tests for nonhuman characters before all ensemble frames.","ACCEPT","Long-form animation magnifies identity drift."),
item(4,"Ngila Dickson","W10-P08","Red carries wet mud from field into later Forgotten Court, across separated locations.",
"Keep tracked costume wetness, surface mud and material wear per character/time; recheck after edits.","ACCEPT","Weather and travel effects must persist without cloning character assets."),
item(5,"Andy Serkis","W10-P07","Humiliation is public and reactive; the captured outlaw is not an injured generic victim.",
"Hold gaze toward galleries after the secure manual binding, with physically readable body language.","ADAPT","Performance delivers emotional stakes without inventing an injury or dialogue."),
item(6,"Rob Alonzo","W10-P06","The lasso closes around torso/upper arms, never neck; skid causes fall before manual tie.",
"Use three causal movement setups and stunt-safe geometry references before any AI motion render.","HOLD","The source explicitly prevents instant knots and hazardous neck catches."),
item(7,"James Baxter","W10-P15","A hound on soft shoulder, truck on raised strip, driver in cab establish opposed scales.",
"Design legible silhouettes from both POVs; maintain truck/tire/animal separation throughout.","ACCEPT","Readable silhouette communicates a blockade that is never an actual collision."),
item(8,"Frank Masi","W10-P19","Birthday reveal relies on distinct guest, host and wrapped prop in a coherent room.",
"Lock lens/eyelines and one spatial master before coverage; preserve subject scale and birthday light.","ADAPT","Shot continuity beats disconnected posed hero portraits."),
item(9,"John Knoll","W10-P24","Lightning moves from the surviving battery after the chair-side refusal and hand signal.",
"Maintain shot-linked VFX source versions, seeds, output hashes, masks, negative constraints and editable sound stems.","HOLD","A fully baked one-pass clip is not compositable source authority."),
item(10,"Jill Bogdanowicz","W10-P10","The Storm Coast terrace and Central Basin court occupy different exposures.",
"Create separate scoped color palettes anchored to regional conditions; keep readable faces.","ADAPT","One blanket storm LUT falsely merges geography."),
item(11,"Thelma Schoonmaker","W10-P13","Pause, hope, deliberate volume increase and resumed drilling form an ordered comic choice.",
"Reserve real silent screen time before the purposeful escalation, with reaction footage serving causality.","ACCEPT","A nonstop jackhammer montage would erase the joke."),
item(12,"Randy Thom","W10-P14","The household waterfall, courtyard machinery and speaker form layered acoustic sources.",
"Produce separate compressor, jackhammer, waterfall and music stems; withhold identifiable licensed song cues.","HOLD","Sound is a story mechanism requiring editability and clearance."),
item(13,"jrr_tolkien","W10-P11","The Commonwealth changes unevenly under one regional front.",
"Use ordinary infrastructure wear and continued roads to sell world history without a map-dump.","ADAPT","Inhabited world depth should be legible from material consequences."),
item(14,"cs_lewis","W10-P23","Refused protection for surrender creates a meaningful choice.",
"Allow silence and facial/body hesitation at the refusal, not merely a spectacle countdown.","ADAPT","Moral imagination is expressed through actual costs and temptation."),
item(15,"george_rr_martin","W10-P04","The league has six matchups and twelve distinct lives; results cannot erase the losers.",
"Cross-check each story's two subjects and distinct aftermath against the official board.","ACCEPT","Ensemble integrity and causal pressure prevent winner-only mythologizing."),
item(16,"jk_rowling","W10-P20","Opening a burger gift is separate from the later cake impact.",
"Protect three distinct beats: invitation, box reveal and delayed cake consequence.","ACCEPT","Setup and payoff work only if reveal and physical joke are temporally distinct."),
item(17,"john_grisham","W10-P27","Public sports-data folios must remain readable without stalling the movie.",
"Use economical graphic inserts and a clear spoken transition into the next dramatic scene.","ADAPT","Information should propel the story instead of becoming a spreadsheet slideshow."),
item(18,"ursula_k_le_guin","W10-P03","The civic address is an inhabited institution, not a commissioner portrait reveal.",
"Show restrained ordinary work and read exact supplied copy; preserve a separate institutional voice.","ACCEPT","Voice/culture emerge from labor and lived place."),
item(19,"brandon_sanderson","W10-P24","Lightning is a surviving battery consequence, not unmotivated magic.",
"Diagram the first disabled battery, remaining charge path, controlling gesture and field effects before VFX.","ACCEPT","Hard spatial mechanics create causality and readable costs."),
item(20,"joe_abercrombie","W10-P10","The bent rim and mud carry an intimate loss beyond team statistics.",
"Stay in the ruined court long enough to register fingers on the loose net and accumulated exhaustion.","ADAPT","Human-scale consequences prevent hollow grandeur.")
]
sha=hashlib.sha256(EVIDENCE.read_bytes()).hexdigest()
assignment={
 "assignment_id":"SCHEMIN-W10-FILM-INKLINGS-BENCH-20261122",
 "production":"memo-os","evidence_sha":sha,
 "decision_question":"How can all 34 source folios become a 30-minute film without changing source results, geography, character identity or release gates?",
 "review_mode":"SIMULATED_SINGLE_AUTHOR_METHOD_LENS_ANALYSIS_NOT_EXTERNAL_PARTICIPATION",
 "source":"memo-os/week-10/preproduction/render-inputs/manifest.json",
 "synthesis":"One 30-minute Commonwealth film preserves the source's six causal matchups, score provenance, varied world weather, emotional choices and physical blocking. Emphasize geography-first staging, long-form continuity, separate sound stems and editorial rhythm; no automatic canon promotion.",
 "findings":findings
}
(HERE/"METHOD_LENS_WORKSHOP_INPUT.json").write_text(json.dumps(assignment,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
spec=importlib.util.spec_from_file_location("inklings_workshop",COUNCIL/"inklings_workshop.py")
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
result=module.reconcile(assignment,json.loads(ADVISORS.read_text()),json.loads(BENCH.read_text()))
result["execution_note"]="Validation/reconciliation executed against repository code. Creative findings are modeled using documented published-method domains, NOT independently performed human consultant reviews, board votes or real agent consultations."
result["review_mode"]=assignment["review_mode"]
(HERE/"METHOD_LENS_RECONCILIATION.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
print(json.dumps({"result":result["status"],"advisor_count":len(result["selected_advisors"]),"findings":len(findings),"accepted":len(result["accepted"]),"dissent":len(result["dissent"]),"umpire":result["umpire"]},indent=2))
