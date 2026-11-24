import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
const m=JSON.parse(readFileSync(new URL('../evidence/gpu-all-place-history-sweep-20261124/manifest.json',import.meta.url)));
test('physical history sweep is source-pinned and unpublished',()=>{
 assert.equal(m.sourceRevision,'7f040d13d82bfa75c885f374f15072a3edab993d');
 assert.equal(m.stateAsOf,'end_of_week_3_2026');
 assert.match(m.observerSha256,/^[a-f0-9]{64}$/);
 assert.equal(m.renderer,'three-webgl2');
 assert.match(m.gpu,/Apple M3 Pro/);
 assert.equal(m.status,'CANDIDATE_NOT_APPROVED');
 assert.equal(m.publicationAuthorized,false);
 assert.equal(m.sourceUnchanged,true);
 assert.equal(m.weatherStatus,'GLOBAL_CALM');
 assert.equal(m.ordinaryWaterAdvanced,true);
 assert.equal(m.explicitPause,true);
 for(const k of ['browserExceptions','consoleErrors','externalRequests'])assert.equal(m[k],0);
});
test('all 23 locations are visited, without fabricating history for the 16 missing records',()=>{
 assert.equal(m.places.length,23);
 assert.equal(new Set(m.places.map(p=>p.placeId)).size,23);
 const recorded=m.places.filter(p=>p.historyAvailable);
 assert.deepEqual(recorded.map(p=>[p.placeId,p.sourceEventIds]),[
  ['LOC-COUNTRY-CLUB-JACKSON',['EVT-W3-COUNTRY-CLUB-CHILI']],
  ['LOC-LLC-BOARDROOM',['EVT-W2-LLC-INTRUSION']],
  ['LOC-BRIDGE-MOUNTAIN-LAKE',['EVT-W3-BRIDGE']],
  ['LOC-DK-MUD-HILL',['EVT-W3-MIRE-HILL']],
  ['LOC-RED-SLOB-ALPINE-ROUTE',['EVT-W3-ALPINE-WAGER']],
  ['LOC-SOUTHERN-SPEEDWAY',['EVT-W3-SPEEDWAY']],
  ['LOC-LLC-STORM-CITY',['EVT-W3-LLC-STORM']]
 ]);
 const missing=m.places.filter(p=>!p.historyAvailable);
 assert.equal(missing.length,16);
 for(const p of missing){
  assert.deepEqual(p.sourceEventIds,[]);
  assert.equal(p.cameraBefore,undefined);
  assert.equal(p.waterFrozen,undefined);
 }
 for(const id of ['LOC-MUD-DOGS-SWAMP','LOC-TDS-WATERFALL-TEMPLE'])assert.ok(missing.some(p=>p.placeId===id));
});
test('all seven recorded history journeys retain camera and resume ordinary water',()=>{
 for(const p of m.places.filter(p=>p.historyAvailable)){
  assert.equal(p.readOnly,true);
  assert.ok(p.waterFrozen>=p.waterBefore&&p.waterBefore>0);
  assert.equal(p.waterHeld,p.waterFrozen);
  assert.ok(p.waterResumed>p.waterHeld);
  const b=[...p.cameraBefore.target,p.cameraBefore.distance,p.cameraBefore.yaw,p.cameraBefore.pitch];
  const a=[...p.cameraAfter.target,p.cameraAfter.distance,p.cameraAfter.yaw,p.cameraAfter.pitch];
  const tolerances=[.002,.002,.002,.002,.00002,.00002];
  assert.equal(a.length,6);assert.equal(b.length,6);
  for(let i=0;i<6;i++)assert.ok(Number.isFinite(a[i])&&Number.isFinite(b[i])&&Math.abs(a[i]-b[i])<=tolerances[i],p.placeId);
 }
});
