import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {projectAtlas} from '../../src/observer-world.mjs';
import {spatialBindings} from '../spatial.mjs';
import {buildAtlasSiteAssets} from '../atlas-site-assets.mjs';

const source=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const bindings=spatialBindings({locations:projectAtlas(source.locations)}),original=JSON.stringify(bindings);
const id='LOC-CHILI-STABLE',name='Chili Stable open-slat fronts · candidate';
const build=()=>buildAtlasSiteAssets(THREE,bindings,()=>4);
const site=a=>a.locations.find(l=>l.id===id);
const fronts=a=>site(a)?.group.children.find(c=>c.name===name);
const centers=[-4,-1,2];

test('Chili stable remains source-bound, retains three landmarks, gold bars and actor-free enclosure',()=>{
 const record=source.locations.find(l=>l.id===id),a=build(),s=site(a),o=fronts(a);
 assert.equal(record.canon_status,'PERMANENT_CANON');
 assert.deepEqual(record.persistent_landmarks,['stable','pit smoke','Dark Horse enclosure']);
 assert.ok(s&&o);assert.equal(a.locations.length,20);assert.equal(a.water.length,4);
 assert.deepEqual(s.sourceLandmarks,record.persistent_landmarks);
 assert.equal(s.group.userData.locationId,id);assert.equal(s.group.userData.canonStatus,record.canon_status);
 assert.equal(s.group.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
 for(const key of record.persistent_landmarks)
  assert.ok(s.group.children.some(c=>c.userData.sourceLandmark===key));
 const bars=s.group.children.filter(c=>c.geometry?.type==='BoxGeometry'&&
  c.geometry.parameters.width===2.1&&c.geometry.parameters.height===.12&&c.geometry.parameters.depth===.1);
 assert.deepEqual(bars.map(o=>o.position.toArray()),centers.map(x=>[x,1.26,.35]));
 assert.ok(s.group.children.some(c=>c.name==='Dark Horse enclosure — no actor'));
 assert.equal(s.group.children.filter(c=>c.name===name).length,1);
 assert.equal(s.group.children.filter(c=>c.geometry?.type==='BoxGeometry'&&
  c.geometry.parameters.width===2.1&&c.geometry.parameters.height===1.7&&c.geometry.parameters.depth===.12).length,0);
 for(const other of a.locations.filter(l=>l.id!==id))
  assert.ok(!other.group.children.some(c=>c.name===name));
 assert.equal(a.worldMutationAllowed,false);assert.equal(a.weatherMutationAllowed,false);
 assert.deepEqual(a.principalCharacters,[]);assert.equal(JSON.stringify(bindings),original);
 a.dispose();
});

test('one indexed mesh models 27 separated slats in original three flat-panel envelopes',()=>{
 const a=build(),o=fronts(a),g=o.geometry,p=g.getAttribute('position'),c=g.getAttribute('color');
 assert.equal(g.type,'BufferGeometry');assert.ok(g.getIndex());
 assert.deepEqual(o.position.toArray(),[0,0,0]);assert.deepEqual(o.userData.bayCenters,centers);
 assert.equal(o.userData.slatsPerBay,9);assert.equal(o.material.vertexColors,true);
 assert.equal(p.count,264);assert.equal(c.count,p.count);assert.equal(g.getIndex().count,1188);
 let lo=Infinity,hi=-Infinity;const hit=new Set();
 for(let i=0;i<p.count;i++){
  const x=p.getX(i),y=p.getY(i),z=p.getZ(i);
  assert.ok([x,y,z].every(Number.isFinite));
  assert.ok(y>=.299999&&y<=2.000001&&z>=.189999&&z<=.310001);
  const bay=centers.findIndex(cx=>Math.abs(x-cx)<=1.050001);
  assert.notEqual(bay,-1);hit.add(bay);
  for(const v of [c.getX(i),c.getY(i),c.getZ(i)]){
   assert.ok(Number.isFinite(v)&&v>.12&&v<.45);lo=Math.min(lo,v);hi=Math.max(hi,v);
  }
 }
 assert.deepEqual([...hit].sort(),[0,1,2]);assert.ok(hi-lo>.19);
 const index=g.getIndex();
 const hasFaceAt=(x,y)=>{
  for(let i=0;i<index.count;i+=3){
   const ids=[index.getX(i),index.getX(i+1),index.getX(i+2)];
   const xs=ids.map(j=>p.getX(j)),ys=ids.map(j=>p.getY(j));
   if(Math.min(...xs)-1e-5<=x&&Math.max(...xs)+1e-5>=x&&
      Math.min(...ys)-1e-5<=y&&Math.max(...ys)+1e-5>=y)return true;
  }
  return false;
 };
 for(const cx of centers){
  for(let i=0;i<9;i++)assert.ok(hasFaceAt(cx+(i-4)*.235,1),'slat has physical faces');
  for(let i=0;i<8;i++)
   assert.equal(hasFaceAt(cx+(i-3.5)*.235,1),false,'between-slat opening remains genuinely empty');
 }
 const b=build(),other=fronts(b).geometry;
 assert.deepEqual(p.array,other.getAttribute('position').array);
 assert.deepEqual(c.array,other.getAttribute('color').array);
 assert.deepEqual(g.getIndex().array,other.getIndex().array);
 a.dispose();b.dispose();
});

test('El Niño global calm does not stop water; pause and owned mesh cleanup work once',()=>{
 const a=build(),o=fronts(a),snapshot=o.geometry.getAttribute('position').array.slice();
 a.tick(1.9,{globalCalm:true,storm:0});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===1.9));
 a.tick(4.6,{globalCalm:true,storm:0});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===4.6));
 a.tick(8,{paused:true,globalCalm:true,storm:8});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===4.6));
 assert.deepEqual(o.geometry.getAttribute('position').array,snapshot);
 let geos=0,mats=0;
 o.geometry.addEventListener('dispose',()=>geos++);
 o.material.addEventListener('dispose',()=>mats++);
 a.dispose();a.dispose();a.tick(11);
 assert.equal(geos,1);assert.equal(mats,1);
 assert.equal(JSON.stringify(bindings),original);
});
