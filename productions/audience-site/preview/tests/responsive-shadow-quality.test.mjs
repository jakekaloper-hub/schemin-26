import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
const source=readFileSync(new URL('../three-world.mjs',import.meta.url),'utf8');
const quality=source.slice(source.indexOf('export function rendererQuality('),source.indexOf('/** Shadows are cast')).replace('export function','function');
const setCamera=source.slice(source.indexOf(' function setCamera(c){'),source.indexOf(' async function prepare(c)'));
assert.ok(setCamera.startsWith(' function setCamera(c){'));
function fixture({width=390,height=844,dpr=2,maxTextureSize=4096,initialSize=1024}={}){
 const canvas={clientWidth:width,clientHeight:height},env={devicePixelRatio:dpr},allocations=[],resizes=[];
 const shadowMap={needsUpdate:false};
 const mapSize={x:initialSize,y:initialSize,set(x,y){this.x=x;this.y=y;allocations.push([x,y]);}};
 const sun={shadow:{mapSize}};
 let pixelRatio=1;
 const renderer={capabilities:{maxTextureSize},shadowMap,setPixelRatio(v){pixelRatio=v;},getPixelRatio(){return pixelRatio;},setSize(w,h){resizes.push([w,h]);}};
 const camera={position:{set(){}},lookAt(){},updateMatrixWorld(){},updateProjectionMatrix(){}};
 const sky={position:{copy(){}}},stats={};
 const run=new Function('canvas','globalThis','renderer','camera','sky','sun','templeMist','stats',
  'let lastWidth=0,lastHeight=0,lastPixelRatio=0;\n'+quality+'\n'+setCamera+'\nreturn setCamera;')(canvas,env,renderer,camera,sky,sun,null,stats);
 return {canvas,env,allocations,resizes,mapSize,shadowMap,stats,frame(){shadowMap.needsUpdate=false;run({target:[0,4,0],distance:60,yaw:.2,pitch:.8});return shadowMap.needsUpdate;}};
}
test('mobile to desktop restores the existing 2048 shadow tier at the exact breakpoint',()=>{
 const x=fixture();assert.equal(x.frame(),false);
 x.canvas.clientWidth=699;assert.equal(x.frame(),false);
 x.canvas.clientWidth=700;assert.equal(x.frame(),true);
 assert.deepEqual(x.allocations,[[2048,2048]]);
 assert.equal(x.stats.pixelRatio,1.5);
 assert.equal(x.frame(),false);
});
test('desktop to mobile reduces shadow texels by four and does not reallocate on same-tier resizes',()=>{
 const x=fixture({width:1440,height:900,initialSize:2048});assert.equal(x.frame(),false);
 x.canvas.clientWidth=390;assert.equal(x.frame(),true);
 assert.deepEqual(x.allocations,[[1024,1024]]);
 assert.equal(x.stats.pixelRatio,1.25);
 x.canvas.clientHeight=700;assert.equal(x.frame(),false);
 x.canvas.clientWidth=500;assert.equal(x.frame(),false);
 assert.equal(x.allocations.length,1);
});
test('DPR changes and repeated camera frames do not dirty static shadow coverage',()=>{
 const x=fixture();x.frame();x.env.devicePixelRatio=1;
 assert.equal(x.frame(),false);assert.equal(x.stats.pixelRatio,1);
 assert.equal(x.frame(),false);assert.deepEqual(x.allocations,[]);
});
test('hardware maximum caps the existing tier without repeated allocation',()=>{
 const x=fixture({width:1440,initialSize:2048,maxTextureSize:1024});
 assert.equal(x.frame(),true);assert.deepEqual(x.allocations,[[1024,1024]]);
 x.canvas.clientWidth=1600;assert.equal(x.frame(),false);
 x.canvas.clientWidth=500;assert.equal(x.frame(),false);
 assert.equal(x.allocations.length,1);
});
test('viewport changes remain in the actual render signature, including paused frames',()=>{
 const render=source.slice(source.indexOf(' function render(c,time,'),source.indexOf(' function project(p)'));
 assert.ok(render.includes('paused?lastTime:time,strength,storm,canvas.clientWidth,canvas.clientHeight'));
 assert.ok(render.includes('setCamera(c)'));
 assert.ok(render.includes('if(!paused)lastTime=time;regional.tick(lastTime,{paused})'));
});
