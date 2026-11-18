import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {cameraStep} from '../spatial.mjs';

const source=readFileSync(new URL('../app.mjs',import.meta.url),'utf8');
const template=readFileSync(new URL('../index.template.html',import.meta.url),'utf8');
const begin=source.indexOf("canvas.addEventListener('pointerdown'");
const end=source.indexOf("canvas.addEventListener('wheel'",begin);
assert.ok(begin>0&&end>begin,'real pointer handlers exist');
const handlers=source.slice(begin,end);

function setup({paused=false,control=true}={}){
 const events={},selections=[],captures=[],calls={pick:0},ui={};
 const canvas={style:{},setPointerCapture:id=>captures.push(id),addEventListener:(type,callback)=>events[type]=callback};
 const $=id=>ui[id]??(ui[id]={hidden:true,textContent:'',style:{}});
 const renderer={pick(x,y){calls.pick++;return{id:'LOC-MUD-DOGS-SWAMP',name:'Mud Dogs Swamp'};}};
 const evaluate=new Function('canvas','$','renderer','canControl','cameraStep','structuredClone','select','innerWidth',
  "let pointers=new Map(),pointerStart=null,dragDistance=0,pinchDistance=null,pinchCenter=null,multiTouchGesture=false;"+
  "let target={target:[0,0,0],yaw:0,pitch:.7,distance:80},camera=structuredClone(target),paused="+JSON.stringify(paused)+";"+
  handlers+
  "return {snapshot:()=>({target:structuredClone(target),camera:structuredClone(camera),pointerCount:pointers.size,multiTouchGesture,dragDistance})};");
 const api=evaluate(canvas,$,renderer,()=>control,cameraStep,structuredClone,id=>selections.push(id),1000);
 const pointer=(type,id,x,y,extra={})=>events[type]({pointerId:id,clientX:x,clientY:y,pointerType:'touch',button:0,shiftKey:false,...extra});
 return {pointer,api,selections,captures,calls,ui};
}

test('two-finger centroid moves orbit yaw/pitch while pinch changes distance without selecting',()=>{
 const x=setup();
 x.pointer('pointerdown',1,100,100);
 x.pointer('pointerdown',2,200,100);
 const before=x.api.snapshot();
 x.pointer('pointermove',1,110,110);
 const during=x.api.snapshot();
 assert.notEqual(during.target.yaw,before.target.yaw,'touch orbit yaw');
 assert.notEqual(during.target.pitch,before.target.pitch,'touch orbit pitch');
 assert.notEqual(during.target.distance,before.target.distance,'pinch zoom');
 assert.deepEqual(during.target.target,[0,0,0],'orbit does not rewrite the geographic anchor');
 assert.equal(during.multiTouchGesture,true);
 x.pointer('pointerup',2,200,100);
 const half=x.api.snapshot();
 x.pointer('pointermove',1,135,130);
 assert.deepEqual(x.api.snapshot().target,half.target,'orphan finger cannot cause camera jump');
 x.pointer('pointerup',1,135,130);
 assert.deepEqual(x.selections,[]);
 assert.equal(x.calls.pick,0);
 assert.equal(x.api.snapshot().pointerCount,0);
});

test('one-finger pan and genuine tap inspection still work, with paused camera snapping to target',()=>{
 const x=setup({paused:true});
 x.pointer('pointerdown',7,80,90);
 x.pointer('pointermove',7,112,109);
 const moved=x.api.snapshot();
 assert.notDeepEqual(moved.target.target,[0,0,0]);
 assert.equal(moved.target.yaw,0,'one finger does not orbit');
 assert.deepEqual(moved.camera,moved.target,'paused preview uses the current desired camera immediately');
 x.pointer('pointerup',7,112,109);
 assert.equal(x.calls.pick,0,'drag is not a place tap');
 x.pointer('pointerdown',8,150,170);
 x.pointer('pointerup',8,150,170);
 assert.deepEqual(x.selections,['LOC-MUD-DOGS-SWAMP']);
 assert.equal(x.calls.pick,1);
 assert.deepEqual(x.captures,[7,8]);
});

test('third finger, cancellation, and unavailable world input never activate spurious inspection',()=>{
 const x=setup();
 x.pointer('pointerdown',1,100,100);
 x.pointer('pointerdown',2,160,100);
 x.pointer('pointerdown',3,220,100);
 const before=x.api.snapshot().target;
 x.pointer('pointermove',3,250,120);
 assert.deepEqual(x.api.snapshot().target,before,'third finger does not create an inconsistent orbit');
 x.pointer('pointercancel',3,250,120);
 x.pointer('pointerup',2,160,100);
 x.pointer('pointerup',1,100,100);
 assert.equal(x.calls.pick,0);
 assert.equal(x.api.snapshot().pointerCount,0);
 const blocked=setup({control:false});
 blocked.pointer('pointerdown',4,90,90);
 blocked.pointer('pointerup',4,90,90);
 assert.deepEqual(blocked.captures,[]);
 assert.equal(blocked.calls.pick,0);
 assert.match(source,/Drag to pan · Two-finger rotate or pinch · Tap a place/);
 assert.match(template,/two-finger drag orbits and a pinch changes distance/);
 assert.doesNotMatch(handlers,/fetch\(|publish|writeWorld|createEvent|historySession\s*=/);
});
