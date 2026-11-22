import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {projectAtlas} from '../../src/observer-world.mjs';
import {spatialBindings} from '../spatial.mjs';
import {buildAtlasSiteAssets} from '../atlas-site-assets.mjs';

const source=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const bindings=spatialBindings({locations:projectAtlas(source.locations)});
const snapshot=JSON.stringify(bindings),build=()=>buildAtlasSiteAssets(THREE,bindings,()=>4);
function smoothstep(a,b,x){const t=Math.max(0,Math.min(1,(x-a)/(b-a)));return t*t*(3-2*t);}
function contactCrest(x,y,time,gate=1){
 const radius=Math.hypot(x,y),interior=1-smoothstep(.58,.95,radius);
 const axis=Math.abs(y+.016),span=smoothstep(-.85,-.62,x)*(1-smoothstep(.45,.65,x));
 const band=Math.exp(-axis*13)*span,wave=Math.sin(axis*26-time*1.35+x*3.1);
 return gate*interior*band*smoothstep(.40,.90,wave);
}

test('source-exact Storm City port uses the existing barrier-contact mesh, no new water or canon',()=>{
 const a=build(),place=a.locations.find(x=>x.id==='LOC-LLC-STORM-CITY'),port=a.water.find(w=>w.kind==='sheltered port');
 assert.ok(place&&port&&place.group.children.includes(port.mesh));
 assert.ok(source.locations.find(x=>x.id==='LOC-LLC-STORM-CITY').persistent_landmarks.includes('storm barriers'));
 assert.equal(a.locations.length,20);assert.equal(a.water.length,4);
 assert.deepEqual(a.water.filter(w=>w.material.uniforms.uBarrier.value===1).map(w=>w.kind),['sheltered port']);
 assert.equal(port.mesh.geometry.getAttribute('position').count,393);
 assert.equal(port.mesh.geometry.index.count,2184);
 assert.equal(port.mesh.children.length,0);
 assert.equal(Object.keys(port.material.uniforms).length,9);
 assert.equal(port.material.depthWrite,false);
 assert.equal(a.worldMutationAllowed,false);assert.equal(a.weatherMutationAllowed,false);
 assert.deepEqual(a.principalCharacters,[]);assert.equal(JSON.stringify(bindings),snapshot);
 a.dispose();
});

test('port-only optical crest follows the real barrier displacement phase and normal, not weather',()=>{
 const a=build(),port=a.water.find(w=>w.kind==='sheltered port');
 const vs=port.material.vertexShader,fs=port.material.fragmentShader;
 assert.match(vs,/varying float vBarrierCrest;/);
 assert.match(fs,/varying float vBarrierCrest;/);
 assert.ok(vs.includes('vBarrierCrest=uBarrier*interior*barrierBand*smoothstep(.40,.90,barrierWave);'));
 assert.ok(vs.includes('p.z+=uBarrier*uAmplitude*.20*interior*barrierBand*barrierWave;'));
 assert.ok(vs.includes('float barrierWave=sin(barrierAxis*26.-uTime*1.35+position.x*3.1);'));
 assert.ok(fs.includes('vec3 barrierNormal=faceNormal.y<0.?-faceNormal:faceNormal;'));
 assert.ok(fs.includes('float barrierReflect=pow(max(dot(reflect(-barrierKey,barrierNormal),eyeRay),0.),12.);'));
 assert.ok(fs.includes('barrierCrest=vBarrierCrest*(.35+.65*barrierReflect);'));
 assert.ok(fs.includes('c=clamp(c+vec3(.028,.046,.045)*barrierCrest,0.,1.);'));
 assert.ok(!Object.hasOwn(port.material.uniforms,'uBarrierCrest'),'vertex varying, no new uniform');
 assert.ok(!fs.includes('uStorm')&&!fs.includes('uGlobalCalm'),'weather stays upstream');
 for(const water of a.water.filter(w=>w!==port))assert.equal(water.material.uniforms.uBarrier.value,0);
 a.dispose();
});

test('moving contact stays bounded and inside original shore; calm advances and explicit pause holds',()=>{
 let peak=0,moved=0;
 for(let xi=-13;xi<=9;xi++)for(let yi=-12;yi<=12;yi++){
  const x=xi*.05,y=yi*.01,one=contactCrest(x,y,1.2),two=contactCrest(x,y,3.7);
  assert.ok(Number.isFinite(one)&&Number.isFinite(two)&&one>=0&&two>=0&&one<=1&&two<=1);
  assert.equal(contactCrest(x,y,1.2,0),0,'unrelated water has no port crest');
  peak=Math.max(peak,one,two);moved=Math.max(moved,Math.abs(one-two));
 }
 assert.ok(peak>.6&&moved>.5,'visible wave crests change with ordinary time');
 for(const [x,y] of [[1,0],[-1,0],[0,1],[0,-1]])assert.equal(contactCrest(x,y,1.2),0,'original shoreline held');
 const a=build(),port=a.water.find(w=>w.kind==='sheltered port');
 a.tick(1.2,{globalCalm:true,storm:0});a.tick(3.7,{globalCalm:true,storm:0});
 assert.equal(port.material.uniforms.uTime.value,3.7);
 a.tick(20,{paused:true,globalCalm:true,storm:0});
 assert.equal(port.material.uniforms.uTime.value,3.7);
 assert.equal(JSON.stringify(bindings),snapshot);a.dispose();
});
