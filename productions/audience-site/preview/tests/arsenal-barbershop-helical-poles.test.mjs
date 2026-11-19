import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {projectAtlas} from '../../src/observer-world.mjs';
import {spatialBindings} from '../spatial.mjs';
import {buildAtlasSiteAssets} from '../atlas-site-assets.mjs';

const source=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const bindings=spatialBindings({locations:projectAtlas(source.locations)}),original=JSON.stringify(bindings);
const id='LOC-ARSENAL-BARBERSHOP';
const build=()=>buildAtlasSiteAssets(THREE,bindings,()=>4);
const site=a=>a.locations.find(l=>l.id===id);
const helix=a=>site(a)?.group.children.find(o=>o.name==='Arsenal barber-pole helical bands · candidate');

test('source-exact Arsenal site, landmarks and both ivory cores remain intact',()=>{
 const record=source.locations.find(l=>l.id===id);
 assert.equal(record.canon_status,'PERMANENT_CANON');
 assert.deepEqual(record.persistent_landmarks,['barber chair','Arsenal-red owner history']);
 const a=build(),s=site(a),h=helix(a);
 assert.ok(s&&h);assert.equal(a.locations.length,20);assert.equal(a.water.length,4);
 assert.deepEqual(s.sourceLandmarks,record.persistent_landmarks);
 assert.equal(s.group.userData.locationId,id);
 assert.equal(s.group.userData.canonStatus,record.canon_status);
 assert.equal(s.group.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
 assert.ok(s.group.children.some(o=>o.name==='Barber chair'&&o.userData.sourceLandmark==='barber chair'));
 assert.ok(s.group.children.some(o=>o.userData.sourceLandmark==='Arsenal-red owner history'));
 assert.ok(s.group.children.some(o=>o.name==='Pitched roof candidate'));
 const poles=s.group.children.filter(o=>o.name==='Shop stripe');
 assert.equal(poles.length,2);
 for(let i=0;i<2;i++){
  assert.deepEqual(poles[i].position.toArray(),[[-2.2,1.35,3],[2.2,1.35,3]][i]);
  assert.equal(poles[i].geometry.parameters.height,2);
  assert.equal(poles[i].geometry.parameters.radiusTop,.1);
  assert.equal(poles[i].geometry.parameters.radiusBottom,.1);
 }
 assert.equal(s.group.children.filter(o=>o.name==='Arsenal barber-pole helical bands · candidate').length,1);
 assert.equal(s.group.children.filter(o=>o.name==='').filter(o=>o.geometry?.type==='CylinderGeometry'&&o.geometry.parameters?.radiusTop===.115).length,0);
 for(const other of a.locations.filter(l=>l.id!==id))assert.equal(other.group.children.some(o=>o.name===h.name),false);
 assert.equal(a.worldMutationAllowed,false);assert.equal(a.weatherMutationAllowed,false);
 assert.deepEqual(a.principalCharacters,[]);assert.equal(JSON.stringify(bindings),original);
 a.dispose();
});

test('one indexed double-sided physical stripe wraps five turns around each existing core deterministically',()=>{
 const a=build(),o=helix(a),geo=o.geometry,p=geo.getAttribute('position'),c=geo.getAttribute('color'),n=geo.getAttribute('normal');
 assert.equal(geo.type,'BufferGeometry');
 assert.equal(p.count,404);assert.equal(geo.getIndex().count,1200);
 assert.equal(c.count,p.count);assert.equal(n.count,p.count);
 assert.equal(o.material.vertexColors,true);assert.equal(o.material.side,THREE.DoubleSide);
 assert.deepEqual(o.position.toArray(),[0,0,0]);
 let lo=1,hi=0;const turns=[];
 for(let pole=0;pole<2;pole++){
  const x0=[-2.2,2.2][pole],offset=pole*202;
  let last=null,total=0;
  for(let i=0;i<=100;i++){
   const j=offset+2*i;
   const x=p.getX(j),z=p.getZ(j);
   const angle=Math.atan2(z-3,x-x0);
   if(last!==null){
    let delta=angle-last;
    if(delta< -Math.PI)delta+=2*Math.PI;
    if(delta> Math.PI)delta-=2*Math.PI;
    assert.ok(delta>.25&&delta<.38);
    total+=delta;
   }
   last=angle;
  }
  turns.push(total/(2*Math.PI));
 }
 for(let i=0;i<p.count;i++){
  const x=p.getX(i),y=p.getY(i),z=p.getZ(i);
  const center=i<202?-2.2:2.2;
  assert.ok([x,y,z].every(Number.isFinite));
  assert.ok(Math.abs(Math.hypot(x-center,z-3)-.119)<.00001);
  assert.ok(y>=.35&&y<=2.35);
  for(const value of [c.getX(i),c.getY(i),c.getZ(i)]){
   assert.ok(Number.isFinite(value)&&value>.09&&value<.7);
   lo=Math.min(lo,value);hi=Math.max(hi,value);
  }
 }
 assert.ok(turns.every(t=>Math.abs(t-5)<.00001));
 assert.ok(hi-lo>.5);
 const b=build(),h=helix(b);
 assert.deepEqual(p.array,h.geometry.getAttribute('position').array);
 assert.deepEqual(c.array,h.geometry.getAttribute('color').array);
 assert.deepEqual(geo.getIndex().array,h.geometry.getIndex().array);
 a.dispose();b.dispose();
});

test('global El Niño calm cannot stop ordinary water; pause and owned disposal are distinct',()=>{
 const a=build(),h=helix(a),originalGeometry=h.geometry.getAttribute('position').array.slice();
 a.tick(1.7,{globalCalm:true,storm:0});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===1.7));
 a.tick(4.3,{globalCalm:true,storm:0});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===4.3));
 a.tick(10,{paused:true,globalCalm:true,storm:8});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===4.3));
 assert.deepEqual(h.geometry.getAttribute('position').array,originalGeometry);
 let gDisposed=0,mDisposed=0;
 h.geometry.addEventListener('dispose',()=>gDisposed++);
 h.material.addEventListener('dispose',()=>mDisposed++);
 a.dispose();a.dispose();a.tick(20);
 assert.equal(gDisposed,1);assert.equal(mDisposed,1);
 assert.equal(JSON.stringify(bindings),original);
});
