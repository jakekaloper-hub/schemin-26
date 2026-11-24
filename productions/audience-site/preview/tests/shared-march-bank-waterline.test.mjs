import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {projectAtlas} from '../../src/observer-world.mjs';
import {spatialBindings} from '../spatial.mjs';
import {buildAtlasSiteAssets} from '../atlas-site-assets.mjs';

const source=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const bindings=spatialBindings({locations:projectAtlas(source.locations)});
const unchanged=JSON.stringify(bindings);
const build=()=>buildAtlasSiteAssets(THREE,bindings,()=>4);
function smooth(a,b,x){const t=Math.max(0,Math.min(1,(x-a)/(b-a)));return t*t*(3-2*t);}
function bankWake(x,y,time,step=.002,gate=1){
 const phase=(px,py)=>py*18.8-time*2.1+Math.sin(px*5)*.55;
 const footprint=Math.abs(phase(x+step,y)-phase(x,y))+Math.abs(phase(x,y+step)-phase(x,y));
 return gate*smooth(.55,.67,Math.abs(y))*(1-smooth(.76,.87,Math.abs(y)))
  *(1-smooth(.78,.93,Math.hypot(x,y)))
  *Math.pow(Math.max(Math.sin(phase(x,y)),0),4)*(1-smooth(.35,1.15,footprint));
}

test('Shared March alone has the bank-waterline gate; all Atlas places and four original water meshes survive',()=>{
 const a=build(),place=a.locations.find(x=>x.id==='LOC-TDS-CHILI-SHARED-MARCH');
 const river=a.water.find(x=>x.kind==='watercourse crossing');
 assert.ok(place&&river&&place.group.children.includes(river.mesh));
 assert.ok(source.locations.find(x=>x.id===place.id).persistent_landmarks.includes('watercourse crossing'));
 assert.equal(a.locations.length,20);assert.equal(a.water.length,4);
 assert.deepEqual(a.water.filter(w=>w.material.uniforms.uCrossing.value===1).map(w=>w.kind),['watercourse crossing']);
 for(const w of a.water){
  assert.equal(w.mesh.geometry.getAttribute('position').count,393);
  assert.equal(w.mesh.geometry.index.count,2184);
  assert.equal(w.mesh.children.length,0);
  assert.deepEqual(Object.keys(w.material.uniforms).sort(),['uAmplitude','uBarrier','uBridge','uColor','uCrossing','uLakeGlint','uLightLevel','uMire','uTime','uViewSheen']);
  assert.equal(w.material.transparent,true);
  assert.equal(w.material.depthWrite,false);
 }
 assert.equal(a.worldMutationAllowed,false);assert.equal(a.weatherMutationAllowed,false);
 assert.deepEqual(a.principalCharacters,[]);
 assert.equal(JSON.stringify(bindings),unchanged);a.dispose();
});

test('bank glints read the unchanged physically displaced crossing phase and fade below a pixel',()=>{
 const a=build(),river=a.water.find(w=>w.kind==='watercourse crossing');
 const vertex=river.material.vertexShader,fragment=river.material.fragmentShader;
 for(const token of [
  'float crossingWave=sin(position.y*18.8-uTime*2.1+sin(position.x*5.)*.55);',
  'p.z+=uCrossing*uAmplitude*.34*interior*crossingWave;'
 ])assert.ok(vertex.includes(token),token);
 for(const token of [
  'float bankPhase=bankXY.y*18.8-uTime*2.1+sin(bankXY.x*5.)*.55;',
  'float bankBand=smoothstep(.55,.67,bankY)*(1.-smoothstep(.76,.87,bankY));',
  'float bankInterior=1.-smoothstep(.78,.93,length(bankXY));',
  'float bankFootprint=fwidth(bankPhase);',
  'float bankWake=uCrossing*bankBand*bankInterior*pow(max(sin(bankPhase),0.),4.)*(1.-smoothstep(.35,1.15,bankFootprint));',
  'c=clamp(c+vec3(.035,.051,.041)*bankWake,0.,1.);'
 ])assert.ok(fragment.includes(token),token);
 assert.ok(!fragment.includes('uGlobalCalm')&&!fragment.includes('uStorm'));
 assert.deepEqual(Object.keys(river.material.uniforms).sort(),['uAmplitude','uBarrier','uBridge','uColor','uCrossing','uLakeGlint','uLightLevel','uMire','uTime','uViewSheen']);
 assert.ok(bankWake(0,.71,2.5,.002)>.8,'close moving bank glint must be readable');
 assert.ok(bankWake(0,.71,2.5,.09)<.001,'subpixel bank glint must fade');
 a.dispose();
});

test('bank pattern is bounded to original water interior and moves during synthetic global calm, stopping on explicit pause',()=>{
 let peak=0,moving=0;
 for(let xi=-15;xi<=15;xi++)for(let yi=-90;yi<=90;yi++){
  const x=xi*.04,y=yi*.01,p=bankWake(x,y,1.3),q=bankWake(x,y,3.2);
  assert.ok(Number.isFinite(p)&&Number.isFinite(q)&&p>=0&&p<=1&&q>=0&&q<=1);
  assert.equal(bankWake(x,y,1.3,.002,0),0,'other water has no Shared March bank wake');
  if(Math.hypot(x,y)>=.93)assert.ok(p<1e-12&&q<1e-12,'shoreline remains unchanged');
  peak=Math.max(peak,p,q);moving=Math.max(moving,Math.abs(p-q));
 }
 assert.ok(peak>.9&&moving>.6,'waterline changes with ordinary time');
 const a=build(),river=a.water.find(w=>w.kind==='watercourse crossing');
 a.tick(1.3,{globalCalm:true,storm:0});a.tick(3.2,{globalCalm:true,storm:0});
 assert.equal(river.material.uniforms.uTime.value,3.2);
 a.tick(8,{paused:true,globalCalm:true,storm:0});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===3.2));
 assert.equal(JSON.stringify(bindings),unchanged);a.dispose();
});
