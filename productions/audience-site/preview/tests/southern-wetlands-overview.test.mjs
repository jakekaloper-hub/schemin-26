import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {atlasToScene,regionOverviewCamera} from '../spatial.mjs';

const source=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const ids=['LOC-MUD-DOGS-SWAMP','LOC-COUNTRY-CLUB-JACKSON','LOC-TDS-WATERFALL-TEMPLE'];
const bindings=source.locations.map(p=>({id:p.id,zoneId:p.physical_zone_id,anchor:atlasToScene(p.abstract_position),visible:true,visited:false}));
const original=JSON.stringify(source),boundOriginal=JSON.stringify(bindings);
const dot=(a,b)=>a.reduce((sum,v,i)=>sum+v*b[i],0);
function checkFrustum(aspect){
 const c=regionOverviewCamera(bindings,'REG-SOUTHERN-WETLANDS',aspect);
 const expected=bindings.filter(p=>p.zoneId==='REG-SOUTHERN-WETLANDS');
 assert.deepEqual(expected.map(p=>p.id).sort(),[...ids].sort());
 const fit=Math.max(1,1.25/aspect),d=c.distance*(c.distance>100?fit:Math.min(fit,1.25));
 const half=Math.tan(41.25*Math.PI/360),r=[Math.cos(c.yaw),0,-Math.sin(c.yaw)];
 const u=[-Math.sin(c.yaw)*Math.sin(c.pitch),Math.cos(c.pitch),-Math.cos(c.yaw)*Math.sin(c.pitch)];
 const dir=[Math.sin(c.yaw)*Math.cos(c.pitch),Math.sin(c.pitch),Math.cos(c.yaw)*Math.cos(c.pitch)];
 for(const p of expected)for(const dx of [-8,8])for(const dz of [-8,8])for(const y of [0,12]){
  const offset=[p.anchor[0]+dx-c.target[0],y-c.target[1],p.anchor[2]+dz-c.target[2]];
  const depth=d-dot(offset,dir);
  assert.ok(depth>0,'source site remains in front of camera: '+p.id);
  assert.ok(Math.abs(dot(offset,r))<depth*half*aspect,'source site and bounded model fit horizontally: '+p.id);
  assert.ok(Math.abs(dot(offset,u))<depth*half,'source site and bounded model fit vertically: '+p.id);
 }
 assert.deepEqual(c.target,[-11,4,55]);
 assert.ok(c.distance>=12&&c.distance<=280);
 return c;
}
test('Source-defined Southern Wetlands overview fills landscape more closely than old 105-unit magic number',()=>{
 const c=checkFrustum(1440/813);
 assert.ok(c.distance<105&&c.distance>65);
 assert.equal(bindings.length,23);
 assert.ok(bindings.every(p=>p.visible&&!p.visited));
 assert.equal(JSON.stringify(source),original);assert.equal(JSON.stringify(bindings),boundOriginal);
});
test('Portrait and tablet fit preserve all three original site envelopes using the real responsive camera rule',()=>{
 for(const aspect of [390/844,4/3,1])checkFrustum(aspect);
 assert.equal(JSON.stringify(source),original);
});
test('Regional camera rejects nonexistent, damaged or extreme views without creating geography',()=>{
 assert.throws(()=>regionOverviewCamera(bindings,'REG-NOT-REAL'),/UNKNOWN_REGION/);
 assert.throws(()=>regionOverviewCamera(bindings,'REG-SOUTHERN-WETLANDS',0),/INVALID_REGIONAL_VIEW/);
 assert.throws(()=>regionOverviewCamera([{zoneId:'REG-SOUTHERN-WETLANDS',anchor:[1,NaN,3]}],'REG-SOUTHERN-WETLANDS'),/INVALID_REGIONAL_ANCHOR/);
 const changed=bindings.map(p=>({...p,visited:true,visible:false}));
 assert.deepEqual(regionOverviewCamera(changed,'REG-SOUTHERN-WETLANDS',1440/813),regionOverviewCamera(bindings,'REG-SOUTHERN-WETLANDS',1440/813));
 assert.equal(JSON.stringify(bindings),boundOriginal);
});
test('Existing observer regional button consumes source camera and returns from inspection to world ownership',()=>{
 const host=readFileSync(new URL('../app.mjs',import.meta.url),'utf8');
 const handler=host.match(/\$\('#wetlandsView'\)\.onclick=\(\)=>\{[\s\S]*?\n\};/);
 assert.ok(handler,'Source-bound overview control must remain wired');
 assert.match(handler[0],/regionOverviewCamera\(bindings,'REG-SOUTHERN-WETLANDS',canvas\.clientWidth\/Math\.max\(1,canvas\.clientHeight\)\)/);
 assert.match(handler[0],/dispatch\(\{type:'world_view'\}\);selected=null/);
 assert.match(handler[0],/if\(fromInspector\).*\.focus\(\{preventScroll:true\}\)/);
 assert.doesNotMatch(handler[0],/fetch\(|publicationAuthorized|weather|location\.reload/);
});
