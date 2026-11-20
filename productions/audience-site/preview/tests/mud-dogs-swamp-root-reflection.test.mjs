import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';
import {batchStaticGeometry} from '../three-world.mjs';

const atlas=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const ids=['LOC-MUD-DOGS-SWAMP','LOC-TDS-WATERFALL-TEMPLE','LOC-COUNTRY-CLUB-JACKSON'];
const bindings=ids.map(id=>{
 const p=atlas.locations.find(x=>x.id===id);
 assert.ok(p,'Missing source location '+id);
 return {id,anchor:[p.abstract_position[0],0,p.abstract_position[1]],
   canonStatus:p.canon_status,landmarks:p.persistent_landmarks};
});
const baseline=JSON.stringify(atlas),inputBaseline=JSON.stringify(bindings);
const build=()=>buildRegionalAssets(THREE,bindings,()=>2);
const get=(a,kind)=>a.water.find(w=>w.kind===kind);
const clamp=x=>Math.max(0,Math.min(1,x));
function smooth(lo,hi,x){const t=clamp((x-lo)/(hi-lo));return t*t*(3-2*t);}
function reflection(x,y,t,incidence,bank=1){
 const across=Math.abs(x+.12*Math.sin(y*1.3-t*.21));
 const along=Math.abs(y);
 const streak=(1-smooth(.12,.58,across))*(1-smooth(.60,2.10,along));
 const breakup=.55+.45*Math.sin(y*10+t*.51+x*4);
 const view=smooth(.22,.80,1-incidence);
 return clamp(streak*breakup*.20*view*bank);
}
test('Existing Mud Dogs source tree positions alone anchor five illustrated mirror sites',()=>{
 const a=build(),swamp=get(a,'swamp'),mud=a.locations[0].group;
 assert.equal(atlas.locations.find(x=>x.id===ids[0]).physical_zone_id,'REG-SOUTHERN-WETLANDS');
 assert.equal(atlas.locations.find(x=>x.id===ids[0]).canon_status,'PERMANENT_CANON');
 assert.deepEqual(a.locations.map(x=>x.id),ids);
 const trunks=mud.children.filter(x=>x.userData.wetlandPart==='trunk')
   .sort((x,y)=>x.userData.wetlandStand-y.userData.wetlandStand);
 assert.equal(trunks.length,14);
 assert.equal(swamp.material.uniforms.uRootSiteCount.value,5);
 for(let i=0;i<5;i++){
  const actual=swamp.material.uniforms.uRootSites.value[i];
  assert.ok(Math.abs(actual.x-(.5+trunks[i*3].position.x/21))<1e-6);
  assert.ok(Math.abs(actual.y-(.5-trunks[i*3].position.z/16.4))<1e-6);
 }
 assert.ok(a.water.filter(w=>w.kind!=='swamp')
   .every(w=>(w.material.uniforms.uRootSiteCount?.value??0)===0));
 assert.equal(swamp.mesh.geometry.getAttribute('position').count,385);
 assert.equal(swamp.mesh.geometry.getIndex().count,2160);
 assert.equal(swamp.mesh.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
 assert.equal(a.worldMutationAllowed,false);
 assert.deepEqual(a.principalCharacters,[]);
 assert.equal(JSON.stringify(atlas),baseline);
 assert.equal(JSON.stringify(bindings),inputBaseline);
 a.dispose();
});

test('One preexisting water shader contains root-anchored reflections with no weather inputs or additional uniforms',()=>{
 const a=build(),swamp=get(a,'swamp'),shader=swamp.material.fragmentShader;
 const begin=shader.indexOf('}else if(uWetland>.5){');
 const end=shader.indexOf('}else if(uRiver>.5){',begin);
 assert.ok(begin>0&&end>begin);
 const section=shader.slice(begin,end);
 assert.match(section,/float trunkReflection=0\./);
 assert.match(section,/mirrorAcross=abs\(delta\.x\+\.12\*sin\(delta\.y\*1\.3-uTime\*\.21\)\)/);
 assert.match(section,/mirrorStreak=\(1\.-smoothstep\(\.12,\.58,mirrorAcross\)\)/);
 assert.match(section,/mirrorBreakup=\.55\+\.45\*sin\(delta\.y\*10\.\+uTime\*\.51\+delta\.x\*4\.\)/);
 assert.match(section,/trunkReflection=max\(trunkReflection,mirrorStreak\*mirrorBreakup\)/);
 assert.match(section,/trunkView=smoothstep\(\.22,\.80,1\.-viewIncidence\)/);
 assert.match(section,/trunkMirrorMix=clamp\(trunkReflection\*\.20\*trunkView\*bankFade,0\.,\.20\)/);
 assert.match(section,/contactTint=mix\(contactTint,vec3\(\.11,\.19,\.17\),trunkMirrorMix\)/);
 assert.doesNotMatch(section,/uWeather|uStorm|uRain|uGlobalCalm/);
 assert.doesNotMatch(shader.slice(end),/trunkReflection|trunkMirrorMix|mirrorBreakup/);
 assert.ok(a.water.every(w=>!('uTrunkReflection' in w.material.uniforms)));
 assert.equal(swamp.material.transparent,true);
 assert.equal(swamp.mesh.children.length,0);
 a.dispose();
});

test('Reflections are finite, visibly water-animated, perspective and bank constrained',()=>{
 const first=reflection(.08,.25,1,.12),next=reflection(.08,.25,7,.12);
 assert.ok(first>.01&&Math.abs(first-next)>.003);
 assert.equal(reflection(.08,.25,1,1),0,'near-overhead view');
 assert.equal(reflection(.08,.25,1,.12,0),0,'water bank');
 assert.equal(reflection(2,2.5,1,.12),0,'beyond inherited root site envelope');
 let visible=0;
 for(const t of [0,1,5,11,100])for(let i=-35;i<=35;i++)for(let j=-35;j<=35;j++){
  const v=reflection(i*.08,j*.08,t,.1);
  assert.ok(Number.isFinite(v)&&v>=0&&v<=.20+1e-12);
  if(v>.002)visible++;
 }
 assert.ok(visible>500,'the effect is spatial, not a single sample');
});

test('Synthetic global calm leaves all six old water clocks moving; pause, batching and disposal survive',()=>{
 const a=build(),swamp=get(a,'swamp'),mud=a.locations[0].group;
 const oldCount=mud.children.length,batches=batchStaticGeometry(THREE,mud);
 assert.ok(mud.children.length<oldCount);
 assert.ok(mud.children.includes(swamp.mesh),'moving water is not batched away');
 for(const g of batches.geometries)g.dispose();
 const moving=a.water.filter(w=>['swamp','channel','river','waterfall','pool','pond'].includes(w.kind));
 assert.equal(moving.length,6);
 let geomDispose=0,matDispose=0;
 swamp.mesh.geometry.addEventListener('dispose',()=>geomDispose++);
 swamp.material.addEventListener('dispose',()=>matDispose++);
 a.tick(3,{globalCalm:true,storm:0});
 a.tick(11,{globalCalm:true,storm:0});
 assert.ok(moving.every(w=>w.material.uniforms.uTime.value===11));
 a.tick(16,{paused:true,globalCalm:true,storm:0});
 assert.ok(moving.every(w=>w.material.uniforms.uTime.value===11));
 a.tick(24,{globalCalm:true,storm:0});
 assert.ok(moving.every(w=>w.material.uniforms.uTime.value===24));
 a.dispose();a.dispose();a.tick(28);
 assert.equal(geomDispose,1);assert.equal(matDispose,1);
 assert.equal(JSON.stringify(atlas),baseline);
 assert.equal(JSON.stringify(bindings),inputBaseline);
});
