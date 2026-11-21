import test from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';

const bindings=[
  {id:'LOC-COUNTRY-CLUB-JACKSON',anchor:[57,0,24],canonStatus:'PERMANENT_CANON',landmarks:['water hazards','clubhouse']},
  {id:'LOC-MUD-DOGS-SWAMP',anchor:[42,0,16],canonStatus:'PERMANENT_CANON',landmarks:['mud channels']},
  {id:'LOC-TDS-WATERFALL-TEMPLE',anchor:[32,0,29],canonStatus:'PERMANENT_CANON',landmarks:['waterfall']},
];
const build=(locations=bindings)=>buildRegionalAssets(THREE,locations,()=>2);

test('existing Country Club pond gets a separate subdued radial-ripple shader without new waterbody or boundary',()=>{
  const a=build(),pond=a.water.find(w=>w.kind==='pond');
  assert.ok(pond,'the existing pond mesh is retained');
  assert.equal(pond.material.uniforms.uPond.value,1);
  assert.equal(pond.material.uniforms.uWetland.value,0);
  assert.equal(pond.material.uniforms.uFlow.value.length(),0,'no invented pond current');
  assert.match(pond.material.fragmentShader,/else if\(uPond>\.5\)/);
  assert.match(pond.material.fragmentShader,/ripple\s*=\s*\(wave1\*\.6\+wave2\*\.4\)\*bank/);
  assert.match(pond.material.fragmentShader,/uTime\*2\.4/,'visible ripples evolve with the environmental clock');
  assert.equal(a.water.filter(w=>w.kind==='pond').length,1);
  assert.equal(pond.mesh.geometry.name,'Candidate Country Club pond surface');
  assert.equal(pond.mesh.geometry.getAttribute('position').count,321,'same 40-sided rim, tessellated interior');
  assert.equal(pond.mesh.material.transparent,true);
  a.dispose();
});

test('pond ripples advance during global calm and freeze on explicit pause',()=>{
  const a=build(),pond=a.water.find(w=>w.kind==='pond');
  a.tick(3,{storm:0});assert.equal(pond.material.uniforms.uTime.value,3);
  a.tick(5,{storm:0});assert.equal(pond.material.uniforms.uTime.value,5);
  a.tick(19,{storm:0,paused:true});assert.equal(pond.material.uniforms.uTime.value,5);
  assert.equal(a.water.filter(w=>w.kind!=='pond').every(w=>w.material.uniforms.uPond?.value===0||w.material.uniforms.uPond===undefined),true);
  a.dispose();
});

test('ripples remain presentation-only, isolated to the existing site and unchanged source Atlas',()=>{
  const snapshot=JSON.stringify(bindings),a=build();
  assert.deepEqual(a.locations.map(p=>p.id),bindings.map(p=>p.id));
  assert.equal(a.locations.find(p=>p.id==='LOC-COUNTRY-CLUB-JACKSON').group.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
  assert.equal(a.locations.find(p=>p.id==='LOC-COUNTRY-CLUB-JACKSON').group.userData.stateResolution,'UNRESOLVED_NOT_CURRENT_STATE');
  assert.equal(a.worldMutationAllowed,false);
  assert.deepEqual(a.principalCharacters,[]);
  const wet=a.water.filter(w=>['swamp','channel'].includes(w.kind));
  assert.ok(wet.every(w=>w.material.uniforms.uWetland.value===1));
  assert.ok(wet.every(w=>w.material.uniforms.uPond.value===0));
  assert.equal(JSON.stringify(bindings),snapshot);
  a.dispose();
});
