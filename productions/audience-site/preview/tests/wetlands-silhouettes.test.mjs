import test from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';

const bindings=[
  {id:'LOC-TDS-WATERFALL-TEMPLE',anchor:[32,0,29],canonStatus:'PERMANENT_CANON'},
  {id:'LOC-MUD-DOGS-SWAMP',anchor:[42,0,16],canonStatus:'PERMANENT_CANON'},
  {id:'LOC-COUNTRY-CLUB-JACKSON',anchor:[57,0,24],canonStatus:'PERMANENT_CANON'},
];
const build=(items=bindings)=>buildRegionalAssets(THREE,items,()=>2);
const findSwamp=(assets)=>assets.locations.find(p=>p.id==='LOC-MUD-DOGS-SWAMP').group;

test('illustrative wetland bank has a layered irregular transition entirely outside the original swamp water ellipse',()=>{
  const assets=build();
  const bank=findSwamp(assets).getObjectByName('Candidate wetland shoreline transition');
  assert.ok(bank?.geometry?.isBufferGeometry,'a bank mesh must be present');
  assert.equal(bank.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
  assert.ok(bank.geometry.index.count>=200,'bank must have authored continuous triangulation');
  const positions=bank.geometry.attributes.position;
  assert.ok(positions.count>=150);
  for(let i=0;i<positions.count;i++){
    const normalized=Math.hypot(positions.getX(i)/10.5,positions.getZ(i)/8.2);
    assert.ok(normalized>=1.005&&normalized<=1.28,`bank edge crossed water or expanded beyond candidate (${normalized})`);
    assert.ok(Number.isFinite(positions.getY(i)));
  }
  assert.ok(bank.geometry.attributes.color,'multi-tone transitions rather than a flat ring');
  assets.dispose();
});

test('wetland trees have distinct clustered crowns and grounded root buttresses, without changing other places',()=>{
  const assets=build();
  const swamp=findSwamp(assets);
  const trees=swamp.children.filter(o=>Number.isInteger(o.userData?.wetlandStand));
  const stands=new Set(trees.map(o=>o.userData.wetlandStand));
  assert.equal(stands.size,14);
  const crowns=new Set();
  for(const stand of stands){
    const lobes=trees.filter(o=>o.userData.wetlandStand===stand&&o.userData.wetlandPart==='canopy-lobe');
    const roots=trees.filter(o=>o.userData.wetlandStand===stand&&o.userData.wetlandPart==='buttress-root');
    assert.ok(lobes.length>=3,'nonuniform crown layering');
    assert.ok(roots.length>=3,'root flares grounded at wetland');
    crowns.add(lobes.map(x=>x.scale.y.toFixed(2)).join(','));
  }
  assert.ok(crowns.size>=2,'not every tree should repeat one identical silhouette');
  for(const place of assets.locations.filter(x=>x.id!=='LOC-MUD-DOGS-SWAMP')){
    assert.equal(place.group.getObjectByName('Candidate wetland shoreline transition'),undefined);
    assert.equal(place.group.children.filter(o=>Number.isInteger(o.userData?.wetlandStand)).length,0);
  }
  assets.dispose();
});

test('silhouettes remain visual-only while water advances in calm and stops on pause',()=>{
  const before=JSON.stringify(bindings);
  const assets=build();
  assert.equal(assets.worldMutationAllowed,false);
  assert.deepEqual(assets.principalCharacters,[]);
  assert.deepEqual(assets.locations.map(x=>x.id),bindings.map(x=>x.id));
  assert.ok(assets.locations.every(x=>x.group.userData.visualAuthority==='CANDIDATE_NOT_APPROVED'));
  const w=assets.water.find(x=>x.kind==='swamp');
  assets.tick(3,{storm:0});assert.equal(w.material.uniforms.uTime.value,3);
  assets.tick(7,{storm:0});assert.equal(w.material.uniforms.uTime.value,7);
  assets.tick(9,{storm:0,paused:true});assert.equal(w.material.uniforms.uTime.value,7);
  assert.equal(JSON.stringify(bindings),before);
  assets.dispose();
});
