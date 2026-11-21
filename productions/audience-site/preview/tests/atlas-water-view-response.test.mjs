import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {projectAtlas} from '../../src/observer-world.mjs';
import {spatialBindings} from '../spatial.mjs';
import {buildAtlasSiteAssets} from '../atlas-site-assets.mjs';

const source=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const bindings=spatialBindings({locations:projectAtlas(source.locations)});
const build=()=>buildAtlasSiteAssets(THREE,bindings,()=>4);
const gains=new Map([
 ['mountain lake',.52],['mire',.12],['sheltered port',.42],['watercourse crossing',.24]
]);

test('only four inherited water bodies receive their own bounded view-response gain',()=>{
 const original=JSON.stringify(bindings),a=build();
 assert.equal(a.locations.length,20);
 assert.equal(a.water.length,4);
 assert.deepEqual(new Set(a.water.map(w=>w.kind)),new Set(gains.keys()));
 for(const {mesh,material,kind} of a.water){
  assert.equal(material.uniforms.uViewSheen.value,gains.get(kind));
  assert.ok(material.uniforms.uViewSheen.value>=0&&material.uniforms.uViewSheen.value<=.52);
  assert.equal(material.transparent,true);
  assert.equal(material.depthWrite,false);
  assert.equal(mesh.geometry.getAttribute('position').count,393);
  assert.equal(mesh.geometry.index.count,2184);
  for(let i=337;i<393;i++)assert.ok(Math.abs(Math.hypot(mesh.geometry.getAttribute('position').getX(i),mesh.geometry.getAttribute('position').getY(i))-1)<1e-6);
 }
 assert.equal(JSON.stringify(bindings),original);
 assert.equal(a.worldMutationAllowed,false);
 assert.equal(a.weatherMutationAllowed,false);
 assert.ok(a.locations.every(l=>l.group.userData.visualAuthority==='CANDIDATE_NOT_APPROVED'));
 a.dispose();
});

test('existing displaced geometry drives the camera-dependent shader without extra render layers',()=>{
 const a=build();
 for(const {mesh,material} of a.water){
  const vertex=material.vertexShader,fragment=material.fragmentShader;
  assert.match(vertex,/p\.z\+=uAmplitude\*interior/);
  assert.match(vertex,/vWorld=\(modelMatrix\*vec4\(p,1\.\)\)\.xyz/);
  assert.match(fragment,/cross\(dFdx\(vWorld\),dFdy\(vWorld\)\)/);
  assert.match(fragment,/cameraPosition-vWorld/);
  assert.match(fragment,/uViewSheen\*grazing/);
  assert.match(fragment,/clamp\(uColor\+vec3\(\.09,\.15,\.14\)\*line\*gap\+viewTint,0\.,1\.\)/);
  assert.match(fragment,/gl_FragColor=vec4\(c,\.87\*edge\)/);
  assert.equal(mesh.material,material);
  assert.equal(mesh.children.length,0);
 }
 a.dispose();
});

test('numerical view response is finite, low-amplitude, and distinguishes overhead from grazing views',()=>{
 const a=build();
 function shine(gain,eye){
  const len=Math.hypot(...eye),cos=Math.abs(eye[1]/len);
  const grazing=(1-Math.min(1,Math.max(0,cos)))**2;
  return [.10,.16,.15].map(c=>c*gain*grazing);
 }
 for(const {material} of a.water){
  const gain=material.uniforms.uViewSheen.value;
  const top=shine(gain,[0,1,0]),oblique=shine(gain,[1,.25,0]),level=shine(gain,[1,.01,0]);
  for(const i of [0,1,2]){
   assert.equal(top[i],0);
   assert.ok(Number.isFinite(oblique[i])&&oblique[i]>top[i]&&oblique[i]<level[i]);
   assert.ok(level[i]<=.16*.52+1e-9,'bounded fraction of display gamut');
  }
 }
 a.tick(2,{storm:0,globalCalm:true});
 a.tick(3.5,{storm:0,globalCalm:true});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===3.5));
 a.tick(50,{paused:true});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===3.5));
 a.dispose();
});
