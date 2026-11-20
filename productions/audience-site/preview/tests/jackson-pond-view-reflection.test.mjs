import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';

const atlas=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const ids=['LOC-TDS-WATERFALL-TEMPLE','LOC-MUD-DOGS-SWAMP','LOC-COUNTRY-CLUB-JACKSON'];
const bindings=ids.map(id=>{
  const place=atlas.locations.find(p=>p.id===id);
  assert.ok(place,'missing canonical place '+id);
  return {id,anchor:[place.abstract_position[0],0,place.abstract_position[1]],
    canonStatus:place.canon_status,landmarks:place.persistent_landmarks};
});
const build=()=>buildRegionalAssets(THREE,bindings,()=>2);
const pond=a=>a.water.find(w=>w.kind==='pond');
const club=a=>a.locations.find(l=>l.id==='LOC-COUNTRY-CLUB-JACKSON').group;
const smooth=(lo,hi,value)=>{
  const p=Math.max(0,Math.min(1,(value-lo)/(hi-lo)));
  return p*p*(3-2*p);
};
const gain=(incidence,radius)=>(.035+.19*(1-Math.max(0,Math.min(1,incidence)))**2)
  *(1-smooth(.68,.95,radius));

test('Jackson pond keeps source location, inherited geometry and unresolved Week 3 history',()=>{
  const initialAtlas=JSON.stringify(atlas),initialInputs=JSON.stringify(bindings),a=build(),p=pond(a);
  const arch=club(a).getObjectByName('Candidate Week 9 pond-side stone arch');
  assert.deepEqual(a.locations.map(x=>x.id),ids);
  assert.equal(atlas.locations.find(x=>x.id===ids[2]).canon_status,'PERMANENT_CANON');
  assert.ok(atlas.locations.find(x=>x.id===ids[2]).current_state.some(x=>x.includes('chili contamination')));
  assert.ok(atlas.locations.find(x=>x.id===ids[2]).current_state.some(x=>x.includes('cleanup state')));
  assert.deepEqual(p.mesh.position.toArray(),[7,.06,6]);
  assert.deepEqual(p.mesh.scale.toArray(),[3.8,2.3,1]);
  assert.equal(p.mesh.rotation.x,-Math.PI/2);
  assert.equal(p.mesh.geometry.getAttribute('position').count,321);
  assert.equal(p.mesh.geometry.index.count,1800);
  assert.equal(a.water.filter(w=>w.kind==='pond').length,1);
  assert.deepEqual(arch.children.filter(o=>o.userData.bridgePart==='stone-arch').map(o=>o.position.x),[-.88,.71]);
  assert.equal(arch.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
  assert.equal(arch.userData.navigable,false);
  assert.deepEqual(arch.userData.routeIds,[]);
  assert.equal(club(a).userData.stateResolution,'UNRESOLVED_NOT_CURRENT_STATE');
  assert.equal(a.worldMutationAllowed,false);assert.deepEqual(a.principalCharacters,[]);
  assert.equal(JSON.stringify(atlas),initialAtlas);
  assert.equal(JSON.stringify(bindings),initialInputs);
  a.dispose();
});

test('existing displaced pond normals drive bounded grazing-reflection without new weather or geometry',()=>{
  const a=build(),p=pond(a),frag=p.material.fragmentShader;
  assert.equal(p.material.isShaderMaterial,true);
  assert.equal(p.material.uniforms.uPond.value,1);
  assert.equal(p.material.uniforms.uFlow.value.length(),0);
  assert.ok(frag.includes('vec3 pondCross=cross(dFdx(vWorld),dFdy(vWorld));'));
  assert.ok(frag.includes('vec3 pondEye=normalize(cameraPosition-vWorld);'));
  assert.ok(frag.includes('float pondGrazing=pow(1.-clamp(abs(dot(pondNormal,pondEye)),0.,1.),2.);'));
  assert.ok(frag.includes('float pondReflectMix=(.035+.19*pondGrazing)*bank;'));
  assert.ok(frag.includes('pondTint=mix(pondTint,vec3(.40,.52,.48),pondReflectMix);'));
  assert.ok(frag.includes('pondTint+vec3(.09,.13,.11)*ripple+pondLight+pondBridgeLight'));
  assert.doesNotMatch(frag,/uniform float uStorm|uniform float uWeather|uniform float uRain/);
  for(const r of [0,.2,.50,.68,.76,.95,1])for(const incidence of [0,.1,.45,.9,1]){
    const value=gain(incidence,r);
    assert.ok(Number.isFinite(value)&&value>=0&&value<=.2250000001);
    if(r>=.95)assert.equal(value,0,'fixed bank must receive no new reflection');
  }
  assert.ok(gain(.1,.25)>gain(.8,.25),'grazing exceeds overhead');
  assert.ok(gain(.1,.25)>gain(.1,.82),'interior exceeds bank');
  assert.ok(gain(.2,.40)>.05,'visible nonzero interior reflectance');
  for(const w of a.water.filter(w=>w.kind!=='pond'))assert.equal(w.material.uniforms.uPond?.value??0,0);
  a.dispose();
});

test('El Nino calm retains ordinary water animation; explicit pause holds; disposal only once',()=>{
  const before=JSON.stringify(bindings),a=build(),p=pond(a);
  const waters=a.water.filter(w=>['pond','swamp','channel','river','waterfall','pool'].includes(w.kind));
  assert.equal(waters.length,6);
  a.tick(3,{globalCalm:true,storm:0});assert.ok(waters.every(w=>w.material.uniforms.uTime.value===3));
  a.tick(9,{globalCalm:true,storm:0});assert.ok(waters.every(w=>w.material.uniforms.uTime.value===9));
  a.tick(15,{globalCalm:true,storm:7,paused:true});assert.ok(waters.every(w=>w.material.uniforms.uTime.value===9));
  a.tick(19,{globalCalm:true,storm:0});assert.ok(waters.every(w=>w.material.uniforms.uTime.value===19));
  let mats=0,geos=0;
  p.material.addEventListener('dispose',()=>mats++);
  p.mesh.geometry.addEventListener('dispose',()=>geos++);
  a.dispose();a.dispose();a.tick(30);
  assert.equal(mats,1);assert.equal(geos,1);
  assert.equal(JSON.stringify(bindings),before);
});
