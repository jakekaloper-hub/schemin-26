import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {cameraStep,defaultCamera} from '../spatial.mjs';
const source=readFileSync(new URL('../app.mjs',import.meta.url),'utf8');
const start=source.indexOf('function handleWorldKey(e){');
const end=source.indexOf("document.addEventListener('keydown',handleWorldKey);",start);
assert.ok(start>=0&&end>start);
function setup(){
 const calls=[],nodes=new Map();
 const $=id=>{if(!nodes.has(id))nodes.set(id,{hidden:true,isConnected:true,focus(){calls.push(id);}});return nodes.get(id);};
 const canvas=$('#world'),body={};
 let enabled=true;
 const build=new Function('$','canvas','document','canControl','escapePanels','cameraStep','defaultCamera',
 "let target=defaultCamera(),camera=defaultCamera(),paused=true,inspectionReturnFocus=$('#placesToggle');\n"+source.slice(start,end)+"\nreturn {handleWorldKey,snapshot:()=>({target,camera})};");
 const app=build($,canvas,{body},()=>enabled,()=>{for(const id of ['#placesPanel','#infoPanel','#inspector'])$(id).hidden=true;calls.push('close');},cameraStep,defaultCamera);
 const press=(key,target=canvas,extra={})=>{let prevented=false;app.handleWorldKey({key,target,preventDefault(){prevented=true;},...extra});return prevented;};
 return {$,canvas,body,calls,app,press,disable(){enabled=false;}};
}
test('history, memory or fallback input owner cannot close world panels or move camera',()=>{
 const x=setup();x.$('#inspector').hidden=false;x.disable();const before=x.app.snapshot();
 assert.equal(x.press('Escape'),false);assert.equal(x.press('ArrowLeft'),false);
 assert.deepEqual(x.app.snapshot(),before);assert.deepEqual(x.calls,[]);assert.equal(x.$('#inspector').hidden,false);
});
test('Escape restores each visible panel opener instead of stealing focus to the canvas',()=>{
 for(const [panel,opener] of [['#placesPanel','#placesToggle'],['#infoPanel','#infoToggle'],['#inspector','#placesToggle']]){
  const x=setup();x.$(panel).hidden=false;
  assert.equal(x.press('Escape',{}),true);assert.deepEqual(x.calls,['close',opener]);assert.equal(x.$(panel).hidden,true);
 }
 const x=setup();x.$('#inspector').hidden=false;x.$('#placesToggle').isConnected=false;
 assert.equal(x.press('Escape'),true);assert.deepEqual(x.calls,['close','#world']);
});
test('native controls, modifiers and already consumed keys never pan the world',()=>{
 const x=setup();const before=x.app.snapshot();
 assert.equal(x.press('ArrowRight',{}),false);assert.equal(x.press('+',{},{}),false);
 assert.equal(x.press('ArrowLeft',x.canvas,{ctrlKey:true}),false);
 assert.equal(x.press('ArrowLeft',x.canvas,{defaultPrevented:true}),false);
 assert.equal(x.press('Escape'),false);assert.deepEqual(x.app.snapshot(),before);
});
test('focused world retains arrow and zoom navigation, including paused camera updates',()=>{
 const x=setup();const before=x.app.snapshot().target;
 assert.equal(x.press('ArrowRight'),true);assert.notDeepEqual(x.app.snapshot().target,before);
 assert.equal(x.press('+',x.body),true);assert.deepEqual(x.app.snapshot().camera,x.app.snapshot().target);
});
