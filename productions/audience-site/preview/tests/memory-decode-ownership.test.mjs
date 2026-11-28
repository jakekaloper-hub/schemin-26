import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {memoryAssetResult} from '../memory.mjs';

const source=readFileSync(new URL('../memory-ui.mjs',import.meta.url),'utf8');
const start=source.indexOf('async function showMemoryPage(){');
const end=source.indexOf('\nfunction enterMemory()',start);
assert.ok(start>=0&&end>start);
const excerpt=source.slice(start,end);

// Execute the actual decode handler with controlled asynchronous image decodes.
// Synthetic images and DOM nodes; no private artwork or browser acceptance.
function harness(){
 const queue=[],nodes=new Map();
 const $=id=>{if(!nodes.has(id))nodes.set(id,{});return nodes.get(id);};
 class DeferredImage{
  naturalWidth=1;naturalHeight=1;
  decode(){return new Promise((resolve,reject)=>queue.push({resolve,reject}));}
 }
 const create=new Function('$','Image','memoryAssetResult',`
  const memoryImage=$('#memoryImage');
  let memorySession={pageIndex:0,loadToken:1,status:'LOADING'},memoryTouch=null,memoryGeneration=1;
  const currentMemory=()=>({pages:[{id:'a',width:1,height:1,alt:'A'},{id:'b',width:1,height:1,alt:'B'}]});
  const memoryAssets={a:'data:image/jpeg;base64,fixtureA',b:'data:image/jpeg;base64,fixtureB'};
  const syncMemoryChrome=()=>{},layoutMemoryImage=()=>{};
  ${excerpt}
  return {show:showMemoryPage,advance(){memorySession={...memorySession,pageIndex:1,loadToken:2,status:'LOADING'};},
   close(){memorySession=null;memoryGeneration++;},
   snapshot(){return {status:memorySession?.status,hidden:memoryImage.hidden,failure:$('#memoryFailure').hidden,loading:$('#memoryLoading').hidden,alt:memoryImage.alt};}};
 `);
 return {...create($,DeferredImage,memoryAssetResult),queue};
}

test('a stale same-page rejection cannot overwrite a successful newer retry',async()=>{
 const h=harness(),a=h.show(),b=h.show();
 h.queue[1].resolve();await b;
 const ready=h.snapshot();assert.equal(ready.status,'READY');assert.equal(ready.failure,true);
 h.queue[0].reject(Error('stale'));await a;
 assert.deepEqual(h.snapshot(),ready);
});
test('a stale same-page success cannot override a failed newer retry',async()=>{
 const h=harness(),a=h.show(),b=h.show();
 h.queue[1].reject(Error('latest'));await b;
 const failed=h.snapshot();assert.equal(failed.status,'FAILED');assert.equal(failed.hidden,true);
 h.queue[0].resolve();await a;
 assert.deepEqual(h.snapshot(),failed);
});
test('stale completion during a newer attempt does not hide its loading state',async()=>{
 const h=harness(),a=h.show(),b=h.show();
 const pending=h.snapshot();assert.equal(pending.loading,false);
 h.queue[0].resolve();await a;assert.deepEqual(h.snapshot(),pending);
 h.queue[1].resolve();await b;assert.equal(h.snapshot().status,'READY');
});
test('changing folios still rejects the previous page completion',async()=>{
 const h=harness(),a=h.show();h.advance();const b=h.show();
 h.queue[1].resolve();await b;
 const next=h.snapshot();assert.equal(next.alt,'B');assert.equal(next.status,'READY');
 h.queue[0].reject(Error('old page'));await a;assert.deepEqual(h.snapshot(),next);
});
test('closing the reader still retires pending decodes',async()=>{
 const h=harness(),a=h.show();h.close();const closed=h.snapshot();
 h.queue[0].resolve();await a;assert.deepEqual(h.snapshot(),closed);
});
