import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {createWetlandWaterHaze,createBaseWaterMaterial} from '../three-world.mjs';

const source=readFileSync(new URL('../three-world.mjs',import.meta.url),'utf8');

test('Mud Dogs water-haze is one deterministic, source-identified bounded non-actor optical candidate',()=>{
 const a=createWetlandWaterHaze(THREE),b=createWetlandWaterHaze(THREE);
 assert.equal(a.type,'Points');
 assert.equal(a.name,'Mud Dogs water-haze · optical candidate');
 assert.equal(a.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
 assert.equal(a.userData.locationId,'LOC-MUD-DOGS-SWAMP');
 assert.equal(a.userData.waterAndWeatherAuthority,'NONE');
 assert.equal(a.userData.navigable,false);
 assert.equal(a.castShadow,false);
 assert.equal(a.receiveShadow,false);
 const p=a.geometry.getAttribute('position'),phase=a.geometry.getAttribute('aPhase');
 assert.equal(p.count,96);assert.equal(phase.count,96);
 assert.deepEqual(Array.from(p.array),Array.from(b.geometry.getAttribute('position').array));
 assert.deepEqual(Array.from(phase.array),Array.from(b.geometry.getAttribute('aPhase').array));
 for(let i=0;i<p.count;i++){
  const [x,y,z]=[p.getX(i),p.getY(i),p.getZ(i)];
  assert.ok([x,y,z,phase.getX(i)].every(Number.isFinite));
  assert.ok((x/10.5)**2+(z/8.2)**2<.72,'candidate halo stays inside the existing water disc');
  assert.ok(y>=.20&&y<.80,'mist remains close to the already modeled water');
 }
 assert.equal(a.material.uniforms.uTime.value,0);
 assert.equal(Object.keys(a.material.uniforms).join(','),'uTime');
 assert.equal(a.material.transparent,true);
 assert.equal(a.material.depthWrite,false);
 assert.equal(a.material.depthTest,true);
 assert.equal(a.material.fog,false);
 assert.equal(a.material.map,undefined);
 assert.doesNotMatch(a.material.vertexShader+a.material.fragmentShader,/uStorm|uStrength|uGlobalCalm|uWeather|fetch\(|Math\.random/);
 assert.match(a.material.fragmentShader,/gl_PointCoord/);
 assert.match(a.material.fragmentShader,/#include <colorspace_fragment>/);
 let g=0,m=0;a.geometry.addEventListener('dispose',()=>g++);a.material.addEventListener('dispose',()=>m++);
 a.geometry.dispose();a.material.dispose();b.geometry.dispose();b.material.dispose();
 assert.equal(g,1);assert.equal(m,1);
});

test('swamp haze attaches only to the source-identified regional site and preserves all existing Atlas frames',()=>{
 assert.match(source,/const framesBySite=siteViewFrames\(THREE,siteLocations\)/);
 assert.match(source,/const swampSite=regional\.locations\.find\(l=>l\.id==='LOC-MUD-DOGS-SWAMP'\)/);
 assert.match(source,/const swampHaze=swampSite\?createWetlandWaterHaze\(THREE\):null/);
 assert.match(source,/if\(swampHaze\)swampSite\.group\.add\(swampHaze\)/);
 assert.match(source,/if\(swampHaze\)\{swampHaze\.geometry\.dispose\(\);swampHaze\.material\.dispose\(\);\}/);
 assert.match(source,/regional\.tick\(lastTime,\{paused\}\);atlasSites\?\.tick\(lastTime,\{paused\}\)/);
 assert.match(source,/if\(!paused\)lastTime=time/);
 assert.match(source,/if\(swampHaze\)swampHaze\.material\.uniforms\.uTime\.value=lastTime/);
 assert.match(source,/oceanMaterial\.uniforms\.uTime\.value=lastTime/);
 assert.doesNotMatch(source,/swampHaze\.material\.uniforms\.uStorm/);
 const water=createBaseWaterMaterial(THREE);assert.equal(water.uniforms.uTime.value,0);water.dispose();
});

test('optical drift is small compared with the existing swamp disc and has no geographic or weather authority',()=>{
 const haze=createWetlandWaterHaze(THREE);
 const s=haze.material.vertexShader;
 assert.match(s,/p\.x\+=\.23\*sin\(uTime\*\.19\+aPhase\)/);
 assert.match(s,/p\.z\+=\.19\*cos\(uTime\*\.17\+aPhase\*1\.3\)/);
 assert.match(s,/p\.y\+=\.035\*sin\(uTime\*\.29\+aPhase\)/);
 assert.match(s,/gl_PointSize=clamp\(2600\.\/max\(1\.,-mvPosition\.z\),2\.,64\.\)/);
 assert.match(haze.material.fragmentShader,/vec2 p=\(gl_PointCoord\*2\.-1\.\)\*vec2\(1\.,2\.1\)/);
 assert.ok(haze.material.uniforms.uTime.value===0);
 assert.equal(haze.renderOrder,3);
 assert.equal(haze.frustumCulled,false);
 haze.geometry.dispose();haze.material.dispose();
});
