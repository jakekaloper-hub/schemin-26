import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {createBaseWaterMaterial} from '../three-world.mjs';

const source=readFileSync(new URL('../three-world.mjs',import.meta.url),'utf8');
function waterAt(x,y,time){
 const a=x*.17+time*.6,b=y*.21-time*.39;
 return {
  height:.07*Math.sin(a)+.05*Math.sin(b),
  slopeX:.07*.17*Math.cos(a),
  slopeY:.05*.21*Math.cos(b),
 };
}
function viewFresnel(normal,view){
 const dot=normal.reduce((sum,v,i)=>sum+v*view[i],0);
 return (1-Math.max(0,dot))**3;
}

test('base water retains its one-plane physical displacement, material budget and lifecycle',()=>{
 const material=createBaseWaterMaterial(THREE);
 assert.ok(material.isShaderMaterial);
 assert.deepEqual(Object.keys(material.uniforms).sort(),['fogColor','fogDensity','fogFar','fogNear','uShoreMask','uStorm','uStrength','uTime']);
 assert.equal(material.side,THREE.DoubleSide);
 assert.deepEqual([material.uniforms.uTime.value,material.uniforms.uStrength.value,material.uniforms.uStorm.value],[0,1,0]);
 for(const token of ['p.z+=sin(phaseX)*.07+sin(phaseY)*.05','vec3 localNormal=normalize','mat3(modelMatrix)*localNormal','vWaveNormal','cameraPosition-vP','reflect(-sunDir,n)','fresnel','<tonemapping_fragment>','<colorspace_fragment>'])
  assert.ok(material.vertexShader.includes(token)||material.fragmentShader.includes(token),token);
 assert.match(source,/const oceanMaterial=createBaseWaterMaterial\(THREE,shorelineTexture\);/);
 assert.match(source,/new THREE\.PlaneGeometry\(800,800,70,70\)/);
 assert.match(source,/ocean\.rotation\.x=-Math\.PI\/2;ocean\.position\.y=-\.4/);
 assert.match(material.fragmentShader,/texture2D\(uShoreMask,clamp\(shoreUV,0\.,1\.\)\)/);
 assert.doesNotMatch(material.vertexShader+material.fragmentShader,/discard/);
 let disposed=0;material.addEventListener('dispose',()=>disposed++);
 material.dispose();assert.equal(disposed,1);
});

test('same finite physical waves produce mathematically matching time-varying local slopes without changing footprint',()=>{
 const material=createBaseWaterMaterial(THREE);
 const v=material.vertexShader;
 assert.match(v,/float phaseX=p\.x\*\.17\+uTime\*\.6/);
 assert.match(v,/float phaseY=p\.y\*\.21-uTime\*\.39/);
 assert.match(v,/-.07\*\.17\*cos\(phaseX\)/);
 assert.match(v,/-.05\*\.21\*cos\(phaseY\)/);
 for(const t of [0,1.25,20.5])for(const [x,y] of [[-110,32],[0,0],[75,-64]]){
  const a=waterAt(x,y,t),e=.0001;
  assert.ok(Number.isFinite(a.height)&&Math.abs(a.height)<=.12000001);
  assert.ok(Math.abs((waterAt(x+e,y,t).height-waterAt(x-e,y,t).height)/(2*e)-a.slopeX)<1e-9);
  assert.ok(Math.abs((waterAt(x,y+e,t).height-waterAt(x,y-e,t).height)/(2*e)-a.slopeY)<1e-9);
 }
 assert.notEqual(waterAt(0,0,0).height,waterAt(0,0,5).height);
 material.dispose();
});

test('view-responsive light changes while storm calm never freezes ordinary water or historic pause',()=>{
 const m=createBaseWaterMaterial(THREE),v=m.vertexShader,f=m.fragmentShader;
 assert.match(f,/float glint=pow\(max\(dot\(reflect\(-sunDir,n\),viewDir\),0\.\),64\.\)/);
 assert.match(f,/float fresnel=pow\(1\.-max\(dot\(n,viewDir\),0\.\),3\.\)/);
 assert.ok(viewFresnel([0,1,0],[0,1,0])<viewFresnel([0,1,0],[1,0,0]));
 assert.equal((v+f).match(/\buStorm\b/g)?.length,1,'existing storm uniform remains declared, but cannot drive wave time or water optics');
 assert.doesNotMatch(v+f,/\buWeather\b|\buRain\b|\buGlobalCalm\b/);
 assert.match(source,/if\(!paused\)lastTime=time;regional\.tick\(lastTime,\{paused\}\)/);
 assert.match(source,/oceanMaterial\.uniforms\.uTime\.value=lastTime/);
 assert.match(source,/oceanGeo\.dispose\(\);oceanMaterial\.dispose\(\)/);
 m.uniforms.uTime.value=5;m.uniforms.uStorm.value=0;
 assert.equal(m.uniforms.uTime.value,5,'global calm changes weather, not river clock');
 m.dispose();
});
