import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {riverFlowSheen,nextWaterPhase,riverCurrentRipple,buildWorldGeometry} from '../renderer.mjs';

const source=readFileSync(new URL('../renderer.mjs',import.meta.url),'utf8');
const channel=z=>7+7*Math.sin(z*.034)+3*Math.sin(z*.091);
const glslSheen=(x,z,t)=>{
 const d=x-channel(z),gate=Math.min(1,Math.max(0,(z+54)/14));
 return Math.exp(-(d*d)/58)*gate*Math.pow(.5+.5*Math.cos(z*.74+x*.12-t*1.25),8);
};

test('new river glint is finite, deterministic and bounded to the existing trough',()=>{
 for(const z of [-100,-54,-47,-40,0,35,85])for(const offset of [0,2,12,50])for(const t of [0,.5,2,10]){
  const sheen=riverFlowSheen(channel(z)+offset,z,t);
  assert.ok(Number.isFinite(sheen));
  assert.ok(sheen>=0 && sheen<=1+1e-12);
  assert.ok(Math.abs(sheen-glslSheen(channel(z)+offset,z,t))<1e-12);
  if(z<=-54)assert.equal(sheen,0);
  if(offset===50)assert.ok(sheen<1e-15);
 }
 assert.notEqual(riverFlowSheen(channel(35),35,0),riverFlowSheen(channel(35),35,1));
 for(const bad of [[NaN,0,0],[0,Infinity,0],[0,0,NaN]])assert.throws(()=>riverFlowSheen(...bad),/INVALID_RIVER_CURRENT_POSITION/);
});

test('native shader applies a low-energy water-only, ordinary-clock river optic',()=>{
 assert.match(source,/float riverSheen\(float x,float z,float t\)/);
 assert.match(source,/riverSheen\(vWorld\.x,vWorld\.z,uTime\)\*\.048\*uStrength/);
 assert.match(source,/if\(uWater>\.5\)\{vec3 view=normalize\(uEye-vWorld\)/);
 assert.match(source,/gl\.uniform1f\(loc\.uTime,waterTime\)/);
 assert.match(source,/waterTime=nextWaterPhase\(waterTime,time,paused\)/);
 assert.doesNotMatch(source,/riverSheen\([^)]*uStorm/);
});

test('Canvas fallback uses identical flow clock and bounded color increment',()=>{
 assert.match(source,/const riverGlint=riverFlowSheen\(x,z,waterFrame\)/);
 assert.match(source,/riverGlint\*\[6,8,7\]\[i\]\*strength/);
 assert.match(source,/const waterFrame=Math\.floor\(lastWater\*8\)\/8/);
 const t=2.125,x=channel(38),z=38;
 assert.ok(riverFlowSheen(x,z,t)>0);
 assert.equal(nextWaterPhase(t,12,true),t);
 assert.equal(nextWaterPhase(t,12,false),12);
 assert.equal(riverFlowSheen(x,z,nextWaterPhase(t,12,true)),riverFlowSheen(x,z,t));
 assert.notEqual(riverFlowSheen(x,z,12),riverFlowSheen(x,z,t));
});

test('river shading does not change canonical places, water surface or weather domain',()=>{
 const old=riverCurrentRipple(channel(30),30,2);
 assert.ok(Math.abs(old)<.056);
 const g=buildWorldGeometry([],8,0,{waterCellSize:8});
 assert.equal(g.water.values.length/9,38400);
 assert.ok(g.water.values.every(Number.isFinite));
 assert.match(source,/waterTime=nextWaterPhase\(waterTime,time,paused\)/);
 assert.match(source,/gl\.uniform1f\(loc\.uStorm,storm\)/);
});
