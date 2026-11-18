import test from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';

const bindings=[
  {id:'LOC-COUNTRY-CLUB-JACKSON',anchor:[57,0,24],canonStatus:'PERMANENT_CANON',landmarks:['water hazards','clubhouse']},
  {id:'LOC-MUD-DOGS-SWAMP',anchor:[42,0,16],canonStatus:'PERMANENT_CANON',landmarks:['mud channels']},
  {id:'LOC-TDS-WATERFALL-TEMPLE',anchor:[32,0,29],canonStatus:'PERMANENT_CANON',landmarks:['waterfall']}
];
const build=()=>buildRegionalAssets(THREE,bindings,()=>2);
const smooth=(a,b,x)=>{const q=Math.max(0,Math.min(1,(x-a)/(b-a)));return q*q*(3-2*q);};
const offset=(u,v,t)=>{
  const x=(u-.5)*2,y=(v-.5)*2,r=Math.hypot(x,y);
  const hold=1-smooth(.66,.97,r);
  const a=Math.hypot((x+.19),(y-.08)*1.25);
  const b=Math.hypot((x-.25)*1.2,y+.18);
  return (.012*Math.sin(a*33-t*2.4)+.007*Math.sin(b*25-t*1.75))*hold;
};

test('existing Country Club pond has eight interior rings and exact original 40-segment fixed outer bank',()=>{
  const source=JSON.stringify(bindings),assets=build();
  const pond=assets.water.find(w=>w.kind==='pond');
  assert.ok(pond);
  assert.equal(assets.water.filter(w=>w.kind==='pond').length,1);
  assert.equal(pond.mesh.geometry.name,'Candidate Country Club pond surface');
  assert.deepEqual(pond.mesh.position.toArray(),[7,.06,6]);
  assert.deepEqual(pond.mesh.scale.toArray(),[3.8,2.3,1]);
  assert.equal(pond.mesh.rotation.x,-Math.PI/2);
  const pos=pond.mesh.geometry.getAttribute('position');
  const uv=pond.mesh.geometry.getAttribute('uv');
  assert.equal(pos.count,321);assert.equal(uv.count,321);
  assert.equal(pond.mesh.geometry.index.count,1800);
  for(let i=0;i<pos.count;i++){
    assert.ok(Math.hypot(pos.getX(i),pos.getY(i))<=1.000001);
    assert.equal(pos.getZ(i),0);
  }
  for(let k=0;k<40;k++){
    const i=1+7*40+k,theta=k*2*Math.PI/40;
    assert.ok(Math.abs(pos.getX(i)-Math.cos(theta))<.000001);
    assert.ok(Math.abs(pos.getY(i)-Math.sin(theta))<.000001);
    assert.ok(Math.hypot(pos.getX(i),pos.getY(i))>.999999);
  }
  assert.equal(assets.worldMutationAllowed,false);
  assert.deepEqual(assets.principalCharacters,[]);
  assert.equal(JSON.stringify(bindings),source);
  assets.dispose();
});

test('pond-only GPU water relief moves the inherited two concentric wavefronts, never the perimeter',()=>{
  const assets=build(),pond=assets.water.find(w=>w.kind==='pond');
  const shader=pond.material.vertexShader,frag=pond.material.fragmentShader;
  assert.equal(pond.material.uniforms.uPond.value,1);
  assert.equal(pond.material.uniforms.uFlow.value.length(),0,'no candidate pond current');
  assert.match(shader,/uniform float uPond;/);
  assert.match(shader,/if\(uPond>\.5\)/);
  assert.match(shader,/pondHold=1\.-smoothstep\(\.66,\.97,pondRadius\)/);
  assert.match(shader,/p\.z\+=\(\.012\*pondA\+\.007\*pondB\)\*pondHold/);
  assert.match(frag,/pondNormal=pondCrossSize>/);
  assert.match(frag,/pondLight=vec3\(\.08,\.12,\.10\)\*pondRelief\*bank/);
  assert.doesNotMatch(shader,/\buWeather\b|\buStorm\b/i);
  for(const t of [0,3,27]){
    for(const [u,v] of [[.5,.5],[.31,.62],[.7,.48],[0,.5],[.5,0],[1,.5],[.5,1]]){
      const d=offset(u,v,t);
      assert.ok(Math.abs(d)<=.01900001);
      if(u===0||u===1||v===0||v===1)assert.ok(Math.abs(d)<1e-12,'bank remains fixed');
    }
  }
  assert.ok(Math.abs(offset(.31,.62,0)-offset(.31,.62,3))>.001,'physical interior movement');
  for(const other of assets.water.filter(w=>w.kind!=='pond'))
    assert.equal(other.material.uniforms.uPond?.value??0,0,'no pond relief on '+other.kind);
  assets.dispose();
});

test('normal pond motion survives synthetic El Nino calm, freezes on explicit pause and does not modify source',()=>{
  const initial=JSON.stringify(bindings),assets=build(),pond=assets.water.find(w=>w.kind==='pond');
  assets.tick(2,{storm:0});assert.equal(pond.material.uniforms.uTime.value,2);
  assets.tick(11,{storm:0});assert.equal(pond.material.uniforms.uTime.value,11);
  assets.tick(20,{storm:0,paused:true});assert.equal(pond.material.uniforms.uTime.value,11);
  assets.tick(24,{storm:0});assert.equal(pond.material.uniforms.uTime.value,24);
  assert.equal(assets.locations.find(l=>l.id==='LOC-COUNTRY-CLUB-JACKSON').group.userData.stateResolution,'UNRESOLVED_NOT_CURRENT_STATE');
  assert.equal(JSON.stringify(bindings),initial);
  assets.dispose();assets.dispose();
});
