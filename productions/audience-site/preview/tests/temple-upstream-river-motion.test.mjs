import test from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';

const bindings=[
 {id:'LOC-TDS-WATERFALL-TEMPLE',anchor:[31,0,51],canonStatus:'PERMANENT_CANON',landmarks:['waterfall']},
 {id:'LOC-MUD-DOGS-SWAMP',anchor:[42,0,16],canonStatus:'PERMANENT_CANON',landmarks:['mud channels']},
 {id:'LOC-COUNTRY-CLUB-JACKSON',anchor:[57,0,24],canonStatus:'PERMANENT_CANON',landmarks:['water hazards']}
];
const build=()=>buildRegionalAssets(THREE,bindings,()=>2);
const displacement=(u,v,t)=>{
 const radius=Math.hypot((u-.5)*2,(v-.5)*2);
 const x=Math.max(0,Math.min(1,(radius-.68)/(.96-.68)));
 const smooth=x*x*(3-2*x),hold=1-smooth;
 return (.026*Math.sin(v*26-t*1.9+Math.sin(u*8)*.35)
   +.009*Math.sin((u+v)*35-t*2.2))*hold;
};

test('Temple existing upstream river alone receives tessellated interior with unchanged physical rim',()=>{
 const before=JSON.stringify(bindings),a=build(),river=a.water.find(w=>w.kind==='river');
 assert.ok(river);
 assert.equal(a.water.filter(w=>w.kind==='river').length,1);
 assert.deepEqual(river.mesh.position.toArray(),[-5.8,7.2,-1.5]);
 assert.deepEqual(river.mesh.scale.toArray(),[2.2,2.6,1]);
 assert.equal(river.mesh.rotation.x,-Math.PI/2);
 assert.equal(river.mesh.geometry.name,'Candidate Temple upstream river surface');
 const geo=river.mesh.geometry,pos=geo.getAttribute('position'),uv=geo.getAttribute('uv');
 assert.equal(pos.count,385);
 assert.equal(uv.count,pos.count);
 assert.equal(geo.index.count,2160);
 for(let i=0;i<pos.count;i++){
   assert.ok(Number.isFinite(pos.getX(i))&&Number.isFinite(pos.getY(i)));
   assert.ok(Math.hypot(pos.getX(i),pos.getY(i))<=1.000001);
   assert.equal(pos.getZ(i),0);
 }
 for(let i=1+7*48;i<pos.count;i++)assert.ok(Math.abs(Math.hypot(pos.getX(i),pos.getY(i))-1)<1e-6);
 for(const w of a.water.filter(w=>w.kind!=='river')){
   assert.equal(w.material.uniforms.uRiver?.value??0,0,'no river motion assigned to '+w.kind);
 }
 assert.equal(a.water.find(w=>w.kind==='pond').mesh.geometry.type,'CircleGeometry');
 assert.equal(a.water.find(w=>w.kind==='pool').mesh.geometry.name,'Candidate Temple plunge pool surface');
 assert.equal(a.water.find(w=>w.kind==='waterfall').mesh.geometry.type,'PlaneGeometry');
 assert.equal(JSON.stringify(bindings),before);
 assert.equal(a.worldMutationAllowed,false);
 assert.deepEqual(a.principalCharacters,[]);
 assert.equal(a.locations[0].group.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
 a.dispose();
});

test('existing Temple river vertex shader uses bounded, advancing interior displacement without moving its shoreline',()=>{
 const a=build(),river=a.water.find(w=>w.kind==='river');
 const shader=river.material.vertexShader,fragment=river.material.fragmentShader;
 assert.equal(river.material.uniforms.uRiver.value,1);
 assert.equal(river.material.uniforms.uWetland.value,0);
 assert.equal(river.material.uniforms.uFall.value,0);
 assert.match(shader,/uniform float uRiver;/);
 assert.match(shader,/if\(uRiver>\.5\)/);
 assert.match(shader,/p\.z\+=\(\.026\*riverPhase\+\.009\*riverCross\)\*riverHold/);
 assert.match(shader,/riverHold=1\.-smoothstep\(\.68,\.96,riverRadius\)/);
 assert.match(shader,/uTime\*1\.9/);
 assert.match(fragment,/else if\(uRiver>\.5\)/);
 assert.match(fragment,/runGlint/);
 assert.doesNotMatch(shader,/\buStorm\b|\buWeather\b/i);
 assert.doesNotMatch(fragment,/\buStorm\b|\buWeather\b/i);
 for(const t of [0,1.8,24])for(const [u,v] of [[0,.5],[1,.5],[.5,0],[.5,1],[.25,.25],[.5,.5],[.36,.62]]){
   const d=displacement(u,v,t);
   assert.ok(Math.abs(d)<=.03500001,'motion envelope bounded');
   if(u===0||u===1||v===0||v===1)assert.ok(Math.abs(d)<1e-12,'outer edge remains fixed');
 }
 assert.ok(Math.abs(displacement(.36,.62,0)-displacement(.36,.62,1.8))>.001,'interior vertex actually moves');
 a.dispose();
});

test('ordinary upstream river motion advances during synthetic global calm but stops on explicit pause',()=>{
 const a=build(),river=a.water.find(w=>w.kind==='river'),before=JSON.stringify(bindings);
 a.tick(3,{storm:0});assert.equal(river.material.uniforms.uTime.value,3);
 a.tick(9,{storm:0});assert.equal(river.material.uniforms.uTime.value,9);
 a.tick(21,{storm:0,paused:true});assert.equal(river.material.uniforms.uTime.value,9);
 a.tick(21,{storm:0});assert.equal(river.material.uniforms.uTime.value,21);
 assert.equal(JSON.stringify(bindings),before);
 a.dispose();
});
