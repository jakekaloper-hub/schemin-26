import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {nextWaterPhase} from '../renderer.mjs';

const source=readFileSync(new URL('../renderer.mjs',import.meta.url),'utf8');
const vertex=source.split('const VS=\x60')[1]?.split('\x60;')[0];
const fragment=source.split('const FS=\x60')[1]?.split('\x60;')[0];
const height=(x,z,time)=>.11*Math.sin(x*.21+time*.55)+.07*Math.sin(z*.31+time*.34);
function normal(x,z,time){
 const sx=.11*.21*Math.cos(x*.21+time*.55);
 const sz=.07*.31*Math.cos(z*.31+time*.34);
 const magnitude=Math.hypot(sx,1,sz);
 return [-sx/magnitude,1/magnitude,-sz/magnitude];
}

test('secondary native WebGL water surface normal shares both original vertex-wave phases and coefficients',()=>{
 assert.ok(vertex&&fragment,'Original shader sources are present');
 assert.ok(vertex.includes('if(uWater>.5)p.y+=sin(p.x*.21+uTime*.55)*.11+sin(p.z*.31+uTime*.34)*.07;'));
 assert.ok(fragment.includes('float slopeX=.11*.21*cos(vWorld.x*.21+uTime*.55);'));
 assert.ok(fragment.includes('float slopeZ=.07*.31*cos(vWorld.z*.31+uTime*.34);'));
 assert.ok(fragment.includes('n=normalize(vec3(-slopeX,1.,-slopeZ));'));
 assert.ok(!fragment.includes('sin(vWorld.x*.31+uTime*.55)*.12'),'Old unrelated optical normal must be removed');
 assert.ok(fragment.includes('dot(view,n)')&&fragment.includes('reflect(-normalize(uSun),n)'),'Fresnel and sparkle share the physical normal');
});

test('analytic normals agree with finite differences of real displaced water vertices',()=>{
 for(const [x,z,t] of [[0,0,0],[3,-7,1.9],[-12,6.4,3.8],[45,29,9.1]]){
  const h=.0001;
  const dx=(height(x+h,z,t)-height(x-h,z,t))/(2*h);
  const dz=(height(x,z+h,t)-height(x,z-h,t))/(2*h);
  const expected=[-dx,1,-dz];
  const m=Math.hypot(...expected),normalized=expected.map(v=>v/m);
  const actual=normal(x,z,t);
  for(let i=0;i<3;i++)assert.ok(Math.abs(actual[i]-normalized[i])<1e-9,'Normal mismatch at '+x+','+z+','+t+' index '+i);
  assert.ok(Math.abs(Math.hypot(...actual)-1)<1e-12,'Normal must be unit length');
  assert.ok(actual[1]>.999,'Water surface remains nearly horizontal; no fictitious steep wave');
 }
 assert.ok(Math.hypot(...normal(0,0,0).map((v,i)=>v-normal(0,0,4)[i]))>.03,'Normal moves with the actual water phase');
});

test('weather calm does not freeze ordinary water; only explicit pause holds shared phase',()=>{
 assert.ok(source.includes('waterTime=nextWaterPhase(waterTime,time,paused);'));
 assert.ok(source.includes('gl.uniform1f(loc.uTime,waterTime);'));
 assert.ok(source.includes('gl.uniform1f(loc.uStorm,storm);'));
 assert.ok(!vertex.includes('uStorm')&&!fragment.includes('uGlobalCalm'),'Wave phase is not storm-authorized');
 const duringCalm=nextWaterPhase(1,2.75,false);
 assert.equal(duringCalm,2.75);
 assert.equal(nextWaterPhase(duringCalm,9.5,true),duringCalm);
 assert.equal(nextWaterPhase(duringCalm,10.5,false),10.5);
 assert.ok(source.includes('gl.drawArrays(gl.TRIANGLES,0,ocean.count);'),'Original water draw budget remains');
});