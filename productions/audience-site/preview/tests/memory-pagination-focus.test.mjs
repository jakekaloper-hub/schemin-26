import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';

const source=readFileSync(new URL('../memory-ui.mjs',import.meta.url),'utf8');
const start=source.indexOf('function syncMemoryChrome(){');
const end=source.indexOf('\nasync function showMemoryPage()',start);
assert.ok(start>=0&&end>start);
const excerpt=source.slice(start,end);

// Execute the real chrome update; a synthetic DOM models focus loss when a
// focused native button becomes disabled. This is not a browser/AT acceptance test.
function run({count=3,index,focus}){
 const document={activeElement:null},events=[],nodes=new Map();
 function button(id){
  let disabled=false;const attrs={};
  return {id,dataset:{},textContent:'',setAttribute(key,value){attrs[key]=value;},focus(options){
   if(disabled)throw Error('focused disabled button');
   document.activeElement=this;events.push(['focus',id,options,attrs['aria-current']]);
  },get disabled(){return disabled;},set disabled(value){
   disabled=value;events.push(['disabled',id,value]);
   if(value&&document.activeElement===this)document.activeElement=null;
  }};
 }
 const $=id=>{if(!nodes.has(id))nodes.set(id,button(id));return nodes.get(id);};
 const pages=Array.from({length:count},(_,i)=>({title:'Page '+i,pdfPage:i+1}));
 const memoryButtons=pages.map((_,i)=>{const b=button('page'+i);b.dataset.memoryPage=String(i);return b;});
 document.activeElement=focus.startsWith('page')?memoryButtons[Number(focus.slice(4))]:$(focus);
 const memorySession={pageIndex:index,view:'FOLIO',loadToken:2};
 new Function('$','document','currentMemory','memorySession','memoryButtons','layoutMemoryImage',excerpt+'\nsyncMemoryChrome();')(
  $,document,()=>({pages}),memorySession,memoryButtons,()=>{});
 return {focus:document.activeElement?.id,events,previous:$('#memoryPrevious').disabled,next:$('#memoryNext').disabled,session:memorySession};
}
test('last page retains keyboard focus before Next becomes disabled',()=>{
 const x=run({index:2,focus:'#memoryNext'});
 assert.equal(x.focus,'page2');assert.equal(x.next,true);assert.equal(x.previous,false);
 assert.ok(x.events.findIndex(e=>e[0]==='focus')<x.events.findIndex(e=>e[0]==='disabled'&&e[1]==='#memoryNext'));
 assert.deepEqual(x.events.find(e=>e[0]==='focus'),['focus','page2',{preventScroll:true},'page']);
});
test('first page retains keyboard focus before Previous becomes disabled',()=>{
 const x=run({index:0,focus:'#memoryPrevious'});
 assert.equal(x.focus,'page0');assert.equal(x.previous,true);assert.equal(x.next,false);
 assert.ok(x.events.findIndex(e=>e[0]==='focus')<x.events.findIndex(e=>e[0]==='disabled'&&e[1]==='#memoryPrevious'));
});
test('interior pagination and unrelated reader controls never have focus stolen',()=>{
 for(const scenario of [{index:1,focus:'#memoryNext'},{index:1,focus:'#memoryPrevious'},{index:2,focus:'page1'},{index:0,focus:'#memoryBack'},{index:0,focus:'#memoryRetry'}]){
  const x=run(scenario);assert.equal(x.focus,scenario.focus);
  assert.equal(x.events.some(e=>e[0]==='focus'),false);
  assert.deepEqual(x.session,{pageIndex:scenario.index,view:'FOLIO',loadToken:2});
 }
});
test('single-page memory keeps a focused boundary control in the reader',()=>{
 for(const focus of ['#memoryNext','#memoryPrevious']){
  const x=run({count:1,index:0,focus});assert.equal(x.focus,'page0');assert.equal(x.previous,true);assert.equal(x.next,true);
 }
});
