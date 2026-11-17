import test from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';

const bindings=[
 {id:'LOC-TDS-WATERFALL-TEMPLE',anchor:[31,0,51],canonStatus:'PERMANENT_CANON',landmarks:['waterfall']},
 {id:'LOC-MUD-DOGS-SWAMP',anchor:[42,0,16],canonStatus:'PERMANENT_CANON'},
 {id:'LOC-COUNTRY-CLUB-JACKSON',anchor:[57,0,24],canonStatus:'PERMANENT_CANON'},
];
const build=()=>buildRegionalAssets(THREE,bindings,()=>2);

test('Temple existing receiving pool gets a bounded candidate plunge-only eddy and foam shader',()=>{
 const before=JSON.stringify(bindings),a=build();
 const plunge=a.water.find(w=>w.kind==='pool');
 assert.ok(plunge,'existing receiving pool');
 assert.equal(plunge.material.uniforms.uPlunge.value,1);
 assert.deepEqual(plunge.mesh.position.toArray(),[-5.8,.30,3]);
 assert.deepEqual(plunge.mesh.scale.toArray(),[3.8,2.8,1]);
 assert.equal(plunge.mesh.geometry.type,'CircleGeometry');
 assert.match(plunge.material.fragmentShader,/else if\(uPlunge>\.5\)/);
 assert.match(plunge.material.fragmentShader,/plungeCore/);
 assert.match(plunge.material.fragmentShader,/foam/);
 assert.match(plunge.material.fragmentShader,/boundary/);
 assert.match(plunge.material.fragmentShader,/smoothstep\(/);
 assert.equal(JSON.stringify(bindings),before);
 assert.equal(a.worldMutationAllowed,false);
 assert.deepEqual(a.principalCharacters,[]);
 a.dispose();
});

test('special plunge foam never redirects the river, wetland, pond, or falling sheet',()=>{
 const a=build();
 assert.equal(a.water.filter(w=>w.kind==='pool').length,1);
 for(const w of a.water.filter(w=>w.kind!=='pool'))assert.equal(w.material.uniforms.uPlunge?.value??0,0,`unexpected plunge selector on ${w.kind}`);
 assert.equal(a.water.filter(w=>w.kind==='waterfall').length,1);
 assert.equal(a.water.filter(w=>w.kind==='pond').length,1);
 assert.ok(a.water.some(w=>w.kind==='swamp')&&a.water.some(w=>w.kind==='channel'));
 assert.doesNotMatch(a.water.find(w=>w.kind==='pool').material.fragmentShader,/\buStorm\b|\buWeather\b/);
 a.dispose();
});

test('global calm does not stop plunge or river animation, but explicit pause does',()=>{
 const a=build();
 const motions=a.water.filter(w=>['pool','river','waterfall','swamp','channel'].includes(w.kind));
 a.tick(2,{storm:0});assert.ok(motions.every(w=>w.material.uniforms.uTime.value===2));
 a.tick(11,{storm:0});assert.ok(motions.every(w=>w.material.uniforms.uTime.value===11));
 a.tick(19,{storm:0,paused:true});assert.ok(motions.every(w=>w.material.uniforms.uTime.value===11));
 a.dispose();
});
