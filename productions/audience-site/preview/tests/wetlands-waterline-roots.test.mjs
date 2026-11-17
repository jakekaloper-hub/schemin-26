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
const swamp=(assets)=>assets.locations.find(x=>x.id==='LOC-MUD-DOGS-SWAMP').group;
const roots=(assets)=>swamp(assets).getObjectByName('Candidate wetland waterline root knees');

test('existing Mud Dogs tree stands have bounded, genuinely tapered waterline root candidates',()=>{
 const assets=build(),knees=roots(assets);
 assert.ok(knees?.isMesh);
 assert.equal(knees.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
 assert.equal(knees.userData.sourceStands,14);
 assert.ok(knees.userData.rootCount>=45&&knees.userData.rootCount<=70);
 assert.deepEqual(knees.userData.routeIds,[]);assert.equal(knees.userData.navigable,false);
 const p=knees.geometry.getAttribute('position'),uv=knees.geometry.getAttribute('uv');
 const normals=knees.geometry.getAttribute('normal');
 assert.equal(p.count,knees.userData.rootCount*21);
 assert.equal(uv.count,p.count);assert.equal(normals.count,p.count);
 assert.equal(knees.geometry.getIndex().count,knees.userData.rootCount*84);
 const heights=new Set();
 for(let i=0;i<p.count;i++){
  const r=Math.hypot(p.getX(i)/10.5,p.getZ(i)/8.2);
  assert.ok(r<=.94,'waterline roots must not cross the existing swamp footprint');
  assert.ok(p.getY(i)>=.10&&p.getY(i)<.85);
  assert.ok(Number.isFinite(normals.getX(i))&&Number.isFinite(normals.getY(i))&&Number.isFinite(normals.getZ(i)));
  if(i%21===14)heights.add(p.getY(i).toFixed(3));
 }
 assert.ok(heights.size>=5,'roots should vary in height instead of repeating one cone');
 assert.equal(knees.geometry.attributes.color,undefined,'existing trunk material uses its source texture/UV');
 assets.dispose();
});

test('the root mesh reuses existing textured tree-trunk material and static batching',()=>{
 const assets=build(),wetland=swamp(assets),k=roots(assets);
 const stand=wetland.children.find(x=>x.userData.wetlandPart==='trunk');
 assert.ok(stand&&k);assert.equal(k.material,stand.material);
 const before=JSON.stringify(bindings);
 const result=batchStaticGeometry(THREE,wetland);
 assert.ok(result.geometries.length>0);
 const compiled=wetland.children.filter(x=>x.userData?.compiledFrom?.includes('Candidate wetland waterline root knees'));
 assert.equal(compiled.length,1,'root projections should enter existing opaque static group');
 assert.equal(compiled[0].material,stand.material);
 assert.ok(compiled[0].geometry.attributes.uv,'textured batch needs UVs');
 assert.equal(JSON.stringify(bindings),before);
 for(const g of result.geometries)g.dispose();assets.dispose();
});

test('candidate root geometry is location-only and cannot freeze calm water or write world state',()=>{
 const before=JSON.stringify(bindings),assets=build();
 assert.equal(assets.root.getObjectsByProperty('name','Candidate wetland waterline root knees').length,1);
 for(const l of assets.locations.filter(x=>x.id!=='LOC-MUD-DOGS-SWAMP'))
  assert.equal(l.group.getObjectByName('Candidate wetland waterline root knees'),undefined);
 assert.equal(assets.worldMutationAllowed,false);
 assert.deepEqual(assets.principalCharacters,[]);
 assert.deepEqual(assets.locations.map(l=>l.id),bindings.map(l=>l.id));
 const w=assets.water.find(x=>x.kind==='swamp');
 assets.tick(2,{storm:0});assert.equal(w.material.uniforms.uTime.value,2);
 assets.tick(5,{storm:0});assert.equal(w.material.uniforms.uTime.value,5);
 assets.tick(9,{storm:0,paused:true});assert.equal(w.material.uniforms.uTime.value,5);
 assert.equal(JSON.stringify(bindings),before);
 assets.dispose();
});
