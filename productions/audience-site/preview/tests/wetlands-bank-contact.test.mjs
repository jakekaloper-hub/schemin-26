import test from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';

const bindings=[
  {id:'LOC-MUD-DOGS-SWAMP',anchor:[42,0,16],canonStatus:'PERMANENT_CANON'},
  {id:'LOC-TDS-WATERFALL-TEMPLE',anchor:[32,0,29],canonStatus:'PERMANENT_CANON'},
  {id:'LOC-COUNTRY-CLUB-JACKSON',anchor:[57,0,24],canonStatus:'PERMANENT_CANON'}
];
const build=()=>buildRegionalAssets(THREE,bindings,()=>2);

test('Candidate bank-contact treatment is confined to existing wetland surfaces, not Temple or pond',()=>{
  const before=JSON.stringify(bindings),a=build();
  const swamp=a.water.find(w=>w.kind==='swamp');
  const channel=a.water.find(w=>w.kind==='channel');
  assert.ok(swamp&&channel);
  assert.equal(swamp.material.uniforms.uBankContact.value,.76);
  assert.equal(channel.material.uniforms.uBankContact.value,.42);
  assert.ok(a.water.filter(w=>!['swamp','channel'].includes(w.kind))
    .every(w=>w.material.uniforms.uBankContact.value===0));
  for(const w of [swamp,channel]){
    assert.equal(w.mesh.geometry.getAttribute('position').count,385);
    assert.equal(w.mesh.geometry.index.count,2160);
    assert.equal(w.material.depthWrite,false);
  }
  assert.equal(a.worldMutationAllowed,false);
  assert.deepEqual(a.principalCharacters,[]);
  assert.equal(JSON.stringify(bindings),before);
  a.dispose();
});

test('Near-bank wave contact uses a broken moving mask, leaves the existing footprint rim unchanged',()=>{
  const a=build(),swamp=a.water.find(w=>w.kind==='swamp');
  const shader=swamp.material.fragmentShader;
  assert.match(shader,/uniform float uBankContact/);
  assert.match(shader,/bankCrest=1\.-smoothstep\(\.0,\.022,abs\(bankRadius-/);
  assert.match(shader,/bankBreakup=/);
  assert.match(shader,/bankAngle\*13\.\+uTime\*\.63/);
  assert.match(shader,/bankMask=smoothstep\(\.73,\.84,bankRadius\)/);
  assert.match(shader,/1\.-smoothstep\(\.965,1\.,bankRadius\)/);
  assert.match(shader,/contactLight=.*uBankContact/);
  assert.match(shader,/contactTint\+lowSheen\+quietEddy\+rootSheen\+contactLight/);
  assert.doesNotMatch(shader,/storm|weather/i);
  assert.match(swamp.material.vertexShader,/shoreHold=1\.-smoothstep\(\.65,\.96/);
  assert.equal(swamp.mesh.geometry.getAttribute('position').count,385);
  a.dispose();
});

test('Bank lap keeps ordinary environmental time under global calm, stops only on explicit pause',()=>{
  const original=JSON.stringify(bindings),a=build();
  const wet=a.water.filter(w=>['swamp','channel'].includes(w.kind));
  a.tick(3,{storm:0});
  assert.deepEqual(wet.map(w=>w.material.uniforms.uTime.value),[3,3]);
  a.tick(8,{storm:0});
  assert.deepEqual(wet.map(w=>w.material.uniforms.uTime.value),[8,8]);
  a.tick(17,{storm:0,paused:true});
  assert.deepEqual(wet.map(w=>w.material.uniforms.uTime.value),[8,8]);
  a.tick(19,{storm:0});
  assert.deepEqual(wet.map(w=>w.material.uniforms.uTime.value),[19,19]);
  assert.deepEqual(a.locations.map(l=>l.id),bindings.map(l=>l.id));
  assert.equal(JSON.stringify(bindings),original);
  a.dispose();
});
