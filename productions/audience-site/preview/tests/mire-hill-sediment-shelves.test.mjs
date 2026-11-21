import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {projectAtlas} from '../../src/observer-world.mjs';
import {spatialBindings} from '../spatial.mjs';
import {buildAtlasSiteAssets} from '../atlas-site-assets.mjs';

const source=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const bindings=spatialBindings({locations:projectAtlas(source.locations)}),before=JSON.stringify(bindings);
const build=()=>buildAtlasSiteAssets(THREE,bindings,()=>4);
const id='LOC-DK-MUD-HILL',name='Mire Hill sediment shelves · candidate';
function parts(a){
 const site=a.locations.find(l=>l.id===id);
 assert.ok(site,'recorded encounter site present');
 const shelves=site.group.children.filter(o=>o.name===name);
 assert.equal(shelves.length,1,'one batchable sediment mesh');
 const mire=a.water.find(w=>w.kind==='mire');
 assert.ok(mire&&site.group.children.includes(mire.mesh));
 return {site,shelves:shelves[0],mire};
}

test('Mire Hill only has local candidate shoals, source landmarks and water unchanged',()=>{
 const record=source.locations.find(l=>l.id===id);
 assert.equal(record.physical_zone_id,'REG-CENTRAL-BASIN');
 assert.deepEqual(record.persistent_landmarks,['hill','mire','battle standards']);
 const a=build(),{site,shelves,mire}=parts(a);
 assert.deepEqual(site.sourceLandmarks,record.persistent_landmarks);
 assert.equal(site.group.userData.canonStatus,record.canon_status);
 assert.equal(site.group.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
 assert.equal(shelves.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
 assert.equal(shelves.userData.sourceWaterKind,'mire');
 assert.equal(shelves.userData.shoalCount,12);
 assert.equal(a.water.length,4);assert.equal(a.locations.length,20);
 for(const w of a.water){
  assert.equal(w.mesh.geometry.getAttribute('position').count,393);
  assert.equal(w.mesh.geometry.index.count,2184);
  assert.equal(w.mesh.children.length,0);
 }
 for(const other of a.locations.filter(l=>l.id!==id))
  assert.equal(other.group.children.filter(o=>o.name===name).length,0,other.id);
 assert.equal(mire.mesh.position.x,1);assert.equal(mire.mesh.position.z,1.3);
 assert.equal(a.worldMutationAllowed,false);assert.equal(a.weatherMutationAllowed,false);
 assert.deepEqual(a.principalCharacters,[]);assert.equal(JSON.stringify(bindings),before);
 a.dispose();
});

test('twelve separated physical silt shelves stay within original mire ellipse and reproduce exactly',()=>{
 const a=build(),s=parts(a).shelves,b=build(),copy=parts(b).shelves;
 const pos=s.geometry.getAttribute('position'),colors=s.geometry.getAttribute('color'),idx=s.geometry.index;
 assert.equal(s.geometry.type,'BufferGeometry');
 assert.equal(pos.count,12*5*9);assert.equal(colors.count,pos.count);
 assert.equal(idx.count,12*4*8*6);
 assert.equal(s.material.isMeshStandardMaterial,true);
 assert.equal(s.material.vertexColors,true);
 assert.equal(s.material.metalness,0);assert.equal(s.material.roughness,.97);
 assert.equal(s.castShadow,false);
 assert.deepEqual(s.position.toArray(),[1,0,1.3]);
 assert.deepEqual(Array.from(pos.array),Array.from(copy.geometry.getAttribute('position').array));
 assert.deepEqual(Array.from(colors.array),Array.from(copy.geometry.getAttribute('color').array));
 assert.deepEqual(Array.from(idx.array),Array.from(copy.geometry.index.array));
 let crest=0,low=Infinity,inner=Infinity,outer=0,variation=new Set();
 for(let i=0;i<pos.count;i++){
  const x=pos.getX(i),y=pos.getY(i),z=pos.getZ(i),r=Math.hypot(x/7.2,z/5.2);
  assert.ok([x,y,z,r].every(Number.isFinite));
  inner=Math.min(inner,r);outer=Math.max(outer,r);crest=Math.max(crest,y);low=Math.min(low,y);
  variation.add(colors.getX(i).toFixed(4));
  for(const shade of [colors.getX(i),colors.getY(i),colors.getZ(i)])assert.ok(shade>0&&shade<.5);
 }
 assert.ok(inner>=.80&&outer<=.985,'all sediment within unchanged mire water ellipse');
 assert.ok(low>=.215&&crest<=.281&&crest>.25,'visible but shallow relief');
 assert.ok(variation.size>20,'nonuniform deterministic sediment shades');
 const perPatch=5*9,indicesPerPatch=4*8*6;
 for(let patch=0;patch<12;patch++){
  const slice=Array.from(idx.array.slice(patch*indicesPerPatch,(patch+1)*indicesPerPatch));
  assert.ok(slice.every(n=>n>=patch*perPatch&&n<(patch+1)*perPatch),'no triangle connects shoals');
 }
 assert.equal(JSON.stringify(bindings),before);a.dispose();b.dispose();
});

test('environment shelves do not override ordinary water in global calm, pause or cleanup',()=>{
 const a=build(),{shelves,mire}=parts(a);
 assert.equal(shelves.material.uniforms,undefined);
 a.tick(1.3,{storm:0,globalCalm:true});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===1.3));
 a.tick(3.9,{storm:0,globalCalm:true});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===3.9));
 a.tick(11,{storm:5,globalCalm:true,paused:true});
 assert.equal(mire.material.uniforms.uTime.value,3.9);
 let gCount=0,mCount=0;
 shelves.geometry.addEventListener('dispose',()=>gCount++);
 shelves.material.addEventListener('dispose',()=>mCount++);
 a.dispose();a.dispose();a.tick(20);
 assert.equal(gCount,1);assert.equal(mCount,1);
 assert.equal(mire.material.uniforms.uTime.value,3.9);
 assert.equal(JSON.stringify(bindings),before);
});
