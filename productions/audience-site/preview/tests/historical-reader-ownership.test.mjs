import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {closePlaceHistory} from '../place-history.mjs';
import {closeMemory,memoryView} from '../memory.mjs';
const read=name=>readFileSync(new URL('../'+name,import.meta.url),'utf8');
const app=read('app.mjs');
const gate=app.match(/function canControl\(\)\{[^\n]+\}/)?.[0];
const cancel=app.match(/function cancelWorldGesture\(\)\{[\s\S]*?\n\}/)?.[0];
assert.ok(cancel,'reuse the actual world gesture cancellation helper');
assert.ok(gate,'reuse the actual shared world input gate');
function entry(name,kind,action='enter'){
 const s=read(name),start=s.indexOf('function '+action+kind+'('),end=s.indexOf('\n}',start);
 assert.ok(start>=0&&end>start);
 return s.slice(start,end+2);
}
const entries={History:entry('place-history-ui.mjs','History'),Memory:entry('memory-ui.mjs','Memory')};
const exits={History:entry('place-history-ui.mjs','History','exit'),Memory:entry('memory-ui.mjs','Memory','exit')};
// Source-executing DOM stub: no real browser, GPU, private folios, or canonical data.
function run(kind,scenario={}){
 const calls=[],node={isConnected:true,focus(){calls.push('focus')},append(){},replaceChildren(){},setAttribute(){},removeAttribute(){}};
 const captured=new Set([1]),tooltip={hidden:false},canvas={style:{cursor:'grabbing'},hasPointerCapture:id=>captured.has(id),releasePointerCapture(id){captured.delete(id);calls.push('release:'+id)}};
 const env={
  canvas,
  state:{phase:scenario.phase??'EXPLORING',inputOwner:scenario.owner??'WORLD'},
  $:id=>id==='#fallback'?{hidden:!scenario.fallback}:id==='#tooltip'?tooltip:node,
  selected:scenario.noSelected?null:{id:'LOC-TEST',name:'Synthetic place'},
  selectedMemory:()=>{calls.push('lookup');return scenario.noMemory?null:{pages:[]}},
  document:{activeElement:node,body:{classList:{add(){calls.push('body')},remove(){calls.push('body-closed')}}}},
  catalog:{history:{status:'RELEASE_CANDIDATE'},stateAsOf:'end_of_week_3_2026'},
  memoryIndex:{},openMemory:(_index,id,camera)=>{calls.push('open');return {locationId:id,returnCamera:structuredClone(camera),inputOwner:'MEMORY'}},
  openPlaceHistory:(_catalog,id,camera)=>{calls.push('open');return {locationId:id,returnCamera:structuredClone(camera),inputOwner:'HISTORY',entries:[]}},
  closeMemory,closePlaceHistory,memoryView,innerWidth:scenario.narrow?600:1000,historyEntries:node,memoryImage:node,
  restoreFallbackPlace:id=>{calls.push('fallback:'+id);return !!scenario.exitFallback},
  historyDialog:{showModal(){calls.push('modal')},close(){calls.push('closed')}},memoryDialog:{showModal(){calls.push('modal')},close(){calls.push('closed')}},
  memoryButtons:[],showMemoryPage:()=>calls.push('load'),structuredClone
 };
 const factory=new Function(...Object.keys(env),
  'let historySession='+(scenario.history?'{}':'null')+',memorySession='+(scenario.memory?'{}':'null')+
  ',historyPreviousFocus,memoryPreviousFocus,camera={target:[1,2,3]},target={target:'+(scenario.settled?'[1,2,3]':'[8,9,10]')+'},pointers=new Map([[1,{}]]),pointerStart={},dragDistance=8,pinchDistance=5,pinchCenter={},multiTouchGesture=true,memoryGeneration=0,memoryZoom,lastTime=0;\n'+
  gate+'\n'+cancel+'\n'+entries[kind]+'\n'+exits[kind]+'\nenter'+kind+'();const frozen=structuredClone({camera,target});'+
  (scenario.roundTrip?'exit'+kind+'();':'')+'return {camera,target,frozen,pointerCount:pointers.size,pointerStart,dragDistance,pinchDistance,pinchCenter,multiTouchGesture};');
 return {calls,...factory(...Object.values(env)),captured:[...captured],tooltipHidden:tooltip.hidden,cursor:canvas.style.cursor};
}
const denied=[
 {name:'active history',history:true},{name:'active private memory',memory:true},
 {name:'non-world input owner',owner:'HISTORY'},{name:'readiness reveal',phase:'REVEALING'},
 {name:'graphics fallback',fallback:true},{name:'no selected place',noSelected:true}
];
for(const kind of Object.keys(entries)){
 test(kind+' refuses competing input owners without camera, focus, or lookup side effects',()=>{
  for(const scenario of denied){
   const x=run(kind,scenario);
   assert.deepEqual(x.calls,[],scenario.name);
   assert.deepEqual(x.target,{target:[8,9,10]},scenario.name);
   assert.deepEqual(x.camera,{target:[1,2,3]},scenario.name);
   assert.equal(x.pointerCount,1,scenario.name);
   assert.deepEqual(x.captured,[1],scenario.name);
   assert.equal(x.tooltipHidden,false,scenario.name);
   assert.equal(x.cursor,'grabbing',scenario.name);
  }
 });
 test(kind+' still opens from an active selected world view and freezes the approach',()=>{
  const x=run(kind);
  assert.equal(x.calls.filter(c=>c==='open').length,1);
  assert.equal(x.calls.filter(c=>c==='modal').length,1);
  assert.deepEqual(x.target,x.camera);
  assert.equal(x.pointerCount,0);
  assert.deepEqual(x.captured,[]);
  assert.equal(x.calls.filter(c=>c==='release:1').length,1);
  assert.equal(x.pointerStart,null);
  assert.equal(x.dragDistance,0);
  assert.equal(x.pinchDistance,null);
  assert.equal(x.pinchCenter,null);
  assert.equal(x.multiTouchGesture,false);
  assert.equal(x.tooltipHidden,true);
  assert.equal(x.cursor,'grab');
 });
}
test('missing private edition remains unavailable without opening or changing camera',()=>{
 const x=run('Memory',{noMemory:true});
 assert.deepEqual(x.calls,['lookup']);
 assert.deepEqual(x.target,{target:[8,9,10]});
 assert.equal(x.pointerCount,1);
 assert.deepEqual(x.captured,[1]);
 assert.equal(x.tooltipHidden,false);
 assert.equal(x.cursor,'grabbing');
});

for(const kind of Object.keys(entries)){
 test(kind+' returns to the frozen pose and resumes the original approach, not the intermediate position',()=>{
  for(const scenario of [{roundTrip:true},{roundTrip:true,narrow:true},{roundTrip:true,exitFallback:true}]){
   const x=run(kind,scenario);
   assert.deepEqual(x.frozen,{camera:{target:[1,2,3]},target:{target:[1,2,3]}},'reader freezes the exact observation pose');
   assert.deepEqual(x.camera,x.frozen.camera,'closing does not jump to the destination');
   assert.deepEqual(x.target,{target:[8,9,10]},'resume the pre-reader camera destination');
   assert.equal(x.calls.filter(c=>c==='closed').length,1);
   assert.ok(x.calls.includes('fallback:LOC-TEST'));
  }
 });
 test(kind+' settled returns keep the camera and destination identical',()=>{
  const x=run(kind,{roundTrip:true,settled:true});
  assert.deepEqual(x.camera,x.target);assert.deepEqual(x.camera,x.frozen.camera);
 });
}
