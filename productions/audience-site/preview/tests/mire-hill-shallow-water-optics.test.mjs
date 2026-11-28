import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {projectAtlas} from '../../src/observer-world.mjs';
import {spatialBindings} from '../spatial.mjs';
import {buildAtlasSiteAssets} from '../atlas-site-assets.mjs';

const source=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const bindings=spatialBindings({locations:projectAtlas(source.locations)});
const sourceSnapshot=JSON.stringify(bindings);
const siteId='LOC-DK-MUD-HILL';
const smooth=(a,b,x)=>{const t=Math.max(0,Math.min(1,(x-a)/(b-a)));return t*t*(3-2*t);};
function tint(x,y,grazing,enabled=1){
 const r=Math.hypot(x,y),rim=smooth(.62,.86,r)*(1-smooth(.91,.975,r));
 const patch=Math.max(0,Math.min(1,.72+.28*Math.sin(x*22+Math.sin(y*13)*1.2)*Math.sin(y*19)));
 return .17*enabled*rim*patch*(1-.7*grazing);
}
const build=()=>buildAtlasSiteAssets(THREE,bindings,()=>4);

test('source-exact Mire Hill uses existing water disk and immutable Atlas bindings',()=>{
 const a=build(),mire=a.water.find(w=>w.kind==='mire');
 const place=source.locations.find(p=>p.id===siteId);
 const site=a.locations.find(p=>p.id===siteId);
 assert.ok(place?.persistent_landmarks.includes('mire'));
 assert.ok(site&&mire&&site.group.children.includes(mire.mesh));
 assert.equal(site.group.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
 assert.equal(a.locations.length,20);
 assert.equal(a.water.length,4);
 assert.deepEqual(new Set(a.water.map(w=>w.kind)),new Set(['mountain lake','mire','sheltered port','watercourse crossing']));
 for(const w of a.water){
  assert.equal(w.material.uniforms.uMire.value,w===mire?1:0);
  assert.equal(w.mesh.geometry.getAttribute('position').count,393);
  assert.equal(w.mesh.geometry.index.count,2184);
  assert.equal(w.material.depthWrite,false);
  assert.equal(w.mesh.children.length,0);
 }
 assert.equal(a.worldMutationAllowed,false);
 assert.equal(a.weatherMutationAllowed,false);
 assert.deepEqual(a.principalCharacters,[]);
 assert.equal(JSON.stringify(bindings),sourceSnapshot);
 a.dispose();
});

test('bounded pigment reacts to actual view angle, fades before source disk edge, and never touches other waters',()=>{
 const a=build(),mire=a.water.find(w=>w.kind==='mire'),shader=mire.material.fragmentShader;
 for(const phrase of ['float mireRim=smoothstep(.62,.86,length(mireXY))*(1.-smoothstep(.91,.975,length(mireXY)));',
  'float mirePatch=clamp(.72+.28*sin(mireXY.x*22.+sin(mireXY.y*13.)*1.2)*sin(mireXY.y*19.),0.,1.);',
  'float mireShallow=uMire*mireRim*mirePatch*(1.-.7*grazing);',
  'c=mix(c,vec3(.31,.29,.22),.17*mireShallow);'])assert.ok(shader.includes(phrase),phrase);
 assert.equal(tint(0,0,0),0);
 assert.equal(tint(.99,.01,0),0,'no pigment at unchanged water perimeter');
 const overhead=tint(.87,.02,0),grazing=tint(.87,.02,1);
 assert.ok(overhead>.08&&overhead<=.17);
 assert.ok(grazing>0&&grazing<overhead*.31);
 for(let ix=-10;ix<=10;ix++)for(let iy=-10;iy<=10;iy++){
  const val=tint(ix/10,iy/10,.5);
  assert.ok(Number.isFinite(val)&&val>=0&&val<=.17);
  assert.equal(tint(ix/10,iy/10,.5,0),0);
 }
 for(const w of a.water.filter(w=>w!==mire)){
  assert.equal(w.material.uniforms.uMire.value,0);
  assert.ok(w.material.fragmentShader.includes('float mireShallow=uMire*'));
  assert.equal(tint(.87,.02,0,w.material.uniforms.uMire.value),0);
 }
 assert.equal(JSON.stringify(bindings),sourceSnapshot);
 a.dispose();
});

test('El Niño synthetic global calm does not freeze independent water; explicit pause does',()=>{
 const a=build(),mire=a.water.find(w=>w.kind==='mire');
 a.tick(1.25,{globalCalm:true,storm:0});
 assert.equal(mire.material.uniforms.uTime.value,1.25);
 a.tick(3.5,{globalCalm:true,storm:0});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===3.5));
 a.tick(9,{globalCalm:true,storm:0,paused:true});
 assert.equal(mire.material.uniforms.uTime.value,3.5);
 a.dispose();
 assert.equal(JSON.stringify(bindings),sourceSnapshot);
});
