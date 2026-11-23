import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {defaultCamera,locationCamera,cameraStep,shortestCameraYawArc,easeObserverCamera,spatialBindings} from '../spatial.mjs';
import {buildObserverCatalog} from '../../scripts/build-observer-catalog.mjs';

const app=readFileSync(new URL('../app.mjs',import.meta.url),'utf8');
const spatial=readFileSync(new URL('../spatial.mjs',import.meta.url),'utf8');
const read=name=>JSON.parse(readFileSync(new URL('../../../../world/data/'+name,import.meta.url),'utf8'));
const catalog=buildObserverCatalog({locations:read('locations.json'),weatherRegions:read('weather_regions.json'),worldState:read('current_world_state.json'),revision:'0'.repeat(40)});

test('camera yaw uses the short visual arc after three full user orbits, not three reverse spins',()=>{
 const bindings=spatialBindings(catalog),before=JSON.stringify(bindings);
 const original=defaultCamera(),sameView={...original,yaw:original.yaw+3*2*Math.PI};
 const location=locationCamera(bindings,'LOC-COUNTRY-CLUB-JACKSON');
 let current={...sameView,target:[...sameView.target]},remaining=0;
 for(let i=0;i<120;i++){
  const prior=current.yaw;
  current=easeObserverCamera(current,location,1/60);
  const movement=Math.abs(current.yaw-prior);
  assert.ok(movement<.2,'no single-frame azimuth jump');
  remaining+=movement;
 }
 assert.ok(remaining<Math.PI,'no unnecessary orbit during world-to-place flight');
 assert.ok(Math.abs(shortestCameraYawArc(current.yaw,location.yaw))<.0001,'arrives at source-bound viewpoint orientation');
 assert.ok(Math.hypot(...current.target.map((v,i)=>v-location.target[i]))<.001,'approaches exact source Atlas anchor');
 assert.equal(JSON.stringify(bindings),before,'visual navigation must not change location identities or anchors');
 assert.equal(bindings.length,23,'all established places remain visible');
});

test('shortest arc crosses ±π seam without a full turn and handles direct antipodes deterministically',()=>{
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

test('damped flight retains original distance/elevation/target easing and no-source mutation',()=>{
 const initial={target:[-28,12,49],distance:130,pitch:.9,yaw:1.2};
 const desired={target:[14,0,52],distance:30,pitch:.65,yaw:.12};
 const original=JSON.stringify({initial,desired});
 const f=1-Math.exp(-.016*6);
 const step=easeObserverCamera(initial,desired,.016);
 for(const k of ['distance','pitch'])assert.ok(Math.abs(step[k]-(initial[k]+(desired[k]-initial[k])*f))<1e-12);
 for(let i=0;i<3;i++)assert.ok(Math.abs(step.target[i]-(initial.target[i]+(desired.target[i]-initial.target[i])*f))<1e-12);
 assert.equal(JSON.stringify({initial,desired}),original);
 assert.deepEqual(easeObserverCamera(initial,desired,0),initial);
 assert.throws(()=>easeObserverCamera(initial,desired,-.1),/INVALID_CAMERA_EASING/);
 assert.throws(()=>easeObserverCamera(initial,{...desired,target:[1,Infinity,3]},.016),/INVALID_CAMERA_EASING/);
 assert.throws(()=>easeObserverCamera(initial,desired,Infinity),/INVALID_CAMERA_EASING/);
});

test('actual observer uses shortest arc only during active exploration, preserving pause/reveal/history',()=>{
 assert.match(app,/const \{[^\n]*easeObserverCamera[^\n]*\}=Spatial/);
 assert.match(app,/state\.phase==='EXPLORING'&&!paused\)\{camera=easeObserverCamera\(camera,target,dt\);\}/);
 assert.match(app,/if\(paused\)camera=structuredClone\(target\)/,'explicit pause still snaps only view, not ordinary time');
 assert.match(app,/if\(memorySession\|\|historySession\)\{lastTime=t;return;\}/,'recorded history isolates world animation');
 assert.match(app,/dispatch\(\{type:'world_view'\}\)/,'whole-world navigation preserved');
 assert.match(app,/const clock=observerClock\(new Date\(\)\.toISOString\(\)\)/,'shared Eastern clock remains');
 assert.match(app,/renderer\.render\(camera,animationTime,\{strength:light\.strength,storm:demo\|\|0,paused\}\)/,'independent water phase remains');
 assert.doesNotMatch(spatial,/fetch\(|publishObserver|writeWorldState|createPrincipalCharacter/);
 const orbit=cameraStep(defaultCamera(),{yaw:6*Math.PI});
 assert.ok(Math.abs(shortestCameraYawArc(orbit.yaw,defaultCamera().yaw))<1e-10);
});
