import test from 'node:test';
import assert from 'node:assert/strict';
import {buildObserverCatalog} from '../scripts/build-observer-catalog.mjs';
const source=()=>({
  locations:{coordinate_space:'abstract-only',locations:[
   {id:'LOC-CLUB',name:'The Club',physical_zone_id:'REG-SOUTHERN-WETLANDS',canon_status:'PERMANENT_CANON',abstract_position:[12,34]},
   {id:'LOC-SWAMP',name:'The Swamp',physical_zone_id:'REG-SOUTHERN-WETLANDS',canon_status:'PERMANENT_CANON',abstract_position:[30,45]}]},
  weatherRegions:{weather_regions:[{id:'WX-EASTERN-STORM',source_zone_ids:['REG-SOUTHERN-WETLANDS'],propagation_order:['REG-SOUTHERN-WETLANDS']}]},
  worldState:{as_of:'end_of_week_3_2026'},revision:'a'.repeat(40),
  worldMemory:{schema_version:'1.0',status:'RELEASE_CANDIDATE',events:[{
   event_id:'EVT-W3-CLUB',location:'LOC-CLUB',week:3,era:'2026',memory_class:'HISTORICAL',
   source:['memo-os/week-3/RECEIPT.md'],physical_effect:['chili contamination history'],
   social_effect:[],reputation_effect:[],institutional_effect:[],secondary_tags:['TEMPORARY_PHYSICAL_STATE'],
   current_relevance:true,expiry_condition:'restoration must be explicit',superseded_by:null,
  }]},
});
test('historical entries are location-exact, retain original source language and are marked candidate-only',()=>{
  const input=source(),original=structuredClone(input); const data=buildObserverCatalog(input);
  assert.deepEqual(input,original);
  assert.equal(data.history.status,'RELEASE_CANDIDATE');
  assert.equal(data.history.publicationAuthorized,false);
  assert.equal(data.history.events.length,1);
  const e=data.history.events[0];
  assert.equal(e.locationId,'LOC-CLUB');assert.equal(e.id,'EVT-W3-CLUB');assert.equal(e.week,3);
  assert.deepEqual(e.effects.physical,['chili contamination history']);
  assert.equal(e.expiryCondition,'restoration must be explicit');
  assert.deepEqual(e.sourceReceipts,['memo-os/week-3/RECEIPT.md']);
  assert.equal(JSON.stringify(data.history).includes('LOC-SWAMP'),false);
});
test('unmapped, duplicate, suspicious or promoted source-memory records fail closed',()=>{
  const change=(mutate)=>{const x=source();mutate(x);return ()=>buildObserverCatalog(x)};
  assert.throws(change(x=>x.worldMemory.events[0].location='LOC-FAKE'),/UNKNOWN_HISTORY_LOCATION/);
  assert.throws(change(x=>x.worldMemory.events.push(structuredClone(x.worldMemory.events[0]))),/DUPLICATE_HISTORY/);
  assert.throws(change(x=>x.worldMemory.events[0].source=['../private/secret']),/INVALID_HISTORY_RECEIPT/);
  assert.throws(change(x=>x.worldMemory.status='PUBLISHED'),/HISTORY_AUTHORITY/);
});
test('legacy test projection without a memory input never invents place history',()=>{
 const x=source();delete x.worldMemory;
 const c=buildObserverCatalog(x);assert.equal(c.history.status,'NOT_CONNECTED');assert.deepEqual(c.history.events,[]);
});
