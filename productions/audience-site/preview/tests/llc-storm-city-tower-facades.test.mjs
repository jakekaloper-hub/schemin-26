import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {projectAtlas} from '../../src/observer-world.mjs';
import {spatialBindings} from '../spatial.mjs';
import {buildAtlasSiteAssets} from '../atlas-site-assets.mjs';

const source=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const bindings=spatialBindings({locations:projectAtlas(source.locations)});
const unchanged=JSON.stringify(bindings);
const id='LOC-LLC-STORM-CITY';
const expected=[[-4,-3,6],[0,-3.5,8],[4,-3,5.6],[-3,0,4],[2,0,4.7]];
const build=()=>buildAtlasSiteAssets(THREE,bindings,()=>4);
function towers(a){
 const site=a.locations.find(l=>l.id===id);
 assert.ok(site,'source Port City exists');
 return {site,objects:site.group.children.filter(o=>o.name==='Mercantile tower')};
}
test('only source-exact provisional LLC Port City carries five upgraded mercantile towers',()=>{
 const record=source.locations.find(l=>l.id===id);
 assert.equal(record.canon_status,'PROVISIONAL_CANON');
 assert.deepEqual(record.persistent_landmarks,['mercantile towers','storm barriers']);
 assert.deepEqual(record.current_state,['Week 3 El Niño weather-event history']);
 const a=build(),{site,objects}=towers(a);
 assert.equal(objects.length,5);assert.equal(a.locations.length,20);
 assert.equal(site.group.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
 assert.equal(site.group.userData.canonStatus,record.canon_status);
 for(const mark of record.persistent_landmarks)assert.ok(site.group.children.some(o=>o.userData.sourceLandmark===mark),mark);
 assert.equal(objects[0].userData.sourceLandmark,'mercantile towers');
 assert.ok(site.group.children.some(o=>o.name==='Storm barrier'&&o.userData.sourceLandmark==='storm barriers'));
 for(const other of a.locations.filter(l=>l.id!==id))
  assert.equal(other.group.children.filter(o=>o.name==='Mercantile tower').length,0,other.id);
 assert.equal(a.worldMutationAllowed,false);assert.equal(a.weatherMutationAllowed,false);
 assert.deepEqual(a.principalCharacters,[]);assert.equal(JSON.stringify(bindings),unchanged);
 a.dispose();
});
test('five original tower envelopes gain deterministic bounded mortar relief with shared static material',()=>{
 const a=build(),objects=towers(a).objects,b=build(),again=towers(b).objects;
 const materials=new Set();let affected=0,minColor=Infinity,maxColor=-Infinity;
 for(let k=0;k<expected.length;k++){
  const [x,z,h]=expected[k],o=objects[k],g=o.geometry,pp=g.getAttribute('position'),c=g.getAttribute('color');
  const ys=Math.max(20,Math.round(h*6));
  const base=new THREE.BoxGeometry(2.7,h,2.5,10,ys,10),before=base.getAttribute('position');
  assert.equal(g.type,'BoxGeometry');
  assert.deepEqual([g.parameters.width,g.parameters.height,g.parameters.depth],[2.7,h,2.5]);
  assert.deepEqual([g.parameters.widthSegments,g.parameters.heightSegments,g.parameters.depthSegments],[10,ys,10]);
  assert.deepEqual(o.position.toArray(),[x,.95+h/2,z]);
  assert.deepEqual(o.rotation.toArray(),[0,0,0,'XYZ']);
  assert.deepEqual(o.scale.toArray(),[1,1,1]);
  assert.equal(pp.count,before.count);assert.equal(pp.count,c.count);
  assert.ok(pp.count>1000 && pp.count<4000);
  assert.equal(o.material.vertexColors,true);assert.equal(o.material.roughness,.96);assert.equal(o.material.metalness,0);
  materials.add(o.material);
  for(let i=0;i<pp.count;i++){
   const xx=pp.getX(i),yy=pp.getY(i),zz=pp.getZ(i);
   assert.ok([xx,yy,zz].every(Number.isFinite));
   assert.ok(Math.abs(xx)<=1.350001&&Math.abs(yy)<=h/2+.000001&&Math.abs(zz)<=1.250001);
   const d=Math.hypot(xx-before.getX(i),yy-before.getY(i),zz-before.getZ(i));
   assert.ok(d<=.04001,'no outward expansion/deep damage');
   if(d>.005)affected++;
   for(const ch of [c.getX(i),c.getY(i),c.getZ(i)]){
    assert.ok(Number.isFinite(ch)&&ch>.20&&ch<.85);
    minColor=Math.min(minColor,ch);maxColor=Math.max(maxColor,ch);
   }
  }
  assert.deepEqual(Array.from(pp.array),Array.from(again[k].geometry.getAttribute('position').array));
  assert.deepEqual(Array.from(c.array),Array.from(again[k].geometry.getAttribute('color').array));
  assert.ok(g.getAttribute('normal'));
  base.dispose();
 }
 assert.equal(materials.size,1,'one shared static material across five towers');
 assert.ok(affected>1200,'physical relief across facades, not merely painted color');
 assert.ok(maxColor-minColor>.12,'visible but bounded mineral modulation');
 a.dispose();b.dispose();
});
test('masonry retains ordinary sheltered port water during calm, shared pause and single disposal',()=>{
 const a=build(),{objects}=towers(a),port=a.water.find(w=>w.kind==='sheltered port');
 assert.ok(port);assert.equal(a.water.length,4);
 assert.equal(port.material.uniforms.uBarrier.value,1);
 const initial=objects.map(o=>o.geometry.getAttribute('position').array.slice());
 a.tick(2.25,{globalCalm:true,storm:0});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===2.25));
 a.tick(5.5,{globalCalm:true,storm:0});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===5.5));
 a.tick(9,{paused:true,globalCalm:true,storm:8});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===5.5));
 for(let i=0;i<objects.length;i++)assert.deepEqual(objects[i].geometry.getAttribute('position').array,initial[i]);
 assert.equal(JSON.stringify(bindings),unchanged);
 let geoDisposals=0,materialDisposals=0;
 objects[0].geometry.addEventListener('dispose',()=>geoDisposals++);
 objects[0].material.addEventListener('dispose',()=>materialDisposals++);
 a.dispose();a.dispose();a.tick(15);
 assert.equal(geoDisposals,1);assert.equal(materialDisposals,1);
 assert.equal(port.material.uniforms.uTime.value,5.5);
});
