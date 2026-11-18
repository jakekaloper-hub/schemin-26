import test from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';

const bindings=[
 {id:'LOC-MUD-DOGS-SWAMP',anchor:[42,0,16],canonStatus:'PERMANENT_CANON'},
 {id:'LOC-TDS-WATERFALL-TEMPLE',anchor:[32,0,29],canonStatus:'PERMANENT_CANON'},
 {id:'LOC-COUNTRY-CLUB-JACKSON',anchor:[57,0,24],canonStatus:'PERMANENT_CANON'}
];
const build=()=>buildRegionalAssets(THREE,bindings,()=>2);
const site=a=>a.locations.find(x=>x.id==='LOC-MUD-DOGS-SWAMP').group;
const swamp=a=>a.water.find(x=>x.kind==='swamp');
const drift=(i,t)=>.075*Math.sin(t*.35+i*2.399)+.025*Math.sin(t*.79+i*2.399*1.71);
const uv=(i,t)=>[.5+(Math.sin(i*5)*7+drift(i,t))/21,.5-(Math.cos(i*9)*5+drift(i,t)*.57)/16.4];

test('twelve wake centers follow exact inherited GPU foliage phases and inverted rotated-plane V',()=>{
 const before=JSON.stringify(bindings),a=build(),w=swamp(a),f=site(a).getObjectByName('Candidate Mud Dogs floating foliage');
 const p=f.geometry.getAttribute('position'),ph=f.geometry.getAttribute('aPhase'),sites=w.material.uniforms.uPadSites.value;
 assert.equal(w.material.uniforms.uPadSiteCount.value,12);assert.equal(sites.length,12);
 assert.equal(f.userData.discs,12);
 for(const t of [0,1.2,9,57.3]){
   a.tick(t,{storm:0});
   for(let i=0;i<12;i++){
     const expected=uv(i,t);
     assert.ok(Math.abs(ph.getX(i*10)-i*2.399)<1e-4);
     assert.ok(Math.abs(p.getX(i*10)-Math.sin(i*5)*7)<1e-5);
     assert.ok(Math.abs(p.getZ(i*10)-Math.cos(i*9)*5)<1e-5);
     assert.ok(Math.abs(sites[i].x-expected[0])<1e-12);
     assert.ok(Math.abs(sites[i].y-expected[1])<1e-12);
     assert.ok(Math.hypot((sites[i].x-.5)*2,(sites[i].y-.5)*2)<.98);
   }
 }
 assert.ok(uv(0,0)[1]<.5,'positive world Z maps to negative UV V');
 assert.equal(JSON.stringify(bindings),before);
 assert.equal(a.worldMutationAllowed,false);assert.deepEqual(a.principalCharacters,[]);
 assert.deepEqual(a.locations.map(x=>x.id),bindings.map(x=>x.id));
 a.dispose();
});

test('wake field is low-contrast, finite, bank masked, and only on inherited swamp water',()=>{
 const a=build(),w=swamp(a),channel=a.water.find(x=>x.kind==='channel');
 const shader=w.material.fragmentShader;
 assert.match(shader,/uniform float uPadSiteCount;uniform vec2 uPadSites\[12\]/);
 assert.match(shader,/if\(uPadSiteCount>\.5\)/);
 assert.match(shader,/padDelta=\(vUv-uPadSites\[i\]\)\*vec2\(21\.,16\.4\)/);
 assert.match(shader,/padDistance<1\.05/);
 assert.match(shader,/padInterior=1\.-smoothstep\(\.32,1\.05,padDistance\)/);
 assert.match(shader,/padDistance\*12\.-uTime\*2\.05/);
 assert.match(shader,/padContactSheen=vec3\(\.10,\.14,\.11\)\*\(padContactWake\*\.42\*bankFade\)/);
 assert.match(shader,/contactTint\+=reliefLight\+padContactSheen/);
 assert.doesNotMatch(shader,/\bstorm\b|\bweather\b|\buRain\b/i);
 assert.equal(channel.material.uniforms.uPadSiteCount.value,0);
 assert.ok(a.water.filter(x=>x.kind!=='swamp').every(x=>x.material.uniforms.uPadSiteCount.value===0));
 assert.equal(a.water.filter(x=>x.kind==='swamp').length,1);
 assert.equal(w.mesh.geometry.getAttribute('position').count,385);
 assert.equal(w.mesh.geometry.getIndex().count,2160);
 assert.deepEqual([w.mesh.scale.x,w.mesh.scale.y],[10.5,8.2]);
 const smooth=(lo,hi,x)=>{let q=Math.max(0,Math.min(1,(x-lo)/(hi-lo)));return q*q*(3-2*q);};
 const signal=(dist,time,bank=1)=>{
   if(dist>=1.05)return [0,0,0];
   const interior=1-smooth(.32,1.05,dist);
   const crest=Math.pow(Math.max(0,Math.sin(dist*12-time*2.05)),8);
   return [.10,.14,.11].map(c=>c*interior*crest*.42*bank);
 };
 for(const d of [0,.1,.3,.6,1.04,1.05,4])for(const t of [0,1.2,17,101]){
   const v=signal(d,t);
   assert.ok(v.every((x,i)=>Number.isFinite(x)&&x>=0&&x<=[.042,.0588,.0462][i]+1e-9));
   assert.deepEqual(signal(d,t,0),[0,0,0]);
 }
 a.dispose();
});

test('global calm advances wake centers while explicit pause freezes both meshes and all center uniforms',()=>{
 const a=build(),w=swamp(a),channel=a.water.find(x=>x.kind==='channel');
 const foliage=site(a).getObjectByName('Candidate Mud Dogs floating foliage');
 const centers=w.material.uniforms.uPadSites.value;
 a.tick(3,{storm:0});
 const before=centers.map(x=>x.toArray());
 assert.equal(w.material.uniforms.uTime.value,3);
 assert.equal(foliage.material.uniforms.uTime.value,3);
 a.tick(22,{storm:0,paused:true});
 assert.deepEqual(centers.map(x=>x.toArray()),before);
 assert.equal(w.material.uniforms.uTime.value,3);
 assert.equal(foliage.material.uniforms.uTime.value,3);
 a.tick(22,{storm:0});
 assert.ok(centers.some((x,i)=>Math.abs(x.x-before[i][0])>1e-5));
 assert.equal(w.material.uniforms.uTime.value,22);
 assert.equal(channel.material.uniforms.uTime.value,22);
 assert.equal(foliage.material.uniforms.uTime.value,22);
 let disposed=0;w.material.addEventListener('dispose',()=>disposed++);
 a.dispose();a.dispose();assert.equal(disposed,1);
});