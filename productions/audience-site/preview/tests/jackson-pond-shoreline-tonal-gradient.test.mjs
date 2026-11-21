import test from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';

// These source identities establish scope; they do not define bathymetry.
const bindings=[
  {id:'LOC-COUNTRY-CLUB-JACKSON',anchor:[57,0,24],canonStatus:'PERMANENT_CANON',landmarks:['clubhouse','water hazards']},
  {id:'LOC-TDS-WATERFALL-TEMPLE',anchor:[32,0,29],canonStatus:'PERMANENT_CANON',landmarks:['waterfall']},
  {id:'LOC-MUD-DOGS-SWAMP',anchor:[42,0,16],canonStatus:'PERMANENT_CANON',landmarks:['mud channels']}
];
const build=()=>buildRegionalAssets(THREE,bindings,()=>2);
const smooth=(lo,hi,x)=>{
  const t=Math.max(0,Math.min(1,(x-lo)/(hi-lo)));
  return t*t*(3-2*t);
};
const tone=(p,time,base)=>{
  // Numerical reconstruction of the bounded pond-only shader expression.
  const [x,y]=p,shoreRadius=Math.hypot(x,y);
  const shoreBand=smooth(.43,.96,shoreRadius);
  const shoreGrain=.5+.5*Math.sin(x*17.3+time*.14)*Math.sin(y*15.1-time*.11);
  const shoreMix=Math.max(0,Math.min(1,shoreBand*(.91+.09*shoreGrain)));
  const micro=.5+.5*Math.sin(x*7.3+Math.sin(y*8.2+time*.17));
  const brightness=.98+.04*micro;
  return [
    base.r*(.80+(1.17-.80)*shoreMix)*brightness,
    base.g*(.86+(1.12-.86)*shoreMix)*brightness,
    base.b*(.90+(.91-.90)*shoreMix)*brightness
  ];
};

test('Jackson tonal detail uses only its inherited circular pond, material, shoreline and Atlas identity',()=>{
  const source=JSON.stringify(bindings),a=build(),pond=a.water.find(w=>w.kind==='pond');
  assert.ok(pond);
  assert.equal(a.water.filter(w=>w.kind==='pond').length,1);
  assert.equal(pond.mesh.geometry.name,'Candidate Country Club pond surface');
  assert.deepEqual(pond.mesh.position.toArray(),[7,.06,6]);
  assert.deepEqual(pond.mesh.scale.toArray(),[3.8,2.3,1]);
  assert.equal(pond.mesh.rotation.x,-Math.PI/2);
  assert.equal(pond.mesh.geometry.getAttribute('position').count,321);
  assert.equal(pond.mesh.geometry.getIndex().count,1800);
  const p=pond.mesh.geometry.getAttribute('position');
  for(let i=1+7*40;i<p.count;i++)
    assert.ok(Math.abs(Math.hypot(p.getX(i),p.getY(i))-1)<1e-6,
      'the full original shoreline perimeter remains unchanged');
  assert.equal(pond.material.isShaderMaterial,true);
  assert.deepEqual(Object.keys(pond.material.uniforms).sort(),
    Object.keys(a.water.find(w=>w.kind==='swamp').material.uniforms).sort(),
    'existing material/uniform contract must not expand');
  assert.equal(pond.material.uniforms.uPond.value,1);
  assert.equal(a.worldMutationAllowed,false);
  assert.deepEqual(a.principalCharacters,[]);
  assert.equal(JSON.stringify(bindings),source);
  a.dispose();
});

test('new deep-to-bank tonal cue remains smooth, bounded, scene-only and ordinary-time-driven',()=>{
  const a=build(),pond=a.water.find(w=>w.kind==='pond');
  const frag=pond.material.fragmentShader,vert=pond.material.vertexShader;
  assert.match(frag,/float shoreRadius=length\(p\);/);
  assert.match(frag,/float shoreBand=smoothstep\(\.43,\.96,shoreRadius\);/);
  assert.match(frag,/float shoreGrain=\.5\+\.5\*sin\(p\.x\*17\.3\+uTime\*\.14\)/);
  assert.match(frag,/float shoreMix=clamp\(shoreBand\*\(\.91\+\.09\*shoreGrain\),0\.,1\.\);/);
  assert.match(frag,/vec3 pondTint=mix\(uColor\*vec3\(\.80,\.86,\.90\),/);
  assert.match(frag,/pondTint\*=\.98\+\.04\*micro;/);
  assert.match(frag,/pondReflectMix/);
  assert.match(frag,/bridgeMirrorMix/);
  assert.match(vert,/pondHold=1\.-smoothstep\(\.66,\.97,pondRadius\)/);
  assert.doesNotMatch(frag,/\buWeather\b|\buStorm\b|\buRain\b/i);
  assert.doesNotMatch(vert,/\buWeather\b|\buStorm\b|\buRain\b/i);
  const color=pond.material.uniforms.uColor.value;
  const deep=tone([0,0],0,color),nearBank=tone([.93,0],0,color);
  assert.ok(nearBank[1]>deep[1]*1.18,'shoreline is subtly lighter than the center');
  let changed=false;
  for(const time of [0,5,21,100]){
    for(const p of [[0,0],[.35,.17],[.64,.43],[.92,0],[1,0]]){
      const rgb=tone(p,time,color);
      assert.ok(rgb.every(Number.isFinite),'finite interpolated color');
      assert.ok(rgb[0]>=color.r*.78&&rgb[0]<=color.r*1.22);
      assert.ok(rgb[1]>=color.g*.84&&rgb[1]<=color.g*1.18);
      assert.ok(rgb[2]>=color.b*.88&&rgb[2]<=color.b*.94);
    }
    if(Math.abs(tone([.64,.43],time,color)[0]-tone([.64,.43],0,color)[0])>.00002)changed=true;
  }
  assert.ok(changed,'shoreline variation advances on ordinary water time');
  assert.equal(a.water.find(w=>w.kind==='river').material.uniforms.uPond.value,0);
  assert.equal(a.water.find(w=>w.kind==='swamp').material.uniforms.uPond.value,0);
  a.dispose();
});

test('El Niño global WEATHER calm preserves ordinary pond water clock; explicit pause/dispose still govern it',()=>{
  const source=JSON.stringify(bindings),a=build(),pond=a.water.find(w=>w.kind==='pond');
  let disposeCount=0;
  pond.material.addEventListener('dispose',()=>disposeCount++);
  a.tick(3,{storm:0});assert.equal(pond.material.uniforms.uTime.value,3);
  a.tick(11,{storm:0});assert.equal(pond.material.uniforms.uTime.value,11);
  assert.equal(a.water.find(w=>w.kind==='river').material.uniforms.uTime.value,11);
  assert.equal(a.water.find(w=>w.kind==='swamp').material.uniforms.uTime.value,11);
  a.tick(20,{storm:0,paused:true});assert.equal(pond.material.uniforms.uTime.value,11);
  a.tick(20,{storm:0});assert.equal(pond.material.uniforms.uTime.value,20);
  assert.equal(JSON.stringify(bindings),source);
  a.dispose();a.dispose();
  assert.equal(disposeCount,1,'material disposed exactly once');
});
