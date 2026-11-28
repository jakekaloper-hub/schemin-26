import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
const source=readFileSync(new URL('../memory-ui.mjs',import.meta.url),'utf8');

function setup(source){
 const start=source.indexOf("$('#memoryViewport').addEventListener('pointerdown'"),end=source.indexOf("window.addEventListener('resize'",start);
 assert.ok(start>=0&&end>start,'actual memory gesture handlers');
 const handlers=source.slice(start,end),events={},moves=[];
 const api=new Function('$','nextMemory','let memorySession={},memoryZoom=false,memoryTouch=null;'+handlers+';return {setSession:v=>memorySession=v,setZoom:v=>memoryZoom=v};')(()=>({addEventListener:(kind,fn)=>events[kind]=fn}),delta=>moves.push(delta));
 const pointer=(kind,id,x,y,extra={})=>events[kind]?.({pointerId:id,pointerType:'touch',isPrimary:true,clientX:x,clientY:y,...extra});
 return {pointer,moves,...api};
}
test('only the initiating primary touch can turn an open historical folio',()=>{
 const x=setup(source);
 x.pointer('pointerdown',1,200,50);
 x.pointer('pointerup',9,100,50,{pointerType:'mouse'});
 assert.deepEqual(x.moves,[]);
 x.pointer('pointerup',2,100,50,{isPrimary:false});
 assert.deepEqual(x.moves,[]);
 x.pointer('pointerup',1,100,50);
 assert.deepEqual(x.moves,[1]);
 x.pointer('pointerdown',3,100,50);
 x.pointer('pointerup',3,200,50);
 assert.deepEqual(x.moves,[1,-1]);
});
test('second touch retires the swipe so a pinch cannot turn historical pages',()=>{
 const x=setup(source);
 x.pointer('pointerdown',1,200,50);
 x.pointer('pointerdown',2,190,50,{isPrimary:false});
 x.pointer('pointerup',1,90,50);
 x.pointer('pointerup',2,290,50,{isPrimary:false});
 assert.deepEqual(x.moves,[]);
});
test('closed or zoomed readers do not dispatch a stale swipe',()=>{
 for(const change of [x=>x.setSession(null),x=>x.setZoom(true)]){
  const x=setup(source);
  x.pointer('pointerdown',1,200,50);change(x);x.pointer('pointerup',1,90,50);
  assert.deepEqual(x.moves,[]);
 }
});
test('only matching cancellation or capture loss retires a gesture',()=>{
 for(const kind of ['pointercancel','lostpointercapture']){
  const x=setup(source);
  x.pointer('pointerdown',1,200,50);
  x.pointer(kind,9,0,0);
  x.pointer('pointerup',1,100,50);
  assert.deepEqual(x.moves,[1]);
  x.pointer('pointerdown',2,200,50);
  x.pointer(kind,2,0,0);
  x.pointer('pointerup',2,100,50);
  assert.deepEqual(x.moves,[1]);
 }
});
test('small or vertical movements and zoomed entry do not turn a page',()=>{
 const x=setup(source);
 x.pointer('pointerdown',1,100,50);x.pointer('pointerup',1,125,50);
 x.pointer('pointerdown',2,100,50);x.pointer('pointerup',2,180,150);
 x.setZoom(true);x.pointer('pointerdown',3,200,50);x.pointer('pointerup',3,100,50);
 assert.deepEqual(x.moves,[]);
});
test('page, view, zoom and reader exit invalidate the prior touch origin',()=>{
 assert.match(source,/async function showMemoryPage\(\)\{\s*memoryTouch=null;/);
 assert.match(source,/function exitMemory\(\)\{\s*memoryTouch=null;/);
 assert.match(source,/\$\('#memoryView'\)\.onclick=\(\)=>\{memoryTouch=null;/);
 assert.match(source,/\$\('#memoryZoom'\)\.onclick=\(\)=>\{memoryTouch=null;/);
 assert.match(source,/function enterMemory\(\)\{[\s\S]*?showMemoryPage\(\);/);
});
test('fit original folios reserve horizontal swipes but zoomed folios retain native two-axis pan',()=>{
 const template=readFileSync(new URL('../index.template.html',import.meta.url),'utf8');
 const fit=template.match(/#memoryViewport\.original\{([^}]+)\}/)?.[1];
 const zoomed=template.match(/#memoryViewport\.original\.zoomed\{([^}]+)\}/)?.[1];
 assert.ok(fit,'original folio viewport rule');
 assert.match(fit,/(?:^|;)touch-action:pan-y(?:;|$)/);
 assert.ok(zoomed,'zoomed original viewport rule');
 assert.match(zoomed,/(?:^|;)touch-action:pan-x pan-y(?:;|$)/);
 assert.match(fit,/(?:^|;)overflow:auto(?:;|$)/);
});
