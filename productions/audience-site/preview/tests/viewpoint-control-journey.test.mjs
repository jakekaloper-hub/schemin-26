import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {defaultCamera,locationCamera,modeCamera,nearestObserverViewYaw,regionOverviewCamera} from '../spatial.mjs';
const host=readFileSync(new URL('../app.mjs',import.meta.url),'utf8');
const markup=readFileSync(new URL('../index.template.html',import.meta.url),'utf8');
const source=host.slice(host.indexOf('function syncViewControls('),host.indexOf('function setPaused('));
assert.ok(source.includes('function wholeWorld()'));
function setup(){
 const nodes={},doc={activeElement:null},actions=[];
 const $=id=>nodes[id]??(nodes[id]={hidden:false,isConnected:true,dataset:{},attrs:{},active:false,contains:()=>false,focus(){doc.activeElement=this;},setAttribute(k,v){this.attrs[k]=v;},classList:{toggle(k,v){nodes[id].active=v;}}});
 const modes=['AERIAL','OVERHEAD','PANORAMIC'];
 const views=modes.map(mode=>{const b=$(mode);b.dataset.view=mode;return b;});
 const wetlands=$('#wetlandsView');doc.querySelectorAll=()=>views;
 const canvas=$('#world');canvas.clientWidth=1440;canvas.clientHeight=900;
 const bindings=[{id:'LOC-MUD-DOGS-SWAMP',name:'Mud Dogs Swamp',zoneId:'REG-SOUTHERN-WETLANDS',anchor:[0,0,10],landmarks:[],canonStatus:'PERMANENT_CANON'}];
 const factory=new Function('$','document','canvas','bindings','catalog','dispatch','escapePanels','defaultCamera','locationCamera','modeCamera','nearestObserverViewYaw','regionOverviewCamera','updateMemoryEntry','updateHistoryEntry','structuredClone','canControl',
 'let state={phase:"EXPLORING",inputOwner:"WORLD"},camera=defaultCamera(),target=defaultCamera(),selected=null,paused=true,inspectionReturnFocus=canvas,renderer={height:()=>0};\n'+source+'\nreturn {select,wholeWorld,syncViewControls,snapshot:()=>({selected,target,camera})};');
 const api=factory($,doc,canvas,bindings,{stateAsOf:'end_of_week_3_2026'},a=>actions.push(a),()=>{},defaultCamera,locationCamera,modeCamera,nearestObserverViewYaw,regionOverviewCamera,()=>{},()=>{},structuredClone,()=>true);
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
