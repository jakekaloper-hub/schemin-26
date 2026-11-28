import test from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';

const bindings=[
 {id:'LOC-MUD-DOGS-SWAMP',anchor:[42,0,16],canonStatus:'PERMANENT_CANON'},
 {id:'LOC-TDS-WATERFALL-TEMPLE',anchor:[32,0,29],canonStatus:'PERMANENT_CANON'},
 {id:'LOC-COUNTRY-CLUB-JACKSON',anchor:[57,0,24],canonStatus:'PERMANENT_CANON'},
];
const create=()=>buildRegionalAssets(THREE,bindings,()=>2);
const clamp=(x,min,max)=>Math.max(min,Math.min(max,x));
const normalize=(x,y,z)=>{
 const size=Math.hypot(x,y,z);
 return size>.00001?[x/size,y/size,z/size]:[0,1,0];
};
const response=(normal,bankFade=1)=>{
 const n=normalize(...normal),light=normalize(.30,.91,.27);
 const slope=clamp((1-clamp(Math.abs(n[1]),0,1))*14,0,.42);
 const facing=clamp(Math.abs(n.reduce((sum,v,i)=>sum+v*light[i],0)),0,1);
 return [.10,.15,.12].map(c=>c*slope*(.4+.6*facing)*bankFade);
};

test('Southern Wetlands response uses physically displaced world geometry only on inherited swamp and channel surfaces',()=>{
 const a=create(),wet=a.water.filter(w=>['swamp','channel'].includes(w.kind));
 assert.deepEqual(wet.map(w=>w.kind),['swamp','channel']);
 const shader=wet[0].material.fragmentShader;
 const start=shader.indexOf('}else if(uWetland>.5){'),end=shader.indexOf('}else if(uRiver>.5){');
 assert.ok(start>=0&&end>start);
 const scoped=shader.slice(start,end);
 assert.match(scoped,/wetlandFace=cross\(dFdx\(vWorld\),dFdy\(vWorld\)\)/);
 assert.match(scoped,/wetlandFaceSize>\.00001\?wetlandFace\/wetlandFaceSize:vec3\(0\.,1\.,0\.\)/);
 assert.match(scoped,/reliefSlope=clamp\(\(1\.-clamp\(abs\(wetlandNormal\.y\),0\.,1\.\)\)\*14\.,0\.,\.42\)/);
 assert.match(scoped,/reliefFacing=clamp\(abs\(dot\(wetlandNormal,normalize\(vec3\(\.30,\.91,\.27\)\)\)\),0\.,1\.\)/);
 assert.match(scoped,/reliefLight=vec3\(\.10,\.15,\.12\)\*reliefSlope\*\(\.4\+\.6\*reliefFacing\)\*bankFade/);
 assert.match(scoped,/contactTint\+=reliefLight/);
 assert.match(scoped,/gl_FragColor=vec4\(contactTint\+lowSheen\+quietEddy\+rootSheen\+contactLight\+channelSheen,\.92\)/);
 assert.doesNotMatch(scoped,/\buStorm\b|\buWeather\b|\buRain\b/);
 for(const w of wet)assert.equal(w.material.fragmentShader,shader);
 assert.equal(a.water.find(w=>w.kind==='pond').material.uniforms.uWetland.value,0);
 assert.equal(a.water.find(w=>w.kind==='river').material.uniforms.uWetland.value,0);
 a.dispose();
});

test('geometry-driven tint is finite, low-contrast, bounded, orientation-safe and fades at the inherited rim',()=>{
 const flat=response([0,1,0]),folded=response([.22,.97,.10]);
 assert.deepEqual(flat,[0,0,0],'flat water gets no fabricated relief light');
 assert.ok(folded.some(v=>v>.001),'actual geometric slope changes shade');
 for(const normal of [[0,1,0],[0,-1,0],[.13,.98,.25],[.5,.7,-.5],[0,0,0],[100,-100,1]]){
  const light=response(normal);
  assert.ok(light.every((v,i)=>Number.isFinite(v)&&v>=0&&v<=[.042,.063,.0504][i]+1e-8));
  assert.deepEqual(response(normal,0),[0,0,0],'shore mask cannot brighten beyond the water footprint');
  assert.ok(light.every((v,i)=>Math.abs(v-response(normal.map(n=>-n))[i])<1e-12),
   'two-sided surface orientation must not reverse the response');
 }
});

test('existing source water geometry and calm/pause clocks are unchanged; no added water mesh or canon writes',()=>{
 const before=JSON.stringify(bindings),a=create(),wet=a.water.filter(w=>['swamp','channel'].includes(w.kind));
 assert.deepEqual(a.locations.map(l=>l.id),bindings.map(p=>p.id));
 assert.equal(a.worldMutationAllowed,false);assert.deepEqual(a.principalCharacters,[]);
 for(const [w,x,z,rx,rz] of [[wet[0],0,0,10.5,8.2],[wet[1],-6,7,4.2,4.5]]){
  assert.equal(w.mesh.geometry.getAttribute('position').count,385);
  assert.equal(w.mesh.geometry.getIndex().count,2160);
  assert.deepEqual(w.mesh.position.toArray(),[x,w.kind==='swamp'?.12:.14,z]);
  assert.deepEqual([w.mesh.scale.x,w.mesh.scale.y],[rx,rz]);
  assert.equal(w.material.uniforms.uWetland.value,1);
  assert.equal(w.material.transparent,true);assert.equal(w.material.depthWrite,false);
 }
 a.tick(2,{storm:0});assert.deepEqual(wet.map(w=>w.material.uniforms.uTime.value),[2,2]);
 a.tick(7,{paused:true,storm:0});assert.deepEqual(wet.map(w=>w.material.uniforms.uTime.value),[2,2]);
 a.tick(8,{storm:0});assert.deepEqual(wet.map(w=>w.material.uniforms.uTime.value),[8,8]);
 assert.equal(JSON.stringify(bindings),before);
 a.dispose();a.dispose();
});
