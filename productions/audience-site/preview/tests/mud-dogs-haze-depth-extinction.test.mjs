import test from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from '../vendor/three.module.js';
import {createWetlandWaterHaze} from '../three-world.mjs';

const smoothstep=(a,b,x)=>{
 const t=Math.max(0,Math.min(1,(x-a)/(b-a)));
 return t*t*(3-2*t);
};
const attenuation=d=>smoothstep(4,14,d)*(1-smoothstep(95,165,d));

test('Mud Dogs source-anchored haze attenuates with camera depth, not weather',()=>{
 const haze=createWetlandWaterHaze(THREE);
 try{
  assert.equal(haze.name,'Mud Dogs water-haze · optical candidate');
  assert.equal(haze.userData.locationId,'LOC-MUD-DOGS-SWAMP');
  assert.equal(haze.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
  assert.equal(haze.userData.waterAndWeatherAuthority,'NONE');
  assert.equal(haze.geometry.getAttribute('position').count,96);
  assert.deepEqual(Object.keys(haze.material.uniforms),['uTime','uLightLevel','uPixelRatio']);
  const s=haze.material.vertexShader;
  assert.match(s,/gl_PointSize=clamp\(2600\.\/max\(1\.,-mvPosition\.z\),2\.,64\.\)\*uPixelRatio/);
  assert.match(s,/float viewDepth=max\(0\.,-mvPosition\.z\)/);
  assert.match(s,/float nearVisibility=smoothstep\(4\.,14\.,viewDepth\)/);
  assert.match(s,/float farVisibility=1\.-smoothstep\(95\.,165\.,viewDepth\)/);
  assert.match(s,/vOpacity=\(\.13\+\.055\*\(\.5\+\.5\*sin\(uTime\*\.21\+aPhase\)\)\)\*nearVisibility\*farVisibility/);
  assert.doesNotMatch(s+haze.material.fragmentShader,/uStorm|uGlobalCalm|uWeather|uRain/);
  assert.equal(haze.material.depthWrite,false);
  assert.equal(haze.material.transparent,true);
 }finally{haze.geometry.dispose();haze.material.dispose();}
});

test('depth envelope preserves close local view and ordinary haze animation',()=>{
 assert.equal(attenuation(0),0);
 assert.equal(attenuation(4),0);
 assert.ok(attenuation(9)>0&&attenuation(9)<1);
 assert.equal(attenuation(14),1);
 assert.equal(attenuation(60),1);
 assert.equal(attenuation(95),1);
 assert.ok(attenuation(130)>0&&attenuation(130)<1);
 assert.equal(attenuation(165),0);
 assert.equal(attenuation(260),0);
 const haze=createWetlandWaterHaze(THREE);
 try{
  const before=Array.from(haze.geometry.getAttribute('position').array);
  haze.material.uniforms.uTime.value=18.5;
  assert.equal(haze.material.uniforms.uTime.value,18.5);
  assert.deepEqual(Array.from(haze.geometry.getAttribute('position').array),before);
  assert.deepEqual(Object.keys(haze.material.uniforms),['uTime','uLightLevel','uPixelRatio']);
 }finally{haze.geometry.dispose();haze.material.dispose();}
});

test('Mud Dogs haze receives shared-clock radiance only, independent of drift and optical density',()=>{
 const haze=createWetlandWaterHaze(THREE);
 try{
  const {uniforms,vertexShader,fragmentShader}=haze.material;
  assert.equal(uniforms.uLightLevel.value,1);
  assert.doesNotMatch(vertexShader,/uLightLevel/);
  assert.match(fragmentShader,/float light=clamp\(uLightLevel,0\.,1\.\)/);
  assert.match(fragmentShader,/vec3 radiance=vec3\(\.69,\.80,\.73\)\*mix\(\.30,1\.,light\)/);
  assert.match(fragmentShader,/gl_FragColor=vec4\(radiance,vOpacity\*halo\)/);
  assert.doesNotMatch(fragmentShader,/uStorm|uGlobalCalm|uWeather/);
  uniforms.uTime.value=12;
  uniforms.uLightLevel.value=.2;
  assert.equal(uniforms.uTime.value,12);
 }finally{haze.geometry.dispose();haze.material.dispose();}
});
