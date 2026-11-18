import test from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';

const bindings=[
 {id:'LOC-MUD-DOGS-SWAMP',anchor:[42,0,16],canonStatus:'PERMANENT_CANON'},
 {id:'LOC-TDS-WATERFALL-TEMPLE',anchor:[32,0,29],canonStatus:'PERMANENT_CANON'},
 {id:'LOC-COUNTRY-CLUB-JACKSON',anchor:[57,0,24],canonStatus:'PERMANENT_CANON'},
];
const build=()=>buildRegionalAssets(THREE,bindings,()=>2);
const floaters=a=>a.locations.find(x=>x.id==='LOC-MUD-DOGS-SWAMP').group.getObjectByName('Candidate Mud Dogs floating foliage');

test('all twelve inherited water discs preserve exact centers, original footprint bounds and source identity',()=>{
 const before=JSON.stringify(bindings),a=build(),f=floaters(a);
 assert.ok(f?.isMesh&&f.material.isShaderMaterial);
 assert.equal(f.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
 assert.deepEqual(f.userData.sourceEnvironment,['mud channels','cypress-like wetlands']);
 assert.equal(f.userData.discs,12);assert.equal(f.userData.localCenterPreserved,true);
 assert.deepEqual(f.userData.routeIds,[]);assert.deepEqual(f.userData.principalCharacters,[]);
 assert.equal(f.userData.navigable,false);assert.equal(f.userData.drawBudgetDelta,1);
 const p=f.geometry.getAttribute('position'),ph=f.geometry.getAttribute('aPhase'),edge=f.geometry.getAttribute('aEdge');
 assert.equal(p.count,120);assert.equal(ph.count,120);assert.equal(edge.count,120);
 assert.equal(f.geometry.getIndex().count,324);
 const colors=f.geometry.getAttribute('aTint');assert.equal(colors.count,120);
 const uniqueCenters=new Set();
 for(let i=0;i<12;i++){
   const cx=Math.sin(i*5)*7,cz=Math.cos(i*9)*5,r=.18+(i%3)*.08,start=i*10;
   uniqueCenters.add(p.getX(start).toFixed(4)+','+p.getZ(start).toFixed(4));
   assert.ok(Math.abs(p.getX(start)-cx)<1e-5);
   assert.ok(Math.abs(p.getZ(start)-cz)<1e-5);
   assert.equal(edge.getX(start),0);
   for(let k=0;k<10;k++){
     const j=start+k;
     assert.ok([p.getX(j),p.getY(j),p.getZ(j),ph.getX(j)].every(Number.isFinite));
     assert.ok(Math.abs(ph.getX(j)-i*2.399)<.0001,'each disc has one unchanged phase');
     assert.equal(p.getY(j),.16);
     assert.ok(Math.hypot(p.getX(j)-cx,p.getZ(j)-cz)<=r+.00001,'never expands old disc');
     if(k)assert.equal(edge.getX(j),1);
     const normalized=Math.hypot(p.getX(j)/10.5,p.getZ(j)/8.2);
     assert.ok(normalized<.99,'no new water-boundary crossing');
   }
 }
 assert.equal(uniqueCenters.size,12);
 assert.equal(JSON.stringify(bindings),before);
 assert.equal(a.worldMutationAllowed,false);assert.deepEqual(a.principalCharacters,[]);
 for(const loc of a.locations.filter(x=>x.id!=='LOC-MUD-DOGS-SWAMP'))
   assert.equal(loc.group.getObjectByName('Candidate Mud Dogs floating foliage'),undefined);
 a.dispose();
});

test('GPU bob/drift is independently phased, bounded, visible, calm-state active and paused only explicitly',()=>{
 const a=build(),f=floaters(a),shader=f.material.vertexShader,m=f.material;
 assert.equal(m.transparent,false);assert.equal(m.depthWrite,true);assert.equal(f.castShadow,false);
 assert.equal(f.userData.ambientClock,'ORDINARY_ENVIRONMENT');
 assert.equal(f.userData.illustrativeMaxHorizontalDrift,.1);
 assert.match(shader,/float drift=\.075\*sin\(uTime\*\.35\+aPhase\)\+\.025\*sin/);
 assert.match(shader,/p\.x\+=drift;p\.z\+=drift\*\.57/);
 assert.match(shader,/p\.y\+=\.010\*sin/);
 assert.doesNotMatch(shader,/\buStorm\b|\buWeather\b|\buRain\b/);
 const p=f.geometry.getAttribute('position');
 const before=f.geometry.boundingSphere.radius;
 const unpadded=f.geometry.clone();unpadded.computeBoundingSphere();
 assert.ok(Math.abs(before-unpadded.boundingSphere.radius-.12)<1e-5,'moving discs need extra GPU culling margin');
 unpadded.dispose();
 let moved=false;
 for(let i=0;i<12;i++){
   const phase=i*2.399,cx=p.getX(i*10),cz=p.getZ(i*10),r=.18+(i%3)*.08;
   let prior=null;
   for(const time of [0,1.2,11,97]){
     const drift=.075*Math.sin(time*.35+phase)+.025*Math.sin(time*.79+phase*1.71);
     assert.ok(Math.abs(drift)<=.1+1e-12);
     for(let k=0;k<10;k++){
       const j=i*10+k,edge=k?1:0;
       const bob=.010*Math.sin(time*.90+phase)+.009*edge*Math.sin(time*.52+phase*1.30);
       assert.ok(Math.abs(bob)<=.019+1e-12);
       assert.ok(Math.hypot((p.getX(j)+drift)/10.5,(p.getZ(j)+drift*.57)/8.2)<1,
         'animated disc stays inside inherited water surface');
     }
     const current=[cx+drift,cz+drift*.57];
     if(prior&&Math.abs(current[0]-prior[0])>.003)moved=true;
     prior=current;
   }
 }
 assert.ok(moved,'foliage must visibly drift rather than just duplicate static discs');
 const water=a.water.find(w=>w.kind==='swamp');
 a.tick(2,{storm:0});assert.equal(m.uniforms.uTime.value,2);assert.equal(water.material.uniforms.uTime.value,2);
 a.tick(5,{storm:0});assert.equal(m.uniforms.uTime.value,5);assert.equal(water.material.uniforms.uTime.value,5);
 a.tick(17,{storm:0,paused:true});assert.equal(m.uniforms.uTime.value,5);assert.equal(water.material.uniforms.uTime.value,5);
 a.dispose();
});

test('one GPU draw owns the inherited surface detail, disposes once, and introduces no new actors or routes',()=>{
 const a=build(),f=floaters(a),m=f.material,g=f.geometry;
 assert.equal(a.root.getObjectsByProperty('name','Candidate Mud Dogs floating foliage').length,1);
 assert.equal(f.userData.drawBudgetDelta,1);
 assert.equal(a.water.filter(w=>w.kind==='swamp').length,1);
 let materialDisposals=0,geometryDisposals=0;
 m.addEventListener('dispose',()=>materialDisposals++);
 g.addEventListener('dispose',()=>geometryDisposals++);
 a.dispose();a.dispose();
 assert.equal(materialDisposals,1);assert.equal(geometryDisposals,1);
});
