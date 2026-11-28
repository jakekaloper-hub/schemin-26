import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {projectAtlas} from '../../src/observer-world.mjs';
import {spatialBindings} from '../spatial.mjs';
import {buildAtlasSiteAssets} from '../atlas-site-assets.mjs';

const source=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const bindings=spatialBindings({locations:projectAtlas(source.locations)});
const original=JSON.stringify(bindings);
const build=()=>buildAtlasSiteAssets(THREE,bindings,()=>4);
function mappedMaterials(a){
 const materials=new Set();
 a.root.traverse(o=>{if(o.isMesh&&o.material?.map)materials.add(o.material);});
 return [...materials];
}
const pixel=(map,x,y)=>map.image.data[(y*64+x)*4];

test('existing 20 non-Wetlands candidates share deterministic, coherent, periodic stone and wood reflectance',()=>{
 const a=build(),b=build();
 try{
  assert.equal(a.locations.length,20);
  const materials=mappedMaterials(a);
  const stone=materials.find(m=>m.color.getHexString()==='c3bda5')?.map;
  const wood=materials.find(m=>m.color.getHexString()==='785738')?.map;
  assert.ok(stone&&wood&&stone!==wood,'original mapped stone and wood materials are present');
  const maps=[...new Set(materials.map(m=>m.map))];
  assert.deepEqual(new Set(maps),new Set([stone,wood]),'no per-mesh albedo allocations');
  for(const t of maps){
   assert.equal(t.image.width,64);assert.equal(t.image.height,64);
   assert.equal(t.image.data.length,64*64*4);
   assert.equal(t.wrapS,THREE.RepeatWrapping);assert.equal(t.wrapT,THREE.RepeatWrapping);
   assert.equal(t.colorSpace,THREE.SRGBColorSpace);
   const d=t.image.data;
   for(let i=0;i<d.length;i+=4){
    assert.equal(d[i],d[i+1]);assert.equal(d[i],d[i+2]);
    assert.equal(d[i+3],255);
   }
  }
  assert.ok(pixel(stone,8,8)-pixel(stone,0,8)>50,'first course mortar contrasts with coherent stone face');
  assert.ok(pixel(stone,0,24)-pixel(stone,16,24)>35,'second course has staggered joints');
  let horizontal=0,vertical=0,edge=0,count=0;
  for(let y=2;y<62;y++)for(let x=2;x<62;x++){
   horizontal+=Math.abs(pixel(wood,x+1,y)-pixel(wood,x,y));
   vertical+=Math.abs(pixel(wood,x,y+1)-pixel(wood,x,y));count++;
  }
  for(let y=0;y<64;y++)edge+=Math.abs(pixel(wood,63,y)-pixel(wood,0,y));
  assert.ok(horizontal>vertical*2.5,'wood fibres run longitudinally rather than isotropic pixel noise');
  assert.ok(edge/64<16,'repeat boundary has no discontinuous bright edge');
  const other=mappedMaterials(b);
  const otherStone=other.find(m=>m.color.getHexString()==='c3bda5')?.map;
  const otherWood=other.find(m=>m.color.getHexString()==='785738')?.map;
  assert.deepEqual(stone.image.data,otherStone.image.data);
  assert.deepEqual(wood.image.data,otherWood.image.data);
  assert.equal(JSON.stringify(bindings),original);
 }finally{a.dispose();b.dispose();}
});

test('refined albedo preserves source anchors, coupled tangent normals and independent ordinary water clock',()=>{
 const a=build();
 try{
  const normals=[...new Set(mappedMaterials(a).map(m=>m.normalMap))];
  assert.equal(normals.length,2,'the same two shared albedo-derived tangent normal maps remain');
  assert.ok(normals.every(t=>t.colorSpace===THREE.NoColorSpace));
  assert.deepEqual(a.locations.map(l=>l.id).length,20);
  for(const l of a.locations){
   const src=bindings.find(b=>b.id===l.id);
   assert.ok(src);assert.equal(l.group.position.x,src.anchor[0]);
   assert.equal(l.group.position.z,src.anchor[2]);
   assert.equal(l.group.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
  }
  a.tick(2,{storm:0,globalCalm:true});
  assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===2));
  a.tick(5,{storm:0,globalCalm:true});
  assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===5));
  a.tick(10,{paused:true,globalCalm:true});
  assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===5));
  assert.equal(a.worldMutationAllowed,false);
  assert.equal(a.weatherMutationAllowed,false);
  assert.deepEqual(a.principalCharacters,[]);
  assert.equal(JSON.stringify(bindings),original);
 }finally{a.dispose();}
});
