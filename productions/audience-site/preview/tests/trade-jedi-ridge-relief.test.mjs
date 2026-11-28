import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {projectAtlas} from '../../src/observer-world.mjs';
import {spatialBindings} from '../spatial.mjs';
import {buildAtlasSiteAssets} from '../atlas-site-assets.mjs';

const source=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const bindings=spatialBindings({locations:projectAtlas(source.locations)}),before=JSON.stringify(bindings);
const build=()=>buildAtlasSiteAssets(THREE,bindings,()=>4);
const id='LOC-TRADE-JEDI-MOUNTAIN-BASE',name='Trade Jedi high ridge · candidate';
const site=a=>a.locations.find(x=>x.id===id);
const ridge=a=>site(a)?.group.children.find(x=>x.name===name);

test('source-bound Trade Jedi high ridge alone is replaced without new landmarks',()=>{
 const upstream=source.locations.find(x=>x.id===id);
 assert.deepEqual(upstream.persistent_landmarks,['high ridge','war-room overlook']);
 const a=build(),s=site(a),r=ridge(a);
 assert.ok(s&&r);assert.equal(a.locations.length,20);
 assert.equal(s.group.children.filter(x=>x.name===name).length,1);
 assert.equal(r.userData.sourceLandmark,'high ridge');
 assert.ok(s.group.children.some(x=>x.userData.sourceLandmark==='war-room overlook'));
 assert.ok(s.group.children.some(x=>x.name==='Approach step'));
 for(const other of a.locations.filter(x=>x.id!==id))assert.equal(other.group.children.filter(x=>x.name===name).length,0,other.id);
 assert.deepEqual(s.sourceLandmarks,upstream.persistent_landmarks);
 assert.equal(s.group.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
 assert.equal(a.worldMutationAllowed,false);assert.equal(a.weatherMutationAllowed,false);
 assert.deepEqual(a.principalCharacters,[]);assert.equal(JSON.stringify(bindings),before);
 a.dispose();
});

test('single static ridge retains exact footprint transform and bounded colored stone relief',()=>{
 const a=build(),r=ridge(a),geo=r.geometry,pos=geo.getAttribute('position'),colors=geo.getAttribute('color');
 assert.equal(geo.type,'IcosahedronGeometry');
 assert.ok(pos.count>=500&&pos.count<=1300);
 assert.equal(pos.count,colors.count);assert.ok(geo.getAttribute('normal'));
 assert.deepEqual(r.position.toArray(),[0,1.3,0]);
 assert.deepEqual(r.scale.toArray(),[7,2.5,5.5]);
 assert.deepEqual([r.rotation.x,r.rotation.y,r.rotation.z],[.13,.3,.07]);
 assert.equal(r.material.vertexColors,true);assert.equal(r.material.roughness,.98);
 let low=Infinity,high=-Infinity,radialMin=Infinity,radialMax=-Infinity;
 for(let i=0;i<pos.count;i++){
  const xyz=[pos.getX(i),pos.getY(i),pos.getZ(i)],rad=Math.hypot(...xyz);
  assert.ok(xyz.every(Number.isFinite));
  assert.ok(rad>=.975999&&rad<=1.024001);
  radialMin=Math.min(radialMin,rad);radialMax=Math.max(radialMax,rad);
  const rgb=[colors.getX(i),colors.getY(i),colors.getZ(i)];
  assert.ok(rgb.every(v=>Number.isFinite(v)&&v>.19&&v<.4));
  const light=rgb.reduce((p,v)=>p+v,0)/3;
  low=Math.min(low,light);high=Math.max(high,light);
 }
 assert.ok(radialMax-radialMin>.018);
 assert.ok(high-low>.02);
 assert.equal(JSON.stringify(bindings),before);a.dispose();
});

test('static stone preserves calm-weather ordinary water, explicit pause and exact disposal',()=>{
 const a=build(),r=ridge(a),original=r.geometry.getAttribute('position').array.slice();
 a.tick(1.1,{globalCalm:true,storm:0});
 assert.ok(a.water.length>=4&&a.water.every(w=>w.material.uniforms.uTime.value===1.1));
 a.tick(3.4,{globalCalm:true,storm:0});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===3.4));
 a.tick(6.7,{paused:true,storm:3});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===3.4));
 assert.deepEqual(r.geometry.getAttribute('position').array,original);
 let disposed=0;r.material.addEventListener('dispose',()=>disposed++);
 a.dispose();a.dispose();assert.equal(disposed,1);
 assert.equal(JSON.stringify(bindings),before);
});
