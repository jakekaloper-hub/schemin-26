import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';

const source=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const ids=['LOC-TDS-WATERFALL-TEMPLE','LOC-MUD-DOGS-SWAMP','LOC-COUNTRY-CLUB-JACKSON'];
const bindings=ids.map(id=>{
  const place=source.locations.find(p=>p.id===id);
  return {id,anchor:[place.abstract_position[0],0,place.abstract_position[1]],
    canonStatus:place.canon_status,landmarks:place.persistent_landmarks};
});
const before=JSON.stringify(bindings);
const build=()=>buildRegionalAssets(THREE,bindings,()=>2);
const club=a=>a.locations.find(l=>l.id==='LOC-COUNTRY-CLUB-JACKSON').group;
const pond=a=>a.water.find(w=>w.kind==='pond');
function smooth(a,b,x){
  const q=Math.max(0,Math.min(1,(x-a)/(b-a)));
  return q*q*(3-2*q);
}
function bridgeOffset(u,v,t){
  const x=(u-.5)*2,y=(v-.5)*2,r=Math.hypot(x,y);
  const bank=1-smooth(.66,.97,r);
  const dA=Math.hypot(x-(-.88/3.8),(y-0)*1.28);
  const dB=Math.hypot(x-(.71/3.8),(y-0)*1.28);
  const holdA=1-smooth(.08,.39,dA),holdB=1-smooth(.08,.39,dB);
  return .0035*(Math.sin(dA*37-t*2.05)*holdA+
    Math.sin(dB*33-t*1.82+1.2)*holdB)*bank;
}
function bridgeLight(u,v,t){
  const x=(u-.5)*2,y=(v-.5)*2;
  const dA=Math.hypot(x+(.88/3.8),y*1.28);
  const dB=Math.hypot(x-(.71/3.8),y*1.28);
  const crestA=(1-smooth(.08,.43,dA))*Math.pow(Math.max(Math.sin(dA*37-t*2.05),0),10);
  const crestB=(1-smooth(.08,.43,dB))*Math.pow(Math.max(Math.sin(dB*33-t*1.82+1.2),0),10);
  const breakup=.5+.5*Math.sin(y*27+t*.68+x*11);
  const bank=1-smooth(.68,.95,Math.hypot(x,y));
  return Math.min(1,Math.max(0,(crestA+crestB)*breakup*bank));
}

test('existing Jackson arch bases anchor two pond-local contact sites without an Atlas route or topology change',()=>{
  const canonical=source.locations.find(p=>p.id===ids[2]),a=build(),p=pond(a);
  const b=club(a).getObjectByName('Candidate Week 9 pond-side stone arch');
  assert.equal(canonical.canon_status,'PERMANENT_CANON');
  assert.ok(canonical.persistent_landmarks.includes('water hazards'));
  assert.ok(canonical.current_state.some(s=>s.includes('chili contamination')));
  assert.ok(canonical.current_state.some(s=>s.includes('cleanup state')));
  assert.deepEqual(a.locations.map(l=>l.id),ids);
  assert.equal(a.water.filter(w=>w.kind==='pond').length,1);
  assert.deepEqual(p.mesh.position.toArray(),[7,.06,6]);
  assert.deepEqual(p.mesh.scale.toArray(),[3.8,2.3,1]);
  assert.equal(p.mesh.geometry.getAttribute('position').count,321);
  assert.equal(p.mesh.geometry.index.count,1800);
  assert.equal(p.material.uniforms.uFlow.value.length(),0);
  assert.equal(b.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
  assert.equal(b.userData.navigable,false);
  assert.deepEqual(b.userData.routeIds,[]);
  const arches=b.children.filter(o=>o.userData.bridgePart==='stone-arch');
  assert.deepEqual(arches.map(o=>o.position.x),[-.88,.71]);
  for(const arch of arches){
    const px=arch.position.x/p.mesh.scale.x;
    assert.ok(Math.abs(px)<.24);
    assert.ok(Math.abs(bridgeOffset(.5+px/2,.5,1))<=.007000001);
  }
  assert.equal(a.worldMutationAllowed,false);
  assert.deepEqual(a.principalCharacters,[]);
  assert.equal(JSON.stringify(bindings),before);a.dispose();
});

test('actual pond shader adds bounded, interior-only physically displaced arch contact and restrained light',()=>{
  const a=build(),p=pond(a),vs=p.material.vertexShader,fs=p.material.fragmentShader;
  assert.match(vs,/bridgeA=vec2\(-\.88\/3\.8,0\.\)/);
  assert.match(vs,/bridgeB=vec2\(\.71\/3\.8,0\.\)/);
  assert.match(vs,/p\.z\+=\.0035\*\(bridgePulseA\*bridgeHoldA\+bridgePulseB\*bridgeHoldB\)\*pondHold/);
  assert.match(fs,/bridgeContact=clamp\(\(bridgeCrestA\+bridgeCrestB\)\*bridgeBreak\*bank,0\.,1\.\)/);
  assert.match(fs,/pondBridgeLight=vec3\(\.042,\.061,\.052\)\*bridgeContact/);
  assert.match(fs,/pondTint\+vec3\(\.09,\.13,\.11\)\*ripple\+pondLight\+pondBridgeLight/);
  assert.doesNotMatch(vs,/\buWeather\b|\buStorm\b/);
  let moving=false,lit=false;
  for(let ix=0;ix<=24;ix++)for(let iy=0;iy<=24;iy++){
    const u=ix/24,v=iy/24;
    for(const t of [0,1.7,5.3,19]){
      const d=bridgeOffset(u,v,t),l=bridgeLight(u,v,t);
      assert.ok(Number.isFinite(d)&&Number.isFinite(l));
      assert.ok(Math.abs(d)<=.007000001,'two local wavelets are bounded');
      assert.ok(l>=0&&l<=1,'bounded broken water light');
      if(t===1.7&&Math.abs(d-bridgeOffset(u,v,0))>.0003)moving=true;
      if(l>.2)lit=true;
      if(u===0||u===1||v===0||v===1)assert.ok(Math.abs(d)<1e-12,'inherited bank fixed');
    }
  }
  assert.ok(moving,'contact motion advances with ordinary pond time');
  assert.ok(lit,'actual broken bridge-contact light, not a dead formula');
  for(const other of a.water.filter(w=>w.kind!=='pond')){
    assert.equal(other.material.uniforms.uPond?.value??0,0);
    assert.equal(other.material.fragmentShader.includes('pondBridgeLight'),true,'shared shader source but pond-only branch');
  }
  a.dispose();
});

test('pond, river and waterfall keep moving in global calm, explicit pause freezes, disposal once only',()=>{
  const a=build(),p=pond(a),geo=p.mesh.geometry,mat=p.material;
  let geoDisposals=0,matDisposals=0;
  geo.addEventListener('dispose',()=>geoDisposals++);
  mat.addEventListener('dispose',()=>matDisposals++);
  a.tick(1.7,{globalCalm:true,storm:0});
  assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===1.7));
  a.tick(5.3,{globalCalm:true,storm:0});
  assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===5.3));
  a.tick(9,{globalCalm:true,storm:6,paused:true});
  assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===5.3));
  a.tick(11,{globalCalm:true,storm:0});
  assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===11));
  assert.equal(club(a).userData.stateResolution,'UNRESOLVED_NOT_CURRENT_STATE');
  a.dispose();a.dispose();a.tick(12);
  assert.equal(geoDisposals,1);assert.equal(matDisposals,1);
  assert.equal(JSON.stringify(bindings),before);
});
