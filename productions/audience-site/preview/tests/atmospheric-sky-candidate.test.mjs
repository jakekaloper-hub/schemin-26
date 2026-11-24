import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {createAtmosphericSky,createBaseWaterMaterial,applyAtmosphereLighting} from '../three-world.mjs';

import {illustrativeLight} from '../spatial.mjs';

const source=readFileSync(new URL('../three-world.mjs',import.meta.url),'utf8');

test('source-neutral sky is bounded to one disposable, camera-centered atmosphere candidate',()=>{
 const sky=createAtmosphericSky(THREE),other=createAtmosphericSky(THREE);
 assert.ok(sky.isMesh&&sky.geometry.type==='SphereGeometry');
 assert.equal(sky.geometry.parameters.widthSegments,24);
 assert.equal(sky.geometry.parameters.heightSegments,12);
 assert.equal(sky.scale.x,1000);
 assert.equal(sky.frustumCulled,false);
 assert.equal(sky.renderOrder,-1000);
 assert.equal(sky.castShadow,false);
 assert.equal(sky.receiveShadow,false);
 assert.equal(sky.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
 assert.equal(sky.material.side,THREE.BackSide);
 assert.equal(sky.material.depthTest,false);
 assert.equal(sky.material.depthWrite,false);
 assert.equal(sky.material.fog,false);
 assert.equal(sky.material.toneMapped,false);
 assert.equal(sky.material.uniforms.uDaylight.value,1);
 assert.notStrictEqual(sky.material.uniforms.uHorizon.value,other.material.uniforms.uHorizon.value);
 assert.equal(sky.material.uniforms.uHorizon.value.getHexString(),'bed1cf');
 assert.match(sky.material.fragmentShader,/smoothstep\(\.015,\.72,max\(ray\.y,0\.\)\)/);
 assert.match(sky.material.fragmentShader,/normalize\(vec3\(-95\.,150\.,60\.\)\)/);
 assert.match(sky.material.fragmentShader,/#include <colorspace_fragment>/);
 assert.doesNotMatch(sky.material.vertexShader+sky.material.fragmentShader,/\buTime\b|\buStorm\b|\buGlobalCalm\b|fetch\(|Math\.random/);
 let d=0,m=0;sky.geometry.addEventListener('dispose',()=>d++);sky.material.addEventListener('dispose',()=>m++);
 sky.geometry.dispose();sky.material.dispose();other.geometry.dispose();other.material.dispose();
 assert.equal(d,1);assert.equal(m,1);
});

test('sky follows camera and existing fog rather than changing source geography or water/weather time',()=>{
 assert.match(source,/const sky=createAtmosphericSky\(THREE\);scene\.add\(sky\)/);
 assert.match(source,/camera\.updateMatrixWorld\(true\);sky\.position\.copy\(camera\.position\)/);
 assert.match(source,/applyAtmosphereLighting\(sky,scene\.background,scene\.fog\.color,strength\)/);
 assert.match(source,/sky\.geometry\.dispose\(\);sky\.material\.dispose\(\)/);
 assert.match(source,/if\(!paused\)lastTime=time;regional\.tick\(lastTime,\{paused\}\)/);
 assert.match(source,/oceanMaterial\.uniforms\.uTime\.value=lastTime/);
 assert.match(source,/const oceanGeo=new THREE\.PlaneGeometry\(800,800,70,70\)/);
 const water=createBaseWaterMaterial(THREE);
 assert.equal(water.uniforms.uTime.value,0);
 assert.equal(water.uniforms.uStorm.value,0);
 assert.match(water.vertexShader,/p\.z\+=sin\(phaseX\)\*\.07\+sin\(phaseY\)\*\.05/);
 water.dispose();
});

test('shared illustrative Eastern-clock strength drives continuous horizon and zenith contrast without solar halo at night',()=>{
 const sky=createAtmosphericSky(THREE),background=new THREE.Color(),fog=new THREE.Color();
 const sample=hour=>{
  applyAtmosphereLighting(sky,background,fog,illustrativeLight(hour).strength);
  assert.ok(background.equals(fog)&&fog.equals(sky.material.uniforms.uHorizon.value));
  return {day:sky.material.uniforms.uDaylight.value,rgb:background.toArray()};
 };
 const night=sample(0),dawn=sample(6),morning=sample(9),noon=sample(12),dusk=sample(18);
 for(const edge of [dawn,dusk]){assert.ok(edge.day<1e-12);edge.rgb.forEach((v,i)=>assert.ok(Math.abs(v-night.rgb[i])<1e-12));}
 assert.deepEqual(night,{day:0,rgb:[.055,.085,.13]});
 assert.ok(morning.day>0&&morning.day<1);
 assert.ok(Math.abs(noon.day-1)<1e-12);
 [.5,.63,.64].forEach((v,i)=>assert.ok(Math.abs(noon.rgb[i]-v)<1e-12));
 night.rgb.forEach((v,i)=>assert.ok(v<morning.rgb[i]&&morning.rgb[i]<noon.rgb[i]));
 assert.match(sky.material.fragmentShader,/mix\(vec3\(\.012,\.025,\.052\),vec3\(\.28,\.43,\.53\),light\)/);
 assert.match(sky.material.fragmentShader,/halo\*\.21\*light\*upper/);
 sky.geometry.dispose();sky.material.dispose();
});

test('direct terrain sunlight shares the atmospheric daylight while ambient illumination remains at night',()=>{
 const sky=createAtmosphericSky(THREE),background=new THREE.Color(),fog=new THREE.Color();
 const sample=hour=>{
  const strength=illustrativeLight(hour).strength;
  const daylight=applyAtmosphereLighting(sky,background,fog,strength);
  assert.equal(daylight,sky.material.uniforms.uDaylight.value);
  return {direct:2.5*daylight,ambient:.45+strength*.95};
 };
 const night=sample(0),dawn=sample(6),morning=sample(9),noon=sample(12),dusk=sample(18);
 assert.equal(night.direct,0);
 assert.ok(night.ambient>0);
 assert.ok(dawn.direct<1e-12&&dusk.direct<1e-12);
 assert.ok(morning.direct>0&&morning.direct<noon.direct);
 assert.ok(Math.abs(noon.direct-2.5)<1e-12);
 assert.ok(Math.abs(noon.ambient-1.4)<1e-12);
 assert.match(source,/const daylight=applyAtmosphereLighting\(sky,scene\.background,scene\.fog\.color,strength\)/);
 assert.match(source,/sun\.intensity=2\.5\*daylight;hemisphere\.intensity=\.45\+strength\*\.95/);
 sky.geometry.dispose();sky.material.dispose();
});
