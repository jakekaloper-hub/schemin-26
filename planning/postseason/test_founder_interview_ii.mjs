#!/usr/bin/env node
import assert from 'node:assert/strict';
import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';
import {drawHistorical,drawOne} from './draw_championship_trials.mjs';
import {compilePersistentTraces} from './build_permanent_impact_ledger.mjs';
const root=path.dirname(fileURLToPath(import.meta.url));
const read=n=>JSON.parse(fs.readFileSync(path.join(root,n),'utf8'));
const history=read('HISTORICAL_POSTSEASON_ENCOUNTERS_2015_2025.founder_v2.json'),lex=read('OBSTACLE_LEXICON_120_V1.json');
const draw=read('HISTORICAL_CEREMONIAL_DRAW_2015_2025.proposal.json');
const impact=read('ISLAND_PERMANENT_IMPACT_LEDGER_2015_2025.proposal.json');
const scenes=read('INKLINGS_INTERVIEW_II_56_MATCH_SCENE_CONTRACTS.proposal.json');
const body=read('INKLINGS_OWNER_BODY_CONSEQUENCE_2015_2025.proposal.json');
const clone=x=>JSON.parse(JSON.stringify(x));
const successes=[];
function test(name,fn){fn();successes.push(name);}
test('Every historical fixture receives one auditable ceremonial draw',()=>{
 const regenerated=drawHistorical(history,lex);
 assert.deepEqual(regenerated,draw);
 assert.equal(draw.ceremonies.length,56);
 assert.equal(new Set(draw.ceremonies.map(x=>x.fixture_id)).size,56);
 assert.equal(draw.winner_ids_in_draw_data,0);
});
test('No ceremonial draw can be influenced by fantasy winner or score',()=>{
 const altered=clone(history);
 for(const f of altered.fixtures){f.home.points=991;f.away.points=-3;f.winner_slot=999;}
 assert.deepEqual(drawHistorical(altered,lex),draw);
});
test('A public draw cannot use an incompatible stadium or unavailable challenge',()=>{
 const f=clone(history.fixtures[0]);
 f.staging.venue_id='CAND-POST-BREAKWATER';
 assert.throws(()=>drawOne({fixture:f,obstacles:[],historySalt:'CONSTITUTION-TEST'}),/No compatible challenge/);
 const candidate=drawOne({fixture:history.fixtures[0],obstacles:lex.obstacles});
 assert.ok(candidate.eligible_count>0);
 assert.equal(candidate.source_exclusion_verified,true);
});
test('All 56 material terrain traces reproduce and survive year-to-year',()=>{
 const reg=compilePersistentTraces(history,draw);
 assert.deepEqual(reg,impact);
 assert.equal(impact.traces.length,56);
 assert.equal(impact.annual_states[0].cumulative_traces_at_close,3);
 assert.equal(impact.annual_states.at(-1).cumulative_traces_at_close,56);
 assert.ok(impact.annual_states.every((y,i)=>i===0||y.cumulative_traces_at_close>impact.annual_states[i-1].cumulative_traces_at_close));
});
test('Fixed historic Last Field accumulates exactly eleven effects without destroying original foundation',()=>{
 const finales=impact.traces.filter(x=>x.round==='FINAL');
 assert.equal(finales.length,11);
 assert.ok(finales.every(x=>x.site_id==='CAND-POST-LAST-FIELD'));
 assert.ok(finales.every(x=>x.final_stadium_rule.includes('foundation')));
 assert.ok(finales.every(x=>x.year_after.restored_function&&x.year_after.history_not_erased));
});
test('No old physical injury is asserted as actual human owner medical history',()=>{
 assert.equal(body.games.length,56);
 assert.equal(body.counts.fictional_participant_effects,112);
 assert.ok(body.games.every(x=>x.team_slot_health_fiction.every(t=>t.source==='INVENTED_CHARACTER_FICTION__NOT_REAL_PERSON_HEALTH_DATA')));
});
test('All 168 direct-performance phases require personally competing principal on both sides',()=>{
 assert.equal(scenes.cards.length,56);
 assert.equal(scenes.cards.reduce((a,x)=>a+x.acts.length,0),168);
 assert.ok(scenes.cards.every(x=>x.acts.every(p=>p.solo_contender_A.personally_competes&&p.solo_contender_B.personally_competes)));
 assert.ok(scenes.cards.every(x=>x.character_canon.includes('SPECIFIC REAL OWNER NOT ASSUMED')));
});
test('No historical sports score, fixture title or winner changed',()=>{
 const known=new Map(history.fixtures.map(x=>[x.id,x]));
 for(const s of scenes.cards){
 const source=known.get(s.fixture_id);assert.ok(source);
 assert.deepEqual(s.verified_sports.home,source.home);
 assert.deepEqual(s.verified_sports.away,source.away);
 assert.equal(s.verified_sports.winner_slot,source.winner_slot);
 assert.deepEqual(s.draw.ticket_hash,draw.ceremonies.find(x=>x.fixture_id===s.fixture_id).draw_ticket_sha256);
 }
});
test('Injury and scar state remains nonlethal without active World mutation',()=>{
 assert.ok(impact.traces.every(t=>t.active_world_state_writeback===false));
 assert.ok(scenes.cards.every(s=>s.physical_history.world_state_writeback===false));
 assert.ok(body.limits.includes('No principal-character permanent death'));
 assert.ok(!scenes.cards.some(s=>s.year>=2026));
});
test('Future 2026 outcomes never appear in historical draw/impact/scene records',()=>{
 assert.ok(draw.ceremonies.every(x=>x.year<=2025));
 assert.ok(impact.traces.every(x=>x.year<=2025));
 assert.ok(scenes.cards.every(x=>x.year<=2025));
});
console.log(JSON.stringify({status:'PASS',checks:successes.length,ceremonies:56,permanent_traces:56,story_phases:168,personal_body_effects:112,results:successes},null,2));
