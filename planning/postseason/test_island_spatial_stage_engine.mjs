#!/usr/bin/env node
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {VENUES,evaluatePhysicalFit} from './arena_physical_affordances.mjs';
import {route,validateStageContest} from './build_island_spatial_stage_engine.mjs';
const dir=path.dirname(fileURLToPath(import.meta.url)),read=n=>JSON.parse(fs.readFileSync(path.join(dir,n),'utf8'));
const spatial=read('ISLAND_SPATIAL_STAGE_ENGINE_V1.proposal.json');
const history=read('HISTORICAL_POSTSEASON_ENCOUNTERS_2015_2025.founder_v2.json');
const obstacle=read('OBSTACLE_LEXICON_120_V1.json');
const scenes=read('INKLINGS_INTERVIEW_II_56_MATCH_SCENE_CONTRACTS.proposal.json');
const checks=[];function t(label,callback){callback();checks.push(label);}
const ids=new Map(obstacle.obstacles.map(x=>[x.id,x]));
const draw=read('HISTORICAL_CEREMONIAL_DRAW_2015_2025.proposal.json');
const dmap=new Map(draw.ceremonies.map(x=>[x.fixture_id,x]));
t('23 conceptual positions are complete without invented Atlas coordinates',()=>{
 assert.equal(spatial.diagrams.length,23);
 assert.equal(new Set(spatial.diagrams.map(x=>x.id)).size,23);
 assert.ok(spatial.diagrams.every(x=>x.coordinates===null&&x.screen_position.length===2));
 assert.equal(spatial.grid.actual_coordinates,null);
 assert.match(spatial.grid.units,/DISPLAY_PIXELS/);
});
t('All 56 historical fixtures map to six permanent round grounds',()=>{
 assert.equal(spatial.scene_packets.length,56);
 assert.equal(spatial.permanent_round_sites.length,6);
 assert.equal(new Set(spatial.scene_packets.map(x=>x.fixture_id)).size,56);
 const src=new Map(history.fixtures.map(x=>[x.id,x]));
 for(const p of spatial.scene_packets){
 const f=src.get(p.fixture_id);assert.ok(f);
 assert.equal(p.venue_candidate_id,f.staging.venue_id);
 assert.equal(p.source_verified_winner_slot,f.winner_slot);
 assert.ok(p.physical_fit.eligible);
 }
});
t('Every historical trial includes two personally acting contenders at three safe stages',()=>{
 assert.equal(spatial.scene_packets.reduce((n,x)=>n+x.stage_axes.length,0),168);
 assert.ok(spatial.scene_packets.every(x=>x.stage_axes.every(st=>st.personally_performed)));
 for(const p of spatial.scene_packets)for(const stage of p.stage_axes){
 assert.ok(stage.A[0]<0&&stage.B[0]>0);
 assert.ok(Math.hypot(stage.A[0],stage.A[1])<stage.contest_ring);
 assert.ok(Math.hypot(stage.B[0],stage.B[1])<stage.contest_ring);
 assert.ok(Math.hypot(stage.A[0]-stage.B[0],stage.A[1]-stage.B[1])>stage.barrier_radius*2);
 }
});
t('Spectator, contender, broadcast and service entries are separately traceable',()=>{
 for(const s of spatial.scene_packets){
  assert.equal(s.access.contender[0],'CONTENDER_FORTRESS');
  assert.equal(s.access.spectator[0],'TAILGATE_COMMONS');
  assert.equal(s.access.broadcast[0],'BROADCAST_HQ');
  assert.equal(s.access.service[0],'UTILITY_PLANT');
  assert.ok(!s.access.spectator.includes('CONTENDER_FORTRESS'));
 }
});
t('The Last Field orientation is constant in eleven documented championship presentations',()=>{
 const finals=spatial.scene_packets.filter(x=>x.round==='FINAL');
 assert.equal(finals.length,11);
 assert.ok(finals.every(x=>x.venue_candidate_id==='CAND-POST-LAST-FIELD'));
 assert.ok(spatial.permanent_round_sites.find(x=>x.id==='CAND-POST-LAST-FIELD').preservation_rule.includes('FOUNDATION_FIXED'));
});
t('Strong weather prevents windward and dangerous harbor stage production',()=>{
 const chosen=ids.get(dmap.get('HIST-POST-2025-QF-2').selected_obstacle_id);
 const storm=validateStageContest({venue_id:'CAND-POST-SALTWIND',year:2025,round:'QF',obstacle:chosen,conditions:{weather:'STORM'}});
 assert.equal(storm.eligible,false);assert.ok(storm.reasons.includes('CLOSED_SEVERE_CLIFF_WEATHER'));
 const water=validateStageContest({venue_id:'CAND-POST-BREAKWATER',year:2025,round:'QF',obstacle:chosen,conditions:{tide:'STORM_SURGE'}});
 assert.equal(water.eligible,false);
});
t('Old-era unavailable arena is never used for an opening trial',()=>{
 const o=obstacle.obstacles.find(x=>x.name==='Stone Circle Sumo');
 const fit=validateStageContest({venue_id:'CAND-POST-IRON-QUARRY',round:'QF',year:2015,obstacle:o});
 assert.equal(fit.eligible,false);assert.ok(fit.reasons.includes('VENUE_NOT_BUILT_FOR_THIS_ERA'));
});
t('Broadcast and public routes cannot enter protected memorial as generic shortcut',()=>{
 assert.equal(route('MUSEUM_TROPHY_HALL','FARRELL_SANCTUARY','public'),null);
 assert.ok(route('MUSEUM_TROPHY_HALL','FARRELL_SANCTUARY','memorial_public'));
});
t('No output claims a real physics solver, actual time, or live GIS promotion',()=>{
 assert.equal(spatial.no_sport_result_simulation,true);
 assert.equal(spatial.no_live_world_data_mutation,true);
 assert.equal(spatial.no_2026_outcome,true);
 assert.ok(spatial.scene_packets.every(x=>x.deferred_real_geometry.length>=4));
 assert.ok(spatial.scene_packets.every(x=>x.physical_fit.structural_certification===false));
});
t('Scenic material history remains tied to exact documented fixture IDs',()=>{
 const set=new Set(scenes.cards.map(x=>x.fixture_id));
 assert.ok(spatial.scene_packets.every(x=>set.has(x.fixture_id)));
 assert.ok(spatial.scene_packets.every(x=>x.persistent_fixture_impact==='TRACE-'+x.fixture_id));
});
console.log(JSON.stringify({status:'PASS',tests:checks.length,fixtures:56,stage_positions:168,diagram_nodes:23,independent_certification:false,details:checks},null,2));
