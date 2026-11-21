import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {createBaseWaterMaterial} from '../three-world.mjs';

const source=readFileSync(new URL('../three-world.mjs',import.meta.url),'utf8');
const phaseA=(x,z,t)=>x*1.7+Math.sin(z*.7)+t*.65;
const phaseB=(x,z,t)=>z*2.1-t*.41;
const fade=width=>{
 const t=Math.max(0,Math.min(1,(width-.5)/1.5));
 return 1-t*t*(3-2*t);
};
function worldAtPixel(camera,x,y){
 const origin=camera.position.clone();
 const direction=new THREE.Vector3(x,y,.5).unproject(camera).sub(origin).normalize();
 const distance=(-.4-origin.y)/direction.y;
 assert.ok(Number.isFinite(distance)&&distance>0,'test ray intersects existing horizontal water surface');
 return origin.addScaledVector(direction,distance);
}
function phaseFootprint(camera,width,height,time){
 const p=worldAtPixel(camera,0,0);
 const right=worldAtPixel(camera,2/width,0);
 const down=worldAtPixel(camera,0,-2/height);
 const extent=phase=>Math.abs(phase(right.x,right.z,time)-phase(p.x,p.z,time))
  +Math.abs(phase(down.x,down.z,time)-phase(p.x,p.z,time));
 return Math.max(extent(phaseA),extent(phaseB));
}
function aimedCamera(distance){
 const camera=new THREE.PerspectiveCamera(41.25,800/600,.2,1900);
 camera.position.set(0,distance*.28,distance);
 camera.lookAt(0,-.4,0);
 camera.updateProjectionMatrix();camera.updateMatrixWorld(true);
 return camera;
}

test('base water band-limits only its fine optics using WebGL2 fragment footprint',()=>{
 assert.equal(THREE.REVISION,'187');
 const material=createBaseWaterMaterial(THREE);
 const v=material.vertexShader,f=material.fragmentShader;
 assert.equal(material.fog,true);
 assert.equal(material.side,THREE.DoubleSide);
 assert.deepEqual(Object.keys(material.uniforms).sort(),['fogColor','fogDensity','fogFar','fogNear','uShoreMask','uStorm','uStrength','uTime']);
 assert.match(f,/float opticalPhaseA=vP\.x\*1\.7\+sin\(vP\.z\*\.7\)\+uTime\*\.65/);
 assert.match(f,/float opticalPhaseB=vP\.z\*2\.1-uTime\*\.41/);
 assert.match(f,/max\(fwidth\(opticalPhaseA\),fwidth\(opticalPhaseB\)\)/);
 assert.match(f,/1\.-smoothstep\(\.5,2\.,opticalPixelSpan\)/);
 assert.match(f,/pow\(max\(w,0\.\),9\.\)\*fineDetailFade/);
 assert.match(f,/vWaveNormal\+fineDetailFade\*vec3/);
 assert.ok(!v.includes('fwidth('),'screen derivatives remain in fragment shader');
 assert.match(v,/p\.z\+=sin\(phaseX\)\*\.07\+sin\(phaseY\)\*\.05/);
 assert.match(f,/#include <fog_fragment>/);
 assert.match(source,/new THREE\.PlaneGeometry\(800,800,70,70\)/);
 assert.match(source,/ocean\.rotation\.x=-Math\.PI\/2;ocean\.position\.y=-\.4/);
 assert.match(f,/texture2D\(uShoreMask,clamp\(shoreUV,0\.,1\.\)\)/);
 assert.doesNotMatch(v+f,/discard/);
 let count=0;material.addEventListener('dispose',()=>count++);material.dispose();assert.equal(count,1);
});

test('actual perspective footprint fades undersampled fine reflections, not close water',()=>{
 const near=phaseFootprint(aimedCamera(70),800,600,2);
 const mid=phaseFootprint(aimedCamera(400),800,600,2);
 const far=phaseFootprint(aimedCamera(1250),800,600,2);
 assert.ok([near,mid,far].every(Number.isFinite),[near,mid,far].join(':'));
 assert.ok(near<mid&&mid<far,[near,mid,far].join(':'));
 assert.ok(fade(near)>.95,'near fine optical detail remains');
 assert.ok(fade(mid)<fade(near),'middle-distance detail is attenuated');
 assert.ok(fade(far)<.05,'far subpixel glints do not shimmer');
 assert.equal(fade(0),1);assert.equal(fade(2.5),0);
});

test('optical LOD leaves normal water time, calm weather and explicit replay pause separate',()=>{
 const material=createBaseWaterMaterial(THREE),v=material.vertexShader,f=material.fragmentShader;
 assert.equal((v+f).match(/\buStorm\b/g)?.length,1);
 assert.doesNotMatch(v+f,/\buWeather\b|\buGlobalCalm\b/);
 assert.match(source,/if\(!paused\)lastTime=time;regional\.tick\(lastTime,\{paused\}\)/);
 assert.match(source,/oceanMaterial\.uniforms\.uTime\.value=lastTime/);
 const sample=(t)=>.07*Math.sin(t*.6)+.05*Math.sin(-t*.39);
 assert.notEqual(sample(0),sample(4));
 assert.notEqual(phaseA(10,5,0),phaseA(10,5,4));
 assert.ok(phaseFootprint(aimedCamera(70),800,600,0)>0);
 assert.equal(phaseFootprint(aimedCamera(70),800,600,0),phaseFootprint(aimedCamera(70),800,600,4));
 material.uniforms.uStorm.value=0;material.uniforms.uTime.value=4;
 assert.equal(material.uniforms.uTime.value,4);
 material.dispose();
});
