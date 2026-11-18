import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {projectAtlas} from '../../src/observer-world.mjs';
import {spatialBindings} from '../spatial.mjs';
import {buildAtlasSiteAssets} from '../atlas-site-assets.mjs';
const source=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const bindings=spatialBindings({locations:projectAtlas(source.locations)}),before=JSON.stringify(bindings);
const build=()=>buildAtlasSiteAssets(THREE,bindings,()=>4);
const crossingId='LOC-TDS-CHILI-SHARED-MARCH';
function smoothstep(a,b,x){const f=Math.max(0,Math.min(1,(x-a)/(b-a)));return f*f*(3-2*f);}
function displacement(w,x,y,t){
 const inside=1-smoothstep(.58,.95,Math.hypot(x,y));
 const a=Math.sin(x*12.7-t*1.18+Math.sin(y*7.5)*.45),b=Math.sin(y*10.2+t*.74+x*3);
 const crossing=Math.sin(y*18.8-t*2.1+Math.sin(x*5)*.55);
 return w.material.uniforms.uAmplitude.value*inside*(.72*a+.28*b+w.material.uniforms.uCrossing.value*.34*crossing);
}
test('only the existing source-bound Shared March crossing has localized presentation-flow gain',()=>{
 const a=build(),site=a.locations.find(x=>x.id===crossingId);
 assert.ok(site);assert.equal(a.locations.length,20);assert.equal(a.water.length,4);
 assert.deepEqual(new Set(a.water.map(w=>w.kind)),new Set(['mountain lake','mire','sheltered port','watercourse crossing']));
 const active=a.water.filter(w=>w.material.uniforms.uCrossing.value===1);
 assert.equal(active.length,1);assert.equal(active[0].kind,'watercourse crossing');
 assert.ok(site.group.children.includes(active[0].mesh));
 for(const w of a.water){
  assert.equal(w.material.uniforms.uCrossing.value,w.kind==='watercourse crossing'?1:0);
  assert.equal(w.mesh.geometry.getAttribute('position').count,393);
  assert.equal(w.mesh.geometry.index.count,2184);
  assert.equal(w.mesh.children.length,0);assert.equal(w.material.depthWrite,false);
 }
 assert.deepEqual(a.principalCharacters,[]);
 assert.equal(a.worldMutationAllowed,false);assert.equal(a.weatherMutationAllowed,false);
 assert.equal(JSON.stringify(bindings),before);a.dispose();
});
test('advected GPU crossing ripple and subtle sheen share time and preserve exact shore',()=>{
 const a=build(),w=a.water.find(w=>w.kind==='watercourse crossing');
 assert.match(w.material.vertexShader,/uniform float uCrossing;/);
 assert.match(w.material.vertexShader,/float crossingWave=sin\(position\.y\*18\.8-uTime\*2\.1\+sin\(position\.x\*5\.\)\*\.55\)/);
 assert.match(w.material.vertexShader,/p\.z\+=uCrossing\*uAmplitude\*\.34\*interior\*crossingWave/);
 assert.match(w.material.fragmentShader,/crossingSheen=uCrossing\*pow\(max\(sin\(vUv\.y\*72\.-uTime\*2\.1/);
 assert.match(w.material.fragmentShader,/vec3\(\.035,\.065,\.06\)\*crossingSheen/);
 const pos=w.mesh.geometry.getAttribute('position');let peak=0,changed=0;
 for(let i=0;i<pos.count;i++){
  const x=pos.getX(i),y=pos.getY(i),d1=displacement(w,x,y,1.2),d2=displacement(w,x,y,3.7);
  assert.ok(Number.isFinite(d1)&&Number.isFinite(d2));
  peak=Math.max(peak,Math.abs(d1),Math.abs(d2));changed=Math.max(changed,Math.abs(d1-d2));
  if(Math.hypot(x,y)>.95)assert.ok(Math.abs(d1)<1e-12&&Math.abs(d2)<1e-12);
 }
 assert.ok(peak>.001&&peak<=.0134+1e-8,'water relief remains within 1.34x original amplitude');
 assert.ok(changed>.002,'physical water responds to elapsed time');
 for(const other of a.water.filter(x=>x!==w)){
  assert.equal(other.material.uniforms.uCrossing.value,0);
  for(const [x,y] of [[.2,.3],[-.4,.1],[1,0]]){
   const d=displacement(other,x,y,2.3),inside=1-smoothstep(.58,.95,Math.hypot(x,y));
   const old=other.material.uniforms.uAmplitude.value*inside*
    (.72*Math.sin(x*12.7-2.3*1.18+Math.sin(y*7.5)*.45)+.28*Math.sin(y*10.2+2.3*.74+x*3));
   assert.ok(Math.abs(d-old)<1e-12);
  }
 }
 a.dispose();
});
test('global-calm water runs, explicit pause freezes, sources and disposal are unchanged',()=>{
 const a=build(),waters=[...a.water],cross=waters.find(w=>w.kind==='watercourse crossing');
 a.tick(2,{storm:0,globalCalm:true});assert.equal(cross.material.uniforms.uTime.value,2);
 a.tick(4.5,{storm:0,globalCalm:true});assert.ok(waters.every(w=>w.material.uniforms.uTime.value===4.5));
 a.tick(20,{paused:true});assert.ok(waters.every(w=>w.material.uniforms.uTime.value===4.5));
 assert.ok(waters.every(w=>w.mesh.parent));
 assert.ok(a.locations.every(x=>x.group.userData.visualAuthority==='CANDIDATE_NOT_APPROVED'));
 assert.equal(JSON.stringify(bindings),before);
 let freed=0;cross.mesh.geometry.addEventListener('dispose',()=>freed++);
 cross.material.addEventListener('dispose',()=>freed++);
 a.dispose();a.dispose();assert.equal(freed,2);
 a.tick(99);assert.equal(cross.material.uniforms.uTime.value,4.5);
});
