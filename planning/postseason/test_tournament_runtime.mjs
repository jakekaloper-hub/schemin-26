#!/usr/bin/env node
import assert from 'node:assert/strict';
import {evaluateIslandTournament,IslandBracketError,ROUNDS} from './tournament_runtime.mjs';
const tests=[];
function test(name,run){run();tests.push(name);}
function bad(name,change,stage='QF'){
 const s=baseline(),matches=fixtures(stage);
 if(stage==='QF')s.fixtures=matches.slice(0,3);
 else if(stage==='SF')s.fixtures=matches.slice(0,5);
 else s.fixtures=matches;
 change(s);
 assert.throws(()=>evaluateIslandTournament(s,{testMode:true}),IslandBracketError);
 tests.push(name);
}
function base(){
 return {season:2026,league_id:'1417621',qualification_locked:false,entrants:[],fixtures:[],reseed:false};
}
function baseline(){
 return {season:2026,league_id:'1417621',qualification_locked:true,snapshot_id:'synthetic-fixture-snapshot-2026',source:'TEST',reseed:false,
 entrants:Array.from({length:7},(_,i)=>({team_id:'T'+(i+1),seed:i+1})),fixtures:[]};
}
const mk=(fixture_id,round,week,venue_candidate_id,home_id,away_id,home_points,away_points,winner_id)=>({
fixture_id,round,week,venue_candidate_id,home_id,away_id,home_points,away_points,winner_id,status:'FINAL',
certified:true,source:'TEST',snapshot_id:'synthetic-matchup-'+fixture_id
});
function fixtures(stage){
 const arr=[
mk('Q1','QF',15,'CAND-POST-IRON-QUARRY','T2','T7',122,91,'T2'),
mk('Q2','QF',15,'CAND-POST-SALTWIND','T3','T6',102,127,'T6'),
mk('Q3','QF',15,'CAND-POST-BREAKWATER','T4','T5',132,97,'T4'),
mk('S1','SF',16,'CAND-POST-CROWN-STAIR','T1','T4',143,128,'T1'),
mk('S2','SF',16,'CAND-POST-GROVE','T2','T6',123,134,'T6'),
mk('F1','FINAL',17,'CAND-POST-LAST-FIELD','T1','T6',139,156,'T6')];
 return stage==='QF'?arr.slice(0,3):stage==='SF'?arr.slice(0,5):arr;
}
test('No 2026 qualified teams pre-lock; no invented winner',()=>{
 const x=evaluateIslandTournament(base());
 assert.equal(x.status,'AWAITING_QUALIFICATION');
 assert.equal(x.champion,null);
 assert.equal(x.beach_count,null);
});
test('Seven entrants and seed 1 bye before first outcome',()=>{
 const x=evaluateIslandTournament(baseline(),{testMode:true});
 assert.equal(x.status,'TOURNAMENT_IN_PROGRESS');
 assert.equal(x.bye_team_id,'T1');
 assert.equal(x.round,'QF');
 assert.equal(x.beach_count,5);
 assert.equal(x.contender_team_ids.length,7);
 assert.equal(x.certified_events.filter(e=>e.type==='FIRST_ROUND_BYE').length,1);
});
test('One certified quarterfinal creates first beach transfer only',()=>{
 const s=baseline();s.fixtures=[fixtures('QF')[0]];
 const x=evaluateIslandTournament(s,{testMode:true});
 assert.equal(x.beach_count,6);
 assert.equal(x.team_status.T7.state,'ELIMINATED_QF');
 assert.equal(x.team_status.T2.state,'ADVANCED');
 assert.equal(x.certified_events.filter(e=>e.type==='SHOREWARD_DESCENT').length,1);
 assert.equal(x.champion,null);
});
test('Provisional quarterfinal does not eliminate either team',()=>{
 const s=baseline();const x=fixtures('QF')[0];x.status='IN_PROGRESS';x.certified=false;x.winner_id=null;
 s.fixtures=[x];const out=evaluateIslandTournament(s,{testMode:true});
 assert.equal(out.beach_count,5);assert.equal(out.team_status.T7.state,'QUALIFIED');
});
test('Three QF results produce four surviving contenders',()=>{
 const s=baseline();s.fixtures=fixtures('QF');
 const x=evaluateIslandTournament(s,{testMode:true});
 assert.equal(x.beach_count,8);assert.deepEqual(x.contender_team_ids.slice().sort(),['T1','T2','T4','T6']);
 assert.equal(x.round,'SF');assert.equal(x.champion,null);
});
test('One semifinal result adds exactly one beach newcomer',()=>{
 const s=baseline();s.fixtures=fixtures('SF').slice(0,4);
 const x=evaluateIslandTournament(s,{testMode:true});
 assert.equal(x.beach_count,9);assert.equal(x.team_status.T4.state,'ELIMINATED_SF');
 assert.equal(x.round,'SF');
});
test('Both semifinals close the finalist selection, not the title',()=>{
 const s=baseline();s.fixtures=fixtures('SF');
 const x=evaluateIslandTournament(s,{testMode:true});
 assert.equal(x.beach_count,10);assert.deepEqual(x.contender_team_ids.slice().sort(),['T1','T6']);
 assert.equal(x.round,'FINAL');assert.equal(x.champion,null);
});
test('The actual championship state appears only after Last Field certified',()=>{
 const s=baseline();s.fixtures=fixtures('FINAL');
 const x=evaluateIslandTournament(s,{testMode:true});
 assert.equal(x.beach_count,11);assert.equal(x.champion,'T6');assert.equal(x.round,'COMPLETE');
 assert.equal(x.team_status.T1.state,'RUNNER_UP');
 assert.equal(x.award.venue_candidate_id,'CAND-POST-LAST-FIELD');
 assert.match(x.publication,/HOLD/);
 assert.equal(x.certified_events.filter(e=>e.type==='SHOREWARD_DESCENT').length,6);
});
test('Six distinct fixture venue slots follow permanent round reservations',()=>{
 assert.deepEqual(ROUNDS.map(r=>r.slots),[3,2,1]);
 assert.deepEqual(ROUNDS.map(r=>r.week),[15,16,17]);
});
bad('Reject unverified real ESPN qualification in test mode',s=>s.source='ESPN');
bad('Reject eight qualifiers or duplicate seed',s=>s.entrants.push({team_id:'T8',seed:8}));
bad('Reject reseeded championship',s=>s.reseed=true);
bad('Reject invented winner inconsistent with real score',s=>s.fixtures[0].winner_id='T7');
bad('Reject outcome not certified by source',s=>s.fixtures[0].certified=false);
bad('Reject semifinal in quarterfinal stage',s=>s.fixtures.push(fixtures('SF')[3]));
bad('Reject round venue crossover',s=>s.fixtures[0].venue_candidate_id='CAND-POST-CROWN-STAIR');
bad('Reject invalid old loser returned as finalist',s=>{s.fixtures=fixtures('FINAL');s.fixtures[5].home_id='T7';},'FINAL');
bad('Reject a contender entering two QFs',s=>s.fixtures[1].away_id='T2');
bad('Reject duplicate venue use within same round',s=>s.fixtures[1].venue_candidate_id=s.fixtures[0].venue_candidate_id);
bad('Reject forecast-like winner before final lock',s=>{s.fixtures[0].status='IN_PROGRESS';s.fixtures[0].certified=false;},'QF');
bad('Reject wrong playoff week',s=>s.fixtures[0].week=16);
console.log(JSON.stringify({status:'PASS',cases:tests.length,season:2026,sporting_data:'SYNTHETIC_TEST_ONLY',future_results_published:0,tests},null,2));
