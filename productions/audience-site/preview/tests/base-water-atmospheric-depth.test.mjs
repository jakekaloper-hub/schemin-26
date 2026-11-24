import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {createBaseWaterMaterial} from '../three-world.mjs';

const source=readFileSync(new URL('../three-world.mjs',import.meta.url),'utf8');
const density=.0018; // Existing scene FogExp2 density, never a separate weather parameter.
const wave=(x,y,t)=>.07*Math.sin(x*.17+t*.6)+.05*Math.sin(y*.21-t*.39);
const fogFactor=d=>1-Math.exp(-density*density*d*d);
function viewDepth(camera,water,p){
 camera.updateMatrixWorld(true);water.updateMatrixWorld(true);
 const modelView=new THREE.Matrix4().multiplyMatrices(camera.matrixWorldInverse,water.matrixWorld);
 return -new THREE.Vector3(...p).applyMatrix4(modelView).z;
}

test('existing base water participates in world atmospheric fog without new draw calls or custom uniforms',()=>{
 const material=createBaseWaterMaterial(THREE);
 assert.equal(material.fog,true);
 assert.equal(material.side,THREE.DoubleSide);
 assert.deepEqual(Object.keys(material.uniforms).sort(),['fogColor','fogDensity','fogFar','fogNear','uShoreMask','uStorm','uStrength','uTime']);
 assert.match(source,/new THREE\.FogExp2\('#bed1cf',\.0018\)/);
 assert.match(source,/new THREE\.PlaneGeometry\(800,800,70,70\)/);
 assert.match(source,/ocean\.rotation\.x=-Math\.PI\/2;ocean\.position\.y=-\.4/);
 for(const [shader,chunk] of [[material.vertexShader,'fog_pars_vertex'],[material.vertexShader,'fog_vertex'],[material.fragmentShader,'fog_pars_fragment'],[material.fragmentShader,'fog_fragment']])
  assert.ok(shader.includes('#include <'+chunk+'>'),chunk);
 assert.match(material.vertexShader,/vec4 mvPosition=modelViewMatrix\*vec4\(p,1\.\)/);
 assert.match(material.vertexShader,/gl_Position=projectionMatrix\*mvPosition/);
 assert.doesNotMatch(material.vertexShader+material.fragmentShader,/uniform (?:vec3 fogColor|float fogDensity)/);
 assert.match(source,/applyAtmosphereLighting\(sky,scene\.background,scene\.fog\.color,strength\)/);assert.match(source,/fogColor\.copy\(background\)/);
 material.dispose();
});

test('native pinned-Three fog uniforms are complete and isolated between water materials',()=>{
 const first=createBaseWaterMaterial(THREE),second=createBaseWaterMaterial(THREE);
 assert.deepEqual(Object.keys(THREE.UniformsLib.fog).sort(),['fogColor','fogDensity','fogFar','fogNear']);
 for(const name of Object.keys(THREE.UniformsLib.fog)){
  assert.ok(first.uniforms[name]&&second.uniforms[name],name);
  assert.notStrictEqual(first.uniforms[name],second.uniforms[name],name+' isolated uniform object');
 }
 assert.notStrictEqual(first.uniforms.fogColor.value,second.uniforms.fogColor.value);
 first.uniforms.fogDensity.value=density;first.uniforms.fogColor.value.copy(new THREE.Color('#bed1cf'));
 assert.equal(first.uniforms.fogDensity.value,density);
 assert.notEqual(second.uniforms.fogDensity.value,density);
 assert.equal(first.uniforms.uTime.value,0);
 assert.equal(first.uniforms.uStorm.value,0);
 first.dispose();second.dispose();
});

test('pinned Three fog uses actual displaced model-view depth, fading distant water into scene haze',()=>{
 assert.equal(THREE.REVISION,'187');
 assert.match(THREE.ShaderChunk.fog_vertex,/vFogDepth = - mvPosition\.z/);
 assert.match(THREE.ShaderChunk.fog_pars_fragment,/uniform float fogDensity/);
 assert.match(THREE.ShaderChunk.fog_fragment,/fogDensity \* fogDensity \* vFogDepth \* vFogDepth/);
 const camera=new THREE.PerspectiveCamera(41.25,1,.2,1900);
 camera.position.set(0,20,100);camera.lookAt(0,-.4,0);
 const water=new THREE.Mesh(new THREE.PlaneGeometry(800,800,70,70),createBaseWaterMaterial(THREE));
 water.rotation.x=-Math.PI/2;water.position.y=-.4;
 for(const t of [0,8.5]){
  const near=[0,-50,wave(0,-50,t)],far=[0,300,wave(0,300,t)];
  const a=viewDepth(camera,water,near),b=viewDepth(camera,water,far);
  assert.ok(Number.isFinite(a)&&Number.isFinite(b)&&a>0&&b>a,[a,b].join(':'));
  assert.ok(fogFactor(b)>fogFactor(a)&&fogFactor(b)<1&&fogFactor(a)>=0);
 }
 water.geometry.dispose();water.material.dispose();
});

test('optical fog does not change storm authority, historic pause or ordinary moving-water clock',()=>{
 const material=createBaseWaterMaterial(THREE);
 const vertex=material.vertexShader,fragment=material.fragmentShader;
 assert.match(vertex,/p\.z\+=sin\(phaseX\)\*\.07\+sin\(phaseY\)\*\.05/);
 assert.match(source,/if\(!paused\)lastTime=time;regional\.tick\(lastTime,\{paused\}\)/);
 assert.match(source,/oceanMaterial\.uniforms\.uTime\.value=lastTime/);
 assert.match(source,/oceanGeo\.dispose\(\);oceanMaterial\.dispose\(\)/);
 assert.equal((vertex+fragment).match(/\buStorm\b/g)?.length,1);
 assert.doesNotMatch(THREE.ShaderChunk.fog_fragment,/\buStorm\b|\buWeather\b|\buGlobalCalm\b/);
 assert.notEqual(wave(0,0,0),wave(0,0,6));
 material.uniforms.uStorm.value=0;material.uniforms.uTime.value=6;
 assert.equal(material.uniforms.uTime.value,6);
 let disposed=0;material.addEventListener('dispose',()=>disposed++);material.dispose();assert.equal(disposed,1);
});
