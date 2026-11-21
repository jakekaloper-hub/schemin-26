import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {projectAtlas} from '../../src/observer-world.mjs';
import {spatialBindings} from '../spatial.mjs';
import {buildAtlasSiteAssets} from '../atlas-site-assets.mjs';

const source=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const bindings=spatialBindings({locations:projectAtlas(source.locations)}),before=JSON.stringify(bindings);
const id='LOC-STORM-BOWL',name='Weather-exposed venue';
const build=()=>buildAtlasSiteAssets(THREE,bindings,()=>4);
const site=a=>a.locations.find(l=>l.id===id);
const floor=a=>site(a)?.group.children.find(o=>o.name===name);

test('Storm Bowl venue remains source-exact with service counter and 17 existing seats',()=>{
 const record=source.locations.find(l=>l.id===id),a=build(),s=site(a),o=floor(a);
 assert.equal(record.canon_status,'PROVISIONAL_CANON');
 assert.deepEqual(record.persistent_landmarks,['weather-exposed venue','service counter']);
 assert.ok(s&&o);assert.equal(a.locations.length,20);assert.equal(a.water.length,4);
 assert.equal(s.group.userData.locationId,id);
 assert.deepEqual(s.sourceLandmarks,record.persistent_landmarks);
 assert.equal(s.group.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
 assert.ok(s.group.children.some(x=>x.userData.sourceLandmark==='weather-exposed venue'));
 assert.ok(s.group.children.some(x=>x.userData.sourceLandmark==='service counter'));
 assert.equal(s.group.children.filter(x=>x.name==='Broken-ring seating').length,17);
 assert.equal(s.group.children.filter(x=>x.name===name).length,1);
 assert.equal(s.group.children.filter(x=>x.name==='Pavilion floor').length,1);
 assert.ok(a.locations.filter(x=>x.id!==id).every(x=>!x.group.children.some(y=>y.name===name)));
 assert.equal(a.worldMutationAllowed,false);assert.equal(a.weatherMutationAllowed,false);
 assert.deepEqual(a.principalCharacters,[]);
 assert.equal(JSON.stringify(bindings),before);a.dispose();
});

test('one indexed concave sand mesh preserves original storm-venue cylinder envelope and fixed rim',()=>{
 const a=build(),b=build(),o=floor(a),g=o.geometry,p=g.getAttribute('position'),c=g.getAttribute('color');
 assert.equal(g.type,'BufferGeometry');assert.ok(g.getIndex());
 assert.equal(p.count,578);assert.equal(g.getIndex().count,3456);
 assert.equal(c.count,p.count);assert.equal(o.material.vertexColors,true);
 assert.equal(o.material.roughness,.99);
 assert.deepEqual(o.position.toArray(),[0,.225,0]);
 assert.equal(o.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
 assert.equal(o.userData.originalTopRadius,6.6);
 assert.equal(o.userData.originalBottomRadius,6.9);
 assert.equal(o.userData.originalHeight,.45);
 const topEnd=1+8*64,topRimStart=1+7*64;
 let minTop=Infinity,deep=0,low=Infinity,high=-Infinity;
 for(let i=0;i<p.count;i++){
  const x=p.getX(i),y=p.getY(i),z=p.getZ(i),r=Math.hypot(x,z);
  assert.ok([x,y,z].every(Number.isFinite));
  assert.ok(r<=6.90001&&y>=-.225001&&y<=.225001,'original cylinder bounds');
  for(const v of [c.getX(i),c.getY(i),c.getZ(i)]){
   assert.ok(Number.isFinite(v)&&v>=0&&v<=1);
   low=Math.min(low,v);high=Math.max(high,v);
  }
  if(i<topEnd){
   assert.ok(r<=6.60001&&y>=.065,'top stays within old outer radius and shallowness');
   minTop=Math.min(minTop,y);
   if(y<.15)deep++;
  }
  if(i>=topRimStart&&i<topEnd){
   assert.ok(Math.abs(r-6.6)<.00001,'original top rim radial extent');
   assert.ok(Math.abs(y-.225)<.000001,'rim remains at source-candidate presentation height');
  }
 }
 assert.ok(minTop<.13&&deep>45,'visible real concavity, not only material shading');
 assert.ok(high-low>.18,'deterministic varied mineral vertex shading');
 assert.deepEqual(p.array,floor(b).geometry.getAttribute('position').array);
 assert.deepEqual(c.array,floor(b).geometry.getAttribute('color').array);
 assert.deepEqual(g.getIndex().array,floor(b).geometry.getIndex().array);
 assert.equal(JSON.stringify(bindings),before);a.dispose();b.dispose();
});

test('El Niño global calm never freezes other-site water; paused clock and owned disposal are unchanged',()=>{
 const a=build(),o=floor(a),positions=o.geometry.getAttribute('position').array.slice();
 a.tick(1.3,{globalCalm:true,storm:0});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===1.3));
 a.tick(5.1,{globalCalm:true,storm:0});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===5.1));
 a.tick(8,{globalCalm:true,storm:9,paused:true});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===5.1));
 assert.deepEqual(o.geometry.getAttribute('position').array,positions);
 let geometryDisposals=0,materialDisposals=0;
 o.geometry.addEventListener('dispose',()=>geometryDisposals++);
 o.material.addEventListener('dispose',()=>materialDisposals++);
 a.dispose();a.dispose();a.tick(10);
 assert.equal(geometryDisposals,1);assert.equal(materialDisposals,1);
 assert.equal(JSON.stringify(bindings),before);
});
