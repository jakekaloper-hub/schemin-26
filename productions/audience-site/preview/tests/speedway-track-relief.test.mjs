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
const id='LOC-SOUTHERN-SPEEDWAY',name='Rutted oval race course · candidate';
const site=a=>a.locations.find(x=>x.id===id);
const track=a=>site(a)?.group.children.find(x=>x.name===name);

test('only the source-recorded Southern Speedway receives one authored gravel/rut surface',()=>{
 const upstream=source.locations.find(x=>x.id===id);
 assert.deepEqual(upstream.persistent_landmarks,['oval/race course','grandstand']);
 const a=build(),s=site(a),course=track(a);
 assert.ok(s&&course);assert.equal(a.locations.length,20);
 assert.equal(s.group.children.filter(x=>x.name===name).length,1);
 assert.ok(s.group.children.some(x=>x.name==='Grandstand tier'),'grandstand preserved');
 assert.deepEqual(s.sourceLandmarks,upstream.persistent_landmarks);
 assert.equal(course.userData.sourceLandmark,'oval/race course');
 assert.equal(s.group.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
 for(const other of a.locations.filter(x=>x.id!==id))assert.equal(other.group.children.filter(x=>x.name===name).length,0,other.id);
 assert.equal(a.worldMutationAllowed,false);assert.equal(a.weatherMutationAllowed,false);
 assert.deepEqual(a.principalCharacters,[]);assert.equal(JSON.stringify(bindings),before);
 a.dispose();
});

test('single static ring retains footprint and level rim with bounded physical ruts and granular shading',()=>{
 const a=build(),course=track(a),geo=course.geometry,pos=geo.getAttribute('position'),color=geo.getAttribute('color');
 assert.equal(geo.type,'RingGeometry');
 assert.equal(geo.parameters.innerRadius,4.2);assert.equal(geo.parameters.outerRadius,6.7);
 assert.equal(geo.parameters.thetaSegments,144);assert.equal(geo.parameters.phiSegments,20);
 assert.ok(pos.count>=3000&&pos.count<=3100);
 assert.ok(geo.index.count<=17500);
 assert.equal(color.count,pos.count);assert.ok(geo.getAttribute('normal'));
 assert.equal(course.material.vertexColors,true);
 assert.equal(course.material.roughness,.98);
 assert.deepEqual(course.position.toArray(),[0,.35,0]);
 assert.equal(course.rotation.x,-Math.PI/2);assert.equal(course.scale.y,.64);
 let min=Infinity,max=-Infinity,edgeCount=0,low=Infinity,high=-Infinity;
 let rutSum=0,rutCount=0,shoulderSum=0,shoulderCount=0;
 for(let i=0;i<pos.count;i++){
  const x=pos.getX(i),y=pos.getY(i),z=pos.getZ(i),r=Math.hypot(x,y);
  assert.ok([x,y,z,r].every(Number.isFinite));
  assert.ok(r>=4.19999&&r<=6.70001,'original course footprint');
  assert.ok(z>=-.09&&z<=.012,'bounded sub-surface granular relief');
  if(Math.abs(r-4.2)<.00001||Math.abs(r-6.7)<.00001){edgeCount++;assert.ok(Math.abs(z)<.00001,'unmoved inner/outer rim');}
  if(r>4.95&&r<5.12||r>5.75&&r<5.9){rutSum+=z;rutCount++;}
  if(r>5.35&&r<5.52){shoulderSum+=z;shoulderCount++;}
  const channels=[color.getX(i),color.getY(i),color.getZ(i)];
  assert.ok(channels.every(v=>Number.isFinite(v)&&v>0&&v<1));
  const lum=channels.reduce((p,q)=>p+q,0)/3;
  low=Math.min(low,lum);high=Math.max(high,lum);
  min=Math.min(min,z);max=Math.max(max,z);
 }
 assert.ok(edgeCount>200);
 assert.ok(rutCount>200&&shoulderCount>100);
 assert.ok(rutSum/rutCount<shoulderSum/shoulderCount-.015,'two visibly incised wheel lanes');
 assert.ok(min<-.035&&max>.004,'physical grooves and gravel micro-relief');
 assert.ok(high-low>.055,'localized wear color variation');
 assert.equal(JSON.stringify(bindings),before);a.dispose();
});

test('static candidate track is weather-independent; inherited animated water still obeys calm and explicit pause',()=>{
 const a=build(),course=track(a),original=course.geometry.getAttribute('position').array.slice();
 a.tick(1.1,{globalCalm:true,storm:0});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===1.1));
 a.tick(3.4,{globalCalm:true,storm:0});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===3.4));
 a.tick(6.7,{paused:true,storm:3});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===3.4));
 assert.deepEqual(course.geometry.getAttribute('position').array,original);
 let count=0;course.material.addEventListener('dispose',()=>count++);
 a.dispose();a.dispose();assert.equal(count,1);
 assert.equal(JSON.stringify(bindings),before);
});
