import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
const source=readFileSync(new URL('../app.mjs',import.meta.url),'utf8');
const fallback=source.slice(source.indexOf('function showFallback('),source.indexOf('function escapePanels('));
const draw=source.slice(source.indexOf('function draw(t){'),source.indexOf('function clamp01('));
assert.ok(fallback.startsWith('function showFallback('));
assert.ok(draw.startsWith('function draw(t){'));
// Execute the actual host draw and fallback handlers with a controlled frame queue.
function fixture({failure=null,paused=false,history=false,memory=false,hidden=false}={}){
 const nodes={'#fallback':{hidden:true},'#fallbackReason':{},'#splash':{hidden:true},'#skipReveal':{hidden:true},'#hint':{style:{}}};
 const queue=new Map(),cancelled=[],restored=[],rendered=[],ambient=[];
 let serial=0,retired=0,lose;
 const renderer={render(_camera,time,options){
  rendered.push({time,options});
  if(failure==='context'){lose('Original context-loss reason');throw Error('secondary render failure');}
  if(failure==='renderer')throw Error('render failure');
 }};
 const api=new Function('$','renderer','requestAnimationFrame','cancelAnimationFrame','cancelWorldGesture','restoreFallbackPlace','observerClock','illustrativeLight','drawAmbient','document','paused','historySession','memorySession',
  'let state={phase:"EXPLORING"},camera={target:[0,0,0],distance:30,pitch:.6,yaw:0},target=structuredClone(camera),selected={id:"LOC-MUD-DOGS-SWAMP"},ready=true,animationTime=10,lastTime=1000,frameId=0,revealStart=0,demo=0;\n'+fallback+'\n'+draw+'\nreturn {draw,showFallback,read:()=>({ready,animationTime,lastTime})};')(
  id=>nodes[id],renderer,fn=>{queue.set(++serial,fn);return serial;},id=>{cancelled.push(id);queue.delete(id);},()=>retired++,id=>restored.push(id),()=>({hour:12,minute:0}),()=>({strength:1}),time=>{ambient.push(time);if(failure==='ambient')throw Error('overlay failure');},{hidden},paused,history?{}:null,memory?{}:null);
 lose=api.showFallback;
 return {...api,nodes,queue,cancelled,restored,rendered,ambient,retired:()=>retired,step(t){const [id,fn]=queue.entries().next().value;queue.delete(id);fn(t);}};
}
for(const failure of ['renderer','ambient'])test('post-readiness '+failure+' failure retires the frame and retains selected-place source access',()=>{
 const x=fixture({failure});x.draw(1020);
 assert.equal(x.nodes['#fallback'].hidden,false);
 assert.match(x.nodes['#fallbackReason'].textContent,/graphics frame did not complete/);
 assert.equal(x.read().ready,false);
 assert.deepEqual(x.cancelled,[1]);assert.equal(x.queue.size,0);
 assert.deepEqual(x.restored,['LOC-MUD-DOGS-SWAMP']);assert.equal(x.retired(),1);
 assert.equal(x.rendered.length,1);assert.equal(x.ambient.length,failure==='ambient'?1:0);
 x.draw(1040);assert.equal(x.rendered.length,1);assert.equal(x.queue.size,0);
});
test('a context loss followed by an exception preserves the first fallback reason',()=>{
 const x=fixture({failure:'context'});x.draw(1020);
 assert.equal(x.nodes['#fallbackReason'].textContent,'Original context-loss reason');
 assert.equal(x.queue.size,0);assert.equal(x.retired(),1);
 assert.deepEqual(x.restored,['LOC-MUD-DOGS-SWAMP']);assert.equal(x.ambient.length,0);
});
test('healthy global-calm frames retain ordinary water motion and exactly one successor',()=>{
 const x=fixture();x.draw(1020);x.step(1040);
 assert.equal(x.queue.size,1);assert.equal(x.nodes['#fallback'].hidden,true);
 assert.deepEqual(x.rendered.map(r=>r.options.storm),[0,0]);
 assert.ok(x.rendered[0].time>10);assert.ok(x.rendered[1].time>x.rendered[0].time);
 assert.deepEqual(x.ambient,x.rendered.map(r=>r.time));assert.deepEqual(x.cancelled,[]);
});
test('explicit pause and hidden document retain water phase on healthy frames',()=>{
 for(const options of [{paused:true},{hidden:true}]){
  const x=fixture(options);x.draw(1020);x.step(1040);
  assert.deepEqual(x.rendered.map(r=>r.time),[10,10]);
  assert.equal(x.queue.size,1);assert.equal(x.nodes['#fallback'].hidden,true);
 }
});
test('open source history and private memory continue to hold the observation without rendering',()=>{
 for(const options of [{history:true},{memory:true}]){
  const x=fixture(options);x.draw(1020);x.step(1040);
  assert.equal(x.read().animationTime,10);assert.equal(x.read().lastTime,1040);
  assert.equal(x.rendered.length,0);assert.equal(x.ambient.length,0);assert.equal(x.queue.size,1);
  assert.equal(x.nodes['#fallback'].hidden,true);
 }
});
