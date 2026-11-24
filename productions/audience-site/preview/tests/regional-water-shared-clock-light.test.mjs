import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';

const bindings=[
 {id:'LOC-COUNTRY-CLUB-JACKSON',anchor:[57,0,24],canonStatus:'PERMANENT_CANON',landmarks:['water hazards','clubhouse']},
 {id:'LOC-MUD-DOGS-SWAMP',anchor:[42,0,16],canonStatus:'PERMANENT_CANON',landmarks:['mud channels']},
 {id:'LOC-TDS-WATERFALL-TEMPLE',anchor:[32,0,29],canonStatus:'PERMANENT_CANON',landmarks:['waterfall']}
];
test('every inherited regional water material has base-water-equivalent RGB-only light response',()=>{
 const source=JSON.stringify(bindings),a=buildRegionalAssets(THREE,bindings,()=>2);
 try {
  assert.deepEqual([...new Set(a.water.map(w=>w.kind))].sort(),['channel','landing-ripple','pond','pool','river','swamp','waterfall']);
  for(const {material:m} of a.water){
   assert.equal(m.uniforms.uLightLevel.value,1);
   assert.match(m.fragmentShader,/uniform float uLightLevel;/);
   assert.match(m.fragmentShader,/gl_FragColor\.rgb\*=\.45\+\.55\*clamp\(uLightLevel,0\.,1\.\);/);
   assert.doesNotMatch(m.vertexShader,/uLightLevel/);
   assert.doesNotMatch(m.fragmentShader,/\buStorm\b|\buWeather\b/);
   assert.equal(m.transparent,true);assert.equal(m.depthWrite,false);
  }
  a.tick(2,{storm:0});for(const w of a.water)w.material.uniforms.uLightLevel.value=.2;
  a.tick(8,{storm:0});for(const w of a.water){assert.equal(w.material.uniforms.uTime.value,8);assert.equal(w.material.uniforms.uLightLevel.value,.2);}
  a.tick(20,{paused:true});for(const w of a.water)assert.equal(w.material.uniforms.uTime.value,8);
  assert.equal(JSON.stringify(bindings),source);assert.equal(a.worldMutationAllowed,false);
 }finally{a.dispose();}
});
test('primary renderer binds existing shared clock to regional water outside the motion gate',()=>{
 const source=readFileSync(new URL('../three-world.mjs',import.meta.url),'utf8');
 assert.match(source,/if\(!paused\)lastTime=time;regional\.tick\(lastTime,\{paused\}\);/);
 assert.match(source,/for\(const w of regional\.water\)w\.material\.uniforms\.uLightLevel\.value=strength;/);
 assert.match(source,/col\*=\.45\+\.55\*uStrength;/);
});
