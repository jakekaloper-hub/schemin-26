import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';

const atlas=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const ids=['LOC-COUNTRY-CLUB-JACKSON','LOC-TDS-WATERFALL-TEMPLE','LOC-MUD-DOGS-SWAMP'];
const bindings=ids.map(id=>{const s=atlas.locations.find(p=>p.id===id);return {id,anchor:[s.abstract_position[0],0,s.abstract_position[1]],canonStatus:s.canon_status,landmarks:s.persistent_landmarks};});
const build=()=>buildRegionalAssets(THREE,bindings,()=>2);
const bridge=a=>a.locations[0].group.getObjectByName('Candidate Week 9 pond-side stone arch');
const near=(a,b)=>assert.ok(Math.abs(a-b)<1e-6,a+' != '+b);
const parts=a=>bridge(a).children.filter(o=>o.userData.bridgePart==='baluster'||o.userData.bridgePart==='coping');
test('existing Jackson balustrade receives only bounded relief; all original objects and footprints remain',()=>{
 const a=build(),b=build(),source=JSON.stringify(bindings);
 try{
 const objects=parts(a),repeat=parts(b);
 assert.equal(bridge(a).children.length,17);
 assert.equal(objects.length,14);
 assert.equal(objects.filter(o=>o.userData.bridgePart==='baluster').length,10);
 assert.equal(objects.filter(o=>o.userData.bridgePart==='coping').length,4);
 let recessed=0;
 for(let i=0;i<objects.length;i++){
  const o=objects[i],p=o.geometry.getAttribute('position'),c=o.geometry.getAttribute('color'),n=o.geometry.getAttribute('normal');
  assert.equal(o.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
  assert.equal(o.userData.navigable,false);assert.deepEqual(o.userData.routeIds,[]);
  assert.equal(o.material.vertexColors,true);
  assert.equal(o.material.transparent,false);
  assert.equal(c.count,p.count);assert.equal(n.count,p.count);
  assert.deepEqual(p.array,repeat[i].geometry.getAttribute('position').array);
  assert.deepEqual(c.array,repeat[i].geometry.getAttribute('color').array);
  const side=i<7?-.81:.78,slot=i%7;
  near(o.position.x,side);
  if(slot>0&&slot<6){
   near(o.position.y,1.89);near(o.position.z,[-2.26,-1.13,0,1.13,2.26][slot-1]);
   assert.equal(o.userData.bridgePart,'baluster');
   assert.deepEqual(o.userData.originalDimensions,[.105,.13,.50]);
   for(let k=0;k<p.count;k++){
    const y=p.getY(k),r=Math.hypot(p.getX(k),p.getZ(k)),limit=.13-(y+.25)*.025/.5;
    assert.ok(r<=limit+1e-6);assert.ok(y>=-.250001&&y<=.250001);
    if(Math.abs(y)<.24&&r<limit-.006)recessed++;
   }
   // Exact top/bottom rims remain seven-sided polygons, not enlarged cylinders.
   for(let row=0;row<=12;row++){
    const y=p.getY(row*29),limit=.13-(y+.25)*.025/.5;
    for(let j=0;j<=28;j++){
     const k=row*29+j,angle=j*2*Math.PI/28;
     const poly= Math.cos(Math.PI/7)/Math.cos((angle%(2*Math.PI/7))-Math.PI/7);
     const r=Math.hypot(p.getX(k),p.getZ(k));
     assert.ok(r<=limit*poly+1e-6);
     if(row===0||row===12)near(r,limit*poly);
    }
   }
  }else{
   assert.equal(o.userData.bridgePart,'coping');near(o.position.z,0);
   const [w,h,d]=slot===0?[.26,.15,5.42]:[.22,.14,5.30];
   near(o.position.y,slot===0?1.555:2.21);
   assert.deepEqual(o.userData.originalDimensions,[w,h,d]);
   const bounds=o.geometry.boundingBox;
   for(let axis=0;axis<3;axis++){near(bounds.max.getComponent(axis),[w,h,d][axis]/2);near(bounds.min.getComponent(axis),-[w,h,d][axis]/2);}
   for(let k=0;k<p.count;k++){
    const x=p.getX(k),y=p.getY(k),z=p.getZ(k);
    assert.ok(Math.abs(x)<=w/2+1e-6&&Math.abs(y)<=h/2+1e-6&&Math.abs(z)<=d/2+1e-6);
    if(y>0&&y<h/2-.003&&Math.abs(x)<w/2-1e-6)recessed++;
   }
  }
  assert.ok([...p.array,...c.array,...n.array].every(Number.isFinite));
 }
 assert.ok(recessed>100);
 assert.equal(a.locations[0].group.userData.stateResolution,'UNRESOLVED_NOT_CURRENT_STATE');
 assert.equal(a.worldMutationAllowed,false);assert.deepEqual(a.principalCharacters,[]);
 assert.equal(JSON.stringify(bindings),source);
 console.log(JSON.stringify({objects:objects.length,recessedVertices:recessed,vertices:objects.reduce((s,o)=>s+o.geometry.getAttribute('position').count,0)}));
 }finally{a.dispose();b.dispose();}
});
test('balustrade materials retain original stone colors and dispose once; water clock unchanged',()=>{
 const a=build();
 const objects=parts(a);assert.equal(objects.length,14);
 const mats=new Set(objects.map(o=>o.material));assert.equal(mats.size,2);
 assert.deepEqual([...mats].map(m=>m.color.getHexString()).sort(),['b4ad89','ddd2a6']);
 let disposals=0;objects[0].geometry.addEventListener('dispose',()=>disposals++);
 a.tick(2,{globalCalm:true});assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===2));
 a.tick(4,{globalCalm:true,paused:true});assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===2));
 a.dispose();a.dispose();assert.equal(disposals,1);
});
