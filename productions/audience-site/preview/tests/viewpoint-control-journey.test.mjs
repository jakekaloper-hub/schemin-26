import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {defaultCamera,locationCamera,modeCamera,nearestObserverViewYaw,regionOverviewCamera} from '../spatial.mjs';
const host=readFileSync(new URL('../app.mjs',import.meta.url),'utf8');
const markup=readFileSync(new URL('../index.template.html',import.meta.url),'utf8');
const source=host.slice(host.indexOf('function syncViewControls('),host.indexOf('function setPaused('));
assert.ok(source.includes('function wholeWorld()'));
const controlGate=host.match(/^function canControl\(\)\{[^\n]+\}$/m)?.[0];
assert.ok(controlGate,'reuse actual world input ownership gate');
function setup(){
 const nodes={},doc={activeElement:null},actions=[];
 const $=id=>nodes[id]??(nodes[id]={hidden:false,isConnected:true,dataset:{},attrs:{},active:false,contains:()=>false,focus(){doc.activeElement=this;},setAttribute(k,v){this.attrs[k]=v;},classList:{toggle(k,v){nodes[id].active=v;}}});
 const modes=['AERIAL','OVERHEAD','PANORAMIC'];
 const views=modes.map(mode=>{const b=$(mode);b.dataset.view=mode;return b;});
 const wetlands=$('#wetlandsView');doc.querySelectorAll=()=>views;
 const canvas=$('#world');canvas.clientWidth=1440;canvas.clientHeight=900;
 const bindings=[{id:'LOC-MUD-DOGS-SWAMP',name:'Mud Dogs Swamp',zoneId:'REG-SOUTHERN-WETLANDS',anchor:[0,0,10],landmarks:[],canonStatus:'PERMANENT_CANON'}];
 const factory=new Function('$','document','canvas','bindings','catalog','dispatch','escapePanels','defaultCamera','locationCamera','modeCamera','nearestObserverViewYaw','regionOverviewCamera','updateMemoryEntry','updateHistoryEntry','structuredClone',
 'let state={phase:"EXPLORING",inputOwner:"WORLD"},camera=defaultCamera(),target=defaultCamera(),selected=null,paused=true,inspectionReturnFocus=canvas,renderer={height:()=>0},historySession=null,memorySession=null;\n'+controlGate+'\n'+source+'\nreturn {select,wholeWorld,syncViewControls,block:(owner)=>{historySession=owner==="HISTORY"?{}:null;memorySession=owner==="MEMORY"?{}:null;$("#fallback").hidden=owner!=="FALLBACK";state.inputOwner=owner==="READER"?"READER":"WORLD";state.phase=owner==="REVEALING"?"REVEALING":"EXPLORING";},snapshot:()=>({selected,target,camera})};');
 const api=factory($,doc,canvas,bindings,{stateAsOf:'end_of_week_3_2026'},a=>actions.push(a),()=>{},defaultCamera,locationCamera,modeCamera,nearestObserverViewYaw,regionOverviewCamera,()=>{},()=>{},structuredClone);
 api.block(null);
 function check(mode){for(const [i,b] of [...views,wetlands].entries()){const active=[...modes,'WETLANDS'][i]===mode;assert.equal(b.active,active);assert.equal(b.attrs['aria-pressed'],String(active));}}
 return {$,api,views,wetlands,check,actions};
}
test('actual viewpoint handlers keep selected visual and accessibility state synchronized through wetlands, place and whole-world navigation',()=>{
 const x=setup();x.api.syncViewControls('AERIAL');x.check('AERIAL');
 x.views[1].onclick();x.check('OVERHEAD');
 x.wetlands.onclick();x.check('WETLANDS');
 x.api.select('LOC-MUD-DOGS-SWAMP');x.check(null);
 x.$('#inspectorWorld').onclick();x.check('AERIAL');assert.equal(x.api.snapshot().selected,null);
 x.views[2].onclick();x.check('PANORAMIC');x.$('#returnWorld').onclick();x.check('AERIAL');
 assert.deepEqual(x.actions.map(a=>a.type),['camera','world_view','inspect','world_view','camera','world_view']);
});
test('initial markup has exactly one pressed viewpoint; whole world remains a momentary return action',()=>{
 for(const mode of ['AERIAL','OVERHEAD','PANORAMIC'])assert.match(markup,new RegExp('data-view="'+mode+'" aria-pressed="'+(mode==='AERIAL')+'"'));
 assert.match(markup,/id="wetlandsView" aria-pressed="false"/);
 assert.match(markup,/id="returnWorld">Whole world/);
});

test('stale navigation callbacks cannot change the selected source place or camera while reading, revealing or in graphics fallback',()=>{
 for(const owner of ['HISTORY','MEMORY','FALLBACK','READER','REVEALING']){
  const x=setup();x.api.select('LOC-MUD-DOGS-SWAMP');x.check(null);
  const before=structuredClone(x.api.snapshot()),actions=structuredClone(x.actions);
  x.api.block(owner);
  x.api.select('LOC-MUD-DOGS-SWAMP');x.$('#inspectorWorld').onclick();x.$('#returnWorld').onclick();
  for(const b of x.views)b.onclick();x.wetlands.onclick();x.$('#reframePlace').onclick();
  assert.deepEqual(x.api.snapshot(),before,owner);assert.deepEqual(x.actions,actions,owner);x.check(null);
  x.api.block(null);x.$('#inspectorWorld').onclick();x.check('AERIAL');
  assert.equal(x.api.snapshot().selected,null);assert.equal(x.actions.length,actions.length+1);
 }
});

test('inspector reframe restores the selected source view after another viewpoint without a new visit',()=>{
 const x=setup();x.api.select('LOC-MUD-DOGS-SWAMP');
 const expected=structuredClone(x.api.snapshot().target);
 x.views[1].onclick();x.check('OVERHEAD');assert.notDeepEqual(x.api.snapshot().target,expected);
 const actions=structuredClone(x.actions),selected=x.api.snapshot().selected;
 x.$('#reframePlace').onclick();x.check(null);
 assert.deepEqual(x.api.snapshot().target,expected);assert.deepEqual(x.api.snapshot().camera,expected);
 assert.equal(x.api.snapshot().selected,selected);assert.deepEqual(x.actions,actions);
 assert.equal(x.$('#inspector').hidden,false);
});
test('reframe with no selected place is inert and inspector has a native button',()=>{
 assert.match(markup,/id="reframePlace" type="button" class="textbutton">REFRAME SELECTED PLACE/);
 const x=setup(),before=structuredClone(x.api.snapshot());
 x.$('#reframePlace').onclick();assert.deepEqual(x.api.snapshot(),before);assert.deepEqual(x.actions,[]);
});
