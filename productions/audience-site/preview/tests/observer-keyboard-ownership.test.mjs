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
 const $=id=>{if(!nodes.has(id))nodes.set(id,{hidden:true,isConnected:true,setAttribute(){},focus(){calls.push(id);}});return nodes.get(id);};
 const canvas=$('#world'),body={};
 let enabled=true;
 const escape=source.slice(source.indexOf('function escapePanels(){'),source.indexOf('function indexButton(')).replace('function escapePanels(){','function clearPanels(){');
 const infoStart=source.indexOf('function closeInfo(){');
 const info=source.slice(infoStart>=0?infoStart:source.indexOf("$('#infoToggle').onclick="),source.indexOf("$('#placeSearch').oninput="));
 const build=new Function('$','canvas','document','canControl','cameraStep','defaultCamera','calls','structuredClone',
 "let target=defaultCamera(),camera=defaultCamera(),paused=true,inspectionReturnFocus=$('#placesToggle'),selected={id:'LOC-TEST'},infoFromInspector=false;function closeInspector(){};\n"+escape+"\nfunction escapePanels(){clearPanels();calls.push('close');}\n"+info+"\n"+source.slice(start,end)+"\nreturn {handleWorldKey,escapePanels,snapshot:()=>({target,camera}),setYaw:yaw=>{target.yaw=yaw;camera.yaw=yaw;}};");
 const app=build($,canvas,{body},()=>enabled,cameraStep,defaultCamera,calls,structuredClone);
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

test('source boundaries from the selected place return to that inspector without moving the camera',()=>{
 for(const dismiss of [x=>x.$('#infoClose').onclick(),x=>x.press('Escape',{}),x=>x.$('#infoToggle').onclick()]){
  const x=setup();x.$('#inspector').hidden=false;const before=x.app.snapshot();
  x.$('#inspectSource').onclick();
  assert.equal(x.$('#inspector').hidden,true);assert.equal(x.$('#infoPanel').hidden,false);
  assert.equal(x.calls.at(-1),'#infoClose');
  dismiss(x);
  assert.equal(x.$('#infoPanel').hidden,true);assert.equal(x.$('#inspector').hidden,false);
  assert.equal(x.calls.at(-1),'#inspectSource');assert.deepEqual(x.app.snapshot(),before);
 }
});
test('global info and unrelated panel navigation do not resurrect the prior inspector',()=>{
 const x=setup();x.$('#inspector').hidden=false;x.$('#inspectSource').onclick();
 x.app.escapePanels();x.$('#infoToggle').onclick();x.$('#infoClose').onclick();
 assert.equal(x.$('#inspector').hidden,true);assert.equal(x.calls.at(-1),'#infoToggle');
});
test('graphics or reader ownership prevents Escape and prevents restoring an unavailable world inspector',()=>{
 const x=setup();x.$('#inspector').hidden=false;x.$('#inspectSource').onclick();x.disable();
 assert.equal(x.press('Escape',{}),false);assert.equal(x.$('#infoPanel').hidden,false);
 x.$('#infoClose').onclick();assert.equal(x.$('#inspector').hidden,true);
});

test('arrow navigation stays screen-relative after orbiting the world',()=>{
 const cases=[
  [0,[[3,0],[-3,0],[0,-3],[0,3]]],
  [Math.PI/2,[[0,-3],[0,3],[-3,0],[3,0]]],
  [Math.PI,[[-3,0],[3,0],[0,3],[0,-3]]],
  [-Math.PI/2,[[0,3],[0,-3],[3,0],[-3,0]]]
 ];
 for(const [yaw,expected] of cases){
  for(const [i,key] of ['ArrowRight','ArrowLeft','ArrowUp','ArrowDown'].entries()){
   const x=setup();x.app.setYaw(yaw);
   assert.equal(x.press(key),true);
   const {target,camera}=x.app.snapshot(),[dx,dz]=expected[i];
   assert.ok(Math.abs(target.target[0]-dx)<1e-9&&Math.abs(target.target[2]-dz)<1e-9,`${key} at ${yaw}`);
   assert.equal(target.yaw,yaw);assert.deepEqual(camera,target);
  }
 }
});
