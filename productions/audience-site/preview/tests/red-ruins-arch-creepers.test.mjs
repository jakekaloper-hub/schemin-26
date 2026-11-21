import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {projectAtlas} from '../../src/observer-world.mjs';
import {spatialBindings} from '../spatial.mjs';
import {buildAtlasSiteAssets} from '../atlas-site-assets.mjs';

const source=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const bindings=spatialBindings({locations:projectAtlas(source.locations)});
const snapshot=JSON.stringify(bindings);
const id='LOC-RED-RUINS',name='Red Ruins arch creepers · candidate';
const build=()=>buildAtlasSiteAssets(THREE,bindings,()=>4);
function get(a){
 const site=a.locations.find(l=>l.id===id);
 assert.ok(site);
 const creepers=site.group.children.filter(o=>o.name===name);
 assert.equal(creepers.length,1,'one batched local foliage surface');
 return {site,creepers:creepers[0]};
}
test('source-bound Red Leopard Ruins alone gains arch vegetation without losing original landmarks',()=>{
 const record=source.locations.find(l=>l.id===id);
 assert.equal(record.canon_status,'PERMANENT_CANON');
 assert.deepEqual(record.persistent_landmarks,['jungle ruins','predator banners']);
 const a=build(),{site,creepers}=get(a);
 assert.equal(a.locations.length,20);
 assert.equal(site.group.userData.canonStatus,record.canon_status);
 assert.deepEqual(site.sourceLandmarks,record.persistent_landmarks);
 assert.equal(site.group.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
 assert.equal(creepers.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
 assert.equal(creepers.userData.sourceLandmark,'jungle ruins');
 assert.equal(site.group.children.filter(o=>o.name==='Masonry arch candidate').length,3);
 assert.equal(site.group.children.filter(o=>o.name==='Moving predator banner · candidate cloth').length,2);
 assert.equal(site.group.children.filter(o=>o.name==='Banner mast').length,2);
 for(const other of a.locations.filter(l=>l.id!==id))
  assert.equal(other.group.children.filter(o=>o.name===name).length,0,other.id);
 assert.equal(a.worldMutationAllowed,false);assert.equal(a.weatherMutationAllowed,false);
 assert.deepEqual(a.principalCharacters,[]);assert.equal(JSON.stringify(bindings),snapshot);a.dispose();
});
test('twelve arch-rooted creeper strands carry finite deterministic physical leaves inside terrace bounds',()=>{
 const a=build(),o=get(a).creepers,b=build(),copy=get(b).creepers;
 const geo=o.geometry,pos=geo.getAttribute('position'),color=geo.getAttribute('color');
 assert.equal(geo.type,'BufferGeometry');
 assert.equal(pos.count,408,'12 strands: eight pairs, six leaf triangles each');
 assert.equal(color.count,408);assert.equal(geo.index.count,720);
 assert.equal(o.material.isMeshStandardMaterial,true);
 assert.equal(o.material.vertexColors,true);
 assert.equal(o.material.side,THREE.DoubleSide);
 assert.equal(o.material.roughness,.97);assert.equal(o.material.metalness,0);
 assert.equal(o.castShadow,false);assert.equal(o.receiveShadow,false);
 assert.deepEqual(o.position.toArray(),[0,0,0]);
 let minX=Infinity,maxX=-Infinity,minY=Infinity,maxY=-Infinity,minZ=Infinity,maxZ=-Infinity;
 for(let i=0;i<pos.count;i++){
  const x=pos.getX(i),y=pos.getY(i),z=pos.getZ(i);
  assert.ok([x,y,z].every(Number.isFinite));
  minX=Math.min(minX,x);maxX=Math.max(maxX,x);
  minY=Math.min(minY,y);maxY=Math.max(maxY,y);
  minZ=Math.min(minZ,z);maxZ=Math.max(maxZ,z);
  for(const c of [color.getX(i),color.getY(i),color.getZ(i)])
   assert.ok(Number.isFinite(c)&&c>.08&&c<.5,'bounded living-green foliage');
 }
 assert.ok(minX>=-5.8&&maxX<=5.8,'existing ruined terrace lateral envelope');
 assert.ok(minY>=3.15&&maxY<=4.40001,'arch-local hanging, not new towers');
 assert.ok(minZ>=-2.08&&maxZ<=-1.85,'stone arch front-facing drape');
 assert.deepEqual(Array.from(pos.array),Array.from(copy.geometry.getAttribute('position').array));
 assert.deepEqual(Array.from(color.array),Array.from(copy.geometry.getAttribute('color').array));
 assert.deepEqual(Array.from(geo.index.array),Array.from(copy.geometry.index.array));
 assert.equal(JSON.stringify(bindings),snapshot);a.dispose();b.dispose();
});
test('candidate greenery changes no storm/water state; ordinary motion persists through calm and pause; cleanup once',()=>{
 const a=build(),o=get(a).creepers,unchangedPositions=o.geometry.getAttribute('position').array.slice();
 assert.equal(a.water.length,4);
 a.tick(2.5,{globalCalm:true,storm:0});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===2.5));
 a.tick(4.75,{globalCalm:true,storm:0});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===4.75));
 a.tick(9.1,{globalCalm:true,storm:6,paused:true});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===4.75));
 assert.deepEqual(o.geometry.getAttribute('position').array,unchangedPositions);
 assert.equal(JSON.stringify(bindings),snapshot);
 let geometries=0,materials=0;
 o.geometry.addEventListener('dispose',()=>geometries++);
 o.material.addEventListener('dispose',()=>materials++);
 a.dispose();a.dispose();a.tick(11);
 assert.equal(geometries,1);assert.equal(materials,1);
 assert.equal(a.water[0].material.uniforms.uTime.value,4.75);
});
