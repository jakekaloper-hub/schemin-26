import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {createAtmosphericSky,createBaseWaterMaterial} from '../three-world.mjs';

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
 assert.equal(sky.material.uniforms.uStrength.value,1);
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
 assert.match(source,/scene\.fog\.color\.copy\(scene\.background\);sky\.material\.uniforms\.uHorizon\.value\.copy\(scene\.fog\.color\);sky\.material\.uniforms\.uStrength\.value=strength/);
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
