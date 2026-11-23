import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
const source=readFileSync(new URL('../app.mjs',import.meta.url),'utf8');
const start=source.indexOf("window.addEventListener('pagehide',");
assert.ok(start>=0);
function setup(hasRenderer=true){
 const handlers=new Map(),cancelled=[];
 let disposals=0;
 const build=new Function('window','cancelAnimationFrame','renderer','performance',
  'let frameId=42,lastTime=100;\n'+source.slice(start)+'\nreturn ()=>({lastTime,frameId});');
 const read=build({addEventListener(type,fn){assert.ok(!handlers.has(type));handlers.set(type,fn);}},
  id=>cancelled.push(id),hasRenderer?{dispose(){disposals++;}}:undefined,{now:()=>9000});
 return {fire(type,persisted){handlers.get(type)({persisted});},read,cancelled,disposals:()=>disposals};
}
test('cached back/forward transition preserves the existing frame and renderer',()=>{
 const x=setup();x.fire('pagehide',true);
 assert.deepEqual(x.cancelled,[]);assert.equal(x.disposals(),0);
 x.fire('pageshow',true);
 assert.deepEqual(x.read(),{lastTime:9000,frameId:42});
 assert.deepEqual(x.cancelled,[]);assert.equal(x.disposals(),0);
});
test('ordinary navigation still cancels the frame and disposes resources',()=>{
 const x=setup();x.fire('pageshow',false);
 assert.equal(x.read().lastTime,100);
 x.fire('pagehide',false);
 assert.deepEqual(x.cancelled,[42]);assert.equal(x.disposals(),1);
});
test('page departure before renderer initialization is safe',()=>{
 const x=setup(false);x.fire('pagehide',false);
 assert.deepEqual(x.cancelled,[42]);assert.equal(x.disposals(),0);
});
