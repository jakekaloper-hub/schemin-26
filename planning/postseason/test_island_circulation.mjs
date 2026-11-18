#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';

const dir=path.dirname(fileURLToPath(import.meta.url));
const t=JSON.parse(fs.readFileSync(path.join(dir,'ISLAND_CAUSEWAY_TOPOLOGY.founder_v2.json'),'utf8'));
const names=new Set(t.nodes.map(n=>n.id)),edges=t.edges;
const expectedArenas=['IRON_QUARRY','SALTWIND_STEPS','BREAKWATER_GROUNDS','CROWN_STAIR','GROVE_STANDARDS','LAST_FIELD'];
const checks=[];
function test(name,fn){fn();checks.push(name);}
function route(start,end,mode,graph=edges){
  const seen=new Set([start]),q=[start],previous=new Map();
  for(const id of q){
    if(id===end){const path=[end];let p=end;while(previous.has(p)){p=previous.get(p);path.unshift(p);}return path;}
    for(const e of graph){
      if(!e.modes.includes(mode))continue;
      const other=e.from===id?e.to:e.to===id?e.from:null;
      if(other && !seen.has(other)){seen.add(other);previous.set(other,id);q.push(other);}
    }
  }
  return null;
}
test('23 unique spatial nodes and 45 route segments',()=>{
  assert.equal(t.nodes.length,23);assert.equal(names.size,23);assert.equal(edges.length,45);
  assert.ok(edges.every(e=>names.has(e.from)&&names.has(e.to)&&e.status==='PLANNING_ONLY'));
  assert.ok(t.nodes.every(n=>n.coordinates===null && n.status==='PROPOSED_ONLY'));
});
test('Public can reach six spectator arenas over actual causeway',()=>{
 for(const site of expectedArenas){const p=route('MAINLAND_PUBLIC_LITTORAL',site,'public');assert.ok(p,site);assert.ok(p.includes('CAUSEWAY_RIDGE'),site);}
});
test('Public access to beach and historical memorial through checkpoint',()=>{
 for(const site of ['LOSERS_BEACH','CHAMPIONS_WALK','MUSEUM_TROPHY_HALL'])assert.ok(route('MAINLAND_PUBLIC_LITTORAL',site,'public'),site);
 assert.ok(route('MUSEUM_TROPHY_HALL','FARRELL_SANCTUARY','memorial_public'));
});
test('Contenders use private admissions and travel to every arena',()=>{
 assert.ok(route('ISLAND_ENTRY_CHECK','CONTENDER_FORTRESS','contender'));
 assert.ok(route('CONTENDER_FORTRESS','BYE_HOUSE','contender'));
 for(const site of expectedArenas){const p=route('CONTENDER_FORTRESS',site,'contender');assert.ok(p,site);assert.ok(!p.includes('TAILGATE_COMMONS'),site);}
});
test('Independent stadium broadcast control routes exist',()=>{
 for(const site of expectedArenas)assert.ok(route('BROADCAST_HQ',site,'media'),site);
});
test('Separate power and venue maintenance routes exist',()=>{
 for(const site of expectedArenas)assert.ok(route('UTILITY_PLANT',site,'service'),site);
 assert.ok(route('UTILITY_PLANT','BROADCAST_HQ','service'));
});
test('Shoreside escorted elimination route is distinct from public tournament gate',()=>{
 const p=route('CONTENDER_FORTRESS','LOSERS_BEACH','post_elimination');
 assert.deepEqual(p,['CONTENDER_FORTRESS','LOSERS_BEACH']);
});
test('Beach, crowd center and final ground can reach emergency pier independently',()=>{
 for(const site of ['LOSERS_BEACH','TAILGATE_COMMONS','LAST_FIELD'])assert.ok(route(site,'EMERGENCY_PIER','emergency'),site);
 assert.ok(route('EMERGENCY_PIER','MAINLAND_PUBLIC_LITTORAL','emergency'));
});
test('Causeway loss breaks mainland road admissions; reject false promise of access',()=>{
 const broken=edges.filter(e=>e.from!=='CAUSEWAY_RIDGE'&&e.to!=='CAUSEWAY_RIDGE');
 assert.equal(route('MAINLAND_PUBLIC_LITTORAL','TAILGATE_COMMONS','public',broken),null);
});
test('Restricted contender house is inaccessible by public-only paths',()=>{
 assert.equal(route('MAINLAND_PUBLIC_LITTORAL','CONTENDER_FORTRESS','public'),null);
 assert.equal(route('MAINLAND_PUBLIC_LITTORAL','BYE_HOUSE','public'),null);
});
test('No stadium can use a memorial-only route as sporting entrance',()=>{
 assert.equal(route('FARRELL_SANCTUARY','LAST_FIELD','memorial_public'),null);
});
test('All links and points remain fictional and unmeasured',()=>{
 assert.match(t.status,/CANDIDATE/);
 assert.ok(edges.every(e=>!('meters' in e)&&!('time_minutes' in e)));
});
console.log(JSON.stringify({status:'PASS',checks:checks.length,nodes:names.size,links:edges.length,results:checks},null,2));
