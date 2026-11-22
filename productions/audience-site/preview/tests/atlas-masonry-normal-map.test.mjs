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
function architecturalMaterials(a){
 const materials=new Set();
 a.root.traverse(o=>{if(o.isMesh&&o.material?.map)materials.add(o.material);});
 return [...materials];
}
function normals(a){
 return [...new Set(architecturalMaterials(a).map(m=>m.normalMap))];
}
test('existing stone and wood candidate surfaces share only two bounded, non-color tangent normal textures',()=>{
 const a=build(),materials=architecturalMaterials(a),maps=normals(a);
 assert.equal(a.locations.length,20);
 assert.ok(materials.length>=5);
 assert.equal(maps.length,2,'one stone and one wood normal map, not per-mesh allocations');
 for(const m of materials){
  assert.ok(m.normalMap,'mapped architecture must have directional micro-normal response');
  assert.equal(m.normalScale.x,.6);assert.equal(m.normalScale.y,.6);
  assert.equal(m.normalMap.colorSpace,THREE.NoColorSpace);
  assert.equal(m.normalMap.wrapS,THREE.RepeatWrapping);
  assert.equal(m.normalMap.wrapT,THREE.RepeatWrapping);
  assert.equal(m.normalMap.image.width,64);assert.equal(m.normalMap.image.height,64);
  assert.equal(m.normalMap.image.data.length,64*64*4);
 }
 for(const tex of maps){
  const data=tex.image.data;let deviations=0;
  for(let i=0;i<data.length;i+=4){
   const n=[data[i]/127.5-1,data[i+1]/127.5-1,data[i+2]/127.5-1];
   assert.ok(n.every(Number.isFinite));assert.ok(Math.abs(Math.hypot(...n)-1)<.02);
   assert.equal(data[i+3],255);
   assert.ok(n[2]>.8,'surface roughness relief must remain shallow');
   if(Math.abs(n[0])>.01||Math.abs(n[1])>.01)deviations++;
  }
  assert.ok(deviations>64,'normal texture must encode non-flat physical relief');
 }
 assert.equal(JSON.stringify(bindings),original);
 a.dispose();
});
test('normal bytes are repeatable; water clock, history-source boundary and shared texture disposal are unchanged',()=>{
 const a=build(),b=build(),one=normals(a),two=normals(b),disposed=new Map();
 assert.equal(one.length,2);assert.equal(two.length,2);
 for(let i=0;i<one.length;i++){
  assert.deepEqual(one[i].image.data,two[i].image.data);
  disposed.set(one[i],0);
  one[i].addEventListener('dispose',()=>disposed.set(one[i],disposed.get(one[i])+1));
 }
 const anchors=a.locations.map(l=>[l.id,l.group.position.x,l.group.position.z,l.group.userData.visualAuthority]);
 a.tick(3,{globalCalm:true,storm:0});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===3));
 a.tick(6,{globalCalm:true,storm:0});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===6));
 a.tick(9,{paused:true});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===6));
 assert.deepEqual(a.locations.map(l=>[l.id,l.group.position.x,l.group.position.z,l.group.userData.visualAuthority]),anchors);
 assert.equal(a.worldMutationAllowed,false);assert.equal(a.weatherMutationAllowed,false);
 assert.deepEqual(a.principalCharacters,[]);assert.equal(JSON.stringify(bindings),original);
 a.dispose();a.dispose();b.dispose();
 assert.ok([...disposed.values()].every(n=>n===1),'each shared normal map released exactly once');
});
