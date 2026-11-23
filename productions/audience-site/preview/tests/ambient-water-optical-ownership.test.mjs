import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';

const source=readFileSync(new URL('../app.mjs',import.meta.url),'utf8');
const begin=source.indexOf('function sizeAmbientCanvas(');
const end=source.indexOf('\nfunction draw(t){',begin);
assert.ok(begin>=0&&end>begin,'Use the actual observer ambient implementation');

function instrument(rendererName,demo=null){
 const calls={height:0,projection:0,ellipses:0,strokes:0,clips:0,clears:0};
 const ambient={width:0,height:0};
 const ambientCtx={
  setTransform(){},clearRect(){calls.clears++;},beginPath(){},
  ellipse(){calls.ellipses++;},stroke(){calls.strokes++;},
  save(){},restore(){},moveTo(){},lineTo(){},closePath(){},
  clip(){calls.clips++;}
 };
 const renderer={
  stats:{renderer:rendererName},
  height(){calls.height++;return -1;},
  project(){calls.projection++;return {x:100,y:100,depth:.5};}
 };
 const context={ambient,ambientCtx,renderer,canvas:{clientWidth:640,clientHeight:360},camera:{target:[0,0,0],distance:30,yaw:0,pitch:.65},innerWidth:640,innerHeight:360,
  window:{devicePixelRatio:1},demo,
  weather:{affectedZoneIds:['REG-EASTERN-STORM-COAST']}};
 const {drawAmbient,needsAmbientFallbackGlints}=vm.runInNewContext(
  source.slice(begin,end)+'\n({drawAmbient,needsAmbientFallbackGlints})',context
 );
 return {calls,drawAmbient,needsAmbientFallbackGlints};
}

test('Three.js water is shaded only in depth-tested WebGL, without screen-space glints',()=>{
 const x=instrument('three-webgl2',0);
 assert.equal(x.needsAmbientFallbackGlints('three-webgl2'),false);
 x.drawAmbient(12);
 assert.equal(x.calls.ellipses,0);
 assert.equal(x.calls.height,0);
 assert.equal(x.calls.projection,0);
 assert.equal(x.calls.clears,1);
});

test('native WebGL also keeps ownership of its existing physical water shading',()=>{
 const x=instrument('native-webgl',null);
 x.drawAmbient(13);
 assert.equal(x.calls.ellipses,0);
 assert.equal(x.calls.height,0);
});

test('Canvas2D fallback retains the 120 water glints, including during synthetic calm',()=>{
 const x=instrument('canvas2d-spatial-fallback',0);
 assert.equal(x.needsAmbientFallbackGlints('canvas2d-spatial-fallback'),true);
 x.drawAmbient(12);
 assert.equal(x.calls.ellipses,120);
 assert.equal(x.calls.height,120);
 assert.equal(x.calls.strokes,120);
 assert.equal(x.calls.clips,0);
});

test('bounded regional storm optics reproject 110 existing-world drop columns without duplicating WebGL water glints',()=>{
 const x=instrument('three-webgl2',1);
 x.drawAmbient(12);
 assert.equal(x.calls.ellipses,0);
 assert.equal(x.calls.clips,0,'world-projected rain no longer clips an unoccluded screen polygon');
 assert.ok(x.calls.height>110,'each drop samples both the original ground point and bounded terrain sightlines');
 assert.equal(x.calls.projection,220,'both 3D endpoints of 110 rain strokes project through the world camera');
 assert.equal(x.calls.strokes,110);
});

test('weather demonstration, ordinary water time, and physical shader remain unchanged',()=>{
 const physical=readFileSync(new URL('../three-world.mjs',import.meta.url),'utf8');
 const fallback=readFileSync(new URL('../renderer.mjs',import.meta.url),'utf8');
 assert.match(source,/if\(demo>0\)for\(const id of weather\.affectedZoneIds\)/);
 assert.match(source,/if\(!paused&&!document\.hidden\)animationTime\+=dt/);
 assert.match(source,/renderer\.render\(camera,animationTime,\{strength:light\.strength,storm:demo\|\|0,paused\}\)/);
 assert.match(physical,/oceanMaterial\.uniforms\.uTime\.value=lastTime/);
 assert.match(fallback,/renderer:'canvas2d-spatial-fallback'/);
});
