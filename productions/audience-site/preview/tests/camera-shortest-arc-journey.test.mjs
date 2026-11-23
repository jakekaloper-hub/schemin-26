import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {defaultCamera,locationCamera,cameraStep,shortestCameraYawArc,nearestObserverViewYaw,spatialBindings} from '../spatial.mjs';
import {buildObserverCatalog} from '../../scripts/build-observer-catalog.mjs';

const app=readFileSync(new URL('../app.mjs',import.meta.url),'utf8');
const spatial=readFileSync(new URL('../spatial.mjs',import.meta.url),'utf8');
const read=name=>JSON.parse(readFileSync(new URL('../../../../world/data/'+name,import.meta.url),'utf8'));
const catalog=buildObserverCatalog({locations:read('locations.json'),weatherRegions:read('weather_regions.json'),worldState:read('current_world_state.json'),revision:'0'.repeat(40)});

test('three full user orbits preserve intended drag then yield a short world-to-place flight',()=>{
 const bindings=spatialBindings(catalog),before=JSON.stringify(bindings);
 let rendered=defaultCamera();
 // Deliberate user input remains unwrapped, even beyond three rotations.
 for(let i=0;i<18;i++)rendered=cameraStep(rendered,{yaw:Math.PI/3});
 assert.ok(rendered.yaw>5*Math.PI);
 const location=locationCamera(bindings,'LOC-COUNTRY-CLUB-JACKSON');
 const target=nearestObserverViewYaw(rendered,location);
 assert.ok(Math.abs(target.yaw-rendered.yaw)<Math.PI,'navigation destination must be the nearest angular equivalent');
 let current={...rendered,target:[...rendered.target]},travel=0;
 for(let i=0;i<120;i++){
  const prior=current.yaw,f=1-Math.exp(-1/60*6);
  current={target:current.target.map((v,k)=>v+(target.target[k]-v)*f),
   distance:current.distance+(target.distance-current.distance)*f,
   yaw:current.yaw+(target.yaw-current.yaw)*f,
   pitch:current.pitch+(target.pitch-current.pitch)*f};
  travel+=Math.abs(current.yaw-prior);
 }
 assert.ok(travel<Math.PI,'view transition cannot spin through past revolutions');
 assert.ok(Math.abs(shortestCameraYawArc(current.yaw,location.yaw))<.0001,'arrives at original source-bound viewing orientation');
 assert.ok(Math.hypot(...current.target.map((v,i)=>v-location.target[i]))<.001,'retains source Atlas anchor');
 assert.equal(JSON.stringify(bindings),before);
 assert.equal(bindings.length,23,'all established places remain visible');
});

test('nearest yaw crosses the ±π seam without jumping and handles antipodes consistently',()=>{
 assert.ok(Math.abs(shortestCameraYawArc(Math.PI-.01,-Math.PI+.02)-.03)<1e-10);
 assert.ok(Math.abs(shortestCameraYawArc(-Math.PI+.02,Math.PI-.01)+.03)<1e-10);
 assert.equal(shortestCameraYawArc(0,Math.PI),Math.PI);
 assert.equal(shortestCameraYawArc(0,-Math.PI),-Math.PI);
 assert.ok(Math.abs(shortestCameraYawArc(6*Math.PI+.10,.15)-.05)<1e-10);
 for(const bad of [NaN,Infinity,-Infinity,'1',undefined]){
  assert.throws(()=>shortestCameraYawArc(bad,0),/INVALID_CAMERA_YAW/);
  assert.throws(()=>shortestCameraYawArc(0,bad),/INVALID_CAMERA_YAW/);
 }
});

test('retargeting preserves physical camera framing and never mutates source or inputs',()=>{
 const initial={target:[-28,12,49],distance:130,pitch:.9,yaw:19.2};
 const desired={target:[14,0,52],distance:30,pitch:.65,yaw:.12};
 const original=JSON.stringify({initial,desired});
 const destination=nearestObserverViewYaw(initial,desired);
 assert.deepEqual(destination.target,desired.target);
 assert.equal(nearestObserverViewYaw({...initial,yaw:.2},{...desired,yaw:0}).yaw,0,'local navigation retains the exact target yaw, including zero');
 assert.notStrictEqual(destination.target,desired.target,'return an independent target array');
 assert.equal(destination.distance,desired.distance);
 assert.equal(destination.pitch,desired.pitch);
 assert.ok(Math.abs(destination.yaw-initial.yaw)<=Math.PI);
 assert.equal(JSON.stringify({initial,desired}),original);
 for(const bad of [null,{...desired,target:[1,Infinity,3]}, {...desired,yaw:NaN}]){
  assert.throws(()=>nearestObserverViewYaw(initial,bad),/INVALID_CAMERA_VIEW/);
 }
});

test('real observer rebases only explicit navigation destinations, not manual drag, pause, reveal or history',()=>{
 assert.match(app,/const \{[^\n]*nearestObserverViewYaw[^\n]*\}=Spatial/);
 assert.match(app,/target=nearestObserverViewYaw\(camera,target\)/,'inspecting a place rebases yaw');
 assert.match(app,/target=nearestObserverViewYaw\(camera,defaultCamera\(\)\)/,'returning to whole world rebases yaw');
 assert.match(app,/target=nearestObserverViewYaw\(camera,overview\)/,'Wetlands overview rebases yaw');
 const viewHandlers=app.slice(app.indexOf("for(const b of document.querySelectorAll('[data-view]')"),app.indexOf('function setPaused'));
 assert.match(viewHandlers,/target=nearestObserverViewYaw\(camera,target\)/,'view-mode rebases yaw');
 assert.match(app,/else if\(state\.phase==='EXPLORING'&&!paused\)\{const f=1-Math\.exp\(-dt\*6\);for\(const k of \['distance','pitch','yaw'\]\)/,'raw damping remains for multi-turn user drag');
 assert.match(app,/if\(paused\)camera=structuredClone\(target\)/);
 assert.match(app,/if\(memorySession\|\|historySession\)\{lastTime=t;return;\}/);
 assert.match(app,/dispatch\(\{type:'world_view'\}\)/);
 assert.match(app,/const clock=observerClock\(new Date\(\)\.toISOString\(\)\)/);
 assert.match(app,/renderer\.render\(camera,animationTime,\{strength:light\.strength,storm:demo\|\|0,paused\}\)/);
 assert.doesNotMatch(spatial,/fetch\(|publishObserver|writeWorldState|createPrincipalCharacter/);
});
