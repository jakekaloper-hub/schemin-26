import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {canvasWaterDisplacement,nextWaterPhase,waterSheenDrift} from '../renderer.mjs';

const source=readFileSync(new URL('../renderer.mjs',import.meta.url),'utf8');
const sheenLine=source.split('\n').find(line=>line.includes('for(let i=0;i<110;i++){'));
assert.ok(sheenLine,'Use the actual existing Canvas sheen loop, not a duplicate implementation');
const drawSheen=new Function('hash','height','waterSheenDrift','canvasWaterDisplacement','waterFrame','project','ctx',sheenLine);
const hash=(x,y)=>{const value=Math.sin(x*127.1+y*311.7)*43758.5453;return value-Math.floor(value);};

function capture(phase,groundHeight=()=>-1){
 const points=[],strokes=[];
 const ctx={beginPath(){},moveTo(){},lineTo(){},stroke(){strokes.push(1);}};
 drawSheen(hash,groundHeight,waterSheenDrift,canvasWaterDisplacement,phase,
  p=>{points.push([...p]);return {x:p[0],y:p[1]};},ctx);
 return {points,strokes};
}

test('both ends of all 110 existing fallback glints follow the physically animated water surface',()=>{
 assert.match(sheenLine,/const endX=x\+1\+hash\(i,1\)\*2/);
 assert.match(sheenLine,/project\(\[x,-\.4\+canvasWaterDisplacement\(x,z,waterFrame\),z\]\)/);
 assert.match(sheenLine,/project\(\[endX,-\.4\+canvasWaterDisplacement\(endX,z,waterFrame\),z\]\)/);
 assert.doesNotMatch(sheenLine,/project\(\[x,-\.3,z\]\)/);
 for(const t of [.125,.625,2.375]){
  const {points,strokes}=capture(t);
  assert.equal(points.length,220);
  assert.equal(strokes.length,110,'No new glints, sprites or draw passes');
  for(let i=0;i<110;i++){
   const a=points[2*i],b=points[2*i+1];
   const z=hash(i,11)*170+35;
   const x=hash(i,7)*250-125+waterSheenDrift(i,t);
   const endX=x+1+hash(i,1)*2;
   assert.ok(Math.abs(a[0]-x)<1e-10&&Math.abs(b[0]-endX)<1e-10);
   assert.equal(a[2],z);assert.equal(b[2],z);
   for(const p of [a,b]){
    assert.ok(Math.abs(p[1]-(-.4+canvasWaterDisplacement(p[0],p[2],t)))<1e-12);
    assert.ok(Math.abs(p[1]+.4)<=.235000001,'Original .18 standing plus bounded .055 river ripple');
   }
  }
 }
});

test('existing ground-height water mask still suppresses every sheen stroke over non-water terrain',()=>{
 const visible=capture(.625,()=>-1),masked=capture(.625,()=>3);
 assert.equal(visible.strokes.length,110);
 assert.equal(masked.strokes.length,0);
 assert.equal(masked.points.length,0);
});

test('global calm retains ordinary shimmer travel, but explicit pause fixes the exact surface',()=>{
 const t=nextWaterPhase(.125,.875,false),held=nextWaterPhase(t,90,true);
 assert.equal(t,.875);assert.equal(held,t);
 assert.deepEqual(capture(t),capture(held));
 const moving=capture(1.375);
 assert.notDeepEqual(capture(t).points,moving.points);
 assert.match(source,/lastWater=nextWaterPhase\(lastWater,time,paused\)/);
 assert.match(source,/const waterFrame=Math.floor\(lastWater\*8\)\/8/);
 assert.match(source,/gl\.uniform1f\(loc\.uTime,waterTime\)/);
 assert.match(source,/gl\.uniform1f\(loc\.uStorm,storm\)/);
 assert.match(source,/for\(let i=0;i<110;i\+\+\)/);
 assert.doesNotMatch(source,/fetch\(|writeWorldState|publishObserver|createPrincipalCharacter/);
});
