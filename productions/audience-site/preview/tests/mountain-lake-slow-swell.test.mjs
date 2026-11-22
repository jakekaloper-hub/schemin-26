import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {projectAtlas} from '../../src/observer-world.mjs';
import {spatialBindings} from '../spatial.mjs';
import {buildAtlasSiteAssets} from '../atlas-site-assets.mjs';

const catalog=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const bindings=spatialBindings({locations:projectAtlas(catalog.locations)});
const original=JSON.stringify(bindings);
const build=()=>buildAtlasSiteAssets(THREE,bindings,()=>4);
const smooth=(a,b,x)=>{const t=Math.max(0,Math.min(1,(x-a)/(b-a)));return t*t*(3-2*t);};
const height=(x,y,t,amplitude,bridge)=> {
 const interior=1-smooth(.58,.95,Math.hypot(x,y));
 const waveA=Math.sin(x*12.7-t*1.18+Math.sin(y*7.5)*.45);
 const waveB=Math.sin(y*10.2+t*.74+x*3);
 const baseWave=.72*waveA+.28*waveB;
 const swell=Math.sin(x*5.25+y*3.35-t*.53+Math.sin(y*1.8)*.16);
 return amplitude*interior*(baseWave*(1-.22*bridge)+bridge*.22*swell);
};

test('source-exact Mountain Lake alone blends a slow physical swell into existing water mesh',()=>{
 const a=build(),lake=a.water.find(w=>w.kind==='mountain lake');
 assert.ok(lake);
 assert.equal(a.water.length,4);
 assert.equal(a.locations.length,20);
 assert.ok(a.locations.find(l=>l.id==='LOC-BRIDGE-MOUNTAIN-LAKE').group.children.includes(lake.mesh));
 assert.equal(a.water.filter(w=>w.material.uniforms.uBridge.value===1).length,1);
 for(const w of a.water){
  const shader=w.material.vertexShader;
  assert.ok(shader.includes('float lakeSwell=sin(position.x*5.25+position.y*3.35-uTime*.53+sin(position.y*1.8)*.16);'));
  assert.ok(shader.includes('p.z+=uAmplitude*interior*(.72*waveA+.28*waveB);'));
  assert.ok(shader.includes('p.z+=uBridge*uAmplitude*interior*.22*(lakeSwell-(.72*waveA+.28*waveB));'));
  assert.ok(shader.includes('vWorld=(modelMatrix*vec4(p,1.)).xyz;'));
  assert.ok(w.material.fragmentShader.includes('cross(dFdx(vWorld),dFdy(vWorld))'));
  assert.equal(w.mesh.geometry.getAttribute('position').count,393);
  assert.equal(w.mesh.geometry.index.count,2184);
  assert.equal(w.material.uniforms.uBridge.value,w===lake?1:0);
  assert.equal(w.mesh.children.length,0);
 }
 assert.equal(a.weatherMutationAllowed,false);
 assert.equal(a.worldMutationAllowed,false);
 assert.deepEqual(a.principalCharacters,[]);
 assert.equal(JSON.stringify(bindings),original);
 a.dispose();
});

test('Lake swell moves while global weather is calm, stops on pause and cannot shift original rim',()=>{
 const a=build(),lake=a.water.find(w=>w.kind==='mountain lake');
 const amp=lake.material.uniforms.uAmplitude.value;
 assert.ok(amp>0&&amp<=.03);
 let changed=0,slowDifference=0;
 for(let i=-20;i<=20;i++)for(let j=-20;j<=20;j++){
  const x=i/25,y=j/25,r=Math.hypot(x,y);
  const t1=height(x,y,1.0,amp,1),t2=height(x,y,2.8,amp,1);
  const base=height(x,y,1.0,amp,0);
  for(const h of [t1,t2,base])assert.ok(Number.isFinite(h)&&Math.abs(h)<=amp+1e-9);
  if(r>=.95){assert.ok(Math.abs(t1)<1e-12);assert.ok(Math.abs(t2)<1e-12);}
  changed=Math.max(changed,Math.abs(t1-t2));
  slowDifference=Math.max(slowDifference,Math.abs(t1-base));
 }
 assert.ok(changed>.008,'water actually changes over time');
 assert.ok(slowDifference>.001,'lake geometry differs from inherited other-water phase');
 const positions=Array.from(lake.mesh.geometry.getAttribute('position').array);
 for(let i=1+56*6;i<393;i++){
  const attr=lake.mesh.geometry.getAttribute('position');
  assert.ok(Math.abs(Math.hypot(attr.getX(i),attr.getY(i))-1)<1e-6);
  assert.equal(attr.getZ(i),0);
 }
 a.tick(1,{globalCalm:true,storm:0});
 a.tick(2.8,{globalCalm:true,storm:0});
 assert.equal(lake.material.uniforms.uTime.value,2.8);
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===2.8));
 a.tick(10,{paused:true,globalCalm:true,storm:0});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===2.8));
 assert.deepEqual(Array.from(lake.mesh.geometry.getAttribute('position').array),positions);
 assert.equal(JSON.stringify(bindings),original);
 let released=0;
 lake.mesh.geometry.addEventListener('dispose',()=>released++);
 lake.material.addEventListener('dispose',()=>released++);
 a.dispose();a.dispose();a.tick(11);
 assert.equal(released,2);
 assert.equal(lake.material.uniforms.uTime.value,2.8);
});
