import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';

const atlas=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const ids=['LOC-TDS-WATERFALL-TEMPLE','LOC-MUD-DOGS-SWAMP','LOC-COUNTRY-CLUB-JACKSON'];
const bindings=ids.map(id=>{
 const source=atlas.locations.find(p=>p.id===id);
 assert.ok(source,'missing source-bound location '+id);
 return {id,anchor:[source.abstract_position[0],0,source.abstract_position[1]],
   canonStatus:source.canon_status,landmarks:source.persistent_landmarks};
});
const build=()=>buildRegionalAssets(THREE,bindings,()=>2);
const roofs=a=>a.locations.find(p=>p.id===ids[2]).group.children
 .filter(o=>o.userData?.estateRoofPart==='hip-course');
const expected=[
 [0,3.75,0,8.8,1.6,5.2],[-5,2.9,.1,2.7,1.1,4.2],
 [5,2.9,.1,2.7,1.1,4.2],[0,3.275,3.1,9.6,.75,2.7]
];
const approx=(a,b,epsilon=1e-5)=>assert.ok(Math.abs(a-b)<=epsilon,`expected ${a} ≈ ${b}`);

test('all four inherited Jackson roofs preserve exact transforms, original square-pyramid envelope and shared batch material',()=>{
 const original=JSON.stringify(bindings),snapshot=JSON.stringify(atlas),a=build(),list=roofs(a);
 assert.equal(list.length,4);
 assert.deepEqual(a.locations.map(l=>l.id),ids);
 assert.equal(new Set(list.map(o=>o.material.uuid)).size,1);
 assert.ok(a.locations.find(l=>l.id===ids[2]).group.children.some(
   o=>o!==list[0]&&o.material===list[0].material),'no new roof material or draw slot');
 for(let i=0;i<list.length;i++){
   const o=list[i],[x,y,z,w,h,d]=expected[i];
   o.position.toArray().forEach((coordinate,axis)=>approx(coordinate,[x,y,z][axis]));
   assert.deepEqual(o.scale.toArray(),[w/Math.SQRT2,1,d/Math.SQRT2]);
   assert.deepEqual(o.userData.originalRoofDimensions,[w,h,d]);
   assert.equal(o.userData.originalRoofIndex,i);
   assert.equal(o.userData.sourceLandmark,'clubhouse');
   assert.equal(o.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
   assert.deepEqual(o.userData.routeIds,[]);
   assert.equal(o.userData.navigable,false);
   assert.deepEqual(o.userData.principalCharacters,[]);
   assert.equal(o.geometry.name,'Candidate Jackson recessed hip-roof courses');
   const pos=o.geometry.getAttribute('position');
   assert.ok(pos.count>200,'four original surfaces have tessellated grooves');
   let maxInset=0,baseCount=0;
   for(let j=0;j<pos.count;j++){
     const px=pos.getX(j),py=pos.getY(j),pz=pos.getZ(j);
     assert.ok([px,py,pz].every(Number.isFinite));
     const span=(h/2-py)/h;
     assert.ok(span>=-1e-5&&span<=1+1e-5);
     // Original rotated four-sided cone has a square local envelope.
     assert.ok(Math.abs(px)<=span/Math.SQRT2+1e-5);
     assert.ok(Math.abs(pz)<=span/Math.SQRT2+1e-5);
     if(Math.hypot(px,pz)<1e-8||span<1e-5)continue;
     const ratio=Math.max(Math.abs(px),Math.abs(pz))/(span/Math.SQRT2);
     assert.ok(ratio<=1.00002&&ratio>=.962,'inward-only, never visibly enlarged');
     if(span>.08&&span<.92)maxInset=Math.max(maxInset,1-ratio);
     if(span>.99999){baseCount++;approx(ratio,1,2e-5);}
   }
   assert.ok(baseCount>=32,'original square eaves remain untouched');
   assert.ok(maxInset>.02&&maxInset<.04,'actual visible but bounded recessed courses');
   const normals=pos.count===o.geometry.getAttribute('normal').count
     ?o.geometry.getAttribute('normal'):null;
   assert.ok(normals);
   assert.ok([...normals.array].every(Number.isFinite));
   assert.ok(o.geometry.boundingSphere.radius>0);
 }
 assert.equal(a.worldMutationAllowed,false);assert.deepEqual(a.principalCharacters,[]);
 assert.equal(JSON.stringify(bindings),original);
 assert.equal(JSON.stringify(atlas),snapshot);
 a.dispose();
});

test('roof relief is deterministic, Jackson-only, and cannot resolve Week 3 contamination',()=>{
 const a=build(),b=build(),aa=roofs(a),bb=roofs(b);
 assert.equal(aa.length,bb.length);
 for(let i=0;i<aa.length;i++)assert.deepEqual(
  aa[i].geometry.getAttribute('position').array,bb[i].geometry.getAttribute('position').array);
 for(const loc of a.locations.filter(l=>l.id!==ids[2]))
  assert.equal(loc.group.children.filter(o=>o.userData?.estateRoofPart).length,0);
 const club=a.locations.find(l=>l.id===ids[2]).group;
 assert.equal(club.userData.stateResolution,'UNRESOLVED_NOT_CURRENT_STATE');
 const source=atlas.locations.find(p=>p.id===ids[2]);
 assert.equal(source.canon_status,'PERMANENT_CANON');
 assert.ok(source.current_state.some(t=>t.includes('chili contamination')));
 assert.ok(source.current_state.some(t=>t.includes('cleanup state')));
 a.dispose();b.dispose();
});

test('El Nino global calm keeps ordinary waterfall, river, swamp and pond moving; pause and disposal are idempotent',()=>{
 const original=JSON.stringify(bindings),a=build(),rs=roofs(a),waters=a.water.filter(w=>
   ['waterfall','river','pool','swamp','channel','pond'].includes(w.kind));
 assert.equal(waters.length,6);
 let roofDisposals=0,materialDisposals=0;
 rs[0].geometry.addEventListener('dispose',()=>roofDisposals++);
 rs[0].material.addEventListener('dispose',()=>materialDisposals++);
 a.tick(2,{globalCalm:true,storm:0});assert.ok(waters.every(w=>w.material.uniforms.uTime.value===2));
 a.tick(7,{globalCalm:true,storm:0});assert.ok(waters.every(w=>w.material.uniforms.uTime.value===7));
 a.tick(19,{globalCalm:true,storm:6,paused:true});
 assert.ok(waters.every(w=>w.material.uniforms.uTime.value===7));
 a.tick(22,{globalCalm:true,storm:0});assert.ok(waters.every(w=>w.material.uniforms.uTime.value===22));
 a.dispose();a.dispose();a.tick(28);
 assert.equal(roofDisposals,1);assert.equal(materialDisposals,1);
 assert.equal(JSON.stringify(bindings),original);
});

test('each Jackson hip ridge keeps distinct face normals at identical positions and UVs',()=>{
 const a=build();
 try{
  for(const roof of roofs(a)){
   const geo=roof.geometry,p=geo.getAttribute('position'),n=geo.getAttribute('normal'),uv=geo.getAttribute('uv');
   assert.equal(geo.index.count,4608,'no additional triangles');
   for(const row of [6,12,18])for(const column of [0,8,16,24]){
    const i=row*33+column,corner=new THREE.Vector3().fromBufferAttribute(p,i);
    const coincident=[];
    for(let j=0;j<p.count;j++)if(corner.distanceTo(new THREE.Vector3().fromBufferAttribute(p,j))<1e-6)coincident.push(j);
    assert.equal(coincident.length,2,`two face vertices at row ${row} column ${column}`);
    const [left,right]=coincident;
    const nl=new THREE.Vector3().fromBufferAttribute(n,left),nr=new THREE.Vector3().fromBufferAttribute(n,right);
    assert.ok(nl.dot(nr)<.80,`distinct ridge normals at row ${row} column ${column}`);
    approx(nl.length(),1);approx(nr.length(),1);
    if(column!==0){approx(uv.getX(left),uv.getX(right));approx(uv.getY(left),uv.getY(right));}
   }
  }
 }finally{a.dispose();}
});
