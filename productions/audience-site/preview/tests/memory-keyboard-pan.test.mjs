import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
const source=readFileSync(new URL('../memory-ui.mjs',import.meta.url),'utf8');

function setup({view='FOLIO',zoom=false,open=true}={}){
 const start=source.indexOf("document.addEventListener('keydown'"),end=source.indexOf('},true);',start);
 assert.ok(start>=0&&end>start,'actual historical key handler');
 const moves=[],scrolls=[];let exits=0,handler;
 const document={addEventListener:(kind,fn,capture)=>{assert.equal(kind,'keydown');assert.equal(capture,true);handler=fn;}};
 new Function('document','$','nextMemory','exitMemory','memorySession','memoryZoom',source.slice(start,end+8))(document,selector=>{
  assert.equal(selector,'#memoryViewport');return {scrollBy:opts=>scrolls.push(opts)};
 },delta=>moves.push(delta),()=>exits++,open?{view}:null,zoom);
 const key=(key,extra={})=>{let prevented=false,stopped=false;handler({key,preventDefault:()=>{prevented=true;},stopImmediatePropagation:()=>{stopped=true;},...extra});return {prevented,stopped};};
 return {key,moves,scrolls,exits:()=>exits};
}
test('zoomed original arrow keys pan without turning or resetting the folio',()=>{
 const x=setup({zoom:true});
 for(const key of ['ArrowLeft','ArrowRight','ArrowUp','ArrowDown'])assert.deepEqual(x.key(key),{prevented:true,stopped:true});
 assert.deepEqual(x.scrolls,[{left:-48,top:0,behavior:'auto'},{left:48,top:0,behavior:'auto'},{left:0,top:-48,behavior:'auto'},{left:0,top:48,behavior:'auto'}]);
 assert.deepEqual(x.moves,[]);assert.equal(x.exits(),0);
});
test('fitted folio and scenic detail retain page shortcuts',()=>{
 for(const view of ['FOLIO','SCENE']){
  const x=setup({view});assert.deepEqual(x.key('ArrowLeft'),{prevented:true,stopped:true});
  assert.deepEqual(x.key('ArrowRight'),{prevented:true,stopped:true});
  assert.deepEqual(x.moves,[-1,1]);assert.deepEqual(x.scrolls,[]);
  assert.deepEqual(x.key('ArrowUp'),{prevented:false,stopped:false});
 }
});
test('modifier shortcuts and previously handled keys are not stolen',()=>{
 for(const zoom of [false,true]){
  const x=setup({zoom});
  for(const extra of [{altKey:true},{ctrlKey:true},{metaKey:true},{shiftKey:true},{defaultPrevented:true}]){
   assert.deepEqual(x.key('ArrowRight',extra),{prevented:false,stopped:false});
  }
  assert.deepEqual(x.moves,[]);assert.deepEqual(x.scrolls,[]);
 }
});
test('Escape returns in either view without panning or turning',()=>{
 for(const zoom of [false,true]){
  const x=setup({zoom});assert.deepEqual(x.key('Escape'),{prevented:true,stopped:true});
  assert.equal(x.exits(),1);assert.deepEqual(x.moves,[]);assert.deepEqual(x.scrolls,[]);
 }
});
test('closed history does not consume world keys',()=>{
 const x=setup({open:false,zoom:true});
 for(const key of ['Escape','ArrowLeft','ArrowRight','ArrowUp','ArrowDown'])assert.deepEqual(x.key(key),{prevented:false,stopped:false});
 assert.equal(x.exits(),0);assert.deepEqual(x.moves,[]);assert.deepEqual(x.scrolls,[]);
});
