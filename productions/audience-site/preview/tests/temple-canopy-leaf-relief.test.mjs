import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';
import {batchStaticGeometry} from '../three-world.mjs';
const atlas=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const ids=['LOC-TDS-WATERFALL-TEMPLE','LOC-MUD-DOGS-SWAMP','LOC-COUNTRY-CLUB-JACKSON'];
const bindings=ids.map(id=>{
 const p=atlas.locations.find(x=>x.id===id);
 return {id,anchor:[p.abstract_position[0],0,p.abstract_position[1]],canonStatus:p.canon_status,landmarks:p.persistent_landmarks};
});
const stands=[[-10,-1,1.5],[-9,5,1.25],[-2,-6,1.4],[6,-4,1.5],[7,1,1.3],[6,6,1.1],[-2,7,.9]];
const build=()=>buildRegionalAssets(THREE,bindings,()=>2);
const temple=a=>a.locations.find(l=>l.id===ids[0]).group;
const crowns=a=>temple(a).children.filter(o=>o.userData.templeCanopyPart==='crown');
const near=(a,b)=>assert.ok(Math.abs(a-b)<1e-6, a+' != '+b);
test('21 existing Temple crowns have deterministic leaf-scale relief and light variation without expanding the candidate envelope',()=>{
 const before=JSON.stringify(bindings),a=build(),b=build(),base=new THREE.IcosahedronGeometry(1,2);
 try{
 assert.ok(bindings[0].landmarks.includes('dense vegetation'));
 const c=crowns(a),again=crowns(b),old=base.getAttribute('position');
 assert.equal(c.length,21);assert.equal(again.length,21);
 let changes=0,peak=0,tonalSpan=0;
 for(let i=0;i<c.length;i++){
  const o=c[i],[x,z,s]=stands[Math.floor(i/3)],j=i%3,angle=j*2.1+.3;
  const centre=[x+Math.cos(angle)*.65*s,3.05*s,z+Math.sin(angle)*.65*s];
  centre.forEach((v,k)=>near(o.position.getComponent(k),v));
  [1.1*s,.75*s,.95*s].forEach((v,k)=>near(o.scale.getComponent(k),v));
  [.19+centre[0]*.07,centre[2]*.16,.1].forEach((v,k)=>near(o.rotation.toArray()[k],v));
  assert.equal(o.userData.sourceLandmark,'dense vegetation');
  assert.equal(o.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
  assert.equal(o.userData.navigable,false);assert.deepEqual(o.userData.routeIds,[]);
  assert.equal(o.material.vertexColors,true);
  const p=o.geometry.getAttribute('position'),col=o.geometry.getAttribute('color'),n=o.geometry.getAttribute('normal');
  assert.equal(p.count,old.count);assert.equal(col.count,p.count);assert.equal(n.count,p.count);
  assert.deepEqual(p.array,again[i].geometry.getAttribute('position').array);
  assert.deepEqual(col.array,again[i].geometry.getAttribute('color').array);
  let lo=1,hi=0;
  for(let k=0;k<p.count;k++){
   const r=Math.hypot(old.getX(k),old.getY(k),old.getZ(k)),v=Math.hypot(p.getX(k),p.getY(k),p.getZ(k));
   assert.ok(v<=r+1e-6&&v>=r*.84-1e-6);
   const delta=r-v;peak=Math.max(peak,delta);if(delta>.04)changes++;
   for(const q of [col.getX(k),col.getY(k),col.getZ(k)]){assert.ok(q>=.52&&q<=1);lo=Math.min(lo,q);hi=Math.max(hi,q);}
   assert.ok([n.getX(k),n.getY(k),n.getZ(k)].every(Number.isFinite));
  }
  tonalSpan=Math.max(tonalSpan,hi-lo);
 }
 assert.ok(changes>200&&peak>.09);assert.ok(tonalSpan>.25);
 assert.equal(new Set(c.map(o=>o.material)).size,2);
 for(const other of a.locations.slice(1))assert.ok(!other.group.children.some(o=>o.userData.templeCanopyPart));
 assert.equal(JSON.stringify(bindings),before);assert.equal(a.worldMutationAllowed,false);
 assert.deepEqual(a.principalCharacters,[]);
 console.log(JSON.stringify({crowns:c.length,vertices:c.length*old.count,changes,peak,tonalSpan}));
 }finally{base.dispose();a.dispose();b.dispose();}
});
test('Temple crown materials retain opaque batching and color attributes; ordinary water and disposal remain independent',()=>{
 const a=build(),c=crowns(a);assert.equal(c.length,21);
 const mats=new Set(c.map(o=>o.material)),geo=c[0].geometry;let disposed=0;
 geo.addEventListener('dispose',()=>disposed++);
 const batch=batchStaticGeometry(THREE,temple(a));
 try{
 for(const m of mats){const objects=temple(a).children.filter(o=>o.material===m);assert.equal(objects.length,1);assert.ok(objects[0].geometry.getAttribute('color'));}
 a.tick(3,{globalCalm:true,storm:0});assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===3));
 a.tick(5,{globalCalm:true,paused:true});assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===3));
 }finally{for(const g of batch.geometries)g.dispose();a.dispose();a.dispose();}
 assert.equal(disposed,1);
});
