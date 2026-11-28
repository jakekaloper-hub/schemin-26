import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {projectAtlas} from '../../src/observer-world.mjs';
import {spatialBindings} from '../spatial.mjs';
import {buildAtlasSiteAssets} from '../atlas-site-assets.mjs';
const data=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const bindings=spatialBindings({locations:projectAtlas(data.locations)}),snapshot=JSON.stringify(bindings);
const build=()=>buildAtlasSiteAssets(THREE,bindings,()=>4);
const smooth=(a,b,x)=>{let t=Math.max(0,Math.min(1,(x-a)/(b-a)));return t*t*(3-2*t);};
function crest(x,y,t,gate=1){
 const r=Math.min(Math.hypot(x+.39,y),Math.hypot(x-.39,y));
 return gate*(1-smooth(.58,.95,Math.hypot(x,y)))*Math.exp(-r*8)*smooth(.40,.90,Math.sin(r*24-t*1.7));
}
test('source-bound Mountain Lake alone gets the crest and original water geometry and authority',()=>{
 const a=build(),lake=a.water.find(x=>x.kind==='mountain lake'),site=a.locations.find(x=>x.id==='LOC-BRIDGE-MOUNTAIN-LAKE');
 assert.ok(site&&lake&&site.group.children.includes(lake.mesh));
 assert.ok(data.locations.some(x=>x.id===site.id));
 assert.equal(a.locations.length,20);assert.equal(a.water.length,4);
 assert.equal(a.water.filter(x=>x.material.uniforms.uBridge.value===1).length,1);
 for(const w of a.water){
  assert.equal(w.material.uniforms.uBridge.value,w===lake?1:0);
  assert.equal(w.mesh.geometry.getAttribute('position').count,393);
  assert.equal(w.mesh.geometry.index.count,2184);
  assert.equal(w.mesh.children.length,0);
  assert.deepEqual(Object.keys(w.material.uniforms).sort(),['uAmplitude','uBarrier','uBridge','uColor','uCrossing','uLakeGlint','uLightLevel','uMire','uTime','uViewSheen']);
 }
 assert.deepEqual(a.principalCharacters,[]);assert.equal(a.worldMutationAllowed,false);
 assert.equal(a.weatherMutationAllowed,false);assert.equal(JSON.stringify(bindings),snapshot);a.dispose();
});
test('lake bridge optical crest follows the physical ripple phase and displaced-water normal',()=>{
 const a=build(),w=a.water.find(x=>x.kind==='mountain lake'),v=w.material.vertexShader,f=w.material.fragmentShader;
 assert.ok(v.includes('varying float vBridgeCrest;')&&f.includes('varying float vBridgeCrest;'));
 assert.ok(v.includes('float bridgeWave=exp(-bridgeR*8.)*sin(bridgeR*24.-uTime*1.7);'));
 assert.ok(v.includes('vBridgeCrest=uBridge*interior*exp(-bridgeR*8.)*smoothstep(.40,.90,bridgeWave);'));
 assert.ok(v.includes('p.z+=uBridge*uAmplitude*.16*interior*bridgeWave;'));
 assert.ok(f.includes('sin(bridgeR*24.-uTime*1.7)')&&!f.includes('bridgeR*34.-uTime*1.7'));
 assert.ok(f.includes('vec3 bridgeNormal=faceNormal.y<0.?-faceNormal:faceNormal;'));
 assert.ok(f.includes('bridgeCrest=vBridgeCrest*(.40+.60*bridgeReflect);'));
 assert.ok(f.includes('c=clamp(c+vec3(.025,.046,.044)*bridgeCrest,0.,1.);'));
 assert.ok(!f.includes('uGlobalCalm')&&!f.includes('uStorm'));
 assert.ok(!Object.hasOwn(w.material.uniforms,'uBridgeCrest'));a.dispose();
});
test('under synthetic El Niño calm ordinary crest advances, rim stays fixed and explicit pause holds',()=>{
 let peak=0,changed=0;
 for(let ix=-90;ix<=90;ix++)for(let iy=-35;iy<=35;iy++){
  const x=ix/100,y=iy/100,a=crest(x,y,.6),b=crest(x,y,2.5);
  assert.ok(Number.isFinite(a)&&Number.isFinite(b)&&a>=0&&a<=1&&b>=0&&b<=1);
  assert.equal(crest(x,y,.6,0),0);
  if(Math.hypot(x,y)>=.95)assert.ok(a<1e-12&&b<1e-12);
  peak=Math.max(peak,a,b);changed=Math.max(changed,Math.abs(a-b));
 }
 assert.ok(peak>.7&&changed>.5);
 const a=build(),lake=a.water.find(w=>w.kind==='mountain lake');
 a.tick(.6,{globalCalm:true,storm:0});a.tick(2.5,{globalCalm:true,storm:0});
 assert.equal(lake.material.uniforms.uTime.value,2.5);
 a.tick(10,{paused:true,globalCalm:true,storm:0});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===2.5));
 assert.equal(JSON.stringify(bindings),snapshot);a.dispose();
});
