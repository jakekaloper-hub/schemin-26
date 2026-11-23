import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {canvasWaterDisplacement,createWorldRenderer,nextWaterPhase} from '../renderer.mjs';

test('existing fallback water grid inherits bounded, deterministic ordinary-time physical waves',()=>{
 const pts=[[-320,-320],[-8,42],[0,0],[67,-52],[304,304]];
 for(const [x,z] of pts){
  const a=canvasWaterDisplacement(x,z,.125),b=canvasWaterDisplacement(x,z,.625);
  assert.ok(Math.abs(a)<=.18000001&&Math.abs(b)<=.18000001,'same GPU wave amplitude envelope');
  assert.notEqual(a,b,'ordinary wave surface must advance without weather input');
  assert.equal(a,canvasWaterDisplacement(x,z,.125),'stable at identical source point and time');
 }
 for(const bad of [NaN,Infinity,-Infinity,undefined,'3']){
  assert.throws(()=>canvasWaterDisplacement(bad,1,0),/INVALID_CANVAS_WATER_POSITION/);
  assert.throws(()=>canvasWaterDisplacement(0,bad,0),/INVALID_CANVAS_WATER_POSITION/);
  assert.throws(()=>canvasWaterDisplacement(0,1,bad),/INVALID_CANVAS_WATER_POSITION/);
 }
 const phase=nextWaterPhase(0,.625,false);
 assert.equal(canvasWaterDisplacement(8,4,nextWaterPhase(phase,50,true)),canvasWaterDisplacement(8,4,phase));
});

test('actual Canvas compatibility draws moving water geometry under calm and holds exact surface on pause',()=>{
 const oldDpr=globalThis.devicePixelRatio;
 globalThis.devicePixelRatio=1;
 const frames=[];
 let current={draws:0,shapeX:0,shapeY:0,polygons:0},last=[0,0];
 const gradient={addColorStop(){}};
 const ctx={
  createLinearGradient(){return gradient;},setTransform(){},
  fillRect(){frames.push(current);current={draws:0,shapeX:0,shapeY:0,polygons:0};},
  beginPath(){},moveTo(x,y){last=[x,y];},lineTo(){},closePath(){},
  fill(){current.polygons++;current.shapeX+=Math.round(last[0]*1e4);current.shapeY+=Math.round(last[1]*1e4);},
  stroke(){}
 };
 const canvas={clientWidth:900,clientHeight:650,width:0,height:0,getContext(type){return type==='2d'?ctx:null;}};
 let renderer;
 try{
  renderer=createWorldRenderer(canvas,[],{});
  assert.equal(renderer.stats.renderer,'canvas2d-spatial-fallback');
  assert.ok(renderer.stats.waterTriangles>=3000,'existing 40-by-40 water grid is reused');
  const camera={target:[0,2,50],distance:190,yaw:.2,pitch:.17};
  renderer.render(camera,.125,{strength:1,storm:0,paused:false});
  const calmA={...current};
  assert.ok(calmA.polygons>200,'actual polygons, not just glints');
  renderer.render(camera,.5,{strength:1,storm:0,paused:false});
  const calmB={...current};
  assert.ok(Math.abs(calmA.polygons-calmB.polygons)<=40,'the same fixed water mesh may clip at viewport edges as waves move');
  assert.notDeepEqual([calmA.shapeX,calmA.shapeY],[calmB.shapeX,calmB.shapeY],'water geometry advances during synthetic calm');
  renderer.render(camera,5,{strength:1,storm:0,paused:true});
  renderer.render(camera,9,{strength:1,storm:0,paused:true});
  assert.deepEqual(current,calmB,'explicit pause creates no additional draw or wave change');
  renderer.render(camera,.875,{strength:1,storm:0,paused:false});
  assert.notDeepEqual(current,calmB,'resuming advances moving water');
 }finally{
  renderer?.dispose();
  if(oldDpr===undefined)delete globalThis.devicePixelRatio;else globalThis.devicePixelRatio=oldDpr;
 }
});

test('fallback waves cannot rewrite places, weather authority or higher-quality WebGL renderers',()=>{
 const source=readFileSync(new URL('../renderer.mjs',import.meta.url),'utf8');
 assert.match(source,/waterTriangles\.push\(\{pts,center,water:true\}\)/);
 assert.match(source,/p\[1\]\+canvasWaterDisplacement\(p\[0\],p\[2\],waterFrame\)/);
 assert.match(source,/lastWater=nextWaterPhase\(lastWater,time,paused\)/);
 assert.match(source,/gl\.uniform1f\(loc\.uTime,waterTime\)/);
 assert.match(source,/let vp,eye,disposed=false,waterTime=0/);
 assert.doesNotMatch(source,/fetch\(|writeWorldState|publishObserver|createPrincipalCharacter/);
});
