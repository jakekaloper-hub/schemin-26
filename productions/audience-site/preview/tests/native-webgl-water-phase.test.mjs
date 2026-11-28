import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {nextWaterPhase} from '../renderer.mjs';

test('native WebGL fallback ordinary-water phase holds at the observed timestamp across explicit pause',()=>{
 let phase=nextWaterPhase(0,1.25,false);
 assert.equal(phase,1.25);
 phase=nextWaterPhase(phase,4.75,false);
 assert.equal(phase,4.75);
 phase=nextWaterPhase(phase,40,true);
 assert.equal(phase,4.75,'pause must not snap animated water back to zero');
 phase=nextWaterPhase(phase,93,true);
 assert.equal(phase,4.75,'pause must remain stable after repeated frames');
 assert.equal(nextWaterPhase(phase,5.25,false),5.25,'resume follows the existing observer clock');
});

test('synthetic global calm changes atmospheric inputs, never the ordinary-water phase',()=>{
 let phase=0;
 for(const [time,weather] of [[.5,{strength:1,storm:3}],[1.75,{strength:.9,storm:0}],[2.9,{strength:.7,storm:0}]]){
  // Weather deliberately is not an input to the source-independent phase helper.
  assert.ok(Number.isFinite(weather.strength)&&Number.isFinite(weather.storm));
  phase=nextWaterPhase(phase,time,false);
  assert.equal(phase,time);
 }
 assert.equal(nextWaterPhase(phase,20,true),2.9);
});

test('water clock rejects invalid numbers instead of injecting NaN into the GPU',()=>{
 for(const bad of [NaN,Infinity,-Infinity,undefined,'1']){
  assert.throws(()=>nextWaterPhase(bad,2,false),/INVALID_WATER_PHASE/);
  assert.throws(()=>nextWaterPhase(1,bad,true),/INVALID_WATER_PHASE/);
 }
 assert.equal(nextWaterPhase(0,0,true),0);
});

test('native WebGL render path sends held ordinary time, not zero, to its existing GLSL uTime',()=>{
 const source=readFileSync(new URL('../renderer.mjs',import.meta.url),'utf8');
 assert.match(source,/let vp,eye,disposed=false,waterTime=0;/);
 assert.match(source,/waterTime=nextWaterPhase\(waterTime,time,paused\)/);
 assert.match(source,/gl\.uniform1f\(loc\.uTime,waterTime\)/);
 assert.doesNotMatch(source,/gl\.uniform1f\(loc\.uTime,paused\?0:time\)/);
 assert.match(source,/if\(uWater>\.5\)p\.y\+=sin\(p\.x\*\.21\+uTime\*\.55\)/);
 assert.match(source,/if\(uWater>\.5\)\{float slopeX=/);
 assert.match(source,/currentSlope=riverSlope\(vWorld\.x,vWorld\.z,uTime\)/);
 assert.match(source,/n=normalize\(vec3\(-slopeX-currentSlope\.x,1\.,-slopeZ-currentSlope\.y\)\)/);
 // This fix affects only native fallback; the source-bound Three and regional assets stay untouched.
 assert.doesNotMatch(source,/fetch\(|writeWorldState|publishObserver|createPrincipalCharacter/);
});
