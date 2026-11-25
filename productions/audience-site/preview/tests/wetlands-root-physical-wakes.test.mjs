import test from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';

const bindings=[
 {id:'LOC-TDS-WATERFALL-TEMPLE',anchor:[31,0,51],canonStatus:'PERMANENT_CANON'},
 {id:'LOC-MUD-DOGS-SWAMP',anchor:[42,0,16],canonStatus:'PERMANENT_CANON'},
 {id:'LOC-COUNTRY-CLUB-JACKSON',anchor:[57,0,24],canonStatus:'PERMANENT_CANON'}
];
const build=()=>buildRegionalAssets(THREE,bindings,()=>2);
const smooth=(a,b,x)=>{const t=Math.max(0,Math.min(1,(x-a)/(b-a)));return t*t*(3-2*t);};
const rootRelief=(u,v,t,sites)=>{
 let field=0;
 for(const site of sites){
   const d=Math.hypot((u-site.x)*21,(v-site.y)*16.4);
   const fade=1-smooth(.55,3.25,d);
   const pulse=Math.max(0,Math.sin(d*7.1-t*1.6))**6;
   field=Math.max(field,pulse*fade);
 }
 const shoreHold=1-smooth(.65,.96,Math.hypot((u-.5)*2,(v-.5)*2));
 return .006*field*shoreHold;
};

test('five original UV-aligned tree roots drive the same existing swamp geometry, not the channel',()=>{
 const before=JSON.stringify(bindings),a=build();
 const swamp=a.water.find(w=>w.kind==='swamp'),channel=a.water.find(w=>w.kind==='channel');
 assert.ok(swamp&&channel);
 assert.equal(a.water.filter(w=>w.kind==='swamp').length,1);
 assert.equal(swamp.material.uniforms.uRootSiteCount.value,5);
 assert.equal(channel.material.uniforms.uRootSiteCount.value,0);
 assert.equal(swamp.mesh.geometry.getAttribute('position').count,385);
 assert.equal(swamp.mesh.geometry.index.count,2160);
 assert.deepEqual(swamp.mesh.position.toArray(),[0,.12,0]);
 assert.deepEqual(swamp.mesh.scale.toArray(),[10.5,8.2,1]);
 assert.equal(swamp.mesh.rotation.x,-Math.PI/2);
 const stands=[];
 for(let i=0;i<14;i++){
   const angle=i*2.4,r=3.8+(i%4)*1.5;
   if(i%3===0)stands.push([Math.cos(angle)*r,Math.sin(angle)*r]);
 }
 const sites=swamp.material.uniforms.uRootSites.value;
 assert.equal(sites.length,stands.length);
 for(let i=0;i<sites.length;i++){
   assert.ok(Math.abs((sites[i].x-.5)*21-stands[i][0])<1e-10);
   assert.ok(Math.abs((.5-sites[i].y)*16.4-stands[i][1])<1e-10,
    'rotated -PI/2 disk must not mirror the root impact along Z');
 }
 assert.equal(JSON.stringify(bindings),before);
 assert.equal(a.worldMutationAllowed,false);
 assert.deepEqual(a.principalCharacters,[]);
 assert.equal(a.locations[1].group.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
 a.dispose();
});

test('vertex-stage root contact matches existing fragment ripple phase and is bounded to interior',()=>{
 const a=build(),water=a.water.find(w=>w.kind==='swamp');
 const shader=water.material.vertexShader,fragment=water.material.fragmentShader;
 assert.match(shader,/uniform float uRootSiteCount;uniform vec2 uRootSites\[5\]/);
 const vertexBranch=shader.slice(shader.indexOf('if(uWetland>.5)'),shader.indexOf('if(uRiver>.5)'));
 for(const expression of [
  /if\(uRootSiteCount>\.5\)/,
  /for\(int i=0;i<5;i\+\+\)/,
  /rootDistance=length\(\(uv-uRootSites\[i\]\)\*vec2\(21\.,16\.4\)\)/,
  /rootFade=1\.-smoothstep\(\.55,3\.25,rootDistance\)/,
  /rootPulse=pow\(max\(sin\(rootDistance\*7\.1-uTime\*1\.6\),0\.\),6\.\)/,
  /p\.z\+=\.006\*rootRelief\*shoreHold/
 ])assert.match(vertexBranch,expression);
 assert.match(fragment,/rootWake=max\(rootWake,wakeFade\*wakeCrest\)/);
 assert.match(fragment,/rootWakeCoordinate=rootDistance\*7\.1-uTime\*1\.6/);
 assert.match(fragment,/wakeCrest=pow\(max\(sin\(rootWakeCoordinate\),0\.\),6\.\)\s*\*\(1\.-smoothstep\(\.35,1\.15,fwidth\(rootWakeCoordinate\)\)\)/);
 assert.doesNotMatch(shader,/\buStorm\b|\buWeather\b/i);
 assert.equal(water.material.uniforms.uRiver.value,0);
 const sites=water.material.uniforms.uRootSites.value;
 const uv=water.mesh.geometry.getAttribute('uv');
 let moving=0,positive=0;
 for(let i=0;i<uv.count;i++){
   const u=uv.getX(i),v=uv.getY(i);
   const at0=rootRelief(u,v,0,sites),at1=rootRelief(u,v,1.1,sites);
   assert.ok(Number.isFinite(at0)&&Number.isFinite(at1));
   assert.ok(at0>=0&&at0<=.00600001&&at1>=0&&at1<=.00600001);
   moving=Math.max(moving,Math.abs(at1-at0));positive=Math.max(positive,at0,at1);
   if(Math.hypot((u-.5)*2,(v-.5)*2)>.96){
     assert.ok(at0<1e-12&&at1<1e-12,'original rim never deforms');
   }
 }
 assert.ok(positive>.002,'root ripples actually displace existing mesh vertices');
 assert.ok(moving>.002,'root ripples change position with ordinary clock');
 assert.equal(rootRelief(.5,.5,0,[]),0,'zero sites leave water unaffected');
 assert.equal(rootRelief(.95,.95,2,sites),0,'impact remains inside water surface');
 a.dispose();
});

test('swamp-only relief continues during global calm, freezes on explicit pause and disposes cleanly',()=>{
 const before=JSON.stringify(bindings),a=build(),swamp=a.water.find(w=>w.kind==='swamp');
 for(const w of a.water.filter(w=>w.kind!=='swamp')){
  assert.equal(w.material.uniforms.uRootSiteCount?.value??0,0,w.kind+' must receive no tree wake sites');
 }
 a.tick(2,{storm:0});assert.equal(swamp.material.uniforms.uTime.value,2);
 a.tick(11,{storm:0});assert.equal(swamp.material.uniforms.uTime.value,11);
 a.tick(19,{storm:0,paused:true});assert.equal(swamp.material.uniforms.uTime.value,11);
 a.tick(21,{storm:0});assert.equal(swamp.material.uniforms.uTime.value,21);
 assert.equal(JSON.stringify(bindings),before);
 a.dispose();a.dispose();
});
