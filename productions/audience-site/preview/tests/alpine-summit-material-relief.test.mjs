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
const id='LOC-RED-SLOB-ALPINE-ROUTE';
const stoneName='Alpine summit stone · candidate',snowName='Alpine summit snow · candidate';
const site=a=>a.locations.find(x=>x.id===id);
const part=(a,name)=>site(a)?.group.children.find(x=>x.name===name);

test('source Alpine Wager Route alone gains the two shaded static surfaces, not new landmarks',()=>{
 const upstream=source.locations.find(x=>x.id===id);
 assert.ok(upstream.persistent_landmarks.includes('summit'));
 assert.ok(upstream.persistent_landmarks.includes('base camp'));
 assert.ok(upstream.persistent_landmarks.includes('wager marker'));
 const a=build(),s=site(a);
 assert.ok(s);assert.equal(a.locations.length,20);
 assert.equal(s.group.children.filter(x=>[stoneName,snowName].includes(x.name)).length,2);
 for(const other of a.locations.filter(x=>x.id!==id))assert.equal(other.group.children.filter(x=>[stoneName,snowName].includes(x.name)).length,0,other.id);
 assert.equal(s.group.children.filter(x=>x.name==='Wager marker').length,1);
 assert.ok(s.group.children.some(x=>x.name==='Pitched roof candidate'),'base camp geometry retained');
 assert.deepEqual(s.sourceLandmarks,upstream.persistent_landmarks);
 assert.equal(s.group.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
 assert.equal(a.worldMutationAllowed,false);assert.equal(a.weatherMutationAllowed,false);
 assert.deepEqual(a.principalCharacters,[]);assert.equal(JSON.stringify(bindings),before);
 a.dispose();
});

test('alpine granite and snow surfaces have numeric bounded relief and differentiated vertex colors',()=>{
 const a=build(),stone=part(a,stoneName),snow=part(a,snowName);
 assert.ok(stone&&snow);
 assert.deepEqual(stone.position.toArray(),[0,1.4,-1.7]);
 assert.deepEqual(snow.position.toArray(),[.2,4.2,-1.8]);
 assert.deepEqual(stone.scale.toArray(),[5.5,4.1,4.1]);
 assert.deepEqual(snow.scale.toArray(),[3.8,.85,2.9]);
 let means=[];
 for(const o of [stone,snow]){
  const geo=o.geometry,pos=geo.getAttribute('position'),colors=geo.getAttribute('color');
  assert.equal(geo.type,'IcosahedronGeometry');
  assert.ok(pos.count>=500);
  assert.equal(pos.count,colors.count);
  assert.ok(geo.getAttribute('normal'));
  assert.equal(o.material.vertexColors,true);
  assert.equal(o.material.roughness,.96);
  assert.ok(o.material!== (o===stone?snow.material:stone.material),'each surface uses isolated material');
  let lo=Infinity,hi=-Infinity,light=0,dark=0;
  for(let i=0;i<pos.count;i++){
   const r=Math.hypot(pos.getX(i),pos.getY(i),pos.getZ(i));
   assert.ok(r>=.970999&&r<=1.029001,'2.9 percent maximum radial relief');
   const c=[colors.getX(i),colors.getY(i),colors.getZ(i)];
   assert.ok(c.every(x=>Number.isFinite(x)&&x>0&&x<1));
   const lum=(c[0]+c[1]+c[2])/3;
   lo=Math.min(lo,lum);hi=Math.max(hi,lum);light+=lum;dark+=1;
  }
  assert.ok(hi-lo>.04,'surface relief shading must vary');
  means.push(light/dark);
 }
 assert.ok(means[1]>means[0],'snow cap visibly brighter than stone');
 assert.equal(JSON.stringify(bindings),before);
 a.dispose();
});

test('static alpine relief is weather-independent; inherited water obeys ordinary time and pause',()=>{
 const a=build(),stone=part(a,stoneName),snow=part(a,snowName);
 const original=stone.geometry.getAttribute('position').array.slice();
 a.tick(1.1,{globalCalm:true,storm:0});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===1.1));
 a.tick(3.4,{globalCalm:true,storm:0});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===3.4));
 a.tick(6.7,{paused:true,storm:3});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===3.4));
 assert.deepEqual(stone.geometry.getAttribute('position').array,original);
 let disposed=0;for(const material of [stone.material,snow.material])material.addEventListener('dispose',()=>disposed++);
 a.dispose();a.dispose();assert.equal(disposed,2);
 assert.equal(JSON.stringify(bindings),before);
});
