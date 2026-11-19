#!/usr/bin/env node
/**
 * Repeatable Founder V2 Championship Island preproduction pipeline.
 * --check (default) validates preserved outputs without modifying the repo.
 * --refresh regenerates ONLY two noncanon preview files after independent structural checks.
 * No network use, no world/data writes, no art, no public deployment, no claims of live agents.
 */
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {compile,validate} from './build_postseason_inklings_packets.mjs';
import {exportConsumers} from './export_postseason_consumers.mjs';

const root=path.dirname(fileURLToPath(import.meta.url));
const paths={
  history:'HISTORICAL_POSTSEASON_ENCOUNTERS_2015_2025.founder_v2.json',
  sites:'ISLAND_SITE_EVOLUTION_2015_2025.founder_v2.json',
  bridge:'ISLAND_CAUSEWAY_TOPOLOGY.founder_v2.json',
  contract:'POSTSEASON_2026_ISLAND_EVENT_CONTRACT.proposal.json',
  broadcast:'CHAMPIONSHIP_ISLAND_BROADCAST_HERITAGE_2015_2026.proposal.json',
  obstacles:'OBSTACLE_LEXICON_120_V1.json',
  bindings:'HISTORICAL_CHALLENGE_OPTION_BINDINGS_56_V1.json',
  material:'ISLAND_MATERIAL_MEMORY_2015_2025_V1.json',
  draw:'HISTORICAL_CEREMONIAL_DRAW_2015_2025.proposal.json',
  impacts:'ISLAND_PERMANENT_IMPACT_LEDGER_2015_2025.proposal.json',
  scenes:'INKLINGS_INTERVIEW_II_56_MATCH_SCENE_CONTRACTS.proposal.json',
  body:'INKLINGS_OWNER_BODY_CONSEQUENCE_2015_2025.proposal.json',
  finalesV2:'INKLINGS_ELEVEN_CHAMPIONSHIP_FINALES_INTERVIEW_II_V2.proposal.json',
  storyboard:'INKLINGS_INTERVIEW_II_VISUAL_STORYBOARDS_56.proposal.json',
  spatial:'ISLAND_SPATIAL_STAGE_ENGINE_V1.proposal.json',
  rigs:'HISTORICAL_RIG_INTERLOCK_PROTOCOLS_V1.proposal.json',
  atlasSiting:'ATLAS_NEUTRAL_CAUSEWAY_SITING_HYPOTHESIS_V1.proposal.json',
  cards:'INKLINGS_2015_2025_COMPILED_PRODUCTION_CARDS.proposal.json',
  export:'POSTSEASON_CROSS_OS_PREPRODUCTION_EXPORT.founder_v2.json'
};
const get=k=>fs.readFileSync(path.join(root,paths[k]),'utf8');
const parse=k=>JSON.parse(get(k));
const sha=t=>crypto.createHash('sha256').update(t).digest('hex');
const equal=(a,b,msg)=>assert.deepStrictEqual(a,b,msg);
function verifyTopology(t){
  const ids=new Set(t.nodes.map(x=>x.id));
  assert.equal(ids.size,23,'Expected 23 unique conceptual island nodes');
  assert.equal(t.edges.length,45,'Expected 45 conceptual links');
  const adj=new Map([...ids].map(n=>[n,[]]));
  for(const edge of t.edges) {
    assert.ok(ids.has(edge.from)&&ids.has(edge.to),'Dangling edge');
    adj.get(edge.from).push(edge.to); adj.get(edge.to).push(edge.from);
  }
  const seen=new Set(['MAINLAND_PUBLIC_LITTORAL']),stack=[...seen];
  for(const node of stack)for(const neighbor of adj.get(node)||[])if(!seen.has(neighbor)){seen.add(neighbor);stack.push(neighbor);}
  assert.equal(seen.size,ids.size,'Disconnected island access node');
  assert.ok(t.nodes.every(n=>n.coordinates===null),'Invented geographic coordinates');
}
function verifyVenueFacts(h,s){
 const byID=new Map(s.sites.map(site=>[site.id,site]));
 assert.equal(h.fixtures.length,56);
 assert.equal(h.annual.length,11);
 assert.equal(s.annual.length,11);
 for(const encounter of h.fixtures) {
   const site=byID.get(encounter.staging.venue_id);
   assert.ok(site,'Unknown stage site');
   const owner={QF:'QUARTERFINAL_ONLY',SF:'SEMIFINAL_ONLY',FINAL:'FINAL_ONLY'}[encounter.round];
   assert.equal(site.round_assignment,owner,'Arena assigned to wrong round');
 }
 for(const season of h.annual){
   const matches=h.fixtures.filter(f=>f.year===season.year);
   const found=s.annual.find(a=>a.year===season.year);
   assert.ok(found,'Missing site year');
   equal([...new Set(matches.map(x=>x.staging.venue_id))].sort(),found.site_ids.slice().sort(),'Site usage drift');
 }
}
function build(){
 const hraw=get('history');
 const history=JSON.parse(hraw),sites=parse('sites'),topology=parse('bridge'),contract=parse('contract'),broadcast=parse('broadcast');
 validate(history,sites);
 verifyTopology(topology);
 verifyVenueFacts(history,sites);
 assert.equal(contract.schema,'schemin.postseason_island_event_contract.founder_v2');
 const cards=compile(history,sites,sha(hraw));
 const exportData=exportConsumers(cards,topology,contract,broadcast,parse('obstacles'),parse('bindings'),parse('material'),parse('draw'),parse('impacts'),parse('scenes'),parse('body'),parse('finalesV2'),parse('storyboard'),parse('spatial'),parse('rigs'),parse('atlasSiting'));
 assert.equal(cards.headline.challenge_stages,168);
 assert.equal(exportData.publication_status,'HOLD_NO_INDEPENDENT_UMPIRE_OR_ACTIVE_ATLAS_PROMOTION');
 assert.equal(exportData.postseason_2026.champion,null);
 assert.equal(exportData.commonwealth_site.deployed,false);
 return {cards,exportData,history,topology};
}
function atomicSave(k,obj){
 const filepath=path.join(root,paths[k]);
 const tmp=filepath+'.pipeline-tmp';
 fs.writeFileSync(tmp,JSON.stringify(obj,null,2)+'\n','utf8');
 fs.renameSync(tmp,filepath);
}
function main(argv){
 const refresh=argv.includes('--refresh');
 assert.ok(argv.every(x=>x==='--refresh'||x==='--check'),'Unknown pipeline argument');
 assert.ok(!(argv.includes('--refresh')&&argv.includes('--check')),'Choose check or refresh');
 const {cards,exportData,history,topology}=build();
 if(refresh) {
   atomicSave('cards',cards);
   atomicSave('export',exportData);
 } else {
   equal(parse('cards'),cards,'Stored Inklings cards out of sync; use --refresh to regenerate previews only');
   equal(parse('export'),exportData,'Stored cross-OS export out of sync; use --refresh to regenerate previews only');
 }
 console.log(JSON.stringify({
   status:'PASS',mode:refresh?'REFRESH_PREVIEWS':'CHECK_ONLY',
   years:history.annual.length,fixtures:history.fixtures.length,
   stages:cards.headline.challenge_stages,network_nodes:topology.nodes.length,
   source_status:'VERIFIED_SPORTS_PLUS_NONCANON_FICTION',
   publication_status:exportData.publication_status,
   next:'INDEPENDENT_UMPIRE_ATLAS_CANON_REVIEW'
 }));
}
main(process.argv.slice(2));
