import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {projectAtlas} from '../../src/observer-world.mjs';
import {spatialBindings} from '../spatial.mjs';
import {buildAtlasSiteAssets} from '../atlas-site-assets.mjs';

const source=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const bindings=spatialBindings({locations:projectAtlas(source.locations)});
const original=JSON.stringify(bindings), build=()=>buildAtlasSiteAssets(THREE,bindings,()=>4);
const eligible=new Set(['mountain lake','mire','sheltered port','watercourse crossing']);
function smoothstep(a,b,x){const t=Math.max(0,Math.min(1,(x-a)/(b-a)));return t*t*(3-2*t);}
function phase(kind,x,y,time){return kind==='crossing'?y*72-time*2.1+Math.sin(x*16)*.55:x*52+Math.sin(y*19)*.9-time*.7;}
function footprint(kind,x,y,time,step){const p=phase(kind,x,y,time);return Math.abs(phase(kind,x+step,y,time)-p)+Math.abs(phase(kind,x,y+step,time)-p);}
const attenuate=width=>1-smoothstep(.35,1.15,width);

test('existing four source-bound moving water disks retain geometry, uniforms and authority',()=>{
 const a=build();assert.equal(a.locations.length,20);assert.equal(a.water.length,4);
 assert.deepEqual(new Set(a.water.map(w=>w.kind)),eligible);
 for(const water of a.water){
  assert.equal(water.mesh.geometry.getAttribute('position').count,393);
  assert.equal(water.mesh.geometry.index.count,2184);
  assert.equal(water.mesh.children.length,0);
  assert.equal(Object.keys(water.material.uniforms).length,9,'no new GLSL uniforms');
  assert.equal(water.material.depthWrite,false);
  assert.equal(water.material.transparent,true);
 }
 assert.equal(a.water.filter(w=>w.material.uniforms.uCrossing.value===1).length,1);
 assert.equal(a.weatherMutationAllowed,false);
 assert.equal(a.worldMutationAllowed,false);
 assert.deepEqual(a.principalCharacters,[]);
 assert.equal(JSON.stringify(bindings),original);
 a.dispose();
});

test('derivative footprint attenuates only painted moving streaks, not the physically displaced wave',()=>{
 const a=build();
 for(const water of a.water){
  const vs=water.material.vertexShader,fs=water.material.fragmentShader;
  for(const term of ['float linePhase=vUv.x*52.+sin(vUv.y*19.)*.9-uTime*.7;',
   'float lineFootprint=fwidth(linePhase);',
   'float line=pow(max(sin(linePhase),0.),17.)*(1.-smoothstep(.35,1.15,lineFootprint));',
   'float crossingPhase=vUv.y*72.-uTime*2.1+sin(vUv.x*16.)*.55;',
   'float crossingFootprint=fwidth(crossingPhase);',
   'float crossingSheen=uCrossing*pow(max(sin(vUv.y*72.-uTime*2.1+sin(vUv.x*16.)*.55),0.),18.)',
   'crossingSheen*=1.-smoothstep(.35,1.15,crossingFootprint);'])
    assert.ok(fs.includes(term),term);
  assert.ok(vs.includes('p.z+=uAmplitude*interior*(.72*waveA+.28*waveB);'),'physical water displacement preserved');
  assert.ok(vs.includes('p.z+=uCrossing*uAmplitude*.34*interior*crossingWave;'),'crossing displacement preserved');
  assert.ok(!vs.includes('fwidth('),'raster footprint stays in fragment shader');
  assert.ok(!fs.includes('uGlobalCalm')&&!fs.includes('uStorm'),'weather policy remains upstream');
 }
 a.dispose();
});

test('high-detail reflection survives close view but fades when subpixel; ordinary time continues under global calm',()=>{
 const x=.33,y=.27;
 for(const kind of ['line','crossing']){
  const near=attenuate(footprint(kind,x,y,1.2,.002));
  const far=attenuate(footprint(kind,x,y,1.2,.05));
  assert.ok(near>.9,kind+': close optical detail remains visible');
  assert.ok(far<.01,kind+': subpixel detail fades');
  assert.ok(near<=1&&far>=0&&Number.isFinite(near)&&Number.isFinite(far));
  assert.ok(Math.abs(Math.sin(phase(kind,x,y,1.2))-Math.sin(phase(kind,x,y,3.7)))>.2,kind+': ordinary time advances phase');
  assert.ok(Math.abs(footprint(kind,x,y,1.2,.002)-footprint(kind,x,y,3.7,.002))<1e-12,'distance attenuation is clock-independent within floating-point precision');
 }
 const a=build();
 a.tick(1.2,{globalCalm:true,storm:0});a.tick(3.7,{globalCalm:true,storm:0});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===3.7));
 a.tick(9,{paused:true});assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===3.7));
 assert.equal(JSON.stringify(bindings),original);
 a.dispose();
});
