#!/usr/bin/env python3
"""Human-readable counterweight triage of 20 genuine LOCAL MODEL responses, not 20 human consultations."""
from pathlib import Path
import json, collections
HERE=Path(__file__).resolve().parent
source=json.loads((HERE/"LOCAL_MODEL_20_LENS_INPUT.json").read_text())
q={f["advisor"]:f for f in source["findings"]}
actions={
"Doug Chiang":("HOLD","Source contract already distinguishes first disabled battery. Actual red-energy deflection and throne look need a rendered set test.","P22/P24 VFX causal diagram and two battery identifiers before approval."),
"Dylan Cole":("REJECT","Model incorrectly says mountain lake is unsourced. P11 source venue LOC-BRIDGE-MOUNTAIN-LAKE and Upper Basin Connector already allow mountain-lake description.","Retain source geography; prohibit a newly invented separate location."),
"Joe Letteri":("HOLD","Model voted ACCEPT but no actual three-head rig or character pixels were inspected.","One body with exactly three heads, one frame-by-frame continuity receipt."),
"Ngila Dickson":("ACCEPT","Wet costume/mud from Storm Coast to later court is a valid existing source constraint.","Attach Red's canonical appearance and verify mud progression across P08–P10."),
"Andy Serkis":("ADAPT","Wounded pride supported by DK reaction, but invented psychological motives should not be canonized.","Use an averted gaze or tension in actor candidate, no new official quote or injury."),
"Rob Alonzo":("HOLD","Torso catch and slipping boot are required; schematic rope reel cannot certify physical body mechanics or manual tie.","Rig and three-shot motion test: no neck, rope continuity, skid before manual knot."),
"James Baxter":("ACCEPT","Truck/hound geometry and raised road separation are source-locked already.","Maintain both silhouettes and visible distance in P15–P17."),
"Frank Masi":("ADAPT","Warm birthday room and consistent guest-host eyeline are sound camera suggestions, but no shot pixels exist.","Master lens/eyeline placement and light references before P19 render."),
"John Knoll":("HOLD","A VFX simulation and edit-ready passes for the surviving battery do not exist.","Previs first disabled battery then charged second and finger-to-lightning path."),
"Jill Bogdanowicz":("ADAPT","Specific left/right hoop impact and temporal later-court logic is source-supported.","Keep right-wall backboard, later inland light and branch trajectory consistent."),
"Thelma Schoonmaker":("REJECT","Model suggests an extra exaggerated gesture; new comic business risks overriding the exact approved speaker-volume choice.","Keep original pause / hopeful glance / existing speaker turn; test genuine silence."),
"Randy Thom":("HOLD","Five local M01 audio buses now exist; the source P13–P14 temple scene does not yet have validated separate stems or soundtrack clearance.","Produce independent waterfall, speaker, compressor and drill layers before mixing P13–P14."),
"jrr_tolkien":("REJECT","Model misidentified mountain lake as a new invention. The documented setting already includes LOC-BRIDGE-MOUNTAIN-LAKE.","Retain established connector and regional timing, no invented route."),
"cs_lewis":("REJECT","A proposed golden retriever reward is unsupported by P23 source and contradicts the no-new-canon constraint.","Keep existing blade/arch bargain and refusal; add no reward or dog."),
"george_rr_martin":("ACCEPT","Source already requires all six results and twelve teams represented by accurate board.","Use film graphics source extract for official figures, do not invent missing outcomes."),
"jk_rowling":("ACCEPT","200-point significance already appears in P01; visual callback to 200 Burger in P20 can be achieved without new dialogue.","Motif: P01 exact scores → P20 box / burger reveal → P21 separate cake."),
"john_grisham":("ADAPT","Data pages risk crowding. Model's advice to structure official type is sound when not changing values.","Use native graphic payload plus restrained editorial hierarchy; audience read-time QA pending."),
"ursula_k_le_guin":("ACCEPT","Civic voice benefits from material consequences and the original published source already names broken hoop and delivery road.","Preserve anonymous labor at records desk and source P03 emotion."),
"brandon_sanderson":("HOLD","Model correctly flags untested VFX, battery relation and arch lamp.","Do not release P22–P24 lightning until energy geometry and exposure are checked."),
"joe_abercrombie":("REJECT","Model suggests cracked basketball not in canon. Red's bent rim and loose net are existing grounded props.","Use source broken hoop, carried mud and fingers on loose net; no new ball.")
}
assert len(actions)==len(q)==20
rows=[]; ledger=[]
for advisor,(status,reason,action) in actions.items():
    finding=q[advisor]
    ledger.append({"lens":advisor,"actual_model_decision":finding["decision"],"editorial_verdict":status,
        "reason":reason,"next_test_or_implementation":action,"source_anchor":finding["source_anchor"],
        "status":"SOURCE-GROUNDED_DESK_TRIAGE_NOT_FINAL_DIRECTOR_APPROVAL"})
    rows.append("| "+advisor+" | "+finding["decision"]+" | **"+status+"** | "+reason.replace("|","/")+" | "+action.replace("|","/")+" |")
counts=dict(collections.Counter(x["editorial_verdict"] for x in ledger))
packet={
 "schema":"schemin.week10.model_review_triage.v1","date":"2026-11-22",
 "method":"Actual local Qwen3-8B independent per-discipline model responses → source-backed assistant editorial triage",
 "real_person_participation":False,"bullpen_director_execution":"Core router was run; no independent director model workers or authenticated Umpire signoff claimed",
 "umpire":"PENDING","status":"CANDIDATE_WITH_HELD_PRODUCTION_GATES",
 "counts":counts,"record":ledger}
(HERE/"SCREENPLAY_REVIEW_DECISIONS.json").write_text(json.dumps(packet,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
markdown=[
 "# Week 10 film — actual twenty-model-pass review and editorial counterweights",
 "",
 "This ledger documents twenty **actual local Qwen3-8B inference runs**, each independently prompted with a frozen scene and a registered craft discipline. It does **not** claim contact with the named authors, artists or real Bullpen directors.",
 "",
 "**Status:** source-grounded triage only. Editorial verdicts are not individual real-person signatures, release permissions or rendered-pixel QA.",
 "",
 "The red-team rejected several hallucinated proposals. Most notably, a model proposed adding a *golden retriever* to the field-throne bargain; another mistakenly treated the already-established Mountain Lake bridge as a new place; another invented a cracked basketball prop. None has been added to the screenplay or source canon.",
 "",
 "## Individual review results",
 "",
 "| Published-method lens | Model output | Editorial decision | Rationale | Action / test |",
 "|---|---|---|---|---|",
 *rows,
 "",
 "## Verified production changes after review",
 "",
 "- **Rodeo geography corrected:** the rear-left service gate appears to screen left and Chili's path now runs toward it; rope endpoint remains at torso height, not neck; still purely schematic, not fully rigged.",
 "- **Film facts retained:** P18 combination totals correctly distinguish HMB's 113.86 and LLC's 103.66; all full source publication copy, including row/callout data, is retained in the screenplay JSON.",
 "- **Sound separation implemented for M01:** isolated DX, VO, FX, AMB and MX WAV stems at 48kHz/24-bit, mixed 42-second rehearsal MP4; **temple** layer isolation remains pending.",
 "- **Official scoreboard and roster graphics isolated:** the native typography contract is drawn from source packet copy and exact SHA-256, not synthesized by an image/video model.",
 "",
 "## Still held",
 "",
 "True character likeness/rigging, binding mechanics, cinematic compositing/lighting, temple acoustic design, performance casting/ADR, source/reference rights, full 30-minute animated footage, independent Umpire and Founder publication approval.",
 "",
 "The Closer must not equate twenty model responses with twenty approved production gates."
]
(HERE/"SCREENPLAY_REVIEW_DECISIONS.md").write_text("\n".join(markdown)+"\n",encoding="utf-8")
print(json.dumps(counts,indent=2))
