import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';

const source=readFileSync(new URL('../app.mjs',import.meta.url),'utf8');
const start=source.indexOf('function sizeAmbientCanvas(');
const end=source.indexOf('\nconst zoneBounds=',start);
assert.ok(start>=0&&end>start,'Expected actual source helper in observer app');
const sizeAmbientCanvas=vm.runInNewContext(source.slice(start,end)+'\nsizeAmbientCanvas');

function surface(){
 const mutations={width:0,height:0},transforms=[];
 let width=0,height=0;
 return {mutations,transforms,
  canvas:{
   get width(){return width;},set width(v){width=v;mutations.width++;},
   get height(){return height;},set height(v){height=v;mutations.height++;}
  },
  ctx:{setTransform(...args){transforms.push(args);}}
 };
}
test('retina backing dimensions preserve CSS-space coordinates and a sharp 2x scale',()=>{
 const x=surface();
 assert.deepEqual(Array.from(sizeAmbientCanvas(x.canvas,x.ctx,1440,900,2)),[1440,900]);
 assert.equal(x.canvas.width,2880);assert.equal(x.canvas.height,1800);
 assert.deepEqual(x.transforms.at(-1),[2,0,0,2,0,0]);
});
test('high-density mobile backing is capped at 2x and zoom retains fractional scaling',()=>{
 const x=surface();
 sizeAmbientCanvas(x.canvas,x.ctx,390,844,3.5);
 assert.deepEqual([x.canvas.width,x.canvas.height],[780,1688]);
 assert.deepEqual(x.transforms.at(-1),[2,0,0,2,0,0]);
 sizeAmbientCanvas(x.canvas,x.ctx,390,844,1.5);
 assert.deepEqual([x.canvas.width,x.canvas.height],[585,1266]);
 assert.deepEqual(x.transforms.at(-1),[1.5,0,0,1.5,0,0]);
});
test('resize reallocates only when necessary and restores the correct transform on every frame',()=>{
 const x=surface();
 sizeAmbientCanvas(x.canvas,x.ctx,640,360,2);
 sizeAmbientCanvas(x.canvas,x.ctx,640,360,2);
 assert.deepEqual(x.mutations,{width:1,height:1});
 assert.equal(x.transforms.length,2);
 sizeAmbientCanvas(x.canvas,x.ctx,500,360,2);
 assert.deepEqual(x.mutations,{width:2,height:1});
 assert.deepEqual(x.transforms.at(-1),[2,0,0,2,0,0]);
});
test('invalid viewport and DPR stay finite without exceeding the backing budget',()=>{
 const x=surface();
 assert.deepEqual(Array.from(sizeAmbientCanvas(x.canvas,x.ctx,NaN,0,Infinity)),[1,1]);
 assert.deepEqual([x.canvas.width,x.canvas.height],[1,1]);
 assert.deepEqual(x.transforms.at(-1),[1,0,0,1,0,0]);
 sizeAmbientCanvas(x.canvas,x.ctx,100,100,-10);
 assert.deepEqual([x.canvas.width,x.canvas.height],[100,100]);
});
test('the existing atmospheric weather gate and ordinary-water render path stay independent',()=>{
 assert.match(source,/sizeAmbientCanvas\(ambient,ambientCtx,innerWidth,innerHeight,window\.devicePixelRatio\)/);
 assert.match(source,/if\(demo>0\)for\(const id of weather\.affectedZoneIds\)/);
 assert.match(source,/renderer\.render\(camera,animationTime,\{strength:light\.strength,storm:demo\|\|0,paused\}\)/);
 assert.match(source,/if\(!paused&&!document\.hidden\)animationTime\+=dt/);
 assert.doesNotMatch(source,/ambient\.width!==w\|\|ambient\.height!==h/);
});
