#!/usr/bin/env node
'use strict';
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const read=p=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));
const candidateStore=read('world/data/atlas_location_candidates.json');
const schema=read('schemas/atlas-location-candidate.schema.json');
const active=read('world/data/locations.json');
const routes=read('world/data/routes.json');
const regions=read('world/data/physical_zones.json');
const id='CAND-AFTER-DARK-BROADCAST-HOUSE';
const tests=[];function test(name,fn){try{fn();tests.push({name,status:'PASS'});}catch(e){tests.push({name,status:'FAIL',error:e.message});}}
const candidates=candidateStore.candidates.filter(x=>x.id===id),candidate=candidates[0],props=schema.properties.candidates.items.properties,required=schema.properties.candidates.items.required;
test('candidate exists exactly once',()=>assert.equal(candidates.length,1));
test('all candidate IDs unique',()=>assert.equal(new Set(candidateStore.candidates.map(c=>c.id)).size,candidateStore.candidates.length));
test('schema required keys',()=>required.forEach(k=>assert.ok(Object.hasOwn(candidate,k),k)));
test('schema known keys',()=>Object.keys(candidate).forEach(k=>assert.ok(Object.hasOwn(props,k),k)));
test('schema enums and strings',()=>{for(const [k,p] of Object.entries(props)){if(!Object.hasOwn(candidate,k))continue;const v=candidate[k];if(p.enum)assert.ok(p.enum.includes(v),k);if(p.type==='string')assert.equal(typeof v,'string',k);if(p.type==='boolean')assert.equal(typeof v,'boolean',k);if(p.pattern)assert.match(v,new RegExp(p.pattern));if(p.type==='array'){assert.ok(Array.isArray(v),k);if(p.items?.pattern)v.forEach(item=>assert.match(item,new RegExp(p.items.pattern)));if(p.items?.type==='string')v.forEach(item=>assert.equal(typeof item,'string'));}if(p.minItems)assert.ok(v.length>=p.minItems,k);}});
test('top-level schema',()=>{schema.required.forEach(k=>assert.ok(Object.hasOwn(candidateStore,k)));assert.equal(candidateStore.status,schema.properties.status.const);});
test('region is grounded',()=>candidate.likely_physical_zone_ids.forEach(z=>assert.ok(regions.regions.some(r=>r.id===z),z)));
test('site remains noncanonical',()=>assert.ok(!active.locations.some(l=>l.id.includes('AFTER-DARK'))));
test('no fabricated existing direct route',()=>assert.ok(!routes.routes.some(r=>JSON.stringify(r).includes('AFTER-DARK'))));
test('no asserted adjacency',()=>assert.equal(candidate.related_active_location_ids.length,0));
test('pre-modern technology candidate',()=>assert.equal(candidate.technology_translation,'FUNCTIONAL_ANALOGUE'));
test('canonical weather not inferred from generated concepts',()=>{const fx={weather:'RAIN',manifestation:null};assert.equal(deriveStage(fx).elNino,false);});
test('explicit El Nino requires evidence',()=>{assert.equal(deriveStage({weather:'RAIN',manifestation:{verified:true}}).elNino,true);assert.equal(deriveStage({weather:'RAIN',manifestation:{verified:false}}).elNino,false);});
test('rain and fog set appropriate effects',()=>{assert.equal(deriveStage({weather:'RAIN'}).crew,'protect_props');assert.equal(deriveStage({weather:'FOG'}).skyline,'occluded');});
test('severe weather holds production',()=>assert.equal(deriveStage({weather:'SEVERE'}).broadcast,'HOLD'));
test('flood does not invent damage',()=>assert.equal(deriveStage({weather:'FLOOD'}).structuralDamage,false));
test('state persistence without an approved delta',()=>{const a=nextState({scar:'REPAIRED_WITH_SCAR'},{approved:false,scar:'RESTORED'});assert.equal(a.scar,'REPAIRED_WITH_SCAR');});
test('state changes only with approved delta',()=>{const a=nextState({scar:'REPAIRED_WITH_SCAR'},{approved:true,scar:'RESTORED'});assert.equal(a.scar,'RESTORED');});
function deriveStage(f){return {elNino:f.manifestation?.verified===true,crew:f.weather==='RAIN'?'protect_props':'normal',skyline:f.weather==='FOG'?'occluded':'subject_to_visibility',broadcast:f.weather==='SEVERE'?'HOLD':'PROVISIONAL',structuralDamage:false};}
function nextState(s,d){return d.approved?{...s,scar:d.scar}:structuredClone(s);}
const failed=tests.filter(x=>x.status==='FAIL');console.log(JSON.stringify({suite:'after-dark-p2e',total:tests.length,passed:tests.length-failed.length,failed:failed.length,tests},null,2));if(failed.length)process.exitCode=1;
