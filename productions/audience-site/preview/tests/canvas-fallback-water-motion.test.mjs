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

test('Canvas density-only redraw preserves CSS projection and the paused water frame',()=>{
 const before=globalThis.devicePixelRatio;
 globalThis.devicePixelRatio=1;
 const transforms=[],frames=[],resizes=[0,0];let points=[],bw=0,bh=0;
 const gradient={addColorStop(){}};
 const ctx={
  createLinearGradient(){return gradient;},setTransform(...v){transforms.push(v);},
  fillRect(){points=[];frames.push(points);},beginPath(){},moveTo(x,y){if(points.length<80)points.push([x,y]);},
  lineTo(){},closePath(){},fill(){},stroke(){}
 };
 const canvas={clientWidth:901,clientHeight:651,
  get width(){return bw;},set width(v){bw=Math.floor(v);resizes[0]++;},
  get height(){return bh;},set height(v){bh=Math.floor(v);resizes[1]++;},
  getContext(type){return type==='2d'?ctx:null;}
 };
 let renderer;
 try{
  renderer=createWorldRenderer(canvas,[],{});
  const camera={target:[0,2,50],distance:190,yaw:.2,pitch:.17},held={strength:1,storm:0,paused:true};
  renderer.render(camera,.5,{...held,paused:false});
  const projection=renderer.project([0,0,50]),first=frames[0];
  assert.ok(first.length>0);
  assert.deepEqual([bw,bh],[901,651]);assert.deepEqual(resizes,[1,1]);
  globalThis.devicePixelRatio=2;
  renderer.render(camera,9,held);
  assert.deepEqual([bw,bh],[1351,976]);
  assert.deepEqual(transforms.at(-1),[1351/901,0,0,976/651,0,0]);
  assert.equal(frames.length,2);assert.deepEqual(frames[1],first);
  assert.deepEqual(renderer.project([0,0,50]),projection);
  globalThis.devicePixelRatio=3;
  renderer.render(camera,10,held);
  assert.equal(frames.length,2,'same capped backing need not repaint');
  assert.deepEqual(resizes,[2,2]);
  globalThis.devicePixelRatio=1;
  renderer.render(camera,11,held);
  assert.deepEqual([bw,bh],[901,651]);assert.deepEqual(resizes,[3,3]);
  assert.equal(frames.length,3);assert.deepEqual(frames[2],first);
  assert.deepEqual(renderer.project([0,0,50]),projection);
  renderer.render(camera,12,held);assert.equal(frames.length,3);
  // Browser zoom may temporarily hide the canvas; it must not poison the cache.
  canvas.clientWidth=0;renderer.render(camera,13,held);assert.equal(frames.length,3);
  canvas.clientWidth=901;globalThis.devicePixelRatio=1.25;renderer.render(camera,14,held);
  assert.deepEqual([bw,bh],[1126,813]);
  assert.deepEqual(transforms.at(-1),[1126/901,0,0,813/651,0,0]);
  assert.deepEqual(frames[3],first);assert.equal(frames.length,4);
  renderer.render(camera,.875,{...held,paused:false});
  assert.equal(frames.length,5,'ordinary water resumes after density transition');
 }finally{
  renderer?.dispose();
  if(before===undefined)delete globalThis.devicePixelRatio;else globalThis.devicePixelRatio=before;
 }
});

function compatibilityPickingFixture(native){
 const gradient={addColorStop(){}},ctx={createLinearGradient(){return gradient;},setTransform(){},fillRect(){},beginPath(){},moveTo(){},lineTo(){},closePath(){},fill(){},stroke(){}};
 let bound=null;const constants=new Map();
 const methods={createShader:()=>({}),createProgram:()=>({}),createBuffer:()=>({}),createTexture:()=>({}),createRenderbuffer:()=>({}),createFramebuffer:()=>({}),
  getShaderParameter:()=>true,getProgramParameter:()=>true,getAttribLocation:()=>0,getUniformLocation:()=>({}),isContextLost:()=>false,
  bindFramebuffer:(_target,value)=>{bound=value;},getParameter:()=>bound,checkFramebufferStatus:()=>gl.FRAMEBUFFER_COMPLETE};
 const gl=new Proxy(methods,{get(target,key){if(key in target)return target[key];if(/^[A-Z0-9_]+$/.test(key)){if(!constants.has(key))constants.set(key,constants.size+1);return constants.get(key);}return ()=>{};}});
 const canvas={clientWidth:900,clientHeight:650,width:0,height:0,left:137,top:91,
  getBoundingClientRect(){return {left:this.left,top:this.top,width:this.clientWidth,height:this.clientHeight};},
  getContext(type){return type==='2d'?ctx:native&&type==='webgl'?gl:null;},
  addEventListener(){},removeEventListener(){}};
 return canvas;
}

for(const native of [false,true])test((native?'Native WebGL':'Canvas')+' compatibility selects existing place using client coordinates after canvas relocation',()=>{
 const before=globalThis.devicePixelRatio;globalThis.devicePixelRatio=1;
 const canvas=compatibilityPickingFixture(native),binding={id:'LOC-MUD-DOGS-SWAMP',anchor:[0,0,50],visited:false};
 const camera={target:[0,2,50],distance:190,yaw:.2,pitch:.17};
 let renderer;
 try{
  renderer=createWorldRenderer(canvas,[binding],{});
  assert.equal(renderer.stats.renderer,native?'native-webgl':'canvas2d-spatial-fallback');
  renderer.render(camera,.5,{strength:1,storm:0,paused:false});
  let q=renderer.project(binding.renderAnchor);
  assert.ok(q&&q.depth>=-1&&q.depth<=1);
  assert.equal(renderer.pick(q.x+canvas.left,q.y+canvas.top),binding,'pointer uses client rather than canvas-local coordinates');
  assert.equal(renderer.pick(q.x,q.y),null,'untranslated local coordinate must not select a displaced place');
  // Moving the DOM element does not change source projection or the place.
  canvas.left=235;canvas.top=175;
  assert.equal(renderer.pick(q.x+canvas.left,q.y+canvas.top),binding);
  assert.equal(renderer.pick(NaN,q.y+canvas.top),null);
  assert.equal(renderer.pick(canvas.left-1,canvas.top+1),null);
  globalThis.devicePixelRatio=2;
  renderer.render(camera,10,{strength:1,storm:0,paused:true});
  q=renderer.project(binding.renderAnchor);
  assert.equal(renderer.pick(q.x+canvas.left,q.y+canvas.top),binding,'backing density does not scale client hits');
  // Synthetic near-plane probe uses the existing camera and only the test binding.
  const t=camera.target,d=camera.distance,dir=[Math.sin(camera.yaw)*Math.cos(camera.pitch),Math.sin(camera.pitch),Math.cos(camera.yaw)*Math.cos(camera.pitch)];
  binding.renderAnchor=t.map((v,i)=>v+dir[i]*(d-.15));
  const near=renderer.project(binding.renderAnchor);
  assert.ok(near&&near.depth< -1,'probe is in front of eye but clipped by near plane');
  assert.equal(renderer.pick(near.x+canvas.left,near.y+canvas.top),null);
  assert.equal(binding.visited,false);
 }finally{
  renderer?.dispose();
  if(before===undefined)delete globalThis.devicePixelRatio;else globalThis.devicePixelRatio=before;
 }
});
