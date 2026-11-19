import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {projectAtlas} from '../../src/observer-world.mjs';
import {spatialBindings} from '../spatial.mjs';
import {buildAtlasSiteAssets} from '../atlas-site-assets.mjs';

const src=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const bindings=spatialBindings({locations:projectAtlas(src.locations)}),original=JSON.stringify(bindings);
const id='LOC-CHINS-ROAD-COMMONS',build=()=>buildAtlasSiteAssets(THREE,bindings,()=>4);
const site=a=>a.locations.find(l=>l.id===id);
const wheels=a=>site(a)?.group.children.find(c=>c.name==='Road Commons caravan open-spoke wheels · candidate');
const centers=[[2.3,.275,1],[3.9,.275,1],[2.3,.275,4],[3.9,.275,4]];

test('Road Commons remains source-exact, with both chassis and three original landmarks',()=>{
 const record=src.locations.find(l=>l.id===id),a=build(),s=site(a),w=wheels(a);
 assert.equal(record.canon_status,'PROVISIONAL_CANON');
 assert.deepEqual(record.persistent_landmarks,['roadside hall','BBQ yard','caravan court']);
 assert.ok(s&&w);assert.equal(a.locations.length,20);assert.equal(a.water.length,4);
 assert.deepEqual(s.sourceLandmarks,record.persistent_landmarks);
 assert.equal(s.group.userData.locationId,id);assert.equal(s.group.userData.canonStatus,record.canon_status);
 assert.equal(s.group.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
 for(const key of record.persistent_landmarks)assert.ok(s.group.children.some(c=>c.userData.sourceLandmark===key));
 const chassis=s.group.children.filter(c=>c.geometry?.type==='BoxGeometry'&&c.geometry.parameters.width===2.4&&c.geometry.parameters.height===.4&&c.geometry.parameters.depth===1.1);
 assert.deepEqual(chassis.map(c=>c.position.toArray()),[[3.1,.8,1],[3.1,.8,4]]);
 assert.equal(s.group.children.filter(c=>c.name===w.name).length,1);
 assert.equal(s.group.children.filter(c=>c.geometry?.type==='CylinderGeometry'&&c.geometry.parameters.radiusTop===.4&&c.geometry.parameters.height===.15).length,0);
 for(const other of a.locations.filter(l=>l.id!==id))assert.ok(!other.group.children.some(c=>c.name===w.name));
 assert.equal(a.worldMutationAllowed,false);assert.equal(a.weatherMutationAllowed,false);
 assert.deepEqual(a.principalCharacters,[]);assert.equal(JSON.stringify(bindings),original);
 a.dispose();
});
test('four open physical rims/hubs and eight spokes per wheel are bounded and deterministic',()=>{
 const a=build(),o=wheels(a),g=o.geometry,p=g.getAttribute('position'),c=g.getAttribute('color');
 assert.equal(g.type,'BufferGeometry');assert.ok(g.getIndex().count>0);
 assert.equal(o.material.vertexColors,true);assert.equal(o.material.side,THREE.DoubleSide);
 assert.deepEqual(o.position.toArray(),[0,0,0]);assert.deepEqual(o.userData.wheelCenters,centers);
 assert.equal(o.userData.wheelCount,4);assert.equal(o.userData.spokesPerWheel,8);
 assert.equal(p.count,c.count);assert.ok(p.count<2100&&g.getIndex().count/3<2200);
 const hits=new Set();let lo=Infinity,hi=-Infinity;
 for(let i=0;i<p.count;i++){
  const v=[p.getX(i),p.getY(i),p.getZ(i)];assert.ok(v.every(Number.isFinite));
  const ci=centers.findIndex(([x,y,z])=>Math.abs(v[0]-x)<=.07501&&Math.hypot(v[1]-y,v[2]-z)<=.40001);
  assert.notEqual(ci,-1);hits.add(ci);
  for(const q of [c.getX(i),c.getY(i),c.getZ(i)]){
   assert.ok(Number.isFinite(q)&&q>.07&&q<.43);lo=Math.min(lo,q);hi=Math.max(hi,q);
  }
 }
 assert.deepEqual([...hits].sort(),[0,1,2,3]);assert.ok(hi-lo>.13);
 for(const [x,y,z] of centers){
  let rim=0,hub=0,spoke=0,gap=0;
  for(let i=0;i<p.count;i++){
   if(Math.abs(p.getX(i)-x)>.07501)continue;
   const dy=p.getY(i)-y,dz=p.getZ(i)-z,r=Math.hypot(dy,dz);
   if(r>.288&&r<.401)rim++;if(r<.117)hub++;
   if(r>.14&&r<.27){
    spoke++;
    const angle=Math.atan2(dy,dz),delta=Math.atan2(Math.sin(angle-Math.PI/8),Math.cos(angle-Math.PI/8));
    if(Math.abs(delta)<.08)gap++;
   }
  }
  assert.ok(rim>0&&hub>0&&spoke>0);assert.equal(gap,0,'spoke openings remain clear');
 }
 const b=build(),g2=wheels(b).geometry;
 assert.deepEqual(p.array,g2.getAttribute('position').array);
 assert.deepEqual(c.array,g2.getAttribute('color').array);
 assert.deepEqual(g.getIndex().array,g2.getIndex().array);
 a.dispose();b.dispose();
});
test('El Niño calm retains ordinary water, pause freezes, and local resources clean once',()=>{
 const a=build(),o=wheels(a),saved=o.geometry.getAttribute('position').array.slice();
 a.tick(1.7,{globalCalm:true,storm:0});assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===1.7));
 a.tick(4.3,{globalCalm:true,storm:0});assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===4.3));
 a.tick(8,{paused:true,globalCalm:true,storm:7});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===4.3));
 assert.deepEqual(o.geometry.getAttribute('position').array,saved);
 let geos=0,mats=0;
 o.geometry.addEventListener('dispose',()=>geos++);o.material.addEventListener('dispose',()=>mats++);
 a.dispose();a.dispose();a.tick(10);
 assert.equal(geos,1);assert.equal(mats,1);assert.equal(JSON.stringify(bindings),original);
});
