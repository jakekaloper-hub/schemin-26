import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {projectAtlas} from '../../src/observer-world.mjs';
import {spatialBindings} from '../spatial.mjs';
import {buildAtlasSiteAssets} from '../atlas-site-assets.mjs';

const source=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const bindings=spatialBindings({locations:projectAtlas(source.locations)});
const before=JSON.stringify(bindings);
const id='LOC-LLC-STORM-CITY';
const build=()=>buildAtlasSiteAssets(THREE,bindings,()=>4);
const find=a=>{
 const site=a.locations.find(l=>l.id===id);
 assert.ok(site,'the original source-defined port exists');
 const objects=site.group.children.filter(o=>o.name==='Storm barrier');
 assert.equal(objects.length,1,'one original named barrier remains');
 return {site,barrier:objects[0]};
};
const signature=b=>JSON.stringify({
 position:Array.from(b.geometry.getAttribute('position').array),
 color:Array.from(b.geometry.getAttribute('color').array),
 index:Array.from(b.geometry.index.array)
});

test('original source-bound harbor barrier has a batched physical jointed face within its prior envelope',()=>{
 const record=source.locations.find(x=>x.id===id);
 assert.equal(record.canon_status,'PROVISIONAL_CANON');
 assert.ok(record.persistent_landmarks.includes('storm barriers'));
 assert.deepEqual(record.current_state,['Week 3 El Niño weather-event history']);
 const a=build(),{site,barrier}=find(a),geo=barrier.geometry;
 assert.equal(barrier.userData.sourceLandmark,'storm barriers');
 assert.equal(barrier.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
 assert.equal(barrier.userData.finishClaim,false);
 assert.equal(barrier.material.vertexColors,true);
 assert.equal(geo.type,'BufferGeometry');
 assert.ok(geo.getAttribute('normal'));
 assert.ok(geo.index.count>5000,'multiple real indexed stone faces, not a painted rectangle');
 assert.ok(barrier.userData.stoneUnits>=150,'staggered stone-unit surface');
 const bounds=new THREE.Box3().setFromBufferAttribute(geo.getAttribute('position'));
 const eps=.0001;
 assert.ok(bounds.min.x>=-6.5-eps && bounds.max.x<=6.5+eps);
 assert.ok(bounds.min.y>=.9-eps && bounds.max.y<=2.25+eps);
 assert.ok(bounds.min.z>=3.725-eps && bounds.max.z<=4.275+eps);
 const z=geo.getAttribute('position'),front=new Set();
 for(let i=0;i<z.count;i++)if(z.getZ(i)>4.22)front.add(z.getZ(i).toFixed(4));
 assert.ok(front.size>=4,'physical staggered face depths');
 assert.equal(site.group.children.filter(x=>x.name==='Mercantile tower').length,5);
 assert.equal(a.locations.length,20);
 assert.equal(a.worldMutationAllowed,false);
 assert.equal(a.weatherMutationAllowed,false);
 assert.deepEqual(a.principalCharacters,[]);
 assert.equal(JSON.stringify(bindings),before);
 a.dispose();
});

test('storm barrier mesh is deterministic, disposes and remains independent of weather and ordinary water',()=>{
 const a=build(),b=build(),barrier=find(a).barrier,peer=find(b).barrier;
 assert.equal(signature(barrier),signature(peer));
 const meshBefore=signature(barrier);
 let disposed=0;
 barrier.geometry.addEventListener('dispose',()=>disposed++);
 a.tick(1,{storm:0});const times=a.water.map(w=>w.material.uniforms.uTime.value);
 assert.ok(times.every(t=>t===1));
 a.tick(3,{storm:0});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===3),
  'synthetic calm cannot freeze ordinary source-bound water');
 a.tick(7,{paused:true});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===3));
 assert.equal(signature(barrier),meshBefore,'no weather or replay mutation of barrier');
 assert.equal(JSON.stringify(bindings),before);
 a.dispose();a.dispose();b.dispose();
 assert.equal(disposed,1);
});
