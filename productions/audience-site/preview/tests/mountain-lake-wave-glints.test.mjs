import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {projectAtlas} from '../../src/observer-world.mjs';
import {spatialBindings} from '../spatial.mjs';
import {buildAtlasSiteAssets} from '../atlas-site-assets.mjs';

const source=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const bindings=spatialBindings({locations:projectAtlas(source.locations)}),original=JSON.stringify(bindings);
const placeId='LOC-BRIDGE-MOUNTAIN-LAKE',build=()=>buildAtlasSiteAssets(THREE,bindings,()=>4);
const smooth=(a,b,x)=>{const f=Math.max(0,Math.min(1,(x-a)/(b-a)));return f*f*(3-2*f);};
const norm=a=>a.map(x=>x/Math.hypot(...a));
const dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0);
const reflect=(incident,normal)=>incident.map((x,i)=>x-2*dot(incident,normal)*normal[i]);
const sunlight=norm([.43,.79,.37]);

// Independent numeric sample of the pre-existing displaced lake wave and bridge contact.
function height(w,x,y,t){
 const inside=1-smooth(.58,.95,Math.hypot(x,y)),amp=w.material.uniforms.uAmplitude.value;
 const waves=.72*Math.sin(x*12.7-t*1.18+Math.sin(y*7.5)*.45)+.28*Math.sin(y*10.2+t*.74+x*3);
 const radius=Math.min(Math.hypot(x+.39,y),Math.hypot(x-.39,y));
 return amp*inside*(waves+.16*Math.exp(-radius*8)*Math.sin(radius*24-t*1.7));
}
function upNormal(w,x,y,t){
 const e=.0002,dx=(height(w,x+e,y,t)-height(w,x-e,y,t))/(2*e);
 const dy=(height(w,x,y+e,t)-height(w,x,y-e,t))/(2*e);
 return norm([-dx,1,dy]); // disk rotates -90 degrees, displacement is world up
}
function viewGlint(w,x,y,t,eye){
 const n=upNormal(w,x,y,t),ray=reflect(sunlight.map(x=>-x),n);
 return (1-smooth(.58,.95,Math.hypot(x,y)))*Math.pow(Math.max(dot(ray,eye),0),12);
}

test('source-exact Mountain Lake alone gets highlights, no new water or footprint',()=>{
 const a=build(),place=source.locations.find(l=>l.id===placeId);
 const site=a.locations.find(l=>l.id===placeId),lake=a.water.find(w=>w.kind==='mountain lake');
 assert.ok(place&&site&&lake&&site.group.children.includes(lake.mesh));
 assert.equal(site.group.userData.canonStatus,place.canon_status);
 assert.equal(a.locations.length,20);assert.equal(a.water.length,4);
 assert.equal(a.water.filter(w=>w.material.uniforms.uLakeGlint.value===1).length,1);
 for(const w of a.water){
  assert.equal(w.material.uniforms.uLakeGlint.value,w===lake?1:0);
  assert.equal(w.material.uniforms.uBridge.value,w===lake?1:0);
  assert.equal(w.mesh.geometry.getAttribute('position').count,393);
  assert.equal(w.mesh.geometry.index.count,2184);
  assert.equal(w.mesh.children.length,0);
  assert.equal(w.material.depthWrite,false);assert.equal(w.material.transparent,true);
 }
 assert.deepEqual(a.principalCharacters,[]);
 assert.equal(a.worldMutationAllowed,false);assert.equal(a.weatherMutationAllowed,false);
 assert.equal(JSON.stringify(bindings),original);a.dispose();
});
test('physical wave normals, camera angle and existing rim determine restrained glints',()=>{
 const a=build(),lake=a.water.find(w=>w.kind==='mountain lake'),f=lake.material.fragmentShader,v=lake.material.vertexShader;
 for(const word of ['uniform float uLakeGlint;','cross(dFdx(vWorld),dFdy(vWorld))',
   'vec3 lakeNormal=faceNormal.y<0.?-faceNormal:faceNormal;',
   'dot(reflect(-lakeSun,lakeNormal),eyeRay)','float lakeGlint=0.;',
   'if(uLakeGlint>.5)','vec3(.13,.18,.17)*lakeGlint'])assert.ok(f.includes(word),word);
 assert.ok(v.includes('vWorld=(modelMatrix*vec4(p,1.)).xyz'));
 assert.ok(v.includes('p.z+=uAmplitude*interior'));
 const x=.31,y=.16,t=1.2,peakEye=norm(reflect(sunlight.map(z=>-z),upNormal(lake,x,y,t)));
 const peak=viewGlint(lake,x,y,t,peakEye),later=viewGlint(lake,x,y,3.7,peakEye);
 assert.ok(peak>.95&&peak<=1);
 assert.ok(later>=0&&later<.5,'moving waves alter the same camera reflection');
 assert.equal(viewGlint(lake,x,y,t,peakEye.map(n=>-n)),0,'opposite camera direction has no sun glint');
 assert.equal(viewGlint(lake,1,0,t,peakEye),0,'original shoreline has no added glint');
 assert.ok(.13*peak<=.13&&.18*peak<=.18,'candidate gain is numerically bounded');
 for(const w of a.water.filter(w=>w!==lake))assert.equal(w.material.uniforms.uLakeGlint.value,0);
 assert.equal(JSON.stringify(bindings),original);a.dispose();
});
test('global calm leaves lake in motion; explicit pause and cleanup retain existing contracts',()=>{
 const a=build(),lake=a.water.find(w=>w.kind==='mountain lake'),p=lake.mesh.geometry.getAttribute('position').array.slice();
 a.tick(1.2,{globalCalm:true,storm:0});assert.equal(lake.material.uniforms.uTime.value,1.2);
 a.tick(3.7,{globalCalm:true,storm:0});assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===3.7));
 assert.notEqual(height(lake,.31,.16,1.2),height(lake,.31,.16,3.7));
 a.tick(20,{paused:true,storm:4});assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===3.7));
 assert.deepEqual(lake.mesh.geometry.getAttribute('position').array,p);
 assert.equal(JSON.stringify(bindings),original);
 let disposed=0;
 lake.mesh.geometry.addEventListener('dispose',()=>disposed++);
 lake.material.addEventListener('dispose',()=>disposed++);
 a.dispose();a.dispose();a.tick(100);
 assert.equal(disposed,2);assert.equal(lake.material.uniforms.uTime.value,3.7);
});
