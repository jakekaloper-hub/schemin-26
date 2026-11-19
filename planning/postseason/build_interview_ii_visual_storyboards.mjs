#!/usr/bin/env node
/** Interview II visual storyboard preproduction compiler.
 * Storyboards are text-camera shot contracts, not actual rendered photos/video.
 */
import fs from 'node:fs';import path from 'node:path';import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
const root=path.dirname(fileURLToPath(import.meta.url));
const read=n=>JSON.parse(fs.readFileSync(path.join(root,n),'utf8'));
const scenes=read('INKLINGS_INTERVIEW_II_56_MATCH_SCENE_CONTRACTS.proposal.json');
const impacts=read('ISLAND_PERMANENT_IMPACT_LEDGER_2015_2025.proposal.json');
const effects=read('INKLINGS_OWNER_BODY_CONSEQUENCE_2015_2025.proposal.json');
const broadcast=read('CHAMPIONSHIP_ISLAND_BROADCAST_HERITAGE_2015_2026.proposal.json');
const byId=(a,k)=>new Map(a.map(x=>[x[k],x]));
const impactBy=byId(impacts.traces,'fixture_id'),effectsBy=byId(effects.games,'fixture_id');
const mediaBy=byId(broadcast.years,'year');
const cards=[];
for(const scene of scenes.cards){
 const impact=impactBy.get(scene.fixture_id),effect=effectsBy.get(scene.fixture_id),media=mediaBy.get(scene.year);
 if(!impact||!effect||!media)throw Error('Storyboards missing source '+scene.fixture_id);
 const shot=(n,beat,lens,visual,performers,truth='FICTIONAL_PREPRODUCTION')=>({
   shot_id:'SHOT-'+scene.fixture_id+'-'+String(n).padStart(2,'0'),
   sequence:n,beat,lens,visual,performers,
   witness_status:truth,location_id:scene.venue_id,year:scene.year,
   referenced_scars:[impact.trace_id],
   rendering_status:'BLOCKED_NO_HISTORICAL_CHARACTER_REFERENCE_AND_ACTIVE_ATLAS',
   needs_independent_visual_qa:true
 });
 const a=scene.verified_sports.home,b=scene.verified_sports.away;
 const list=[
  shot(1,'venue_establishing','wide_grounded_environment',
   'Establish '+scene.venue_id+' in '+scene.year+'; show the already accumulated arena wear and era-correct facilities. Preserve original gates and stonework.',[], 'UNPROMOTED_ATLAS_ART_DIRECTION'),
  shot(2,'public_ceremonial_draw','official_table_close',
   'Show a stage-safe ceremonial selection of '+scene.draw.name+' on a public information board, with its reproducible ticket hash archived; no source result displayed until the end.',[], 'FOUNDER_II_INVENTED_HISTORIC_RITUAL'),
 ];
 for(const stage of scene.acts){
  list.push(shot(2*stage.number+1,'act_'+stage.number+'_contender_A','character_grounded_medium',
    a.name+' personally performs: '+stage.solo_contender_A.action+'. Background: '+stage.objective,[{slot:a.team_slot,label:a.name,direct_personal_performance:true}]));
  list.push(shot(2*stage.number+2,'act_'+stage.number+'_contender_B','character_grounded_medium',
    b.name+' personally counters: '+stage.solo_contender_B.action+'. The same neutral arena and stage objective must remain unchanged.',[{slot:b.team_slot,label:b.name,direct_personal_performance:true}]));
 }
 list.push(shot(9,'source_certified_result','arena_public_results_wide',
    'Show winner only after the season-specific verified result lock; visual overlay: '+scene.commentary.official_call,[{slot:scene.verified_sports.winner_slot,label:'verified_survivor'}], 'ESPN_RESULT_PLUS_FICTIONAL_STAGING'));
 list.push(shot(10,'lasting_impact_close','macro_location_material',
    'Show the mark at '+impact.original_material_anchor+': '+impact.impact.material_consequence+'. Document it before repair. Do not destroy the historical permanent Last Field foundation.',[]));
 list.push(shot(11,'contender_departure','follow_long_lens',
    'The eliminated physical competitor personally leaves the protected contender quarter. Losers Beach is a single modest resort, shown as reflective rather than an entirely new battle complex.',[]));
 list.push(shot(12,'central_tournament_broadcast','broadcast_desk_and_crowd',
    'An objective announcer confirms the exact score and which remaining contest survives. Era rule: '+media.coverage_heritage_proposal,[], 'PROPOSED_ERA_TECH_DEPENDENT'));
 assert.equal(list.length,12);
 assert.ok(list.every(x=>x.rendering_status.startsWith('BLOCKED')));
 cards.push({fixture_id:scene.fixture_id,year:scene.year,round:scene.round,
   scene_performer_status:'ONLY_THE_TWO_FRANCHISE_PERSONAS_NOT_UNVERIFIED_REAL_OWNER_MAPPING',
   story_beats:scene.acts.map(x=>x.label),
   production_cameras:list,
   broadcast_era:media.era_status,
   protected_heritage:impact.trace_id,
   injury_references:effect.team_slot_health_fiction.map(x=>({slot:x.team_slot,effect:x.in_contest_personal_effect,fiction_only:true})),
   source_result:scene.verified_sports,
   cut_release:'PREVIS_ONLY_NOT_RENDERED'};
}
assert.equal(cards.length,56);
const obj={schema:'schemin.postseason.interview_ii_visual_storyboards.v1',status:'CAMERA_AND_VISUAL_PREPRODUCTION_NOT_ACTUAL_RENDER',
 source:'INKLINGS_INTERVIEW_II_56_MATCH_SCENE_CONTRACTS.proposal.json',
 counts:{fixtures:56,shot_contracts:cards.reduce((n,x)=>n+x.production_cameras.length,0)},
 no_character_identity_backfill:true,no_2026_winner:true,
 cameras_source:'Narrative/venue/geography sources, no actual footage',
 cards};
const out=path.join(root,'INKLINGS_INTERVIEW_II_VISUAL_STORYBOARDS_56.proposal.json'),serial=JSON.stringify(obj,null,2)+'\n';
if(process.argv.includes('--check'))assert.equal(fs.readFileSync(out,'utf8'),serial);
else fs.writeFileSync(out,serial);
console.log(JSON.stringify({status:'PASS',...obj.counts,no_unverified_real_owner_images:true,actual_renders:0}));
