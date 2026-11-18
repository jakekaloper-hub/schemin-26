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
const fringe=a=>a.locations.find(x=>x.id==='LOC-MUD-DOGS-SWAMP').group.getObjectByName('Candidate Mud Dogs canopy fringe');

test('exact existing 56 strands gain phase and rooted tip weights, with original vertex and triangle topology',()=>{
  const original=JSON.stringify(bindings),a=build(),f=fringe(a);
  assert.ok(f&&f.material.isShaderMaterial);
  assert.equal(f.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
  assert.equal(f.userData.sourceStands,14);
  assert.equal(f.userData.strands,56);
  assert.equal(f.userData.triangles,1344);
  assert.deepEqual(f.userData.routeIds,[]);
  assert.deepEqual(f.userData.principalCharacters,[]);
  assert.equal(f.userData.navigable,false);
  assert.equal(f.userData.ambientClock,'ORDINARY_ENVIRONMENT');
  const p=f.geometry.getAttribute('position'),s=f.geometry.getAttribute('aSway');
  assert.equal(p.count,1792);assert.equal(s.count,p.count);
  assert.equal(f.geometry.getIndex().count,4032);
  const phases=new Set();
  for(let block=0;block<56;block++){
    const start=block*32;
    const phase=s.getX(start);phases.add(phase.toFixed(4));
    for(let cross=0;cross<4;cross++)for(let row=0;row<4;row++)for(let side=0;side<2;side++){
      const k=start+cross*8+row*2+side;
      assert.ok(Math.abs(s.getX(k)-phase)<1e-5);
      assert.ok(Math.abs(s.getY(k)-row/3)<1e-6);
      assert.ok([p.getX(k),p.getY(k),p.getZ(k)].every(Number.isFinite));
    }
  }
  assert.equal(phases.size,56,'each original hanging strand has its own ambient phase');
  assert.equal(JSON.stringify(bindings),original);
  a.dispose();
});

test('bounded GPU tip motion leaves crown attachment fixed and never alters topology or weather state',()=>{
  const a=build(),f=fringe(a),shader=f.material.vertexShader;
  assert.match(shader,/tipWeight=aSway\.y\*aSway\.y/);
  assert.match(shader,/p\.x\+=oscillation\*tipWeight/);
  assert.match(shader,/p\.z\+=oscillation\*tipWeight\*\.62/);
  assert.doesNotMatch(shader,/uStorm|uRain|uWeather|uWindSpeed/);
  assert.equal(f.userData.illustrativeMaxTipDisplacement,.19);
  const unpadded=f.geometry.clone();
  unpadded.computeBoundingSphere();
  assert.ok(Math.abs(f.geometry.boundingSphere.radius-unpadded.boundingSphere.radius-.22)<1e-5,
    'moving tips retain the bounded GPU-culling envelope around the original mesh');
  unpadded.dispose();
  const displace=(phase,weight,time)=>{
    const oscillation=.12*Math.sin(time*.62+phase)+.04*Math.sin(time*1.07+phase*1.57);
    return [oscillation*weight*weight,oscillation*weight*weight*.62];
  };
  for(const phase of [0,1.17,6.33,15.2])for(const time of [0,1.5,13,90])
    for(const w of [0,1/3,2/3,1]){
      const [x,z]=displace(phase,w,time);
      assert.ok(Number.isFinite(x)&&Number.isFinite(z));
      assert.ok(Math.hypot(x,z)<=.19);
      if(w===0)assert.deepEqual([x,z],[0,0],'crown attachments never move');
    }
  assert.ok(Math.abs(displace(1.17,1,0)[0]-displace(1.17,1,3)[0])>.01);
  assert.equal(a.worldMutationAllowed,false);
  assert.deepEqual(a.principalCharacters,[]);
  a.dispose();
});

test('independent clock advances animated strands and ordinary water in global calm, with explicit pause and disposal',()=>{
  const a=build(),f=fringe(a),m=f.material,swamp=a.water.find(w=>w.kind==='swamp');
  assert.ok(m.uniforms.uTime);
  assert.equal(m.uniforms.uFoliage.value.isColor,true);
  assert.equal(m.transparent,false);assert.equal(m.depthWrite,true);
  assert.equal(f.castShadow,false);
  a.tick(2,{storm:0});
  assert.equal(m.uniforms.uTime.value,2);assert.equal(swamp.material.uniforms.uTime.value,2);
  a.tick(7,{storm:0});
  assert.equal(m.uniforms.uTime.value,7);assert.equal(swamp.material.uniforms.uTime.value,7);
  a.tick(17,{storm:0,paused:true});
  assert.equal(m.uniforms.uTime.value,7);assert.equal(swamp.material.uniforms.uTime.value,7);
  let disposal=0;m.addEventListener('dispose',()=>disposal++);
  a.dispose();a.dispose();assert.equal(disposal,1);
  for(const other of a.locations.filter(p=>p.id!=='LOC-MUD-DOGS-SWAMP')){
    assert.equal(other.group.getObjectByName('Candidate Mud Dogs canopy fringe'),undefined);
  }
});
