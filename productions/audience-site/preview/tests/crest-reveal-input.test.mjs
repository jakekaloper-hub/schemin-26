import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
const source=readFileSync(new URL('../app.mjs',import.meta.url),'utf8');
const layout=readFileSync(new URL('../index.template.html',import.meta.url),'utf8');

test('crest and reveal isolate all world interaction but keep Skip Reveal independently reachable',()=>{
 const start=layout.indexOf('<div id="worldInteraction" inert>'),end=layout.indexOf('</div><!-- worldInteraction -->');
 assert.ok(start>=0&&end>start);
 const world=layout.slice(start,end),rest=layout.slice(end);
 for(const id of ['world','motionToggle','infoToggle','placesToggle','placesPanel','inspector','infoPanel','demoLoss','demoWin','demoStreak','returnWorld'])assert.ok(world.includes('id="'+id+'"'),id);
 assert.ok(world.includes('class="skip"'));
 for(const id of ['splash','skipReveal','fallback','historyDialog','memoryDialog']){
  assert.ok(!world.includes('id="'+id+'"'),id);assert.ok(rest.includes('id="'+id+'"'),id);
 }
});
function fixture({focusSkip=false,reduced=false}={}){
 const start=source.indexOf('function finishReveal(){'),end=source.indexOf('function canControl(){',start);
 assert.ok(start>=0&&end>start);
 const skip={hidden:false},surface={inert:true},other={},focuses=[],timers=[],storage=[];
 const splash={hidden:false,classList:{add(){}}};
 const canvas={focus(options){focuses.push({unlocked:!surface.inert,skipHidden:skip.hidden,options});}};
 const doc={activeElement:focusSkip?skip:other};
 const nodes={'#skipReveal':skip,'#worldInteraction':surface};
 const run=new Function('$','document','canvas','splash','setTimeout','sessionStorage','reduced','structuredClone',
  'let target={target:[1,2,3]},camera={},ready=false;'+source.slice(start,end)+';finishReveal();return {ready,camera,target};');
 const result=run(id=>nodes[id],doc,canvas,splash,(fn,ms)=>timers.push({fn,ms}),{setItem:(...args)=>storage.push(args)},reduced,structuredClone);
 return {result,skip,surface,focuses,timers,storage,splash};
}
test('focused Skip Reveal transfers focus after world interaction unlocks and the skip control hides',()=>{
 const x=fixture({focusSkip:true});
 assert.equal(x.surface.inert,false);assert.equal(x.skip.hidden,true);
 assert.deepEqual(x.focuses,[{unlocked:true,skipHidden:true,options:{preventScroll:true}}]);
 assert.equal(x.result.ready,true);assert.deepEqual(x.result.camera,x.result.target);
 assert.deepEqual(x.storage,[['commonwealth-observer-seen','1']]);
});
test('automatic and reduced-motion reveal unlock world controls without stealing focus',()=>{
 for(const reduced of [false,true]){
  const x=fixture({reduced});
  assert.equal(x.surface.inert,false);assert.equal(x.skip.hidden,true);
  assert.deepEqual(x.focuses,[]);assert.equal(x.result.ready,true);
  assert.equal(x.timers.length,1);assert.equal(x.timers[0].ms,reduced?0:1200);
  x.timers[0].fn();assert.equal(x.splash.hidden,true);
 }
});
