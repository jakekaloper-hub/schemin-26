import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';

const atlas=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const ids=['LOC-TDS-WATERFALL-TEMPLE','LOC-MUD-DOGS-SWAMP','LOC-COUNTRY-CLUB-JACKSON'];
const bindings=ids.map(id=>{
  const source=atlas.locations.find(p=>p.id===id);
  assert.ok(source,'missing authoritative Atlas location '+id);
  return {id,anchor:[source.abstract_position[0],0,source.abstract_position[1]],
    canonStatus:source.canon_status,landmarks:source.persistent_landmarks};
});
const make=()=>buildRegionalAssets(THREE,bindings,()=>2);
const pond=a=>a.water.find(w=>w.kind==='pond');
const smooth=(min,max,v)=>{
  const t=Math.max(0,Math.min(1,(v-min)/(max-min)));
  return t*t*(3-2*t);
};
// The exact bounded fragment optics, mirrored in JavaScript for numeric edge tests.
const mirror=(x,y,grazing,time)=>{
  const bridgeA=-.88/3.8,bridgeB=.71/3.8;
  const bank=1-smooth(.68,.95,Math.hypot(x,y));
  const stripA=1-smooth(.012,.089,Math.abs(x-bridgeA+.012*Math.sin(y*27-time*.46)));
  const stripB=1-smooth(.012,.089,Math.abs(x-bridgeB+.012*Math.sin(y*24-time*.39+1.3)));
  const len=1-smooth(.38,.83,Math.abs(y));
  const breakup=.48+.52*(.5+.5*Math.sin(y*42-time*.84+x*12));
  return Math.max(0,Math.min(.17,Math.max(stripA,stripB)*len*breakup
    *smooth(.02,.5,grazing)*bank*.17));
};

test('Jackson bridge mirror stays source-bound, unresolved, and inside inherited pond',()=>{
  const originalAtlas=JSON.stringify(atlas),originalBindings=JSON.stringify(bindings);
  const a=make(),p=pond(a),g=a.locations.find(l=>l.id===ids[2]).group;
  const arch=g.getObjectByName('Candidate Week 9 pond-side stone arch');
  const state=atlas.locations.find(l=>l.id===ids[2]).current_state;
  assert.deepEqual(a.locations.map(l=>l.id),ids);
  assert.ok(state.some(s=>s.includes('chili contamination')));
  assert.ok(state.some(s=>s.includes('cleanup state')));
  assert.deepEqual(p.mesh.position.toArray(),[7,.06,6]);
  assert.deepEqual(p.mesh.scale.toArray(),[3.8,2.3,1]);
  assert.equal(p.mesh.geometry.getAttribute('position').count,321);
  assert.equal(p.mesh.geometry.index.count,1800);
  assert.deepEqual(arch.children.filter(o=>o.userData.bridgePart==='stone-arch')
    .map(o=>o.position.x),[-.88,.71]);
  assert.equal(g.userData.stateResolution,'UNRESOLVED_NOT_CURRENT_STATE');
  assert.equal(a.water.filter(w=>w.kind==='pond').length,1);
  assert.equal(a.worldMutationAllowed,false);
  assert.deepEqual(a.principalCharacters,[]);
  assert.equal(JSON.stringify(atlas),originalAtlas);
  assert.equal(JSON.stringify(bindings),originalBindings);
  a.dispose();
});

test('existing pond material has two time-broken camera-dependent, bounded bridge mirrors',()=>{
  const a=make(),p=pond(a),f=p.material.fragmentShader;
  assert.equal(p.material.uniforms.uPond.value,1);
  assert.ok(f.includes('float bridgeMirrorA=1.-smoothstep(.012,.089,'));
  assert.ok(f.includes('float bridgeMirrorB=1.-smoothstep(.012,.089,'));
  assert.ok(f.includes('float bridgeMirrorLength=1.-smoothstep(.38,.83,abs(p.y));'));
  assert.ok(f.includes('float bridgeMirrorGrazing=smoothstep(.02,.5,pondGrazing);'));
  assert.ok(f.includes('float bridgeMirrorMix=clamp(max(bridgeMirrorA,bridgeMirrorB)'));
  assert.ok(f.includes('pondTint=mix(pondTint,vec3(.17,.23,.20),bridgeMirrorMix);'));
  assert.ok(f.includes('pondTint+vec3(.09,.13,.11)*ripple+pondLight+pondBridgeLight'));
  assert.doesNotMatch(f,/uniform float uStorm|uniform float uWeather|uniform float uRain/);
  assert.equal(p.material.uniforms.uFlow.value.length(),0);
  for(const w of a.water.filter(w=>w!==p))assert.equal(w.material.uniforms.uPond?.value??0,0);
  for(const x of [-1,-.5,-.88/3.8,0,.71/3.8,.5,1])
    for(const y of [-1,-.67,-.2,0,.2,.67,1])
      for(const angle of [0,.15,.5,.9,1])
        for(const t of [0,1.9,8.5]){
          const v=mirror(x,y,angle,t);
          assert.ok(Number.isFinite(v)&&v>=0&&v<=.17+1e-12);
          assert.equal(v,mirror(x,y,angle,t),'determinism');
          if(Math.hypot(x,y)>=.95||angle===0)assert.equal(v,0,'bank/overhead suppression');
        }
  const left=mirror(-.88/3.8,.12,.9,2),right=mirror(.71/3.8,.12,.9,2);
  assert.ok(left>.02 && right>.02,'both existing masonry faces appear');
  assert.ok(mirror(-.88/3.8,.12,.9,2)>mirror(-.88/3.8,.12,.03,2));
  assert.equal(mirror(.84,0,1,2),0,'no unrelated third reflective anchor');
  assert.notEqual(mirror(-.88/3.8,.12,.9,2),mirror(-.88/3.8,.12,.9,4),'ordinary motion');
  a.dispose();
});

test('El Nino global calm still advances every ordinary water clock, pause and disposal remain bounded',()=>{
  const initial=JSON.stringify(bindings),a=make(),p=pond(a);
  const all=a.water.filter(w=>['swamp','channel','river','waterfall','pool','pond'].includes(w.kind));
  assert.equal(all.length,6);
  a.tick(4,{globalCalm:true,storm:0});
  assert.ok(all.every(w=>w.material.uniforms.uTime.value===4));
  a.tick(9,{globalCalm:true,storm:0});
  assert.ok(all.every(w=>w.material.uniforms.uTime.value===9));
  a.tick(15,{paused:true,globalCalm:true,storm:8});
  assert.ok(all.every(w=>w.material.uniforms.uTime.value===9));
  let disposeMat=0,disposeGeo=0;
  p.material.addEventListener('dispose',()=>disposeMat++);
  p.mesh.geometry.addEventListener('dispose',()=>disposeGeo++);
  a.dispose();a.dispose();a.tick(20);
  assert.equal(disposeMat,1);assert.equal(disposeGeo,1);
  assert.equal(JSON.stringify(bindings),initial);
});
