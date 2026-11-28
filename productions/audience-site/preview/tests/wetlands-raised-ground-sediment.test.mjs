import test from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';

const bindings=[
 {id:'LOC-MUD-DOGS-SWAMP',anchor:[42,0,16],canonStatus:'PERMANENT_CANON'},
 {id:'LOC-TDS-WATERFALL-TEMPLE',anchor:[32,0,29],canonStatus:'PERMANENT_CANON'},
 {id:'LOC-COUNTRY-CLUB-JACKSON',anchor:[57,0,24],canonStatus:'PERMANENT_CANON'}
];
const islands=[[1,.1,1,4,1.2,3],[-6,.1,-3,3,.9,2.7],[6,.2,-4,3.5,1,2.8],[-4,.1,5,2.7,.8,2]];
const create=()=>buildRegionalAssets(THREE,bindings,()=>2);
const ground=a=>a.locations.find(x=>x.id==='LOC-MUD-DOGS-SWAMP').group
 .getObjectByName('Candidate wetland raised-ground relief');

test('wet-silt candidate reuses precisely the four inherited raised-ground meshes and draw budget',()=>{
 const a=create(),g=ground(a),p=g.geometry.getAttribute('position');
 const c=g.geometry.getAttribute('color'),island=g.geometry.getAttribute('aIsland');
 assert.equal(g.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
 assert.deepEqual(g.userData.sourceEnvironment,['raised ground','mudflats']);
 assert.equal(g.userData.islandCount,4);
 assert.equal(p.count,452);assert.equal(c.count,452);assert.equal(island.count,452);
 assert.equal(g.geometry.getIndex().count,2352);
 assert.equal(g.material.vertexColors,true);
 for(let i=0;i<p.count;i++){
   const k=island.getX(i),[x,y,z,sx,sy,sz]=islands[k];
   assert.ok(Number.isInteger(k)&&k>=0&&k<4);
   assert.ok(Math.hypot((p.getX(i)-x)/sx,(p.getZ(i)-z)/sz)<=1.02);
   assert.ok(p.getY(i)>=y-.22*sy&&p.getY(i)<=y+1.20*sy);
 }
 assert.equal(a.root.getObjectsByProperty('name','Candidate wetland raised-ground relief').length,1);
 assert.equal(a.water.filter(w=>w.kind==='swamp').length,1);
 a.dispose();
});

test('terrace silt and lower wet margins are deterministic, distinct and bounded',()=>{
 const a=create(),colors=ground(a).geometry.getAttribute('color');
 const baseline=['#697456','#626952','#555844','#393e35'].map(v=>new THREE.Color(v));
 let untouched=0,silted=0,wetted=0;const variation=new Set();
 for(let k=0;k<4;k++)for(let ring=0;ring<4;ring++)for(let i=0;i<28;i++){
   const j=k*113+1+ring*28+i,angle=i*2*Math.PI/28;
   const scale=.90+.095*(.5+.5*Math.sin(angle*8+k+ring));
   const old=baseline[ring].clone().multiplyScalar(scale);
   const actual=[colors.getX(j),colors.getY(j),colors.getZ(j)];
   for(let ch=0;ch<3;ch++)assert.ok(Number.isFinite(actual[ch])&&actual[ch]>=0&&actual[ch]<=1);
   assert.ok(Math.max(...actual.map((v,ch)=>Math.abs(v-[old.r,old.g,old.b][ch])))<.08);
   if(ring===0){
     assert.ok(Math.abs(actual[0]-old.r)<1e-6);
     assert.ok(Math.abs(actual[1]-old.g)<1e-6);
     assert.ok(Math.abs(actual[2]-old.b)<1e-6);
     untouched++;
   }
   if(ring===1&&actual[0]>old.r+.0002)silted++;
   if(ring===3&&actual[0]<old.r-.001)wetted++;
   variation.add(actual.map(v=>v.toFixed(3)).join(':'));
 }
 assert.equal(untouched,112);
 assert.ok(silted>=60,'upper terrace carries broken silt tone');
 assert.ok(wetted>=100,'lower margin darkens around four islands');
 assert.ok(variation.size>=70,'color bands do not flatten to identical fill');
 a.dispose();
});

test('sediment candidate leaves source, other locations and ordinary calm-water time untouched',()=>{
 const before=JSON.stringify(bindings),a=create();
 assert.equal(a.worldMutationAllowed,false);assert.deepEqual(a.principalCharacters,[]);
 assert.deepEqual(a.locations.map(l=>l.id),bindings.map(l=>l.id));
 for(const l of a.locations.filter(x=>x.id!=='LOC-MUD-DOGS-SWAMP'))
   assert.equal(l.group.getObjectByName('Candidate wetland raised-ground relief'),undefined);
 const water=a.water.find(w=>w.kind==='swamp');
 assert.equal(water.mesh.geometry.getAttribute('position').count,385);
 assert.equal(water.mesh.geometry.getIndex().count,2160);
 a.tick(2,{storm:0});a.tick(8,{storm:0});
 assert.equal(water.material.uniforms.uTime.value,8);
 a.tick(15,{storm:0,paused:true});assert.equal(water.material.uniforms.uTime.value,8);
 assert.equal(JSON.stringify(bindings),before);
 a.dispose();
});
