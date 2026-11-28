import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {illustrativeLight} from '../spatial.mjs';
const source=readFileSync(new URL('../app.mjs',import.meta.url),'utf8');
const startup=source.slice(source.indexOf('// Graphics loss is terminal'),source.indexOf('// A persisted pagehide'));
function fixture({lossAt,returning=false,hour=12,minute=0}={}){
 const clockInputs=[],lights=[];
 const callbacks=new Map(),actions=[],nodes={'#fallback':{hidden:true},'#skipReveal':{hidden:true}};
 let serial=0,lose,draws=0,rendered=0,finished=0,resolve,reject;
 const preparation=new Promise((yes,no)=>{resolve=yes;reject=no;});
 const raf=fn=>{callbacks.set(++serial,fn);return serial;};
 const fallback=reason=>{nodes['#fallback'].hidden=false;nodes['#skipReveal'].hidden=true;actions.push(reason);};
 const create=(_canvas,_bindings,options)=>{
  lose=options.onContextLost;
  if(lossAt==='constructor')lose();
  return {prepare:()=>preparation,render(_camera,time,options){rendered++;lights.push({time,strength:options.strength});if(lossAt==='render')lose();}};
 };
 new Function('$','requestAnimationFrame','createWorldRenderer','showFallback','dispatch','finishReveal','draw','splash','setTimeout','observerClock','illustrativeLight','performance',
  `let frameId,renderer,canvas,bindings=[],camera={},revealStart,state={phase:'${returning?'EXPLORING':'REVEALING'}'};\n${startup}`)(
  key=>nodes[key],raf,create,fallback,a=>actions.push(a.id),()=>finished++,()=>draws++,{classList:{add(){}}},()=>{},iso=>{clockInputs.push(iso);return {hour,minute};},illustrativeLight,{now:()=>1000});
 async function step(){const entry=callbacks.entries().next().value;assert.ok(entry);callbacks.delete(entry[0]);return entry[1]();}
 return {nodes,actions,callbacks,step,clockInputs,lights,lose:()=>lose(),resolve,reject,stats:()=>({rendered,finished,draws})};
}
const assertStopped=x=>{assert.equal(x.nodes['#fallback'].hidden,false);assert.equal(x.nodes['#skipReveal'].hidden,true);assert.equal(x.callbacks.size,0);assert.ok(!x.actions.includes('first-frame'));assert.equal(x.stats().finished,0);};
for(const returning of [false,true])test(`successful first frame starts exactly one loop (returning=${returning})`,async()=>{
 const x=fixture({returning});await x.step();const preparing=x.step();x.resolve();await preparing;await x.step();
 assert.deepEqual(x.actions,['geometry','renderer','first-frame']);assert.equal(x.callbacks.size,1);assert.equal(x.stats().rendered,1);assert.equal(x.stats().finished,returning?1:0);await x.step();assert.equal(x.stats().draws,1);
});
test('synchronous context loss during renderer creation stops startup',async()=>{const x=fixture({lossAt:'constructor'});await x.step();await x.step();assertStopped(x);assert.equal(x.stats().rendered,0);});
test('context loss during asynchronous preparation cannot resume reveal',async()=>{const x=fixture();await x.step();const preparing=x.step();x.lose();x.resolve();await preparing;assertStopped(x);assert.equal(x.stats().rendered,0);assert.ok(!x.actions.includes('renderer'));});
test('preparation rejection after context loss preserves original fallback reason',async()=>{const x=fixture();await x.step();const preparing=x.step();x.lose();x.reject(Error('late rejection'));await preparing;assertStopped(x);assert.equal(x.actions.filter(a=>a.includes('graphics context was lost')).length,1);assert.ok(!x.actions.some(a=>a.includes('late rejection')));});
test('context loss in first render cannot schedule reveal',async()=>{const x=fixture({lossAt:'render'});await x.step();const preparing=x.step();x.resolve();await preparing;assertStopped(x);assert.equal(x.stats().rendered,1);});
test('already queued first-frame callback cannot revive graphics after loss',async()=>{const x=fixture();await x.step();const preparing=x.step();x.resolve();await preparing;x.lose();await x.step();assertStopped(x);});

for(const [hour,minute,returning] of [[0,0,false],[6,30,false],[12,0,true],[23,45,true]])test(`readiness uses Eastern-clock light before revealing (hour=${hour}, minute=${minute}, returning=${returning})`,async()=>{
 const x=fixture({hour,minute,returning});await x.step();const preparing=x.step();x.resolve();await preparing;
 assert.deepEqual(x.lights,[{time:0,strength:illustrativeLight(hour+minute/60).strength}]);
 assert.equal(x.clockInputs.length,1);assert.ok(Number.isFinite(Date.parse(x.clockInputs[0])));
 assert.ok(!x.actions.includes('first-frame'));await x.step();assert.ok(x.actions.includes('first-frame'));
});
