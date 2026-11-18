import test from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';
import {batchStaticGeometry} from '../three-world.mjs';

const bindings=[
  {id:'LOC-MUD-DOGS-SWAMP',anchor:[42,0,16],canonStatus:'PERMANENT_CANON'},
  {id:'LOC-TDS-WATERFALL-TEMPLE',anchor:[32,0,29],canonStatus:'PERMANENT_CANON'},
  {id:'LOC-COUNTRY-CLUB-JACKSON',anchor:[57,0,24],canonStatus:'PERMANENT_CANON'},
];
const build=()=>buildRegionalAssets(THREE,bindings,()=>2);
const swamp=assets=>assets.locations.find(p=>p.id==='LOC-MUD-DOGS-SWAMP').group;
const fringe=assets=>swamp(assets).getObjectByName('Candidate Mud Dogs canopy fringe');

test('hanging fringe uses only the 14 existing tree crowns and stays airborne at bounded geometry cost',()=>{
  const assets=build(),g=swamp(assets),f=fringe(assets);
  assert.ok(f?.isMesh);assert.equal(f.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
  assert.equal(f.userData.sourceStands,14);assert.equal(f.userData.strands,56);
  assert.equal(f.userData.triangles,1344);
  assert.deepEqual(f.userData.routeIds,[]);assert.equal(f.userData.navigable,false);
  const p=f.geometry.getAttribute('position'),uv=f.geometry.getAttribute('uv'),normals=f.geometry.getAttribute('normal');
  assert.equal(p.count,1792);assert.equal(uv.count,p.count);assert.equal(normals.count,p.count);
  assert.equal(f.geometry.getIndex().count,4032);
  const trunks=g.children.filter(x=>x.userData.wetlandPart==='trunk');
  assert.equal(trunks.length,14);
  for(let j=0;j<p.count;j++){
    const x=p.getX(j),y=p.getY(j),z=p.getZ(j);
    assert.ok(Number.isFinite(x)&&Number.isFinite(y)&&Number.isFinite(z));
    assert.ok(y>1.55&&y<6.5,'fringe must hang from existing canopy, not create ground or crossing');
    assert.ok(trunks.some(t=>Math.hypot(x-t.position.x,z-t.position.z)<1.5),
      'every strand must remain close to an existing illustrated stand');
    assert.ok([normals.getX(j),normals.getY(j),normals.getZ(j)].every(Number.isFinite));
  }
  assert.ok(new Set(trunks.map(x=>x.userData.wetlandStand)).size===14);
  assets.dispose();
});

test('moving fringe uses one explicitly budgeted GPU draw while existing opaque foliage still batches',()=>{
  const assets=build(),g=swamp(assets),f=fringe(assets);
  const hanging=g.children.find(x=>x.userData.wetlandPart==='hanging-vegetation');
  assert.ok(hanging&&hanging.material!==f.material);
  assert.ok(f.material.isShaderMaterial);
  assert.equal(f.userData.drawBudgetDelta,1);
  assert.equal(f.castShadow,false);
  assert.equal(f.receiveShadow,false);
  const staticMossBefore=g.children.filter(x=>x.isMesh&&x.material===hanging.material).length;
  assert.ok(staticMossBefore>1);
  const {geometries}=batchStaticGeometry(THREE,g);
  assert.ok(g.children.includes(f),'animated geometry must remain independently GPU-driven');
  assert.equal(g.children.filter(x=>x===f).length,1,'only one extra scenic draw is retained');
  assert.equal(g.children.filter(x=>x.isMesh&&x.material===hanging.material).length,1,
    'existing static opaque foliage should remain a single batch');
  for(const other of assets.locations.filter(x=>x.id!=='LOC-MUD-DOGS-SWAMP'))
    assert.equal(other.group.getObjectByName('Candidate Mud Dogs canopy fringe'),undefined);
  for(const geo of geometries)geo.dispose();assets.dispose();
});

test('canopy addition preserves source bounds, spectator authority, ordinary calm-water motion and pause',()=>{
  const before=JSON.stringify(bindings),assets=build();
  assert.deepEqual(assets.locations.map(x=>x.id),bindings.map(x=>x.id));
  assert.equal(assets.worldMutationAllowed,false);assert.deepEqual(assets.principalCharacters,[]);
  for(const place of assets.locations)assert.equal(place.group.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
  const w=assets.water.find(x=>x.kind==='swamp');
  assets.tick(3,{storm:0});assert.equal(w.material.uniforms.uTime.value,3);
  assets.tick(6,{storm:0});assert.equal(w.material.uniforms.uTime.value,6);
  assets.tick(9,{storm:0,paused:true});assert.equal(w.material.uniforms.uTime.value,6);
  assert.equal(JSON.stringify(bindings),before);
  assets.dispose();
});
