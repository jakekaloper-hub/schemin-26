import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
const host=readFileSync(new URL('../app.mjs',import.meta.url),'utf8');
const markup=readFileSync(new URL('../index.template.html',import.meta.url),'utf8');
const start=host.indexOf('function wholeWorld(){');
const end=host.indexOf("\n$('#placesToggle').onclick=",start);
assert.ok(start>=0&&end>start,'reuse the existing world transition');
const worldFn=host.slice(start,end);
function setup({origin='index',active='inside',connected=true,paused=true,phase='EXPLORING'}={}){
 const calls=[],actions=[],nodes={},document={activeElement:null};
 const $=id=>nodes[id]??(nodes[id]={hidden:false,isConnected:true,focus(options){document.activeElement=this;calls.push({id,options});}});
 const canvas=$('#world'),index=$('#placesToggle'),inside=$('#inspectorWorld'),toolbar=$('#returnWorld');
 $('#inspector').contains=el=>el===inside;index.isConnected=connected;
 document.activeElement=active==='inside'?inside:toolbar;
 const initial={target:[3,1,8],yaw:.2,pitch:.7,distance:25};
 const world={target:[0,0,0],yaw:0,pitch:1,distance:110};
 const factory=new Function('$','document','canvas','dispatch','defaultCamera','escapePanels','inspectionReturnFocus','structuredClone',
  'let state={phase:'+JSON.stringify(phase)+'},selected={id:"LOC-SOURCE"},target='+JSON.stringify(initial)+',camera='+JSON.stringify(initial)+',paused='+JSON.stringify(paused)+';\n'+worldFn+
  '\nreturn {wholeWorld,snapshot:()=>({selected,target,camera})};');
 const api=factory($,document,canvas,a=>actions.push(a),()=>structuredClone(world),
  ()=>{$('#inspector').hidden=true;$('#placesPanel').hidden=true;},origin==='index'?index:canvas,structuredClone);
 return {api,document,calls,actions,canvas,index,inside,toolbar,world,nodes};
}
test('inspector has visible direct world return and resets state, camera and keyboard focus',()=>{
 assert.equal((markup.match(/id="inspectorWorld"/g)||[]).length,1);
 assert.match(markup,/id="inspectorWorld" type="button" class="textbutton"/);
 assert.match(host,/\$\('#inspectorWorld'\)\.onclick=wholeWorld/);
 assert.match(host,/\$\('#returnWorld'\)\.onclick=wholeWorld/);
 const x=setup();x.api.wholeWorld();
 assert.deepEqual(x.actions,[{type:'world_view'}]);
 assert.equal(x.api.snapshot().selected,null);
 assert.deepEqual(x.api.snapshot().target,x.world);
 assert.deepEqual(x.api.snapshot().camera,x.world);
 assert.equal(x.nodes['#inspector'].hidden,true);
 assert.equal(x.document.activeElement,x.index);
 assert.deepEqual(x.calls.at(-1).options,{preventScroll:true});
});
test('canvas origin and disconnected index fall back safely without source/canon edits',()=>{
 for(const options of [{origin:'canvas'},{origin:'index',connected:false}]){
  const x=setup(options);x.api.wholeWorld();
  assert.equal(x.document.activeElement,x.canvas);
  assert.deepEqual(x.actions,[{type:'world_view'}]);
 }
 assert.doesNotMatch(worldFn,/fetch\(|publish|createEvent|writeWorld/);
});
test('existing outer whole-world toolbar retains focus and inactive phases do nothing',()=>{
 const x=setup({active:'toolbar',paused:false});const oldCamera=structuredClone(x.api.snapshot().camera);
 x.api.wholeWorld();assert.equal(x.document.activeElement,x.toolbar);
 assert.equal(x.calls.length,0);assert.deepEqual(x.api.snapshot().camera,oldCamera);
 const closed=setup({phase:'REVEALING'}),before=closed.api.snapshot();
 closed.api.wholeWorld();assert.deepEqual(closed.actions,[]);
 assert.deepEqual(closed.api.snapshot(),before);assert.equal(closed.calls.length,0);
});
