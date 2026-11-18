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

test('existing Mud Dogs tree stations, not invented canopy locations, drive five water-shade anchors',()=>{
  const before=JSON.stringify(bindings),a=build();
  const mud=a.locations.find(l=>l.id==='LOC-MUD-DOGS-SWAMP').group;
  const trunks=mud.children.filter(m=>m.userData.wetlandPart==='trunk')
    .sort((x,y)=>x.userData.wetlandStand-y.userData.wetlandStand);
  assert.equal(trunks.length,14);
  const swamp=a.water.find(w=>w.kind==='swamp');
  assert.equal(swamp.material.uniforms.uRootSiteCount.value,5);
  const sites=swamp.material.uniforms.uRootSites.value;
  assert.equal(sites.length,5);
  for(let i=0;i<5;i++){
    assert.ok(Math.abs(sites[i].x-(.5+trunks[i*3].position.x/21))<1e-6);
    assert.ok(Math.abs(sites[i].y-(.5+trunks[i*3].position.z/16.4))<1e-6);
  }
  assert.equal(swamp.mesh.geometry.getAttribute('position').count,385);
  assert.equal(swamp.mesh.geometry.getIndex().count,2160);
  assert.deepEqual([swamp.mesh.scale.x,swamp.mesh.scale.y],[10.5,8.2]);
  assert.equal(swamp.mesh.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
  assert.equal(a.worldMutationAllowed,false);
  assert.deepEqual(a.principalCharacters,[]);
  assert.deepEqual(a.locations.map(l=>l.id),bindings.map(l=>l.id));
  assert.equal(JSON.stringify(bindings),before);
  a.dispose();
});

test('one existing swamp shader gains a bounded, position-anchored, water-fragmented shade signal',()=>{
  const a=build(),swamp=a.water.find(w=>w.kind==='swamp');
  const shader=swamp.material.fragmentShader;
  assert.match(shader,/float canopyShade=0\./);
  assert.match(shader,/canopyFade=1\.-smoothstep\(1\.05,2\.50,rootDistance\)/);
  assert.match(shader,/wateryBreakup=\.5\+\.5\*sin\(delta\.x\*3\.8-uTime\*\.27\)/);
  assert.match(shader,/canopyShade=max\(canopyShade,canopyFade\*\(\.66\+\.34\*wateryBreakup\)\)/);
  assert.match(shader,/contactTint\*=1\.-\.072\*canopyShade\*bankFade/);
  assert.match(shader,/if\(float\(i\)>=uRootSiteCount\)break/);
  assert.match(shader,/rootWake=max\(rootWake,wakeFade\*wakeCrest\)/);
  assert.doesNotMatch(shader,/uniform float uStorm|uniform float uRain|uniform float uWeather/i);
  assert.equal(a.water.find(w=>w.kind==='channel').material.uniforms.uRootSiteCount.value,0,
    'existing channel must have zero canopy anchors');
  assert.ok(a.water.filter(w=>!['swamp','channel'].includes(w.kind))
    .every(w=>(w.material.uniforms.uRootSiteCount?.value??0)===0));
  assert.ok(a.water.every(w=>w.mesh.isMesh));
  a.dispose();
});

test('shade attenuation is finite and restrained, changes with the ordinary water clock, and pauses',()=>{
  const smoothstep=(lo,hi,x)=>{const t=Math.max(0,Math.min(1,(x-lo)/(hi-lo)));return t*t*(3-2*t);};
  const shade=(dx,dy,time,bankFade=1)=>{
    const r=Math.hypot(dx,dy);
    const envelope=1-smoothstep(1.05,2.50,r);
    const broken=.5+.5*Math.sin(dx*3.8-time*.27)*Math.sin(dy*4.4+time*.21);
    return 1-.072*envelope*(.66+.34*broken)*bankFade;
  };
  for(const t of [0,3,17,100])for(const offset of [[0,0],[.4,1.4],[2.5,0],[10,10]]){
    const value=shade(...offset,t);
    assert.ok(Number.isFinite(value)&&value>=.928&&value<=1);
  }
  assert.equal(shade(4,0,9),1,'outside existing candidate crown field there is no tint');
  assert.ok(Math.abs(shade(.4,1.4,2)-shade(.4,1.4,12))>1e-4,
    'ordinary water motion visibly fragments the shaded patch in time');
  const before=JSON.stringify(bindings),a=build();
  const swamp=a.water.find(w=>w.kind==='swamp'),channel=a.water.find(w=>w.kind==='channel');
  a.tick(2,{storm:0});
  assert.equal(swamp.material.uniforms.uTime.value,2);
  assert.equal(channel.material.uniforms.uTime.value,2);
  a.tick(12,{storm:0});
  assert.equal(swamp.material.uniforms.uTime.value,12);
  a.tick(20,{storm:0,paused:true});
  assert.equal(swamp.material.uniforms.uTime.value,12);
  assert.equal(channel.material.uniforms.uTime.value,12);
  assert.equal(JSON.stringify(bindings),before);
  a.dispose();
});
