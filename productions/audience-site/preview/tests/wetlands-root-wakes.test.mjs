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

test('five low-cost water wake sites coincide with EXISTING illustrated Mud Dogs stands',()=>{
 const a=build(),swamp=a.locations.find(l=>l.id==='LOC-MUD-DOGS-SWAMP').group;
 const trunks=swamp.children.filter(x=>x.userData.wetlandPart==='trunk')
   .sort((a,b)=>a.userData.wetlandStand-b.userData.wetlandStand);
 assert.equal(trunks.length,14);
 const water=a.water.find(w=>w.kind==='swamp');
 assert.equal(water.mesh.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
 assert.equal(water.mesh.userData.sourceStands,14);
 assert.equal(water.mesh.userData.illustrativeWakeSites,5);
 assert.equal(water.material.uniforms.uRootSiteCount.value,5);
 const sites=water.material.uniforms.uRootSites.value;
 assert.equal(sites.length,5);
 for(let i=0;i<sites.length;i++){
   assert.ok(sites[i] instanceof THREE.Vector2);
   const stand=trunks[i*3];
   assert.ok(Math.abs(sites[i].x-(.5+stand.position.x/21))<1e-6);
   assert.ok(Math.abs(sites[i].y-(.5+stand.position.z/16.4))<1e-6);
   assert.ok(Math.hypot((sites[i].x-.5)*2,(sites[i].y-.5)*2)<.96);
 }
 assert.equal(water.mesh.geometry.getAttribute('position').count,385,'existing tessellated water retained');
 assert.equal(water.mesh.geometry.index.count,2160,'no additional wetland water triangles');
 a.dispose();
});

test('root wakes are low-intensity shader motion only on the EXISTING swamp surface',()=>{
 const a=build(),wet=a.water.filter(w=>['swamp','channel'].includes(w.kind));
 assert.deepEqual(wet.map(w=>w.kind),['swamp','channel']);
 const swamp=wet[0],channel=wet[1];
 const fragment=swamp.material.fragmentShader;
 assert.match(fragment,/uniform vec2 uRootSites\[5\]/);
 assert.match(fragment,/if\(float\(i\)>=uRootSiteCount\)break/);
 assert.match(fragment,/rootWake=max\(rootWake,wakeFade\*wakeCrest\)/);
 assert.match(fragment,/rootWake\*\.68\*bankFade/);
 assert.match(fragment,/wakeFade=1\.-smoothstep\(\.55,3\.25,rootDistance\)/);
 assert.match(fragment,/rootDistance\*7\.1-uTime\*1\.6/);
 assert.doesNotMatch(fragment,/storm|weather/i);
 assert.equal(channel.material.uniforms.uRootSiteCount.value,0);
 assert.ok(a.water.filter(w=>!['swamp','channel'].includes(w.kind))
   .every(w=>(w.material.uniforms.uRootSiteCount?.value??0)===0));
 assert.ok(a.water.every(w=>w.mesh.isMesh));
 assert.ok(a.worldMutationAllowed===false);
 a.dispose();
});

test('wake movement survives global calm, freezes on pause, and leaves Atlas and history immutable',()=>{
 const before=JSON.stringify(bindings),a=build(),swamp=a.water.find(w=>w.kind==='swamp');
 a.tick(4,{storm:0});assert.equal(swamp.material.uniforms.uTime.value,4);
 a.tick(9,{storm:0});assert.equal(swamp.material.uniforms.uTime.value,9);
 a.tick(22,{storm:0,paused:true});assert.equal(swamp.material.uniforms.uTime.value,9);
 a.tick(22,{storm:0});assert.equal(swamp.material.uniforms.uTime.value,22);
 assert.deepEqual(a.locations.map(l=>l.id),bindings.map(l=>l.id));
 assert.deepEqual(a.principalCharacters,[]);
 assert.equal(JSON.stringify(bindings),before);
 a.dispose();
});
