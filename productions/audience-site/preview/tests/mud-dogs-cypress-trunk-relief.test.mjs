import test from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';
import {batchStaticGeometry} from '../three-world.mjs';

const bindings=[
 {id:'LOC-MUD-DOGS-SWAMP',anchor:[42,0,16],canonStatus:'PERMANENT_CANON',landmarks:['mud channels','raised ground','cypress-like wetlands']},
 {id:'LOC-TDS-WATERFALL-TEMPLE',anchor:[32,0,29],canonStatus:'PERMANENT_CANON',landmarks:['waterfall','temple stone','dense vegetation']},
 {id:'LOC-COUNTRY-CLUB-JACKSON',anchor:[57,0,24],canonStatus:'PERMANENT_CANON',landmarks:['clubhouse','water hazards']}
];
const build=()=>buildRegionalAssets(THREE,bindings,()=>2);
const trunks=a=>a.locations.find(l=>l.id==='LOC-MUD-DOGS-SWAMP').group.children
 .filter(o=>o.userData.wetlandPart==='trunk').sort((a,b)=>a.userData.wetlandStand-b.userData.wetlandStand);

test('all 14 original Mud Dogs stands gain real bounded deterministic cypress bark relief with unchanged anchors',()=>{
 const source=JSON.stringify(bindings),a=build(),t=trunks(a);
 assert.equal(t.length,14);
 const material=t[0].material;
 const oldLowPoly=new THREE.CylinderGeometry(.20,.45,3.3,8);
 for(let i=0;i<t.length;i++){
  const o=t[i],h=3.3+(i%3)*.9;
  const radius=3.8+(i%4)*1.5,angle=i*2.4;
  assert.equal(o.userData.wetlandStand,i);
  assert.equal(o.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
  assert.equal(o.userData.originalRadiusEnvelopePreserved,true);
  assert.equal(o.geometry.name,'Candidate Mud Dogs fluted cypress-like trunk');
  assert.deepEqual(o.position.toArray().map(n=>+n.toFixed(7)),
   [Math.cos(angle)*radius,.12+h/2,Math.sin(angle)*radius].map(n=>+n.toFixed(7)));
  assert.equal(o.material,material,'all stands keep the existing trunk material/batch');
  assert.ok(o.geometry.getAttribute('position').count>oldLowPoly.getAttribute('position').count*3);
  const p=o.geometry.getAttribute('position'),normal=o.geometry.getAttribute('normal');
  const baseRadii=new Set(),topRadii=new Set();
  for(let k=0;k<p.count;k++){
   const x=p.getX(k),y=p.getY(k),z=p.getZ(k),r=Math.hypot(x,z);
   assert.ok(Number.isFinite(x)&&Number.isFinite(y)&&Number.isFinite(z));
   assert.ok(Math.abs(y)<=h/2+1e-5,'stand top and base remain stationary');
   const originalRadius=.20+(.45-.20)*((h/2-y)/h);
   assert.ok(r<=originalRadius+1e-5,'fluting never exceeds original radial envelope');
   assert.ok(Number.isFinite(normal.getX(k))&&Number.isFinite(normal.getY(k))&&Number.isFinite(normal.getZ(k)));
   if(r>.00001&&Math.abs(y+h/2)<1e-5)baseRadii.add(r.toFixed(4));
   if(r>.00001&&Math.abs(y-h/2)<1e-5)topRadii.add(r.toFixed(4));
  }
  assert.ok(baseRadii.size>=6,'actual base has flutes, not a flat octagon');
  assert.ok(topRadii.size>=6,'actual crown-side bark is nonuniform');
 }
 oldLowPoly.dispose();
 const a2=build(),t2=trunks(a2);
 for(let i=0;i<14;i++)assert.deepEqual(Array.from(t[i].geometry.getAttribute('position').array),
   Array.from(t2[i].geometry.getAttribute('position').array),'same input regenerates byte-identical geometry');
 assert.deepEqual(a.locations.map(l=>l.id),bindings.map(l=>l.id));
 assert.equal(JSON.stringify(bindings),source);
 assert.equal(a.worldMutationAllowed,false);assert.deepEqual(a.principalCharacters,[]);
 a2.dispose();a.dispose();
});

test('cypress fluting remains one mesh per original stand and shares opaque static batch with existing roots',()=>{
 const a=build(),group=a.locations.find(l=>l.id==='LOC-MUD-DOGS-SWAMP').group;
 const stands=trunks(a),knees=group.getObjectByName('Candidate wetland waterline root knees');
 assert.equal(stands.length,14);
 assert.equal(knees.material,stands[0].material);
 assert.equal(stands.filter(o=>o.material!==stands[0].material).length,0);
 const result=batchStaticGeometry(THREE,group);
 const matches=group.children.filter(o=>o.isMesh&&o.material===stands[0].material);
 assert.equal(matches.length,1,'original bark and root materials still compile into one opaque batch');
 assert.ok(matches[0].geometry.getAttribute('uv'),'source bark texture retains UV coordinates');
 for(const g of result.geometries)g.dispose();
 a.dispose();
});

test('Mud Dogs bark geometry stays isolated from Temple, Jackson, calm-water movement and cleanup',()=>{
 const source=JSON.stringify(bindings),a=build(),t=trunks(a),first=t[0];
 let geomDisposals=0;first.geometry.addEventListener('dispose',()=>geomDisposals++);
 for(const l of a.locations.filter(x=>x.id!=='LOC-MUD-DOGS-SWAMP'))
  assert.equal(l.group.getObjectByName('Candidate Mud Dogs fluted cypress-like trunk'),undefined);
 const swamp=a.water.find(w=>w.kind==='swamp'),river=a.water.find(w=>w.kind==='river');
 a.tick(2,{globalCalm:true,storm:0});assert.equal(swamp.material.uniforms.uTime.value,2);
 assert.equal(river.material.uniforms.uTime.value,2);
 a.tick(6,{globalCalm:true,storm:0});assert.equal(swamp.material.uniforms.uTime.value,6);
 a.tick(8,{globalCalm:true,paused:true});assert.equal(swamp.material.uniforms.uTime.value,6);
 a.tick(11,{globalCalm:true});assert.equal(swamp.material.uniforms.uTime.value,11);
 a.dispose();a.dispose();
 assert.equal(geomDisposals,1,'geometry disposes once');
 assert.equal(JSON.stringify(bindings),source);
});
