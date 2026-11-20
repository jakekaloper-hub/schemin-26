#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
import {evaluatePhysicalFit,VENUES,candidateCompatibility} from './arena_physical_affordances.mjs';
const dir=path.dirname(fileURLToPath(import.meta.url));
const read=name=>JSON.parse(fs.readFileSync(path.join(dir,name),'utf8'));
const lexicon=read('OBSTACLE_LEXICON_120_V1.json');
const history=read('HISTORICAL_POSTSEASON_ENCOUNTERS_2015_2025.founder_v2.json');
const original=read('INKLINGS_2015_2025_COMPILED_PRODUCTION_CARDS.proposal.json');
const previous=new Map(original.cards.map(c=>[c.verified_fixture_id,c]));
assert.equal(lexicon.obstacles.length,120);
const preferences={
'FORM-DUEL':['combat','endurance','hybrid','sports'],
'FORM-PURSUIT':['racing','traverse','endurance','tactical'],
'FORM-ENDURANCE':['endurance','traverse','hybrid','combat'],
'FORM-TACTICAL':['tactical','board','puzzles','engineering'],
'FORM-SPORT':['sports','marksmanship','hybrid','endurance'],
'FORM-WATER':['aquatic','engineering','traverse','racing'],
'FORM-ENGINEERING':['engineering','tactical','puzzles','board'],
'FORM-NEGOTIATION':['board','puzzles','hybrid','tactical']
};
const used=new Set();
function choose(fixture,blocked=new Set()){
 const rank=preferences[fixture.staging.encounter_form];
 if(!rank)throw Error('Unsupported source editorial form '+fixture.staging.encounter_form);
 const valid=lexicon.obstacles.filter(o=>
   !blocked.has(o.id) && evaluatePhysicalFit({obstacle:o,venue_id:fixture.staging.venue_id,round:fixture.round,year:fixture.year}).eligible);
 valid.sort((a,b)=>{
  const ra=rank.indexOf(a.family),rb=rank.indexOf(b.family);
  const rankA=ra===-1?999:ra,rankB=rb===-1?999:rb;
  if(rankA!==rankB)return rankA-rankB;
  const diversity=(a.family===b.family?0:1);
  return a.id.localeCompare(b.id);
 });
 return valid[0]||null;
}
const proposals=history.fixtures.map(f=>{
 const preferred=choose(f,used);
 if(!preferred)throw Error('No unique historically compatible obstacle for '+f.id);
 used.add(preferred.id);
 const alternatives=[preferred.id],temp=new Set([preferred.id]);
 for(let i=0;i<2;i++){const alt=choose(f,temp);if(!alt)break;alternatives.push(alt.id);temp.add(alt.id);}
 const prior=previous.get(f.id);
 if(!prior)throw Error('Missing historical original signature '+f.id);
 const fit=evaluatePhysicalFit({obstacle:preferred,venue_id:f.staging.venue_id,round:f.round,year:f.year});
 return {
  fixture_id:f.id,year:f.year,round:f.round,venue_candidate_id:f.staging.venue_id,
  historical_source:{home:f.home,away:f.away,winner_slot:f.winner_slot,matchup_period:f.scoring_period},
  editorial_input_form:f.staging.encounter_form,
  picked_obstacle_id:preferred.id,scenario:preferred.name,family:preferred.family,
  alternate_obstacles:alternatives.slice(1),title_venue_binding_status:'FROZEN_SOURCE_SCORES_PROPOSED_CONTEST',
  three_stages:preferred.three_phase.map((s,i)=>({
   ...s,performer_brief:'Both named contenders must exert agency in stage '+(i+1)+'.',
   original_signature_beat:i===1?prior.storyroom.signature_action:null,
   actual_winner_not_physically_inferred:f.winner_slot,
   action_status:'PROPOSED_FICTION'
  })),
  spectator_cutaway:prior.storyroom.spectator_cutaway,
  physical_contract:fit,
  legacy_proposal:prior.storyroom.heritage_consequence,
  site_scar_application:'NOT_AUTOMATIC_WORLD_STATE_WRITE',
  source_notation:'ESPN/Flaim score truth; obstacle/stages NEW FICTION',
  release:'HOLD_CHARACTER_ATLAS_UMPIRE'
 };
});
assert.equal(proposals.length,56);
assert.equal(new Set(proposals.map(x=>x.picked_obstacle_id)).size,56);
assert.ok(proposals.every(p=>p.physical_contract.eligible&&p.three_stages.length===3));
const compatibility=candidateCompatibility(lexicon,2026);
const output={
 schema:'schemin.postseason.obstacle_options_for_history.v1',
 status:'CREATIVE_OPTION_SET_NOT_HISTORIC_ACTUAL_TRIALS',
 sources:['HISTORICAL_POSTSEASON_ENCOUNTERS_2015_2025.founder_v2.json','INKLINGS_2015_2025_COMPILED_PRODUCTION_CARDS.proposal.json','OBSTACLE_LEXICON_120_V1.json'],
 count:{fixtures:proposals.length,unique_selected_obstacles:56,curated_seeds:120,venue_scenario_combinations_2026:compatibility.total_valid_site_scenario_pairs},
 compatibility,
 notes:['No winner changes','Three phases per obstacle are original scenewriting, not proven physical history','Historic site selection follows Founder fixed-round design','Do not publish any 2026 entrant/winner from this registry','Proposed memory scars require a separately governed world-state event'],
 proposals
};
const filename=path.join(dir,'HISTORICAL_CHALLENGE_OPTION_BINDINGS_56_V1.json');
const result=JSON.stringify(output,null,2)+'\n';
if(process.argv.includes('--check'))assert.equal(fs.readFileSync(filename,'utf8'),result);
else fs.writeFileSync(filename,result);
console.log(JSON.stringify({status:'PASS',mode:process.argv.includes('--check')?'CHECK':'BUILD',count:output.count,selected_families:[...new Set(proposals.map(x=>x.family))],blocked:proposals.filter(x=>!x.physical_contract.eligible).length}));
