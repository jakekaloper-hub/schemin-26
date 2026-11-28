import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {historyForLocation} from '../place-history.mjs';

const source=readFileSync(new URL('../app.mjs',import.meta.url),'utf8');
const layout=readFileSync(new URL('../index.template.html',import.meta.url),'utf8');
const snippet=source.match(/\/\* FALLBACK_JOURNEY_START:[\s\S]*?\*\/([\s\S]*?)\/\* FALLBACK_JOURNEY_END \*\//)?.[1];
class Element {
  constructor(tag,onFocus){this.tag=tag;this.children=[];this.dataset={};this.listeners={};this.textContent='';this.onFocus=onFocus;}
  append(...nodes){this.children.push(...nodes);}
  replaceChildren(...nodes){this.children=[...nodes];}
  addEventListener(type,handler){this.listeners[type]=handler;}
  focus(){this.onFocus(this);}
}
const fixture=(status='RELEASE_CANDIDATE')=>{
  const bindings=Array.from({length:23},(_,i)=>({id:'LOC-'+i,name:'Place '+i,landmarks:['landmark '+i],canonStatus:'PERMANENT_CANON'}));
  const event={id:'EVT-W2-EXACT',locationId:'LOC-0',year:2026,week:2,publicationAuthorized:false,
    effects:{physical:['recorded physical change'],social:['recorded social change'],reputation:[],institutional:[]},
    sourceReceipts:['memo-os/week-2/RECEIPT.md'],expiryCondition:'requires source restoration'};
  const catalog={locations:bindings,stateAsOf:'end_of_week_3_2026',history:{status,publicationAuthorized:false,events:[event]}};
  let focused=null;const create=tag=>new Element(tag,n=>focused=n);
  const nodes=Object.fromEntries(['#placeList','#fallbackPlaces','#fallbackDetail','#fallback','#retry'].map(key=>[key,create('div')]));
  assert.ok(snippet,'source-bound fallback block must exist');
  nodes['#fallback'].hidden=true;
  const restore=new Function('document','$','bindings','catalog','PlaceHistory','indexButton',snippet+'\nreturn restoreFallbackPlace;')(
    {createElement:create},key=>nodes[key],bindings,catalog,{historyForLocation},()=>create('button'));
  return {catalog,nodes,restore,focused:()=>focused};
};
const flatten=n=>[n.textContent||'',...n.children.flatMap(flatten)].join(' ');
const historyButton=d=>d.children.find(x=>x.dataset?.fallbackHistory);

test('fallback preserves 23 Atlas sites through place, recorded history, same-place return and all-place index',()=>{
  const x=fixture(),{nodes}=x,d=nodes['#fallbackDetail'];
  assert.equal(nodes['#placeList'].children.length,23);
  assert.equal(nodes['#fallbackPlaces'].children.length,23);
  const b=nodes['#fallbackPlaces'].children[0];b.listeners.click();
  assert.equal(x.focused().tag,'h2');assert.match(flatten(d),/Place 0/);
  const read=historyButton(d);assert.ok(read);assert.equal(read.dataset.fallbackHistory,'LOC-0');read.onclick();
  assert.equal(x.focused().tag,'button');
  assert.match(flatten(d),/EVT-W2-EXACT/);
  assert.match(flatten(d),/recorded physical change/);
  assert.match(flatten(d),/recorded social change/);
  assert.match(flatten(d),/memo-os\/week-2\/RECEIPT.md/);
  assert.match(flatten(d),/do not establish present-day conditions/);
  assert.equal(nodes['#fallbackPlaces'].children.length,23);
  d.children[0].onclick();assert.equal(x.focused().dataset.fallbackHistory,'LOC-0');
  d.children.find(n=>n.tag==='button'&&n.textContent.includes('All Atlas places')).onclick();
  assert.equal(d.children.length,0);assert.equal(x.focused(),b);
  assert.equal(x.catalog.history.events[0].id,'EVT-W2-EXACT');
});
test('unrecorded locations remain available, without borrowed story',()=>{
  const x=fixture(),d=x.nodes['#fallbackDetail'];
  x.nodes['#fallbackPlaces'].children[17].listeners.click();
  assert.match(flatten(d),/No location-exact World Memory entry/);
  assert.equal(historyButton(d),undefined);assert.equal(x.focused().tag,'h2');
});
test('invalid history authority fails closed and still leaves index',()=>{
  const x=fixture('PUBLISHED'),d=x.nodes['#fallbackDetail'];
  x.nodes['#fallbackPlaces'].children[0].listeners.click();
  assert.match(flatten(d),/did not pass its read-only authority checks/);
  assert.doesNotMatch(flatten(d),/recorded physical change/);
  assert.equal(historyButton(d),undefined);
  assert.equal(x.nodes['#fallbackPlaces'].children.length,23);
});
test('offline markup retains source-only and no-external-request bounds',()=>{
  assert.match(layout,/id="fallbackPlaces"/);assert.match(layout,/id="fallbackDetail"/);
  assert.match(layout,/#fallbackDetail \.fallback-history-record/);
  assert.match(source,/PlaceHistory\.historyForLocation\(catalog,place\.id\)/);
  assert.match(source,/Source receipt paths \(not public links\)/);
  assert.doesNotMatch(snippet,/fetch\(|localStorage|writeWorld|publish|createEvent/);
});

test('graphics-loss return uses exact location and restores the recorded-history control',()=>{
  const x=fixture(),d=x.nodes['#fallbackDetail'];
  assert.equal(x.restore('LOC-0',true),false);assert.equal(d.children.length,0);
  x.nodes['#fallback'].hidden=false;
  assert.equal(x.restore('LOC-0',true),true);
  assert.equal(x.focused().dataset.fallbackHistory,'LOC-0');
  assert.match(flatten(d),/Place 0/);assert.equal(x.nodes['#fallbackPlaces'].children.length,23);
  x.focused().onclick();assert.match(flatten(d),/EVT-W2-EXACT/);
  d.children[0].onclick();assert.equal(x.focused().dataset.fallbackHistory,'LOC-0');
  assert.equal(x.restore('LOC-17'),true);assert.equal(x.focused().tag,'h2');
  assert.match(flatten(d),/Place 17/);assert.equal(historyButton(d),undefined);
});
test('unknown or unselected graphics-loss return focuses retry without borrowing history',()=>{
  const x=fixture();x.nodes['#fallback'].hidden=false;
  assert.equal(x.restore('LOC-UNKNOWN',true),true);assert.equal(x.focused(),x.nodes['#retry']);
  assert.equal(x.nodes['#fallbackDetail'].children.length,0);
});

test('graphics loss defers handoff while a historical reader owns focus',()=>{
  const code=source.slice(source.indexOf('function showFallback('),source.indexOf('function escapePanels('));
  for(const owner of ['history','memory',null]){
    const nodes=Object.fromEntries(['#fallback','#fallbackReason','#splash','#skipReveal','#worldSurface'].map(key=>[key,{hidden:key!=='#worldSurface'}]));
    const calls=[];
    const loss=new Function('$','cancelAnimationFrame','restoreFallbackPlace','historySession','memorySession','cancelWorldGesture',
      'let ready=true,frameId=42,selected={id:"LOC-0"};'+code+';return showFallback;')(
      key=>nodes[key],id=>calls.push(id),id=>calls.push(id),owner==='history'?{}:null,owner==='memory'?{}:null,()=>calls.push('cancel gesture'));
    loss('graphics lost');assert.equal(nodes['#fallback'].hidden,false);assert.equal(nodes['#worldSurface'].hidden,true);
    assert.deepEqual(calls,owner?['cancel gesture',42]:['cancel gesture',42,'LOC-0']);
    loss('duplicate loss');assert.deepEqual(calls,owner?['cancel gesture',42,'cancel gesture',42]:['cancel gesture',42,'LOC-0','cancel gesture',42]);
  }
});
test('historical modal exit routes restored source ID before attempting world focus',()=>{
  for(const [kind,file] of [['history','place-history-ui.mjs'],['memory','memory-ui.mjs']]){
    const cap=kind[0].toUpperCase()+kind.slice(1),ui=readFileSync(new URL('../'+file,import.meta.url),'utf8');
    const start=ui.indexOf('function exit'+cap+'(){'),end=ui.indexOf('\n}',start)+2;
    assert.ok(start>=0&&end>start);
    for(const fallback of [true,false]){
      const calls=[],saved={locationId:'LOC-0',camera:{target:[1,2,3]}};
      const noop=()=>{};
      const exit=new Function(kind==='history'?'closePlaceHistory':'closeMemory',kind+'Dialog','document',kind+'PreviousFocus','restoreFallbackPlace','memoryImage',
        'let '+kind+'Session={},camera,target,lastTime,memoryGeneration=0,memoryZoom=false;'+ui.slice(start,end)+';return exit'+cap+';')(
        ()=>saved,{close:()=>calls.push('close')},{body:{classList:{remove:noop}}},{isConnected:true,focus:()=>calls.push('world focus')},
        (id,history)=>{calls.push([id,history??false]);return fallback;},{removeAttribute:noop});
      exit();assert.deepEqual(calls,['close',['LOC-0',kind==='history'],...fallback?[]:['world focus']]);
    }
  }
});

test('terminal fallback removes all graphics controls from navigation without hiding source readers',()=>{
  const start=layout.indexOf('<div id="worldSurface">'),end=layout.indexOf('</div><!-- worldSurface -->');
  assert.ok(start>=0&&end>start);
  const world=layout.slice(start,end),rest=layout.slice(end);
  for(const id of ['world','motionToggle','infoToggle','placesToggle','placesPanel','inspector','infoPanel','skipReveal','splash'])assert.ok(world.includes('id="'+id+'"'),id);
  assert.match(world,/class="skip"/);
  for(const id of ['fallback','fallbackPlaces','fallbackDetail','memoryDialog','historyDialog']){
    assert.ok(rest.includes('id="'+id+'"'),id);assert.ok(!world.includes('id="'+id+'"'),id);
  }
  assert.match(layout,/\[hidden\]\{display:none!important\}/);
});
