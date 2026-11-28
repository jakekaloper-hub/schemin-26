import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {projectAtlas} from '../../src/observer-world.mjs';
import {spatialBindings} from '../spatial.mjs';
import {buildAtlasSiteAssets} from '../atlas-site-assets.mjs';

const atlas=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const bindings=spatialBindings({locations:projectAtlas(atlas.locations)});
const sourceBefore=JSON.stringify(bindings);
const build=()=>buildAtlasSiteAssets(THREE,bindings,()=>4);
const bridgeId='LOC-BRIDGE-MOUNTAIN-LAKE';
const smoothstep=(a,b,x)=>{const k=Math.max(0,Math.min(1,(x-a)/(b-a)));return k*k*(3-2*k);};
function relief(w,x,y,time){
 const interior=1-smoothstep(.58,.95,Math.hypot(x,y));
 const base=.72*Math.sin(x*12.7-time*1.18+Math.sin(y*7.5)*.45)+.28*Math.sin(y*10.2+time*.74+x*3);
 const crossing=w.material.uniforms.uCrossing.value*.34*Math.sin(y*18.8-time*2.1+Math.sin(x*5)*.55);
 const bridgeR=Math.min(Math.hypot(x+.39,y),Math.hypot(x-.39,y));
 const contact=w.material.uniforms.uBridge.value*.16*Math.exp(-bridgeR*8)*Math.sin(bridgeR*24-time*1.7);
 return w.material.uniforms.uAmplitude.value*interior*(base+crossing+contact);
}
test('source bridge site alone owns the two candidate lake-contact ripples and no added geometry',()=>{
 const a=build(),site=a.locations.find(x=>x.id===bridgeId),lake=a.water.find(x=>x.kind==='mountain lake');
 assert.ok(site&&lake&&site.group.children.includes(lake.mesh));
 assert.equal(a.locations.length,20);assert.equal(a.water.length,4);
 assert.deepEqual(new Set(a.water.map(w=>w.kind)),new Set(['mountain lake','mire','sheltered port','watercourse crossing']));
 assert.equal(a.water.filter(w=>w.material.uniforms.uBridge.value===1).length,1);
 assert.equal(lake.material.uniforms.uBridge.value,1);
 assert.equal(lake.material.uniforms.uCrossing.value,0);
 for(const w of a.water){
  assert.equal(w.material.uniforms.uBridge.value,w===lake?1:0);
  assert.equal(w.mesh.geometry.getAttribute('position').count,393);
  assert.equal(w.mesh.geometry.index.count,2184);
  assert.equal(w.mesh.children.length,0);
  assert.equal(w.material.depthWrite,false);
 }
 assert.deepEqual(a.principalCharacters,[]);
 assert.equal(a.worldMutationAllowed,false);assert.equal(a.weatherMutationAllowed,false);
 assert.equal(JSON.stringify(bindings),sourceBefore);a.dispose();
});
test('two time-advected physical lake-contact ripple fronts leave rim fixed and other waters unchanged',()=>{
 const a=build(),lake=a.water.find(w=>w.kind==='mountain lake');
 assert.match(lake.material.vertexShader,/uniform float uBridge;/);
 assert.match(lake.material.vertexShader,/float bridgeR=min\(length\(position\.xy-vec2\(-\.39,0\.\)\),length\(position\.xy-vec2\(\.39,0\.\)\)\)/);
 assert.match(lake.material.vertexShader,/p\.z\+=uBridge\*uAmplitude\*\.16\*interior\*bridgeWave/);
 assert.match(lake.material.fragmentShader,/float bridgeSheen=uBridge\*exp\(-bridgeR\*10\.\)/);
 assert.match(lake.material.fragmentShader,/vec3\(\.055,\.09,\.08\)\*bridgeSheen/);
 const pos=lake.mesh.geometry.getAttribute('position');
 let peak=0,changed=0,contactMotion=0;
 for(let i=0;i<pos.count;i++){
  const x=pos.getX(i),y=pos.getY(i),d1=relief(lake,x,y,1.2),d2=relief(lake,x,y,3.7);
  assert.ok(Number.isFinite(d1)&&Number.isFinite(d2));
  peak=Math.max(peak,Math.abs(d1),Math.abs(d2));changed=Math.max(changed,Math.abs(d1-d2));
  if(Math.hypot(x,y)>.95)assert.ok(Math.abs(d1)<1e-12&&Math.abs(d2)<1e-12);
 }
 for(const x of [-.39,.39]){
  const t1=relief(lake,x,0,1.2),t2=relief(lake,x,0,3.7);
  contactMotion=Math.max(contactMotion,Math.abs(t1-t2));
 }
 assert.ok(peak>.001&&peak<=.028*1.16+1e-7);
 assert.ok(changed>.002&&contactMotion>.001);
 for(const w of a.water.filter(w=>w!==lake)){
  assert.equal(w.material.uniforms.uBridge.value,0);
  for(const [x,y] of [[.2,.3],[-.4,.1],[1,0]]){
   const old=relief(w,x,y,2.3);const r=Math.hypot(x,y),interior=1-smoothstep(.58,.95,r);
   const normal=interior*w.material.uniforms.uAmplitude.value*(.72*Math.sin(x*12.7-2.3*1.18+Math.sin(y*7.5)*.45)+.28*Math.sin(y*10.2+2.3*.74+x*3));
   const crossing=w.material.uniforms.uCrossing.value*.34*w.material.uniforms.uAmplitude.value*interior*Math.sin(y*18.8-2.3*2.1+Math.sin(x*5)*.55);
   assert.ok(Math.abs(old-normal-crossing)<1e-12);
  }
 }
 assert.equal(JSON.stringify(bindings),sourceBefore);a.dispose();
});
test('global calm does not stop moving lake, explicit pause does; repeat disposal remains idempotent',()=>{
 const a=build(),lake=a.water.find(w=>w.kind==='mountain lake');
 a.tick(2,{storm:0,globalCalm:true});assert.equal(lake.material.uniforms.uTime.value,2);
 a.tick(4.5,{storm:0,globalCalm:true});assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===4.5));
 a.tick(20,{paused:true});assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===4.5));
 assert.ok(a.locations.every(x=>x.group.userData.visualAuthority==='CANDIDATE_NOT_APPROVED'));
 assert.equal(JSON.stringify(bindings),sourceBefore);
 let disposed=0;
 lake.mesh.geometry.addEventListener('dispose',()=>disposed++);
 lake.material.addEventListener('dispose',()=>disposed++);
 a.dispose();a.dispose();assert.equal(disposed,2);a.tick(44);assert.equal(lake.material.uniforms.uTime.value,4.5);
});
