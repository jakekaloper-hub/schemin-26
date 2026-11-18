import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {projectAtlas} from '../../src/observer-world.mjs';
import {spatialBindings} from '../spatial.mjs';
import {buildAtlasSiteAssets} from '../atlas-site-assets.mjs';
const source=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const bindings=spatialBindings({locations:projectAtlas(source.locations)}),untouched=JSON.stringify(bindings);
const build=()=>buildAtlasSiteAssets(THREE,bindings,()=>4);
const smooth=(a,b,v)=>{let t=Math.max(0,Math.min(1,(v-a)/(b-a)));return t*t*(3-2*t);};
const relief=(w,x,y,t)=>{let r=Math.hypot(x,y),m=Math.hypot(x-.12,y+.08);return w.material.uniforms.uMire.value*w.material.uniforms.uAmplitude.value*.22*Math.exp(-m*3.2)*(1-smooth(.58,.95,r))*Math.sin(m*17-t*.81+x*4.8-y*3.1);};
test('source exact Mire Hill visual-only gate preserves all existing water bodies and geometry',()=>{
 const a=build(),mire=a.water.find(w=>w.kind==='mire'),site=a.locations.find(s=>s.id==='LOC-DK-MUD-HILL');
 assert.ok(mire&&site&&site.group.children.includes(mire.mesh));
 assert.ok(source.locations.find(x=>x.id==='LOC-DK-MUD-HILL').persistent_landmarks.includes('mire'));
 assert.equal(a.locations.length,20);assert.equal(a.water.length,4);
 assert.deepEqual(new Set(a.water.map(w=>w.kind)),new Set(['mire','mountain lake','sheltered port','watercourse crossing']));
 for(const w of a.water){assert.equal(w.material.uniforms.uMire.value,w===mire?1:0);assert.equal(w.mesh.geometry.getAttribute('position').count,393);assert.equal(w.mesh.geometry.index.count,2184);assert.equal(w.mesh.children.length,0);}
 assert.equal(a.worldMutationAllowed,false);assert.equal(a.weatherMutationAllowed,false);assert.deepEqual(a.principalCharacters,[]);
 assert.equal(site.group.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');assert.equal(JSON.stringify(bindings),untouched);a.dispose();
});
test('mire physical eddy and sediment tint share the clock, remain bounded and have fixed rim',()=>{
 const a=build(),mire=a.water.find(w=>w.kind==='mire');
 for(const s of ['uniform float uMire;','float mireBand=exp(-mireR*3.2)*interior;','float mireWave=sin(mireR*17.-uTime*.81+position.x*4.8-position.y*3.1);','p.z+=uMire*uAmplitude*.22*mireBand*mireWave;'])assert.ok(mire.material.vertexShader.includes(s),s);
 for(const s of ['float mireSilt=uMire*exp(-mireR*3.2)*(.5+.5*sin(mireR*17.-uTime*.81+mireXY.x*4.8-mireXY.y*3.1))','c=clamp(c+vec3(.052,.034,-.008)*mireSilt,0.,1.);'])assert.ok(mire.material.fragmentShader.includes(s),s);
 let peak=0,delta=0;const p=mire.mesh.geometry.getAttribute('position');
 for(let i=0;i<p.count;i++){const x=p.getX(i),y=p.getY(i),v=relief(mire,x,y,1.25),v2=relief(mire,x,y,3.75);
  assert.ok(Number.isFinite(v)&&Number.isFinite(v2));peak=Math.max(peak,Math.abs(v),Math.abs(v2));delta=Math.max(delta,Math.abs(v-v2));
  assert.ok(Math.abs(v)<=.00264+1e-8&&Math.abs(v2)<=.00264+1e-8);
  if(Math.hypot(x,y)>=.95)assert.ok(Math.abs(v)<1e-12&&Math.abs(v2)<1e-12);
 }
 assert.ok(peak>.0006&&delta>.001);
 for(const w of a.water.filter(w=>w!==mire)){assert.equal(w.material.uniforms.uMire.value,0);assert.ok(Math.abs(relief(w,0,0,1.25))<1e-12);}
 assert.equal(JSON.stringify(bindings),untouched);a.dispose();
});
test('global calm allows normal mire water movement; explicit pause and idempotent disposal',()=>{
 const a=build(),mire=a.water.find(w=>w.kind==='mire');
 a.tick(1.25,{storm:0,globalCalm:true});assert.equal(mire.material.uniforms.uTime.value,1.25);
 a.tick(3.75,{storm:0,globalCalm:true});assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===3.75));
 a.tick(12,{storm:0,globalCalm:true,paused:true});assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===3.75));
 let n=0;mire.mesh.geometry.addEventListener('dispose',()=>n++);mire.material.addEventListener('dispose',()=>n++);
 a.dispose();a.dispose();assert.equal(n,2);a.tick(25);assert.equal(mire.material.uniforms.uTime.value,3.75);
 assert.equal(JSON.stringify(bindings),untouched);
});
