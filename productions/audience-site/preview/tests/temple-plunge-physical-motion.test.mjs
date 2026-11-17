import test from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';

const bindings=[
  {id:'LOC-TDS-WATERFALL-TEMPLE',anchor:[31,0,51],canonStatus:'PERMANENT_CANON',landmarks:['waterfall']},
  {id:'LOC-MUD-DOGS-SWAMP',anchor:[42,0,16],canonStatus:'PERMANENT_CANON',landmarks:['mud channels']},
  {id:'LOC-COUNTRY-CLUB-JACKSON',anchor:[57,0,24],canonStatus:'PERMANENT_CANON',landmarks:['water hazards']},
];
const build=()=>buildRegionalAssets(THREE,bindings,()=>2);
const displacement=(u,v,t)=>{
  const r=Math.hypot((u-.5)*2,(v-.5)*2);
  const x=Math.max(0,Math.min(1,(r-.64)/(.96-.64)));
  const hold=1-x*x*(3-2*x);
  return (.017*Math.sin(r*29-t*1.75+Math.sin(u*13)*.23)
    +.006*Math.sin((u*16-v*12)+t*.88))*hold;
};

test('Temple plunge retessellates the same receiving pool with its original 40-segment rim fixed',()=>{
  const before=JSON.stringify(bindings),a=build(),pool=a.water.find(w=>w.kind==='pool');
  assert.ok(pool);
  assert.equal(a.water.filter(w=>w.kind==='pool').length,1);
  assert.equal(pool.mesh.geometry.name,'Candidate Temple plunge pool surface');
  assert.deepEqual(pool.mesh.position.toArray(),[-5.8,.30,3]);
  assert.deepEqual(pool.mesh.scale.toArray(),[3.8,2.8,1]);
  assert.equal(pool.mesh.rotation.x,-Math.PI/2);
  const pos=pool.mesh.geometry.getAttribute('position'),uv=pool.mesh.geometry.getAttribute('uv');
  assert.equal(pos.count,321,'center plus eight existing-footprint 40-sided rings');
  assert.equal(uv.count,pos.count);
  assert.equal(pool.mesh.geometry.index.count,1800);
  for(let i=0;i<pos.count;i++){
    assert.ok(Number.isFinite(pos.getX(i))&&Number.isFinite(pos.getY(i)));
    assert.ok(Math.hypot(pos.getX(i),pos.getY(i))<=1.000001);
    assert.equal(pos.getZ(i),0);
  }
  for(let k=0;k<40;k++){
    const i=1+7*40+k,angle=k*2*Math.PI/40;
    assert.ok(Math.abs(pos.getX(i)-Math.cos(angle))<1e-6);
    assert.ok(Math.abs(pos.getY(i)-Math.sin(angle))<1e-6);
    assert.ok(Math.hypot(pos.getX(i),pos.getY(i))>.999999);
  }
  assert.equal(a.water.find(w=>w.kind==='pond').mesh.geometry.type,'CircleGeometry');
  assert.equal(a.water.find(w=>w.kind==='river').mesh.geometry.name,'Candidate Temple upstream river surface');
  assert.equal(a.water.find(w=>w.kind==='waterfall').mesh.geometry.type,'PlaneGeometry');
  assert.equal(a.locations[0].group.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
  assert.deepEqual(a.principalCharacters,[]);
  assert.equal(a.worldMutationAllowed,false);
  assert.equal(JSON.stringify(bindings),before);
  a.dispose();
});

test('plunge-only shader physically moves bounded interior vertices but never the waterline',()=>{
  const a=build(),pool=a.water.find(w=>w.kind==='pool');
  const shader=pool.material.vertexShader;
  assert.equal(pool.material.uniforms.uPlunge.value,1);
  assert.equal(pool.material.uniforms.uRiver.value,0);
  assert.equal(pool.material.uniforms.uWetland.value,0);
  assert.match(shader,/uniform float uPlunge;/);
  assert.match(shader,/if\(uPlunge>\.5\)/);
  assert.match(shader,/plungeHold=1\.-smoothstep\(\.64,\.96,plungeRadius\)/);
  assert.match(shader,/p\.z\+=\(\.017\*plungeWave\+\.006\*plungeCross\)\*plungeHold/);
  assert.doesNotMatch(shader,/\buStorm\b|\buWeather\b/i);
  for(const t of [0,1.8,24])for(const [u,v] of [[0,.5],[1,.5],[.5,0],[.5,1],[.25,.25],[.5,.5],[.36,.62]]){
    const d=displacement(u,v,t);
    assert.ok(Math.abs(d)<=.02300001,'bounded local vertical relief');
    if(u===0||u===1||v===0||v===1)assert.ok(Math.abs(d)<1e-12,'fixed original outer rim');
  }
  assert.ok(Math.abs(displacement(.36,.62,0)-displacement(.36,.62,1.8))>.001,'interior actually moves');
  for(const other of a.water.filter(w=>w.kind!=='pool')){
    assert.equal(other.material.uniforms.uPlunge?.value??0,0,'isolated from '+other.kind);
  }
  a.dispose();
});

test('physical plunge motion follows the shared environment clock through calm and freezes on pause',()=>{
  const before=JSON.stringify(bindings),a=build(),pool=a.water.find(w=>w.kind==='pool');
  a.tick(2,{storm:0});assert.equal(pool.material.uniforms.uTime.value,2);
  a.tick(11,{storm:0});assert.equal(pool.material.uniforms.uTime.value,11);
  a.tick(19,{storm:0,paused:true});assert.equal(pool.material.uniforms.uTime.value,11);
  a.tick(21,{storm:0});assert.equal(pool.material.uniforms.uTime.value,21);
  assert.equal(JSON.stringify(bindings),before);
  a.dispose();a.dispose();
});
