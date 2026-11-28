import test from 'node:test';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {buildWorldGeometry} from '../renderer.mjs';
import {shorelineOpticalStrength,createWaterShorelineTexture,createBaseWaterMaterial} from '../three-world.mjs';

const source=readFileSync(new URL('../three-world.mjs',import.meta.url),'utf8');

test('shore optics are bounded to submerged candidate elevations and fail closed on invalid heights',()=>{
 const water=-.4;
 assert.equal(shorelineOpticalStrength(()=>water,0,0),0,'dry / exact waterline is not a water pixel');
 assert.equal(shorelineOpticalStrength(()=>water+.1,0,0),0,'dry terrain');
 assert.ok(Math.abs(shorelineOpticalStrength(()=>water-.4,0,0)-.75)<1e-12);
 assert.equal(shorelineOpticalStrength(()=>water-1.6,0,0),0,'deep bed');
 assert.equal(shorelineOpticalStrength(()=>water-100,0,0),0,'ocean outside banks');
 assert.throws(()=>shorelineOpticalStrength(()=>Number.NaN,0,0),/INVALID_SHORELINE_HEIGHT/);
 assert.throws(()=>shorelineOpticalStrength(()=>water,Number.NaN,0),/INVALID_SHORELINE_SAMPLE/);
 assert.throws(()=>createWaterShorelineTexture(THREE,()=>0,127),/INVALID_SHORELINE_TEXTURE_SIZE/);
 assert.throws(()=>createWaterShorelineTexture(THREE,null,64),/INVALID_SHORELINE_HEIGHT_PROVIDER/);
});

test('one deterministic compact read-only height-derived mask; exact UV/sample bounds, no map writes',()=>{
 const samples=[],height=(x,z)=>{samples.push([x,z]);return -.4-.8*(1+Math.sin(x*.07)*Math.cos(z*.04));};
 const a=createWaterShorelineTexture(THREE,height,64);
 const first=Buffer.from(a.image.data);
 const b=createWaterShorelineTexture(THREE,height,64);
 assert.equal(first.length,64*64*4);
 assert.deepEqual(Buffer.from(b.image.data),first);
 assert.equal(createHash('sha256').update(first).digest('hex'),createHash('sha256').update(b.image.data).digest('hex'));
 assert.equal(samples.length,2*64*64);
 assert.deepEqual(samples[0],[-110+110/64,-110+110/64]);
 assert.ok(samples.every(([x,z])=>x>-110&&z>-110&&x<110&&z<110));
 assert.ok(first.some((v,i)=>i%4===0&&v>0),'shoreline reaches some submerged pixels');
 assert.ok(first.every((v,i)=>i%4===3?v===255:i%4===0?v<=255:v===0));
 assert.equal(a.image.width,64);assert.equal(a.image.height,64);
 assert.equal(a.format,THREE.RGBAFormat);assert.equal(a.wrapS,THREE.ClampToEdgeWrapping);
 assert.equal(a.wrapT,THREE.ClampToEdgeWrapping);assert.equal(a.colorSpace,THREE.NoColorSpace);
 assert.equal(a.generateMipmaps,false);
 assert.equal(a.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
 assert.equal(a.userData.provenance,'existing-terrain-height');
 let disposals=0;a.addEventListener('dispose',()=>disposals++);a.dispose();
 assert.equal(disposals,1,'texture disposed exactly once in this lifecycle');
 b.dispose();
});

test('original candidate river bed gives wet and dry samples; terrain positions and identity remain unchanged',()=>{
 const bindings=[];
 const {mesh,height}=buildWorldGeometry(bindings,2,0);
 const before=mesh.values.slice();
 const river=shorelineOpticalStrength(height,11,60);
 const bank=shorelineOpticalStrength(height,7,45);
 const dry=shorelineOpticalStrength(height,-50,55);
 assert.equal(dry,0);
 assert.equal(river,0,'deep river channel is not falsely treated as shore foam');
 assert.ok(bank>.5,'the sampled existing near-bank bed produces a localized optical highlight');
 const texture=createWaterShorelineTexture(THREE,height,64);
 const wetPixels=texture.image.data.filter((v,i)=>i%4===0&&v>0).length;
 assert.ok(wetPixels>10&&wetPixels<64*64*.5,'shore cue is spatially localized');
 assert.deepEqual(mesh.values,before,'no geometry or source deformation');
 assert.equal(bindings.length,0);
 texture.dispose();
});

test('same animated plane uses original water time and bound mask; no weather, history or extra draw passes',()=>{
 const terrain=createWaterShorelineTexture(THREE,()=>-1,64);
 const material=createBaseWaterMaterial(THREE,terrain);
 assert.equal(material.uniforms.uShoreMask.value,terrain,'no cloned/orphaned sampler');
 assert.equal(material.uniforms.uTime.value,0);
 assert.equal(material.uniforms.uStorm.value,0);
 assert.match(material.fragmentShader,/texture2D\(uShoreMask,clamp\(shoreUV,0\.,1\.\)\)/);
 assert.match(material.fragmentShader,/vP\.x\*3\.1\+uTime\*\.8/);
 assert.match(material.fragmentShader,/vP\.z\*2\.8-uTime\*\.71/);
 assert.match(material.fragmentShader,/float within=step\(0\.,shoreUV\.x\)/);
 assert.match(material.fragmentShader,/shallows\*breaking\*\.25/);
 assert.doesNotMatch(material.fragmentShader,/\buGlobalCalm\b|\buWeather\b|\buRain\b/);
 assert.match(source,/const shorelineTexture=createWaterShorelineTexture\(THREE,height\)/);
 assert.match(source,/const oceanMaterial=createBaseWaterMaterial\(THREE,shorelineTexture\)/);
 assert.match(source,/oceanGeo\.dispose\(\);oceanMaterial\.dispose\(\);shorelineTexture\.dispose\(\)/);
 assert.match(source,/if\(!paused\)lastTime=time;regional\.tick\(lastTime,\{paused\}\)/);
 assert.match(source,/oceanMaterial\.uniforms\.uTime\.value=lastTime/);
 material.uniforms.uStorm.value=0;material.uniforms.uTime.value=10;
 assert.equal(material.uniforms.uTime.value,10,'calm still permits ordinary water motion');
 material.dispose();terrain.dispose();
});
