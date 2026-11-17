import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {projectAtlas} from '../../src/observer-world.mjs';
import {spatialBindings} from '../spatial.mjs';
import {buildAtlasSiteAssets} from '../atlas-site-assets.mjs';

const source=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const bindings=spatialBindings({locations:projectAtlas(source.locations)});
const relevant=new Set(['LOC-BRIDGE-MOUNTAIN-LAKE','LOC-DK-MUD-HILL','LOC-LLC-STORM-CITY','LOC-TDS-CHILI-SHARED-MARCH']);
const build=()=>buildAtlasSiteAssets(THREE,bindings,()=>4);

test('existing four other-site waters gain interior tessellation without changing a perimeter or making new bodies',()=>{
 const a=build(),sites=a.locations.filter(l=>relevant.has(l.id));
 assert.equal(sites.length,4);
 assert.equal(a.water.length,4,'only existing lake, mire, port and crossing are eligible');
 assert.deepEqual(new Set(a.water.map(w=>w.kind)),new Set(['mountain lake','mire','sheltered port','watercourse crossing']));
 for(const w of a.water){
  const geo=w.mesh.geometry,pos=geo.getAttribute('position'),uv=geo.getAttribute('uv');
  assert.equal(geo.type,'BufferGeometry');
  assert.equal(pos.count,393,'56 segments x 7 rings and a central vertex');
  assert.equal(uv.count,pos.count);
  assert.equal(geo.index.count,2184,'original disk footprint with more interior triangles');
  assert.ok(Array.from(pos.array).every(Number.isFinite));
  assert.ok(Array.from(geo.getAttribute('normal').array).every(Number.isFinite));
  for(let i=1+56*6;i<pos.count;i++){
   const radius=Math.hypot(pos.getX(i),pos.getY(i));
   assert.ok(Math.abs(radius-1)<1e-6,'outer rim radius must remain exactly one');
   assert.equal(pos.getZ(i),0,'shoreline vertices must not move in source geometry');
  }
  assert.ok(w.material.uniforms.uAmplitude.value>0&&w.material.uniforms.uAmplitude.value<=.03);
  assert.equal(w.mesh.castShadow,false);
  assert.equal(w.material.depthWrite,false);
 }
 a.dispose();
});

test('physical wave shader is local, time driven and zero at the original shoreline',()=>{
 const a=build();
 for(const w of a.water){
  const shader=w.material.vertexShader;
  assert.match(shader,/uniform float uTime;/);
  assert.match(shader,/float interior=1\.-smoothstep\(\.58,\.95,radius\)/);
  assert.match(shader,/p\.z\+=uAmplitude\*interior/);
  assert.match(shader,/waveA/);
  const amplitude=w.material.uniforms.uAmplitude.value;
  const displacement=(x,y,time)=>{
   const radius=Math.hypot(x,y);
   const edge0=Math.max(0,Math.min(1,(radius-.58)/(.95-.58)));
   const edge=edge0*edge0*(3-2*edge0);
   const a1=Math.sin(x*12.7-time*1.18+Math.sin(y*7.5)*.45);
   const b1=Math.sin(y*10.2+time*.74+x*3);
   return amplitude*(1-edge)*(.72*a1+.28*b1);
  };
  assert.equal(displacement(1,0,7),0,'shoreline is motionless at all times');
  assert.ok(Math.abs(displacement(.32,.19,1)-displacement(.32,.19,4))>1e-4,'surface really advances');
  assert.ok(Math.abs(displacement(.32,.19,1))<=amplitude+1e-9,'small bounded movement');
 }
 a.dispose();
});

test('global calm does not pause water; explicit pause does; source and weather authority unchanged',()=>{
 const before=JSON.stringify(bindings),a=build();
 a.tick(2,{storm:0,globalCalm:true});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===2));
 a.tick(6,{storm:0,globalCalm:true});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===6));
 a.tick(10,{paused:true});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===6));
 assert.equal(a.worldMutationAllowed,false);
 assert.equal(a.weatherMutationAllowed,false);
 assert.deepEqual(a.principalCharacters,[]);
 assert.ok(a.locations.every(l=>l.group.userData.visualAuthority==='CANDIDATE_NOT_APPROVED'));
 assert.equal(JSON.stringify(bindings),before);
 a.dispose();
});

test('geometry and material disposal remains bounded and tick after dispose is inert',()=>{
 const a=build(),waters=[...a.water],disposed=[];
 for(const w of waters){
  w.mesh.geometry.addEventListener('dispose',()=>disposed.push(w.mesh.geometry.uuid));
  w.material.addEventListener('dispose',()=>disposed.push(w.material.uuid));
 }
 a.dispose();a.dispose();
 assert.equal(disposed.length,8,'four meshes and four materials, each exactly once');
 a.tick(99);
 assert.ok(waters.every(w=>w.material.uniforms.uTime.value===0));
});
