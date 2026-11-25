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
const trunks=a=>temple(a).children.filter(o=>o.userData.templeCanopyPart==='trunk');
const near=(a,b)=>assert.ok(Math.abs(a-b)<1e-6,a+' != '+b);
test('existing seven Temple trunks gain bounded bark relief without moving their ends or stand anchors',()=>{
 const before=JSON.stringify(bindings),a=build(),b=build();
 try{
 const trees=trunks(a),again=trunks(b);assert.equal(trees.length,7);
 let changes=0,vertices=0,peak=0,span=0;
 for(let i=0;i<trees.length;i++){
  const o=trees[i],[x,z,s]=stands[i],h=2.5*s;
  [x,h/2,z].forEach((v,k)=>near(o.position.getComponent(k),v));
  assert.equal(o.userData.sourceLandmark,'dense vegetation');
  assert.equal(o.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
  assert.equal(o.userData.navigable,false);assert.deepEqual(o.userData.routeIds,[]);
  const g=o.geometry,p=g.getAttribute('position'),c=g.getAttribute('color'),n=g.getAttribute('normal');
  const base=new THREE.CylinderGeometry(.15*s,.30*s,h,24,12),old=base.getAttribute('position');
  try{
  assert.equal(p.count,old.count);assert.equal(c.count,p.count);
  assert.deepEqual(p.array,again[i].geometry.getAttribute('position').array);
  assert.deepEqual(c.array,again[i].geometry.getAttribute('color').array);
  let lo=1,hi=0;
  for(let k=0;k<p.count;k++){
   const r=Math.hypot(old.getX(k),old.getZ(k)),q=Math.hypot(p.getX(k),p.getZ(k));
   near(p.getY(k),old.getY(k));assert.ok(q<=r+1e-6&&q>=r*.83-1e-6);
   if(Math.abs(old.getY(k))>=h/2-1e-6){near(p.getX(k),old.getX(k));near(p.getZ(k),old.getZ(k));}
   const delta=r-q;peak=Math.max(peak,delta);if(delta>.01*s)changes++;
   for(const v of [c.getX(k),c.getY(k),c.getZ(k)]){assert.ok(v>=.48&&v<=1);lo=Math.min(lo,v);hi=Math.max(hi,v);}
   assert.ok([n.getX(k),n.getY(k),n.getZ(k)].every(Number.isFinite));vertices++;
  }
  // The cylinder UV seam has coincident positions and colors after sculpting.
  for(let row=0;row<=12;row++)for(let k=0;k<3;k++){
   near(p.array[(row*25)*3+k],p.array[(row*25+24)*3+k]);
   near(c.array[(row*25)*3+k],c.array[(row*25+24)*3+k]);
  }
  span=Math.max(span,hi-lo);
  }finally{base.dispose();}
 }
 assert.ok(changes>300&&peak>.025&&span>.25);
 assert.equal(new Set(trees.map(o=>o.material)).size,1);
 assert.equal(temple(a).children.filter(o=>o.userData.templeCanopyPart==='crown').length,21);
 for(const l of a.locations.slice(1))assert.ok(!l.group.children.some(o=>o.userData.templeCanopyPart==='trunk'));
 assert.equal(JSON.stringify(bindings),before);assert.equal(a.worldMutationAllowed,false);
 assert.deepEqual(a.principalCharacters,[]);
 console.log(JSON.stringify({trunks:trees.length,vertices,changes,peak,span}));
 }finally{a.dispose();b.dispose();}
});
test('bark geometry batches into one opaque material with vertex color and retains ordinary water and disposal',()=>{
 const a=build(),trees=trunks(a);assert.equal(trees.length,7);
 const m=trees[0].material,g=trees[0].geometry;let disposed=0;
 g.addEventListener('dispose',()=>disposed++);
 assert.equal(m.vertexColors,true);assert.equal(m.transparent,false);
 const batch=batchStaticGeometry(THREE,temple(a));
 try{
 const objects=temple(a).children.filter(o=>o.material===m);
 assert.equal(objects.length,1);assert.ok(objects[0].geometry.getAttribute('color'));
 a.tick(3,{globalCalm:true,storm:0});assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===3));
 a.tick(5,{globalCalm:true,paused:true});assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===3));
 }finally{for(const geo of batch.geometries)geo.dispose();a.dispose();a.dispose();}
 assert.equal(disposed,1);
});
