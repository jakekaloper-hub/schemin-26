import test from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';

const bindings = [
  {id:'LOC-MUD-DOGS-SWAMP',anchor:[42,0,16],canonStatus:'PERMANENT_CANON'},
  {id:'LOC-COUNTRY-CLUB-JACKSON',anchor:[57,0,24],canonStatus:'PERMANENT_CANON'},
  {id:'LOC-TDS-WATERFALL-TEMPLE',anchor:[32,0,29],canonStatus:'PERMANENT_CANON'},
];

test('Wetland candidate sheen has bounded per-surface intensity with unchanged non-wetland shader policy',()=>{
  const before=JSON.stringify(bindings);
  const assets=buildRegionalAssets(THREE,bindings,()=>2);
  const swamp=assets.water.find(w=>w.kind==='swamp');
  const channel=assets.water.find(w=>w.kind==='channel');
  const pond=assets.water.find(w=>w.kind==='pond');
  assert.ok(swamp&&channel&&pond);
  for(const w of [swamp,channel]){
    assert.ok(w.material.uniforms.uSheenGain);
    assert.ok(w.material.uniforms.uSheenGain.value>0&&w.material.uniforms.uSheenGain.value<=.75);
    assert.match(w.material.fragmentShader,/uniform\s+float\s+uSheenGain\s*;/);
    assert.match(w.material.fragmentShader,/currentSheen\s*\*\s*uSheenGain/);
    assert.match(w.material.fragmentShader,/smoothstep\(/);
  }
  assert.ok(swamp.material.uniforms.uSheenGain.value<channel.material.uniforms.uSheenGain.value);
  assert.equal(pond.material.uniforms.uSheenGain.value,0);
  assets.tick(2,{storm:0});
  assert.equal(swamp.material.uniforms.uTime.value,2);
  assets.tick(9,{storm:0,paused:true});
  assert.equal(swamp.material.uniforms.uTime.value,2);
  assert.deepEqual(assets.principalCharacters,[]);
  assert.equal(assets.worldMutationAllowed,false);
  assert.equal(JSON.stringify(bindings),before);
  assets.dispose();
});
