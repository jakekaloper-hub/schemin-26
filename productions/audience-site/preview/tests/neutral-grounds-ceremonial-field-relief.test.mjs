import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {projectAtlas} from '../../src/observer-world.mjs';
import {spatialBindings} from '../spatial.mjs';
import {buildAtlasSiteAssets} from '../atlas-site-assets.mjs';

const source=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const bindings=spatialBindings({locations:projectAtlas(source.locations)}),before=JSON.stringify(bindings);
const id='LOC-COMPACT-NEUTRAL-GROUNDS',name='Open ceremonial field';
const build=()=>buildAtlasSiteAssets(THREE,bindings,()=>4);
const site=a=>a.locations.find(l=>l.id===id);
const field=a=>site(a)?.group.children.find(c=>c.name===name);

test('Neutral Grounds field retains source identity, landmarks, pavilion, roads and site isolation',()=>{
 const record=source.locations.find(l=>l.id===id),a=build(),s=site(a),o=field(a);
 assert.equal(record.canon_status,'PROVISIONAL_CANON');
 assert.deepEqual(record.persistent_landmarks,['open ceremonial field','arbiter pavilion','arrival roads']);
 assert.ok(s&&o);assert.equal(a.locations.length,20);assert.equal(a.water.length,4);
 assert.equal(s.group.userData.locationId,id);
 assert.equal(s.group.userData.canonStatus,record.canon_status);
 assert.deepEqual(s.sourceLandmarks,record.persistent_landmarks);
 assert.equal(s.group.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
 for(const landmark of record.persistent_landmarks)
  assert.ok(s.group.children.some(c=>c.userData.sourceLandmark===landmark));
 assert.ok(s.group.children.some(c=>c.name==='Pavilion floor'));
 assert.ok(s.group.children.some(c=>c.name==='Arrival-road presentation'));
 assert.equal(s.group.children.filter(c=>c.name===name).length,1);
 assert.ok(a.locations.filter(l=>l.id!==id).every(l=>!l.group.children.some(c=>c.name===name)));
 assert.equal(a.worldMutationAllowed,false);assert.equal(a.weatherMutationAllowed,false);
 assert.deepEqual(a.principalCharacters,[]);assert.equal(JSON.stringify(bindings),before);
 a.dispose();
});

test('one deterministic indexed mesh has physical gently recessed green relief inside old cylinder envelope',()=>{
 const a=build(),o=field(a),g=o.geometry,p=g.getAttribute('position'),c=g.getAttribute('color');
 assert.equal(g.type,'BufferGeometry');assert.ok(g.getIndex());
 assert.equal(g.getIndex().count,2592);assert.equal(p.count,530);
 assert.equal(c.count,p.count);assert.equal(o.material.vertexColors,true);
 assert.deepEqual(o.position.toArray(),[0,.125,0]);
 assert.equal(o.userData.originalTopRadius,6.5);
 assert.equal(o.userData.originalBottomRadius,6.8);
 assert.equal(o.userData.originalHeight,.25);
 assert.equal(o.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
 const topCount=1+8*48,topRimStart=1+7*48;
 let minTop=.125,depthCount=0,low=Infinity,high=-Infinity;
 for(let i=0;i<p.count;i++){
  const x=p.getX(i),y=p.getY(i),z=p.getZ(i),r=Math.hypot(x,z);
  assert.ok([x,y,z].every(Number.isFinite));
  assert.ok(r<=6.800001&&y>=-.125001&&y<=.125001,'original radius/height envelope');
  for(const v of [c.getX(i),c.getY(i),c.getZ(i)]){
   assert.ok(Number.isFinite(v)&&v>=0&&v<=1);
   low=Math.min(low,v);high=Math.max(high,v);
  }
  if(i<topCount){
   minTop=Math.min(minTop,y);
   if(y<.105)depthCount++;
   assert.ok(r<=6.500001&&y>=.067999);
  }
  if(i>=topRimStart&&i<topCount)
   assert.ok(Math.abs(y-.125)<.000001,'top perimeter stays in original plane');
 }
 assert.ok(minTop<.105&&depthCount>20,'interior has physical recessed relief');
 assert.ok(high-low>.22,'different vertex colors, not a flat tinted disc');
 assert.equal(o.geometry.type,'BufferGeometry');assert.notEqual(o.geometry.type,'CylinderGeometry');
 const b=build(),other=field(b).geometry;
 assert.deepEqual(p.array,other.getAttribute('position').array);
 assert.deepEqual(c.array,other.getAttribute('color').array);
 assert.deepEqual(g.getIndex().array,other.getIndex().array);
 a.dispose();b.dispose();
});

test('El Niño global calm leaves existing water moving; explicit pause and owned disposal remain correct',()=>{
 const a=build(),o=field(a),initial=o.geometry.getAttribute('position').array.slice();
 a.tick(2.1,{globalCalm:true,storm:0});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===2.1));
 a.tick(5.3,{globalCalm:true,storm:0});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===5.3));
 a.tick(8,{globalCalm:true,storm:9,paused:true});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===5.3));
 assert.deepEqual(o.geometry.getAttribute('position').array,initial);
 let geometryDisposed=0,materialDisposed=0;
 o.geometry.addEventListener('dispose',()=>geometryDisposed++);
 o.material.addEventListener('dispose',()=>materialDisposed++);
 a.dispose();a.dispose();a.tick(11);
 assert.equal(geometryDisposed,1);assert.equal(materialDisposed,1);
 assert.equal(JSON.stringify(bindings),before);
});
