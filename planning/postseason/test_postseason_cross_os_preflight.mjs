#!/usr/bin/env node
/**
 * Founder V2 Championship Island cross-OS preflight.
 * Read-only checks. Runs against planning/postseason candidate files.
 * Cannot promote any LOCATION, publish a 2026 winner, or certify independent Umpire.
 */
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {exportConsumers} from './export_postseason_consumers.mjs';

const dir=path.dirname(fileURLToPath(import.meta.url));
const read=name=>JSON.parse(fs.readFileSync(path.join(dir,name),'utf8'));
const clone=x=>JSON.parse(JSON.stringify(x));
const checks=[];
function check(label,fn){fn(); checks.push(label);}
function expectsFailure(label,fn) {
 assert.throws(fn,Error,label);
 checks.push(label);
}
const cards=read('INKLINGS_2015_2025_COMPILED_PRODUCTION_CARDS.proposal.json');
const topology=read('ISLAND_CAUSEWAY_TOPOLOGY.founder_v2.json');
const contract=read('POSTSEASON_2026_ISLAND_EVENT_CONTRACT.proposal.json');
const broadcast=read('CHAMPIONSHIP_ISLAND_BROADCAST_HERITAGE_2015_2026.proposal.json');
const history=read('HISTORICAL_POSTSEASON_ENCOUNTERS_2015_2025.founder_v2.json');
const sites=read('ISLAND_SITE_EVOLUTION_2015_2025.founder_v2.json');
const years=Array.from({length:11},(_,i)=>2015+i);
const roundMap={QF:['CAND-POST-IRON-QUARRY','CAND-POST-SALTWIND','CAND-POST-BREAKWATER'],SF:['CAND-POST-CROWN-STAIR','CAND-POST-GROVE'],FINAL:['CAND-POST-LAST-FIELD']};
const exported=exportConsumers(cards,topology,contract,broadcast);

function reachable(t) {
 const all=new Set(t.nodes.map(n=>n.id));
 const neighbors=new Map([...all].map(n=>[n,[]]));
 for(const e of t.edges){
   assert.ok(all.has(e.from)&&all.has(e.to),'Dangling route node');
   assert.notEqual(e.from,e.to,'Loop is not a valid island route');
   neighbors.get(e.from).push(e.to);
   neighbors.get(e.to).push(e.from);
 }
 const seen=new Set(['MAINLAND_PUBLIC_LITTORAL']),queue=[...seen];
 for(const v of queue)for(const u of neighbors.get(v)||[])if(!seen.has(u)){seen.add(u);queue.push(u);}
 return {count:seen.size,total:all.size};
}
check('Eleven consecutive seasons, 56 matchups and 168 stage beats',()=>{
 assert.equal(history.fixtures.length,56);
 assert.equal(cards.cards.length,56);
 assert.equal(cards.cards.reduce((a,c)=>a+c.beat_sequence.length,0),168);
 assert.deepEqual(history.annual.map(y=>y.year),years);
 assert.deepEqual(cards.annual.map(y=>y.season),years);
});
check('Founder V2 round-specific arena invariants',()=>{
 const byId=new Map(sites.sites.map(x=>[x.id,x]));
 for(const f of history.fixtures){
   const permitted=roundMap[f.round];
   assert.ok(permitted.includes(f.staging.venue_id),f.id);
   assert.equal(byId.get(f.staging.venue_id)?.name,f.staging.venue_name,f.id);
 }
 assert.equal(history.fixtures.filter(f=>f.staging.venue_id==='CAND-POST-LAST-FIELD').length,11);
});
check('All historical scores and winner identities agree with original sporting record',()=>{
 const originals=read('HISTORICAL_POSTSEASON_ENCOUNTERS_2015_2025.proposal.json');
 const originalById=new Map(originals.fixtures.map(f=>[f.id,f]));
 for(const f of history.fixtures) {
   const orig=originalById.get(f.id);
   assert.ok(orig,'Lost source fixture '+f.id);
   assert.deepEqual({home:f.home,away:f.away,winner_slot:f.winner_slot,period:f.scoring_period},
     {home:orig.home,away:orig.away,winner_slot:orig.winner_slot,period:orig.scoring_period},f.id);
 }
});
check('11-year island states match 56 venue assignments',()=>{
 assert.equal(sites.annual.length,11);
 for(const year of years){
   const a=sites.annual.find(y=>y.year===year);
   assert.ok(a);
   const used=[...new Set(history.fixtures.filter(f=>f.year===year).map(f=>f.staging.venue_id))].sort();
   assert.deepEqual([...a.site_ids].sort(),used);
 }
});
check('Causeway and all 23 proposed points connected, no map coordinate invented',()=>{
 assert.equal(topology.nodes.length,23);
 assert.equal(topology.edges.length,45);
 assert.deepEqual(reachable(topology),{count:23,total:23});
 assert.ok(topology.nodes.every(n=>n.coordinates===null && n.status==='PROPOSED_ONLY'));
 assert.ok(topology.edges.every(e=>e.status==='PLANNING_ONLY'));
});
check('Island uses a single fixed championship ground and no early title reveal',()=>{
 assert.deepEqual(contract.venue_assignment.rounds.CHAMPIONSHIP,roundMap.FINAL);
 assert.deepEqual(contract.venue_assignment.rounds.SEMIFINAL,roundMap.SF);
 assert.deepEqual(contract.venue_assignment.rounds.QUARTERFINAL,roundMap.QF);
 assert.equal(exported.postseason_2026.champion,null);
 assert.equal(exported.postseason_2026.qualifiers,null);
 assert.equal(exported.postseason_2026.winners,null);
 assert.equal(exported.postseason_2026.finalists,null);
});
check('Cross-OS export remains preproduction and preserves independent release authority',()=>{
 assert.equal(exported.status,'PREPRODUCTION_EXPORT_NOT_PUBLICATION');
 assert.equal(exported.commonwealth_site.deployed,false);
 assert.equal(exported.commonwealth_site.renders_available,false);
 assert.equal(exported.publication_status,'HOLD_NO_INDEPENDENT_UMPIRE_OR_ACTIVE_ATLAS_PROMOTION');
 assert.equal(exported.memo_os.history_cards.length,56);
 assert.equal(exported.novel_os.encounter_contracts.length,56);
});
check('Modern island broadcast, causeway, and Inklings authorization represented as proposals',()=>{
 assert.match(contract.visual_environment.approach,/CAUSEWAY/);
 assert.match(contract.visual_environment.theme,/RUGGED/);
 assert.match(contract.media_rhythm.in_world_technology,/Founder F08 DESIGN DIRECTION/);
 assert.match(contract.inklings_role.status,/NOT_INDEPENDENT_AGENTS_INVOCATION/);
});
expectsFailure('Reject missing 2025 encounter',()=>{
 const x=clone(cards); x.cards.pop(); exportConsumers(x,topology,contract,broadcast);
});
expectsFailure('Reject missing causeway node',()=>{
 const x=clone(topology); x.nodes=x.nodes.filter(n=>n.id!=='CAUSEWAY_RIDGE'); exportConsumers(cards,x,contract,broadcast);
});
expectsFailure('Reject invented 2026 berth structure',()=>{
 const x=clone(contract); x.schedule.qualification_count=8; exportConsumers(cards,topology,x,broadcast);
});
expectsFailure('Reject promoted-but-uncertified fiction',()=>{
 const x=clone(cards); x.cards[0].creative_status='APPROVED_CANON'; exportConsumers(x,topology,contract,broadcast);
});
check('Every title ceremony remains recorded but Farrell founding date unresolved',()=>{
 assert.equal(history.fixtures.filter(f=>f.round==='FINAL').length,11);
 assert.ok(contract.holds.some(x=>x.toLowerCase().includes('memorial')));
});
console.log(JSON.stringify({status:'PASS',checks:checks.length,years:11,fixtures:56,challenge_stages:168,island_nodes:23,route_edges:45,publication:'HOLD',details:checks},null,2));
