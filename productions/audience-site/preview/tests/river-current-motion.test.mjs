import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {canvasWaterDisplacement,riverCurrentRipple,riverCurrentSlope,nextWaterPhase,buildWorldGeometry} from '../renderer.mjs';
const source=readFileSync(new URL('../renderer.mjs',import.meta.url),'utf8');
const riverX=z=>7+7*Math.sin(z*.034)+3*Math.sin(z*.091);

test('current only moves ordinary water inside existing illustrative river trough',()=>{
 for(const z of [-80,-54,-45,-40,0,30,85])for(const t of [0,2.5,9])for(const off of [0,3,9,30]){
  const ripple=riverCurrentRipple(riverX(z)+off,z,t);
  assert.ok(Number.isFinite(ripple));
  assert.ok(Math.abs(ripple)<=.05500000001);
  if(z<=-54)assert.equal(ripple,0);
 }
 assert.ok(Math.abs(riverCurrentRipple(riverX(25),25,0)-riverCurrentRipple(riverX(25),25,1))>.01);
 assert.ok(Math.abs(riverCurrentRipple(riverX(30)+30,30,2))<1e-10);
});

test('analytic optical slopes agree with physical displaced ripples',()=>{
 const h=1e-4;
 for(const z of [-70,-47,-35,10,70])for(const off of [-7,0,4])for(const t of [0,3]){
  const x=riverX(z)+off;
  const [dx,dz]=riverCurrentSlope(x,z,t);
  const nx=(riverCurrentRipple(x+h,z,t)-riverCurrentRipple(x-h,z,t))/(2*h);
  const nz=(riverCurrentRipple(x,z+h,t)-riverCurrentRipple(x,z-h,t))/(2*h);
  assert.ok(Math.abs(dx-nx)<1e-8);
  assert.ok(Math.abs(dz-nz)<1e-8);
 }
});

test('Canvas fallback uses same travelling river displacement and slope lighting',()=>{
 for(const z of [-70,25])for(const t of [0,1.1,4.4]){
  const x=riverX(z)+2;
  const standing=Math.sin(x*.21+t*.55)*.11+Math.sin(z*.31+t*.34)*.07;
  assert.ok(Math.abs(canvasWaterDisplacement(x,z,t)-standing-riverCurrentRipple(x,z,t))<1e-12);
 }
 assert.match(source,/const \[currentX,currentZ\]=riverCurrentSlope\(x,z,waterFrame\)/);
 assert.match(source,/canvasWaterDisplacement\(p\[0\],p\[2\],waterFrame\)/);
});

test('native shader displaces river and shades matched analytic current normals',()=>{
 assert.match(source,/float riverCurrent\(float x,float z,float t\)/);
 assert.match(source,/\+riverCurrent\(p\.x,p\.z,uTime\)/);
 assert.match(source,/vec2 riverSlope\(float x,float z,float t\)/);
 assert.match(source,/currentSlope=riverSlope\(vWorld\.x,vWorld\.z,uTime\)/);
 assert.match(source,/gl\.uniform1f\(loc\.uTime,waterTime\)/);
 assert.match(source,/waterTime=nextWaterPhase\(waterTime,time,paused\)/);
});

test('existing water domain, pause and weather boundaries are unchanged',()=>{
 assert.equal(nextWaterPhase(6,20,true),6);
 assert.equal(nextWaterPhase(6,20,false),20);
 const geom=buildWorldGeometry([],8,0,{waterCellSize:8});
 assert.equal(geom.water.values.length/9,38400);
 assert.ok(geom.water.values.every(Number.isFinite));
 assert.throws(()=>riverCurrentRipple(0,0,Infinity),/INVALID_RIVER_CURRENT_POSITION/);
 assert.throws(()=>riverCurrentSlope(NaN,0,2),/INVALID_RIVER_CURRENT_POSITION/);
 assert.match(source,/gl\.uniform1f\(loc\.uStorm,storm\)/);
 assert.match(source,/waterTime=nextWaterPhase\(waterTime,time,paused\)/);
});
