import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {historyForLocation,openPlaceHistory,closePlaceHistory} from '../place-history.mjs';
const host=readFileSync(new URL('../app.mjs',import.meta.url),'utf8');
const start=host.indexOf('function select(id){');
const end=host.indexOf('\nfunction wholeWorld(){',start);
assert.ok(start>=0&&end>start,'observer inspection source is present');
const inspection=host.slice(start,end);
function setup(fromIndex){
 const doc={activeElement:null},nodes={},calls=[],actions=[];
 const node=id=>nodes[id]??(nodes[id]={
   hidden:id!=='#inspector',textContent:'',tabIndex:0,isConnected:true,
   focus(options){doc.activeElement=this;calls.push({id,options});},contains:()=>false
 });
 const $=node,canvas=node('#world'),indexButton=node('#indexButton');
 node('#placeList').contains=el=>el===indexButton;
 doc.activeElement=fromIndex?indexButton:canvas;
 const bindings=Array.from({length:23},(_,i)=>({
   id:'LOC-'+i,name:'Atlas place '+i,zoneId:'REG-SOUTHERN-WETLANDS',
   landmarks:['source landmark '+i],canonStatus:'PERMANENT_CANON',anchor:[i,0,0]
 }));
 const catalog={locations:bindings,stateAsOf:'end_of_week_3_2026',history:{
   status:'RELEASE_CANDIDATE',publicationAuthorized:false,events:[{
     id:'EVT-EXACT',locationId:'LOC-0',year:2026,week:3,publicationAuthorized:false,
     effects:{physical:['recorded effect'],social:[],reputation:[],institutional:[]},
     sourceReceipts:['memo-os/source.md']
   }]
 }};
 const before=JSON.stringify(catalog),updates=[];
 const init=new Function('$','document','bindings','catalog','canvas','dispatch','escapePanels',
   'locationCamera','renderer','updateMemoryEntry','updateHistoryEntry',
   "let state={phase:'EXPLORING',inputOwner:'WORLD'},selected=null,target=null,camera=null,paused=false,inspectionReturnFocus=canvas;\n"+inspection+
   "\nreturn {select,closeInspector,snapshot:()=>({selected,target,inspectionReturnFocus})};");
 const app=init($,doc,bindings,catalog,canvas,action=>actions.push(action),
   ()=>{node('#placesPanel').hidden=true;node('#inspector').hidden=true;},
   (places,id)=>({target:[...places.find(x=>x.id===id).anchor],distance:30,yaw:0,pitch:.65}),
   {height:()=>0,siteView:()=>null},()=>updates.push('memory'),()=>updates.push('history'));
 return {$,app,doc,bindings,catalog,before,calls,actions,updates,canvas};
}
test('index→source place→historical record→exact viewpoint return does not lose focus or mutate canon',()=>{
 const x=setup(true);
 assert.equal(x.bindings.length,23);
 x.app.select('LOC-0');
 assert.equal(x.doc.activeElement,x.$('#placeName'));
 assert.equal(x.$('#placeName').tabIndex,-1);
 assert.equal(x.$('#inspector').hidden,false);
 assert.equal(x.$('#placeName').textContent,'Atlas place 0');
 assert.deepEqual(x.updates,['memory','history']);
 assert.deepEqual(x.actions,[{type:'inspect',id:'LOC-0'}]);
 assert.equal(x.app.snapshot().selected.id,'LOC-0');
 assert.equal(historyForLocation(x.catalog,'LOC-0').length,1);
 const camera=x.app.snapshot().target;
 const session=openPlaceHistory(x.catalog,'LOC-0',camera);
 assert.equal(session.inputOwner,'HISTORY');
 assert.equal(session.worldMutationAllowed,false);
 assert.equal(session.liveWeatherAllowed,false);
 assert.deepEqual(closePlaceHistory(session).camera,camera);
 x.app.closeInspector();
 assert.equal(x.doc.activeElement,x.$('#placesToggle'));
 assert.equal(x.$('#inspector').hidden,true);
 assert.equal(x.calls.at(-1).options.preventScroll,true);
 assert.equal(JSON.stringify(x.catalog),x.before);
});
test('canvas picks retain canvas focus and other locations cannot borrow historical records',()=>{
 const x=setup(false);
 x.app.select('LOC-8');
 assert.equal(x.doc.activeElement,x.canvas);
 assert.equal(x.app.snapshot().inspectionReturnFocus,x.canvas);
 assert.deepEqual(historyForLocation(x.catalog,'LOC-8'),[]);
 x.app.closeInspector();
 assert.equal(x.doc.activeElement,x.canvas);
 assert.equal(JSON.stringify(x.catalog),x.before);
});
test('disconnected focus return target falls back to canvas',()=>{
 const x=setup(true);x.app.select('LOC-0');
 x.$('#placesToggle').isConnected=false;
 x.app.closeInspector();
 assert.equal(x.doc.activeElement,x.canvas);
 assert.match(host,/\$\('#inspectorClose'\)\.onclick=closeInspector/);
 assert.match(host,/\$\('#inspectSource'\)\.onclick=\(\)=>\{[^}]*\$\('#infoClose'\)\.focus/);
 assert.doesNotMatch(inspection,/fetch\(|publish|writeWorld|createEvent/);
});
