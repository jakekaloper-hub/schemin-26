import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
const read=name=>readFileSync(new URL('../'+name,import.meta.url),'utf8');
const gate=read('app.mjs').match(/function canControl\(\)\{[^\n]+\}/)?.[0];
assert.ok(gate,'reuse the actual shared world input gate');
function entry(name,kind){
 const s=read(name),start=s.indexOf('function enter'+kind+'('),end=s.indexOf('\n}',start);
 assert.ok(start>=0&&end>start);
 return s.slice(start,end+2);
}
const entries={History:entry('place-history-ui.mjs','History'),Memory:entry('memory-ui.mjs','Memory')};
// Source-executing DOM stub: no real browser, GPU, private folios, or canonical data.
function run(kind,scenario={}){
 const calls=[],node={focus(){calls.push('focus')},append(){},replaceChildren(){},setAttribute(){}};
 const env={
  state:{phase:scenario.phase??'EXPLORING',inputOwner:scenario.owner??'WORLD'},
  $:id=>id==='#fallback'?{hidden:!scenario.fallback}:node,
  selected:scenario.noSelected?null:{id:'LOC-TEST',name:'Synthetic place'},
  selectedMemory:()=>{calls.push('lookup');return scenario.noMemory?null:{pages:[]}},
  document:{activeElement:node,body:{classList:{add(){calls.push('body')}}}},
  catalog:{history:{status:'RELEASE_CANDIDATE'},stateAsOf:'end_of_week_3_2026'},
  memoryIndex:{},openMemory:()=>{calls.push('open');return {}},
  openPlaceHistory:()=>{calls.push('open');return {entries:[]}},
  memoryView:s=>s,innerWidth:1000,historyEntries:node,
  historyDialog:{showModal(){calls.push('modal')}},memoryDialog:{showModal(){calls.push('modal')}},
  memoryButtons:[],showMemoryPage:()=>calls.push('load'),structuredClone
 };
 const factory=new Function(...Object.keys(env),
  'let historySession='+(scenario.history?'{}':'null')+',memorySession='+(scenario.memory?'{}':'null')+
  ',historyPreviousFocus,memoryPreviousFocus,camera={target:[1,2,3]},target={target:[8,9,10]},pointers=new Map([[1,{}]]),pointerStart={},pinchDistance=5,memoryGeneration=0,memoryZoom;\n'+
  gate+'\n'+entries[kind]+'\nenter'+kind+'();return {camera,target,pointerCount:pointers.size};');
 return {calls,...factory(...Object.values(env))};
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
  }
 });
 test(kind+' still opens from an active selected world view and freezes the approach',()=>{
  const x=run(kind);
  assert.equal(x.calls.filter(c=>c==='open').length,1);
  assert.equal(x.calls.filter(c=>c==='modal').length,1);
  assert.deepEqual(x.target,x.camera);
  assert.equal(x.pointerCount,0);
 });
}
test('missing private edition remains unavailable without opening or changing camera',()=>{
 const x=run('Memory',{noMemory:true});
 assert.deepEqual(x.calls,['lookup']);
 assert.deepEqual(x.target,{target:[8,9,10]});
 assert.equal(x.pointerCount,1);
});
