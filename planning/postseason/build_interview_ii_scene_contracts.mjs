#!/usr/bin/env node
/** Interview II original fictional script pack; immutable sports facts. */
import fs from 'node:fs';import path from 'node:path';import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
const root=path.dirname(fileURLToPath(import.meta.url));
const read=n=>JSON.parse(fs.readFileSync(path.join(root,n),'utf8'));
const h=read('HISTORICAL_POSTSEASON_ENCOUNTERS_2015_2025.founder_v2.json');
const draw=read('HISTORICAL_CEREMONIAL_DRAW_2015_2025.proposal.json');
const impacts=read('ISLAND_PERMANENT_IMPACT_LEDGER_2015_2025.proposal.json');
const signatures=read('INKLINGS_56_SIGNATURE_ENCOUNTER_INTERVENTIONS_V1.json');
const lib=read('OBSTACLE_LEXICON_120_V1.json');
const lookup=(a,k)=>new Map(a.map(x=>[x[k],x]));
const dm=lookup(draw.ceremonies,'fixture_id'),im=lookup(impacts.traces,'fixture_id'),sm=lookup(signatures.items,'fixture_id'),om=lookup(lib.obstacles,'id');
const tactics={
combat:['establish legal striking distance','counter a change in grip and balance','personally execute the decisive rule-bound hold'],
marksmanship:['inspect target and take the opening aim','change range and wind reading while the rival responds','fire or throw the last protected, scored attempt'],
racing:['start the approved course personally','choose and defend the decisive racing line','cross the final checkpoint through direct steering or personal effort'],
sports:['perform the first scoring attempt','answer the rival formation and tempo','attempt the last legal scored play'],
tactical:['establish a contested field marker','respond by physically shifting the defended line','personally seize or yield the last standard'],
board:['make the opening wager or move','counter the visible strategic trap with their own judgment','make the personally chosen final legal move'],
engineering:['assemble the first neutral testing component','physically adjust their mechanism under counterpressure','set the last structural pin before official inspection'],
traverse:['enter their own protected climbing lane','adapt grip and route as their opponent gains ground','touch the final certified marker under safety ropes'],
aquatic:['enter the protected course themselves','change their own craft or swimming line while watched','secure the final legal buoy or dock marker'],
endurance:['move the first equal weight or run the first course','choose personally how to recover and counter fatigue','perform the final measured effort'],
puzzles:['inspect sealed neutral clues and begin unlocking','reject an early hypothesis and manipulate the second mechanism','personally open the final rule-governed lock'],
hybrid:['undertake the first event themselves','switch disciplines without appointing a substitute','physically complete the combined final trial']
};
const shots={
QF:['arena wide and public crowd','two opposed entry gates','close counters from both competitor POVs','certified objective finish','shoreward departure'],
SF:['privately guarded contender exit','monumental semifinal geometry','three-stage personal countermove','bracket-wide control-room intercut','loser joins beach'],
FINAL:['unchanged ancient Last Field gateways','distinct solo contender POVs','championship historic succession cutaway','final challenge under official lock','Belt and protected memorial trophy ceremony']
};
const cards=h.fixtures.map(f=>{
 const ticket=dm.get(f.id),scar=im.get(f.id),signature=sm.get(f.id);
 if(!ticket||!scar||!signature)throw Error('Unbound fixture '+f.id);
 const obstacle=om.get(ticket.selected_obstacle_id);if(!obstacle)throw Error('Drawn obstacle unavailable '+f.id);
 const a=f.home,b=f.away,winner=a.team_slot===f.winner_slot?a:b,loser=a.team_slot===f.winner_slot?b:a;
 const acts=obstacle.three_phase.map((stage,i)=>({
  number:i+1,label:stage.beat,objective:stage.objective,
  solo_contender_A:{team_slot:a.team_slot,public_character_name:a.name,action:tactics[obstacle.family][i],personally_competes:true},
  solo_contender_B:{team_slot:b.team_slot,public_character_name:b.name,action:'independently counters and attempts to '+tactics[obstacle.family][i],personally_competes:true},
  scene_text:(i===0?'The gates open on ':i===1?'At the turning point inside ':'At the decisive passage of ')+f.staging.venue_name+
   '. '+a.name+' and '+b.name+' personally face '+obstacle.name+'. '+stage.objective+
   ' '+(i===1?signature.signature_action:stage.unique_action)+
   ' Both sides must act on their own; no roster or entourage takes the stage for either.'+
   ' The physical consequence accumulates at '+scar.original_material_anchor+'.',
  provenance:'ORIGINAL_INKLINGS_FICTION_NOT_ESPN_FACT'
 }));
 return {fixture_id:f.id,year:f.year,round:f.round,venue_id:f.staging.venue_id,
 verified_sports:{home:a,away:b,winner_slot:f.winner_slot,scoring_period:f.scoring_period,source:'ESPN_FLAIM_HISTORICAL'},
 draw:{id:ticket.selected_obstacle_id,name:obstacle.name,family:obstacle.family,ticket_hash:ticket.draw_ticket_sha256,method:'PREDECLARED_NON_OUTCOME_DRAW'},
 opening:'Two season-specific historical franchise personas enter from opposite arena gates. The public draw has called '+obstacle.name+
 '. '+(f.year<=2016?'Founding stone and small stands':f.year<=2020?'Growing six-contender stadium and herald desks':'Modern sporting facility grafted onto preserved historic stone')+
 ' frame the scene. An impartial judge explains the objective before the first contact.',
 acts,commentary:{pre_game:'Explain rules and physically identify both solo challengers.',spectator_cutaway:signature.spectator_cutaway,
 official_call:winner.name+' defeats '+loser.name+' '+winner.points.toFixed(2)+'–'+loser.points.toFixed(2)+'. The result comes from ESPN records, not this fictional obstacle.',
 post_game:'The survivor advances; the eliminated contender walks personally toward the seasonally open beach resort.',
 camera_plan:shots[f.round],release:'WORLD_TECH_AND_YEAR_SPECIFIC_HOLD'},
 physical_history:{trace_id:scar.trace_id,damaged_anchor:scar.original_material_anchor,trace_kind:scar.trace_kind,restoration:scar.year_after.literal_retained_element,
 permanent_memory:true,world_state_writeback:false},
 emotional_turn:signature.legacy_note,
 character_canon:'HISTORIC_TEAM_SLOT_PERSONA; SPECIFIC REAL OWNER NOT ASSUMED',
 independent_umpire:'NOT_SIGNED',art_status:'NOT_RENDERED'
 };
});
assert.equal(cards.length,56);
assert.ok(cards.every(c=>c.acts.length===3&&c.acts.every(a=>a.solo_contender_A.personally_competes&&a.solo_contender_B.personally_competes)));
const out={schema:'schemin.postseason.inklings_interview_ii_scene_contracts.v1',status:'FICTIONAL_SCENE_TREATMENT_NOT_PUBLICATION',
 source:'FOUNDER_INTERVIEW_II_DECISION_REGISTER_2026_11_19.md',counts:{matches:56,phases:168,permanent_traces:56},
 version:'V2',cards};
const dest=path.join(root,'INKLINGS_INTERVIEW_II_56_MATCH_SCENE_CONTRACTS.proposal.json'),text=JSON.stringify(out,null,2)+'\n';
if(process.argv.includes('--check'))assert.equal(fs.readFileSync(dest,'utf8'),text);
else fs.writeFileSync(dest,text);
console.log(JSON.stringify({status:'PASS',...out.counts,solo_character_stages:true,world_mutations:0}));
