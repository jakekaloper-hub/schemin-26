import test from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';

const bindings=[
 {id:'LOC-TDS-WATERFALL-TEMPLE',anchor:[32,0,29],canonStatus:'PERMANENT_CANON'},
 {id:'LOC-MUD-DOGS-SWAMP',anchor:[42,0,16],canonStatus:'PERMANENT_CANON'},
 {id:'LOC-COUNTRY-CLUB-JACKSON',anchor:[57,0,24],canonStatus:'PERMANENT_CANON'},
];
const build=()=>buildRegionalAssets(THREE,bindings,()=>2);
const vegetation=(assets)=>assets.locations.find(x=>x.id==='LOC-MUD-DOGS-SWAMP').group.getObjectByName('Candidate wetland emergent vegetation');

test('wetland bank has a bounded, varied, single-draw emergent vegetation candidate outside the water ellipse',()=>{
 const assets=build();
 const foliage=vegetation(assets);
 assert.ok(foliage?.isMesh,'source-defined Mud Dogs Swamp needs distinct emergent vegetation');
 assert.equal(foliage.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
 assert.deepEqual(foliage.userData.sourceEnvironment,['cypress-like wetlands','raised ground']);
 assert.ok(foliage.material.isShaderMaterial,'wind bending must remain a GPU animation, not hundreds of CPU-updated meshes');
 assert.ok(foliage.material.vertexShader.includes('uTime'),'foliage needs independently advancing animated geometry');
 const p=foliage.geometry.getAttribute('position');
 const s=foliage.geometry.getAttribute('aSway');
 assert.ok(p.count>=900,`expected many independently shaped blades, got ${p.count}`);
 assert.equal(s.count,p.count);
 const heights=new Set();
 for(let i=0;i<p.count;i++){
  const r=Math.hypot(p.getX(i)/10.5,p.getZ(i)/8.2);
  assert.ok(r>=1.06&&r<=1.25,`marsh vegetation intrudes into source water ellipse or extends too far: ${r}`);
  assert.ok(p.getY(i)>=.16&&p.getY(i)<=2.3);
  assert.ok(s.getY(i)>=0&&s.getY(i)<=1);
  if(s.getY(i)===1)heights.add(p.getY(i).toFixed(2));
 }
 assert.ok(heights.size>=12,'height/profile must not be a repeated flat silhouette');
 const angles=[];for(let i=0;i<p.count;i++)if(s.getY(i)===0&&i%3===0){
  const a=(Math.atan2(p.getZ(i)/8.2,p.getX(i)/10.5)+Math.PI*2)%(Math.PI*2);angles.push(a);
 }
 angles.sort((a,b)=>a-b);
 const gaps=angles.slice(1).map((v,i)=>v-angles[i]);gaps.push(angles[0]+Math.PI*2-angles.at(-1));
 assert.ok(Math.max(...gaps)>.14,'bank vegetation must grow in patches with open intervals, not a perfect luminous fence');
 const color=foliage.geometry.getAttribute('aTint');
 let maxLum=0;for(let i=0;i<color.count;i++)maxLum=Math.max(maxLum,(color.getX(i)+color.getY(i)+color.getZ(i))/3);
 assert.ok(maxLum<.33,'wetland blades must remain muted, not bright white or gold around the bank');
 assets.dispose();
});

test('emergent vegetation is limited to Mud Dogs Swamp and does not modify world or neighboring locations',()=>{
 const before=JSON.stringify(bindings);
 const assets=build();
 assert.equal(assets.worldMutationAllowed,false);
 assert.deepEqual(assets.principalCharacters,[]);
 assert.deepEqual(assets.locations.map(x=>x.id),bindings.map(x=>x.id));
 for(const location of assets.locations.filter(x=>x.id!=='LOC-MUD-DOGS-SWAMP')){
  assert.equal(location.group.getObjectByName('Candidate wetland emergent vegetation'),undefined);
 }
 assert.equal(JSON.stringify(bindings),before);
 assets.dispose();
});

test('marsh motion follows environmental clock but pauses; ordinary swamp water remains active during global calm',()=>{
 const assets=build();
 const m=vegetation(assets)?.material;
 assert.ok(m?.uniforms?.uTime);
 const water=assets.water.find(w=>w.kind==='swamp');
 assets.tick(1,{storm:0});assert.equal(m.uniforms.uTime.value,1);assert.equal(water.material.uniforms.uTime.value,1);
 assets.tick(3,{storm:0});assert.equal(m.uniforms.uTime.value,3);assert.equal(water.material.uniforms.uTime.value,3);
 assets.tick(9,{storm:0,paused:true});assert.equal(m.uniforms.uTime.value,3);assert.equal(water.material.uniforms.uTime.value,3);
 assets.dispose();
});
