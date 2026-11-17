import test from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';

const bindings=[
 {id:'LOC-MUD-DOGS-SWAMP',anchor:[42,0,16],canonStatus:'PERMANENT_CANON'},
 {id:'LOC-TDS-WATERFALL-TEMPLE',anchor:[32,0,29],canonStatus:'PERMANENT_CANON'},
 {id:'LOC-COUNTRY-CLUB-JACKSON',anchor:[57,0,24],canonStatus:'PERMANENT_CANON'},
];
const islands=[[1,.1,1,4,1.2,3],[-6,.1,-3,3,.9,2.7],[6,.2,-4,3.5,1,2.8],[-4,.1,5,2.7,.8,2]];
const build=()=>buildRegionalAssets(THREE,bindings,()=>2);
const find=(assets)=>assets.locations.find(p=>p.id==='LOC-MUD-DOGS-SWAMP').group.getObjectByName('Candidate wetland raised-ground relief');

test('four existing raised-ground footprints gain one sculpted, bounded, nonplanar sediment mesh',()=>{
 const a=build(),ground=find(a);
 assert.ok(ground?.isMesh,'sculpted raised-ground relief must replace four simple decorative rock lumps');
 assert.equal(ground.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
 assert.deepEqual(ground.userData.sourceEnvironment,['raised ground','mudflats']);
 assert.deepEqual(ground.userData.routeIds,[]);assert.equal(ground.userData.navigable,false);
 assert.equal(ground.userData.islandCount,4);
 const p=ground.geometry.getAttribute('position'),c=ground.geometry.getAttribute('color'),idx=ground.geometry.getAttribute('aIsland');
 assert.ok(p.count>=300&&p.count<=900,'single authored surface with bounded geometry');
 assert.equal(c.count,p.count);assert.equal(idx.count,p.count);
 assert.ok(ground.geometry.getIndex()?.count>=800,'connected layered triangulation rather than four flat circles');
 const heights=islands.map(()=>new Set());
 for(let i=0;i<p.count;i++){
   const k=idx.getX(i);assert.ok(Number.isInteger(k)&&k>=0&&k<4);
   const [x,y,z,sx,sy,sz]=islands[k];
   const radius=Math.hypot((p.getX(i)-x)/sx,(p.getZ(i)-z)/sz);
   assert.ok(radius<=1.02,`raised-ground geometry ${k} leaked outside existing illustrative footprint (${radius})`);
   assert.ok(p.getY(i)>=y-.22*sy&&p.getY(i)<=y+1.20*sy,'relief stays within existing local height envelope');
   heights[k].add(p.getY(i).toFixed(2));
 }
 assert.ok(heights.every(h=>h.size>=10),'each island must have genuinely differentiated elevations');
 assert.equal(a.water.filter(w=>w.kind==='swamp').length,1);
 a.dispose();
});

test('candidate relief stays in Mud Dogs source location without inventing routes or modifying canonical inputs',()=>{
 const original=JSON.stringify(bindings),a=build();
 assert.equal(a.worldMutationAllowed,false);assert.deepEqual(a.principalCharacters,[]);
 assert.deepEqual(a.locations.map(x=>x.id),bindings.map(x=>x.id));
 assert.equal(a.root.getObjectsByProperty('name','Candidate wetland raised-ground relief').length,1);
 for(const loc of a.locations.filter(x=>x.id!=='LOC-MUD-DOGS-SWAMP'))
   assert.equal(loc.group.getObjectByName('Candidate wetland raised-ground relief'),undefined);
 assert.equal(JSON.stringify(bindings),original);
 a.dispose();
});

test('new static mudflat relief does not interfere with calm-weather water motion or explicit pause',()=>{
 const a=build(),water=a.water.find(w=>w.kind==='swamp');
 assert.ok(find(a));
 a.tick(2,{storm:0});assert.equal(water.material.uniforms.uTime.value,2);
 a.tick(6,{storm:0});assert.equal(water.material.uniforms.uTime.value,6);
 a.tick(9,{storm:0,paused:true});assert.equal(water.material.uniforms.uTime.value,6);
 a.dispose();
});
