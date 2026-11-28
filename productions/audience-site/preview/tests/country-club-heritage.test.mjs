import test from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';

const bindings=[
  {id:'LOC-TDS-WATERFALL-TEMPLE',anchor:[32,0,29],canonStatus:'PERMANENT_CANON'},
  {id:'LOC-MUD-DOGS-SWAMP',anchor:[42,0,16],canonStatus:'PERMANENT_CANON'},
  {id:'LOC-COUNTRY-CLUB-JACKSON',anchor:[57,0,24],canonStatus:'PERMANENT_CANON'},
];
const build=(places=bindings)=>buildRegionalAssets(THREE,places,()=>2);
const club=a=>a.locations.find(p=>p.id==='LOC-COUNTRY-CLUB-JACKSON').group;

test('only Country Club candidate has locally bounded arched masonry pond crossing, not an Atlas route',()=>{
  const a=build(),g=club(a),bridge=g.getObjectByName('Candidate Week 9 pond-side stone arch');
  assert.ok(bridge?.isGroup,'historical-reference bridge should be an authored group');
  assert.equal(bridge.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
  assert.equal(bridge.userData.historicalReference,'W09-COUNTRY-CLUB-FOLIOS-05-08');
  assert.deepEqual(bridge.userData.routeIds,[]);
  assert.equal(bridge.userData.navigable,false);
  const arches=bridge.children.filter(o=>o.userData?.bridgePart==='stone-arch');
  assert.equal(arches.length,2,'parallel arched masonry facades');
  for(const arch of arches)assert.ok(arch.geometry?.type==='ExtrudeGeometry');
  const bounds=new THREE.Box3().setFromObject(bridge);
  assert.ok(bounds.min.x>=3&&bounds.max.x<=11);
  assert.ok(bounds.min.z>=2&&bounds.max.z<=10);
  assert.ok(bounds.min.y>=-.05&&bounds.max.y<=4.2);
  assert.equal(a.locations.filter(p=>p.group.getObjectByName(bridge.name)).length,1);
  a.dispose();
});

test('club has warm, varied canopy silhouettes sourced as Week 9 visual texture only',()=>{
  const a=build(),g=club(a);
  const trees=g.children.filter(o=>o.userData?.estateTreePart==='crown');
  const trunks=g.children.filter(o=>o.userData?.estateTreePart==='trunk');
  const treeIds=new Set(trees.map(o=>o.userData.estateTree));
  assert.ok(treeIds.size>=7,'autumn grove is a spatial layer, not a lone prop');
  assert.equal(trunks.length,treeIds.size,'tree trunks remain grounded');
  assert.ok(trees.length>=treeIds.size*3,'each canopy has layered individual lobes');
  const tones=new Set(trees.map(o=>o.material.color.getHexString()));
  assert.ok(tones.size>=3,'historical fall foliage has multiple warm tints');
  assert.ok([...tones].some(c=>c[0]==='b'||c[0]==='c'||c[0]==='d'));
  for(const place of a.locations.filter(p=>p.id!=='LOC-COUNTRY-CLUB-JACKSON')){
    assert.equal(place.group.children.some(o=>o.userData?.estateTreePart),false);
    assert.equal(place.group.getObjectByName('Candidate Week 9 pond-side stone arch'),undefined);
  }
  a.dispose();
});

test('visual reference changes neither identity nor uncertain cleanup state and ordinary water still moves through calm',()=>{
  const before=JSON.stringify(bindings),a=build();
  assert.deepEqual(a.locations.map(p=>p.id),bindings.map(p=>p.id));
  assert.equal(a.worldMutationAllowed,false);
  assert.deepEqual(a.principalCharacters,[]);
  for(const place of a.locations)assert.equal(place.group.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
  assert.equal(club(a).userData.stateResolution,'UNRESOLVED_NOT_CURRENT_STATE');
  const pond=a.water.find(w=>w.kind==='pond');
  assert.ok(pond,'existing water hazard preserved');
  a.tick(2,{storm:0});assert.equal(pond.material.uniforms.uTime.value,2);
  a.tick(4,{storm:0});assert.equal(pond.material.uniforms.uTime.value,4);
  a.tick(8,{storm:0,paused:true});assert.equal(pond.material.uniforms.uTime.value,4);
  assert.equal(JSON.stringify(bindings),before);
  a.dispose();
});
