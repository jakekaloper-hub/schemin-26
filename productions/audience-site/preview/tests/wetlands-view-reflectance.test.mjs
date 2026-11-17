import test from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';

const bindings=[
 {id:'LOC-MUD-DOGS-SWAMP',anchor:[42,0,16],canonStatus:'PERMANENT_CANON'},
 {id:'LOC-TDS-WATERFALL-TEMPLE',anchor:[32,0,29],canonStatus:'PERMANENT_CANON'},
 {id:'LOC-COUNTRY-CLUB-JACKSON',anchor:[57,0,24],canonStatus:'PERMANENT_CANON'}
];
const build=()=>buildRegionalAssets(THREE,bindings,()=>2);

test('Grazing reflectance is wetland-only, on unchanged source-bound water meshes',()=>{
 const before=JSON.stringify(bindings),a=build();
 const wet=a.water.filter(w=>w.kind==='swamp'||w.kind==='channel');
 assert.deepEqual(wet.map(w=>w.kind),['swamp','channel']);
 for(const w of wet){
  assert.equal(w.material.uniforms.uWetland.value,1);
  assert.equal(w.mesh.geometry.getAttribute('position').count,385);
  assert.equal(w.mesh.geometry.index.count,2160);
  assert.equal(w.material.depthWrite,false);
  assert.equal(w.material.transparent,true);
 }
 assert.ok(a.water.filter(w=>!wet.includes(w)).every(w=>w.material.uniforms.uWetland?.value===0));
 assert.deepEqual(wet.map(w=>[w.mesh.scale.x,w.mesh.scale.y]),[[10.5,8.2],[4.2,4.5]]);
 assert.deepEqual(a.locations.map(l=>l.id),bindings.map(l=>l.id));
 assert.equal(a.worldMutationAllowed,false);
 assert.deepEqual(a.principalCharacters,[]);
 assert.equal(JSON.stringify(bindings),before);
 a.dispose();
});

test('Shader derives bounded grazing reflectance from actual camera angle, not weather',()=>{
 const a=build(),shader=a.water.find(w=>w.kind==='swamp').material.fragmentShader;
 assert.match(shader,/else if\(uWetland>\.5\)/);
 assert.match(shader,/viewToEye=normalize\(cameraPosition-vWorld\)/);
 assert.match(shader,/viewIncidence=clamp\(abs\(viewToEye\.y\),0\.,1\.\)/);
 assert.match(shader,/grazingGain=\.035\+\.21\*pow\(1\.-viewIncidence,2\.\)/);
 assert.match(shader,/reflectedWater=mix\(contactTint,vec3\(\.31,\.41,\.37\),grazingGain\)/);
 assert.match(shader,/gl_FragColor=vec4\(reflectedWater\+lowSheen\+quietEddy\+rootSheen\+contactLight\+channelSheen,\.92\)/);
 assert.doesNotMatch(shader,/uniform float uStorm|uniform float uWeather|uniform float uRain/i);
 const gain=incidence=>.035+.21*Math.pow(1-Math.min(1,Math.max(0,incidence)),2);
 assert.ok(gain(.1)>gain(.5)&&gain(.5)>gain(.95));
 assert.ok(gain(0)<=.245001&&gain(1)>=.035&&gain(1)<gain(0));
 assert.equal(a.water.find(w=>w.kind==='pond').material.uniforms.uWetland.value,0);
 a.dispose();
});

test('Global-calm weather keeps ordinary water time; explicit pause holds phase',()=>{
 const before=JSON.stringify(bindings),a=build();
 const wetlands=a.water.filter(w=>['swamp','channel'].includes(w.kind));
 a.tick(3,{storm:0});
 for(const w of wetlands)assert.equal(w.material.uniforms.uTime.value,3);
 a.tick(7,{storm:0});
 for(const w of wetlands)assert.equal(w.material.uniforms.uTime.value,7);
 a.tick(11,{storm:0,paused:true});
 for(const w of wetlands)assert.equal(w.material.uniforms.uTime.value,7);
 a.tick(15,{storm:0});
 for(const w of wetlands)assert.equal(w.material.uniforms.uTime.value,15);
 assert.equal(JSON.stringify(bindings),before);
 a.dispose();
});
