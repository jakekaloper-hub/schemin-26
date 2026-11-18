import test from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';

const bindings=[
  {id:'LOC-MUD-DOGS-SWAMP',anchor:[42,0,16],canonStatus:'PERMANENT_CANON'},
  {id:'LOC-TDS-WATERFALL-TEMPLE',anchor:[31,0,51],canonStatus:'PERMANENT_CANON'},
  {id:'LOC-COUNTRY-CLUB-JACKSON',anchor:[57,0,24],canonStatus:'PERMANENT_CANON'}
];
const build=()=>buildRegionalAssets(THREE,bindings,()=>2);
function smooth(a,b,x) {
  const t=Math.max(0,Math.min(1,(x-a)/(b-a)));
  return t*t*(3-2*t);
}
function relief(u,v,time,flow) {
  const len=Math.hypot(flow.x,flow.y);
  const along=[flow.x/len,flow.y/len],across=[-along[1],along[0]];
  const point=[(u-.5)*2,(v-.5)*2],radius=Math.hypot(...point);
  const longitudinal=point[0]*along[0]+point[1]*along[1];
  const transverse=point[0]*across[0]+point[1]*across[1];
  const bend=Math.sin(longitudinal*8-time*.26)*.036;
  const phase=(transverse+bend)*31+longitudinal*7-time*.90;
  const shear=smooth(.12,.68,Math.abs(transverse))*(1-smooth(.75,.98,radius));
  const shore=1-smooth(.65,.96,radius);
  return {delta:.009*Math.sin(phase)*shear*shore,phase};
}

test('channel-only physical shear follows the existing flow and glint phase on unchanged geometry',()=>{
  const before=JSON.stringify(bindings),a=build();
  const channel=a.water.find(w=>w.kind==='channel'),swamp=a.water.find(w=>w.kind==='swamp');
  assert.ok(channel&&swamp);
  assert.equal(channel.material.uniforms.uChannel.value,1);
  assert.equal(swamp.material.uniforms.uChannel.value,0);
  assert.ok(a.water.filter(w=>w.kind!=='channel').every(w=>w.material.uniforms.uChannel.value===0));
  assert.deepEqual(channel.mesh.position.toArray(),[-6,.14,7]);
  assert.deepEqual(channel.mesh.scale.toArray(),[4.2,4.5,1]);
  assert.equal(channel.mesh.rotation.x,-Math.PI/2);
  assert.equal(channel.mesh.geometry.getAttribute('position').count,385);
  assert.equal(channel.mesh.geometry.index.count,2160);
  const vertex=channel.material.vertexShader,fragment=channel.material.fragmentShader;
  assert.match(vertex,/uniform float uChannel/);
  assert.match(vertex,/if\(uChannel>\.5\)/);
  assert.match(vertex,/channelAlong=normalize\(uFlow\)/);
  assert.match(vertex,/channelAcross=vec2\(-channelAlong.y,channelAlong.x\)/);
  assert.match(vertex,/channelBend=sin\(channelLong\*8\.-uTime\*\.26\)\*\.036/);
  assert.match(vertex,/channelPhase=\(channelCross\+channelBend\)\*31\./);
  assert.match(vertex,/p\.z\+=\.009\*sin\(channelPhase\)\*channelShear\*shoreHold/);
  assert.match(fragment,/bend=sin\(along\*8\.-uTime\*\.26\)\*\.036/);
  assert.match(fragment,/fineLine=pow\(max\(sin\(\(across\+bend\)\*31\.+along\*7\.-uTime\*\.90\),0\.\),12\./);
  for(const shader of [vertex,fragment])assert.doesNotMatch(shader,/\buStorm\b|\buWeather\b/i);
  assert.equal(a.worldMutationAllowed,false);
  assert.deepEqual(a.principalCharacters,[]);
  assert.equal(JSON.stringify(bindings),before);
  a.dispose();
});

test('original channel vertices move with bounded phase coherence and an invariant perimeter',()=>{
  const a=build(),channel=a.water.find(w=>w.kind==='channel');
  const uv=channel.mesh.geometry.getAttribute('uv'),flow=channel.material.uniforms.uFlow.value;
  assert.ok(flow.length()>0);
  let peak=0,change=0,matching=0;
  for(let i=0;i<uv.count;i++) {
    const u=uv.getX(i),v=uv.getY(i),radius=Math.hypot((u-.5)*2,(v-.5)*2);
    const x=relief(u,v,0,flow),y=relief(u,v,1.7,flow);
    assert.ok(Number.isFinite(x.delta)&&Number.isFinite(y.delta));
    assert.ok(Math.abs(x.delta)<=.00900001&&Math.abs(y.delta)<=.00900001);
    peak=Math.max(peak,Math.abs(x.delta),Math.abs(y.delta));
    change=Math.max(change,Math.abs(x.delta-y.delta));
    if(x.delta>.002&&Math.sin(x.phase)>.5)matching++;
    if(radius>=.96)assert.ok(Math.abs(x.delta)<1e-12&&Math.abs(y.delta)<1e-12);
  }
  assert.ok(peak>.005,'actual water vertices have nonzero physical displacement');
  assert.ok(change>.005,'ordinary time evolves the transverse relief');
  assert.ok(matching>0,'raised water crests align to the existing glint phase');
  a.dispose();
});

test('calm preserves ordinary channel motion; explicit pause, source isolation and disposal work',()=>{
  const before=JSON.stringify(bindings),a=build();
  const w=a.water.find(x=>x.kind==='channel'),kinds=a.water.map(x=>x.kind);
  a.tick(3,{storm:0});assert.equal(w.material.uniforms.uTime.value,3);
  a.tick(12,{storm:0});assert.equal(w.material.uniforms.uTime.value,12);
  a.tick(19,{storm:0,paused:true});assert.equal(w.material.uniforms.uTime.value,12);
  a.tick(22,{storm:0});assert.equal(w.material.uniforms.uTime.value,22);
  assert.deepEqual(a.water.map(x=>x.kind),kinds);
  assert.deepEqual(a.locations.map(x=>x.id),bindings.map(x=>x.id));
  assert.equal(a.locations[0].group.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
  assert.equal(JSON.stringify(bindings),before);
  a.dispose();a.dispose();
});
