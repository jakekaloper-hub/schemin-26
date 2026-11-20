#!/usr/bin/env node
/** Fiction-only body-state continuity across the 56 historical island trials.
 * Stage pain / fatigue are fictional and never prove an injury to a real league member.
 * Propagates each advancing fictional team-slot persona's burden to its next contest.
 */
import fs from 'node:fs';import path from 'node:path';import assert from 'node:assert/strict';
import crypto from 'node:crypto';import {fileURLToPath} from 'node:url';
const root=path.dirname(fileURLToPath(import.meta.url)),read=n=>JSON.parse(fs.readFileSync(path.join(root,n),'utf8'));
const history=read('HISTORICAL_POSTSEASON_ENCOUNTERS_2015_2025.founder_v2.json'),scenes=read('INKLINGS_INTERVIEW_II_56_MATCH_SCENE_CONTRACTS.proposal.json');
const options=read('HISTORICAL_CEREMONIAL_DRAW_2015_2025.proposal.json');
const resultMap=new Map(history.fixtures.map(x=>[x.id,x])),drawMap=new Map(options.ceremonies.map(x=>[x.fixture_id,x]));
const effects={
combat:['bruised shoulder','tender ribs','stiff wrist','scraped knee','shaken grip'],
marksmanship:['raw drawing fingers','forearm strain','trembling shoulder','strained aim','fatigued back'],
racing:['sore hands from steering','strained forearm','impact bruising within protective equipment','tired legs','jolted lower back'],
sports:['bruised forearm','strained calf','sore ankle','aching shoulder','scraped shin'],
tactical:['contusion from controlled grappling','minor shield impact bruise','tired shoulder','scraped hand','sore knee'],
board:['tensed shoulders','fatigued focus','shaking hands under stakes','dry throat from long concentration','aching forearms'],
engineering:['abraded palms','sore back from lifting','strained forearm','fatigued hands','scraped knuckles'],
traverse:['scraped palms','sore forearms','harness abrasion','fatigued calves','tender shins'],
aquatic:['cold-stiffened fingers','fatigued arms','sore shoulder','wet-foot abrasions','tired back'],
endurance:['exhausted legs','bruised lifting grip','strained shoulders','deep muscle soreness','fatigued balance'],
puzzles:['trembling hands under pressure','stiff fingers','mental exhaustion','sore hands from mechanisms','tight jaw'],
hybrid:['strained wrist','fatigued thighs','controlled impact bruise','scraped palm','strained forearm']
};
function hashInt(s){return Number(BigInt('0x'+crypto.createHash('sha256').update(s).digest('hex'))%BigInt(1_000_003));}
const order={QF:0,SF:1,FINAL:2};
const sorted=history.fixtures.slice().sort((a,b)=>a.year-b.year||order[a.round]-order[b.round]||a.id.localeCompare(b.id));
const seasons=new Map();
const gameRecords=[];
const nameFor=(x,id)=>x.home.team_slot===id?x.home.name:x.away.name;
for(const fixture of sorted){
 const year=fixture.year,fid=fixture.id,draw=drawMap.get(fid);
 if(!draw)throw Error('Missing draw '+fid);
 const group=effects[draw.obstacle_family];if(!group)throw Error('Unknown risk for '+fid);
 const previous=seasons.get(year)||new Map();
 seasons.set(year,previous);
 const winner=fixture.winner_slot,loser=fixture.home.team_slot===winner?fixture.away.team_slot:fixture.home.team_slot;
 const participants=[fixture.home.team_slot,fixture.away.team_slot];
 const statuses=participants.map(id=>{
   const prior=previous.get(id)||{accumulated_strain:[],rounds_survived:0};
   const phrase=group[hashInt(fid+'|'+id)%group.length];
   const intensity=['LOW','MODERATE','HIGH'][hashInt(fid+'|intensity|'+id)%3];
   const cumulative=prior.accumulated_strain.length;
   const recoveredPrior=prior.accumulated_strain.slice(-2);
   const won=id===winner;
   return {team_slot:id,franchise_name:nameFor(fixture,id),prior_burden:recoveredPrior,
     in_contest_personal_effect:phrase,injury_classification:'IN_WORLD_FICTIONAL_MINOR_RECOVERABLE',
     intensity,post_round_condition:won?'ADVANCES_WITH_TREATMENT_AND_FATIGUE':'ELIMINATED_MEDICAL_CLEARANCE_THEN_BEACH',
     dramatic_effect:won?'The survivor must personally manage the accumulated strain at the next tournament stage, if one remains.':'The defeated competitor receives event medical attention and retires to the beach after certification.',
     care:['exam by licensed in-world medical staff','rest and protective recovery','no unapproved permanent disability'],
     cumulative_prior_effects:cumulative,
     source:'INVENTED_CHARACTER_FICTION__NOT_REAL_PERSON_HEALTH_DATA',
     final_competition_winner:won};
 });
 for(const s of statuses)if(s.final_competition_winner){
   const prior=previous.get(s.team_slot)||{accumulated_strain:[],rounds_survived:0};
   previous.set(s.team_slot,{accumulated_strain:[...prior.accumulated_strain,s.in_contest_personal_effect],rounds_survived:prior.rounds_survived+1});
 }
 const scene=scenes.cards.find(x=>x.fixture_id===fid);
 if(!scene||scene.acts.length!==3)throw Error('Missing three stage script '+fid);
 gameRecords.push({fixture_id:fid,year,round:fixture.round,combat_stakes:'GLADIATORIAL_HIGH_CONSEQUENCE_NONLETHAL',team_slot_health_fiction:statuses,
    verified_winner_slot:winner,historical_source_ref:fid,physical_terrain_trace_ref:'TRACE-'+fid,
    injury_canon_status:'IN_WORLD_CANDIDATE_NOT_REAL_WORLD_MEDICAL_ASSERTION',spectator_status:'NO_SPECTATOR_INJURY_PERMITTED',
    continued_contender_eligibility_requires:'ESPN_ADVANCEMENT_ONLY'});
}
const annual=Array.from({length:11},(_,i)=>2015+i).map(year=>{
const games=gameRecords.filter(x=>x.year===year);
return {year,fixture_ids:games.map(x=>x.fixture_id),surviving_champion_slot:history.annual.find(x=>x.year===year).champion_slot,
  individual_personal_performances:games.reduce((a,g)=>a+g.team_slot_health_fiction.length,0),
  recorded_fictional_body_effects:games.flatMap(g=>g.team_slot_health_fiction).length,
  no_real_person_medical_inference:true};
});
if(gameRecords.length!==56||annual.reduce((a,x)=>a+x.individual_personal_performances,0)!==112)throw Error('Historical effect record count');
const out={schema:'schemin.postseason.owner_stage_body_continuity.proposal.v1',status:'FICTIONAL_CONTENDER_PERSONA_EFFECTS_NOT_REAL_OWNER_MEDICAL_HISTORY',
 source:'HISTORICAL_POSTSEASON_ENCOUNTERS_2015_2025.founder_v2.json',founder_directives:['F14','F17','F18'],
 counts:{fixtures:56,fictional_participant_effects:112,seasons:11},annual,games:gameRecords,
 limits:['No principal-character permanent death','No spectator injury spectacle','No unsupported real human medical claim','Never change source scores or fixture participants','No injury-generated victory or bracket intervention']};
const text=JSON.stringify(out,null,2)+'\n',target=path.join(root,'INKLINGS_OWNER_BODY_CONSEQUENCE_2015_2025.proposal.json');
if(process.argv.includes('--check'))assert.equal(fs.readFileSync(target,'utf8'),text);
else fs.writeFileSync(target,text);
console.log(JSON.stringify({status:'PASS',...out.counts,source_identity:'TEAM_SLOT_ONLY',character_safety:'RECOVERABLE_FICTION'}));
