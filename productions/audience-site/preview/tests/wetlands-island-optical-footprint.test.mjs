import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';
const source=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const place=source.locations.find(p=>p.id==='LOC-MUD-DOGS-SWAMP');
const bindings=[{id:place.id,anchor:[place.abstract_position[0],0,place.abstract_position[1]],canonStatus:place.canon_status,landmarks:place.persistent_landmarks}];
test('island contact light uses a seam-safe phase gradient only in the fragment shader',()=>{
 const before=JSON.stringify(bindings),a=buildRegionalAssets(THREE,bindings,()=>2);
 try {
  const w=a.water.find(w=>w.kind==='swamp'),s=w.material.fragmentShader,v=w.material.vertexShader;
  const region=s.slice(s.indexOf('float islandLap=0.;'),s.indexOf('vec3 islandSheen'));
  for(const part of ['vec2 lapGradient=24.*delta/max(islandRadius,.00001)','+2.*vec2(-delta.y,delta.x)/max(dot(delta,delta),.00001)','abs(dot(lapGradient,dFdx(delta)))','abs(dot(lapGradient,dFdy(delta)))','*(1.-smoothstep(.35,1.15,lapFootprint))'])assert.ok(region.includes(part),part);
  assert.doesNotMatch(region,/fwidth\(lapPhase\)/);
  assert.doesNotMatch(v,/lapGradient|lapFootprint/);
  assert.match(v,/p\.z\+=\.007\*islandLap\*shoreHold/);
  assert.equal(w.material.uniforms.uIslandSiteCount.value,4);
  assert.equal(w.mesh.geometry.getAttribute('position').count,385);
  for(const other of a.water.filter(x=>x.kind!=='swamp'))assert.equal(other.material.uniforms.uIslandSiteCount?.value??0,0);
  a.tick(2,{globalCalm:true,storm:0});a.tick(5,{globalCalm:true,storm:0});assert.equal(w.material.uniforms.uTime.value,5);
  a.tick(9,{globalCalm:true,storm:0,paused:true});assert.equal(w.material.uniforms.uTime.value,5);
  assert.equal(a.worldMutationAllowed,false);assert.deepEqual(a.principalCharacters,[]);assert.equal(JSON.stringify(bindings),before);
 }finally{a.dispose();}
});
const smooth=(a,b,x)=>{const q=Math.max(0,Math.min(1,(x-a)/(b-a)));return q*q*(3-2*q);};
const phase=(x,y,t)=>24*Math.hypot(x,y)-t*1.85+2*Math.atan2(y,x);
const gradient=(x,y)=>{const r=Math.hypot(x,y);return [24*x/r-2*y/(r*r),24*y/r+2*x/(r*r)];};
const gain=(x,y,h)=>{const g=gradient(x,y);return 1-smooth(.35,1.15,h*(Math.abs(g[0])+Math.abs(g[1])));};
test('island gradient preserves resolved crest movement and suppresses coarse samples without angular seam',()=>{
 let n=0,coarse=0,motion=0;
 for(let i=0;i<120;i++)for(const r of [.87,.97,1.04,1.21])for(const t of [0,2,6]){
  const theta=i*Math.PI/60,x=r*Math.cos(theta),y=r*Math.sin(theta);
  const g=gradient(x,y),h=1e-5;
  // Circular difference removes the atan branch cut without affecting local derivatives.
  const diff=(a,b)=>Math.atan2(Math.sin(a-b),Math.cos(a-b));
  assert.ok(Math.abs(diff(phase(x+h,y,t),phase(x-h,y,t))/(2*h)-g[0])<1e-6);
  assert.ok(Math.abs(diff(phase(x,y+h,t),phase(x,y-h,t))/(2*h)-g[1])<1e-6);
  const near=gain(x,y,.002),far=gain(x,y,.06);
  assert.equal(near,1);n++;if(far<.1)coarse++;
  const crest=time=>Math.max(Math.sin(phase(x,y,time)),0)**4;
  motion=Math.max(motion,near*Math.abs(crest(t)-crest(t+.4)));
 }
 assert.equal(coarse,n);assert.ok(motion>.1);
 assert.ok(Math.abs(gain(-1,1e-6,.02)-gain(-1,-1e-6,.02))<1e-5);
 console.log('island contact samples',n,'coarse suppressed',coarse,'resolved motion',motion);
});
