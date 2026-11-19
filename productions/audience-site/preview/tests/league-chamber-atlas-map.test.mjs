import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {projectAtlas} from '../../src/observer-world.mjs';
import {spatialBindings} from '../spatial.mjs';
import {buildAtlasSiteAssets} from '../atlas-site-assets.mjs';

const source=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const bindings=spatialBindings({locations:projectAtlas(source.locations)});
const snapshot=JSON.stringify(bindings);
const id='LOC-LEAGUE-CHAMBER',build=(b=bindings)=>buildAtlasSiteAssets(THREE,b,()=>4);
function wall(a){
 const site=a.locations.find(l=>l.id===id);
 assert.ok(site,'League Chamber scene exists');
 const landmark=site.group.children.find(o=>o.name==='Map wall');
 const marks=site.group.children.find(o=>o.name==='Unlettered source Atlas map marks');
 assert.ok(landmark&&marks,'map landmark has source-exact markings');
 return {site,landmark,marks};
}
test('source League Chamber wall shows all 23 established places without inventing routes or sites',()=>{
 const a=build(),{site,landmark,marks}=wall(a);
 assert.equal(source.locations.length,23);assert.equal(a.locations.length,20);
 assert.deepEqual(site.sourceLandmarks,bindings.find(b=>b.id===id).landmarks);
 assert.equal(landmark.userData.sourceLandmark,'map wall');
 assert.equal(marks.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
 assert.equal(marks.userData.sourcePath,'world/data/locations.json');
 assert.deepEqual(marks.userData.mappedLocationIds,bindings.map(b=>b.id));
 assert.equal(marks.geometry.getAttribute('position').count,source.locations.length*6);
 assert.equal(marks.material.isMeshStandardMaterial,true);
 assert.equal(marks.castShadow,false);assert.equal(marks.receiveShadow,false);
 assert.equal(a.worldMutationAllowed,false);assert.equal(a.weatherMutationAllowed,false);
 assert.deepEqual(a.principalCharacters,[]);assert.equal(JSON.stringify(bindings),snapshot);a.dispose();
});
test('unlettered symbols project source anchor coordinates and stay independent of visit flags',()=>{
 const a=build(),positions=wall(a).marks.geometry.getAttribute('position');
 const xs=bindings.map(b=>b.anchor[0]),zs=bindings.map(b=>b.anchor[2]);
 const loX=Math.min(...xs),hiX=Math.max(...xs),loZ=Math.min(...zs),hiZ=Math.max(...zs);
 for(let i=0;i<bindings.length;i++){
  const p=Array.from({length:6},(_,j)=>[positions.getX(i*6+j),positions.getY(i*6+j),positions.getZ(i*6+j)]);
  const center=[0,1,2].map(k=>p.reduce((sum,v)=>sum+v[k],0)/6);
  assert.ok(Math.abs(center[0]-4.08*((bindings[i].anchor[0]-loX)/(hiX-loX||1)-.5))<1e-5,bindings[i].id+' east');
  assert.ok(Math.abs(center[1]-1.9+1.30*((bindings[i].anchor[2]-loZ)/(hiZ-loZ||1)-.5))<1e-5,bindings[i].id+' north');
  assert.ok(Math.abs(center[2]+2.565)<1e-5);
  assert.ok(p.every(v=>Math.abs(v[0])<=2.10&&v[1]>=1.20&&v[1]<=2.60));
  assert.ok(wall(a).marks.geometry.getAttribute('normal').getZ(i*6)>.99);
 }
 const hidden=build(bindings.map(b=>({...b,visible:false,visited:false})));
 assert.deepEqual(Array.from(wall(hidden).marks.geometry.getAttribute('position').array),Array.from(positions.array));
 const replay=build();assert.deepEqual(Array.from(wall(replay).marks.geometry.getAttribute('position').array),Array.from(positions.array));
 assert.equal(JSON.stringify(bindings),snapshot);a.dispose();hidden.dispose();replay.dispose();
});
test('one static batchable map retains El Niño calm-water motion, explicit pause, and single disposal',()=>{
 const a=build(),marks=wall(a).marks;
 assert.equal(a.water.length,4);assert.equal(marks.material.uniforms,undefined);
 a.tick(2.2,{globalCalm:true,storm:0});assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===2.2));
 a.tick(4.7,{globalCalm:true,storm:0});assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===4.7));
 a.tick(20,{paused:true,storm:8});assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===4.7));
 let geom=0,mat=0;marks.geometry.addEventListener('dispose',()=>geom++);
 marks.material.addEventListener('dispose',()=>mat++);
 a.dispose();a.dispose();a.tick(30);
 assert.equal(geom,1);assert.equal(mat,1);assert.equal(JSON.stringify(bindings),snapshot);
});
