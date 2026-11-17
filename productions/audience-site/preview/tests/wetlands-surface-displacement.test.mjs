import test from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';

const bindings=[
  {id:'LOC-MUD-DOGS-SWAMP',anchor:[42,0,16],canonStatus:'PERMANENT_CANON',landmarks:['mud channels','raised ground']},
  {id:'LOC-TDS-WATERFALL-TEMPLE',anchor:[31,0,51],canonStatus:'PERMANENT_CANON',landmarks:['waterfall']},
  {id:'LOC-COUNTRY-CLUB-JACKSON',anchor:[57,0,24],canonStatus:'PERMANENT_CANON',landmarks:['water hazards']},
];
const create=()=>buildRegionalAssets(THREE,bindings,()=>2);

test('only Mud Dogs swamp and channel have a tessellated, unchanged-footprint water disk',()=>{
  const a=create(),wet=a.water.filter(w=>w.kind==='swamp'||w.kind==='channel');
  assert.deepEqual(wet.map(w=>w.kind),['swamp','channel']);
  for(const w of wet){
    const geo=w.mesh.geometry,vertices=geo.getAttribute('position'),uv=geo.getAttribute('uv');
    assert.equal(geo.name,'Candidate wetland water surface');
    assert.equal(vertices.count,385,'center + eight 48-segment concentric rings');
    assert.equal(geo.index.count,2160,'48 center wedges + 7*96 ring triangles');
    assert.equal(uv.count,vertices.count);
    assert.equal(w.mesh.rotation.x,-Math.PI/2);
    assert.equal(w.material.uniforms.uWetland.value,1);
    for(let i=0;i<vertices.count;i++){
      assert.ok(Math.hypot(vertices.getX(i),vertices.getY(i))<=1.000001,'not beyond inherited unit ellipse');
      assert.equal(vertices.getZ(i),0,'local surface lies on unchanged source pool plane');
    }
    for(let i=1+7*48;i<vertices.count;i++){
      assert.ok(Math.abs(Math.hypot(vertices.getX(i),vertices.getY(i))-1)<.000001,'outer perimeter unchanged');
    }
    const index=geo.index.array;for(const k of [0,144,300]){
      const i=index[k],j=index[k+1],n=index[k+2];
      const cross=(vertices.getX(j)-vertices.getX(i))*(vertices.getY(n)-vertices.getY(i))-
        (vertices.getY(j)-vertices.getY(i))*(vertices.getX(n)-vertices.getX(i));
      assert.ok(cross>0,'water disk front-facing triangle winding');
    }
  }
  const [swamp,channel]=wet;
  assert.deepEqual(swamp.mesh.position.toArray(),[0,.12,0]);
  assert.deepEqual(swamp.mesh.scale.toArray(),[10.5,8.2,1]);
  assert.deepEqual(channel.mesh.position.toArray(),[-6,.14,7]);
  assert.deepEqual(channel.mesh.scale.toArray(),[4.2,4.5,1]);
  assert.equal(a.water.find(w=>w.kind==='pond').mesh.geometry.type,'CircleGeometry');
  assert.ok(a.water.filter(w=>['river','pool'].includes(w.kind)).every(w=>w.mesh.geometry.type==='CircleGeometry'));
  a.dispose();
});

test('vertex movement follows the existing environment clock and leaves bank/perimeter stationary',()=>{
  const a=create(),w=a.water.find(x=>x.kind==='swamp'),shader=w.material.vertexShader;
  assert.match(shader,/if\(uWetland>\.5\)/,'surface displacement isolated to wetland');
  assert.match(shader,/p\.z\+=crest\*\.018\*shoreHold/,'perpendicular movement of wetland water vertices');
  assert.match(shader,/shoreHold=1\.-smoothstep\(\.65,\.96,length/,'perimeter falloff');
  assert.match(shader,/uTime\*1\.16/,'continuously evolving temporal phase');
  assert.doesNotMatch(shader,/storm|weather/i,'vertex motion does not depend on weather');
  a.tick(5,{storm:0});assert.equal(w.material.uniforms.uTime.value,5);
  a.tick(17,{storm:0,paused:true});assert.equal(w.material.uniforms.uTime.value,5);
  a.tick(17,{storm:0});assert.equal(w.material.uniforms.uTime.value,17);
  a.dispose();
});

test('candidate geometry does not mutate source Atlas, water rules, or world/history authorities',()=>{
  const before=JSON.stringify(bindings),a=create();
  assert.deepEqual(a.locations.map(l=>l.id),bindings.map(l=>l.id));
  assert.equal(a.locations[0].group.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
  assert.equal(a.worldMutationAllowed,false);assert.deepEqual(a.principalCharacters,[]);
  assert.equal(JSON.stringify(bindings),before);
  assert.equal(a.water.filter(w=>['swamp','channel'].includes(w.kind)).length,2);
  assert.ok(a.water.filter(w=>!['swamp','channel'].includes(w.kind)).every(w=>w.material.uniforms.uWetland?.value!==1));
  assert.ok(a.water.some(w=>w.kind==='waterfall')&&a.water.some(w=>w.kind==='pond'));
  a.dispose();
});
