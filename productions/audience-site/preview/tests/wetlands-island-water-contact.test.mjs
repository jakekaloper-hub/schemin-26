import test from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from '../vendor/three.module.js';
import {buildRegionalAssets} from '../regional-assets.mjs';

const bindings=[
  {id:'LOC-MUD-DOGS-SWAMP',anchor:[42,0,16],canonStatus:'PERMANENT_CANON'},
  {id:'LOC-TDS-WATERFALL-TEMPLE',anchor:[31,0,51],canonStatus:'PERMANENT_CANON'},
  {id:'LOC-COUNTRY-CLUB-JACKSON',anchor:[57,0,24],canonStatus:'PERMANENT_CANON'},
];
const islands=[[1,.1,1,4,1.2,3],[-6,.1,-3,3,.9,2.7],
  [6,.2,-4,3.5,1,2.8],[-4,.1,5,2.7,.8,2]];
const create=()=>buildRegionalAssets(THREE,bindings,()=>2);
const smooth=(a,b,x)=>{const t=Math.max(0,Math.min(1,(x-a)/(b-a)));return t*t*(3-2*t);};
function lapping(u,v,time,sites){
  let lap=0;
  for(const site of sites){
    const dx=(u-site.x)/site.z,dy=(v-site.y)/site.w;
    const r=Math.hypot(dx,dy),band=smooth(.86,.97,r)*(1-smooth(1.04,1.22,r));
    const phase=r*24-time*1.85+Math.atan2(dy,dx)*2;
    lap=Math.max(lap,band*Math.max(0,Math.sin(phase))**4);
  }
  const hold=1-smooth(.65,.96,Math.hypot((u-.5)*2,(v-.5)*2));
  return .007*lap*hold;
}

test('exactly four existing relief island ellipses project into the original rotated swamp disk',()=>{
  const before=JSON.stringify(bindings),a=create();
  const w=a.water.find(x=>x.kind==='swamp'),u=w.material.uniforms;
  const relief=a.locations[0].group.getObjectByName('Candidate wetland raised-ground relief');
  assert.ok(relief);assert.equal(relief.userData.islandCount,4);
  assert.equal(u.uIslandSiteCount.value,4);
  assert.equal(u.uIslandSites.value.length,4);
  assert.equal(w.mesh.geometry.getAttribute('position').count,385);
  assert.equal(w.mesh.geometry.index.count,2160);
  assert.equal(w.mesh.rotation.x,-Math.PI/2);
  assert.deepEqual(w.mesh.position.toArray(),[0,.12,0]);
  assert.deepEqual(w.mesh.scale.toArray(),[10.5,8.2,1]);
  const sites=u.uIslandSites.value;
  sites.forEach((s,i)=>{
    const [x,,z,sx,,sz]=islands[i];
    assert.ok(Math.abs((s.x-.5)*21-x)<1e-10);
    assert.ok(Math.abs((.5-s.y)*16.4-z)<1e-10,
      'negative texture V matches the rotated swamp plane, including both Z signs');
    assert.ok(Math.abs(s.z*21-sx*.955)<1e-10);
    assert.ok(Math.abs(s.w*16.4-sz*.955)<1e-10);
  });
  for(const other of a.water.filter(x=>x.kind!=='swamp')){
    assert.equal(other.material.uniforms.uIslandSiteCount?.value??0,0,
      'other water kinds have no island-contact authority: '+other.kind);
  }
  assert.deepEqual(a.locations.map(x=>x.id),bindings.map(x=>x.id));
  assert.equal(JSON.stringify(bindings),before);
  assert.equal(a.worldMutationAllowed,false);assert.deepEqual(a.principalCharacters,[]);
  a.dispose();
});

test('existing water vertices carry small phase-synchronized island contact, with fixed outer boundary',()=>{
  const a=create(),w=a.water.find(x=>x.kind==='swamp');
  const vertex=w.material.vertexShader,fragment=w.material.fragmentShader;
  assert.match(vertex,/uniform float uIslandSiteCount;uniform vec4 uIslandSites\[4\]/);
  assert.match(fragment,/uniform float uIslandSiteCount;uniform vec4 uIslandSites\[4\]/);
  for(const shader of [vertex,fragment]){
    assert.match(shader,/for\(int i=0;i<4;i\+\+\)/);
    assert.match(shader,/contactBand=smoothstep\(\.86,\.97,islandRadius\)/);
    assert.match(shader,/islandRadius\*24\.-uTime\*1\.85\+atan\(delta\.y,delta\.x\)\*2\./);
    assert.doesNotMatch(shader,/\buStorm\b|\buWeather\b/i);
  }
  assert.match(vertex,/p\.z\+=\.007\*islandLap\*shoreHold/);
  assert.match(fragment,/islandSheen=vec3\(\.095,\.13,\.10\)\*\(islandLap\*\.30\*bankFade\)/);
  const uv=w.mesh.geometry.getAttribute('uv'),sites=w.material.uniforms.uIslandSites.value;
  let highest=0,delta=0;
  for(let i=0;i<uv.count;i++){
    const u=uv.getX(i),v=uv.getY(i);
    const a0=lapping(u,v,0,sites),a1=lapping(u,v,1.37,sites);
    assert.ok(Number.isFinite(a0)&&Number.isFinite(a1));
    assert.ok(a0>=0&&a0<=.00700001&&a1>=0&&a1<=.00700001);
    highest=Math.max(highest,a0,a1);delta=Math.max(delta,Math.abs(a1-a0));
    if(Math.hypot((u-.5)*2,(v-.5)*2)>=.96)assert.ok(a0<1e-12&&a1<1e-12);
  }
  assert.ok(highest>.004,'lapping displaces actual inherited water vertices');
  assert.ok(delta>.004,'lapping changes on ordinary environment time');
  assert.equal(lapping(.5,.5,0,[]),0,'zero island sites imply no effect');
  assert.equal(lapping(.99,.99,2,sites),0,'outside water cannot be displaced');
  a.dispose();
});

test('synthetic global calm keeps regular island/water motion; explicit pause and disposal remain effective',()=>{
  const before=JSON.stringify(bindings),a=create();
  const swamp=a.water.find(w=>w.kind==='swamp');
  a.tick(3,{storm:0});assert.equal(swamp.material.uniforms.uTime.value,3);
  a.tick(10,{storm:0});assert.equal(swamp.material.uniforms.uTime.value,10);
  a.tick(19,{storm:0,paused:true});assert.equal(swamp.material.uniforms.uTime.value,10);
  a.tick(20,{storm:0});assert.equal(swamp.material.uniforms.uTime.value,20);
  assert.equal(JSON.stringify(bindings),before);
  assert.equal(a.water.filter(w=>w.kind==='swamp').length,1);
  assert.equal(a.locations[0].group.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
  a.dispose();a.dispose();
});
