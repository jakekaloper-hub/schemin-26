#!/usr/bin/env node
/**
 * Cross-domain counterweight preflight for Founder Interview II.
 * Deterministic implementation audit only, not independent Umpire acceptance.
 */
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const dir=path.dirname(fileURLToPath(import.meta.url));
const read=n=>JSON.parse(fs.readFileSync(path.join(dir,n),'utf8'));
const h=read('HISTORICAL_POSTSEASON_ENCOUNTERS_2015_2025.founder_v2.json');
const draw=read('HISTORICAL_CEREMONIAL_DRAW_2015_2025.proposal.json');
const traces=read('ISLAND_PERMANENT_IMPACT_LEDGER_2015_2025.proposal.json');
const bodies=read('INKLINGS_OWNER_BODY_CONSEQUENCE_2015_2025.proposal.json');
const scenes=read('INKLINGS_INTERVIEW_II_56_MATCH_SCENE_CONTRACTS.proposal.json');
const shots=read('INKLINGS_INTERVIEW_II_VISUAL_STORYBOARDS_56.proposal.json');
const final=read('INKLINGS_ELEVEN_CHAMPIONSHIP_FINALES_INTERVIEW_II_V2.proposal.json');
const exportData=read('POSTSEASON_CROSS_OS_PREPRODUCTION_EXPORT.founder_v2.json');
const tests=[];
function test(name,fn){fn();tests.push(name)}
const fBy=new Map(h.fixtures.map(x=>[x.id,x]));
const dBy=new Map(draw.ceremonies.map(x=>[x.fixture_id,x]));
const tBy=new Map(traces.traces.map(x=>[x.fixture_id,x]));
const bodyBy=new Map(bodies.games.map(x=>[x.fixture_id,x]));
test('56 source fixtures uniquely join to ceremonies, scars, body effects and scripts',()=>{
 assert.equal(fBy.size,56);
 for(const map of [dBy,tBy,bodyBy])assert.equal(map.size,56);
 assert.equal(scenes.cards.length,56);
 assert.equal(shots.cards.length,56);
 for(const row of h.fixtures){
   assert.ok(dBy.has(row.id)&&tBy.has(row.id)&&bodyBy.has(row.id));
   const scene=scenes.cards.find(x=>x.fixture_id===row.id);
   assert.ok(scene);
   assert.equal(scene.verified_sports.winner_slot,row.winner_slot);
   assert.deepEqual(scene.verified_sports.home,row.home);
   assert.deepEqual(scene.verified_sports.away,row.away);
   assert.equal(scene.draw.ticket_hash,dBy.get(row.id).draw_ticket_sha256);
   assert.equal(scene.physical_history.trace_id,tBy.get(row.id).trace_id);
 }
});
test('All independently numbered in-scene stage roles personally performed',()=>{
 for(const scene of scenes.cards){
   assert.deepEqual(scene.acts.map(a=>a.number),[1,2,3]);
   assert.ok(scene.acts.every(a=>a.solo_contender_A.personally_competes&&a.solo_contender_B.personally_competes));
   assert.ok(scene.acts.every(a=>a.scene_text.includes('personally')||a.scene_text.includes('Both sides must act')));
 }
});
test('No clash between permanent Last Field final and semifinal/quarterfinal sites',()=>{
 for(const f of h.fixtures){
 const scene=scenes.cards.find(x=>x.fixture_id===f.id);
 if(f.round==='FINAL')assert.equal(scene.venue_id,'CAND-POST-LAST-FIELD');
 else assert.notEqual(scene.venue_id,'CAND-POST-LAST-FIELD');
 }
});
test('New historical final prose matches its own fixed ceremony ticket',()=>{
 assert.equal(final.scenes.length,11);
 for(const prose of final.scenes){
   const f=h.fixtures.find(x=>x.year===prose.year&&x.round==='FINAL'),d=dBy.get(f.id),t=tBy.get(f.id);
   assert.ok(prose.ceremonial_draw);
   assert.equal(prose.ceremonial_draw.obstacle_id,d.selected_obstacle_id);
   assert.equal(prose.ceremonial_draw.ticket,d.draw_ticket_sha256);
   assert.equal(prose.permanent_trace_id,t.trace_id);
   assert.equal(prose.verified.winner_slot,f.winner_slot);
   assert.equal(prose.venue_id,'CAND-POST-LAST-FIELD');
 }
});
test('Camera shot contracts are complete but explicitly not rendered artifacts',()=>{
 assert.equal(shots.counts.shot_contracts,672);
 assert.equal(shots.cards.length,56);
 for(const sheet of shots.cards){
 assert.equal(sheet.production_cameras.length,12);
 assert.ok(sheet.production_cameras.every(x=>x.rendering_status.includes('BLOCKED')));
 assert.equal(sheet.cut_release,'PREVIS_ONLY_NOT_RENDERED');
 assert.ok(sheet.production_cameras.every(x=>x.location_id!==null));
 }
});
test('Persistent effects accumulate and later repair does not erase original record',()=>{
 assert.equal(traces.traces.length,56);
 assert.equal(traces.annual_states.at(-1).cumulative_traces_at_close,56);
 assert.ok(traces.traces.every(t=>t.year_after.restored_function&&t.year_after.history_not_erased));
 assert.ok(traces.traces.every(t=>!t.active_world_state_writeback));
});
test('Fictional body consequences are not presented as actual owner health data',()=>{
 assert.equal(bodies.counts.fictional_participant_effects,112);
 assert.ok(bodies.games.every(g=>g.team_slot_health_fiction.every(x=>x.source.includes('NOT_REAL_PERSON_HEALTH_DATA'))));
});
test('Cross-OS package contains all new source-bound data and remains unpublished',()=>{
 assert.equal(exportData.interview_ii.ceremonial_draws.length,56);
 assert.equal(exportData.interview_ii.permanent_traces.length,56);
 assert.equal(exportData.interview_ii.in_world_direct_competition.length,56);
 assert.equal(exportData.visual_preproduction.annual_finales.length,11);
 assert.equal(exportData.postseason_2026.champion,null);
 assert.equal(exportData.commonwealth_site.deployed,false);
 assert.equal(exportData.publication_status,'HOLD_NO_INDEPENDENT_UMPIRE_OR_ACTIVE_ATLAS_PROMOTION');
});
console.log(JSON.stringify({status:'PASS',checks:tests.length,scenes:56,finales:11,camera_shots:672,body_effects:112,real_2026_results_written:0,independent_umpire:'NOT_INVOKED',checks_passed:tests},null,2));
