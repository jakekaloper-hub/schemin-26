import test from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';

const bindings=[
  {id:'LOC-MUD-DOGS-SWAMP',anchor:[42,0,16],canonStatus:'PERMANENT_CANON'},
  {id:'LOC-TDS-WATERFALL-TEMPLE',anchor:[32,0,29],canonStatus:'PERMANENT_CANON'},
  {id:'LOC-COUNTRY-CLUB-JACKSON',anchor:[57,0,24],canonStatus:'PERMANENT_CANON'},
];
const build=()=>buildRegionalAssets(THREE,bindings,()=>2);
const stems=a=>a.locations.find(p=>p.id==='LOC-MUD-DOGS-SWAMP').group.getObjectByName('Candidate Mud Dogs waterline stems');

test('the exact 26 inherited waterline stations retain original cylinder topology, dimensions and source authority',()=>{
 const snapshot=JSON.stringify(bindings),a=build(),o=stems(a);
 assert.ok(o?.isMesh&&o.material.isShaderMaterial);
 assert.equal(o.userData.stems,26);
 assert.equal(o.userData.rootStationsPreserved,true);
 assert.equal(o.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
 assert.deepEqual(o.userData.sourceEnvironment,['mud channels','cypress-like wetlands']);
 assert.deepEqual(o.userData.routeIds,[]);assert.deepEqual(o.userData.principalCharacters,[]);
 assert.equal(o.userData.navigable,false);assert.equal(o.userData.drawBudgetDelta,1);
 const reference=new THREE.CylinderGeometry(.04,.06,.55,4);
 const perStem=reference.getAttribute('position').count,perFaces=reference.getIndex().count;
 const p=o.geometry.getAttribute('position'),s=o.geometry.getAttribute('aSway');
 assert.equal(p.count,perStem*26);assert.equal(s.count,p.count);
 assert.equal(o.geometry.getAttribute('normal').count,p.count);
 assert.equal(o.geometry.getIndex().count,perFaces*26);
 const phases=new Set();
 for(let i=0;i<26;i++){
  const angle=i*2.399,r=6.8+Math.sin(i)*.8,x=Math.cos(angle)*r,z=Math.sin(angle)*r,h=.55+(i%3)*.15;
  const first=i*perStem,phase=s.getX(first);phases.add(phase.toFixed(5));
  assert.ok(Math.abs(phase-i*2.399)<.0001);
  let basePoints=0,tipPoints=0;
  for(let j=0;j<perStem;j++){
   const k=first+j,w=s.getY(k),px=p.getX(k),py=p.getY(k),pz=p.getZ(k);
   assert.ok([w,px,py,pz].every(Number.isFinite));
   assert.ok(Math.hypot(px-x,pz-z)<=.06001,'preserve the original 0.04/0.06 cylinder radii');
   assert.ok(py>=.1-.00001&&py<=.1+h+.00001,'preserve original stem heights');
   assert.ok(w>=0&&w<=1);
   assert.ok(Math.abs(w-(py-.1)/h)<.00002,'root-to-tip weights match original geometry');
   if(w<.0001)basePoints++;
   if(w>.9999)tipPoints++;
  }
  assert.ok(basePoints>0&&tipPoints>0);
 }
 assert.equal(phases.size,26,'each stem retains an independent phase');
 for(const loc of a.locations.filter(x=>x.id!=='LOC-MUD-DOGS-SWAMP'))
  assert.equal(loc.group.getObjectByName('Candidate Mud Dogs waterline stems'),undefined);
 assert.equal(JSON.stringify(bindings),snapshot);
 assert.equal(a.worldMutationAllowed,false);assert.deepEqual(a.principalCharacters,[]);
 reference.dispose();a.dispose();
});

test('rooted GPU sway is finite, in the inherited water ellipse, bounded and culling-safe at multiple times',()=>{
 const a=build(),o=stems(a),m=o.material,p=o.geometry.getAttribute('position'),s=o.geometry.getAttribute('aSway');
 assert.equal(o.userData.illustrativeMaxTipDisplacement,.091);
 assert.equal(o.userData.ambientClock,'ORDINARY_ENVIRONMENT');
 assert.equal(m.transparent,false);assert.equal(m.depthWrite,true);
 assert.equal(o.castShadow,false);
 assert.match(m.vertexShader,/rooted=aSway\.y\*aSway\.y/);
 assert.match(m.vertexShader,/p\.x\+=bend\*rooted/);
 assert.match(m.vertexShader,/p\.z\+=bend\*rooted\*\.58/);
 assert.doesNotMatch(m.vertexShader,/uStorm|uRain|uWeather|uWindSpeed/);
 const unpadded=o.geometry.clone();unpadded.computeBoundingSphere();
 assert.ok(Math.abs(o.geometry.boundingSphere.radius-unpadded.boundingSphere.radius-.10)<.00001);
 unpadded.dispose();
 let distinctMotion=false;
 for(const t of [0,1.25,8,60])for(let j=0;j<p.count;j++){
  const phase=s.getX(j),w=s.getY(j);
  const bend=.060*Math.sin(t*.65+phase)+.018*Math.sin(t*1.17+phase*1.33);
  const dx=bend*w*w,dz=dx*.58;
  assert.ok(Number.isFinite(dx)&&Number.isFinite(dz));
  assert.ok(Math.hypot(dx,dz)<.091,'motion stays inside documented culling envelope');
  assert.ok(Math.hypot((p.getX(j)+dx)/10.5,(p.getZ(j)+dz)/8.2)<1,
    'no stem crosses the original water footprint');
  if(w===0)assert.ok(dx===0&&dz===0,'root vertices remain fixed');
  if(w>0.99&&Math.abs(dx)>.005)distinctMotion=true;
 }
 assert.ok(distinctMotion,'upper stems must actually sway');
 a.dispose();
});

test('one animated draw follows ordinary clock through synthetic calm, freezes on explicit pause, and disposes once',()=>{
 const a=build(),o=stems(a),m=o.material,geo=o.geometry;
 assert.equal(a.root.getObjectsByProperty('name','Candidate Mud Dogs waterline stems').length,1);
 assert.equal(o.userData.drawBudgetDelta,1);
 const water=a.water.find(w=>w.kind==='swamp');
 a.tick(1,{storm:0});
 assert.equal(m.uniforms.uTime.value,1);assert.equal(water.material.uniforms.uTime.value,1);
 a.tick(5,{storm:0});
 assert.equal(m.uniforms.uTime.value,5);assert.equal(water.material.uniforms.uTime.value,5);
 a.tick(19,{paused:true,storm:0});
 assert.equal(m.uniforms.uTime.value,5);assert.equal(water.material.uniforms.uTime.value,5);
 let disposedMaterials=0,disposedGeometry=0;
 m.addEventListener('dispose',()=>disposedMaterials++);
 geo.addEventListener('dispose',()=>disposedGeometry++);
 a.dispose();a.dispose();
 assert.equal(disposedMaterials,1);assert.equal(disposedGeometry,1);
});
