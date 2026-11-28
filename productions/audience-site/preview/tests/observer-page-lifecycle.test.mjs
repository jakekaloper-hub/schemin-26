import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
const source=readFileSync(new URL('../app.mjs',import.meta.url),'utf8');
const start=source.indexOf("window.addEventListener('pagehide',");
assert.ok(start>=0);
const cancellation=source.slice(source.indexOf('function cancelWorldGesture(){'),source.indexOf("canvas.addEventListener('contextmenu'"));
assert.ok(cancellation.startsWith('function cancelWorldGesture(){'));
function setup(hasRenderer=true){
 const handlers=new Map(),cancelled=[],released=[],held=new Set([1,2]),tooltip={hidden:false};
 const canvas={style:{cursor:'pointer'},hasPointerCapture:id=>held.has(id),releasePointerCapture:id=>{released.push(id);held.delete(id);}};
 let disposals=0;
 const addEventListener=(type,fn)=>{assert.ok(!handlers.has(type));handlers.set(type,fn);};
 const doc={hidden:false,addEventListener};
 const build=new Function('window','document','cancelAnimationFrame','renderer','performance','canvas','$',
  'let frameId=42,lastTime=100; let pointers=new Map([[1,[0,0]],[2,[10,10]]]),pointerStart=null,dragDistance=99,pinchDistance=10,pinchCenter=[5,5],multiTouchGesture=true;\n'+cancellation+'\n'+source.slice(start)+'\nreturn {read:()=>({lastTime,frameId}),gesture:()=>({count:pointers.size,dragDistance,pinchDistance,pinchCenter,multiTouchGesture})};');
 const api=build({addEventListener},doc,id=>cancelled.push(id),hasRenderer?{dispose(){disposals++;}}:undefined,{now:()=>9000},canvas,()=>tooltip);
 return {fire(type,persisted){handlers.get(type)({persisted});},visibility(hidden){doc.hidden=hidden;handlers.get('visibilitychange')();},has(type){return handlers.has(type);},...api,cancelled,released,held,tooltip,canvas,disposals:()=>disposals};
}
function retired(x){
 assert.deepEqual(x.released,[1,2]);assert.equal(x.held.size,0);
 assert.deepEqual(x.gesture(),{count:0,dragDistance:0,pinchDistance:null,pinchCenter:null,multiTouchGesture:false});
 assert.equal(x.tooltip.hidden,true);assert.equal(x.canvas.style.cursor,'grab');
}
test('cached back/forward transition preserves the existing frame and renderer, retiring captured input',()=>{
 const x=setup();x.fire('pagehide',true);retired(x);
 assert.deepEqual(x.cancelled,[]);assert.equal(x.disposals(),0);
 x.fire('pageshow',true);
 assert.deepEqual(x.read(),{lastTime:9000,frameId:42});
 assert.deepEqual(x.cancelled,[]);assert.equal(x.disposals(),0);
});
test('ordinary navigation still cancels the frame and disposes resources',()=>{
 const x=setup();x.fire('pageshow',false);
 assert.equal(x.read().lastTime,100);
 x.fire('pagehide',false);retired(x);
 assert.deepEqual(x.cancelled,[42]);assert.equal(x.disposals(),1);
});
test('page departure before renderer initialization is safe',()=>{
 const x=setup(false);x.fire('pagehide',false);retired(x);
 assert.deepEqual(x.cancelled,[42]);assert.equal(x.disposals(),0);
});
test('window blur retires the world gesture without touching the render loop or clock',()=>{
 const x=setup();assert.ok(x.has('blur'));x.fire('blur');retired(x);
 x.fire('blur');retired(x);
 assert.deepEqual(x.cancelled,[]);assert.equal(x.disposals(),0);
 assert.deepEqual(x.read(),{lastTime:100,frameId:42});
});
test('only hidden visibility retires gestures; later visible transition is inert',()=>{
 const x=setup();assert.ok(x.has('visibilitychange'));x.visibility(false);
 assert.equal(x.gesture().count,2);assert.deepEqual(x.released,[]);
 x.visibility(true);retired(x);x.visibility(false);retired(x);
 assert.deepEqual(x.cancelled,[]);assert.equal(x.disposals(),0);
 assert.deepEqual(x.read(),{lastTime:100,frameId:42});
});
