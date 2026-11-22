import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createWorldRenderer,nextWaterPhase,waterSheenDrift} from '../renderer.mjs';

test('existing fallback-water glints move with ordinary time, not weather; offset remains bounded',()=>{
 for(const index of [0,1,13,109]){
  const offsets=[0,1.125,3.75,9.25].map(t=>waterSheenDrift(index,t));
  assert.ok(offsets.every(n=>Number.isFinite(n)&&Math.abs(n)<=.65));
  assert.notEqual(offsets[0],offsets[1]);
 }
 for(const bad of [NaN,Infinity,-Infinity,'2',undefined])
  assert.throws(()=>waterSheenDrift(2,bad),/INVALID_WATER_SHEEN_PHASE/);
 for(const index of [-1,1.5,NaN])
  assert.throws(()=>waterSheenDrift(index,0),/INVALID_WATER_SHEEN_PHASE/);
 const calm=nextWaterPhase(.125,.5,false);
 assert.notEqual(waterSheenDrift(2,calm),waterSheenDrift(2,.125));
 assert.equal(nextWaterPhase(calm,50,true),calm,'Only explicit pause holds ordinary water');
});

test('actual Canvas fallback redraws moving water during calm but holds exact scene on pause',()=>{
 const before=globalThis.devicePixelRatio;
 globalThis.devicePixelRatio=1;
 let draws=0;
 const gradient={addColorStop(){}};
 const ctx={
  createLinearGradient(){return gradient;},setTransform(){},fillRect(){draws++;},
  beginPath(){},moveTo(){},lineTo(){},closePath(){},fill(){},stroke(){}
 };
 const canvas={
  clientWidth:900,clientHeight:650,width:0,height:0,
  getContext(type){return type==='2d'?ctx:null;}
 };
 let renderer;
 try{
  renderer=createWorldRenderer(canvas,[],{});
  assert.equal(renderer.stats.renderer,'canvas2d-spatial-fallback');
  const camera={target:[0,2,50],distance:190,yaw:.2,pitch:.17};
  renderer.render(camera,.125,{strength:1,storm:0,paused:false});
  assert.equal(draws,1);
  renderer.render(camera,.20,{strength:1,storm:0,paused:false});
  assert.equal(draws,1,'Sub-frame water time is capped for Canvas efficiency');
  renderer.render(camera,.50,{strength:1,storm:0,paused:false});
  assert.equal(draws,2,'Global calm (storm zero) cannot freeze ordinary water');
  renderer.render(camera,7,{strength:1,storm:0,paused:true});
  renderer.render(camera,10,{strength:1,storm:0,paused:true});
  assert.equal(draws,2,'Repeated pause renders must keep previous pixels');
  renderer.render(camera,.75,{strength:1,storm:0,paused:false});
  assert.equal(draws,3,'Resume uses the observer clock, not the paused argument');
  renderer.render(camera,.75,{strength:.8,storm:0,paused:false});
  assert.equal(draws,4,'Atmosphere changes do not grant authority over water phase');
 }finally{
  renderer?.dispose();
  if(before===undefined)delete globalThis.devicePixelRatio;
  else globalThis.devicePixelRatio=before;
 }
});

test('fallback edit does not alter canonical source, Three renderer or native WebGL water path',()=>{
 const source=readFileSync(new URL('../renderer.mjs',import.meta.url),'utf8');
 assert.match(source,/lastWater=nextWaterPhase\(lastWater,time,paused\)/);
 assert.match(source,/storm,waterFrame\]/);
 assert.match(source,/waterSheenDrift\(i,waterFrame\)/);
 assert.match(source,/gl\.uniform1f\(loc\.uTime,waterTime\)/);
 assert.match(source,/const ratio=Math\.min\(devicePixelRatio\|\|1,1\.6\)/);
 assert.doesNotMatch(source,/fetch\(|writeWorldState|publishObserver|createPrincipalCharacter/);
});
