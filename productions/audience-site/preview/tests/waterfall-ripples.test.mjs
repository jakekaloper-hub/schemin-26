import test from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';
const source=[{id:'LOC-TDS-WATERFALL-TEMPLE',anchor:[10,0,20],canonStatus:'PERMANENT_CANON'}];
const create=()=>buildRegionalAssets(THREE,source,()=>1);

test('waterfall has four independently phased shader-driven landing ripples',()=>{
  const a=create();const rings=a.water.filter(w=>w.kind==='landing-ripple');
  assert.equal(rings.length,4);
  assert.equal(new Set(rings.map(r=>r.material.uniforms.uPhase.value)).size,4);
  assert.ok(rings.every(r=>r.mesh.material.isShaderMaterial&&r.mesh.geometry.type==='RingGeometry'));
  assert.ok(rings.every(r=>r.mesh.castShadow===false));
  a.dispose();
});
test('landing ripples advance in global calm but hold under pause',()=>{
  const a=create();const rings=a.water.filter(w=>w.kind==='landing-ripple');assert.equal(rings.length,4);
  a.tick(2,{storm:0});assert.ok(rings.every(w=>w.material.uniforms.uTime.value===2));
  a.tick(4,{storm:0});assert.ok(rings.every(w=>w.material.uniforms.uTime.value===4));
  a.tick(16,{paused:true});assert.ok(rings.every(w=>w.material.uniforms.uTime.value===4));
  a.dispose();
});
test('ripple candidates neither write the world nor generate unnamed new locations',()=>{
  const before=JSON.stringify(source),a=create();
  assert.deepEqual(a.locations.map(l=>l.id),['LOC-TDS-WATERFALL-TEMPLE']);
  assert.equal(a.worldMutationAllowed,false);
  assert.deepEqual(a.principalCharacters,[]);
  assert.equal(JSON.stringify(source),before);
  a.dispose();a.dispose();
});
