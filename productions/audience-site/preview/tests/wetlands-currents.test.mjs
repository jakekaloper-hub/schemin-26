import test from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';
const bindings=[
 {id:'LOC-MUD-DOGS-SWAMP',anchor:[42,0,16],canonStatus:'PERMANENT_CANON',landmarks:['mud channels','raised ground']},
 {id:'LOC-COUNTRY-CLUB-JACKSON',anchor:[57,0,24],canonStatus:'PERMANENT_CANON',landmarks:['clubhouse','golf grounds','water hazards']},
 {id:'LOC-TDS-WATERFALL-TEMPLE',anchor:[31,0,51],canonStatus:'PERMANENT_CANON',landmarks:['waterfall']},
];
const build=()=>buildRegionalAssets(THREE,bindings,()=>3);
test('Wetland swamp and channel have nonzero candidate currents, unlike estate pond',()=>{
 const a=build(),wet=a.water.filter(x=>['swamp','channel'].includes(x.kind));
 assert.equal(wet.length,2);
 for(const w of wet){assert.equal(w.material.uniforms.uWetland.value,1);assert.ok(w.material.uniforms.uFlow.value instanceof THREE.Vector2);assert.ok(w.material.uniforms.uFlow.value.length()>0);
 assert.match(w.material.fragmentShader,/wetlandUv\s*=\s*vUv\s*\+\s*uFlow\s*\*\s*uTime/);}
 const pond=a.water.find(x=>x.kind==='pond');assert.equal(pond.material.uniforms.uWetland.value,0);assert.equal(pond.material.uniforms.uFlow.value.length(),0);a.dispose();
});
test('Calm permits currents and pause holds their phase',()=>{
 const a=build(),wet=a.water.filter(x=>['swamp','channel'].includes(x.kind));
 a.tick(11,{storm:0});assert.deepEqual(wet.map(x=>x.material.uniforms.uTime.value),[11,11]);
 a.tick(30,{storm:0,paused:true});assert.deepEqual(wet.map(x=>x.material.uniforms.uTime.value),[11,11]);
 a.tick(30,{storm:0});assert.deepEqual(wet.map(x=>x.material.uniforms.uTime.value),[30,30]);a.dispose();
});
test('Only presentation-only wetland shader adds ribbons and eddies; source unchanged',()=>{
 const before=JSON.stringify(bindings),a=build(),w=a.water.find(x=>x.kind==='swamp');
 assert.match(w.material.fragmentShader,/uWetland\s*>\s*\.5/);assert.match(w.material.fragmentShader,/currentSheen/);assert.match(w.material.fragmentShader,/sediment/);
 assert.doesNotMatch(w.material.fragmentShader,/storm|weather/i);assert.equal(a.worldMutationAllowed,false);
 assert.deepEqual(a.principalCharacters,[]);assert.equal(JSON.stringify(bindings),before);
 assert.equal(a.locations[0].group.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');a.dispose();
});
