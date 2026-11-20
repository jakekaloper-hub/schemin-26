#!/usr/bin/env node
/**
 * Evidence-bound screenplay production queue: exactly the 50 unfinished
 * 2015-2025 title-path fixtures. No arbitrary human owner assignments, no
 * extra matchups, no 2026 speculative competitors or results.
 */
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
const root=path.dirname(fileURLToPath(import.meta.url));
const read=n=>JSON.parse(fs.readFileSync(path.join(root,n),'utf8'));
const historical=read('HISTORICAL_POSTSEASON_ENCOUNTERS_2015_2025.founder_v2.json');
const draw=read('HISTORICAL_CEREMONIAL_DRAW_2015_2025.proposal.json');
const scar=read('ISLAND_PERMANENT_IMPACT_LEDGER_2015_2025.proposal.json');
const scripts=read('INKLINGS_SIX_SCREENPLAY_PILOT_LIBRARY_V1.json');
const known=new Set(scripts.scenes.map(x=>x.fixture_id));
const draws=new Map(draw.ceremonies.map(x=>[x.fixture_id,x]));
const scars=new Map(scar.traces.map(x=>[x.fixture_id,x]));
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
function significance(f){
 const margin=Math.abs(f.home.points-f.away.points);
 const flags=[];
 let priority=0;
 if(f.round==='FINAL'){priority+=35;flags.push('CHAMPIONSHIP_TITLE_PATH');}
 else if(f.round==='SF'){priority+=18;flags.push('FINAL_GATE_ON_THE_LINE');}
 else priority+=8;
 if(margin<=1){priority+=30;flags.push('ONE_POINT_OR_LESS_CERTIFICATION');}
 else if(margin<=5){priority+=18;flags.push('TIGHT_FIVE_POINT_CONTEST');}
 else if(margin<=10){priority+=8;flags.push('TEN_POINT_TENSION');}
 if(f.year===2015){priority+=10;flags.push('FOUNDING_YEAR');}
 if(f.year>=2023){priority+=3;flags.push('CONTEMPORARY_WORLD_STATE');}
 return {priority,flags,point_margin:Number(margin.toFixed(2))};
}
const backlog=historical.fixtures.filter(x=>!known.has(x.id)).map(f=>{
 const d=draws.get(f.id),trace=scars.get(f.id);
 assert.ok(d&&trace);
 const key=significance(f);
 const winner=f.home.team_slot===f.winner_slot?f.home:f.away;
 return {
  id:'INKLINGS-ASSIGN-'+f.id,fixture_id:f.id,year:f.year,round:f.round,
  scene_title_candidate:f.home.name+' × '+f.away.name+' — '+d.obstacle_name,
  source_locked:{
   fixture_id:f.id,league_id:'1417621',
   home:f.home,away:f.away,winner_slot:f.winner_slot,certified_winner_name:winner.name,
   scoring_period:f.scoring_period,
   fingerprint:sha(JSON.stringify({id:f.id,home:f.home,away:f.away,win:f.winner_slot,period:f.scoring_period}))
  },
  draw:{id:d.selected_obstacle_id,name:d.obstacle_name,category:d.obstacle_family,ticket:d.draw_ticket_sha256},
  venue:{candidate_id:f.staging.venue_id,round_fixed:true,physical_anchor:trace.original_material_anchor,permanent_scar:trace.trace_id},
  priority:key.priority,priority_factors:key.flags,verified_margin:key.point_margin,
  required_script:{
   words_target:[1200,2200],
   components:['actual round context','existing venue architecture and earlier material memory',
   'ceremonial drawn challenge with legible objective','three causally linked stages',
   'both named principal personas personally perform all stages',
   'at least one opponent countermove and one differentiated personal strategy per phase',
   'professional year-appropriate spectator account','source-certified final result',
   'safe but permanent physical trace / remediation / later World continuity',
   'shoreward elimination or championship postlude'],
   prohibitions:['human owner identity inferred from historic team slot',
   'fatal main POV injury','unapproved contemporary technology before arrival era',
   'fantasy score converted from fictional objective','unverified historical Michael Farrell naming',
   'active Atlas location write','invented 2026 postseason result']
  },
  workflow:{stage:'QUEUED_EDITORIAL',model_drafting_permitted:true,
   model_output_acceptance:'NEVER_AUTOMATIC_CANON',
   deterministic_source_gate:'scene_quality_gate.cjs',
   quality_followup:['Beat Writer creative editor','Architect physical/era check','Scout source provenance',
   'independent Umpire','character canon references'],
   publication:'HOLD'}
 };
});
backlog.sort((a,b)=>b.priority-a.priority||a.year-b.year||a.fixture_id.localeCompare(b.fixture_id));
assert.equal(backlog.length,50);
assert.equal(new Set(backlog.map(x=>x.fixture_id)).size,50);
assert.ok(backlog.every(x=>x.year<=2025));
const countsByYear={};for(const x of backlog)countsByYear[x.year]=(countsByYear[x.year]||0)+1;
const manifest={
schema:'schemin.postseason.inklings_remaining_story_production_queue.v1',
status:'FOUNDER_AUTHORIZED_50_UNFINISHED_FIXTURE_EDITORIAL_ASSIGNMENTS',
source:'HISTORICAL_POSTSEASON_ENCOUNTERS_2015_2025.founder_v2.json',
existing_audited_longform:scripts.scenes.map(x=>x.fixture_id),
census:{historical_fixtures:56,audited_screenplay_pilots:6,remaining_unwritten_pilots:50,by_year:countsByYear},
method:'Prioritize championship title stakes, exceptional verified margins, founding history, and year diversity. Priority does not affect source result, obstacle draw, or bracket.',
next_five:backlog.slice(0,5).map(x=>({fixture_id:x.fixture_id,year:x.year,round:x.round,draw:x.draw.name,priority:x.priority})),
queue:backlog
};
const target=path.join(root,'INKLINGS_50_REMAINING_SCREENPLAY_PRODUCTION_QUEUE_V1.json'),serial=JSON.stringify(manifest,null,2)+'\n';
if(process.argv.includes('--check'))assert.equal(fs.readFileSync(target,'utf8'),serial);
else fs.writeFileSync(target,serial);
console.log(JSON.stringify({status:'PASS',...manifest.census,next_five:manifest.next_five,editorial_backlog_source:'REAL_2015_2025_MATCHUPS_NO_2026'}));
