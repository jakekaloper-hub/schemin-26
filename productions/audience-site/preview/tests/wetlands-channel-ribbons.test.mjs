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

test('Source-bound moving channel ribbons affect the existing channel surface alone',()=>{
 const before=JSON.stringify(bindings),a=build();
 const channel=a.water.find(w=>w.kind==='channel');
 const swamp=a.water.find(w=>w.kind==='swamp');
 assert.ok(channel&&swamp);
 assert.equal(channel.material.uniforms.uChannel.value,1);
 assert.equal(swamp.material.uniforms.uChannel.value,0);
 assert.ok(a.water.filter(w=>w.kind!=='channel')
   .every(w=>(w.material.uniforms.uChannel?.value??0)===0));
 assert.equal(channel.mesh.geometry.getAttribute('position').count,385);
 assert.equal(channel.mesh.geometry.index.count,2160);
 assert.equal(channel.mesh.scale.x,4.2);
 assert.equal(channel.mesh.scale.y,4.5);
 assert.equal(channel.material.depthWrite,false);
 assert.equal(a.worldMutationAllowed,false);
 assert.deepEqual(a.principalCharacters,[]);
 assert.equal(JSON.stringify(bindings),before);
 a.dispose();
});

test('Channel glints follow existing illustrative flow and taper inside original UV bank',()=>{
 const a=build(),channel=a.water.find(w=>w.kind==='channel');
 const shader=channel.material.fragmentShader;
 assert.match(shader,/uniform float uChannel/);
 assert.match(shader,/if\(uChannel>\.5\)/);
 assert.match(shader,/vec2 alongAxis=normalize\(uFlow\)/);
 assert.match(shader,/vec2 crossAxis=vec2\(-alongAxis\.y,alongAxis\.x\)/);
 assert.match(shader,/fineLine=pow\(max\(sin\(/);
 assert.match(shader,/channelRibbons=fineLine\*smoothstep/);
 assert.match(shader,/interior=1\.-smoothstep\(\.70,\.98,length\(p\)\)/);
 assert.match(shader,/contactLight\+channelSheen/);
 assert.doesNotMatch(shader,/storm|weather/i);
 assert.ok(channel.material.uniforms.uFlow.value.length()>0);
 assert.equal(channel.mesh.geometry.getAttribute('position').count,385);
 a.dispose();
});

test('Channel surface keeps moving in El Nino global calm, freezes only when paused',()=>{
 const before=JSON.stringify(bindings),a=build();
 const channel=a.water.find(w=>w.kind==='channel');
 a.tick(3,{storm:0});
 assert.equal(channel.material.uniforms.uTime.value,3);
 a.tick(11,{storm:0});
 assert.equal(channel.material.uniforms.uTime.value,11);
 a.tick(18,{storm:0,paused:true});
 assert.equal(channel.material.uniforms.uTime.value,11);
 a.tick(23,{storm:0});
 assert.equal(channel.material.uniforms.uTime.value,23);
 assert.deepEqual(a.locations.map(l=>l.id),bindings.map(l=>l.id));
 assert.equal(JSON.stringify(bindings),before);
 a.dispose();
});
