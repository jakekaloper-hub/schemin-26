import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {projectAtlas} from '../../src/observer-world.mjs';
import {spatialBindings} from '../spatial.mjs';
import {buildAtlasSiteAssets} from '../atlas-site-assets.mjs';

const source=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const bindings=spatialBindings({locations:projectAtlas(source.locations)});
const originalBindings=JSON.stringify(bindings);
const placeId='LOC-BELT-KEEPER-KEEP';
const build=()=>buildAtlasSiteAssets(THREE,bindings,()=>4);
const site=a=>a.locations.find(l=>l.id===placeId);
const stone=a=>site(a)?.group.children.find(o=>o.name==='Dark keep');

test('provisional Belt Keeper keep is the only site with the source-bound relief facade',()=>{
 const sourcePlace=source.locations.find(l=>l.id===placeId);
 assert.equal(sourcePlace.canon_status,'PROVISIONAL_CANON');
 assert.deepEqual(sourcePlace.persistent_landmarks,['dark keep','championship hall']);
 assert.deepEqual(sourcePlace.current_state,['Belt remains with Belt Keeper']);
 const a=build(),s=site(a),keep=stone(a);
 assert.ok(s&&keep);assert.equal(a.locations.length,20);
 assert.equal(s.group.userData.canonStatus,'PROVISIONAL_CANON');
 assert.equal(s.group.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
 assert.equal(keep.userData.sourceLandmark,'dark keep');
 assert.equal(s.group.children.filter(o=>o.name==='Dark keep').length,1);
 for(const landmark of sourcePlace.persistent_landmarks)
  assert.ok(s.group.children.some(o=>o.userData?.sourceLandmark===landmark),landmark);
 assert.ok(s.group.children.some(o=>o.name==='Pitched roof candidate'));
 assert.ok(s.group.children.some(o=>o.name==='Masonry arch candidate'));
 for(const other of a.locations.filter(l=>l.id!==placeId))
  assert.equal(other.group.children.filter(o=>o.name==='Dark keep').length,0,other.id);
 assert.equal(a.worldMutationAllowed,false);assert.equal(a.weatherMutationAllowed,false);
 assert.deepEqual(a.principalCharacters,[]);assert.equal(JSON.stringify(bindings),originalBindings);
 a.dispose();
});

test('one static keep mesh preserves exact original extents and transform with recessed mortar and stone tones',()=>{
 const a=build(),o=stone(a),g=o.geometry,p=g.getAttribute('position'),c=g.getAttribute('color');
 const baseline=new THREE.BoxGeometry(5.5,6.5,4.8,12,18,10),before=baseline.getAttribute('position');
 assert.equal(g.type,'BoxGeometry');
 assert.deepEqual([g.parameters.width,g.parameters.height,g.parameters.depth],[5.5,6.5,4.8]);
 assert.deepEqual([g.parameters.widthSegments,g.parameters.heightSegments,g.parameters.depthSegments],[12,18,10]);
 assert.deepEqual(o.position.toArray(),[0,4.45,-.8]);
 assert.deepEqual(o.scale.toArray(),[1,1,1]);
 assert.equal(o.material.vertexColors,true);assert.equal(o.material.roughness,.97);
 assert.equal(o.material.metalness,0);
 assert.equal(p.count,c.count);assert.equal(p.count,before.count);
 assert.ok(p.count>900&&p.count<1500);
 let relief=0,edgeFixed=0,minChannel=Infinity,maxChannel=-Infinity;
 for(let i=0;i<p.count;i++){
  const x=p.getX(i),y=p.getY(i),z=p.getZ(i);
  const bx=before.getX(i),by=before.getY(i),bz=before.getZ(i);
  assert.ok([x,y,z].every(Number.isFinite));
  assert.ok(Math.abs(x)<=2.750001&&Math.abs(y)<=3.250001&&Math.abs(z)<=2.400001);
  const delta=Math.hypot(x-bx,y-by,z-bz);
  assert.ok(delta>=0&&delta<=.041001,'no expanded footprint or deep incision');
  if(delta>.005)relief++;
  if(delta<.000001)edgeFixed++;
  for(const channel of [c.getX(i),c.getY(i),c.getZ(i)]){
   assert.ok(Number.isFinite(channel)&&channel>.03&&channel<.16);
   minChannel=Math.min(minChannel,channel);maxChannel=Math.max(maxChannel,channel);
  }
 }
 assert.ok(relief>180,'physically inset stone courses and joints');
 assert.ok(edgeFixed>100,'original face boundaries retained');
 assert.ok(maxChannel-minChannel>.025,'restrained dark mineral coloration');
 assert.ok(g.getAttribute('normal'));
 const b=build(),again=stone(b);
 assert.deepEqual(p.array,again.geometry.getAttribute('position').array);
 assert.deepEqual(c.array,again.geometry.getAttribute('color').array);
 baseline.dispose();a.dispose();b.dispose();
});

test('candidate stone cannot write weather/history and does not arrest ordinary water during El Niño calm',()=>{
 const a=build(),o=stone(a),surface=o.geometry.getAttribute('position').array.slice();
 assert.ok(a.water.length>=4);
 a.tick(1.75,{globalCalm:true,storm:0});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===1.75));
 a.tick(4.25,{globalCalm:true,storm:0});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===4.25));
 a.tick(8,{paused:true,storm:4});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===4.25));
 assert.deepEqual(o.geometry.getAttribute('position').array,surface);
 assert.equal(a.worldMutationAllowed,false);assert.equal(a.weatherMutationAllowed,false);
 assert.equal(JSON.stringify(bindings),originalBindings);
 let disposed=0;o.material.addEventListener('dispose',()=>disposed++);
 a.dispose();a.dispose();assert.equal(disposed,1);
});
